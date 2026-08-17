#!/usr/bin/env python3
"""Turn a photo into a flat, ink-outlined cartoon sticker with a transparent
background — the presenter cutout used by the thumbnails.

This is stylisation, not illustration: no drawing happens, the photo is flattened
to a small palette and given outlines. It reads as a comic sticker rather than a
photo, which is what the hand-drawn thumbnails need.

    .venv/bin/python youtube/cartoonify.py assets/photo_source.png

Steps:
  1. key out the smooth studio background and keep the largest connected region
  2. heavy edge-preserving smoothing, so skin becomes flat areas not noise
  3. quantise to a small palette, then push saturation and contrast
  4. derive ink lines from local contrast and multiply them back on
  5. add a thick white sticker rim and a soft drop shadow
"""

import argparse
import os
import sys
from collections import deque

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
INK = (36, 38, 48)


def keyed_alpha(img, bg_blue_min=140, bg_dominance=42, feather=1.4):
    """Alpha mask that drops a blue/cyan studio backdrop.

    Rule: background is bright and blue-dominant. A navy hoodie is also
    blue-dominant but *dark*, so the brightness floor keeps it. Only the region
    connected to the image corners is removed, so a blue highlight on clothing
    is never punched out.
    """
    w, h = img.size
    r, g, b = img.convert("RGB").split()
    # Channel arithmetic rather than a per-pixel Python loop.
    bright = b.point(lambda v: 255 if v >= bg_blue_min else 0)
    blueish = ImageChops.subtract(b, r).point(
        lambda v: 255 if v >= bg_dominance else 0)
    greenish = g.point(lambda v: 255 if v >= 80 else 0)
    cand = ImageChops.multiply(ImageChops.multiply(bright, blueish), greenish)

    # Keep only the background region connected to an edge, so a blue highlight
    # on clothing is never punched out.
    flags = bytearray(cand.tobytes())
    seen = bytearray(w * h)
    q = deque()
    for sx, sy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
                   (w // 2, 0), (0, h // 2), (w - 1, h // 2)):
        i = sy * w + sx
        if flags[i] and not seen[i]:
            seen[i] = 1
            q.append(i)
    while q:
        i = q.popleft()
        x = i % w
        for j, ok in ((i + 1, x + 1 < w), (i - 1, x > 0),
                      (i + w, i + w < w * h), (i - w, i >= w)):
            if ok and flags[j] and not seen[j]:
                seen[j] = 1
                q.append(j)

    alpha = Image.frombytes("L", (w, h), bytes(seen)).point(
        lambda v: 0 if v else 255)
    return alpha.filter(ImageFilter.GaussianBlur(feather))


def flatten(img, smooth=9, colours=26, saturation=1.28, contrast=1.0,
            shrink=0.4):
    """Edge-preserving smoothing, then a flat palette.

    The shrink/expand pass is the important one: it destroys skin texture while
    keeping large shapes, so quantising afterwards produces smooth flat regions
    instead of the blotches you get from quantising a noisy photo.
    """
    out = img.convert("RGB")
    for size in (smooth, max(5, smooth - 2)):
        out = out.filter(ImageFilter.MedianFilter(size))
    small = out.resize((max(1, int(out.width * shrink)),
                        max(1, int(out.height * shrink))), Image.BILINEAR)
    out = Image.blend(out, small.resize(out.size, Image.BILINEAR), 0.62)
    out = out.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.SMOOTH_MORE)
    out = ImageEnhance.Color(out).enhance(saturation)
    if contrast != 1.0:
        out = ImageEnhance.Contrast(out).enhance(contrast)
    q = out.quantize(colors=colours, method=Image.MEDIANCUT, dither=Image.NONE)
    return q.convert("RGB").filter(ImageFilter.SMOOTH)


def silhouette(alpha, width=3):
    """The outline of the figure itself, from the alpha mask."""
    solid = alpha.point(lambda v: 255 if v > 128 else 0)
    eroded = solid
    for _ in range(max(1, width)):
        eroded = eroded.filter(ImageFilter.MinFilter(3))
    return ImageChops.subtract(solid, eroded).filter(
        ImageFilter.GaussianBlur(0.5))


