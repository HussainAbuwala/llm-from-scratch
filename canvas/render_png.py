#!/usr/bin/env python3
"""Render a frame from a .excalidraw file to an exact-size PNG.

Written because macOS `qlmanage` does not honour SVG dimensions — it scales and
crops unpredictably, which made the SVG preview path unusable twice. This draws
with Pillow instead, using the hand-drawn stroke primitives from
`youtube/sketch.py`, so the output is both exactly the requested size and close
to what Excalidraw itself renders.

    .venv/bin/python canvas/render_png.py canvas/thumbnail_ep0.excalidraw

For the final upload, still prefer exporting from Excalidraw (authentic strokes
and the real Excalifont). This is for checking layout and for a usable
stand-in.
"""

import argparse
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "youtube"))
import sketch  # noqa: E402

HAND_BIG = (sketch.CHALK, 2)     # Chalkboard SE Bold - closest to Excalifont
HAND_SMALL = (sketch.BRADLEY, 0)
MONO = ("/System/Library/Fonts/Menlo.ttc", 0)

_fonts = {}


def font(spec, size):
    path, index = spec
    key = (path, index, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size, index=index)
    return _fonts[key]


def font_for(el):
    fam = el.get("fontFamily", 1)
    size = el.get("fontSize", 20)
    if fam == 3:
        return font(MONO, size)
    return font(HAND_BIG if size >= 46 else HAND_SMALL, size)


def rgb(colour, default=None):
    if not colour or colour == "transparent":
        return default
    c = colour.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def rotate_about(px, py, cx, cy, ang):
    if not ang:
        return (px, py)
    dx, dy = px - cx, py - cy
    c, s = math.cos(ang), math.sin(ang)
    return (cx + dx * c - dy * s, cy + dx * s + dy * c)


def rough_fill_ellipse(d, box, colour, rng, jitter=3.0):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    pts = []
    for i in range(40):
        a = i / 40 * math.tau
        pts.append((cx + math.cos(a) * (rx + rng.uniform(-jitter, jitter)),
                    cy + math.sin(a) * (ry + rng.uniform(-jitter, jitter))))
    d.polygon(pts, fill=colour)


def render(path, frame_index=0, out=None, scale=1.0):
    doc = json.load(open(path))
    els = doc["elements"]
    frames = sorted([e for e in els if e["type"] == "frame"], key=lambda f: f["x"])
    if not frames:
        sys.exit("no frames in this file")
    fr = frames[frame_index]
    W = int(fr["width"] * scale)
    H = int(fr["height"] * scale)
    ox, oy = fr["x"], fr["y"]

    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    rng = sketch.rng_for(7)

    kids = [e for e in els
            if e["type"] != "frame" and e.get("frameId") == fr["id"]]
    labels = {e["containerId"]: e for e in kids
              if e["type"] == "text" and e.get("containerId")}

    def S(v):
        return v * scale

    for el in kids:
        if el["type"] == "text" and el.get("containerId"):
            continue
        x = S(el["x"] - ox)
        y = S(el["y"] - oy)
        w = S(el["width"])
        h = S(el["height"])
        stroke = rgb(el.get("strokeColor"), (30, 30, 30))
        fill = rgb(el.get("backgroundColor"))
        sw = max(1, int(S(el.get("strokeWidth", 2)) * 1.6))
        t = el["type"]

        if t == "rectangle":
            # Honour rotation: Excalidraw spins a rect about its own centre.
            ang = el.get("angle") or 0
            cx, cy = x + w / 2, y + h / 2
            jit = 2.0 * scale
            corners = [rotate_about(px, py, cx, cy, ang) for px, py in
                       ((x, y), (x + w, y), (x + w, y + h), (x, y + h))]
            if fill:
                d.polygon([(px + rng.uniform(-jit, jit), py + rng.uniform(-jit, jit))
                           for px, py in corners], fill=fill)
            if stroke and el.get("strokeColor") != "transparent":
                for a_, b_ in zip(corners, corners[1:] + corners[:1]):
                    sketch.rough_line(d, a_, b_, stroke, sw, rng, jitter=2.2 * scale)
        elif t == "ellipse":
            if fill:
                rough_fill_ellipse(d, (x, y, x + w, y + h), fill, rng, 2.5 * scale)
            sketch.rough_ellipse(d, (x, y, x + w, y + h), stroke, sw, rng,
                                 jitter=2.2 * scale)
        elif t == "diamond":
            pts = [(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h),
                   (x, y + h / 2)]
            if fill:
                d.polygon(pts, fill=fill)
            for a, b in zip(pts, pts[1:] + pts[:1]):
                sketch.rough_line(d, a, b, stroke, sw, rng)
        elif t in ("line", "arrow"):
            pts = [(x + S(px), y + S(py)) for px, py in el["points"]]
            for a, b in zip(pts, pts[1:]):
                sketch.rough_line(d, a, b, stroke, sw, rng, jitter=1.6 * scale)
            if t == "arrow" and el.get("endArrowhead") and len(pts) >= 2:
                sketch.rough_arrow(d, pts[-2], pts[-1], stroke, sw, rng,
                                   head=int(S(26)))
        elif t == "text":
            f = font_for(dict(el, fontSize=int(S(el["fontSize"]))))
            for i, ln in enumerate(el["text"].split("\n")):
                d.text((x, y + i * S(el["fontSize"]) * 1.25), ln, font=f,
                       fill=stroke)

        lbl = labels.get(el["id"])
        if lbl:
            f = font_for(dict(lbl, fontSize=int(S(lbl["fontSize"]))))
            lines = lbl["text"].split("\n")
            lh = S(lbl["fontSize"]) * 1.25
            cy = y + h / 2 - (len(lines) - 1) * lh / 2
            for i, ln in enumerate(lines):
                d.text((x + w / 2, cy + i * lh), ln, font=f,
                       fill=rgb(lbl.get("strokeColor"), (30, 30, 30)),
                       anchor="mm")

    out = out or path.replace(".excalidraw", ".png")
    img.save(out)
    print(f"{out}  {img.width}x{img.height}  {os.path.getsize(out) // 1024} KB")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("-i", "--index", type=int, default=0, help="which frame")
    ap.add_argument("-o", "--out")
    ap.add_argument("-s", "--scale", type=float, default=1.0)
    a = ap.parse_args()
    render(a.file, a.index, a.out, a.scale)
