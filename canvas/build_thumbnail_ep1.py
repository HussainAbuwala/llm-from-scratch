#!/usr/bin/env python3
"""Build the Episode 1 thumbnail as a native Excalidraw scene.

The design deliberately uses the same flat fills, handwriting, and rough strokes
as the presenter canvas. Open the generated file in Excalidraw for final manual
tweaks or export the single 1600x900 frame as PNG.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excalidraw_kit import *  # noqa: F401,F403


cv = Canvas()
sc = cv.scene("Episode 01 thumbnail")

NAVY = "#0b1733"
OFF_WHITE = "#fff9e8"
MINT = "#69db9c"
CYAN = "#74c0fc"

# Flat dark background distinguishes this episode from Episode 0's peach.
sc.add(box(0, 0, 1600, 900, bg=NAVY, stroke="transparent", sw=1,
           roundness=None))

# The thumbnail repeats the video's central promise in plain language.
sc.add(text(70, 105, "I BUILT THE", 78, HAND, OFF_WHITE))
sc.add(text(70, 205, "SMALLEST", 128, HAND, MINT))
sc.add(text(70, 365, "LANGUAGE", 102, HAND, OFF_WHITE))
sc.add(text(70, 490, "MODEL", 118, HAND, OFF_WHITE))
sc.add(line([(72, 636), (650, 612)], stroke=CYAN, sw=5))

# The complete story on the right: two inputs, the entire 4x4 model, one output.
sc.add(box(880, 90, 270, 100, "anna", 48, HAND, bg=BG_BLUE, sw=3))
sc.add(box(1230, 90, 250, 100, "ava", 48, HAND, bg=BG_VIOLET, sw=3))

sc.add(arrow(1015, 205, 1100, 300, stroke=CYAN, sw=4))
sc.add(arrow(1355, 205, 1270, 300, stroke=CYAN, sw=4))

sc.add(box(900, 310, 570, 295, bg=OFF_WHITE, sw=3))
sc.add(text(950, 338, "THE WHOLE MODEL", 36, HAND, VIOLET))
sc.add(text(965, 405, "      a     n     v    END", 24, CODE, GRAY))
sc.add(text(965, 450, "START  1.00  0     0     0", 24, CODE))
sc.add(text(965, 490, "a      0     .25   .25   .50", 24, CODE))
sc.add(text(965, 530, "n      .50   .50   0     0", 24, CODE))
sc.add(text(965, 570, "v      1.00  0     0     0", 24, CODE))
sc.add(arrow(1185, 620, 1185, 682, stroke=CYAN, sw=4))
sc.add(box(1035, 700, 300, 112, "ana", 62, HAND, bg=BG_GREEN, sw=3))

# Small hand-drawn emphasis marks around the generated result.
sc.add(line([(995, 726), (958, 710)], stroke=OFF_WHITE, sw=4))
sc.add(line([(992, 760), (950, 760)], stroke=OFF_WHITE, sw=4))
sc.add(line([(1375, 726), (1412, 710)], stroke=OFF_WHITE, sw=4))
sc.add(line([(1378, 760), (1420, 760)], stroke=OFF_WHITE, sw=4))

sc.add(text(70, 825, "LLM FROM SCRATCH  ·  EP 01", 30, CODE, CYAN))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "thumbnail_ep1.excalidraw")
print(f"thumbnail_ep1.excalidraw: {cv.save(out)} elements")
