# Proceso exitoso — Realme Narzo 20 (RMX2193EEA) C.18
# Fecha: 2026-09-08
# Objetivo: Reparar boot loop Orange State + WiFi/BT muertos

## Síntoma original
- Boot loop en logo Realme (Orange State)
- WiFi y Bluetooth no funcionan
- Firmware C.20 tenía bug; se reinstaló C.18 stock

## Dispositivo
- Modelo: RMX2193EEA (EU)
- SoC: Helio G85 / MT6768
- EMMC: hC9aP3, USER Size 0xe8f800000 (~58 GB)
- GPT: 128 entradas, 128 bytes cada una, sector 512

## Pasos ejecutados
1. Entrada BROM: Vol+ + Vol- + USB → COM9
2. Flash particiones pequeñas (logo, md1img, tee1, scp1, sspm_1, gz1, spmfw)
3. Flash super.img en chunks de 900 MB (7.2 GB total)
4. Flash boot, recovery stock, dtbo, vbmeta parcheado, lk
5. Wipe misc → OK (para resetear Orange State flags)
6. Wipe cache → OK (432 MB)
7. Zero-fill userdata primeros 1 GB (20 bloques de 50 MB) → OK
8. Boot → Recovery Realme → Format Data → Android inicia normal

## Comandos clave
```bash
# Comando base
python mtk.py --serialport COM9 \
  --preloader "D:\...\preloader_oppo6769.bin" \
  --gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512 \
  <comando>

# Escribir ceros en userdata (primer 1 GB)
python mtk.py --serialport COM9 --preloader <preloader> \
  --gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512 \
  wo 0x23C800000 0x3200000 zero_50mb.bin
# Repetir con offset incrementado en 0x3200000 hasta 0x277E00000
```

## Offset userdata
- Inicio: 0x23C800000
- Tamaño: 0xC4F4F8000 (~49.24 GB)
- Solo se escribieron ceros en los primeros 1 GB (hasta 0x277E00000)

## Solución final
El dispositivo arrancó a Android completamente funcional después de:
1. Ceros en headers de userdata (script de 20 bloques)
2. Format Data desde Recovery UI de Realme

Tiempo total de reparación: ~2 horas incluyendo flasheo.