def ink_lines(img, blur=2.6, threshold=11, thickness=3, presmooth=5):
    """Dark outlines from local contrast, as a white-on-black 'L' image.

    Run this on the ORIGINAL photo, not the flattened one — flattening removes
    the local contrast that the features live in, which leaves nothing to trace.
    """
    gray = img.convert("L").filter(ImageFilter.MedianFilter(presmooth))
    diff = ImageChops.difference(gray, gray.filter(ImageFilter.GaussianBlur(blur)))
    lines = diff.point(lambda v: 255 if v > threshold else 0)
    if thickness > 1:
        # MaxFilter needs an odd kernel.
        lines = lines.filter(ImageFilter.MaxFilter(
            thickness if thickness % 2 else thickness + 1))
    return lines.filter(ImageFilter.GaussianBlur(0.6))


def sticker(rgba, rim=14, shadow=10, rim_colour=(255, 255, 255)):
    """Thick outline plus soft shadow — what makes it read as a sticker."""
    a = rgba.split()[3]
    grown = a
    for _ in range(rim):
        grown = grown.filter(ImageFilter.MaxFilter(3))
    grown = grown.point(lambda v: 255 if v > 40 else 0).filter(
        ImageFilter.GaussianBlur(1.0))

    pad = rim + shadow + 12
    w, h = rgba.size
    out = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))

    shade = grown.filter(ImageFilter.GaussianBlur(shadow)).point(
        lambda v: int(v * 0.42))
    dark = Image.new("RGBA", (w, h), (20, 22, 30, 255))
    dark.putalpha(shade)
    out.alpha_composite(dark, (pad + 5, pad + 8))

    rim_img = Image.new("RGBA", (w, h), rim_colour + (255,))
    rim_img.putalpha(grown)
    out.alpha_composite(rim_img, (pad, pad))
    out.alpha_composite(rgba, (pad, pad))
    return out


def cartoonify(path, scale=2, **kw):
    src = Image.open(path).convert("RGB")
    if scale != 1:  # work large, so ink lines stay crisp when placed
        src = src.resize((src.width * scale, src.height * scale), Image.LANCZOS)

    alpha = keyed_alpha(src, feather=kw.get("feather", 1.4 * scale))
    flat = flatten(src, smooth=kw.get("smooth", 9) * scale // 2 * 2 + 1,
                   colours=kw.get("colours", 26))
    # Features traced from the original; colour taken from the flattened version.
    lines = ink_lines(src, blur=kw.get("blur", 3.0) * scale,
                      threshold=kw.get("threshold", 16),
                      thickness=kw.get("thickness", 3))
    lines = ImageChops.lighter(lines, silhouette(alpha,
                                                 kw.get("contour", 3) * scale // 2))

    ink = Image.new("RGB", flat.size, INK)
    flat = Image.composite(ink, flat, lines.point(lambda v: 255 if v > 110 else 0))

    rgba = flat.convert("RGBA")
    rgba.putalpha(alpha)
    return sticker(rgba, rim=kw.get("rim", 14) * scale // 2,
                   shadow=kw.get("shadow", 10) * scale // 2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("-o", "--out", default=os.path.join(HERE, "assets",
                                                        "presenter_cartoon.png"))
    ap.add_argument("--colours", type=int, default=14)
    ap.add_argument("--threshold", type=int, default=11)
    ap.add_argument("--thickness", type=int, default=3)
    ap.add_argument("--no-rim", action="store_true")
    a = ap.parse_args()

    p = a.photo if os.path.isabs(a.photo) else os.path.join(HERE, a.photo)
    if not os.path.exists(p):
        sys.exit(f"no such file: {p}")

    img = cartoonify(p, colours=a.colours, threshold=a.threshold,
                     thickness=a.thickness, rim=0 if a.no_rim else 14)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    img.save(a.out)
    print(f"{a.out}  {img.width}x{img.height}")
