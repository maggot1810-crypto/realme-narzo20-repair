# Script de Backup - Realme 7i (RMX2193)
# Ejecutar antes de hacer cambios al sistema

# Configuración
$adb = "C:\Users\Mgonza131\Documents\Custom ROM\00_tools\platform-tools\adb.exe"
$backupDir = "C:\Users\Mgonza131\Documents\Custom ROM\backups\$(Get-Date -Format 'yyyy-MM-dd_HHmmss')"

# Crear directorio de backup
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

Write-Host "=== Backup de Realme 7i ===" -ForegroundColor Cyan
Write-Host "Directorio: $backupDir" -ForegroundColor Yellow

# Verificar conexión
Write-Host "`n=== Verificando conexión ===" -ForegroundColor Cyan
& $adb devices

# Info del dispositivo
Write-Host "`n=== Info del Dispositivo ===" -ForegroundColor Cyan
$model = & $adb shell getprop ro.product.model
$build = & $adb shell getprop ro.build.display.id
$android = & $adb shell getprop ro.build.version.release
Write-Host "Modelo: $model" -ForegroundColor White
Write-Host "Build: $build" -ForegroundColor White
Write-Host "Android: $android" -ForegroundColor White

# Guardar info del dispositivo
DeviceInfo = @{
    Model = $model
    Build = $build
    Android = $android
    Date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}
$DeviceInfo | Out-File "$backupDir\device-info.txt"

# Backup de apps instaladas
Write-Host "`n=== Backup de Lista de Apps ===" -ForegroundColor Cyan
& $adb shell pm list packages > "$backupDir\packages.txt"
& $adb shell pm list packages -3 > "$backupDir\packages-third-party.txt"
& $adb shell pm list packages -s > "$backupDir\packages-system.txt"
Write-Host "  Lista de apps guardada" -ForegroundColor Green

# Backup de configuración
Write-Host "`n=== Backup de Configuración ===" -ForegroundColor Cyan

# Settings globales
& $adb shell settings list global > "$backupDir\settings-global.txt" 2>&1
& $adb shell settings list secure > "$backupDir\settings-secure.txt" 2>&1
& $adb shell settings list system > "$backupDir\settings-system.txt" 2>&1
Write-Host "  Configuración guardada" -ForegroundColor Green

# Backup de propiedades del sistema
Write-Host "`n=== Backup de System Properties ===" -ForegroundColor Cyan
& $adb shell getprop > "$backupDir\system-properties.txt"
Write-Host "  Propiedades guardadas" -ForegroundColor Green

# Backup de batería
Write-Host "`n=== Backup de Info de Batería ===" -ForegroundColor Cyan
& $adb shell dumpsys battery > "$backupDir\battery-info.txt"
Write-Host "  Info de batería guardada" -ForegroundColor Green

# Backup de particiones (si bootloader está desbloqueado)
Write-Host "`n=== Verificando Bootloader ===" -ForegroundColor Cyan
$bootloader = & $adb shell getprop ro.boot.flash.locked
if ($bootloader -eq "0") {
    Write-Host "  Bootloader desbloqueado - Backup de particiones disponible" -ForegroundColor Green
    
    # Backup de boot y recovery
    & $adb pull /dev/block/by-name/boot "$backupDir\boot.img" 2>&1
    & $adb pull /dev/block/by-name/recovery "$backupDir\recovery.img" 2>&1
    & $adb pull /dev/block/by-name/vbmeta "$backupDir\vbmeta.img" 2>&1
    Write-Host "  Particiones backupadas" -ForegroundColor Green
} else {
    Write-Host "  Bootloader locked - Backup de particiones no disponible" -ForegroundColor Yellow
}

# Backup de archivos importantes del usuario
Write-Host "`n=== Backup de Archivos del Usuario ===" -ForegroundColor Cyan
& $adb pull /sdcard/DCIM "$backupDir\DCIM" 2>&1
& $adb pull /sdcard/Download "$backupDir\Download" 2>&1
& $adb pull /sdcard/Documents "$backupDir\Documents" 2>&1
Write-Host "  Archivos del usuario backupados" -ForegroundColor Green

# Resumen
Write-Host "`n=== Resumen del Backup ===" -ForegroundColor Cyan
Write-Host "Directorio: $backupDir" -ForegroundColor Yellow
Write-Host "Archivos backupados:" -ForegroundColor White

Get-ChildItem -Path $backupDir -Recurse | ForEach-Object {
    Write-Host "  $($_.FullName.Replace($backupDir, '.'))" -ForegroundColor Gray
}

Write-Host "`n=== Backup Completado ===" -ForegroundColor Green
Write-Host "Guarda este directorio en un lugar seguro:" -ForegroundColor Yellow
Write-Host $backupDir -ForegroundColor White
