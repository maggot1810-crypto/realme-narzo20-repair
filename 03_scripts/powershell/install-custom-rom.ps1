# Script de Instalación - Realme 7i (RMX2193)
# Para instalar Custom ROM paso a paso

# Configuración
$adb = "C:\Users\Mgonza131\Documents\Custom ROM\00_tools\platform-tools\adb.exe"
$fastboot = "C:\Users\Mgonza131\Documents\Custom ROM\00_tools\platform-tools\fastboot.exe"

Write-Host "=== Instalación de Custom ROM - Realme 7i ===" -ForegroundColor Cyan
Write-Host "ADVERTENCIA: Esto borrará todos tus datos" -ForegroundColor Red
Write-Host "Asegúrate de tener un backup completo" -ForegroundColor Yellow

$confirm = Read-Host "¿Continuar? (s/n)"
if ($confirm -ne "s") {
    Write-Host "Cancelado" -ForegroundColor Red
    exit
}

# Paso 1: Verificar conexión
Write-Host "`n=== Paso 1: Verificando conexión ===" -ForegroundColor Cyan
& $adb devices
$device = & $adb devices | Select-String "device$"
if (-not $device) {
    Write-Host "ERROR: No se detecta ningún dispositivo" -ForegroundColor Red
    Write-Host "Verifica:" -ForegroundColor Yellow
    Write-Host "  1. Cable USB conectado" -ForegroundColor Gray
    Write-Host "  2. Depuración USB habilitada" -ForegroundColor Gray
    Write-Host "  3. Popup 'Permitir depuración USB' aprobado" -ForegroundColor Gray
    exit
}
Write-Host "  Dispositivo conectado" -ForegroundColor Green

# Paso 2: Verificar bootloader
Write-Host "`n=== Paso 2: Verificando Bootloader ===" -ForegroundColor Cyan
$locked = & $adb shell getprop ro.boot.flash.locked
if ($locked -eq "1") {
    Write-Host "  Bootloader LOCKED" -ForegroundColor Yellow
    Write-Host "  Necesitas desbloquear el bootloader primero" -ForegroundColor Yellow
    Write-Host "  Usa MTK Client o Realme Deep Testing APK" -ForegroundColor Gray
    $continue = Read-Host "¿El bootloader ya está desbloqueado? (s/n)"
    if ($continue -ne "s") {
        Write-Host "Desbloquea el bootloader y vuelve a ejecutar este script" -ForegroundColor Red
        exit
    }
} else {
    Write-Host "  Bootloader desbloqueado" -ForegroundColor Green
}

# Paso 3: Verificar firmware RUI 2
Write-Host "`n=== Paso 3: Verificando Firmware ===" -ForegroundColor Cyan
$build = & $adb shell getprop ro.build.display.id
Write-Host "  Firmware actual: $build" -ForegroundColor White

if ($build -notmatch "RUI.*2|C\.18|C\.33|C\.35") {
    Write-Host "  ADVERTENCIA: No se detecta RUI 2" -ForegroundColor Yellow
    Write-Host "  Las custom ROMs requieren RUI 2 Vendor" -ForegroundColor Yellow
    Write-Host "  Descarga LiteMod RUI-2 C.18:" -ForegroundColor Gray
    Write-Host "  https://drive.google.com/file/d/1h3P24a_IfLRT_LjA2wZOD6Dm1ypGg2Yi/view?usp=sharing" -ForegroundColor Gray
    
    $flashRUI2 = Read-Host "¿Tienes el firmware RUI 2 listo? (s/n)"
    if ($flashRUI2 -ne "s") {
        Write-Host "Descarga el firmware y vuelve a ejecutar este script" -ForegroundColor Red
        exit
    }
}

# Paso 4: Reboot a bootloader
Write-Host "`n=== Paso 4: Reboot a Bootloader ===" -ForegroundColor Cyan
& $adb reboot bootloader
Start-Sleep -Seconds 5
Write-Host "  Esperando dispositivo en fastboot..." -ForegroundColor Yellow

$maxAttempts = 10
$attempt = 0
do {
    $attempt++
    $fastbootDevices = & $fastboot devices 2>&1
    if ($fastbootDevices -match "fastboot") {
        Write-Host "  Dispositivo en fastboot" -ForegroundColor Green
        break
    }
    Write-Host "  Intento $attempt/$maxAttempts..." -ForegroundColor Gray
    Start-Sleep -Seconds 2
} while ($attempt -lt $maxAttempts)

if ($attempt -ge $maxAttempts) {
    Write-Host "ERROR: No se detecta dispositivo en fastboot" -ForegroundColor Red
    exit
}

# Paso 5: Flash vbmeta
Write-Host "`n=== Paso 5: Flash vbmeta ===" -ForegroundColor Cyan
$vbmetaPath = Read-Host "Ruta del archivo vbmeta.img (dejar vacío si no tienes)"
if ($vbmetaPath -and (Test-Path $vbmetaPath)) {
    & $fastboot --disable-verification flash vbmeta $vbmetaPath
    Write-Host "  vbmeta flash correcto" -ForegroundColor Green
} else {
    Write-Host "  Saltando flash vbmeta" -ForegroundColor Yellow
}

# Paso 6: Flash Recovery
Write-Host "`n=== Paso 6: Flash Custom Recovery ===" -ForegroundColor Cyan
$recoveryPath = Read-Host "Ruta del archivo recovery.img"
if (-not $recoveryPath -or -not (Test-Path $recoveryPath)) {
    Write-Host "ERROR: Archivo recovery no encontrado" -ForegroundColor Red
    Write-Host "Descarga TWRP desde:" -ForegroundColor Yellow
    Write-Host "https://github.com/l6174/android_recovery_realme_RMX2193/releases/download/twrp_v1/TWRP_RMX2193_Unofficial.zip" -ForegroundColor Gray
    exit
}

& $fastboot flash recovery $recoveryPath
Write-Host "  Recovery flash correcto" -ForegroundColor Green

# Paso 7: Reboot a Recovery
Write-Host "`n=== Paso 7: Reboot a Recovery ===" -ForegroundColor Cyan
& $fastboot reboot recovery
Start-Sleep -Seconds 10
Write-Host "  El teléfono debería estar en Recovery Mode" -ForegroundColor Green
Write-Host "  Sigue las instrucciones en la pantalla del teléfono" -ForegroundColor Yellow

Write-Host "`n=== Próximos Pasos (en el teléfono) ===" -ForegroundColor Cyan
Write-Host "1. En Recovery, selecciona 'Install'" -ForegroundColor White
Write-Host "2. Navega al firmware RUI 2 (si lo vas a flash)" -ForegroundColor White
Write-Host "3. Flash el firmware" -ForegroundColor White
Write-Host "4. Luego flash la Custom ROM" -ForegroundColor White
Write-Host "5. Wipe Cache/Dalvik" -ForegroundColor White
Write-Host "6. Reboot System" -ForegroundColor White

Write-Host "`n=== Instalación Iniciada ===" -ForegroundColor Green
Write-Host "Sigue las instrucciones en la pantalla del teléfono" -ForegroundColor Yellow
