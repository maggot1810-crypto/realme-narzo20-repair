# Estructura completa del paquete de reparación

```
Custom ROM/
│
├── GUIA_REPARACION_ORANGE_STATE.md      ← Guía principal (lectura inicial)
├── RESUMEN_FLASH_C18.md                 ← Resumen técnico del flash original
│
├── 00_tools/                            ← Herramientas ya instaladas
│   ├── mtkclient/                       ← mtkclient completo
│   │   ├── mtk.py                       ← Comando principal
│   │   ├── mtkclient/
│   │   │   ├── Loader/
│   │   │   │   ├── MTK_DA_V5.bin        ← DA correcto (NO usar V6)
│   │   │   │   └── Preloader/           ← Preloaders por chipset
│   │   │   ├── payloads/
│   │   │   │   └── mt6768_payload.bin   ← Payload BROM para Helio G85
│   │   │   └── Library/
│   │   │       └── xflash/              ← Library con parches
│   │   └── ...
│   ├── platform-tools/                  ← ADB + Fastboot
│   │   ├── adb.exe
│   │   ├── fastboot.exe
│   │   └── ...
│   └── TWRP_extracted/
│       ├── recovery.img
│       └── vbmeta.img
│
├── 01_firmware/
│   └── Realme_RMX2193_C.18_Firmware_extracted/
│       ├── preloader_oppo6769.bin
│       ├── super.img
│       ├── boot.img
│       ├── recovery.img
│       ├── dtbo.img
│       ├── vbmeta.img
│       ├── scatter.txt
│       └── ...
│
├── scripts/                             ← Scripts originales (producción)
│   ├── erase_userdata_headers.py        ← Script FINAL (usar este)
│   ├── erase_userdata_by_write.py       ← Versión anterior
│   ├── erase_userdata_chunks.py         ← Versión con ess (menos confiable)
│   ├── flash_master.py                  ← Flasheo particiones pequeñas
│   ├── format_data.py                   ← Interfaz interactiva
│   └── zero_50mb.bin                    ← Archivo de ceros (50 MB)
│
└── solicitudes/                         ← Paquete completo para réplica
    ├── README.md                        ← Resumen general + links drivers
    ├── drivers/
    │   ├── MTK_VCOM_Drivers_README.md   ← Guía instalación drivers
    │   └── enlaces_descarga.md          ← Links directos descarga
    ├── scripts/
    │   ├── README_scripts.md            ← Referencia rápida scripts
    │   ├── erase_userdata_headers.py    ← Copia del script final
    │   └── flash_master.py              ← Copia del script de flash
    ├── CHECKLIST_REPARACION.md          ← Checklist imprimible
    ├── registro_solicitudes.md          ← Historial de solicitudes
    └── estructura_archivos.md           ← Mapa de archivos
```

---

## Archivos más importantes para empezar

1. **`GUIA_REPARACION_ORANGE_STATE.md`** — Guía paso a paso
2. **`solicitudes/README.md`** — Todo en uno (drivers + herramientas + scripts)
3. **`solicitudes/CHECKLIST_REPARACION.md`** — Para marcar progreso
4. **`solicitudes/scripts/erase_userdata_headers.py`** — El script clave

---

## Qué necesita el usuario antes de empezar

1. Windows 10/11 con Python 3.11+
2. Drivers MTK VCOM instalados
3. mtkclient configurado
4. Firmware C.18 descargado
5. Cable USB básico + puerto USB 2.0
