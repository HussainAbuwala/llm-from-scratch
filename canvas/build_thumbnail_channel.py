#!/usr/bin/env python3
"""Thumbnail for the channel intro — The Unplanned Stack.

Blueprint themed, to match the video it fronts. The hero is the channel's whole
thesis as one picture: a neat dashed line labelled "the plan", and the actual
route thrashing all over it between the same two points. It reads instantly at
feed size, which is where the decision gets made, and it is funnier than any
sentence about curiosity would be.

    python3 build_thumbnail_channel.py
    .venv/bin/python canvas/render_png.py canvas/thumbnail_channel.excalidraw \\
        -o youtube/thumbnails/channel_intro.png

Final upload is better exported from Excalidraw itself (select frame →
Export image → PNG, "only selected") for the real strokes and font.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excalidraw_kit import *  # noqa: F401,F403

NAVY = "#0d1a29"
GRIDL = "#16293d"
CYAN = "#7fd4ff"
CYAN_D = "#3f7ea3"
TXT = "#eaf6ff"
AMBER = "#ffb84d"
CORAL = "#ff7f6e"

cv = Canvas()
sc = cv.scene("Channel intro thumbnail 16:9")

sc.add(box(0, 0, 1600, 900, bg=NAVY, stroke="transparent", sw=1, roundness=None))

# Blueprint grid. Cheap texture that survives being scaled down to a feed.
for gx in range(0, 1601, 50):
    sc.add(line([(gx, 0), (gx, 900)], stroke=GRIDL, sw=1))
for gy in range(0, 901, 50):
    sc.add(line([(0, gy), (1600, gy)], stroke=GRIDL, sw=1))

# ------------------------------------------------------------------- wordmark
sc.add(text(64, 74, "THE UNPLANNED", 104, HAND, TXT))
sc.add(text(64, 200, "STACK", 104, HAND, CYAN))
sc.add(line([(68, 336), (620, 340)], stroke=AMBER, sw=8))

# --------------------------------------------------- the plan vs what happened
# Both routes run between the same two points. That is the whole joke, and it
# survives being scaled down to a 320px feed thumbnail, which is the only size
# that matters for the click.
START, END = (140, 660), (1400, 660)

sc.add(line([START, END], stroke=CYAN_D, sw=4, dash="dashed"))

wander = [START, (220, 560), (300, 720), (400, 476), (518, 740), (635, 520),
          (736, 792), (856, 456), (962, 664), (1071, 508), (1188, 726),
          (1297, 574), END]
sc.add(line(wander, stroke=AMBER, sw=7))

for pt in (START, END):
    sc.add(ellipse(pt[0] - 16, pt[1] - 16, 32, 32, bg=CORAL, stroke=CORAL, sw=2))
sc.add(text(92, 596, "start", 24, CODE, CORAL))
sc.add(text(1356, 700, "now", 24, CODE, CORAL))

# A legend, as any drawing would have. Keeps the labels off the lines entirely
# and fills the right-hand space the wordmark leaves empty.
sc.add(line([(1108, 330), (1188, 330)], stroke=CYAN_D, sw=4, dash="dashed"))
sc.add(text(1208, 312, "the plan", 30, CODE, CYAN_D))
sc.add(line([(1108, 392), (1128, 366), (1148, 414), (1168, 372), (1188, 392)],
            stroke=AMBER, sw=6))
sc.add(text(1208, 374, "what happened", 30, CODE, AMBER))

# ---------------------------------------------------------------- title block
sc.add(box(64, 764, 440, 100, bg="#15293e", stroke=CYAN_D, sw=2))
sc.add(text(88, 780, "THE UNPLANNED STACK", 24, CODE, TXT))
sc.add(text(88, 816, "channel intro · rev 01", 18, CODE, CYAN_D))
sc.add(text(88, 840, "scale: not to scale", 18, CODE, AMBER))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "thumbnail_channel.excalidraw")
print(f"thumbnail_channel.excalidraw: {cv.save(out)} elements")
