import subprocess
import sys
import os

PY = sys.executable
MTK = r"D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\mtk.py"
PRELOADER = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin"
COM = "COM9"
GPT_ARGS = ["--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128", "--sectorsize", "512"]

# Offset y tamaño de userdata (según scatter oficial)
# userdata: 0x23C800000  size 0x0C4F4F8000
USERDATA_OFFSET = 0x23C800000
USERDATA_SIZE = 0xC4F4F8000

# Tamaño de bloque para borrar (ej. 1GB en sectores)
# Tamaño sector = 512 bytes. 1GB = 1024*1024*1024 / 512 = 2,097,152 sectores
CHUNK_SIZE_SECTORS = 2097152
CHUNK_SIZE_BYTES = CHUNK_SIZE_SECTORS * 512

def erase_userdata_chunks():
    total_chunks = (USERDATA_SIZE + CHUNK_SIZE_BYTES - 1) // CHUNK_SIZE_BYTES
    print(f"=== BORRANDO USERDATA POR TROZOS ===")
    print(f"Tamaño total: {USERDATA_SIZE // (1024**3)} GB + resto")
    print(f"Trozos a procesar: {total_chunks} (cada uno ~1GB, el último puede ser menor)")
    
    current_sector = USERDATA_OFFSET // 512
    end_sector = (USERDATA_OFFSET + USERDATA_SIZE) // 512
    
    chunk_num = 0
    while current_sector < end_sector:
        chunk_num += 1
        sectors_to_erase = min(CHUNK_SIZE_SECTORS, end_sector - current_sector)
        chunk_size_gb = sectors_to_erase * 512 / (1024**3)
        
        print(f"\n--- Trozo {chunk_num}/{total_chunks} ---")
        print(f"Sector inicial: {hex(current_sector)} | Tamaño: {chunk_size_gb:.2f} GB")
        
        cmd = [PY, MTK, "--serialport", COM, "--preloader", PRELOADER] + GPT_ARGS + ["ess", hex(current_sector), hex(sectors_to_erase)]
        
        print(f"Ejecutando: {' '.join(cmd)}")
        # Ejecutamos con salida en tiempo real para ver progreso
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print(f"✅ Trozo {chunk_num}/{total_chunks} completado.")
            current_sector += sectors_to_erase
        else:
            print(f"\n❌ Error en trozo {chunk_num}. Reinicia BROM para continuar.")
            input("Presiona ENTER cuando hayas reconectado el teléfono en modo BROM...")
    
    print("\n✅ ¡BORRADO DE USERDATA COMPLETADO!")

if __name__ == "__main__":
    print("Prepara el teléfono en modo BROM (Vol+ + Vol- + USB).")
    input("Presiona ENTER cuando estés en BROM...")
    erase_userdata_chunks()