#!/usr/bin/env python3
"""Canvas for the channel intro video — The Unplanned Stack.

Channel-level rather than series-level: what the channel is, why it exists, and
what is already on it. Lives here because this is where the canvas toolchain is;
move it if a dedicated channel repo ever appears.

Backgrounds use the channel peach (#f9d6a7, sampled from the banner) on the two
bookend scenes and a paler warm tone in between, so the palette stays readable
while the brand still reads.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excalidraw_kit import *  # noqa: F401,F403

PEACH = "#f9d6a7"
WARM = "#fdf7ee"
WHITE = "#ffffff"

cv = Canvas()


def bg(sc, colour=WARM):
    sc.add(box(0, 0, 1600, 900, bg=colour, stroke="transparent", sw=1,
               roundness=None))
    return sc


# ================================================================== 01 title
sc = bg(cv.scene("01 · Title"), PEACH)
sc.add(text(70, 140, "The Unplanned", 106, HAND))
sc.add(text(70, 272, "Stack", 106, HAND, BLUE))
sc.add(line([(74, 408), (640, 412)], stroke=ORANGE, sw=9))
sc.add(text(70, 456, "no fixed blueprint. just curiosity.", 38, HAND, GRAY))
sc.add(text(70, 828, "channel intro", 26, CODE, RED))
# A stack that does not line up — the whole name, in one picture.
stack = [(1046, BG_BLUE), (1092, BG_GREEN), (1022, BG_VIOLET), (1074, WHITE)]
for i, (x, colour) in enumerate(stack):
    sc.add(box(x, 250 + i * 118, 300, 96, bg=colour, sw=3))

# ============================================================== 02 who I am
sc = bg(cv.scene("02 · Who"))
sc.heading("Hi — I'm Hussain.",
           "Software developer. Studied computer science. Permanently nosey about how things work.")
sc.panel(70, 250, 460, 210, "what I do", [
    "Build software for a living.",
    "Have done for a while now.",
], bg=BG_BLUE)
sc.panel(570, 250, 460, 210, "where it started", [
    "Computer science degree —",
    "the formal version of the same",
    "curiosity.",
], bg=BG_GREEN)
sc.panel(1070, 250, 460, 210, "what I actually like", [
    "Science and technology,",
    "and taking things apart to",
    "see why they work.",
], bg=BG_VIOLET)
sc.add(box(70, 540, 1460, 150, bg=BG_YELLOW))
sc.add(text(100, 570, "I have never been satisfied with knowing how to USE something.",
            34, HAND))
sc.add(text(100, 626, "I want to know why it was built that way.", 34, HAND))
sc.note(70, 760,
        "That's the whole personality of this channel, really.")

# ======================================================== 03 why I share it
sc = bg(cv.scene("03 · Why share"))
sc.heading("Explaining it is how I check I understood it.",
           "The fastest way to find the hole in your own understanding is to try to say it out loud.")
loop = [("learn something", BG_BLUE),
        ("try to explain it\nto someone", BG_GREEN),
        ("hit the bit you\ncan't actually say", BG_RED),
        ("go back and\nlearn it properly", BG_VIOLET)]
for i, (label, colour) in enumerate(loop):
    x = 82 + i * 372
    sc.add(box(x, 270, 320, 170, label, 28, HAND, bg=colour))
    if i < 3:
        sc.add(arrow(x + 330, 355, x + 362, 355, sw=3))
sc.add(arrow(1360, 460, 250, 460, via=[(1360, 570), (250, 570)], stroke=GRAY,
             dash="dashed"))
sc.add(text(620, 590, "and around again", 26, HAND, GRAY))
sc.add(box(82, 660, 1450, 150, bg=BG_YELLOW))
sc.add(text(112, 692, "You can nod along to an explanation forever.", 34, HAND))
sc.add(text(112, 748, "You cannot fake giving one.", 34, HAND, RED))

# ================================================================ 04 the wall
sc = bg(cv.scene("04 · The wall"))
sc.heading("At uni, some things were just a wall.",
           "Machine learning. Deep learning. I could follow every step and still not know why any of it was there.")
sc.add(box(82, 250, 460, 92, "deep learning", 34, HAND, bg=BG_RED))
for i, name in enumerate(["optimisation", "probability", "linear algebra",
                          "calculus", "...and so on"]):
    sc.add(box(82, 356 + i * 84, 460, 70, name, 26, HAND, bg=BG_GRAY))
sc.add(text(82, 800, "each one needed the one underneath it", 26, HAND, GRAY))

sc.add(box(620, 250, 520, 300, bg=WHITE, sw=3))
sc.add(text(650, 282, "∇θ L(θ) = E[ ∇θ log πθ(a|s) ]", 26, CODE))
sc.add(text(650, 342, "s.t.  Σ wᵢ = 1,  wᵢ ≥ 0", 26, CODE, GRAY))
sc.add(text(650, 410, "...", 30, CODE, GRAY))
sc.add(text(650, 470, "(a paper, roughly)", 24, HAND, GRAY))
sc.note(1190, 380, "I was never good\nat reading these.")
sc.add(arrow(1186, 400, 1120, 380, stroke=VIOLET, sw=3))
sc.panel(620, 590, 920, 220, "The bit that actually stopped me", [
    "Not the notation. The missing WHY.",
    "Why was this introduced? What was broken before it?",
    "That context existed somewhere — just never next to the thing",
    "I was reading.",
], bg=BG_RED, size=24, title_color=RED)

# ============================================================== 05 what changed
sc = bg(cv.scene("05 · What changed"))
sc.heading("Then you could just… ask.",
           "Not 'ask a search engine'. Ask, follow up, and admit you didn't get it.")
sc.add(box(82, 250, 540, 104, "\"explain backprop to me\"", 30, CODE, bg=WHITE))
sc.add(arrow(352, 366, 352, 414, sw=3))
for i, line_ in enumerate(["at the level I'm actually at",
                           "with only the background I need",
                           "and I can keep asking \"but why?\""]):
    sc.add(box(82, 424 + i * 122, 540, 104, line_, 27, HAND, bg=BG_GREEN))
sc.panel(700, 250, 400, 320, "before", [
    "Read six papers to",
    "find the one paragraph",
    "that explains the",
    "motivation.",
    "",
    "Usually give up.",
], bg=BG_GRAY, size=24, title_color=GRAY)
sc.panel(1140, 250, 400, 320, "now", [
    "The background gets",
    "assembled for me, in",
    "the order I need it,",
    "and nothing more.",
], bg=BG_BLUE, size=24)
sc.add(box(700, 610, 840, 200, bg=BG_YELLOW))
sc.add(text(730, 642, "This is the part that genuinely changed", 32, HAND))
sc.add(text(730, 694, "what I'm able to learn.", 32, HAND))
sc.add(text(730, 752, "Not the answers — the ability to ask again.", 26, HAND, GRAY))

# ============================================================= 06 many formats
sc = bg(cv.scene("06 · Formats"))
sc.heading("And it will explain the same thing five different ways.",
           "Until one of them clicks. Which is a luxury a textbook has never once offered me.")
formats = [("a diagram", BG_BLUE), ("an analogy", BG_GREEN),
           ("the actual code", BG_VIOLET), ("slowly,\nstep by step", BG_YELLOW),
           ("a worked\nexample", WHITE)]
for i, (label, colour) in enumerate(formats):
    x = 70 + i * 300
    sc.add(box(x, 280, 280, 210, label, 30, HAND, bg=colour, sw=3))
sc.add(text(70, 560, "for me it is almost always the diagram —", 34, HAND))
sc.add(text(70, 612, "which is exactly why this video is a canvas and not slides.",
            34, HAND, BLUE))
sc.note(70, 730,
        "Everything I make gets drawn before it gets said.")

# ============================================================ 07 boring parts
sc = bg(cv.scene("07 · The boring parts"))
sc.heading("It also does the boring parts.",
           "Which, if you have ever made anything, you know is most of the work.")
sc.panel(82, 250, 600, 420, "the tedious 80%", [
    "gathering the context",
    "drawing the diagrams",
    "cutting the video",
    "writing the descriptions",
    "rendering, exporting, uploading",
    "…and doing it all again",
], bg=BG_GRAY, size=26, title_color=GRAY)
sc.add(arrow(710, 460, 810, 460, sw=4))
sc.panel(840, 250, 690, 420, "what's left", [
    "The part I actually like:",
    "",
    "understanding the thing,",
    "and finding a way to say it",
    "that makes it obvious.",
], bg=BG_GREEN, size=28)
sc.add(box(82, 710, 1450, 110, bg=BG_YELLOW))
sc.add(text(112, 740, "I'm not going to pretend that isn't a big reason "
                      "this channel exists now.", 30, HAND))

# ============================================================== 08 the deal
sc = bg(cv.scene("08 · The deal"))
sc.heading("So here's the deal.")
sc.add(box(120, 240, 620, 200, "I learn something\nproperly.", 46, HAND,
           bg=BG_BLUE))
sc.add(arrow(770, 340, 860, 340, sw=4))
sc.add(box(880, 240, 620, 200, "Then I show you\nhow it works.", 46, HAND,
           bg=BG_GREEN))
sc.add(box(120, 500, 1380, 130, "starting with computer science", 44, HAND,
           bg=BG_YELLOW))
sc.add(text(120, 690, "Not a tutorial channel. Not \"top 10 tools\".", 32, HAND, GRAY))
sc.add(text(120, 746, "The kind of explanation I wanted when I was stuck.",
            32, HAND, BLUE))

# ========================================================== 09 already posted
sc = bg(cv.scene("09 · Already up"))
sc.heading("There's already a pile of these up.",
           "Systems from First Principles — real systems, rebuilt starting from the simplest thing that works.")
qs = ["how can a webpage\nhijack an AI agent?",
      "how can a lost tracker\nfind your suitcase?",
      "how do many people edit\none design at once?",
      "why do LLMs split reading\nfrom writing?"]
for i, q in enumerate(qs):
    x = 82 + (i % 2) * 730
    y = 230 + (i // 2) * 180
    sc.add(box(x, y, 690, 160, q, 30, HAND, bg=WHITE, sw=3))
sc.add(text(82, 606, "every one of them asks the same three questions:",
            30, HAND, GRAY))
method = ["what problem are we solving?",
          "why does the simplest version fail?",
          "what does each extra piece buy us?"]
for i, m in enumerate(method):
    sc.add(box(82 + i * 490, 660, 460, 130, m, 26, HAND,
               bg=[BG_BLUE, BG_RED, BG_GREEN][i]))

# =============================================================== 10 the name
sc = bg(cv.scene("10 · The name"))
sc.heading("Why \"The Unplanned Stack\"?")
sc.add(text(82, 210, "a stack, in software:", 30, HAND, GRAY))
for i, name in enumerate(["framework", "database", "infrastructure", "deploy"]):
    sc.add(box(82, 260 + i * 104, 420, 90, name, 28, HAND, bg=BG_BLUE, sw=2))
sc.add(text(82, 700, "chosen on purpose. in order.", 28, HAND, BLUE))

sc.add(text(900, 210, "a stack, in practice:", 30, HAND, GRAY))
mine = [("a career", 900), ("a creative life", 946), ("a new country", 876),
        ("whatever I'm curious about", 928)]
for i, (name, x) in enumerate(mine):
    sc.add(box(x, 260 + i * 104, 460, 90, name, 26, HAND, bg=BG_YELLOW, sw=2))
sc.add(text(876, 700, "none of it came pre-chosen.", 28, HAND, RED))
sc.add(box(560, 760, 480, 100, "The Unplanned Stack", 38, HAND, bg=BG_VIOLET))

# ============================================================== 11 where it goes
sc = bg(cv.scene("11 · Where it goes"))
sc.heading("The topics will move around.",
           "Technology mostly, but not only.")
areas = [("technology", BG_BLUE), ("career", BG_GREEN),
         ("creativity", BG_VIOLET), ("building a life\nin Canada", BG_YELLOW)]
for i, (name, colour) in enumerate(areas):
    sc.add(box(82 + i * 370, 230, 340, 170, name, 30, HAND, bg=colour, sw=3))
sc.add(text(82, 450, "the approach won't:", 36, HAND))
keeps = ["stay curious", "understand it deeply",
         "show the real process —\nincluding what didn't work"]
for i, k in enumerate(keeps):
    sc.add(box(82 + i * 490, 520, 460, 170, k, 28, HAND, bg=WHITE, sw=3))
sc.add(text(82, 750, "that last one is the one I care about most.", 32, HAND, RED))

# ================================================================ 12 welcome
sc = bg(cv.scene("12 · Welcome"), PEACH)
sc.add(text(70, 200, "If you're figuring it out", 88, HAND))
sc.add(text(70, 312, "as you go too —", 88, HAND))
sc.add(text(70, 470, "welcome to The Unplanned Stack.", 62, HAND, BLUE))
sc.add(line([(74, 566), (1180, 570)], stroke=ORANGE, sw=8))
sc.add(text(70, 640, "next up: building a language model from scratch,", 34, HAND))
sc.add(text(70, 692, "starting with one so small you can check it with a pencil.",
            34, HAND, GRAY))
sc.add(text(70, 812, "let's get into it.", 34, HAND, RED))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "channel_intro.excalidraw")
print(f"channel_intro.excalidraw: {cv.save(out)} elements, {cv._n} scenes")
