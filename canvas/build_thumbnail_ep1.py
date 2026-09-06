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

PEACH = "#f9d6a7"
WHITE = "#fffdf8"

# Flat background. No paper texture, gradients, shadows, or 3D treatment.
sc.add(box(0, 0, 1600, 900, bg=PEACH, stroke="transparent", sw=1,
           roundness=None))

# Hook: intentionally spare and slightly asymmetrical, like a real board.
sc.add(text(70, 130, "JUST", 152, HAND))
sc.add(box(60, 330, 155, 205, bg=WHITE, stroke="transparent", sw=1,
           roundness=None))
sc.add(text(72, 318, "2", 205, HAND, BLUE))
sc.add(text(245, 356, "NAMES?", 126, HAND))
sc.add(line([(72, 560), (690, 536)], stroke=VIOLET, sw=4))

# The complete story on the right: two training names, one tiny model, one new
# possible output. The boxes are flat Excalidraw elements, not paper cut-outs.
sc.add(box(850, 105, 290, 112, "anna", 54, HAND, bg=BG_BLUE, sw=3))
sc.add(box(1220, 105, 270, 112, "ava", 54, HAND, bg=BG_VIOLET, sw=3))

sc.add(arrow(995, 230, 1090, 345, stroke=VIOLET, sw=4))
sc.add(arrow(1355, 230, 1270, 345, stroke=VIOLET, sw=4))

sc.add(box(965, 350, 440, 160, "MODEL", 58, HAND, bg=BG_VIOLET, sw=3))
sc.add(arrow(1185, 525, 1185, 635, stroke=VIOLET, sw=4))
sc.add(box(1025, 650, 320, 135, "ana", 68, HAND, bg=BG_GREEN, sw=3))

# Small hand-drawn emphasis marks around the generated result.
sc.add(line([(985, 684), (948, 666)], stroke=BLACK, sw=4))
sc.add(line([(980, 720), (936, 720)], stroke=BLACK, sw=4))
sc.add(line([(1385, 684), (1422, 666)], stroke=BLACK, sw=4))
sc.add(line([(1390, 720), (1434, 720)], stroke=BLACK, sw=4))

sc.add(text(70, 822, "LLM FROM SCRATCH  ·  EP 01", 30, CODE, RED))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "thumbnail_ep1.excalidraw")
print(f"thumbnail_ep1.excalidraw: {cv.save(out)} elements")
