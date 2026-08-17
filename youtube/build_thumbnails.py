#!/usr/bin/env python3
"""Generate 1280x720 YouTube thumbnails.

Six concepts in two families, covering three hooks each so they can be A/B tested.

Flat vector — bold, high contrast, conventional:

  01_cant_explain   curiosity   - the honest admission
  02_counting_gpt   promise     - the whole scope, in one staircase
  03_no_api_keys    provocation - from-scratch, stated bluntly

Hand-drawn (see sketch.py) — marker on graph paper, matching the Excalidraw
canvases the videos are actually presented on. Harder to mistake for a template:

  04_notebook       promise     - hand-lettered title, sketched staircase
  05_blackbox       curiosity   - "i can't explain this" + a drawn black box
  06_sticky         curiosity   - whiteboard and sticky notes

Each renders twice: a clean version, and a `_guide` version marking where the
presenter cutout goes. To composite a real cutout (transparent PNG is best):

    .venv/bin/python youtube/build_thumbnails.py --face ~/Desktop/face.png

Needs Pillow:  python3 -m venv .venv && .venv/bin/pip install pillow
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow missing. Run:\n"
             "  python3 -m venv .venv && .venv/bin/pip install pillow\n"
             "then use .venv/bin/python to run this script.")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sketch  # noqa: E402

W, H = 1280, 720
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "thumbnails")

# Series palette, shared with the Excalidraw canvases
INK = (30, 30, 30)
BLUE = (25, 113, 194)
GREEN = (47, 158, 68)
VIOLET = (103, 65, 217)
YELLOW = (255, 212, 59)
RED = (224, 49, 49)
CREAM = (253, 251, 245)
NAVY = (16, 26, 43)
WHITE = (255, 255, 255)
GREY = (138, 148, 166)

F = "/System/Library/Fonts/Supplemental/"
HEAVY = F + "Arial Black.ttf"
MONO = "/System/Library/Fonts/Menlo.ttc"
HAND = F + "Bradley Hand Bold.ttf"
if not os.path.exists(HAND):
    HAND = F + "Comic Sans MS Bold.ttf"
if not os.path.exists(HAND):
    HAND = HEAVY

# Region reserved for the presenter cutout: (x, y, w, h)
FACE_BOX = {
    "01_cant_explain": (838, 108, 442, 612),
    "02_counting_gpt": (830, 150, 450, 570),
    "03_no_api_keys": (820, 130, 460, 590),
    "04_notebook": (852, 168, 428, 552),
    "05_blackbox": (846, 120, 434, 600),
    "06_sticky": (856, 150, 424, 570),
}

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text(d, xy, s, size, fill, path=HEAVY, anchor="ls", spacing=0):
    """Draw text. anchor uses Pillow's two-letter codes; 'ls' = left baseline."""
    f = font(path, size)
    if not spacing:
        d.text(xy, s, font=f, fill=fill, anchor=anchor)
        return d.textlength(s, font=f)
    # Manual tracking, since Pillow has no letter-spacing
    total = sum(d.textlength(c, font=f) for c in s) + spacing * (len(s) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    for c in s:
        d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1])
        x += d.textlength(c, font=f) + spacing
    return total


def width_of(d, s, size, path=HEAVY, spacing=0):
    f = font(path, size)
    if not spacing:
        return d.textlength(s, font=f)
    return sum(d.textlength(c, font=f) for c in s) + spacing * (len(s) - 1)


def squiggle(d, x, y, w, fill=RED, sw=11):
    """Hand-drawn underline — the visual tie to the Excalidraw canvases."""
    pts, steps = [], 48
    for i in range(steps + 1):
        px = x + w * i / steps
        py = y + 7 * __import__("math").sin(i / steps * 3.14159 * 3)
        pts.append((px, py))
    d.line(pts, fill=fill, width=sw, joint="curve")


def chip(d, x, y, label, fill=BLUE, fg=WHITE, size=30, pad=24):
    tw = width_of(d, label, size, spacing=1.5)
    h = size + 30
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + h], radius=h // 2, fill=fill)
    text(d, (x + pad + tw / 2, y + h / 2 + size * 0.36), label, size, fg,
         anchor="ms", spacing=1.5)
    return tw + pad * 2


