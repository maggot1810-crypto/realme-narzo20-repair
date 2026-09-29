import subprocess, sys, os

MTK = r"D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\mtk.py"
PY = r"D:\Usuarios\Administrador\AppData\Local\Programs\Python\Python311\python.exe"
PRELOADER = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin"

# args: name file offset length [mode]
name = sys.argv[1]
file = sys.argv[2]
off = int(sys.argv[3], 16)
length = int(sys.argv[4], 16)
mode = sys.argv[5] if len(sys.argv) > 5 else "w"

base = [PY, MTK, "--serialport", "COM9", "--preloader", PRELOADER,
        "--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128",
        "--sectorsize", "512"]

if mode == "w":
    cmd = base + ["w", name, file]
else:
    cmd = base + ["wo", hex(off), hex(length), file]

r = subprocess.run(cmd, capture_output=True, text=True)
out = r.stdout + r.stderr

# Show last 1200 chars
print(out[-1200:])

ok = "Wrote" in out and "Failed" not in out
if "Couldn't detect partition" in out:
    ok = False
print("RESULT:" + ("SUCCESS" if ok else "FAIL"))
sys.exit(0 if ok else 1)