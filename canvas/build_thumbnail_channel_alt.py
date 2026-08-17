#!/usr/bin/env python3
"""Alternative channel-intro thumbnail — the stack TRACE.

The first version reads "stack" as a set of chosen technologies. This one reads
it the other way a developer hears the word: a stack trace, the thing you get
when something did not go to plan. Same channel name, different pun, and it says
"figuring it out" without needing a metaphor explained.

Text-based, so it stays legible when scaled to a feed. The traceback frames are
deliberately small — they are texture — and the error line is the thing that has
to read at 320px.
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
sc = cv.scene("Channel intro thumbnail — stack trace")

sc.add(box(0, 0, 1600, 900, bg=NAVY, stroke="transparent", sw=1, roundness=None))
for gx in range(0, 1601, 50):
    sc.add(line([(gx, 0), (gx, 900)], stroke=GRIDL, sw=1))
for gy in range(0, 901, 50):
    sc.add(line([(0, gy), (1600, gy)], stroke=GRIDL, sw=1))

sc.add(text(70, 62, "THE UNPLANNED STACK", 34, CODE, CYAN))
sc.add(line([(72, 112), (582, 114)], stroke=AMBER, sw=5))

# The frames. Small on purpose — nobody reads these in a feed, they just make it
# unmistakably a traceback.
trace = [
    "Traceback (most recent call last):",
    "  File \"life.py\", line 1997, in <module>",
    "    grow_up(curious=True)",
    "  File \"life.py\", line 2016, in university",
    "    study(computer_science)",
    "  File \"life.py\", line 2021, in career",
    "    build(software)",
    "  File \"life.py\", line 2024, in canada",
    "    start_over()",
]
for i, ln in enumerate(trace):
    colour = CYAN_D if i % 2 else "#5f92b0"
    sc.add(text(80, 186 + i * 34, ln, 25, CODE, colour))

# The punchline, and the only part that has to survive being shrunk.
sc.add(text(76, 526, "UnplannedStackError:", 70, CODE, CORAL))
sc.add(text(76, 622, "no blueprint found", 70, CODE, AMBER))

sc.add(text(76, 758, "…so I'm figuring it out on camera.", 36, HAND, TXT))

sc.add(box(1114, 762, 440, 82, bg="#15293e", stroke=CYAN_D, sw=2))
sc.add(text(1138, 778, "THE UNPLANNED STACK", 24, CODE, TXT))
sc.add(text(1138, 814, "channel intro · rev 01", 18, CODE, CYAN_D))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "thumbnail_channel_alt.excalidraw")
print(f"thumbnail_channel_alt.excalidraw: {cv.save(out)} elements")
