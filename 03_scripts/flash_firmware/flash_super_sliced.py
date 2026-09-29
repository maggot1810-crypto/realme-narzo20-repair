#!/usr/bin/env python3
"""
flash_super_sliced.py
Flashea super.img en chunks de 300MB desde BROM para RMX2193 (Helio G85).
Cada chunk se reintent indefinidamente hasta que el write sea exitoso.
Se reconecta automáticamente al detectar desconexión del dispositivo.

Uso:
  python flash_super_sliced.py

Requisitos:
  - Batería > 50%
  - Teléfono en modo BROM al iniciar (Vol+ + Vol- + USB)
  - Una vez conectado, el script maneja las reconexiones automáticamente
"""

import os
import sys
import subprocess
import time

# ── Rutas ───────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
PY = sys.executable
MTK = os.path.join(ROOT_DIR, "00_tools", "mtkclient", "mtk.py")
PRELOADER = os.path.join(ROOT_DIR, "01_firmware", "RMX2193_C.18_India", "preloader_oppo6769.bin")
SUPER_IMG = os.path.join(ROOT_DIR, "01_firmware", "RMX2193_C.18_India", "super.img")
COM = "COM7"

SUPER_PHYSICAL_OFFSET = 0x55000000
GPT_ARGS = ["--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128", "--sectorsize", "512"]

CHUNK_SIZE = 300 * 1024 * 1024   # 300 MB por chunk
FILE_SIZE = os.path.getsize(SUPER_IMG)

BAR_WIDTH = 40


# ── Barra de progreso general ──────────────────────────────────
def progress_bar(done_chunks, total_chunks, chunk_name=""):
    pct = done_chunks / total_chunks
    filled = int(BAR_WIDTH * pct)
    bar = "█" * filled + "░" * (BAR_WIDTH - filled)
    print(f"\r  [{bar}] {done_chunks}/{total_chunks} chunks | {pct*100:.1f}% "
          f"| {done_chunks * CHUNK_SIZE / 1024**2:.0f} MB/{FILE_SIZE/1024**3:.2f} GB  {chunk_name}",
          end="", flush=True)


# ── Esperar conexión BROM automática ─────────────────────────────
def wait_for_brom(timeout=120):
    """Espera automáticamente a que el dispositivo esté en BROM."""
    print("\n" + "─" * 60)
    print("  ESPERANDO CONEXIÓN BROM AUTOMÁTICAMENTE...")
    print(f"  Puerto: {COM}")
    print("  Si no detecta el dispositivo, reconecta el USB en modo BROM")
    print("  (Vol ARRIBA + Vol ABAJO + USB)")
    print("─" * 60)
    
    start = time.time()
    while time.time() - start < timeout:
        result = subprocess.run(
            [PY, MTK, "--serialport", COM, "devices"],
            capture_output=True, text=True, timeout=10
        )
        combined = result.stdout + result.stderr
        if "MT6768" in combined or "MT6769" in combined:
            print(f"  ✓ Dispositivo detectado en {COM}")
            return True
        time.sleep(2)
    
    print("  ✗ Timeout: no se detectó dispositivo")
    return False


# ── Flash de un chunk individual ────────────────────────────────
def flash_chunk(chunk_index, start_byte, size):
    temp_chunk = f"super_chunk_{chunk_index}.bin"

    with open(SUPER_IMG, "rb") as f_in, open(temp_chunk, "wb") as f_out:
        f_in.seek(start_byte)
        f_out.write(f_in.read(size))

    write_offset = hex(SUPER_PHYSICAL_OFFSET + start_byte)
    size_hex = hex(size)

    cmd = [PY, MTK, "--serialport", COM, "--preloader", PRELOADER] + GPT_ARGS + [
        "wo", write_offset, size_hex, temp_chunk
    ]

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        os.remove(temp_chunk)
        combined = r.stdout + r.stderr
        if "Wrote" in combined:
            return True, combined
        return False, combined
    except subprocess.TimeoutExpired:
        if os.path.exists(temp_chunk):
            os.remove(temp_chunk)
        return False, "TIMEOUT"
    except Exception as e:
        if os.path.exists(temp_chunk):
            os.remove(temp_chunk)
        return False, str(e)


# ── Loop principal ──────────────────────────────────────────────
def main():
    chunks = []
    current = 0
    while current < FILE_SIZE:
        size = min(CHUNK_SIZE, FILE_SIZE - current)
        chunks.append((current, size))
        current += size

    total = len(chunks)
    done = 0

    print("═" * 60)
    print("  SUPER.IMG FLASHER — CHUNKED (300MB)  |  RMX2193")
    print(f"  Total: {total} chunks  |  {FILE_SIZE/1024**3:.2f} GB")
    print("  Presiona Ctrl+C en cualquier momento para cancelar")
    print("═" * 60)

    for i, (offset, size) in enumerate(chunks):
        chunk_num = i + 1
        attempt = 0

        while True:
            attempt += 1
            progress_bar(done, total, f"| Chunk {chunk_num} intento {attempt}")
            print()

            if not wait_for_brom():
                print(f"  → Esperando conexión...")
                continue

            ok, result = flash_chunk(chunk_num, offset, size)

            if ok:
                print(f"  ✅ Chunk {chunk_num}/{total} OK  ({size/1024**2:.0f} MB)")
                done += 1
                progress_bar(done, total)
                print()
                break
            else:
                err_short = result[:120].replace("\n", " ")
                print(f"  ❌ Chunk {chunk_num} falló (intento {attempt})")
                print(f"     Error: {err_short}")
                print(f"  → Reconectando automáticamente...")
                time.sleep(3)

    print("\n" + "╔" + "═" * 58 + "╗")
    print("║         ✅ SUPER.IMG COMPLETAMENTE FLASHEADO ✅          ║")
    print("╚" + "═" * 58 + "╝")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrumpido por el usuario.")
        sys.exit(1)
