import subprocess
import sys
import os
import time

# Configuración de rutas
PY = sys.executable
MTK = r"D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\mtk.py"
PRELOADER = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin"
COM = "COM9"
GPT_ARGS = ["--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128", "--sectorsize", "512"]

# Configuración de borrado (Rápido: solo el primer 1GB)
USERDATA_START = 0x23C800000
CHUNK_SIZE     = 50 * 1024 * 1024  # 50 MB por bloque
LIMIT_WIPE     = 1024 * 1024 * 1024 # 1 GB total (suficiente para forzar format)

def create_zero_file(path, size):
    if not os.path.exists(path):
        print(f"Creando archivo de ceros temporales de {size // (1024*1024)} MB...")
        with open(path, "wb") as f:
            f.write(b"\x00" * size)
    return path

def main():
    zero_file = r"D:\Usuarios\Administrador\Documents\Custom ROM\scripts\zero_50mb.bin"
    create_zero_file(zero_file, CHUNK_SIZE)

    total_written = 0
    block_num = 0
    max_blocks = LIMIT_WIPE // CHUNK_SIZE
    
    print("="*60)
    print("   BORRADO RÁPIDO DE USERDATA (1 GB) - REALME NARZO 20")
    print("="*60)
    print(f"Offset inicial: 0x{USERDATA_START:X}")
    print(f"Total a limpiar: 1 GB ({max_blocks} bloques de 50 MB)")
    print("Nota: Esto borrará las cabeceras y forzará el formateo al arrancar.\n")

    while total_written < LIMIT_WIPE:
        block_num += 1
        offset = USERDATA_START + total_written

        print(f"--- Bloque {block_num} / {max_blocks} ---")
        print(f"Escribiendo en: 0x{offset:X}...")

        cmd = [PY, MTK, "--serialport", COM, "--preloader", PRELOADER] + GPT_ARGS + \
              ["wo", hex(offset), hex(CHUNK_SIZE), zero_file]

        # Ejecución permitiendo ver la salida de mtkclient en tiempo real
        result = subprocess.run(cmd)

        if result.returncode == 0:
            total_written += CHUNK_SIZE
            pct = (total_written * 100) // LIMIT_WIPE
            print(f"✅ Bloque {block_num} OK. Progreso del formateo rápido: {pct}%")
        else:
            print(f"\n❌ Error en bloque {block_num}. La sesión BROM puede haber expirado.")
            print("1. Desconecta y apaga el teléfono.")
            print("2. Entra de nuevo en modo BROM (Vol+ + Vol- + USB).")
            input("3. Presiona [ENTER] para reintentar este bloque...")

    print("\n" + "="*60)
    print("   ✅ ¡BORRADO RÁPIDO COMPLETADO!")
    print("   Las cabeceras de datos han sido eliminadas.")
    print("   1. Desconecta el USB.")
    print("   2. Enciende el teléfono normalmente.")
    print("   3. Android detectará el daño y se formateará solo.")
    print("="*60)
    input("\nPresiona [ENTER] para salir...")

if __name__ == "__main__":
    main()
