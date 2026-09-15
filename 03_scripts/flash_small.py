"""
Multi-partition flash via mtkclient - runs one BROM session, writes all partitions sequentially.
Usage: python flash_small.py
Requires: user to enter BROM (Power 20s → VolUp+VolDown+USB)
"""
import subprocess, sys, os, time

PY = r"D:\Usuarios\Administrador\AppData\Local\Programs\Python\Python311\python.exe"
MTK = r"D:\Usuarios\Administrador\Documents\Custom ROM\00_tools\mtkclient\mtk.py"
PRELOADER = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted\preloader_oppo6769.bin"
STAGING = r"D:\Usuarios\Administrador\Documents\Custom ROM\01_firmware\Realme_RMX2193_C.18_Firmware_extracted"

# Each tuple: (partition_name, filename)
PARTITIONS = [
    ("logo",   os.path.join(STAGING, "logo.bin")),
    ("md1img", os.path.join(STAGING, "md1img.img")),
    ("tee1",   os.path.join(STAGING, "tee.img")),
    ("scp1",   os.path.join(STAGING, "scp.img")),
    ("sspm_1", os.path.join(STAGING, "sspm.img")),
    ("gz1",    os.path.join(STAGING, "gz.img")),
    ("spmfw",  os.path.join(STAGING, "spmfw.img")),
]

base = [PY, MTK, "--serialport", "COM9", "--preloader", PRELOADER,
        "--gpt-num-part-entries", "128", "--gpt-part-entry-size", "128",
        "--sectorsize", "512"]

# Build comma-separated partition names and filenames
pnames = ",".join(p[0] for p in PARTITIONS)
pfiles = ",".join(p[1] for p in PARTITIONS)

cmd = base + ["w", pnames, pfiles]

print("=== Multi-partition flash ===")
print(f"Partitions: {pnames}")
print(f"Files exist: {all(os.path.exists(p[1]) for p in PARTITIONS)}")
print(f"Total size: {sum(os.path.getsize(p[1]) for p in PARTITIONS if os.path.exists(p[1]))} bytes")
print(f"Command length: {len(' '.join(cmd))} chars")
print()

r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
out = r.stdout + r.stderr

# Print last 2000 chars (progress + result)
lines = out.split('\n')
for line in lines[-50:]:
    if line.strip():
        print(line)

ok = "All partitions written" in out or ("Wrote" in out and "Failed" not in out)
print("\nRESULT:" + ("SUCCESS" if ok else "MIXED/FAIL"))
