#!/usr/bin/env python3
"""Generate a test tone WAV file for audio diagnosis."""

import struct
import math

def generate_sine_wave(frequency=440, duration_seconds=3, sample_rate=48000, amplitude=0.8):
    """Generate a sine wave test tone."""
    num_samples = int(sample_rate * duration_seconds)
    samples = []
    
    for i in range(num_samples):
        t = i / sample_rate
        # Generate sine wave
        sample = amplitude * math.sin(2 * math.pi * frequency * t)
        # Convert to 16-bit PCM
        sample_int = int(sample * 32767)
        samples.append(struct.pack('<h', sample_int))
    
    return b''.join(samples), sample_rate

def write_wav(filename, data, sample_rate=48000, channels=1, bits=16):
    """Write data as a WAV file."""
    with open(filename, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        # File size - 8
        f.write(struct.pack('<I', 36 + len(data)))
        # WAVE format
        f.write(b'WAVE')
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # Chunk size
        f.write(struct.pack('<H', 1))   # Audio format (PCM)
        f.write(struct.pack('<H', channels))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * channels * bits // 8))  # Byte rate
        f.write(struct.pack('<H', channels * bits // 8))  # Block align
        f.write(struct.pack('<H', bits))
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', len(data)))
        f.write(data)

if __name__ == '__main__':
    import sys
    
    filename = sys.argv[1] if len(sys.argv) > 1 else 'test_tone.wav'
    frequency = int(sys.argv[2]) if len(sys.argv) > 2 else 440
    
    print(f"Generating {frequency}Hz test tone...")
    data, sr = generate_sine_wave(frequency=frequency, duration_seconds=3)
    write_wav(filename, data, sample_rate=sr)
    print(f"Saved to: {filename}")
    print(f"File size: {len(data)} bytes")
