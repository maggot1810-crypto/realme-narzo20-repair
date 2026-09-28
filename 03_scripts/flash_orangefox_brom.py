#!/usr/bin/env python3
"""
flash_orangefox_brom.py
Flashea OrangeFox Recovery a RMX2193 desde modo BROM usando mtkclient.
Puerto USB 2.0 obligatorio. Batería > 50% recomendada.
Uso: python flash_orangefox_brom.py [path_img]
"""

import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
MTK = os.path.join(ROOT_DIR, "00_tools", "mtkclient", "mtk.py")
DEFAULT_IMG = r"D:\Usuarios\Administrador\Downloads\Telegram Desktop\OrangeFox-R11.3-RMX2193.img"
ALT_IMG = os.path.join(ROOT_DIR, "OrangeFox-R11.3_12.1-Beta-RMX2193.zip")

MAX_RETRIES = 5
RETRY_DELAY = 3  # segundos


def log(msg: str) -> None:
    print(f"[OF] {msg}")


def run_mtk(args: list[str], timeout: int = 300) -> tuple[int, str, str]:
    cmd = [sys.executable, MTK] + args
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)


def find_recovery_img() -> str:
    """Busca el .img de OrangeFox en varias rutas."""
    candidates = [
        DEFAULT_IMG,
        os.path.join(ROOT_DIR, "OrangeFox-R11.3-RMX2193.img"),
        os.path.join(ROOT_DIR, "00_tools", "TWRP_extracted", "recovery.img"),
    ]
    for path in candidates:
        if os.path.isfile(path) and os.path.getsize(path) > 50_000_000:
            log(f"IMG encontrado: {path} ({os.path.getsize(path) / 1_048_576:.1f} MB)")
            return path
    log("ERROR: No se encontró OrangeFox-R11.3-RMX2193.img")
    log(f"  Ruta buscada: {DEFAULT_IMG}")
    return ""


def check_device() -> bool:
    """Verifica que el dispositivo esté en modo BROM/preloader."""
    log("Esperando dispositivo en BROM... (Vol+ + Vol- + USB)")
    code, out, err = run_mtk(["i"], timeout=60)
    combined = out + err
    if "BROM" in combined or "Preloader" in combined or "Device detected" in combined:
        log("Dispositivo detectado en BROM/Preloader ✓")
        return True
    log("ERROR: Dispositivo no detectado en BROM después de 60s.")
    log("  Reinicia el teléfono y entra a BROM: Vol+ + Vol- + USB")
    return False


def flash_recovery(img_path: str) -> bool:
    """Flashea la imagen de recovery usando mtk.py."""
    log(f"Flasheando recovery desde: {img_path}")
    size_mb = os.path.getsize(img_path) / 1_048_576
    log(f"Tamaño: {size_mb:.1f} MB")

    for attempt in range(1, MAX_RETRIES + 1):
        log(f"Intento {attempt}/{MAX_RETRIES}...")
        code, out, err = run_mtk(["w", "recovery", img_path])
        combined = out + err

        if code == 0 and "Successfully" in combined:
            log("✓ Recovery flasheado exitosamente")
            return True

        if "USBError" in combined or "Input/Output" in combined:
            log(f"⚠ USBError en intento {attempt} — reintentando en {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
            continue

        log(f"✗ Falló intento {attempt}: {combined[:200]}")
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)

    return False


def reboot_to_recovery() -> None:
    """Reinicia y trata de entrar al recovery automáticamente."""
    log("Reiniciando al recovery...")
    run_mtk(["reboot", "recovery"])
    log("Esperando 5 segundos para que el teléfono reinicie...")
    time.sleep(5)
    log("Presiona Vol ARRIBA + Power manualmente si no entra solo.")


def main() -> int:
    log("=" * 55)
    log("  ORANGEFOX FLASHER — BROM MODE (RMX2193)")
    log("=" * 55)

    img_path = sys.argv[1] if len(sys.argv) > 1 else find_recovery_img()
    if not img_path or not os.path.isfile(img_path):
        log("No se pudo encontrar el archivo de recovery.")
        log("Usa: python flash_orangefox_brom.py <ruta_a_la_imagen.img>")
        return 1

    if not check_device():
        return 1

    success = flash_recovery(img_path)
    if not success:
        log("✗ No se pudo flashear la recovery después de varios intentos.")
        log("  Verifica: cable USB 2.0, drivers VCOM, batería > 50%.")
        return 1

    reboot_to_recovery()
    log("")
    log("✓ OrangeFox flasheado. Entra al recovery con Vol+ + Power.")
    log("  Después instala Infinity X desde el recovery.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
