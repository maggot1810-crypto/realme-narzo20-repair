# Script creado: flash_orangefox_brom.py
# Ruta: D:/Usuarios/Administrador/Documents/Custom ROM/03_scripts/flash_orangefox_brom.py

# ============================================================
# USO
# ============================================================
# 1. Apaga el teléfono
# 2. Conecta USB mientras presionas Vol+ + Vol- (modo BROM)
# 3. El script detectará automáticamente
# 4. Flasheará OrangeFox-R11.3-RMX2193.img a recovery
# 5. Al terminar, reiniciará al recovery

# ============================================================
# COMANDO
# ============================================================
python "D:/Usuarios/Administrador/Documents/Custom ROM/03_scripts/flash_orangefox_brom.py"

# O con una imagen personalizada:
python "D:/Usuarios/Administrador/Documents/Custom ROM/03_scripts/flash_orangefox_brom.py" "RUTA/imagen.img"

# ============================================================
# CARACTERÍSTICAS
# ============================================================
# • Detecta automáticamente el archivo OrangeFox-R11.3-RMX2193.img
# • Espera 60s a que conectes el teléfono en BROM
# • Hasta 5 intentos con retry ante USBError
# • Timeout de 300s por comando mtk
# • Verifica dispositivo antes de flashear
# • Revisa puerto USB 2.0 obligatorio

# ============================================================
# RUTAS QUE BUSCA (en orden)
# ============================================================
# 1. D:\Usuarios\Administrador\Downloads\Telegram Desktop\OrangeFox-R11.3-RMX2193.img
# 2. Custom ROM/OrangeFox-R11.3-RMX2193.img
# 3. Custom ROM/00_tools/TWRP_extracted/recovery.img
