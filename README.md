# ⌨️ Keyboard SFX Engine v1.0.1 Clickdy Clackdy

🤔 Why does this exist?
Mechvibes exists. It's fine. But:

Electron — even if it's lightweight Electron, it's still Electron. No thanks.
No random sound picker — same sound fires every single keypress. Sounds like a toy drum pad, not a keyboard. Anyone paying attention will clock it in 10 seconds.
No mouse support — half the immersion just doesn't exist.

This script fixes all three. Pure Python, random pick from a sound library on every keypress, mouse clicks included. That's it. That's the whole reason.

---

So you want people on Discord to think you're a real human sitting at a real desk with a real keyboard?
Same honestly. Here's how to use this thing.

---

## 🚀 Setup (it's literally 4 steps, you got this)

1. Extract the zip somewhere that isn't your desktop you animal
2. Dump your sound files into the `sounds/` subfolders (more on that below)
3. Double click `launch.bat`
4. Pick a device, pick a volume, go touch some grass

The converter runs automatically before anything starts. You don't have to do anything. It just works. You're welcome.

---

## 🔊 Sound Folders

Throw your `.wav`, `.flac`, `.ogg` or `.mp3` files in here:

| Folder | What triggers it |
|---|---|
| `sounds/key_down/` | Any key press |
| `sounds/key_up/` | Any key release |
| `sounds/space_down/` | Spacebar down |
| `sounds/space_up/` | Spacebar up |
| `sounds/enter_down/` | Enter down |
| `sounds/enter_up/` | Enter up |
| `sounds/shift_down/` | Shift down |
| `sounds/shift_up/` | Shift up |
| `sounds/mouse_down/` | Mouse click down |
| `sounds/mouse_up/` | Mouse click up |
| `sounds/mouse_scroll/` | Scroll wheel (read the note below before you @ me) |

More files per folder = more random variation = sounds more like a real keyboard and less like a drum machine. Throw like 5-10 wavs in each one. The default pack (7z file) is a ROG Scope TKL (silver switches) recorded with a HyperX Quadcast in an actual room so the reverb is already baked in naturally. Swap it out if you want, we don't care.

Want different sounds? Record your own keyboard. Or google "mechanical keyboard sound pack" and download one like a normal person. Just run the converter after and it'll sort itself out.

---

## 🔄 The Converter (you don't actually have to think about this)

Everything needs to be 48000Hz 16-bit WAV. The converter handles that automatically every time you launch. Drop literally any audio format in there and it'll fix it. Done. Moving on.

---

## ⚡ Low Latency Mode

When you launch, pick option `2` if the sounds feel like they're a few milliseconds behind your keypresses. Uses a smaller audio buffer so it hits faster.

If your audio starts crackling like a 2003 laptop — go back to option `1`. Your PC can't hang. It's fine.

---

## 🖱️ About The Scroll Wheel

Yes the scroll sound is a placeholder. No it's not a bug. No we're not fixing it.

`pynput` — the library that listens to your inputs — only tells us "scroll happened." It doesn't tell us how fast, how far, or how aggressively you yeeted that wheel. One tick and one full wrist flick look completely identical to the script. So every scroll tick plays the same sound. That's just how it is. If this bothers you more than it should, maybe take a walk outside.

---

## 🎚️ VoiceMeeter Routing (for the VTuber nerds)

```
launch.bat ──► VoiceMeeter Input (A1)
W-Okada    ──► VoiceMeeter Input (A1)
                      │
                      ▼
             VoiceMeeter B1 ──► Discord / Game / OBS or whatever the fuck... the choice is yours.. 
```

Pick a Virtual cable (same as your mic/VC) as your output and mix it in potato or whatever you have... now you have your beautiful VC voice and keyboard on the same audio stream. neat!

---

## 📋 Requirements

- Python 3.11+
- `pip install sounddevice soundfile numpy pynput resampy`
- Windows (sorry Mac/Linux people, pynput global hooks are a Windows thing and this is made for GAMERS... call your self a Mac/Linux gamer? pffff... disgusting...)

---

## 🆓 Freeware and OpenSource

Made by **HomuraMiko** & **Lumi**.

Yes, an AI wrote this README and most of the code. Yes, we told it to. Have a problem? Come at me bruh! (pls don't... I'm weak af)
feel free to edit, append, share, destroy... you own copy, pretty much just do whatever you want with this. no need to credit (mostly because you wouldn't anyways)
We ask for nothing. We just leave our mark and move on. 🐱

🎮 [twitch.tv/homuramiko](https://www.twitch.tv/homuramiko)
▶️ [youtube.com/@homuramiko](https://www.youtube.com/@homuramiko)
