#!/usr/bin/env python3
"""
flash_c18_repair.py
Recupera un RMX2193 en bootloop/Orange State Flasheando C.18 completo desde BROM.
Rutas actualizadas: 01_firmware/RMX2193_C.18_India/

Uso (CLI):
  python flash_c18_repair.py          # menú interactivo
  python flash_c18_repair.py --all    # todo en uno
  python flash_c18_repair.py --small  # solo particiones pequeñas
  python flash_c18_repair.py --core   # solo boot/vbmeta/lk/dtbo
  python flash_c18_repair.py --super  # solo super.img
  python flash_c18_repair.py --erase  # wipe userdata + cache
  python flash_c18_repair.py --reboot # solo reboot

Si falla, desconecta y reconecta USB, luego reejecuta.
"""

import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
MTK = os.path.join(ROOT_DIR, "00_tools", "mtkclient", "mtk.py")
FW_DIR = os.path.join(ROOT_DIR, "01_firmware", "RMX2193_C.18_India")

MAX_RETRIES = 3
RETRY_DELAY = 3
TIMEOUT_SMALL = 120
TIMEOUT_CORE = 300
TIMEOUT_SUPER = 900
TIMEOUT_ERASE = 60


# ── Helpers ──────────────────────────────────────────────────────

def log(msg: str) -> None:
    print(f"\n[REPAIR] {msg}", flush=True)


def run_mtk(args: list[str], timeout: int = 120) -> tuple[int, str, str]:
    cmd = [sys.executable, MTK] + args
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)


def mtk_w(partition: str, img_path: str, timeout: int = 300) -> bool:
    """Flashea una partición con reintentos."""
    for attempt in range(1, MAX_RETRIES + 1):
        log(f"  Partición '{partition}' [{attempt}/{MAX_RETRIES}]")
        code, out, err = run_mtk(["w", partition, img_path], timeout=timeout)
        combined = (out + err).lower()
        if code == 0 and "wrote" in combined and "failed" not in combined:
            log(f"  ✓ '{partition}' OK")
            return True
        if "usberror" in combined or "input/output" in combined:
            log(f"  ⚠ USBError — reintentando en {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
            continue
        log(f"  ✗ Falló: {combined[:200]}")
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)
    log(f"  ✗ '{partition}' falló después de {MAX_RETRIES} intentos")
    return False


def mtk_e(partition: str, timeout: int = 60) -> bool:
    """Borra una partición con reintentos."""
    for attempt in range(1, MAX_RETRIES + 1):
        code, out, err = run_mtk(["e", partition], timeout=timeout)
        combined = (out + err).lower()
        if code == 0:
            log(f"  ✓ '{partition}' borrado")
            return True
        if "usberror" in combined or "input/output" in combined:
            log(f"  ⚠ USBError — reintentando en {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
            continue
        # Partición puede no existir — eso está bien
        if "no such" in combined or "not found" in combined:
            log(f"  - '{partition}' no existe (ignorado)")
            return True
        log(f"  ✗ '{partition}' falló: {combined[:200]}")
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)
    return False


def detect_brom(timeout: int = 60) -> bool:
    """Espera y verifica conexión BROM."""
    log("Esperando dispositivo en BROM... (Vol+ + Vol- + USB)")
    code, out, err = run_mtk(["i"], timeout=timeout)
    combined = (out + err).lower()
    if "brom" in combined or "device detected" in combined or "preloader" in combined:
        log("✓ Dispositivo detectado en BROM")
        return True
    log("✗ Dispositivo no detectado. Verifica conexión BROM.")
    log("  Apaga el teléfono → Vol+ + Vol- + USB → conecta a USB 2.0")
    return False


# ── Fases de flasheo ─────────────────────────────────────────────

def flash_small() -> bool:
    log("═══ FASE 1: Particiones pequeñas ═══")
    small = [
        ("logo",      "logo.bin"),
        ("md1img",    "md1img.img"),
        ("tee",       "tee.img"),
        ("scp",       "scp.img"),
        ("sspm",      "sspm.img"),
        ("gz",        "gz.img"),
        ("spmfw",     "spmfw.img"),
    ]
    ok = True
    for part, filename in small:
        path = os.path.join(FW_DIR, filename)
        if not os.path.isfile(path):
            log(f"  ✗ No encontrado: {filename}")
            ok = False
            continue
        if not mtk_w(part, path, timeout=TIMEOUT_SMALL):
            ok = False
    return ok


