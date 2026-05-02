#!/usr/bin/env python3
"""
convert_samples.py
Converts all audio files in the sounds/ folder to 48000Hz 16-bit WAV.
Double click, press SPACE, done.
"""

import os
import sys
import soundfile as sf
import sounddevice as sd
import numpy as np
from pathlib import Path

def base_path() -> Path:
    """Returns the real folder where the exe (or script) lives on disk."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent

SOUNDS_DIR = base_path() / "sounds"
SUPPORTED   = {".wav", ".flac", ".ogg", ".mp3", ".aiff", ".aif"}
TARGET_SR   = 48000
TARGET_SUBTYPE = "PCM_16"

def convert_file(path: Path) -> str:
    data, sr = sf.read(str(path), dtype="float32", always_2d=True)

    # Resample if needed
    if sr != TARGET_SR:
        import resampy
        data = resampy.resample(data, sr, TARGET_SR, axis=0)

    # Save as 48000Hz 16-bit WAV (overwrite in place)
    wav_path = path.with_suffix(".wav")
    sf.write(str(wav_path), data, TARGET_SR, subtype=TARGET_SUBTYPE)

    # Remove original if it was a different format
    if path.suffix.lower() != ".wav":
        path.unlink()

    return wav_path.name

def main():
    print("\n" + "=" * 50)
    print("  🎵 SAMPLE CONVERTER — 48000Hz 16-bit WAV")
    print("=" * 50)
    print(f"\n  Scanning: {SOUNDS_DIR}\n")

    if not SOUNDS_DIR.exists():
        print("  ❌ sounds/ folder not found next to this script!")
        input("\n  Press ENTER to exit...")
        sys.exit(1)

    files = [
        f for f in SOUNDS_DIR.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED
    ]

    if not files:
        print("  ⚠️  No supported audio files found in sounds/")
        input("\n  Press ENTER to exit...")
        sys.exit(0)

    print(f"  Found {len(files)} file(s)\n")
    auto = "--auto" in sys.argv

    if not auto:
        print("  Press SPACE to convert, any other key to cancel...")
        import msvcrt
        while True:
            key = msvcrt.getch()
            if key == b' ':
                break
            else:
                print("\n  Cancelled.")
                input("  Press ENTER to exit...")
                sys.exit(0)
    else:
        print("  Auto mode — converting...\n")

    print("\n  Converting...\n")

    ok = 0
    skipped = 0
    failed = 0

    for f in files:
        try:
            info = sf.info(str(f))
            if info.samplerate == TARGET_SR and info.subtype == TARGET_SUBTYPE and f.suffix.lower() == ".wav":
                print(f"  ✅ SKIP (already good)  {f.relative_to(SOUNDS_DIR)}")
                skipped += 1
                continue

            out = convert_file(f)
            print(f"  🔄 CONVERTED  {f.relative_to(SOUNDS_DIR.parent)} → {out}")
            ok += 1

        except Exception as e:
            print(f"  ❌ FAILED  {f.name} — {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"  ✅ Converted : {ok}")
    print(f"  ⏭️  Skipped   : {skipped}")
    print(f"  ❌ Failed    : {failed}")
    print("=" * 50)
    input("\n  Done! Press ENTER to exit...")

if __name__ == "__main__":
    main()
