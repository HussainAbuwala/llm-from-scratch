# YouTube

Upload metadata and thumbnail generation, one file per video.

| File | What |
|---|---|
| `VIDEO_00_METADATA.md` | Title, description, tags, chapters, settings for the series intro |
| `build_thumbnails.py` | Generates 1280×720 thumbnails |
| `sketch.py` | Hand-drawn drawing primitives (rough lines, marker, paper, sticky notes) |
| `chapters.py` | Finds real chapter timings in a recorded episode |
| `cartoonify.py` | Turns a photo into a cartoon sticker cutout for thumbnails |
| `thumbnails/` | Generated PNGs — seven concepts, clean and `_guide` versions |

## Thumbnails

```bash
.venv/bin/python youtube/build_thumbnails.py
```

Renders six of the seven concepts, in two families — three flat-vector and three hand-drawn —
each covering a different hook (curiosity, promise, provocation), so they can be
A/B tested in YouTube's *Test & Compare*. Each renders clean plus a `_guide`
version marking the reserved cutout area.

The hand-drawn set (`04`-`06`) uses `sketch.py`: jittered double-stroke lines,
marker fonts, graph paper, rotated sticky notes. Every stroke is two slightly
misaligned passes, which is the same trick Excalidraw and Rough.js use. Prefer
these — they match what the videos actually look like, and flat vector templates
are what read as machine-generated.

To composite your face:

```bash
.venv/bin/python youtube/build_thumbnails.py --face ~/Desktop/cutout.png
```

A transparent PNG works best. The cutout is scaled to fill the reserved box
anchored to the bottom, so head-and-shoulders crops sit correctly.

Requires Pillow in the repo venv:

```bash
python3 -m venv .venv && .venv/bin/pip install pillow
```

## Adding a thumbnail for a new video

Add a function to `CONCEPTS` and an entry to `FACE_BOX` in
`build_thumbnails.py`. Colours come from the same palette as the Excalidraw
canvases (see `canvas/README.md`) — keeping thumbnails, canvases, and the webcam
rim on one palette is what makes the series look like a series.

Two rules that the existing concepts follow:

- Four words maximum at display size. The decision happens at feed size, not
  full size — check every thumbnail at 20% zoom.
- The thumbnail must not repeat the title. They should say different things:
  one carries the hook, the other the promise.

## Chapter timings

```bash
.venv/bin/python youtube/chapters.py "~/Movies/llm-series/llm-....mp4"
```

Prints every still segment with the time its chapter would start, and writes
`chapters_sheet.png` showing the canvas heading visible in each one. Segments
sharing a heading are one chapter.

Why not ffmpeg's scene detection: Excalidraw's zoom-to-frame is an animated pan,
not a hard cut, so `select='gt(scene,...)'` finds **zero** transitions even at a
0.06 threshold. This measures frame-to-frame change directly instead, with the
webcam bubble cropped out so the presenter's movement doesn't swamp the signal.

Grouping stays manual on purpose. Comparing heading pixels automatically was
tried and fails in both directions: the crops are mostly white with thin text, so
different headings score as similar, while the same heading at a different zoom
scores as different. Reading ten headings off the sheet takes a minute.

## The Excalidraw thumbnail

`07_excalidraw_llm.png` is not built here — it comes from
`canvas/build_thumbnail_ep0.py`, as a real Excalidraw scene:

```bash
python3 canvas/build_thumbnail_ep0.py
.venv/bin/python canvas/render_png.py canvas/thumbnail_ep0.excalidraw \
    -o youtube/thumbnails/07_excalidraw_llm.png
```

That is the most coherent option, because it is drawn in the same tool and on the
same peach ground (`#f9d6a7`, sampled from the channel banner) as everything else.
For the actual upload, export it from Excalidraw rather than using the checked-in
PNG — the real Excalifont and stroke engine look better than the Pillow stand-in.
