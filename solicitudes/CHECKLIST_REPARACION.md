# Checklist — Reparación Realme Narzo 20 (RMX2193EEA)
## Imprimir y marcar cada paso completado

---

## 📋 Fase 0 — Preparación del equipo

- [ ] Tener Windows 10/11 instalado y actualizado
- [ ] Tener Python 3.11+ instalado (`python --version`)
- [ ] Tener `uv` instalado (`uv --version`)
- [ ] Tener mtkclient configurado en `00_tools\mtkclient\`
- [ ] Tener firmware C.18 descargado y extraído
- [ ] Tener cable USB básico (no hub, no alargador)
- [ ] Tener acceso a puerto **USB 2.0** (negro, no azul)
- [ ] Tener la guía `GUIA_REPARACION_ORANGE_STATE.md` a mano

---

## 🔧 Fase 1 — Drivers

- [ ] Descargar MTK USB VCOM Drivers desde https://teamandroid.com/download-mediatek-usb-vcom-drivers/
- [ ] Extraer el ZIP a una carpeta
- [ ] Instalar drivers:
  - [ ] Opción auto-installer: ejecutar `Auto_Installer.exe`
  - [ ] Opción manual: Administrador de dispositivos → Agregar hardware heredado
- [ ] Verificar en Administrador de dispositivos que aparece `MediaTek USB Port (COMx)`
- [ ] Probar con mtkclient: `python mtk.py --serialport COM9 printgpt`
- [ ] Si hay error de firma: seguir guía en `drivers/MTK_VCOM_Drivers_README.md`

---

## 📱 Fase 2 — Entrar en modo BROM

- [ ] Apagar el teléfono completamente (mantener Power 20s si es necesario)
- [ ] Mantener presionados Vol+ y Vol- simultáneamente
- [ ] Conectar cable USB al puerto USB 2.0
- [ ] Esperar 2-3 segundos a que Windows detecte el puerto COM
- [ ] Soltar los botones
- [ ] Verificar en Administrador de dispositivos que aparece el COM port
- [ ] El puerto debe ser estable (no debe desaparecer y reaparecer)

---

## 📦 Fase 3 — Flashear particiones pequeñas

**Usar `flash_master.py` o comandos manuales:**

- [ ] Partición `logo`
- [ ] Partición `md1img`
- [ ] Partición `tee1`
- [ ] Partición `scp1`
- [ ] Partición `sspm_1`
- [ ] Partición `gz1`
- [ ] Partición `spmfw`
- [ ] Partición `lk`
- [ ] Partición `boot`
- [ ] Partición `recovery`
- [ ] Partición `dtbo`
- [ ] Partición `vbmeta` (parcheada)
- [ ] Partición `vbmeta_system` (parcheada)
- [ ] Partición `sec1`

> Cada partición requiere entrar de nuevo en BROM.

---

## 📦 Fase 4 — Flashear super.img

- [ ] Verificar tamaño de `super.img` (~7.2 GB)
- [ ] Separar en trozos de 900 MB: `split -b 900M super.img super_part_`
- [ ] Calcular offsets desde scatter file
- [ ] Flashear trozo 1
- [ ] Flashear trozo 2
- [ ] ... repetir hasta completar
- [ ] Verificar que no hubo errores `USBError(5)`

---

## 🧹 Fase 5 — Limpiar particiones de configuración

- [ ] Ejecutar `e misc` → debe mostrar OK
- [ ] Ejecutar `e cache` → debe mostrar OK
- [ ] Ignorar errores en `para`, `expdb`, `seccfg`, `nvram` (pueden no existir)

---

## 🗑️ Fase 6 — Borrar userdata (PASO CLAVE)

- [ ] Ejecutar `python erase_userdata_headers.py`
- [ ] Esperar a que complete los 20 bloques (~10-15 minutos)
- [ ] Verificar mensaje final: `✅ ¡BORRADO RÁPIDO COMPLETADO!`
- [ ] Si hay errores, reconectar BROM y reintentar (el progreso se preserva)

---

## 🔄 Fase 7 — Primer arranque

- [ ] Desconectar el cable USB
- [ ] Mantener presionado Power 8-10 segundos para encender
- [ ] Ver logo Realme → puede haber boot loop breve
- [ ] Si llega a Recovery: seleccionar **Format Data** y confirmar
- [ ] Esperar el formateo (puede tardar varios minutos)
- [ ] Si no llega a Recovery: esperar 5 minutos más en el logo
- [ ] Primer arranque completo puede tardar 3-7 minutos
- [ ] Verificar que Android inicia correctamente
- [ ] Verificar que WiFi y Bluetooth funcionan

---

## ✅ Verificación final

- [ ] El teléfono inicia sin boot loop
- [ ] Muestra pantalla de configuración inicial (idioma, WiFi, etc.)
- [ ] WiFi funciona y puede conectarse a una red
- [ ] Bluetooth funciona y puede emparejarse
- [ ] No hay reboot inesperados
- [ ] La batería carga normalmente

---

## 🚨 Si algo falla

| Síntoma | Acción |
|---------|--------|
| No aparece COM port | Reinstalar drivers MTK VCOM |
| `USBError(5)` | Cambiar a puerto USB 2.0, probar otro cable |
| Boot loop después de flashear | Verificar que boot + super son del mismo firmware |
| Se atasca en logo | Entrar Recovery → Format Data |
| `e userdata` falla | Usar `erase_userdata_headers.py` |
| Orange State permanente | Ejecutar `e misc` de nuevo |

---

*Checklist creado: 2026-09-08*
*Para: RMX2193EEA (Realme Narzo 20, Helio G85/MT6768)*
