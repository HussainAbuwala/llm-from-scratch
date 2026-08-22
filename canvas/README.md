# Canvases

Excalidraw canvases used for on-camera explanation. They are **generated**, not
hand-drawn, so they can be corrected and regenerated when the theory changes.

| File | Video | Scenes |
|---|---|---|
| `series_intro.excalidraw` | Video 0 — series introduction | 10 |
| `episode_01_bigram.excalidraw` | Episode 1 theory — the smallest language model | 28 |
| `thumbnail_ep0.excalidraw` | Video 0 thumbnail — a drawing of the machine | 1 |
| `channel_intro.excalidraw` | Channel intro — The Unplanned Stack | 12 |
| `thumbnail_channel.excalidraw` | Channel intro thumbnail — the plan vs what happened | 1 |
| `thumbnail_channel_alt.excalidraw` | Channel intro thumbnail, alt — the stack trace | 1 |
| `thumbnail_stack.excalidraw` | Channel intro thumbnail — a stack vs my stack | 1 |

## Open one

Go to [excalidraw.com](https://excalidraw.com) → hamburger menu → **Open** →
pick the `.excalidraw` file. Everything is local; nothing is uploaded.

Each scene is a 1600×900 **frame** (16:9). Select a frame and press **Shift+2**
to fill the viewport with it. Frames run left to right in a single row.

See [../RECORDING_SETUP.md](../RECORDING_SETUP.md) for the recording layout.

## Regenerate after editing the scripts

```bash
python3 build_series_intro.py && python3 build_episode_01.py
```

Regenerating **overwrites** the `.excalidraw` files. If you hand-edit a canvas in
Excalidraw and want to keep those edits, either save under a new name or port the
change back into the build script. For recording annotations, work on a copy:

```bash
cp episode_01_bigram.excalidraw episode_01_bigram.RECORDING.excalidraw
```

## Proofread without opening Excalidraw

```bash
python3 render_preview.py
```

Writes `*_preview.html` — a contact sheet of every scene, rendered as SVG. It is
a rough approximation (no hand-drawn stroke style, approximate fonts), useful for
catching overlapping elements and overflowing text. Open it in any browser.

## Files

- `excalidraw_kit.py` — scene builder: elements, frames, and composite helpers
  (`cards`, `bars`, `table`, `tickets`, `panel`).
- `build_series_intro.py` — video 0 content.
- `build_episode_01.py` — episode 1 content.
- `build_channel_intro.py` — channel intro content (channel-level, not part of
  the LLM series; here because the toolchain is here).
- `render_preview.py` — proofreading renderer (HTML/SVG contact sheet).
- `render_png.py` — renders one frame to an exact-size PNG with hand-drawn
  strokes. Use this instead of the SVG path when the output size must be exact:
  macOS `qlmanage` does not honour SVG dimensions and silently scales and crops.
- `build_thumbnail_channel.py` — channel intro thumbnail (route vs plan).
- `build_thumbnail_channel_alt.py` — channel intro thumbnail (stack trace).
- `build_thumbnail_stack.py` — channel intro thumbnail (a stack vs my stack).
- `build_thumbnail_ep0.py` — the video 0 thumbnail as an Excalidraw scene.
  Export the final PNG from Excalidraw itself (select frame → Export image →
  PNG, "only selected") for authentic strokes and the real Excalifont.

## Conventions

Kept consistent so visual language carries across episodes:

| Meaning | Colour |
|---|---|
| Neutral / data / input | grey `#e9ecef` |
| Tokens, explanation, "how it works" | blue `#a5d8ff` |
| Correct, working, the good outcome | green `#b2f2bb` |
| The model, machinery, formal statements | violet `#d0bfff` |
| Warnings, failures, things that break | red `#ffc9c9` |
| The key takeaway of a scene | yellow `#ffec99` |

Monospace (`CODE`) for anything the viewer will type or that is literally a
number; handwritten (`HAND`) for prose. Never prose in monospace — it reads as
output rather than explanation.
