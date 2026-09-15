# Resumen Flash C.18 — Realme Narzo 20 (RMX2193EEA)

## Dispositivo
- **Modelo**: Realme Narzo 20 / RMX2193EEA (EU)
- **Codename**: moon
- **SoC**: Helio G85 / MT6768
- **Storage**: EMMC 119GB (hC9aP3)
- **GPT**: 128 entries, entry size 128, sector 512
- **Bootloader**: DESBLOQUEADO (da seccfg unlock)
- **Estado actual**: Boot loop rápido en Orange State

## Problema original
- Boot loop con Orange State (WiFi/BT no funcionan)
- C.18 es el firmware que arregla WiFi/BT (C.20 tiene bug)
- Se descargó firmware C.18 y se empezó flash

## Puerto y conexión
- **Puerto COM actual**: COM7
- **USB**: PUERTO USB 2.0 OBLIGATORIO (USB 3.0 causa USBError)
- **Drivers MTK VCOM**: instalados y funcionando

## BROM entry (método del usuario)
1. Apagar teléfono completamente
2. Mantener VolUp + VolDown presionados
3. Conectar USB sin soltar teclas
4. Esperar 1-3 segundos hasta que Windows detecte COM port
5. Soltar teclas

## Comando base de mtkclient
```powershell
cd "D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient"
python mtk.py --serialport COM7 --preloader "D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin" --gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512 <COMANDO>
```

## Comandos mtkclient usados
| Comando | Ejemplo |
|---------|---------|
| Print GPT | `printgpt` |
| Write por nombre | `w vbmeta vbmeta.img` |
| Write por offset | `wo 0x53a00000 0x800000 dtbo.img` |
| Erase por nombre | `e vbmeta` |
| Erase por sector | `ess 0x20210 16384` |
| Multi-write | `w logo,md1img,tee1 logo.bin,md1img.img,tee.img` |

## Particiones YA flasheadas (C.18) ✅

| Partición | Archivo | Método | Estado |
|-----------|---------|--------|--------|
| lk | C.18 lk.img (1.1MB) | `w lk` sector 2666496 | ✅ OK |
| boot | C.18 boot.img (32MB, fstab parcheado sin AVB flags) | `w boot` sector 2674688 | ✅ OK |
| recovery | TWRP RMX2193 (102MB) | `w recovery` sector 64 | ✅ OK |
| dtbo | C.18 dtbo.img (194KB) | `wo 0x53a00000` | ✅ OK |
| vbmeta | C.18 parcheado flags=0x03 (4KB) | `w vbmeta` sector 526400 | ✅ OK |
| vbmeta_system | C.18 parcheado flags=0x03 (4KB) | `w vbmeta_system` sector 542784 | ✅ OK |
| vbmeta_vendor | C.18 parcheado flags=0x03 (4KB) | `w vbmeta_vendor` sector 559168 | ✅ OK |
| sec1 | zeros 4KB (crash counter reseteado) | `wo 0x1f800000` | ✅ OK |

## Particiones pendientes de flash ❌

| Partición | Archivo | Tamaño | Nombre en scatter |
|-----------|---------|--------|-------------------|
| **super** | super.img | **7.2GB** | super (0x55000000) |
| md1img | md1img.img | 57MB | md1img |
| tee1 | tee.img | 0.9MB | tee1 |
| scp1 | scp.img | 0.7MB | scp1 |
| sspm_1 | sspm.img | 0.5MB | sspm_1 |
| gz1 | gz.img | 2.5MB | gz1 |
| spmfw | spmfw.img | 0.04MB | spmfw |
| logo | logo.bin | 2.7MB | logo |

## Particiones que NO se necesitan flashear (ya OK o N/A)
- preloader (BOOT1) — no tocar
- pgpt/sgpt — GPT tables — no tocar
- userdata — se formatea desde recovery
- cache — se borra desde recovery
- frp, md_udc, proinfo, protect1, protect2, nvram, nvdata, persist — no flashear
- oppo_custom_* — no críticos
- opporeserve2 — no crítico
- my_custom — no crítico
- cdt_engineering — no crítico

