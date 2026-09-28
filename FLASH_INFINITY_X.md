# Flash Project Infinity X 3.10 (Android 14) - RMX2193
# Creado: 2026-09-28 | Requiere: OrangeFox o PBRP + BROM de respaldo

# ============================================================
# PREPARACIÓN PREVIA
# ============================================================
# • Batería > 50%
# • Cable USB 2.0 (NO USB 3.0)
# • Tener el ZIP en la PC y listo para copiar


# ============================================================
# PASO 1: Copiar archivos al teléfono
# ============================================================
adb devices
adb push "D:/Usuarios/Administrador/Documents/Custom ROM/Project_Infinity-X-3.10-MONET-04.05.2026-VANILLA-UNOFFICIAL.zip" /sdcard/Download/
adb push "D:/Usuarios/Administrador/Documents/Custom ROM/OrangeFox-R11.3_12.1-Beta-RMX2193.zip" /sdcard/Download/
adb shell ls -la /sdcard/Download/


# ============================================================
# PASO 2: Flashear OrangeFox desde BROM (MÉTODO SEGURO)
# ============================================================
# Apagar teléfono, conectar en BROM (Vol+ + Vol- + USB → COM9)

python "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/mtkclient/mtk.py" w recovery "D:/Usuarios/Administrador/Downloads/Telegram Desktop/OrangeFox-R11.3-RMX2193.img"

# Si falla, alternativa con fastboot:
# adb reboot bootloader
# fastboot flash recovery "D:/Usuarios/Administrador/Downloads/Telegram Desktop/OrangeFox-R11.3-RMX2193.img"
# fastboot reboot recovery

# Después del paso 2, NO encender el teléfono


# ============================================================
# PASO 3: Entrar a OrangeFox Recovery
# ============================================================
# Botones: Vol ARRIBA + Power hasta que aparezca el recovery


# ============================================================
# PASO 4: Wipes desde Recovery
# ============================================================
# Desde la UI de OrangeFox:
# 1. Wipe -> Factory Reset -> Swipe to Wipe
# 2. Advanced Wipe -> System, Data, Cache, Dalvik/ART Cache -> Swipe
# 3. Volver al menú principal


# ============================================================
# PASO 5: Instalar Infinity X
# ============================================================
# Método 1 (desde UI):
# Install -> seleccionar /sdcard/Download/Project_Infinity-X-3.10-...zip -> Swipe

# Método 2 (desde ADB sideload):
adb sideload "/d/Usuarios/Administrador/Documents/Custom ROM/Project_Infinity-X-3.10-MONET-04.05.2026-VANILLA-UNOFFICIAL.zip"


# ============================================================
# PASO 6: Post-instalación
# ============================================================
# Opcional: Instalar GApps (NeonGApps arm64 Android 14)
# adb push <gapps-zip> /sdcard/Download/
# Desde recovery: Install -> GApps.zip -> Swipe

# Wipe cache final
# Reboot -> System

# Primer boot puede tardar 10-15 minutos


# ============================================================
# PASO 7: SI FALLA — Volver a C.19 desde BROM
# ============================================================
# Entrar a BROM (Vol+ + Vol- + USB)

python "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/mtkclient/mtk.py" w boot "D:/Usuarios/Administrador/Documents/Custom ROM/01_firmware/RMX2193_C.18_India/boot.img"
python "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/mtkclient/mtk.py" w recovery "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/TWRP_extracted/vbmeta.img"
python "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/mtkclient/mtk.py" w vbmeta "D:/Usuarios/Administrador/Documents/Custom ROM/01_firmware/RMX2193_C.18_India/vbmeta.img"
python "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/mtkclient/mtk.py" w super "D:/Usuarios/Administrador/Documents/Custom ROM/01_firmware/RMX2193_C.18_India/super.img"
python "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/mtkclient/mtk.py" e userdata
python "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/mtkclient/mtk.py" e cache
python "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/mtkclient/mtk.py" reboot


# ============================================================
# NOTAS
# ============================================================
# • El teléfono debe estar EN BROM para usar mtk.py
# • Usar USB 2.0 (puerto USB 2.0 del PC)
# • Si Infinity X no arranca después del primer boot, repetir wipe
# • La primera vez puede tardar 10-15 min en arrancar
# • Si hay bootloop, volver a C.19 con Paso 7
# • GApps opcionales: NeonGApps arm64 Android 14
# • Las particiones system/vendor/product/system_ext están DENTRO de super.img
#   por eso solo se flasea super.img completo
