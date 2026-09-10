# Drivers MTK — Guía completa de instalación

## ¿Por qué son necesarios?

Los drivers MTK VCOM (Virtual COM Port) son el puente entre tu PC y el teléfono en modo BROM. Sin ellos, Windows no puede detectar el dispositivo como un puerto COM y mtkclient no puede comunicarse.

---

## 📥 Descarga oficial

| Paquete | Tamaño | Mejor para | Link |
|---------|--------|-----------|------|
| **MTK USB All Driver v1.0.8** | ~28 MB | Usuarios nuevos | https://teamandroid.com/download-mediatek-usb-vcom-drivers/ |
| **MTK Driver Auto Installer v5.2307** | ~35 MB | Quienes prefieren installer automático | Mismo link, opción 2 |
| **MT67xx Legacy Drivers** | ~20 MB | Dispositivos muy antiguos (MT67xx puro) | Mismo link, opción 3 |

> Para tu Realme Narzo 20 (Helio G85 / MT6768), el paquete **MTK USB All Driver v1.0.8** es el correcto.

---

## 🔧 Instalación paso a paso

### Método 1: Auto-installer (más fácil)

1. Descargar el paquete completo
2. Extraer el ZIP
3. Ejecutar `Auto_Installer.exe` o `Install_Driver.exe`
4. Seguir el asistente (aceptar todo)
5. Reiniciar el PC si lo pide

### Método 2: Manual desde Administrador de dispositivos

**Paso 1 — Preparar el driver:**
1. Descargar y extraer el paquete de drivers
2. Anotar la ruta donde se extrajo

**Paso 2 — Forzar instalación (sin conectar el teléfono):**
1. Abrir **Administrador de dispositivos** (`Win + X` → Administrador de dispositivos)
2. Menú **Acción** → **Agregar hardware heredado**
3. Seleccionar: **Network adapters** (adaptadores de red)
4. Clic en **Siguiente**
5. Seleccionar: **Have Disk...**
6. Navegar a la carpeta extraída y buscar:
   - `cdc-acm.inf` (para VCOM genérico)
   - O `mtk_install.inf` (para MTK específico)
7. Seleccionar el archivo → **Abrir** → **Siguiente**
8. Elegir: ` MediaTek USB Port` o `CDC ACM Device`
9. Completar instalación

**Paso 3 — Conectar el teléfono:**
1. Una vez instalado el driver, conectar el teléfono en modo BROM
2. Verificar en **Puertos (COM y LPT)** que aparece `MediaTek USB Port (COMx)`

---

## ⚠️ Problemas comunes con la firma del driver

Windows 10/11 puede bloquear la instalación porque el driver MTK **no tiene firma digital de Microsoft**.

### Solución A: Excepción durante instalación
- Cuando Windows muestre el warning de firma, hacer clic en **"Install this driver software anyway"**
- Si no aparece el botón, mantener presionada la tecla `Shift` mientras se hace clic en el botón de instalar

### Solución B: Desactivar verificación de firma (temporal)
```
1. Configuración de Windows → Actualización y seguridad
2. Recuperación → Inicio avanzado → Reiniciar ahora
3. Solucionar problemas → Opciones avanzadas → Configuración de inicio → Reiniciar
4. Presionar F7 o 7 para "Desactivar habilitación de firma de controlador"
5. Instalar los drivers normalmente
6. Reiniciar para reactivar la protección
```

### Solución C: Forzar desde PowerShell (Admin)
```powershell
# Desactivar firma temporalmente
bcdedit /set {current} nointegritychecks on
bcdedit /set {current} testsigning on

# Reiniciar e instalar drivers

# Reactivar después
bcdedit /set {current} nointegritychecks off
bcdedit /set {current} testsigning off
```

---

## ✅ Verificar que los drivers están bien instalados

### En Administrador de dispositivos:
1. Abrir `devmgmt.msc`
2. Expandir **Puertos (COM y LPT)**
3. Debe verse: `MediaTek USB Port (COM9)` (o el número que corresponda)
4. **NO debe haber triángulos amarillos**

### Probar con mtkclient:
```bash
cd "D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient"
python mtk.py --serialport COM9 --preloader "path/to/preloader.bin" printgpt
```

Si muestra una tabla con todas las particiones → **drivers funcionando** ✅

Si dice "Couldn't get device configuration" → **reiniciar instalación de drivers**

---

## 📋 Resumen de drivers requeridos

| Driver | Propósito | ¿Necesario? |
|--------|-----------|-------------|
| **MTK VCOM** | Puerto COM en modo BROM | **Obligatorio** |
| **MTK Preloader** | Detección del bootloader | **Obligatorio** |
| **ADB** | Comunicación con Android corriendo | Opcional (ya incluido en platform-tools) |
| **Fastboot** | Bootloader mode flashing | Opcional |

> Los drivers MTK VCOM y Preloader son el mismo paquete — instálalos juntos.

---

*Guía de drivers actualizada: 2026-09-08*
