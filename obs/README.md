# OBS setup

## One-command install

```bash
python3 install_obs_setup.py
```

**Quit OBS first** — OBS rewrites its config on exit and would overwrite the
files this writes.

It creates a new scene collection and profile, both called **LLM Series**, with a
single scene `Canvas + bubble`: screen capture filled to 16:9, plus your face as
a circular bubble bottom-right. Your existing `Untitled` collection and profile
are untouched, and the whole OBS config directory is copied to
`obs-studio.backup-<timestamp>` first.

To revert: OBS → Scene Collection → *Untitled*, and Profile → *Untitled*. Or
delete `~/Library/Application Support/obs-studio` and restore the backup.

The script reads your display UUID and camera device ID out of the existing
collection, so it configures the real hardware rather than guessing.

## Assets

Webcam-bubble assets for the corner-bubble recording layout. OBS has no
circular-crop or border filter, so the round bubble is made from two images.

| File | Used as |
|---|---|
| `bubble_mask.png` | **Image Mask/Blend** filter on the webcam source, type *Alpha Mask (Alpha Channel)* |
| `bubble_ring_blue.png` | Separate **Image** source on top of the webcam — rim + soft shadow |
| `bubble_ring_orange.png` | Same, in the alternate accent colour |

All three are 1024×1024 and aligned to each other, so the mask and the ring must
be given the **identical transform** in OBS (Cmd+E → Edit Transform).

Full step-by-step setup, including permissions and encoder settings, is in
[../RECORDING_SETUP.md](../RECORDING_SETUP.md) sections 4–8.

## Regenerate

```bash
python3 make_bubble_assets.py
```

Standard library only — no Pillow. Edit `RADIUS`, `RING_W`, `SHADOW` or the
`RINGS` colour dict at the top of the script to change the look.
