#!/usr/bin/env python3
"""Channel-intro thumbnail — a stack, and my stack.

The literal reading of the channel name, and the one that needs no interpreting:
a tidy technology stack beside the one you actually end up with. Layers are
different widths, offset, tilted, one is not even a rectangle, and the top one is
sliding off.

It works at feed size because the joke is carried by the SILHOUETTE, not by any
text. Two towers, one tidy, one about to fall over — that survives being scaled to
320px in a way that a labelled diagram does not. The labels are a bonus for people
who stop.

    python3 build_thumbnail_stack.py
    .venv/bin/python canvas/render_png.py canvas/thumbnail_stack.excalidraw \\
        -o youtube/thumbnails/channel_stack.png
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excalidraw_kit import *  # noqa: F401,F403

NAVY = "#0d1a29"
GRIDL = "#16293d"
PANEL = "#15293e"
CYAN = "#7fd4ff"
CYAN_D = "#3f7ea3"
TXT = "#eaf6ff"
AMBER = "#ffb84d"
CORAL = "#ff7f6e"
MINT = "#5fe0b0"
VIOLET = "#b39dff"

cv = Canvas()
sc = cv.scene("Channel thumbnail — a stack vs my stack")

sc.add(box(0, 0, 1600, 900, bg=NAVY, stroke="transparent", sw=1, roundness=None))
for gx in range(0, 1601, 50):
    sc.add(line([(gx, 0), (gx, 900)], stroke=GRIDL, sw=1))
for gy in range(0, 901, 50):
    sc.add(line([(0, gy), (1600, gy)], stroke=GRIDL, sw=1))

sc.add(text(60, 48, "THE UNPLANNED STACK", 74, HAND, TXT))
sc.add(line([(64, 158), (900, 162)], stroke=AMBER, sw=7))

# ------------------------------------------------------------- a tidy stack
sc.add(text(250, 232, "a stack", 34, CODE, CYAN_D))
for i, name in enumerate(["framework", "database", "infra", "deploy"]):
    sc.add(box(180, 316 + i * 122, 400, 106, name, 30, HAND, bg=PANEL,
               stroke=CYAN, sw=3, label_color=TXT))
sc.add(text(180, 828, "chosen. in order.", 30, HAND, CYAN_D))

# divider, so the two read as a comparison rather than one wide picture
sc.add(line([(700, 240), (700, 820)], stroke=GRIDL, sw=3, dash="dashed"))

# --------------------------------------------------------------- my stack
sc.add(text(980, 232, "my stack", 34, CODE, AMBER))
# Top of the tower first, so the wonkiest piece is the one about to slide off.
mine = [
    ("???",           1150, 220, VIOLET, -0.150),
    ("making videos",  880, 440, AMBER,   0.045),
    ("a new country", 1060, 320, CORAL,  -0.060),
    ("software",       900, 430, MINT,    0.020),
]
for i, (name, x, wid, colour, ang) in enumerate(mine):
    sc.add(box(x, 316 + i * 122, wid, 106, name, 28, HAND, bg=PANEL,
               stroke=colour, sw=3, label_color=TXT, angle=ang))
sc.add(text(880, 828, "none of it chosen.", 30, HAND, CORAL))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "thumbnail_stack.excalidraw")
print(f"thumbnail_stack.excalidraw: {cv.save(out)} elements")
