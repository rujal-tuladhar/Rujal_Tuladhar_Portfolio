# -*- coding: utf-8 -*-
"""
Synthesize a seamless 'busy IT office' ambience loop for Nova's background sound.
Output: assets/audio/office-ambience.wav (mono 22.05 kHz 16-bit, 60 s loop)
Tune MASTER_GAIN to change overall loudness, then re-run + push + re-PATCH Vapi
(backgroundSound URL is cached by Vapi per URL, so bump the ?v= query when updating).
"""
import os
import wave
import numpy as np
from scipy.signal import butter, lfilter

SR = 22050
DUR = 60.0
N = int(SR * DUR)
rng = np.random.default_rng(42)

MASTER_GAIN = 1.0          # overall loudness knob
TYPING_GAIN = 0.16         # keyboard prominence (the "IT office" star)
ROOM_GAIN = 0.030          # room tone bed
HVAC_GAIN = 0.020          # air system hum
PHONE_GAIN = 0.030         # distant phone ring
TRANSIENT_GAIN = 0.05      # chairs, paper, mouse clicks


def bp(x, lo, hi, order=3):
    b, a = butter(order, [lo / (SR / 2), hi / (SR / 2)], btype="band")
    return lfilter(b, a, x)


def lp(x, hi, order=3):
    b, a = butter(order, hi / (SR / 2), btype="low")
    return lfilter(b, a, x)


out = np.zeros(N)

# ---- 1. Room tone: pink-ish noise bed -----------------------------------
w = rng.standard_normal(N)
pink = lp(w, 900, 2)
pink += 0.4 * lp(rng.standard_normal(N), 300, 2)
# slow level drift so it breathes
drift = 1.0 + 0.25 * np.sin(2 * np.pi * np.arange(N) / SR / 13.0)
out += ROOM_GAIN * pink / np.max(np.abs(pink)) * drift

# ---- 2. HVAC hum ---------------------------------------------------------
t = np.arange(N) / SR
hvac = (np.sin(2 * np.pi * 60 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)
        + 0.25 * np.sin(2 * np.pi * 180 * t))
hvac *= 1.0 + 0.15 * np.sin(2 * np.pi * t / 9.0)
out += HVAC_GAIN * hvac / np.max(np.abs(hvac))


def add_click(buf, pos, dur_ms, center, width, amp):
    n = int(SR * dur_ms / 1000)
    if pos + n >= len(buf) or n <= 4:
        return
    burst = rng.standard_normal(n) * np.exp(-np.arange(n) / (n / 4.0))
    burst = bp(burst, max(80, center - width), min(SR / 2 - 100, center + width), 2)
    m = np.max(np.abs(burst))
    if m > 0:
        buf[pos:pos + n] += amp * burst / m


# ---- 3. Keyboard typing: three desks, different keyboards ---------------
desks = [
    {"center": 2600, "width": 1400, "amp": 1.00, "speed": 0.085},  # clacky mech
    {"center": 3600, "width": 1600, "amp": 0.65, "speed": 0.105},  # laptop chiclet
    {"center": 1900, "width": 1000, "amp": 0.50, "speed": 0.125},  # distant desk
]
typing = np.zeros(N)
for desk in desks:
    pos = rng.uniform(0.5, 3.0)
    while pos < DUR - 1:
        burst_len = rng.uniform(1.2, 4.5)          # a thought being typed
        end = min(pos + burst_len, DUR - 0.5)
        while pos < end:
            add_click(typing, int(pos * SR), rng.uniform(4, 9),
                      desk["center"] * rng.uniform(0.85, 1.15),
                      desk["width"], desk["amp"] * rng.uniform(0.5, 1.0))
            pos += rng.uniform(desk["speed"] * 0.6, desk["speed"] * 1.8)
        pos += rng.uniform(0.4, 2.5)               # pause, read, think
out += TYPING_GAIN * typing

# ---- 4. Mouse clicks & double-clicks ------------------------------------
trans = np.zeros(N)
for _ in range(22):
    p = rng.uniform(0.5, DUR - 0.5)
    add_click(trans, int(p * SR), rng.uniform(3, 5), 3200, 900, 0.5)
    if rng.random() < 0.35:                        # double-click
        add_click(trans, int((p + 0.12) * SR), 4, 3200, 900, 0.45)

# ---- 5. Chair creaks / paper shuffles (filtered swooshes) ---------------
for _ in range(7):
    p = int(rng.uniform(1, DUR - 2) * SR)
    n = int(SR * rng.uniform(0.25, 0.7))
    sw = rng.standard_normal(n) * np.hanning(n)
    sw = bp(sw, 400, 2200, 2)
    m = np.max(np.abs(sw))
    if m > 0:
        trans[p:p + n] += 0.35 * sw / m
out += TRANSIENT_GAIN * trans

# ---- 6. Distant phone ring (once per loop, two brrings) -----------------
ring = np.zeros(N)
for start in (34.0, 36.4):
    n = int(SR * 1.4)
    p = int(start * SR)
    tt = np.arange(n) / SR
    tone = (np.sin(2 * np.pi * 440 * tt) + np.sin(2 * np.pi * 480 * tt))
    tone *= (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 20 * tt)))   # warble
    env = np.minimum(1, tt * 30) * np.exp(-tt * 1.2)
    ring[p:p + n] += tone * env
ring = lp(ring, 1800, 2)                            # it's across the room
m = np.max(np.abs(ring))
if m > 0:
    out += PHONE_GAIN * ring / m

# ---- 7. Seamless loop: crossfade last second into first -----------------
xf = int(SR * 1.0)
fade = np.linspace(0, 1, xf)
out[:xf] = out[:xf] * fade + out[-xf:] * (1 - fade)
out = out[: N - xf]

# ---- 8. Master: gentle soft-clip + normalize ----------------------------
out *= MASTER_GAIN
out = np.tanh(out * 3.0) / 3.0                      # soft knee
peak = np.max(np.abs(out))
out = out / peak * 0.5                              # peaks at -6 dBFS
rms_db = 20 * np.log10(np.sqrt(np.mean(out ** 2)))

dest = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "assets", "audio", "office-ambience.wav")
os.makedirs(os.path.dirname(dest), exist_ok=True)
pcm = (out * 32767).astype(np.int16)
with wave.open(dest, "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes(pcm.tobytes())

print(f"wrote {dest}")
print(f"duration {len(out)/SR:.1f}s, RMS {rms_db:.1f} dBFS, size {os.path.getsize(dest)/1e6:.2f} MB")
