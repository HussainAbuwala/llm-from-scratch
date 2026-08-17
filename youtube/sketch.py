"""Hand-drawn drawing primitives for Pillow.

Every stroke is drawn as two slightly-different bowed passes with jittered
endpoints — the same trick Rough.js and Excalidraw use. The result reads as
marker on paper rather than as vector output, which is the whole point: the
series is presented on a hand-drawn canvas, so the thumbnails should look drawn
too.

All randomness comes from a seeded `random.Random`, so renders are reproducible.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFilter

F = "/System/Library/Fonts/Supplemental/"
MARKER = "/System/Library/Fonts/MarkerFelt.ttc"      # face 1 = Wide
NOTE = "/System/Library/Fonts/Noteworthy.ttc"        # face 1 = Bold
CHALK = F + "ChalkboardSE.ttc"                       # face 2 = Bold
BRADLEY = F + "Bradley Hand Bold.ttf"

PAPER = (251, 247, 236)
GRID = (206, 216, 226)
PENCIL = (60, 66, 78)


def rng_for(seed):
    return random.Random(seed)


def _bezier(p0, p1, p2, steps=18):
    out = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        out.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return out


def rough_line(d, p1, p2, fill, width=6, rng=None, passes=2, jitter=2.6):
    """One hand-drawn stroke: a couple of bowed passes that don't quite align."""
    rng = rng or random
    for _ in range(passes):
        j = jitter
        a = (p1[0] + rng.uniform(-j, j), p1[1] + rng.uniform(-j, j))
        b = (p2[0] + rng.uniform(-j, j), p2[1] + rng.uniform(-j, j))
        mid = ((a[0] + b[0]) / 2 + rng.uniform(-j, j) * 1.8,
               (a[1] + b[1]) / 2 + rng.uniform(-j, j) * 1.8)
        d.line(_bezier(a, mid, b), fill=fill, width=width, joint="curve")


def rough_rect(d, box, fill_colour=None, outline=PENCIL, width=5, rng=None,
               jitter=2.6):
    x0, y0, x1, y1 = box
    rng = rng or random
    if fill_colour:
        j = jitter * 0.8
        poly = [(x0 + rng.uniform(-j, j), y0 + rng.uniform(-j, j)),
                (x1 + rng.uniform(-j, j), y0 + rng.uniform(-j, j)),
                (x1 + rng.uniform(-j, j), y1 + rng.uniform(-j, j)),
                (x0 + rng.uniform(-j, j), y1 + rng.uniform(-j, j))]
        d.polygon(poly, fill=fill_colour)
    if outline:
        for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                     ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
            rough_line(d, a, b, outline, width, rng, jitter=jitter)


def rough_ellipse(d, box, outline=PENCIL, width=5, rng=None, jitter=4.0):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    rng = rng or random
    for _ in range(2):
        pts, start = [], rng.uniform(0, 0.4)
        steps = 44
        for i in range(steps + 1):
            a = start + i / steps * math.tau * 1.03
            pts.append((cx + math.cos(a) * (rx + rng.uniform(-jitter, jitter)),
                        cy + math.sin(a) * (ry + rng.uniform(-jitter, jitter))))
        d.line(pts, fill=outline, width=width, joint="curve")


def rough_arrow(d, p1, p2, fill=PENCIL, width=5, rng=None, head=20,
                spread=0.42):
    """Line with a hand-drawn head at p2.

    `spread` is the half-angle of the barbs, in radians, measured BACK along the
    shaft. It has to be small (~0.4); a large value swings the barbs past the tip
    and the result reads as a blunt fork rather than an arrow.
    """
    rough_line(d, p1, p2, fill, width, rng)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    for off in (spread, -spread):
        tip = (p2[0] - math.cos(ang + off) * head,
               p2[1] - math.sin(ang + off) * head)
        rough_line(d, p2, tip, fill, width, rng, passes=1, jitter=1.4)


def scribble_out(d, box, fill, width=8, rng=None, loops=7):
    """A crossing-out scribble, the way you'd strike a line of code."""
    x0, y0, x1, y1 = box
    rng = rng or random
    pts, steps = [], loops * 2
    for i in range(steps + 1):
        t = i / steps
        pts.append((x0 + (x1 - x0) * t,
                    (y0 if i % 2 else y1) + rng.uniform(-4, 4)))
    d.line(pts, fill=fill, width=width, joint="curve")


def paper(img, grid=26, tint=PAPER, line=GRID, noise=True):
    """Graph-paper background with a little grain, so it isn't flat colour."""
    w, h = img.size
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, h], fill=tint)
    for x in range(0, w, grid):
        d.line([(x, 0), (x, h)], fill=line, width=1)
    for y in range(0, h, grid):
        d.line([(0, y), (w, y)], fill=line, width=1)
    if noise:
        grain = Image.effect_noise((w, h), 14).convert("L")
        img.paste(Image.composite(
            Image.new("RGB", (w, h), (255, 255, 255)), img,
            grain.point(lambda v: 20 if v > 150 else 0)), (0, 0),
            grain.point(lambda v: 16 if v > 150 else 0))
    return d


def highlight(img, box, colour=(255, 224, 90), alpha=140, rng=None, wobble=6):
    """Marker highlight that overshoots the text, like a real one does."""
    rng = rng or random
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    top = [(x, y0 + rng.uniform(-wobble, wobble)) for x in range(int(x0), int(x1), 40)]
    bot = [(x, y1 + rng.uniform(-wobble, wobble)) for x in range(int(x1), int(x0), -40)]
    if len(top) > 1 and len(bot) > 1:
        ld.polygon(top + bot, fill=colour + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(1.2))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"),
              (0, 0))


def sticky(img, x, y, w, h, colour, angle, label=None, font=None,
           label_fill=PENCIL, rng=None):
    """A rotated sticky note with a soft shadow.

    The label is drawn *before* the rotation so the writing tilts with the note —
    level text on a tilted note is the giveaway that it was composited.
    """
    pad = 30
    layer = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([pad + 5, pad + 7, pad + w + 5, pad + h + 7], fill=(0, 0, 0, 46))
    ld.rectangle([pad, pad, pad + w, pad + h], fill=colour + (255,))
    if label and font:
        ld.text((pad + w / 2, pad + h / 2), label, font=font,
                fill=label_fill + (255,), anchor="mm")
    layer = layer.filter(ImageFilter.GaussianBlur(1.0)).rotate(
        angle, resample=Image.BICUBIC, expand=False)
    img.paste(Image.alpha_composite(
        img.convert("RGBA").crop((x - pad, y - pad,
                                  x - pad + layer.width, y - pad + layer.height)),
        layer).convert("RGB"), (x - pad, y - pad))
    return (x + w / 2, y + h / 2)
