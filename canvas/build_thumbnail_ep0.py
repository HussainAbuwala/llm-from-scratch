#!/usr/bin/env python3
"""Thumbnail for video 0, built as a real Excalidraw scene.

Drawn in Excalidraw rather than in Pillow so the strokes, fills and font are the
genuine article and the thumbnail matches the canvases the videos are presented
on.

The hero is a drawing of the machine itself: text goes in at the top, a cut-open
box shows layers of connected units inside, and next-token probabilities come out
at the bottom. That is the honest picture of what an LLM is, and it states the
series thesis — the box gets opened — without a word of explanation.

    python3 build_thumbnail_ep0.py

Then in Excalidraw: open the file, select the frame, and use
Export image → PNG with "only selected" ticked. The frame is 16:9, so a 1x export
is 1600x900, comfortably above YouTube's 1280x720 minimum.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excalidraw_kit import *  # noqa: F401,F403

cv = Canvas()
sc = cv.scene("EP0 thumbnail 16:9")

# Channel banner background, sampled from the banner artwork itself, so the
# thumbnail and the channel header sit on the same ground.
BANNER = "#f9d6a7"

sc.add(box(0, 0, 1600, 900, bg=BANNER, stroke="transparent", sw=1,
           roundness=None))

# ----------------------------------------------------------------- left column
# Highlight goes in first: element order is z-order. White rather than yellow —
# on peach, white is the higher-contrast marker, and it echoes the white glow
# behind the banner logo.
sc.add(box(52, 452, 452, 104, bg="#ffffff", stroke="transparent", sw=1,
           roundness=None))
sc.add(text(60, 168, "what's", 112, HAND))
sc.add(text(60, 300, "actually", 112, HAND))
sc.add(text(60, 432, "inside?", 112, HAND, BLUE))

sc.add(text(60, 636, "we build", 42, HAND, VIOLET))
sc.add(text(60, 686, "all of this", 42, HAND, VIOLET))
# The arrow itself is added last, so its head sits ON TOP of the machine's white
# fill instead of being painted over by it.

sc.add(text(60, 828, "LLM FROM SCRATCH  ·  EP 0", 32, CODE, RED))

# --------------------------------------------------------------- the machine
# in: a prompt
sc.add(box(700, 116, 840, 80, "The cat sat on the ___", 32, CODE, bg="#ffffff"))
sc.add(arrow(1120, 202, 1120, 252, sw=3))

# the box, cut open so the insides show
sc.add(box(700, 258, 840, 382, bg="#ffffff", sw=3))
sc.add(box(716, 274, 154, 64, "LLM", 32, HAND, label_color="#ffffff",
           bg="#1e1e1e"))

# layers of units, connected. Three columns of three reads as a network at
# thumbnail size; more detail turns to mush once YouTube scales it down.
cols = [(900, BG_BLUE), (1120, BG_GREEN), (1340, BG_VIOLET)]
rows = [400, 492, 584]
R = 38
for ci, (cx, colour) in enumerate(cols):
    if ci == 0:
        continue
    px = cols[ci - 1][0]
    for ry in rows:            # connections first, so units sit on top
        for py in rows:
            sc.add(line([(px + R, py), (cx - R, ry)], stroke=GRAY, sw=2))
for cx, colour in cols:
    for cy in rows:
        sc.add(ellipse(cx - R, cy - R, R * 2, R * 2, bg=colour, sw=2))

sc.add(arrow(1120, 648, 1120, 694, sw=3))

# out: a distribution over the next token
bars = [("mat", 420, BG_YELLOW), ("floor", 248, BG_BLUE), ("chair", 104, "#ffffff")]
for i, (label, w, colour) in enumerate(bars):
    y = 700 + i * 58
    sc.add(text(700, y + 8, label, 26, CODE, GRAY))
    sc.add(box(900, y, w, 46, bg=colour, sw=2))

sc.add(arrow(320, 726, 828, 596, stroke=VIOLET, sw=3))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "thumbnail_ep0.excalidraw")
print(f"thumbnail_ep0.excalidraw: {cv.save(out)} elements")