def vgrad(img, box, top, bottom):
    x0, y0, x1, y1 = box
    g = Image.new("RGB", (1, y1 - y0))
    gd = ImageDraw.Draw(g)
    for i in range(y1 - y0):
        k = i / max(1, y1 - y0 - 1)
        gd.point((0, i), tuple(int(top[c] + (bottom[c] - top[c]) * k) for c in range(3)))
    img.paste(g.resize((x1 - x0, y1 - y0)), (x0, y0))


def put_face(img, d, concept, face_img, guide):
    x, y, w, h = FACE_BOX[concept]
    if face_img is not None:
        # Fill the box, anchored to the bottom (heads at the top, no floating).
        scale = max(w / face_img.width, h / face_img.height)
        fw, fh = int(face_img.width * scale), int(face_img.height * scale)
        resized = face_img.resize((fw, fh), Image.LANCZOS)
        left = (fw - w) // 2
        crop = resized.crop((left, fh - h, left + w, fh))
        img.paste(crop, (x, y), crop if crop.mode == "RGBA" else None)
        return
    if not guide:
        return
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, outline=RED, width=5)
    text(d, (x + w / 2, y + h / 2 - 4), "YOUR FACE", 44, RED, anchor="ms")
    text(d, (x + w / 2, y + h / 2 + 44), "cutout goes here", 28, RED,
         path=HAND, anchor="ms")


# --------------------------------------------------------------- concept 01
def cant_explain(img, d):
    vgrad(img, (0, 0, W, H), (26, 44, 74), NAVY)
    for (cx, cy, cs) in ((1010, 340, 300), (1195, 600, 190), (845, 660, 130)):
        text(d, (cx, cy), "?", cs, (44, 62, 94), anchor="ms")
    text(d, (58, 92), "BUILDING AN LLM FROM SCRATCH", 25, YELLOW, spacing=5.5)
    text(d, (56, 250), "I CAN'T", 118, WHITE)
    text(d, (56, 372), "EXPLAIN", 118, WHITE)
    squiggle(d, 60, 396, width_of(d, "EXPLAIN", 118) - 6)
    text(d, (56, 502), "THIS.", 118, YELLOW)
    # The black box reads as the object of "THIS." — keep it clear of the cutout.
    d.rounded_rectangle([452, 416, 744, 518], radius=16,
                        fill=(0, 0, 0), outline=(57, 80, 122), width=4)
    text(d, (598, 490), "LLM", 70, WHITE, anchor="ms", spacing=4)
    chip(d, 56, 596, "EP 0 · THE PLAN", BLUE)


# --------------------------------------------------------------- concept 02
def counting_gpt(img, d):
    d.rectangle([0, 0, W, H], fill=CREAM)
    text(d, (56, 168), "LLM FROM", 116, INK)
    text(d, (56, 286), "SCRATCH", 116, BLUE)
    squiggle(d, 60, 312, width_of(d, "SCRATCH", 116), fill=(240, 140, 0))
    # ASCII arrows: the handwriting fonts have no glyph for U+2192.
    text(d, (58, 370), "counting -> gradients -> attention -> a GPT",
         28, (107, 114, 128), path=HAND)
    steps = [("COUNT", BLUE), ("LEARN", GREEN), ("ATTEND", VIOLET), ("GPT", YELLOW)]
    for i, (label, colour) in enumerate(steps):
        x, y = 58 + i * 196, 600 - i * 84
        d.rounded_rectangle([x, y, x + 178, y + 82], radius=12, fill=colour)
        text(d, (x + 89, y + 54), label, 30, INK if colour == YELLOW else WHITE,
             anchor="ms", spacing=1)
        if i < 3:
            d.line([(x + 186, y + 18), (x + 190, y - 6)], fill=(170, 175, 185),
                   width=6)
    # Right-align the two chips off the same edge so they can never collide.
    right, gap = 1224, 16
    w_ep = width_of(d, "EP 0", 30, spacing=1.5) + 48
    w_series = width_of(d, "14 EPISODES", 30, spacing=1.5) + 48
    chip(d, right - w_ep, 56, "EP 0", INK)
    chip(d, right - w_ep - gap - w_series, 56, "14 EPISODES", RED)


