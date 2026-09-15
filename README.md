# Custom ROM — Realme Narzo 20 (RMX2193EEA)

## Estructura

| Directorio | Contenido |
|------------|-----------|
| `00_tools/` | mtkclient, platform-tools (adb/fastboot), TWRP extraído |
| `01_firmware/` | Firmware stock: India C.18, futura Global/EEA |
| `02_patches/` | vbmeta parcheados, boot.img patcheado para root |
| `03_scripts/` | Scripts de flasheo, wipe, y automatización |
| `04_kernel/` | Kernels custom (Moonlight, etc.) |
| `05_docs/` | Guías, logs de reparación, documentación |
| `06_audio_test/` | Archivos de prueba de audio (si aplica) |
| `solicitudes/` | Paquetes completos para réplica de reparaciones |

## Dispositivo

- **Modelo:** Realme Narzo 20
- **Codename:** RMX2193EEA
- **Chipset:** MediaTek Helio G85 (MT6768/MT6769)
- **Firmware actual:** C.19 (India IN, actualizado desde C.18)
- **Bootloader:** Desbloqueado (orange state)

## Proceso de reparación documentado

Ver `05_docs/GUIA_REPARACION_ORANGE_STATE.md` y `05_docs/RESUMEN_FLASH_C18.md`

## Siguiente paso

- Buscar firmware Global/EEA para RMX2193
- Flashear desde BROM para corregir redes venezolanas
- Root post-flash si se requiere
