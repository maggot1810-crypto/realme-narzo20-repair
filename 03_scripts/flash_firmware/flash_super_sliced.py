#!/usr/bin/env python3
"""
flash_super_sliced.py
Flashea super.img en chunks de 500MB desde BROM para RMX2193 (Helio G85).
Cada chunk se reintent indefinidamente hasta que el write sea exitoso.

Uso:
  python flash_super_sliced.py

Requisitos:
  - Cable USB 2.0 obligatorio
  - Batería > 50%
  - Telefonos en modo BROM (Vol+ + Vol- + USB) cuando el script lo pida
"""

import os
import sys
import subprocess
import time

# ── Rutas ───────────────────────────────────────────────────────
PY = sys.executable
MTK = r"D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\mtk.py"
PRELOADER = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\RMX2193_C.18_India\preloader_oppo6769.bin"
SUPER_IMG = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\RMX2193_C.18_India\super.img"
COM = "COM5"

SUPER_PHYSICAL_OFFSET = 0x55000000
GPT_ARGS = ["--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128", "--sectorsize", "512"]

CHUNK_SIZE = 300 * 1024 * 1024   # 300 MB por chunk — balance velocidad/estabilidad USB 3.0
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


# ── Esperar conexión BROM ───────────────────────────────────────
def wait_for_brom():
    print("\n" + "─" * 60)
    print("  CONECTAR TELÉFONO EN MODO BROM:")
    print("  1. Apagar teléfono (Power 10s)")
    print("  2. Vol ARRIBA + Vol ABAJO + USB conectado (mantener)")
    print("  3. Presionar ENTER cuando la terminal detecte el dispositivo")
    print("─" * 60)
    input("Presiona [ENTER] cuando esté conectado...")


# ── Flash de un chunk individual ────────────────────────────────
def flash_chunk(chunk_index, start_byte, size):
    temp_chunk = f"super_chunk_{chunk_index}.bin"

    # Extraer chunk del super.img
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
        os.remove(temp_chunk)  # limpiar temporal
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
    # Construir lista de chunks
    chunks = []
    current = 0
    while current < FILE_SIZE:
        size = min(CHUNK_SIZE, FILE_SIZE - current)
        chunks.append((current, size))
        current += size

    total = len(chunks)
    done = 0

    print("═" * 60)
    print("  SUPER.IMG FLASHER — CHUNKED (500MB)  |  RMX2193")
    print(f"  Total: {total} chunks  |  {FILE_SIZE/1024**3:.2f} GB")
    print("  Presiona Ctrl+C en cualquier momento para cancelar")
    print("═" * 60)

    for i, (offset, size) in enumerate(chunks):
        chunk_num = i + 1
        attempt = 0

        while True:
            attempt += 1
            progress_bar(done, total, f"| Chunk {chunk_num} intento {attempt}")
            print()  # nueva línea después del progress bar

            wait_for_brom()
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
                print(f"  → Reconecta en BROM y presiona ENTER para reintentar...")
                input()  # pausa hasta que el usuario conecte y presione ENTER

    print("\n" + "╔" + "═" * 58 + "╗")
    print("║         ✅ SUPER.IMG COMPLETAMENTE FLASHEADO ✅          ║")
    print("╚" + "═" * 58 + "╝")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrumpido por el usuario.")
        sys.exit(1)
