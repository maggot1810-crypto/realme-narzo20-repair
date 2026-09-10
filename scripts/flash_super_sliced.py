import os
import sys
import subprocess
import time

# Configuración de rutas
PY = sys.executable
MTK = r"D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\mtk.py"
PRELOADER = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin"
SUPER_IMG = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\super.img"
COM = "COM9"

# Offset físico de la partición 'super' en EMMC_USER (Sacado del scatter)
SUPER_PHYSICAL_OFFSET = 0x55000000 
GPT_ARGS = ["--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128", "--sectorsize", "512"]

# Dividiremos los 7.2GB en 8 trozos de ~900MB
CHUNK_SIZE = 900 * 1024 * 1024 # 900 MB
FILE_SIZE = os.path.getsize(SUPER_IMG)

def wait_for_brom():
    print("\n" + "="*60)
    print(" ENTRAR EN MODO BROM (NUEVA SESIÓN PARA CADA TROZO):")
    print(" 1. Apaga el teléfono (Power 20s).")
    print(" 2. Vol+ y Vol- presionados + Conectar USB.")
    print("="*60)
    input("Presiona [ENTER] cuando el teléfono esté conectado en COM9...")

def flash_chunk(chunk_index, start_byte, size):
    # Creamos un archivo temporal para el trozo
    temp_chunk = f"super_chunk_{chunk_index}.bin"
    print(f"\n[Slicing] Extrayendo trozo {chunk_index} ({size/1024**2:.1f} MB)...")
    
    with open(SUPER_IMG, "rb") as f_in:
        f_in.seek(start_byte)
        data = f_in.read(size)
        with open(temp_chunk, "wb") as f_out:
            f_out.write(data)
    
    # El offset de escritura es el offset base de super + el inicio del trozo
    write_offset = hex(SUPER_PHYSICAL_OFFSET + start_byte)
    
    print(f"[Flash] Escribiendo trozo {chunk_index} en offset {write_offset}...")
    cmd = [PY, MTK, "--serialport", COM, "--preloader", PRELOADER] + GPT_ARGS + ["wo", write_offset, hex(size), temp_chunk]
    
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        os.remove(temp_chunk) # Limpiar temporal
        if "Wrote" in r.stdout + r.stderr:
            print(f"✅ Trozo {chunk_index} flasheado con éxito.")
            return True
        else:
            print(f"❌ Fallo en trozo {chunk_index}:")
            print(r.stdout + r.stderr)
            return False
    except Exception as e:
        if os.path.exists(temp_chunk): os.remove(temp_chunk)
        print(f"❌ Error: {e}")
        return False

def main():
    chunks = []
    current = 0
    while current < FILE_SIZE:
        size = min(CHUNK_SIZE, FILE_SIZE - current)
        chunks.append((current, size))
        current += size

    print(f"Plan de flasheo: {len(chunks)} trozos detectados.")
    
    for i, (offset, size) in enumerate(chunks):
        success = False
        while not success:
            print(f"\n>>> PROCESANDO TROZO {i+1} de {len(chunks)} (Progreso: {offset/FILE_SIZE*100:.1f}%)")
            wait_for_brom()
            success = flash_chunk(i+1, offset, size)
            if not success:
                print("Reintentando trozo... Prepara el teléfono de nuevo.")
                time.sleep(2)
    
    print("\n" + "#"*60)
    print("  ¡TODO EL SUPER.IMG HA SIDO FLASHEADO POR PARTES!  ")
    print("#"*60)

if __name__ == "__main__":
    main()