## Offset de scatter (todos en EMMC_USER)

```
preloader:    0x00000000 (BOOT1)
recovery:     0x00008000   size 0x06200000
misc:         0x006208000  size 0x00080000
para:         0x006288000
expdb:        0x006A88000
vbmeta:       0x10108000   size 0x00800000 (patched 0x03)
vbmeta_system:0x10908000   size 0x00800000 (patched 0x03)
vbmeta_vendor:0x11108000   size 0x00800000 (patched 0x03)
md_udc:       0x11908000
nvdata:       0x16FA2000
persist:      0x1AFA2000
protect1:     0x1DFA2000
protect2:     0x1E7A2000
seccfg:       0x1F000000
sec1:         0x1F800000   size 0x00200000
proinfo:      0x1FA00000
nvram:        0x1FD00000
lk:           0x51600000   size 0x00200000
lk2:          0x51800000   size 0x00200000
boot:         0x51A00000   size 0x02000000
dtbo:         0x53A00000   size 0x00800000
tee1:         0x54200000   size 0x00500000
tee2:         0x54700000   size 0x00900000
super:        0x55000000   size 0x1CC800000 (7.2GB)
logo:         0x5FA00000   size 0x00300000
md1img:       0x60300000   size 0x03800000
spmfw:        0x67300000   size 0x00020000
scp1:         0x4E800000   size 0x00600000
scp2:         0x4EE00000   size 0x00600000
sspm_1:       0x4F400000   size 0x00100000
sspm_2:       0x4F500000   size 0x00100000
gz1:          0x4F600000   size 0x01000000
gz2:          0x50600000   size 0x01000000
cache:        0x221800000  size 0x01B000000
userdata:     0x23C800000  size 0x0C4F4F8000
```

## Hallazgos técnicos

### DA (Download Agent) — Comportamiento
- **DA usado**: mtkclient MTK_DA_V5.bin (22MB, moderno para MT6768)
- **Explotación**: Kamakiri payload (mt6768_payload.bin)
- **Inestabilidad**: ~50% de sesiones tienen "Wrong magic" al inicio → fallan operaciones
- **Patrón de éxito**: Las sesiones que NO tienen "Wrong magic" al inicio funcionan todo
- **SP Flash Tool v5.1924**: NO sirve — DA oficial (2019) no soporta MT6768 (2020)

### USB / Conexión
- **USB 3.0**: Causa USBError(5) = Input/Output Error → falla lectura GPT y write
- **USB 2.0**: Funciona correctamente para printgpt y writes
- **printgpt**: SIEMPRE funciona (lee GPT desde offset 0/sectors 1-33)
- **detect_partition**: INTERMITENTE — falla ~50% de las veces (USBError tras DA)

### Escritura — Lo que funciona y lo que no
| Método | Funciona | Notas |
|--------|----------|-------|
| `w partname file` | ✅ Cuando DA limpio | Requiere `is_download: true` en scatter |
| `wo offset length file` | ❌ Falla CC_OPTIONAL_DOWNLOAD_ACT | Aunque file OK y offset válido |
| `e partname` | ✅ Cuando DA limpio | Usa detect_partition (intermitente) |
| `ess sector count` | ⚠️ Intermitente | Escribe ceros directamente |
| `printgpt` | ✅ Siempre | Lee GPT raw |

### Boot loop — Causa
- **Boot C.18 + super C.20** → mismatch → kernel crash → reinicio rápido
- **Orange State**: Normal con bootloader desbloqueado, pero el loop es por crash
- **`phenix.uefi_to_recovery=1`**: Hardcoded en C.18 lk (offset 0xA5865), fuerza recovery
- **Recovery stock C.18**: Diferente de TWRP (hash distinto pero tamaño igual = 102MB)
- **TWRP**: No bootea probablemente por mismatch con super C.20

