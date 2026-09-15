#!/usr/bin/env python3
"""Generate a test tone through the phone's speaker for audio diagnosis."""

import subprocess
import sys
import time
import os

# Check if we're on Windows and adb is available
adb_path = "D:/Usuarios/Administrador/Documents/Custom ROM/00_tools/platform-tools/adb.exe"

def run_cmd(cmd):
    """Run command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

# Check device connection
out, err, rc = run_cmd(f'"{adb_path}" devices')
if 'device' not in out or rc != 0:
    print("ERROR: Device not connected")
    sys.exit(1)

print("Device connected. Testing audio output...")
print()

# Try to play a test tone using Android's built-in test mode
# Method 1: Use media playback to generate a sine wave
print("Generating 440Hz test tone for 3 seconds...")

# Create a simple test using audiopatches or raw audio generation
# We'll use ffmpeg to create an audio file and push it
try:
    import subprocess
    # Generate a 3-second 440Hz sine wave at 48kHz
    cmd = f'ffmpeg -f lavfi -i "sine=frequency=440:duration=3" -ar 48000 -ac 2 -f wav -'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if result.returncode == 0 and len(result.stdout) > 0:
        # Push to phone and play
        adb_push = f'"{adb_path}" push /dev/stdin /sdcard/test_tone.wav'
        proc = subprocess.Popen(adb_push, shell=True, stdin=subprocess.PIPE)
        proc.communicate(input=result.stdout)
        
        # Play the tone
        print("Playing test tone... Make sure volume is up!")
        time.sleep(1)
        play_cmd = f'"{adb_path}" shell am start -a android.intent.action.VIEW -d "file:///sdcard/test_tone.wav"'
        subprocess.run(play_cmd, shell=True)
        time.sleep(4)
        print("Test complete.")
except Exception as e:
    print(f"ffmpeg method failed: {e}")
    print("Trying alternative...")
    
    # Alternative: Use the phone's built-in diagnostic mode
    print("Attempting to access hidden diagnostic menu...")
    run_cmd(f'"{adb_path}" shell am start -a android.intent.action.VIEW -d "tel:*#*#3646633#*#*"')
    time.sleep(2)
    print("If diagnostic menu opened, check audio output there.")
    
    print()
    print("Manual test instructions:")
    print("1. Open Settings > Sound & vibration")
    print("2. Adjust music volume to maximum")
    print("3. Play any song at max volume")
    print("4. Check if sound is clear, distorted, or quiet")
    print("5. Note if it's one-sided or both sides")
