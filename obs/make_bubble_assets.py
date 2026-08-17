#!/usr/bin/env python3
"""Generate webcam-bubble assets for OBS.

OBS has no circular-crop or border filter, so the round bubble is made with:

  bubble_mask.png   -> Image Mask/Blend filter on the webcam source
                       (mask type: "Alpha Mask (Alpha Channel)")
  bubble_ring_*.png -> a separate Image source placed on top of the webcam,
                       giving the bubble a coloured rim and a soft shadow

Writes PNGs with the standard library only - no Pillow required.

    python3 make_bubble_assets.py
"""

import os
import struct
import zlib

SIZE = 1024
RINGS = {
    "blue": (0x19, 0x71, 0xC2),
    "orange": (0xF0, 0x8C, 0x00),
}

RADIUS = 452.0        # bubble radius
RING_W = 13.0         # rim thickness
SHADOW = 46.0         # soft shadow reach beyond the rim
SHADOW_A = 0.34       # shadow strength at the rim


def write_png(path, width, height, rows):
    raw = b"".join(b"\x00" + row for row in rows)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)


def cover(edge_distance):
    """Antialiased coverage: 1 inside, 0 outside, ramped over one pixel."""
    return min(1.0, max(0.0, edge_distance + 0.5))


def build(kind, rgb=None):
    c = SIZE / 2.0
    rows = []
    for y in range(SIZE):
        row = bytearray()
        dy = y + 0.5 - c
        for x in range(SIZE):
            dx = x + 0.5 - c
            d = (dx * dx + dy * dy) ** 0.5

            if kind == "mask":
                # White inside, black outside, alpha matching. Encoding the
                # circle in BOTH the colour and the alpha channel means the mask
                # works whichever Image Mask/Blend type is selected in OBS
                # ("Alpha Mask (Alpha Channel)" or "(Colour Channel)").
                v = int(cover(RADIUS - d) * 255 + 0.5)
                row += bytes((v, v, v, v))
            else:
                ring = min(cover(RADIUS - d), cover(d - (RADIUS - RING_W)))
                if ring > 0.002:
                    a = ring
                    r, g, b = rgb
                else:
                    t = (d - RADIUS) / SHADOW
                    a = SHADOW_A * (1.0 - t) ** 2 if 0.0 <= t <= 1.0 else 0.0
                    r = g = b = 0
                row += bytes((r, g, b, int(a * 255 + 0.5)))
        rows.append(bytes(row))
    return rows


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    write_png(os.path.join(here, "bubble_mask.png"), SIZE, SIZE, build("mask"))
    print("bubble_mask.png")
    for name, rgb in RINGS.items():
        write_png(os.path.join(here, f"bubble_ring_{name}.png"), SIZE, SIZE,
                  build("ring", rgb))
        print(f"bubble_ring_{name}.png")