### Parches aplicados
- **boot.img fstab**: Se eliminaron AVB check flags del fstab
- **vbmeta*.img**: Byte en offset 88 cambiado a 0x03 (VERIFICATION_DISABLED + HASHTREE_DISABLED)
- **C.18 lk**: NO parcheado — tiene `phenix.uefi_to_recovery=1` hardcoded

## Directorios de trabajo
```
D:\Usuarios\Administrador\Documents\
├── Custom ROM\
│   ├── 00_tools\
│   │   ├── mtkclient\                          ← mtkclient (git clone)
│   │   │   ├── mtk.py                          ← script principal
│   │   │   └── mtkclient\
│   │   │       ├── Loader\MTK_DA_V5.bin        ← DA usado
│   │   │       └── Library\DA\xflash\xflash_lib.py ← patcheado line 857-858
│   │   ├── platform-tools\                      ← ADB/fastboot
│   │   └── SP_Flash_Tool_v5_1924\              ← Descargado pero NO usable (DA viejo)
│   ├── 01_firmware\
│   │   ├── Realme_RMX2193_C.18_Firmware_extracted\  ← Firmware C.18 extraído
│   │   │   ├── MT6768_Android_scatter.txt      ← Scatter file
│   │   │   ├── preloader_oppo6769.bin          ← Preloader para BROM
│   │   │   ├── super.img                       ← 7.2GB (system/vendor)
│   │   │   ├── md1img.img, tee.img, scp.img, sspm.img, gz.img, spmfw.img, logo.bin
│   │   │   └── ...otras imagenes
│   │   ├── vbmeta_full.img                     ← 8MB original (NO parcheado)
│   │   └── vbmeta_patched.img                 ← 4KB parcheado
│   └── 02_recovery\TWRP_extracted\recovery.img ← TWRP (102MB)
└── flash_c18\                                  ← STAGING para flash
    ├── vbmeta.img, vbmeta_system.img, vbmeta_vendor.img (parcheados)
    ├── recovery_stock_c18.img (stock C.18, NO flasheado aún)
    ├── logo.bin, md1img.img, tee.img, scp.img, sspm.img, gz.img, spmfw.img
    ├── zeros_4k.bin (4KB de ceros para borrado parcial)
    ├── flash_small.py (script multi-write pendientes)
    ├── one_attempt.py (script 1 intento por sesión)
    └── flash_all.txt (lista completa de comandos)
```

## Código patcheado en mtkclient
**Archivo**: `mtkclient/Library/DA/xflash/xflash_lib.py`, línea 857-858
**Cambio**: Si `get_packet_length()` retorna None, usar default `write_packet_length=0x100000`
```python
# Original:
plen = self.get_packet_length()
write_packet_size = plen.write_packet_length

# Patcheado:
plen = self.get_packet_length()
if plen is None:
    plen = type('Packetlen', (), {'write_packet_length': 0x100000, 'read_packet_length': 0x100000})()
write_packet_size = plen.write_packet_length
```

## Próximos pasos
1. Flash MULTI-PARTICIÓN de las pequeñas en UNA sesión limpia: `w logo,md1img,tee1,scp1,sspm_1,gz1,spmfw` con sus archivos correspondientes
2. Flash `super.img` C.18 (7.2GB) por BROM con `w super super.img` — tarda mucho pero es 1 sesión
3. Después de todo: desde recovery TWRP o ADB:
   - `fastboot erase misc` (si llega a fastboot)
   - Format Data desde TWRP
4. Reboot a sistema

## Notas para Hermes Agent
- El firmware C.18 extraído NO incluye `my_custom.img`, `oppo_custom_*.img`, `opporeserve2.img` que están en el scatter. Estas particiones NO son críticas para boot.
- La `recovery_stock_c18.img` (98MB) es diferente de TWRP pero mismo tamaño. No fue flasheada porque el mismatch principal es super (system/vendor).
- El GPT del teléfono está intacto — printgpt confirma todas las particiones correctas.
- **IMPORTANTE**: Cada operación de flash requiere 1 sesión BROM separada. La sesión se muere después de cada `w` exitoso o fallido.