def flash_core() -> bool:
    log("═══ FASE 2: Núcleo del sistema ═══")
    core = [
        ("boot",             "boot.img"),
        ("recovery",         "recovery.img"),
        ("dtbo",             "dtbo.img"),
        ("lk",               "lk.img"),
        ("vbmeta",           "vbmeta.img"),
        ("vbmeta_system",    "vbmeta_system.img"),
        ("vbmeta_vendor",    "vbmeta_vendor.img"),
    ]
    ok = True
    for part, filename in core:
        path = os.path.join(FW_DIR, filename)
        if not os.path.isfile(path):
            log(f"  ✗ No encontrado: {filename}")
            ok = False
            continue
        if not mtk_w(part, path, timeout=TIMEOUT_CORE):
            ok = False
    return ok


def flash_super() -> bool:
    log("═══ FASE 3: Super partition (~7.2 GB) ═══")
    super_path = os.path.join(FW_DIR, "super.img")
    if not os.path.isfile(super_path):
        log(f"✗ super.img no encontrado en {FW_DIR}")
        return False
    size_gb = os.path.getsize(super_path) / (1024 ** 3)
    log(f"Tamaño: {size_gb:.2f} GB — esto puede tardar ~10-15 minutos")
    ok = mtk_w("super", super_path, timeout=TIMEOUT_SUPER)
    if ok:
        log("✓ Super partición flasheada correctamente")
    else:
        log("✗ Fallo al flashear super — necesitas repetir este paso")
    return ok


def flash_erases() -> bool:
    log("═══ FASE 4: Wipe de particiones corruptas ═══")
    parts = ["userdata", "cache", "misc", "para", "expdb", "seccfg",
             "sec1", "nvram", "nvdata", "protect1", "protect2"]
    ok = True
    for part in parts:
        if not mtk_e(part, timeout=TIMEOUT_ERASE):
            ok = False
    return ok


def reboot() -> None:
    log("═══ FASE 5: Reiniciar ═══")
    run_mtk(["reboot"])
    log("✓ Teléfono reiniciando... espera 5-10 minutos en el primer boot")


# ── Menú interactivo ─────────────────────────────────────────────

MENU = """
═══════════════════════════════════════════════════════════
  REALME NARZO 20 (RMX2193) — REPARACIÓN C.18 BROM MODE
═══════════════════════════════════════════════════════════
  1  Particiones pequeñas  (logo, md1, tee, scp, sspm, gz)
  2  Núcleo del sistema    (boot, recovery, lk, dtbo, vbmeta)
  3  Super partition       (~7.2 GB — requiere ~15 min)
  4  Wipe userdata + cache
  5  Reiniciar
  A  TODO EN UNO          (1→2→3→4→5)
  E  SALIR
═══════════════════════════════════════════════════════════
"""


def main_menu():
    while True:
        print(MENU, flush=True)
        choice = input("Elige opción: ").strip().upper()

        if choice == "E":
            print("Saliendo.")
            return
        elif choice == "A":
            if not do_all():
                print("\n⚠ Algunas fases fallaron. Revisa los mensajes arriba.")
            else:
                print("\n✓ Reparación completada. El teléfono debería arrancar.")
            return
        elif choice == "1":
            detect_brom() and flash_small()
        elif choice == "2":
            detect_brom() and flash_core()
        elif choice == "3":
            detect_brom() and flash_super()
        elif choice == "4":
            detect_brom() and flash_erases()
        elif choice == "5":
            detect_brom() and reboot()
        else:
            print("Opción inválida.")


def do_all() -> bool:
    """Ejecuta todas las fases en secuencia."""
    if not detect_brom():
        return False
    ok = True
    ok &= flash_small()
    ok &= flash_core()
    ok &= flash_super()
    ok &= flash_erases()
    if ok:
        reboot()
    return ok


# ── CLI directo ──────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--all" in args:
        do_all()
    elif "--small" in args:
        detect_brom() and flash_small()
    elif "--core" in args:
        detect_brom() and flash_core()
    elif "--super" in args:
        detect_brom() and flash_super()
    elif "--erase" in args:
        detect_brom() and flash_erases()
    elif "--reboot" in args:
        detect_brom() and reboot()
    else:
        main_menu()
