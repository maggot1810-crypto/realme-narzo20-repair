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

def run_mtk_cmd(action, partition):
    cmd = [PY, MTK, "--serialport", COM, "--preloader", PRELOADER] + GPT_ARGS + [action, partition]
    print(f"\n>> Ejecutando: {' '.join(cmd)}")
    try:
        # Ejecutamos permitiendo ver la salida en tiempo real
        result = subprocess.run(cmd, capture_output=False, text=False)
        return result.returncode == 0
    except Exception as e:
        print(f"Error al ejecutar: {e}")
        return False

def main():
    try:
        print("="*60)
        print("       BORRADO DE DATOS - REALME NARZO 20 (C.18)")
        print("="*60)
        print("\nINSTRUCCIONES:")
        print("1. El teléfono debe estar APAGADO.")
        print("2. Mantén presionados VOL+ y VOL-.")
        print("3. Conecta el cable USB.")
        print("4. Suelta los botones cuando escuches el sonido de conexión.")
        print("\nREQUERIMIENTO: El teléfono debe estar en modo BROM (COM9).")
        
        input("\n⏩ Presiona [ENTER] cuando el teléfono esté conectado en BROM...")

        print("\n--- Iniciando borrado de USERDATA ---")
        if run_mtk_cmd("e", "userdata"):
            print("\n✅ USERDATA borrado correctamente.")
        else:
            print("\n❌ FALLÓ el borrado de USERDATA.")

        print("\n--- Iniciando borrado de CACHE ---")
        if run_mtk_cmd("e", "cache"):
            print("\n✅ CACHE borrado correctamente.")
        else:
            print("\n❌ FALLÓ el borrado de CACHE.")

        print("\n" + "="*60)
        print("   ¡OPERACIÓN FINALIZADA!")
        print("   Si ambos dicen OK, ya puedes encender el teléfono.")
        print("="*60)

    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")
    
    input("\nPresiona [ENTER] para cerrar esta ventana...")

if __name__ == "__main__":
    main()
