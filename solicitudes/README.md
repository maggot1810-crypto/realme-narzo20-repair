# PAQUETE COMPLETO — Reparación MTK (Realme Narzo 20 / RMX2193EEA)
## Todos los drivers, herramientas y scripts necesarios

---

## 📦 Contenido del paquete

```
solicitudes/
├── README.md                          ← Este archivo
├── drivers/
│   ├── MTK_VCOM_Drivers_README.md     ← Guía de instalación de drivers
│   └── enlaces_descarga.md            ← Links directos a descargar
├── tools/
│   ├── mtkclient/                     ← Ya instalado en 00_tools
│   ├── platform-tools/                ← ADB + Fastboot (ya instalado)
│   └── TWRP_extracted/                ← Recovery (ya instalado)
├── scripts/
│   ├── erase_userdata_headers.py      ← Script FINAL (recomendado)
│   ├── erase_userdata_by_write.py     ← Versión anterior
│   ├── flash_master.py                ← Flasheo particiones pequeñas
│   └── format_data.py                 ← Interfaz interactiva
├── GUIA_REPARACION_ORANGE_STATE.md    ← Guía para usuarios
└── registro_solicitudes.md            ← Historial de esta sesión
```

---

## 🔧 Requisitos del sistema

| Requisito | Versión mínima | Notas |
|-----------|---------------|-------|
| Sistema operativo | Windows 10/11 (64-bit) | Windows 7 funciona pero requiere más configuración |
| Python | 3.11+ | Ya instalado en tu sistema |
| uv | Última versión | Ya instalado |
| Espacio en disco | 5 GB mínimo | Para firmware + herramientas |
| Puerto USB | **2.0 obligatorio** | USB 3.0 causa errores de comunicación |

---

## 🚨 PASO 1 — Instalar Drivers (CRÍTICO)

### Opción A: MTK VCOM Drivers (Recomendado)

