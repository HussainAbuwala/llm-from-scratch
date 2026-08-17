#!/usr/bin/env python3
"""Canvas for the channel intro video — The Unplanned Stack.

Built as a MAP rather than a deck. Three things do that work:

1. Shots are laid out serpentine across one large world, and the connecting route
   is drawn in the gaps BETWEEN them. Zoom out and the canvas is one territory;
   zoom into a shot and it is a clean frame. Pulling back mid-video becomes a
   usable beat rather than an accident.
2. Shots vary in size. All are 16:9, but the establishing shot is 2x, so its
   content is drawn at 2x and reads as genuinely further away.
3. A route indicator in the corner of every shot advances one station at a time,
   so consecutive shots are visibly part of one journey.

Theme is a wandering blueprint — the joke being a channel whose whole premise is
not having a fixed one. Navy ground, cyan construction lines, dimension ticks,
callout bubbles, a title block. There is deliberately no heading/subtitle
template: each shot is composed differently, because identical furniture in the
same position every time is most of what makes a canvas feel like slides.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import excalidraw_kit as K
from excalidraw_kit import *  # noqa: F401,F403

# ------------------------------------------------------------------- palette
NAVY = "#0d1a29"
PANEL = "#15293e"
CYAN = "#7fd4ff"
CYAN_D = "#3f7ea3"
TXT = "#dceefb"
DIM = "#8fb2c9"
AMBER = "#ffb84d"
CORAL = "#ff7f6e"
MINT = "#5fe0b0"

STATIONS = 11  # detail shots, for the route indicator


class World:
    def __init__(self):
        self.els = []

    def add(self, *items):
        for it in items:
            for el in (it if isinstance(it, list) else [it]):
                self.els.append(el)
        return self

    def shot(self, name, x, y, w=1600, station=None):
        return Shot(self, name, x, y, w, station)

    def save(self, path):
        doc = {"type": "excalidraw", "version": 2,
               "source": "https://excalidraw.com", "elements": self.els,
               "appState": {"gridSize": None, "viewBackgroundColor": NAVY},
               "files": {}}
        with open(path, "w") as fh:
            json.dump(doc, fh, indent=1)
        return len(self.els)


class Shot:
    """One camera position. Authored in local 1600x900 coords whatever its size."""

    def __init__(self, world, name, x, y, w, station):
        h = round(w * 9 / 16)
        fr = K._base("frame", x, y, w, h, stroke="#24445e", bg="transparent",
                     roundness=None, roughness=0)
        fr.update({"type": "frame", "name": name})
        world.els.append(fr)
        self.world, self.fid = world, fr["id"]
        self.ox, self.oy, self.k = x, y, w / 1600.0
        self.add(box(0, 0, 1600, 900, bg=NAVY, stroke="transparent", sw=1,
                     roundness=None))
        if station is not None:
            self.route_marker(station)

    def add(self, *items):
        for it in items:
            for el in (it if isinstance(it, list) else [it]):
                el["x"] = self.ox + el["x"] * self.k
                el["y"] = self.oy + el["y"] * self.k
                el["width"] *= self.k
                el["height"] *= self.k
                if "points" in el:
                    el["points"] = [[px * self.k, py * self.k]
                                    for px, py in el["points"]]
                if "fontSize" in el:
                    el["fontSize"] = el["fontSize"] * self.k
                el["frameId"] = self.fid
                self.world.els.append(el)
        return self

    # -- blueprint vocabulary ---------------------------------------------

    def route_marker(self, station):
        """Where we are on the route — the strongest continuity device here."""
        x0, y, step = 1150, 66, 34
        self.add(line([(x0, y), (x0 + step * (STATIONS - 1), y)],
                      stroke=CYAN_D, sw=1, dash="dotted"))
        for i in range(STATIONS):
            here = i == station
            r = 11 if here else 5
            self.add(ellipse(x0 + i * step - r, y - r, r * 2, r * 2,
                             bg=AMBER if here else NAVY,
                             stroke=AMBER if here else CYAN_D, sw=2))
        self.add(text(x0 - 96, y - 12, "route", 18, CODE, CYAN_D))

    def dim(self, x1, y1, x2, y2, label=None, colour=CYAN_D):
        """Dimension line with tick ends."""
        self.add(line([(x1, y1), (x2, y2)], stroke=colour, sw=1))
        for x in (x1, x2):
            self.add(line([(x, y1 - 9), (x, y1 + 9)], stroke=colour, sw=1))
        if label:
            self.add(text((x1 + x2) / 2 - len(label) * 4.6, y1 - 32, label, 17,
                          CODE, colour))

    def dashed(self, pts, colour=CYAN_D, sw=1):
        return self.add(line(pts, stroke=colour, sw=sw, dash="dashed"))

    def tick(self, x, y, s=10, colour=CYAN_D):
        self.add(line([(x - s, y), (x + s, y)], stroke=colour, sw=1))
        self.add(line([(x, y - s), (x, y + s)], stroke=colour, sw=1))

    def callout(self, cx, cy, r, colour=AMBER, label=None):
        self.add(ellipse(cx - r, cy - r, r * 2, r * 2, bg="transparent",
                         stroke=colour, sw=2, dash="dashed"))
        if label:
            self.add(text(cx - r + 10, cy + r + 12, label, 20, CODE, colour))

    def note(self, x, y, s, size=24, colour=DIM):
        return self.add(text(x, y, s, size, HAND, colour))

    def card(self, x, y, w, h, title=None, lines=None, colour=CYAN,
             title_size=30, size=22, fill=PANEL):
        self.add(box(x, y, w, h, bg=fill, stroke=colour, sw=2))
        if title:
            self.add(text(x + 24, y + 20, title, title_size, HAND, colour))
        if lines:
            self.add(text(x + 24, y + (76 if title else 24), "\n".join(lines),
                          size, HAND, TXT))
        return self


w = World()

# Ground plane behind everything, so pulling back stays navy rather than white.
w.add(box(-3000, -3600, 17000, 9800, bg=NAVY, stroke="transparent", sw=1,
          roundness=None))

GAP, ROW = 2100, 1700
AX = [0, GAP, GAP * 2, GAP * 3, GAP * 4]
ROW_A, ROW_B, ROW_C = 0, ROW, ROW * 2

# ============================================================ 00 · the map
s = w.shot("00 · THE MAP (wide)", 700, -2600, 3200)
s.add(text(90, 150, "THE UNPLANNED", 116, HAND, TXT))
s.add(text(90, 290, "STACK", 116, HAND, CYAN))
s.add(line([(94, 432), (690, 436)], stroke=AMBER, sw=7))
s.note(92, 476, "no fixed blueprint. just curiosity.", 34, DIM)
pts = [(1040, 350), (1150, 380), (1120, 520), (1260, 600), (1230, 730),
       (1420, 762), (1452, 620), (1548, 556)]
s.add(line(pts, stroke=CYAN_D, sw=3, dash="dotted"))
for px, py in pts[::2]:
    s.add(ellipse(px - 7, py - 7, 14, 14, bg=NAVY, stroke=CYAN, sw=2))
s.add(ellipse(1026, 336, 28, 28, bg=AMBER, stroke=AMBER, sw=2))
s.note(866, 396, "you are here", 22, AMBER)
for (lx, ly, lbl) in [(1048, 290, "who I am"), (1174, 364, "why I share it"),
                      (1000, 526, "the wall"), (1288, 586, "what changed"),
                      (1248, 752, "already up"), (1326, 516, "where it goes")]:
    s.add(text(lx, ly, lbl, 19, CODE, DIM))
s.card(1100, 792, 460, 84, None, None, CYAN_D)
s.add(text(1122, 806, "THE UNPLANNED STACK", 20, CODE, TXT))
s.add(text(1122, 838, "channel intro · rev 01 · scale: not to scale", 16, CODE,
           CYAN_D))

# ================================================================ 01 · who
s = w.shot("01 · Who", AX[0], ROW_A, station=0)
s.add(text(80, 160, "Hi — I'm Hussain.", 76, HAND, TXT))
s.dashed([(84, 258), (700, 258)])
s.note(80, 292, "software developer · computer science · permanently nosey", 25)
for i, (label, detail, colour) in enumerate([
        ("builds software", "for a living, and for a while now", CYAN),
        ("studied CS", "the formal version of the same curiosity", MINT),
        ("takes things apart", "to find out why they work that way", AMBER)]):
    y = 420 + i * 130
    s.tick(112, y + 24)
    s.add(text(158, y - 4, label, 34, HAND, colour))
    s.add(text(158, y + 44, detail, 22, HAND, DIM))
s.card(900, 360, 620, 320, None, None, CORAL)
s.add(text(930, 396, "I have never been satisfied", 32, HAND, TXT))
s.add(text(930, 442, "with knowing how to USE", 32, HAND, TXT))
s.add(text(930, 488, "something.", 32, HAND, TXT))
s.add(text(930, 566, "I want to know why it was", 30, HAND, CORAL))
s.add(text(930, 610, "built that way.", 30, HAND, CORAL))
s.note(900, 712, "that's the whole channel, really.", 24, AMBER)

# ========================================================== 02 · why share
s = w.shot("02 · Why share", AX[1], ROW_A, station=1)
s.add(text(80, 110, "Explaining it is how I check", 58, HAND, TXT))
s.add(text(80, 184, "I understood it.", 58, HAND, CYAN))
cyc = [("learn something", CYAN, 300, 400),
       ("explain it out loud", MINT, 720, 340),
       ("hit the bit you\ncan't actually say", CORAL, 1120, 450),
       ("go back and\nlearn it properly", AMBER, 730, 650)]
for label, colour, cx, cy in cyc:
    s.add(box(cx - 150, cy - 60, 300, 120, label, 24, HAND, bg=PANEL,
              stroke=colour, sw=2, label_color=TXT))
s.add(arrow(458, 380, 566, 350, stroke=CYAN_D, sw=2))
s.add(arrow(876, 370, 966, 420, stroke=CYAN_D, sw=2))
s.add(arrow(1040, 530, 892, 620, stroke=CYAN_D, sw=2))
s.add(arrow(576, 650, 330, 470, stroke=CYAN_D, sw=2, dash="dashed"))
s.note(360, 700, "and around again", 22)
s.add(text(80, 786, "You can nod along to an explanation forever.", 30, HAND, TXT))
s.add(text(80, 832, "You cannot fake giving one.", 30, HAND, CORAL))

# ============================================================= 03 · the wall
s = w.shot("03 · The wall", AX[2], ROW_A, station=2)
s.add(text(80, 106, "At uni, some things were just a wall.", 52, HAND, TXT))
s.note(80, 176, "machine learning · deep learning", 24)
for i, (name, wide) in enumerate([("deep learning", 520), ("optimisation", 470),
                                  ("probability", 500), ("linear algebra", 480),
                                  ("calculus", 460)]):
    y = 250 + i * 96          # deep learning on top, calculus at the base
    top = i == 0
    s.add(box(120, y, wide, 84, name, 26, HAND, bg=PANEL,
              stroke=CORAL if top else CYAN_D, sw=2,
              label_color=CORAL if top else TXT))
s.dim(120, 756, 640, 756, "each one needs the one under it")
s.add(ellipse(128, 782, 22, 22, bg=AMBER, stroke=AMBER, sw=2))
s.note(164, 776, "me, down here", 22, AMBER)
s.card(760, 240, 760, 250, None, None, CYAN_D)
s.add(text(790, 276, "∇θ L(θ) = E[ ∇θ log πθ(a|s) ]", 26, CODE, TXT))
s.add(text(790, 332, "s.t.  Σ wᵢ = 1,   wᵢ ≥ 0", 26, CODE, DIM))
s.add(text(790, 410, "(a paper, roughly)", 22, HAND, DIM))
s.add(text(760, 570, "It was never really the notation.", 32, HAND, TXT))
s.add(text(760, 624, "It was the missing WHY:", 32, HAND, CORAL))
s.note(760, 690, "why was this introduced? what was broken before it?", 23)
s.note(760, 730, "that context existed — just never next to", 23)
s.note(760, 768, "the thing I was actually reading.", 23)

# ========================================================= 04 · what changed
s = w.shot("04 · What changed", AX[3], ROW_A, station=3)
s.add(text(80, 116, "Then you could just…", 56, HAND, TXT))
s.add(text(80, 188, "ask.", 56, HAND, AMBER))
s.add(box(80, 296, 560, 92, "\"explain backprop to me\"", 26, CODE, bg=PANEL,
          stroke=CYAN, sw=2, label_color=TXT))
s.add(arrow(360, 400, 360, 442, stroke=CYAN_D, sw=2))
for i, t in enumerate(["at the level I'm actually at",
                       "with only the background I need",
                       "and I can keep asking \"but why?\""]):
    s.add(box(80, 452 + i * 108, 560, 88, t, 23, HAND, bg=PANEL, stroke=MINT,
              sw=2, label_color=TXT))
s.card(760, 296, 370, 300, "before", [
    "read six papers",
    "to find the one",
    "paragraph that",
    "explains why.",
    "",
    "usually give up.",
], CYAN_D, 28, 22)
s.card(1150, 296, 370, 300, "now", [
    "the background",
    "gets assembled,",
    "in the order I",
    "need it, and",
    "nothing more.",
], MINT, 28, 22)
s.add(text(760, 660, "The thing that changed isn't", 30, HAND, TXT))
s.add(text(760, 704, "the answers. It's being able to", 30, HAND, AMBER))
s.add(text(760, 748, "ask again, and admit I didn't follow.", 30, HAND, AMBER))

# ============================================================= 05 · formats
s = w.shot("05 · Formats", AX[4], ROW_A, station=4)
s.add(text(80, 106, "The same idea, five different ways.", 52, HAND, TXT))
s.note(80, 176, "until one of them lands — which no textbook ever offered me", 24)
for i, (label, colour) in enumerate([("a diagram", CYAN), ("an analogy", MINT),
                                     ("the code", AMBER), ("step by step", CORAL),
                                     ("a worked example", CYAN_D)]):
    x = 90 + i * 296
    s.add(box(x, 270, 264, 200, bg=PANEL, stroke=colour, sw=2))
    s.add(text(x + 20, 288, f"VIEW {i + 1}", 17, CODE, colour))
    s.add(text(x + 20, 386, label, 24, HAND, TXT))
    s.tick(x + 132, 244, 8)
s.dim(90, 528, 1466, 528, "one object, five projections")
s.add(text(80, 620, "for me it's almost always the diagram —", 32, HAND, TXT))
s.add(text(80, 672, "which is exactly why this is a canvas", 32, HAND, CYAN))
s.add(text(80, 724, "and not a slide deck.", 32, HAND, CYAN))

# ======================================================== 06 · boring parts
s = w.shot("06 · The boring parts", AX[4], ROW_B, station=5)
s.add(text(80, 116, "It also does the boring parts.", 54, HAND, TXT))
s.note(80, 190, "which, if you have ever made anything, is most of the work", 24)
s.card(80, 280, 620, 400, "the tedious 80%", [
    "gathering the context",
    "drawing the diagrams",
    "cutting the video",
    "writing the descriptions",
    "rendering, exporting, uploading",
    "…then doing it all again",
], CYAN_D, 30, 24)
s.add(arrow(730, 480, 830, 480, stroke=AMBER, sw=3))
s.card(860, 280, 660, 400, "what's left", [
    "the part I actually like:",
    "",
    "understanding the thing,",
    "and finding a way to say it",
    "that makes it obvious.",
], MINT, 30, 26)
s.add(text(80, 760, "I'm not going to pretend that isn't a big reason", 26,
           HAND, AMBER))
s.add(text(80, 802, "this channel exists now.", 26, HAND, AMBER))

# ============================================================== 07 · the deal
s = w.shot("07 · The deal", AX[3], ROW_B, station=6)
s.add(text(80, 140, "So here's the deal.", 60, HAND, TXT))
s.add(box(120, 300, 580, 180, "I learn something\nproperly.", 38, HAND,
          bg=PANEL, stroke=CYAN, sw=3, label_color=TXT))
s.add(arrow(730, 390, 850, 390, stroke=AMBER, sw=3))
s.add(box(880, 300, 580, 180, "Then I show you\nhow it works.", 38, HAND,
          bg=PANEL, stroke=MINT, sw=3, label_color=TXT))
s.dim(120, 570, 1460, 570, "starting with computer science")
s.add(text(120, 650, "Not a tutorial channel. Not \"top 10 tools\".", 28,
           HAND, DIM))
s.add(text(120, 736, "The explanation I wanted back when", 32, HAND, AMBER))
s.add(text(120, 782, "I was the one stuck.", 32, HAND, AMBER))

# ========================================================== 08 · already up
s = w.shot("08 · Already up", AX[2], ROW_B, station=7)
s.add(text(80, 106, "There's already a pile of these up.", 50, HAND, TXT))
s.note(80, 172, "Systems from First Principles — real systems, rebuilt from the "
                "simplest thing that works", 22)
qs = ["how can a webpage\nhijack an AI agent?",
      "how can a lost tracker\nfind your suitcase?",
      "how do many people edit\none design at once?",
      "why do LLMs split reading\nfrom writing?"]
for i, q in enumerate(qs):
    x = 90 + (i % 2) * 740
    y = 240 + (i // 2) * 168
    s.add(box(x, y, 700, 148, q, 26, HAND, bg=PANEL, stroke=CYAN, sw=2,
              label_color=TXT))
s.add(text(90, 596, "every one asks the same three questions:", 26, HAND, DIM))
for i, m in enumerate(["what problem are we solving?",
                       "why does the simplest version fail?",
                       "what does each extra piece buy us?"]):
    s.add(box(90 + i * 478, 648, 448, 130, m, 23, HAND, bg=PANEL,
              stroke=[CYAN, CORAL, MINT][i], sw=2, label_color=TXT))

# ============================================================== 09 · the name
s = w.shot("09 · The name", AX[1], ROW_B, station=8)
s.add(text(80, 106, "Why \"The Unplanned Stack\"?", 52, HAND, TXT))
s.add(text(110, 208, "a stack, in software", 22, CODE, CYAN_D))
for i, n in enumerate(["deploy", "infrastructure", "database", "framework"]):
    s.add(box(110, 252 + i * 92, 420, 78, n, 24, HAND, bg=PANEL, stroke=CYAN,
              sw=2, label_color=TXT))
s.dim(110, 664, 530, 664, "chosen. ordered. planned.")
s.add(text(880, 208, "a stack, in practice", 22, CODE, AMBER))
mine = [("whatever I'm curious about", 866), ("a new country", 946),
        ("a creative life", 886), ("a career", 926)]
for i, (n, x) in enumerate(mine):
    s.add(box(x, 252 + i * 92, 440, 78, n, 22, HAND, bg=PANEL, stroke=AMBER,
              sw=2, label_color=TXT))
s.note(866, 646, "none of it came pre-chosen.", 26, CORAL)
s.add(arrow(520, 806, 596, 806, stroke=CYAN, sw=3))
s.add(text(620, 782, "The Unplanned Stack", 40, HAND, CYAN))

# ========================================================= 10 · where it goes
s = w.shot("10 · Where it goes", AX[1], ROW_C, station=9)
s.add(text(80, 116, "The topics will move around.", 54, HAND, TXT))
for i, n in enumerate(["technology", "career", "creativity",
                       "a life in Canada"]):
    s.add(box(90 + i * 366, 240, 336, 150, n, 27, HAND, bg=PANEL,
              stroke=[CYAN, MINT, AMBER, CORAL][i], sw=2, label_color=TXT))
s.add(text(80, 448, "the approach won't:", 32, HAND, TXT))
for i, k in enumerate(["stay curious", "understand it deeply",
                       "show the real process —\nincluding what didn't work"]):
    s.add(box(90 + i * 478, 516, 448, 170, k, 24, HAND, bg=NAVY, stroke=CYAN_D,
              sw=2, label_color=TXT))
s.note(80, 744, "that last one is the one I actually care about.", 26, AMBER)

# ============================================================== 11 · welcome
s = w.shot("11 · Welcome", AX[2], ROW_C, station=10)
s.add(text(80, 180, "If you're figuring it out", 72, HAND, TXT))
s.add(text(80, 270, "as you go too —", 72, HAND, TXT))
s.add(text(80, 420, "welcome to The Unplanned Stack.", 52, HAND, CYAN))
s.add(line([(84, 506), (1120, 510)], stroke=AMBER, sw=6))
s.note(80, 566, "next up: building a language model from scratch,", 28, TXT)
s.note(80, 610, "starting with one small enough to check with a pencil.", 28)
s.add(text(80, 716, "let's get into it.", 34, HAND, AMBER))
s.card(1100, 786, 460, 84, None, None, CYAN_D)
s.add(text(1122, 800, "THE UNPLANNED STACK", 20, CODE, TXT))
s.add(text(1122, 832, "channel intro · rev 01 · sheet 12 of 12", 16, CODE, CYAN_D))


# ================================================== the route between shots
# Drawn OUTSIDE every frame, so it only appears when you pull back. This is what
# makes the zoomed-out canvas read as one territory instead of twelve cards.
def link(x1, y1, x2, y2, bow=90):
    w.add(line([(x1, y1), ((x1 + x2) / 2, (y1 + y2) / 2 + bow), (x2, y2)],
               stroke=CYAN_D, sw=3, dash="dotted"))


for i in range(4):
    link(AX[i] + 1600, ROW_A + 450, AX[i + 1], ROW_A + 450, 110)
link(AX[4] + 800, ROW_A + 900, AX[4] + 800, ROW_B, 0)
for i in range(4, 1, -1):
    link(AX[i], ROW_B + 450, AX[i - 1] + 1600, ROW_B + 450, -110)
link(AX[1] + 800, ROW_B + 900, AX[1] + 800, ROW_C, 0)
link(AX[1] + 1600, ROW_C + 450, AX[2], ROW_C + 450, 110)
link(1500, ROW_A - 60, 2300, -800, -300)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "channel_intro.excalidraw")
n = w.save(out)
frames = len([e for e in w.els if e["type"] == "frame"])
print(f"channel_intro.excalidraw: {n} elements, {frames} shots")