# --------------------------------------------------------------- concept 03
def no_api_keys(img, d):
    d.rectangle([0, 0, W, H], fill=CREAM)
    d.rectangle([0, 0, 26, H], fill=YELLOW)
    text(d, (66, 96), "BUILDING AN LLM FROM SCRATCH", 25, GREY, spacing=5.5)
    text(d, (64, 240), "NO API", 132, INK)
    text(d, (64, 374), "KEYS.", 132, RED)
    d.rounded_rectangle([64, 432, 724, 508], radius=12, fill=(238, 240, 243))
    text(d, (86, 484), "client.messages.create(...)", 32, GREY, path=MONO)
    d.line([(74, 480), (714, 462)], fill=RED, width=9)
    text(d, (64, 596), "we build the whole thing", 52, BLUE, path=HAND)
    chip(d, 64, 626, "EP 0 · THE PLAN", INK)


# ===================================================== hand-drawn concepts ===
# These use sketch.py: jittered double-stroke lines, marker fonts, graph paper.
# The flat-vector concepts above can read as generic/templated; these look drawn,
# which matches what the videos actually are.

MARKER = sketch.MARKER
CHALKB = sketch.CHALK
NOTEB = sketch.NOTE


def _mfont(path, size, index=0):
    key = (path, size, index)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size, index=index)
    return _cache[key]


def mtext(d, xy, s, size, fill, path=MARKER, index=1, anchor="ls"):
    f = _mfont(path, size, index)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
    return d.textlength(s, font=f)


def mwidth(d, s, size, path=MARKER, index=1):
    return d.textlength(s, font=_mfont(path, size, index))


# --------------------------------------------------------------- concept 04
def notebook(img, d):
    r = sketch.rng_for(4)
    d = sketch.paper(img, grid=26)
    ink = sketch.PENCIL

    w = mwidth(d, "LLM from", 108, CHALKB, 2)
    sketch.highlight(img, (52, 92, 52 + w + 18, 176), rng=r)
    d = ImageDraw.Draw(img)
    mtext(d, (56, 168), "LLM from", 108, ink, CHALKB, 2)
    mtext(d, (56, 292), "scratch", 108, BLUE, CHALKB, 2)
    sketch.rough_line(d, (60, 320), (60 + mwidth(d, "scratch", 108, CHALKB, 2), 322),
                      (240, 140, 0), 9, r)

    steps = [("count", BLUE), ("learn", GREEN), ("attend", VIOLET), ("GPT", (240, 140, 0))]
    for i, (label, colour) in enumerate(steps):
        x, y = 62 + i * 178, 588 - i * 80
        sketch.rough_rect(d, (x, y, x + 158, y + 76), fill_colour=None,
                          outline=colour, width=5, rng=r)
        mtext(d, (x + 79, y + 52), label, 38, colour, MARKER, 1, anchor="ms")
        if i < 3:
            sketch.rough_arrow(d, (x + 166, y + 26), (x + 176, y - 10), ink, 4, r,
                              head=13)

    mtext(d, (56, 398), "ep 0 · the plan", 36, (130, 136, 148), BRADLEY_HAND, 0)
    # Proximity to the "count" box below does the work; an arrow here just
    # collides with the words.
    mtext(d, (64, 552), "start here", 30, RED, BRADLEY_HAND, 0)

    sketch.rough_ellipse(d, (824, 44, 1108, 152), outline=RED, width=6, rng=r)
    mtext(d, (966, 112), "14 episodes", 44, RED, MARKER, 1, anchor="ms")


