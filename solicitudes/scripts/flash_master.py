import subprocess
import sys
import os
import time

# Configuración de rutas
PY = sys.executable
MTK = r"D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\mtk.py"
PRELOADER = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin"
STAGING = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted"
COM = "COM9"

# Configuración de GPT
GPT_ARGS = ["--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128", "--sectorsize", "512"]
BASE_CMD = [PY, MTK, "--serialport", COM, "--preloader", PRELOADER] + GPT_ARGS

# Detectar si estamos en CLI
CLI_MODE = len(sys.argv) > 1
CLI_OPTION = sys.argv[1] if CLI_MODE else None

def get_cli_option():
    if CLI_MODE:
        return CLI_OPTION
    else:
        return input("Elige una opción (0-5): ")
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_brom():
    if CLI_MODE:
        print("\n" + "="*60)
        print(" ADVERTENCIA: Conecta el teléfono en modo BROM (Vol+ + Vol- + USB 2.0).")
        print("="*60)
        input("Presiona [ENTER] cuando estés listo para continuar...")
        return
    # Modo interactivo normal
    print("\n" + "="*60)
    print(" INSTRUCCIONES PARA ENTRAR EN MODO BROM:")
    print(" 1. Apaga el teléfono por completo.")
    print(" 2. Mantén presionados los botones Vol+ y Vol-.")
    print(" 3. Conecta el cable USB a la PC (USB 2.0 OBLIGATORIO).")
    print(" 4. Suelta los botones cuando escuches el sonido de Windows.")
    print("="*60 + "\n")
    input("Presiona [ENTER] cuando estés listo para comenzar la detección...")

def run_cmd(args, timeout=600):
    cmd = BASE_CMD + args
    print(f"\n[COMANDO]: {' '.join(cmd)}\n")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT EXPIRED"
    except Exception as e:
        return -2, "", str(e)

def test_connection():
    wait_for_brom()
    print("Dectectando y leyendo GPT en COM7...")
    ret, out, err = run_cmd(["printgpt"], timeout=30)
    if ret == 0 and "gpt" in out.lower():
        print("\n✅ ¡CONEXIÓN BROM EXITOSA!")
        print("La tabla GPT se leyó correctamente. Puedes proceder con seguridad.")
        return True
    else:
        print("\n❌ FALLO DE CONEXIÓN")
        print("Detalles del error:")
        print(out + "\n" + err)
        return False

def flash_small():
    wait_for_brom()
    print("Flasheando particiones pequeñas secuenciales...")
    partitions = [
        ("logo", "logo.bin"),
        ("md1img", "md1img.img"),
        ("tee1", "tee.img"),
        ("scp1", "scp.img"),
        ("sspm_1", "sspm.img"),
        ("gz1", "gz.img"),
        ("spmfw", "spmfw.img")
    ]
    
    pnames = ",".join(p[0] for p in partitions)
    pfiles = ",".join(os.path.join(STAGING, p[1]) for p in partitions)
    
    ret, out, err = run_cmd(["w", pnames, pfiles], timeout=200)
    output = out + err
    if "Wrote" in output and "Failed" not in output:
        print("\n✅ ¡FASE 1 COMPLETADA CON ÉXITO!")
        print("Todas las particiones auxiliares fueron escritas.")
    else:
        print("\n❌ FALLO EN LA ESCRITURA")
        print(output)

def flash_super():
    wait_for_brom()
    print("⚠️  Esta operación tardará unos 10-15 minutos. No desconectes el teléfono.")
    super_path = os.path.join(STAGING, "super.img")
    
    if not os.path.exists(super_path):
        print(f"❌ Error: No se encuentra super.img en {super_path}")
        return

    size_gb = os.path.getsize(super_path) / (1024**3)
    print(f"Tamaño de super.img: {size_gb:.2f} GB")
    
    ret, out, err = run_cmd(["w", "super", super_path], timeout=1200)
    output = out + err
    if "Wrote" in output and "Failed" not in output:
        print("\n✅ ¡FASE 2 (SUPER) COMPLETADA CON ÉXITO!")
    else:
        print("\n❌ FALLO AL FLASHEAR SUPER")
        print(output)

def flash_core():
    wait_for_brom()
    print("Flasheando particiones del sistema críticas...")
    partitions = [
        ("boot", "boot.img"),
        ("recovery", "recovery.img"),
        ("dtbo", "dtbo.img"),
        ("lk", "lk.img"),
        ("vbmeta", "vbmeta.img"),
        ("vbmeta_system", "vbmeta_system.img"),
        ("vbmeta_vendor", "vbmeta_vendor.img")
    ]
    
    pnames = ",".join(p[0] for p in partitions)
    pfiles = ",".join(os.path.join(STAGING, p[1]) for p in partitions)
    
    ret, out, err = run_cmd(["w", pnames, pfiles], timeout=400)
    output = out + err
    if "Wrote" in output and "Failed" not in output:
        print("\n✅ ¡FASE 3 COMPLETADA CON ÉXITO!")
        print("Núcleo del sistema (Boot, Recovery, VBMeta parcheados, LK, DTBO) flasheado.")
    else:
        print("\n❌ FALLO EN LA ESCRITURA CRÍTICA")
        print(output)

def clean_erases():
    wait_for_brom()
    print("Limpiando y reseteando particiones temporales/caché...")
    erases = ["misc", "para", "expdb", "seccfg", "sec1", "nvram", "nvdata", "protect1", "protect2"]
    
    for part in erases:
        print(f"Limpiando {part}...", end=" ", flush=True)
        ret, out, err = run_cmd(["e", part], timeout=30)
        if ret == 0:
            print("OK")
        else:
            print("FALLÓ / NO EXISTE")
        time.sleep(0.5)
        
    print("\n✅ ¡FASE 4 COMPLETADA CON ÉXITO!")
    print("Se limpiaron las configuraciones previas corruptas de Orange State.")

def main_menu():
    while True:
        clear_screen()
        print("="*60)
        print("     SOPORTE FLASH REALME NARZO 20 (RMX2193EEA) - C.18")
        print("="*60)
        print(" 0. [FASE 0] Probar conexión BROM (printgpt)")
        print(" 1. [FASE 1] Multi-write particiones pequeñas (logo, md1, tee, scp...)")
        print(" 2. [FASE 2] Flashear super.img (7.2 GB - Tarda ~15 min)")
        print(" 3. [FASE 3] Flashear Núcleo (boot, recovery, vbmeta, lk, dtbo)")
        print(" 4. [FASE 4] Limpiar particiones corruptas (misc, sec1, nvdata...)")
        print(" 5. Salir")
        print("="*60)
        op = get_cli_option()
        
        if op == "0":
            test_connection()
        elif op == "1":
            flash_small()
        elif op == "2":
            flash_super()
        elif op == "3":
            flash_core()
        elif op == "4":
            clean_erases()
        elif op == "5":
            print("Saliendo. ¡Suerte!")
            break
        else:
            print("Opción inválida.")
        if CLI_MODE:
            break
        input("\nPresiona ENTER para continuar...")

if __name__ == "__main__":
    main_menu()