#!/usr/bin/env python3
"""Find real chapter timings in a recorded episode.

Excalidraw's zoom-to-frame is an animated pan, not a hard cut, so ffmpeg's
built-in scene detection finds nothing (verified: zero hits even at a 0.06
threshold). This instead measures frame-to-frame change directly, with the
webcam bubble cropped out so the presenter's movement doesn't swamp the signal.

    .venv/bin/python youtube/chapters.py "~/Movies/llm-series/llm-....mp4"

Output:
  1. every still segment, with the transition time that precedes it
  2. `chapters_sheet.png` — the heading visible in each still segment

Grouping is left to you, deliberately. Several stills often show the SAME canvas
scene, because a two-stage zoom or a mid-scene annotation interrupts the stillness
— on episode 0 that happened four times. Automatic grouping by comparing the
heading pixels was tried and does not work: the crops are mostly white with thin
text, so different headings score as similar, while the same heading at a
different zoom scores as different. Reading ten headings off the sheet takes a
minute and is always right.

Requires ffmpeg on PATH (brew install ffmpeg).
"""

import argparse
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

# Analysis resolution for the change signal. Small on purpose: we want big
# layout changes, not pixel detail.
AW, AH = 192, 134
FPS = 4.0
# Crop away the webcam bubble (default layout puts it at x >= 1550).
CROP = "1550:1080:0:0"


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", path])
    return float(r.stdout.strip())


def change_signal(path, tmp):
    raw = os.path.join(tmp, "frames.gray")
    run(["ffmpeg", "-v", "error", "-i", path, "-vf",
         f"fps={FPS},crop={CROP},scale={AW}:{AH},format=gray",
         "-f", "rawvideo", "-pix_fmt", "gray", raw, "-y"])
    data = open(raw, "rb").read()
    n = len(data) // (AW * AH)
    frames = [data[i * AW * AH:(i + 1) * AW * AH] for i in range(n)]
    diffs = [0.0]
    for a, b in zip(frames, frames[1:]):
        diffs.append(sum(abs(p - q) for p, q in zip(a, b)) / (AW * AH))
    return diffs


def segment(diffs, threshold=1.0, min_still=3.0, gap=6):
    """Split into transition bursts and the still segments between them.

    Returns (runs, segs) where segs[i] is the still period BEFORE runs[i], so
    runs[i-1] is the transition that leads into segs[i]. Short stills are kept —
    they are needed to preserve that alignment — and filtered later.
    """
    ts = [i / FPS for i in range(len(diffs))]
    runs, i = [], 0
    while i < len(diffs):
        if diffs[i] > threshold:
            j = i
            while j + 1 < len(diffs) and max(diffs[j + 1:j + 1 + gap] or [0]) > threshold:
                j += 1
            runs.append((ts[i], ts[j]))
            i = j + 1
        else:
            i += 1
    segs, prev = [], 0.0
    for a, b in runs:
        segs.append((prev, a))
        prev = b
    segs.append((prev, ts[-1] if ts else 0.0))
    return runs, segs


def mmss(t):
    return f"{int(t // 60):02d}:{int(t) % 60:02d}"


def sheet(path, segs, out, heading_h=460, tile_w=760):
    tmp = tempfile.mkdtemp()
    tiles = []
    for i, (a, b) in enumerate(segs):
        p = os.path.join(tmp, f"{i:02d}.png")
        run(["ffmpeg", "-v", "error", "-ss", str((a + b) / 2), "-i", path,
             "-frames:v", "1", "-vf",
             f"crop=1550:{heading_h}:0:0,scale={tile_w}:-1", p, "-y"])
        if os.path.exists(p):
            tiles.append((i, a, b, p))
    if not tiles:
        return None
    th = Image.open(tiles[0][3]).height
    cols = 2
    rows = (len(tiles) + cols - 1) // cols
    img = Image.new("RGB", (cols * (tile_w + 8) + 8, rows * (th + 30) + 8),
                    (25, 25, 25))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16)
    for k, (i, a, b, p) in enumerate(tiles):
        x = 8 + (k % cols) * (tile_w + 8)
        y = 8 + (k // cols) * (th + 30)
        d.text((x, y), f"seg {i}  {mmss(a)}-{mmss(b)}  ({b - a:.0f}s)",
               font=f, fill=(255, 220, 90))
        img.paste(Image.open(p), (x, y + 22))
    img.save(out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--threshold", type=float, default=1.0)
    ap.add_argument("--min-still", type=float, default=3.0,
                    help="ignore still segments shorter than this, in seconds")
    ap.add_argument("--min-scene", type=float, default=12.0,
                    help="a still shorter than this is treated as part of a "
                         "transition, not a scene of its own")
    ap.add_argument("--sheet", default="chapters_sheet.png")
    a = ap.parse_args()

    path = os.path.expanduser(a.video)
    if not os.path.exists(path):
        sys.exit(f"no such file: {path}")
    if not run(["which", "ffmpeg"]).stdout.strip():
        sys.exit("ffmpeg not found. brew install ffmpeg")

    total = duration(path)
    print(f"{os.path.basename(path)}  {mmss(total)}  ({total:.1f}s)\n")

    with tempfile.TemporaryDirectory() as tmp:
        diffs = change_signal(path, tmp)
    runs, segs = segment(diffs, a.threshold, a.min_still)
    segs = [(x, y) for x, y in segs if y - x >= a.min_still]

    print(f"{len(segs)} still segments, {len(runs)} transition bursts\n")
    # A chapter starts where the PREVIOUS scene stopped being still — not at the
    # burst immediately before this segment. Those differ whenever a blank
    # mid-pan state splits one transition into two bursts.
    print(f"{'seg':>4}  {'still period':<15} {'len':>6}   starts at")
    last_long_end = 0.0
    for i, (x, y) in enumerate(segs):
        long_enough = y - x >= a.min_scene
        note = "" if long_enough else "   <- short: mid-pan or in-scene zoom"
        print(f"{i:>4}  {mmss(x)}-{mmss(y)}    {y - x:5.0f}s   "
              f"{mmss(last_long_end)}{note}")
        if long_enough:
            last_long_end = y

    out = sheet(path, segs, a.sheet)
    if out:
        print(f"\nheadings: {out}")
        print("Read the heading in each segment. Segments sharing a heading are "
              "ONE chapter,\nstarting at the 'starts at' time of the first.")
