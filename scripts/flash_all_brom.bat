@echo off
echo ============================================
echo   FLASH C.18 - BAT (lk ya hecho, 26 ops)
echo ============================================
echo.
echo Cada paso = 1 BROM:
echo   1. Apaga telefono (Power 20s, suelta, espera 5s)
echo   2. VolUp+VolDown+junto
echo   3. Mete USB
echo   4. ENTER aqui
echo.
echo Si falla el exploit: reconecta BROM y ENTER otra vez.
echo.

cd /d "D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient"
set PL=--preloader "D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin"
set GPT=--gpt-num-part-entries 128 --gpt-part-entry-size 128 --sectorsize 512
set D=D:\Usuarios\Administrador\Documents\flash_c18

:lk2
echo [1/26] w lk2
pause
python mtk.py --serialport COM7 %PL% %GPT% w lk2 %D%\lk.img
if %ERRORLEVEL% NEQ 0 (echo FALLO - reconecta BROM y ENTER) & goto lk2

:boot
echo [2/26] w boot
pause
python mtk.py --serialport COM7 %PL% %GPT% w boot %D%\boot.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto boot

:dtbo
echo [3/26] w dtbo
pause
python mtk.py --serialport COM7 %PL% %GPT% w dtbo %D%\dtbo.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto dtbo

:vbmeta
echo [4/26] w vbmeta
pause
python mtk.py --serialport COM7 %PL% %GPT% w vbmeta %D%\vbmeta.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto vbmeta

:vbs
echo [5/26] w vbmeta_system
pause
python mtk.py --serialport COM7 %PL% %GPT% w vbmeta_system %D%\vbmeta_system.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto vbs

:vbv
echo [6/26] w vbmeta_vendor
pause
python mtk.py --serialport COM7 %PL% %GPT% w vbmeta_vendor %D%\vbmeta_vendor.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto vbv

:md1
echo [7/26] w md1img
pause
python mtk.py --serialport COM7 %PL% %GPT% w md1img %D%\md1img.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto md1

:scp1
echo [8/26] w scp1
pause
python mtk.py --serialport COM7 %PL% %GPT% w scp1 %D%\scp.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto scp1

:scp2
echo [9/26] w scp2
pause
python mtk.py --serialport COM7 %PL% %GPT% w scp2 %D%\scp.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto scp2

:sspm1
echo [10/26] w sspm_1
pause
python mtk.py --serialport COM7 %PL% %GPT% w sspm_1 %D%\sspm.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto sspm1

:sspm2
echo [11/26] w sspm_2
pause
python mtk.py --serialport COM7 %PL% %GPT% w sspm_2 %D%\sspm.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto sspm2

:tee1
echo [12/26] w tee1
pause
python mtk.py --serialport COM7 %PL% %GPT% w tee1 %D%\tee.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto tee1

:tee2
echo [13/26] w tee2
pause
python mtk.py --serialport COM7 %PL% %GPT% w tee2 %D%\tee.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto tee2

:spmfw
echo [14/26] w spmfw
pause
python mtk.py --serialport COM7 %PL% %GPT% w spmfw %D%\spmfw.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto spmfw

:gz1
echo [15/26] w gz1
pause
python mtk.py --serialport COM7 %PL% %GPT% w gz1 %D%\gz.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto gz1

:gz2
echo [16/26] w gz2
pause
python mtk.py --serialport COM7 %PL% %GPT% w gz2 %D%\gz.img
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto gz2

:logo
echo [17/26] w logo
pause
python mtk.py --serialport COM7 %PL% %GPT% w logo %D%\logo.bin
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto logo

:emisc
echo [18/26] e misc
pause
python mtk.py --serialport COM7 %PL% %GPT% e misc
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto emisc

:epara
echo [19/26] e para
pause
python mtk.py --serialport COM7 %PL% %GPT% e para
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto epara

:eexpdb
echo [20/26] e expdb
pause
python mtk.py --serialport COM7 %PL% %GPT% e expdb
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto eexpdb

:eseccfg
echo [21/26] e seccfg
pause
python mtk.py --serialport COM7 %PL% %GPT% e seccfg
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto eseccfg

:esec1
echo [22/26] e sec1
pause
python mtk.py --serialport COM7 %PL% %GPT% e sec1
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto esec1

:envram
echo [23/26] e nvram
pause
python mtk.py --serialport COM7 %PL% %GPT% e nvram
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto envram

:envdata
echo [24/26] e nvdata
pause
python mtk.py --serialport COM7 %PL% %GPT% e nvdata
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto envdata

:eprot1
echo [25/26] e protect1
pause
python mtk.py --serialport COM7 %PL% %GPT% e protect1
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto eprot1

:eprot2
echo [26/26] e protect2
pause
python mtk.py --serialport COM7 %PL% %GPT% e protect2
if %ERRORLEVEL% NEQ 0 (echo FALLO) & goto eprot2

echo.
echo ============================================
echo   TODO LISTO!
echo   Siguiente: TWRP -> Formatear DATA -> reboot
echo ============================================
pause