# --------------------------------------------------------------- concept 05
def blackbox(img, d):
    r = sketch.rng_for(5)
    d = sketch.paper(img, grid=26)
    ink = sketch.PENCIL

    mtext(d, (58, 150), "i can't", 116, ink, CHALKB, 2)
    mtext(d, (58, 272), "explain", 116, ink, CHALKB, 2)
    # Highlight sits behind "this" — the word the whole thumbnail turns on.
    sketch.highlight(img, (50, 316, 60 + mwidth(d, "this", 116, CHALKB, 2), 404),
                     colour=(255, 214, 102), alpha=155, rng=r)
    d = ImageDraw.Draw(img)
    mtext(d, (58, 394), "this", 116, RED, CHALKB, 2)

    box = (392, 300, 700, 424)
    sketch.rough_rect(d, box, fill_colour=(28, 30, 36), outline=ink, width=6, rng=r)
    mtext(d, (546, 380), "LLM", 74, (250, 250, 250), MARKER, 1, anchor="ms")
    for (qx, qy, qs) in ((722, 300, 76), (748, 396, 54), (676, 470, 44)):
        mtext(d, (qx, qy), "?", qs, (150, 158, 172), MARKER, 1)

    mtext(d, (58, 520), "so i'm building one.", 58, BLUE, BRADLEY_HAND, 0)
    sketch.rough_line(d, (62, 540), (62 + mwidth(d, "so i'm building one.", 58, BRADLEY_HAND, 0), 544),
                      BLUE, 6, r)
    mtext(d, (58, 664), "ep 0 · 14 episodes · counting to a GPT", 36,
          (128, 134, 146), BRADLEY_HAND, 0)


# --------------------------------------------------------------- concept 06
def sticky_notes(img, d):
    r = sketch.rng_for(6)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill=(238, 240, 236))
    for x in range(0, W, 3):  # faint whiteboard sheen
        d.line([(x, 0), (x, H)], fill=(242, 244, 240), width=1)

    mtext(d, (58, 118), "how do you even", 62, (110, 116, 128), BRADLEY_HAND, 0)
    mtext(d, (58, 214), "BUILD one?", 116, sketch.PENCIL, CHALKB, 2)
    sketch.rough_line(d, (62, 244), (62 + mwidth(d, "BUILD one?", 116, CHALKB, 2), 248),
                      RED, 10, r)

    notes = [("count", (255, 236, 153), -5), ("learn", (178, 242, 187), 4),
             ("attend", (208, 191, 255), -3), ("GPT", (165, 216, 255), 5)]
    label_font = _mfont(MARKER, 40, 1)
    for i, (label, colour, ang) in enumerate(notes):
        x, y = 62 + i * 176, 360 + (18 if i % 2 else 0)
        sketch.sticky(img, x, y, 152, 152, colour, ang, label=label,
                      font=label_font)
    d = ImageDraw.Draw(img)
    mtext(d, (58, 636), "one episode at a time. i'm learning it too.", 36,
          (110, 116, 128), BRADLEY_HAND, 0)
    mtext(d, (58, 692), "LLM FROM SCRATCH · EP 0", 30, RED, MARKER, 1)


BRADLEY_HAND = sketch.BRADLEY

CONCEPTS = {
    "01_cant_explain": cant_explain,
    "02_counting_gpt": counting_gpt,
    "03_no_api_keys": no_api_keys,
    "04_notebook": notebook,
    "05_blackbox": blackbox,
    "06_sticky": sticky_notes,
}


def render(name, fn, face_img, guide):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    fn(img, d)
    put_face(img, d, name, face_img, guide)
    stem = name + ("_guide" if guide else "")
    path = os.path.join(OUT, stem + ".png")
    img.save(path, optimize=True)
    kb = os.path.getsize(path) // 1024
    print(f"  {stem}.png  {img.width}x{img.height}  {kb} KB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--face", help="PNG cutout of you; transparent background best")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    face_img = None
    if args.face:
        p = os.path.expanduser(args.face)
        if not os.path.exists(p):
            sys.exit(f"no such file: {p}")
        face_img = Image.open(p).convert("RGBA")
        print(f"face: {p} ({face_img.width}x{face_img.height})")

    for name, fn in CONCEPTS.items():
        if face_img is not None:
            render(name, fn, face_img, guide=False)
        else:
            render(name, fn, None, guide=False)
            render(name, fn, None, guide=True)

    print(f"\n{OUT}")
    print("Check each at 20% zoom. If the words aren't readable there, they "
          "won't be readable in the feed.")
