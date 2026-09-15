# Guía de Reparación — Boot Loop Orange State en Realme Narzo 20
## Solución definitiva para firmware C.18 / C.20

---

## ⚠️ Antes de empezar

Esta guía es para **Realme Narzo 20 (RMX2193EEA)** con chip **Helio G85/MT6768**. Los offsets y comandos pueden variar para otros modelos — adapta según tu scatter file.

**Requisitos previos:**
- ☑ Cable USB básico (no hub, no alargador)
- ☑ Puerto **USB 2.0** en tu PC (negro, NO el azul USB 3.0)
- ☑ Drivers MTK VCOM instalados
- ☑ mtkclient configurado con DA `MTK_DA_V5.bin`
- ☑ Firmware C.18 descargado y extraído

---

## 🔍 Síntomas que identifican este problema

| Síntoma | Causa |
|---------|-------|
| Boot loop rápido en logo "Realme" naranja | Datos corruptos en userdata + flags de estado del bootloader |
| WiFi y Bluetooth no funcionan | Configuración NV data dañada por mal flasheo previo |
| Entra en modo recovery pero se atasca | Partición userdata con sistema de archivos inválido |
| Muestra "Orange State" al iniciar | Bootloader desbloqueado + datos de fábrica corruptos |

---

## 🛠️ Paso 1 — Entrar en modo BROM

1. Apaga el teléfono completamente (mantén Power 20 segundos si es necesario)
2. Mantén presionados **Vol+ y Vol-** simultáneamente
3. Conecta el cable USB al puerto **USB 2.0** del PC
4. Espera a que Windows detecte el puerto COM (aparece en Administrador de dispositivos)
5. Suelta los botones

> 💡 **Importante:** Si usas USB 3.0 verás `USBError(5, 'Input/Output Error')`. Siempre usa USB 2.0.

---

## 📦 Paso 2 — Flashear particiones pequeñas

Abre una terminal y ejecuta (ajusta rutas y COM):

```bash
cd "D:\Custom ROM\00_tools\mtkclient"

python mtk.py --serialport COM9 ^
  --preloader "D:\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin" ^
  --gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512 ^
  w logo logo.bin

python mtk.py --serialport COM9 ^
  --preloader "D:\Custom ROM\01_firmware\...preloader_oppo6769.bin" ^
  --gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512 ^
  w boot boot.img

# Repite para: recovery, dtbo, lk, sec1, vbmeta, vbmeta_system
```

Cada comando requiere entrar de nuevo en BROM (reconectar USB).

---

## 📦 Paso 3 — Flashear super.img en trozos

`super.img` es muy grande (~7.2 GB). No flashee de golpe:

```bash
# Separa en trozos de 900 MB
split -b 900M super.img super_part_

# Flashea cada trozo calculando el offset desde el scatter file
# Usa el script flash_super_chunks.py incluido en esta carpeta
```

> ⚠️ **Nunca flashes boot de C.20 con super de C.18** — eso causa crash inmediato.

---

## 🧹 Paso 4 — Limpiar particiones de configuración

Esto resetea los flags de Orange State:

```bash
python mtk.py --serialport COM9 ^
  --preloader "...preloader_oppo6769.bin" ^
  --gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512 ^
  e misc

python mtk.py --serialport COM9 ^
  --preloader "...preloader_oppo6769.bin" ^
  --gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512 ^
  e cache
```

---

## 🗑️ Paso 5 — Borrar userdata (el paso clave)

**NO intentes borrar los 49 GB completos.** Solo necesitas destruir las cabeceras:

### Opción A: Usar el script incluido (recomendado)

```bash
python erase_userdata_headers.py
```

El script escribirá ceros en los primeros 1 GB de userdata en 20 bloques de 50 MB.

### Opción B: Comando manual por bloque

```bash
# Bloque 1 — offset 0x23C800000, tamaño 0x3200000 (50 MB)
python mtk.py --serialport COM9 ^
  --preloader "...preloader_oppo6769.bin" ^
  --gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512 ^
  wo 0x23C800000 0x3200000 zero_50mb.bin

# Bloque 2 — offset 0x23FA00000
python mtk.py --serialport COM9 ^
  --preloader "...preloader_oppo6769.bin" ^
  --gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512 ^
  wo 0x23FA00000 0x3200000 zero_50mb.bin

# Repite incrementando el offset en 0x3200000 hasta 0x277E00000
```

