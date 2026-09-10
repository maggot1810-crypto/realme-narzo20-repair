# Enlaces de descarga — Drivers y herramientas MTK

## Drivers (obligatorios)

### MTK USB VCOM Drivers — Más confiable
- **TeamAndroid** (recomendado): https://teamandroid.com/download-mediatek-usb-vcom-drivers/
  - Paquete: `MTK_USB_All_Driver_v1.0.8.zip`
  - Incluye: VCOM, Preloader, CDC, ADB
  - Compatible: Windows 10/11, 32 y 64 bits

### MTK Driver Auto Installer
- **TechLatest**: https://tech-latest.com/download-mediatek-usb-vcom-drivers-windows
  - Versión 2026
  - Paquete: `Windows_10_MTK_VCOM_USB_Preloader_Drivers.7z`
  - Tamaño: ~28 KB (driver suelto)

### Legacy Drivers (solo si los anteriores fallan)
- **MT65xx** (dispositivos muy viejos): https://androiddrivers.net/drivers/mediatek-usb-vcom-driver-windows
- **MT67xx** (tu caso — Helio G85/MT6768): Mismo link, opción 4

---

## Herramientas de flasheo

### mtkclient (ya instalado)
- GitHub: https://github.com/vvhvvh/mtkclient
- README instalación: https://github.com/vvhvvh/mtkclient/blob/master/README-INSTALL.md
- Ubicación actual: `D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\`

### SP Flash Tool (para backup/restauración)
- Web oficial comunitaria: https://spflashtool.com/
- También: https://baidupan.ml/spflashtool/
- Incluye driver installer automático

### ADB + Fastboot (ya instalado)
- Google: https://developer.android.com/tools/platform-tools
- Ubicación actual: `D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\platform-tools\`

---

## Firmware Realme Narzo 20 (RMX2193EEA)

### Firmware C.18 (el correcto — sin bug WiFi/BT)
- Buscar en: https://www.firmwarefinder.com/realme-narzo-20-rmx2193/
- O: https://fw-update.com/search/?s=RMX2193
- Version: C.18 (no C.20 — ese tiene bug de WiFi)

### Firmware C.20 (evitar — tiene bug)
- Si ya lo tienes, reemplazar por C.18

---

## Scripts útiles (ya creados)

| Script | Propósito | Ubicación |
|--------|-----------|-----------|
| `erase_userdata_headers.py` | Borrar 1 GB headers userdata | `solicitudes/scripts/` |
| `flash_master.py` | Flashear particiones pequeñas | `scripts/` |
| `format_data.py` | Wipe cache + userdata interactivo | `scripts/` |
| `zero_50mb.bin` | Archivo de ceros (50 MB) | `scripts/` |

---

## Recursos adicionales

- **mtkclient wiki**: https://github.com/vvhvvh/mtkclient/wiki
- **Forum XDA Realme Narzo 20**: https://forum.xda-developers.com/c/realme-narzo-20.12553/
- **Guía de scatter files**: Ver `references/scatter_interpretation.md` en skill mtk-flash
