# Script de Debloating - Realme 7i (RMX2193)
# Ejecutar en PowerShell como administrador si es necesario

# Configuración
$adb = "C:\Users\Mgonza131\Documents\Custom ROM\00_tools\platform-tools\adb.exe"

# Verificar conexión
Write-Host "=== Verificando conexión ADB ===" -ForegroundColor Cyan
& $adb devices

# Lista de apps seguras para eliminar
$bloatware = @(
    # ColorOS
    "com.coloros.smartsidebar",
    "com.coloros.karaoke",
    "com.coloros.gamespace",
    "com.coloros.healthcheck",
    "com.coloros.athena",
    "com.coloros.logkit",
    "com.coloros.scenemode",
    "com.coloros.focusmode",
    "com.coloros.floatassistant",
    "com.coloros.locationproxy",
    "com.coloros.wifibackuprestore",
    "com.coloros.deepthinker",
    "com.coloros.notificationmanager",
    "com.coloros.oppoguardelf",
    "com.coloros.oppomultiapp",
    "com.coloros.sau",
    "com.coloros.exsystemservice",
    "com.coloros.compass2",
    
    # Heytap/Oppo
    "com.heytap.pictorial",
    "com.heytap.cast",
    "com.heytap.datamigration",
    "com.heytap.appplatform",
    "com.oppo.operationManual",
    "com.oppoex.afterservice",
    "com.nearme.romupdate",
    "com.nearme.statistics.rom",
    
    # Facebook
    "com.facebook.appmanager",
    "com.facebook.services",
    "com.facebook.system",
    
    # MediaTek
    "com.mediatek.batterywarning",
    "com.mediatek.capctrl.service",
    "com.mediatek.omacp",
    "com.mediatek.smartratswitch.service",
    
    # Debug/Trace
    "com.oplus.crashbox",
    "com.oplus.onetrace",
    "com.debug.loggerui",
    
    # Google Opcionales
    "com.google.android.apps.magazines",
    "com.google.android.projection.gearhead"
)

# Contadores
$exitoso = 0
$fallido = 0
$noinstalado = 0

Write-Host "`n=== Eliminando Bloatware ===" -ForegroundColor Yellow
Write-Host "Total de apps a eliminar: $($bloatware.Count)" -ForegroundColor Cyan

foreach ($app in $bloatware) {
    $result = & $adb shell pm uninstall -k --user 0 $app 2>&1
    
    if ($result -match "Success") {
        Write-Host "[OK] $app" -ForegroundColor Green
        $exitoso++
    } elseif ($result -match "not installed") {
        Write-Host "[SKIP] $app (no instalado)" -ForegroundColor DarkGray
        $noinstalado++
    } else {
        Write-Host "[FAIL] $app - $result" -ForegroundColor Red
        $fallido++
    }
}

# Resumen
Write-Host "`n=== Resumen ===" -ForegroundColor Cyan
Write-Host "Exitosos: $exitoso" -ForegroundColor Green
Write-Host "Fallidos: $fallido" -ForegroundColor Red
Write-Host "No instalados: $noinstalado" -ForegroundColor DarkGray
Write-Host "Total: $($bloatware.Count)" -ForegroundColor White

# Verificar estado del teléfono
Write-Host "`n=== Estado del Teléfono ===" -ForegroundColor Cyan
Write-Host "Batería:" -ForegroundColor Yellow
& $adb shell dumpsys battery | Select-String -Pattern "level|status|health|temperature"

Write-Host "`nPaquetes totales:" -ForegroundColor Yellow
$paquetes = & $adb shell pm list packages | Measure-Object
Write-Host "  $($paquetes.Count) paquetes" -ForegroundColor White

Write-Host "`n=== Proceso Completado ===" -ForegroundColor Green