**Descargar:** [MTK USB VCOM Drivers — TeamAndroid](https://teamandroid.com/download-mediatek-usb-vcom-drivers/)
- Paquete: `MTK_USB_All_Driver_v1.0.8.zip` (~28 MB)
- Incluye: VCOM, Preloader, CDC, ADB drivers

**Instalación manual (si no detecta automáticamente):**

1. Descomprimir el archivo ZIP
2. Ir a **Administrador de dispositivos** (`devmgmt.msc`)
3. Buscar dispositivo con triángulo amarillo bajo "Otros dispositivos"
4. Clic derecho → **Actualizar controlador** → **Buscar en mi equipo**
5. Navegar a la carpeta extraída → marcar **"Incluir subcarpetas"**
6. Seleccionar `cdc-acm.inf` o `mtk_install.inf`
7. Confirmar instalación (puede pedir excepcion de firma)

> ⚠️ **Windows 10/11 puede bloquear la instalación.** Si ves el error:
> - Presionar `Shift` mientras se hace clic en "Sí" para instalar
> - O desactivar la verificación de firma temporalmente:
>   `Configuración → Actualización y seguridad → Recuperación → Inicio avanzado → Reiniciar ahora`
>   → Solucionar problemas → Opciones avanzadas → Configuración de inicio → Reiniciar → tecla 7

### Opción B: SP Flash Tool (instala drivers automáticamente)

1. Descargar [SP Flash Tool](https://spflashtool.com/)
2. Ejecutar `Install_Driver.exe` dentro de la carpeta
3. Seguir asistente (aceptar todo)
4. Reiniciar PC si lo solicita

---

## 📱 PASO 2 — Entrar en modo BROM

```
1. Apagar el teléfono completamente
2. Mantener presionados VOL+ y VOL- simultáneamente
3. Conectar cable USB al puerto USB 2.0 del PC
4. Esperar 2-3 segundos hasta que Windows detecte el puerto COM
5. Soltar los botones
```

**Verificar en Administrador de dispositivos:**
- Expandir **Puertos (COM y LPT)**
- Debe aparecer: `MediaTek USB Port (COM9)` o similar
- Si no aparece → reinstalar drivers

---

## 🛠️ PASO 3 — Herramientas necesarias

### 3.1 mtkclient (Ya instalado)
Ubicación: `D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\`

**Comando base de prueba:**
```bash
python mtk.py --serialport COM9 --preloader "path/to/preloader.bin" printgpt
```

Si muestra la tabla de particiones → **drivers OK** ✅

### 3.2 ADB + Fastboot (Ya instalado)
Ubicación: `D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\platform-tools\`

**Probar conexión:**
```bash
adb devices
```

### 3.3 TWRP Recovery (Ya extraído)
Ubicación: `D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\TWRP_extracted\`
- `recovery.img` — Imagen lista para flashear

### 3.4 SP Flash Tool (Opcional — para backup/restauración)
Descargar de: https://spflashtool.com/
Útil para: hacer backup completo antes de flashear, o restaurar desde backup.

---

## 📋 PASO 4 — Flujo de reparación completo

### Resumen de pasos (desde cero hasta dispositivo funcionando):

1. [ ] Instalar drivers MTK VCOM
2. [ ] Entrar en modo BROM (Vol+ + Vol- + USB)
3. [ ] Verificar conexión: `python mtk.py ... printgpt`
4. [ ] Flashear particiones pequeñas (logo, boot, recovery, dtbo, lk, sec1)
5. [ ] Flashear super.img en trozos (900 MB cada uno)
6. [ ] Limpiar particiones: `e misc`, `e cache`
7. [ ] Ejecutar `erase_userdata_headers.py` (borra 1 GB de userdata)
8. [ ] Desconectar USB, encender dispositivo
9. [ ] Si no arranca: entrar en Recovery → Format Data
10. [ ] Primer arranque completo (3-7 minutos)

---

## 🔗 Enlaces de descarga

| Herramienta | Link | Tamaño estimado |
|-------------|------|----------------|
| MTK USB VCOM Drivers | https://teamandroid.com/download-mediatek-usb-vcom-drivers/ | ~28 MB |
| SP Flash Tool | https://spflashtool.com/ | ~50 MB |
| mtkclient (GitHub) | https://github.com/vvhvvh/mtkclient | ~5 MB |
| Firmware C.18 Realme Narzo 20 | Buscar en @realme community / firmware forums | ~4 GB |

---

## ⚠️ Advertencias importantes

1. **NUNCA uses USB 3.0** — Siempre usa puerto USB 2.0 (negro, no azul)
2. **NUNCA desconectes el cable durante el flasheo** — Puede brickear el dispositivo
3. **NUNCA mixes firmware de diferentes versiones** — C.18 boot + C.20 super = crash
4. **El primer arranque tarda 3-7 minutos** — No reinicies manualmente
5. **Orange State es normal** — Solo indica bootloader desbloqueado, no es error

---

## 🐛 Troubleshooting rápido

| Problema | Solución |
|----------|----------|
| Windows no detecta COM port | Reinstalar drivers MTK VCOM |
| `USBError(5)` | Cambiar a puerto USB 2.0, usar cable diferente |
| `fuse library not installed` | Ignorar — es advertencia cosmética |
| `Wrong magic` en DA | Reentrar en BROM, usar `MTK_DA_V5.bin` |
| Boot loop tras flashear | Verificar que boot + super sean de mismo firmware |
| Se atasca en logo | Entrar Recovery → Format Data |
| `e userdata` falla | Usar `erase_userdata_headers.py` en su lugar |
| Driver bloqueado por firma | Desactivar verificación de firma temporalmente |

---

## 📞 Soporte

Si tienes problemas después de seguir esta guía:
1. Documentar todos los errores vistos en la terminal
2. Verificar que el puerto COM aparece en Administrador de dispositivos
3. Confirmar que el cable USB es 2.0 y está en buen estado
4. Intentar con otro puerto USB 2.0 en el PC

---

*Paquete creado el 2026-09-08 para RMX2193EEA (Realme Narzo 20)*
*Actualizado con todo lo necesario para réplica del procedimiento*
