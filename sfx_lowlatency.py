#!/usr/bin/env python3
import json
import random
import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
from pynput import keyboard, mouse
from pathlib import Path

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
def base_path() -> Path:
    import sys
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent

CONFIG_FILE = base_path() / "config.json"
SOUNDS_DIR  = base_path() / "sounds"

CAT_MAP = {
    "space": ["space"],
    "enter": ["enter", "return"],
    "shift": ["shift", "shift_l", "shift_r"]
}

sound_cache = {}
pressed_keys = set()

output_device_id = None
volume = 0.1

active_sounds = []
lock = threading.Lock()

# ─────────────────────────────────────────
# LOAD SOUNDS
# ─────────────────────────────────────────
def load_sounds():
    print("\n🎵 Loading sounds...")

    folders = [
        "key_down", "key_up",
        "space_down", "space_up",
        "enter_down", "enter_up",
        "shift_down", "shift_up",
        "mouse_down", "mouse_up", "mouse_scroll"
    ]

    for folder in folders:
        path = SOUNDS_DIR / folder
        path.mkdir(parents=True, exist_ok=True)

        files = list(path.glob("*.*"))
        if not files:
            print(f"  ⚠️ {folder} EMPTY")
            continue

        sound_cache[folder] = []

        for f in files:
            try:
                data, fs = sf.read(str(f), dtype="float32")
                if data.ndim == 1:
                    data = np.column_stack([data, data])
                sound_cache[folder].append(data)
            except Exception as e:
                print(f"❌ {f} failed:", e)

        print(f"  ✅ {folder}: {len(files)}")

# ─────────────────────────────────────────
# AUDIO ENGINE
# ─────────────────────────────────────────
def audio_callback(outdata, frames, time_info, status):
    global active_sounds

    buffer = np.zeros((frames, 2), dtype=np.float32)

    with lock:
        still_playing = []
        for snd, pos in active_sounds:
            chunk = snd[pos:pos+frames]
            length = len(chunk)
            buffer[:length] += chunk * volume
            if pos + frames < len(snd):
                still_playing.append((snd, pos + frames))
        active_sounds = still_playing

    outdata[:] = buffer

def play_sfx(category):
    samples = sound_cache.get(category)

    if not samples:
        if "key" not in category:
            state = "down" if "down" in category else "up"
            samples = sound_cache.get(f"key_{state}")
        if not samples:
            return

    snd = random.choice(samples)
    with lock:
        active_sounds.append((snd, 0))

# ─────────────────────────────────────────
# INPUT
# ─────────────────────────────────────────
def get_prefix(key):
    k = str(key).lower()
    for cat, triggers in CAT_MAP.items():
        if any(t in k for t in triggers):
            return cat
    return "key"

def on_press(key):
    k_id = str(key)
    if k_id not in pressed_keys:
        pressed_keys.add(k_id)
        play_sfx(f"{get_prefix(key)}_down")

def on_release(key):
    k_id = str(key)
    if k_id in pressed_keys:
        pressed_keys.discard(k_id)
        play_sfx(f"{get_prefix(key)}_up")

def on_click(x, y, button, pressed):
    play_sfx("mouse_down" if pressed else "mouse_up")

def on_scroll(x, y, dx, dy):
    play_sfx("mouse_scroll")

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    global output_device_id, volume

    conf = {"output_device": None, "volume": 0.1}

    if CONFIG_FILE.exists():
        try:
            conf.update(json.load(open(CONFIG_FILE)))
        except:
            pass

    print("\n=== KEYBOARD SOUND ENGINE (LOW LATENCY) ===")

    devs = sd.query_devices()
    outputs = [(i, d) for i, d in enumerate(devs) if d['max_output_channels'] > 0]

    for i, (idx, d) in enumerate(outputs):
        print(f"[{i}] {d['name']}")

    try:
        choice = input(f"Device [{conf['output_device']}]: ").strip()
        if choice:
            output_device_id = outputs[int(choice)][0]
        else:
            output_device_id = conf['output_device']

        vol = input(f"Volume [{conf['volume']}]: ").strip()
        if vol:
            volume = float(vol)
        else:
            volume = conf['volume']

    except:
        pass

    conf['output_device'] = output_device_id
    conf['volume'] = volume

    with open(CONFIG_FILE, "w") as f:
        json.dump(conf, f)

    load_sounds()

    print("\n⚡ Starting low-latency audio engine...")

    stream = sd.OutputStream(
        samplerate=48000,
        channels=2,
        callback=audio_callback,
        device=output_device_id,
        blocksize=256,  # lower = less delay, try 128 if stable
        latency='low'
    )

    stream.start()

    kb = keyboard.Listener(on_press=on_press, on_release=on_release)
    ms = mouse.Listener(on_click=on_click, on_scroll=on_scroll)

    kb.start()
    ms.start()

    print("🟢 READY — go type like a demon")
    print("Ctrl+C to stop\n")

    try:
        kb.join()
    except KeyboardInterrupt:
        print("\n👋 shutting down")

if __name__ == "__main__":
    main()