---

## 🔄 Paso 6 — Primer arranque

1. Desconecta el USB
2. Mantén presionado Power 8-10 segundos para encender
3. Verás el logo Realme → puede haber un boot loop breve
4. Si llega al recovery, selecciona **Format Data**
5. Confirma y espera (puede tardar 3-7 minutos)

> ⏳ El primer arranque después del formateo es lento. **No toques nada.**

---

## 🐛 Solución de problemas

| Error | Causa | Solución |
|-------|-------|----------|
| `USBError(5, 'Input/Output Error')` | USB 3.0 | Usa puerto USB 2.0 negro |
| `fuse library not installed` | Advertencia inofensiva | Ignorar |
| `Couldn't get device configuration` | Sesión BROM perdida | Reconectar BROM y reintentar |
| `DRAM setup failed` | DA corrupto en transferencia | Reconectar BROM, el progreso se preserva |
| Boot loop tras flashear | Mismatch firmware | Asegurar que boot + super son del mismo firmware (C.18) |
| Se atasca en logo | Userdata no formateado | Entrar en Recovery y hacer Format Data |
| `e userdata` falla | Partición demasiado grande | Usar escritura de ceros (`wo`) en trozos |

---

## 📂 Archivos incluidos

| Archivo | Propósito |
|---------|-----------|
| `flash_master.py` | Flashea particiones pequeñas |
| `erase_userdata_headers.py` | Borda userdata en headers (1 GB) |
| `format_data.py` | Borra cache y userdata con ceros |
| `erase_userdata_chunks.py` | Versión antigua con `ess` (menos confiable) |
| `zero_50mb.bin` | Archivo de datos nulos (50 MB) |
| `scatter.txt` | Offsets de particiones del dispositivo |
| `preloader_oppo6769.bin` | Preloader del firmware C.18 |

---

## 📝 Nota sobre el firmware C.18 vs C.20

El firmware **C.20 tiene un bug conocido** que mata WiFi y Bluetooth. Siempre usa **C.18** para este dispositivo. Si ya flasheaste C.20, el problema persistirá incluso después de reparar el boot loop.

---

## ✅ Resumen rápido (checklist)

- [ ] Puerto USB 2.0 conectado
- [ ] Driver MTK VCOM instalado
- [ ] Modo BROM activo (Vol+ + Vol- + USB)
- [ ] Particiones pequeñas flasheadas (logo, boot, recovery, dtbo, lk)
- [ ] `super.img` flasheada en trozos
- [ ] `misc` y `cache` limpiados
- [ ] Userdata con ceros en primeros 1 GB
- [ ] Format Data desde Recovery
- [ ] Primer arranque completado sin intervención

---
*Guía creada el 2026-09-08 basada en reparación exitosa de RMX2193EEA.*

---

## 📦 Paquete completo de reparación

Todo lo necesario está en la carpeta `solicitudes/`:

| Archivo | Qué contiene |
|---------|-------------|
| `README.md` | Resumen general + links de descarga de drivers |
| `drivers/MTK_VCOM_Drivers_README.md` | Guía detallada de instalación de drivers |
| `drivers/enlaces_descarga.md` | Links directos a drivers y herramientas |
| `scripts/erase_userdata_headers.py` | Script final para borrar userdata |
| `scripts/README_scripts.md` | Referencia rápida de todos los scripts |
| `CHECKLIST_REPARACION.md` | Checklist paso a paso imprimible |
| `registro_solicitudes.md` | Historial de esta sesión |
| `estructura_archivos.md` | Mapa de todos los archivos |

### Flujo recomendado para un usuario nuevo:

1. Leer `solicitudes/README.md`
2. Instalar drivers (ver `drivers/MTK_VCOM_Drivers_README.md`)
3. Seguir `GUIA_REPARACION_ORANGE_STATE.md`
4. Usar `CHECKLIST_REPARACION.md` para marcar progreso
5. Ejecutar `erase_userdata_headers.py` cuando llegue al Paso 5
