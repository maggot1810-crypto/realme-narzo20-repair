#!/usr/bin/env python3
"""
flash_super_sliced.py
Flashea super.img en chunks de 300MB desde BROM para RMX2193 (Helio G85).
Cada chunk se reintent indefinidamente hasta que el write sea exitoso.
Auto-detecta puerto COM y parámetros GPT desde hwparam.json.

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
import json
import re

# ── Rutas ───────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
MTK_DIR = os.path.join(ROOT_DIR, "00_tools", "mtkclient")
MTK = os.path.join(MTK_DIR, "mtk.py")
PRELOADER = os.path.join(ROOT_DIR, "01_firmware", "RMX2193_C.18_India", "preloader_oppo6769.bin")
SUPER_IMG = os.path.join(ROOT_DIR, "01_firmware", "RMX2193_C.18_India", "super.img")
HWPARAM = os.path.join(SCRIPT_DIR, "hwparam.json")
SCATTER = os.path.join(ROOT_DIR, "01_firmware", "RMX2193_C.18_India", "MT6768_Android_scatter.txt")

SUPER_PHYSICAL_OFFSET = 0x55000000
CHUNK_SIZE = 300 * 1024 * 1024  # 300 MB por chunk

BAR_WIDTH = 40


# ── Helpers ──────────────────────────────────────────────────────

def log(msg: str) -> None:
    print(f"\n[SLICED] {msg}", flush=True)


def run_mtk(args: list, timeout: int = 120) -> tuple[int, str, str]:
    cmd = [sys.executable, MTK] + args
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)


def find_com_ports() -> list[str]:
    """Busca puertos COM asignados a dispositivos MTK (VID_0E8D) ACTUALMENTE CONECTADOS."""
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "Get-PnpDevice -PresentOnly | Where-Object {$_.FriendlyName -like '*MediaTek*'} | Select-Object -ExpandProperty FriendlyName"],
            capture_output=True, text=True, timeout=5
        )
        ports = []
        for line in result.stdout.splitlines():
            match = re.search(r'COM(\d+)', line)
            if match:
                ports.append(f"COM{match.group(1)}")
        return ports
    except Exception:
        return []


def find_mtk_brom_port() -> str | None:
    """Encuentra el puerto COM del dispositivo MTK en BROM escaneando todos los COM."""
    coms = find_com_ports()
    if not coms:
        return None
    for com in coms:
        code, out, err = run_mtk(["--serialport", com, "printgpt"], timeout=8)
        combined = out + err
        # Si devuelve GPT sin esperar reconexión, es el puerto correcto
        if code == 0 and ("partition" in combined.lower() or "gpt" in combined.lower() or "preloader" in combined.lower()):
            log(f"  ✓ Puerto BROM detectado: {com}")
            return com
        # Si hubo handshake exitoso pero falló por otra razón
        if "Wrote" in combined or "Read" in combined or "error" not in combined.lower():
            log(f"  ✓ Puerto BROM detectado: {com}")
            return com
    return None


def load_hwparam() -> dict:
    """Carga parámetros GPT desde hwparam.json o scatter."""
    if os.path.isfile(HWPARAM):
        try:
            with open(HWPARAM, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def get_gpt_args(hwparam: dict) -> list[str]:
    """Construye argumentos GPT desde hwparam.json o valores por defecto."""
    default = ["--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128", "--sectorsize", "512"]
    # Intentar leer del scatter file si hwparam no tiene los datos
    if os.path.isfile(SCATTER):
        try:
            with open(SCATTER, "r") as f:
                content = f.read()
            m_entries = re.search(r"gpt_num_part_entries[:\s]+(\d+)", content, re.IGNORECASE)
            m_size = re.search(r"gpt_part_entry_size[:\s]+(\d+)", content, re.IGNORECASE)
            m_sectorsize = re.search(r"block_size[:\s]+0x([0-9a-fA-F]+)", content, re.IGNORECASE)
            if m_entries:
                default[1] = m_entries.group(1)
            if m_size:
                default[3] = m_size.group(1)
            if m_sectorsize:
                default[5] = str(int(m_sectorsize.group(1), 16))
        except Exception:
            pass
    return default


# ── Barra de progreso ───────────────────────────────────────────

def progress_bar(done_chunks, total_chunks, chunk_name=""):
    pct = done_chunks / total_chunks if total_chunks else 0
    filled = int(BAR_WIDTH * pct)
    bar = "█" * filled + "░" * (BAR_WIDTH - filled)
    written_mb = done_chunks * CHUNK_SIZE / 1024**2
    total_gb = FILE_SIZE / 1024**3
    print(f"\r  [{bar}] {done_chunks}/{total_chunks} chunks | {pct*100:.1f}% | "
          f"{written_mb:.0f}MB/{total_gb:.2f}GB  {chunk_name}",
          end="", flush=True)


# ── Flash de un chunk individual ────────────────────────────────

def flash_chunk(com_port: str, chunk_index: int, start_byte: int, size: int,
                gpt_args: list[str]) -> tuple[bool, str]:
    temp_chunk = f"super_chunk_{chunk_index}.bin"
    try:
        with open(SUPER_IMG, "rb") as f_in, open(temp_chunk, "wb") as f_out:
            f_in.seek(start_byte)
            f_out.write(f_in.read(size))

        write_offset = hex(SUPER_PHYSICAL_OFFSET + start_byte)
        size_hex = hex(size)

        cmd = [sys.executable, MTK, "--serialport", com_port,
               "--preloader", PRELOADER, "--skipwdt"] + gpt_args + [
            "wo", write_offset, size_hex, temp_chunk
        ]

        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        combined = r.stdout + r.stderr
        if "Wrote" in combined:
            return True, combined
        return False, combined
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(temp_chunk):
            os.remove(temp_chunk)


# ── Main ─────────────────────────────────────────────────────────

def main():
    global FILE_SIZE

    if not os.path.isfile(SUPER_IMG):
        log(f"ERROR: super.img no encontrado en {SUPER_IMG}")
        sys.exit(1)

    FILE_SIZE = os.path.getsize(SUPER_IMG)
    hwparam = load_hwparam()
    gpt_args = get_gpt_args(hwparam)

    chunks = []
    current = 0
    while current < FILE_SIZE:
        size = min(CHUNK_SIZE, FILE_SIZE - current)
        chunks.append((current, size))
        current += size

    total = len(chunks)
    done = 0

    log("=" * 60)
    log(f"  SUPER.IMG FLASHER — CHUNKED (300MB)  |  RMX2193")
    log(f"  Total: {total} chunks  |  {FILE_SIZE/1024**3:.2f} GB")
    log(f"  GPT: {' '.join(gpt_args)}")
    log("  Conecta el teléfono en modo BROM (Vol+ + Vol- + USB)")
    log("  Presiona Ctrl+C para cancelar")
    log("=" * 60)

    for i, (offset, size) in enumerate(chunks):
        chunk_num = i + 1
        attempt = 0

        while True:
            attempt += 1
            progress_bar(done, total, f"| Chunk {chunk_num} intento {attempt}")
            print()

            # Auto-detectar puerto COM
            com_port = find_mtk_brom_port()
            if not com_port:
                log(f"  → Dispositivo no detectado en {com_port} — esperando reconexión...")
                time.sleep(3)
                continue

            ok, result = flash_chunk(com_port, chunk_num, offset, size, gpt_args)

            if ok:
                log(f"  ✅ Chunk {chunk_num}/{total} OK  ({size/1024**2:.0f} MB)")
                done += 1
                progress_bar(done, total)
                print()
                break
            else:
                err_short = result[:120].replace("\n", " ")
                log(f"  ❌ Chunk {chunk_num} falló (intento {attempt}): {err_short}")
                log(f"  → Reconectando automáticamente...")
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
