# Scripts — Referencia rápida

## erase_userdata_headers.py (USAR ESTE)
Script FINAL y PROBADO. Borra solo los primeros 1 GB de userdata.

```bash
python erase_userdata_headers.py
```

**Qué hace:**
- Crea `zero_50mb.bin` si no existe
- Escribe 20 bloques de 50 MB en userdata
- Muestra progreso en porcentaje
- Retry automático en errores de BROM

**Ajustar antes de usar:**
```python
COM = "COM9"                    # ← Tu puerto COM
PRELOADER = "..."               # ← Ruta al preloader de tu firmware
USERDATA_START = 0x23C800000    # ← Offset desde scatter file
```

---

## flash_master.py
Flashea particiones pequeñas en una sola sesión BROM.

```bash
python flash_master.py
```

**Particiones que flashea:**
logo, md1img, tee1, scp1, sspm_1, gz1, spmfw, lk, boot, recovery, dtbo, vbmeta, vbmeta_system, sec1

---

## format_data.py
Interfaz interactiva para limpiar misc, cache y userdata.

```bash
python format_data.py
```

**Muestra:**
- Menú con opciones
- Progreso por porcentaje
- Mensajes en español

---

## zero_50mb.bin
Archivo de 50 MB de ceros. Generado automáticamente por `erase_userdata_headers.py`.

Si necesitas recrearlo:
```bash
# Usando Python
python -c "with open('zero_50mb.bin','wb') as f: f.write(b'\x00'*52428800)"

# Usando PowerShell
cmd /c "python -c \"with open('zero_50mb.bin','wb') as f: f.write(b'\x00'*52428800)\""
```
