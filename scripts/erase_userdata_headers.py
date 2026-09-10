#!/usr/bin/env python3
"""
erase_userdata_headers.py
Zero-fills the first 1 GB of userdata partition to force Android filesystem reformat.
Target: MTK devices with corrupted userdata causing bootloop/orange state.
Usage: Run while device is in BROM mode on USB 2.0 port.
Adapted from: RMX2193EEA (Realme Narzo 20) C.18 recovery - 2026-09-08
"""
import subprocess
import sys
import os

# === CONFIGURACIÓN - AJUSTAR SEGÚN DISPOSITIVO ===
PY = sys.executable
MTK = r"D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\mtk.py"
PRELOADER = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin"
COM = "COM9"
GPT_ARGS = ["--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128", "--sectorsize", "512"]

# Offsets de userdata (RMX2193EEA / Helio G85)
# CAMBIAR SEGÚN EL SCATTER FILE DEL DISPOSITIVO
USERDATA_START = 0x23C800000
CHUNK_SIZE = 50 * 1024 * 1024      # 50 MB por bloque
LIMIT_WIPE = 1024 * 1024 * 1024    # Solo primeros 1 GB
# === FIN CONFIG ===

def create_zero_file(path, size):
    if not os.path.exists(path):
        print(f"Creando archivo de ceros: {path}")
        with open(path, "wb") as f:
            f.write(b"\x00" * size)
    return path

def main():
    zero_file = r"D:\Usuarios\Administrador\Documents\Custom ROM\scripts\zero_50mb.bin"
    create_zero_file(zero_file, CHUNK_SIZE)

    total_written = 0
    block_num = 0
    print("=" * 60)
    print("   BORRADO RÁPIDO DE USERDATA (1 GB)")
    print("=" * 60)
    print(f"Offset inicial: {hex(USERDATA_START)}")
    print(f"Total a limpiar: {LIMIT_WIPE//(1024*1024)} MB ({LIMIT_WIPE//CHUNK_SIZE} bloques de {CHUNK_SIZE//(1024*1024)} MB)")
    print("Nota: Esto borrará las cabeceras y forzará el formateo al arrancar.")
    print()

    while total_written < LIMIT_WIPE:
        block_num += 1
        offset = USERDATA_START + total_written

        print(f"--- Bloque {block_num} / {LIMIT_WIPE//CHUNK_SIZE} ---")
        print(f"Escribiendo en: {hex(offset)}...")
        cmd = [PY, MTK, "--serialport", COM, "--preloader", PRELOADER] + GPT_ARGS + \
              ["wo", hex(offset), hex(CHUNK_SIZE), zero_file]

        result = subprocess.run(cmd)

        if result.returncode == 0:
            total_written += CHUNK_SIZE
            pct = min(100, (total_written // (LIMIT_WIPE // 100)))
            print(f"✅ Bloque {block_num} OK. Progreso: {pct}%")
        else:
            print(f"❌ Error en bloque {block_num}.")
            print("1. Desconecta y apaga el teléfono.")
            print("2. Entra de nuevo en modo BROM (Vol+ + Vol- + USB).")
            print("3. Presiona [ENTER] para reintentar este bloque...")
            input()

    print()
    print("=" * 60)
    print("   ✅ ¡BORRADO RÁPIDO COMPLETADO!")
    print("   Las cabeceras de datos han sido eliminadas.")
    print("   1. Desconecta el USB.")
    print("   2. Enciende el teléfono normalmente.")
    print("   3. Android detectará el daño y se formateará solo.")
    print("   4. Si no arranca, entra en Recovery y haz Format Data.")
    print("=" * 60)

if __name__ == "__main__":
    main()
