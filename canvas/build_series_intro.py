#!/usr/bin/env python3
"""Canvas for Video 0: the series introduction."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excalidraw_kit import *  # noqa: F401,F403

cv = Canvas()

# ------------------------------------------------------------------ 01 title
sc = cv.scene("01 · Title")
sc.add(text(120, 250, "Building an LLM", 96, HAND))
sc.add(text(120, 370, "From Scratch", 96, HAND, BLUE))
sc.add(line([(124, 500), (900, 500)], stroke=ORANGE, sw=4))
sc.add(text(120, 540, "No API keys. No black boxes. No 'trust me, it works'.",
            30, HAND, GRAY))
sc.add(text(120, 600, "Episode 0 — what we're building, and how", 26, HAND))
sc.add(box(1060, 250, 420, 300, bg=BG_YELLOW, dash="dashed"))
sc.add(text(1090, 280, "the whole series\nin one line:", 26, HAND, GRAY))
sc.add(text(1090, 370, "text\n  → numbers\n     → probabilities\n        → text",
            30, CODE))

# ------------------------------------------------------------- 02 the one idea
sc = cv.scene("02 · The one idea")
sc.heading("There is only one idea.",
           "Everything else in this series is a better way of computing these bars.")
sc.add(box(70, 250, 420, 100, '"The cat sat on the ___"', 26, CODE, bg=BG_GRAY))
sc.add(arrow(500, 300, 600, 300))
sc.add(box(610, 230, 240, 140, "MODEL", 34, HAND, bg=BG_VIOLET))
sc.add(arrow(860, 300, 950, 300))
sc.bars(970, 210, [("mat", 0.32), ("floor", 0.19), ("chair", 0.08),
                   ("moon", 0.0001)], maxw=300, label_w=100)
sc.add(arrow(1120, 470, 1120, 560, stroke=GREEN))
sc.add(box(980, 570, 300, 90, "pick one → 'mat'", 26, CODE, bg=BG_GREEN))
sc.add(arrow(1130, 660, 500, 300, via=[(1130, 730), (560, 730), (560, 300)],
             stroke=GREEN, dash="dashed"))
sc.add(text(640, 745, "append it, and ask again", 24, HAND, GREEN))
sc.add(box(70, 400, 420, 260, bg=BG_NONE, dash="dashed", stroke=GRAY))
sc.add(text(96, 424, "That loop is a language model.", 26, HAND, RED))
sc.add(text(96, 480,
            "GPT-4 does this.\nOur first model does this.\n\n"
            "The gap between them is\n40 years of engineering —\nnot a different idea.",
            22, HAND))

# ------------------------------------------------------- 03 use vs understand
sc = cv.scene("03 · Using vs understanding")
sc.heading("I can use one. I can't yet explain one.",
           "That gap is the reason this series exists.")
sc.panel(80, 220, 640, 380, "USING an LLM", [
    "response = client.messages.create(...)",
    "",
    "It works.",
    "I have no idea why.",
    "",
    "Every part of it is somebody",
    "else's understanding.",
], bg=BG_GRAY, title_color=GRAY)
sc.panel(880, 220, 640, 380, "BUILDING an LLM", [
    "counts → probabilities → loss",
    "→ gradients → attention → GPT",
    "",
    "Slower. Smaller. Worse output.",
    "",
    "But every line is a thing",
    "I can defend.",
], bg=BG_GREEN, title_color=GREEN)
sc.add(box(80, 660, 480, 140, "I am learning this too.", 32, HAND,
           bg=BG_YELLOW))
sc.add(text(620, 672,
            "So you'll see me get things wrong,\ncheck the papers, and fix them"
            "\non camera. That's the format.", 24, HAND, VIOLET))

# ------------------------------------------------------------------- 04 arc
sc = cv.scene("04 · The arc")
sc.heading("Four moves, in order.",
           "Each one exists because the previous one hit a wall.")
steps = [
    ("COUNT", "count what follows what", BG_BLUE),
    ("LEARN", "replace counting\nwith weights + gradients", BG_GREEN),
    ("ATTEND", "let the model choose\nwhat to look at", BG_VIOLET),
    ("GENERATE", "train it, then\nmake it talk", BG_YELLOW),
]
for i, (name, desc, colour) in enumerate(steps):
    x = 110 + i * 360
    y = 620 - i * 120
    sc.add(box(x, y, 300, 150, bg=colour))
    sc.add(text(x + 24, y + 24, name, 34, HAND))
    sc.add(text(x + 24, y + 74, desc, 20, HAND, GRAY))
    if i < 3:
        sc.add(arrow(x + 300, y + 40, x + 360, y - 40, stroke=GRAY))
sc.add(box(110, 790, 300, 70, "YOU ARE HERE", 24, HAND, bg=BG_NONE,
           stroke=RED, dash="dashed"))
sc.add(text(1010, 700, "a small GPT,\ntrained on a laptop,\nthat we wrote",
            24, HAND, ORANGE))

# ------------------------------------------------------------- 05 the episodes
sc = cv.scene("05 · The episodes")
sc.heading("Fourteen episodes.",
           "Each one is a theory video and a build video. Titles may shift; the order won't.")
parts = [
    ("PART 1 · COUNT", "pure Python", BG_BLUE, 1, [
        "The smallest language model",
        "Trigrams & the sparsity wall",
    ]),
    ("PART 2 · LEARN", "NumPy → PyTorch", BG_GREEN, 3, [
        "From counts to weights",
        "Gradients, by hand",
        "Autograd from scratch",
        "Enter PyTorch",
        "Embeddings & the MLP model",
        "Making training actually work",
    ]),
    ("PART 3 · ATTEND", "PyTorch", BG_VIOLET, 9, [
        "Why fixed context breaks",
        "Self-attention from scratch",
        "Multi-head & the block",
        "Build the GPT",
        "Tokenization for real (BPE)",
        "Train it. Make it talk.",
    ]),
]
for col, (title, stack, colour, start, eps) in enumerate(parts):
    x = 70 + col * 500
    sc.add(box(x, 190, 450, 96, bg=colour))
    sc.add(text(x + 22, 208, title, 28, HAND))
    sc.add(text(x + 22, 248, stack, 20, CODE, GRAY))
    for i, name in enumerate(eps):
        y = 310 + i * 82
        sc.add(box(x, y, 450, 64, bg=BG_NONE, sw=1))
        sc.add(text(x + 18, y + 18, f"{start + i:02d}", 26, CODE, GRAY))
        sc.add(text(x + 78, y + 20, name, 22, HAND))
sc.add(text(70, 830, "Ends with a working model. Not a frontier model — a real one.",
            24, HAND, ORANGE))

# --------------------------------------------------------- 06 theory + code
sc = cv.scene("06 · Theory + code")
sc.heading("Every concept ships twice.",
           "If I can't code it, I didn't understand it.")
sc.panel(90, 220, 620, 420, "① THEORY VIDEO", [
    "This canvas.",
    "One example, worked by hand.",
    "Every symbol defined before use.",
    "Where the idea came from",
    "(paper, textbook, chapter).",
    "",
    "Question answered: WHY.",
], bg=BG_BLUE)
sc.panel(890, 220, 620, 420, "② BUILD VIDEO", [
    "An empty file.",
    "The same example, in code.",
    "Tests that would catch me lying.",
    "Real output — including the",
    "runs that came out wrong.",
    "",
    "Question answered: HOW.",
], bg=BG_GREEN)
sc.add(arrow(720, 430, 880, 430, sw=3))
sc.add(box(430, 700, 740, 120, bg=BG_YELLOW))
sc.add(text(460, 726,
            "The hand-worked number and the printed number\nmust match. "
            "On camera. Every time.", 26, HAND))

# ------------------------------------------------------------------- 07 math
sc = cv.scene("07 · The maths")
sc.heading("The maths arrives when it's needed. Not before.",
           "There is no prerequisite course. There is no chapter you have to survive first.")
maths = [
    ("Ep 1", "fractions, probability", BG_BLUE),
    ("Ep 1", "logarithms", BG_BLUE),
    ("Ep 3", "vectors, matrix multiply", BG_GREEN),
    ("Ep 3", "softmax, cross-entropy", BG_GREEN),
    ("Ep 4", "derivatives, chain rule", BG_GREEN),
    ("Ep 5", "gradient descent", BG_GREEN),
    ("Ep 10", "dot product = similarity", BG_VIOLET),
]
sc.add(line([(120, 300), (1480, 300)], stroke=GRAY, sw=3))
for i, (ep, topic, colour) in enumerate(maths):
    x = 120 + i * 196
    sc.add(box(x, 282, 36, 36, bg=colour, roundness={"type": 2}))
    sc.add(text(x - 4, 240, ep, 22, CODE, GRAY))
    sc.add(text(x - 30, 340, topic.replace(", ", ",\n"), 20, HAND))
sc.add(box(120, 500, 1360, 200, bg=BG_YELLOW, dash="dashed"))
sc.add(text(150, 530,
            "Each of these gets introduced from zero, in the episode that needs it,\n"
            "in the smallest form that does the job. If a symbol appears on screen,\n"
            "I have already said out loud what it means.", 28, HAND))
sc.add(text(150, 760, "No calculus prerequisite. No linear algebra prerequisite.",
            26, HAND, RED))

# ------------------------------------------------------------- 08 honest terms
sc = cv.scene("08 · Honest terms")
sc.heading("What you need, and what I'm not promising.")
sc.panel(80, 210, 680, 300, "YOU NEED", [
    "Python you'd call 'okay'  (loops, dicts, functions)",
    "Arithmetic. Genuinely, that's the floor.",
    "A laptop. No GPU until episode 12,",
    "     and free Colab covers that.",
    "Patience for one hand-worked example",
    "     per episode.",
], bg=BG_GREEN, size=21)
sc.panel(830, 210, 680, 300, "YOU DON'T NEED", [
    "Machine-learning background",
    "PyTorch",
    "A maths degree",
    "To have watched anything else first",
], bg=BG_BLUE, size=21)
sc.panel(80, 560, 1430, 280, "NOT PROMISED", [
    "This will not produce ChatGPT. The final model will be small, and it will say",
    "strange things.  It will not be fast, and it will not be production code.",
    "",
    "What it will be: a language model where I can point at any line and tell you",
    "why it's there. That's the deliverable.",
], bg=BG_RED, size=21, title_color=RED)

# --------------------------------------------------------------- 09 artefacts
sc = cv.scene("09 · What you get")
sc.heading("Every episode leaves something behind.",
           "Free, in the description, no signup.")
items = [
    ("THEORY.md", "the written chapter, with\nsources and a glossary", BG_BLUE),
    ("code + tests", "runnable, commented,\nsmall on purpose", BG_GREEN),
    ("this canvas", "the actual Excalidraw file\nfrom the video", BG_VIOLET),
    ("checkpoints", "questions to answer if you\nthink you followed it", BG_YELLOW),
]
for i, (name, desc, colour) in enumerate(items):
    x = 80 + i * 370
    sc.add(box(x, 240, 330, 250, bg=colour))
    sc.add(text(x + 26, 268, name, 30, CODE))
    sc.add(text(x + 26, 330, desc, 21, HAND, GRAY))
sc.add(box(80, 570, 1440, 230, bg=BG_NONE, dash="dashed"))
sc.add(text(110, 600, "How to follow along", 30, HAND))
sc.add(text(110, 655,
            "1.  Watch the theory video. Don't touch a keyboard.\n"
            "2.  Watch the build video with the editor open.\n"
            "3.  Answer the checkpoint questions from memory. If one of them stalls you,\n"
            "     that's the bit to rewatch — not the whole episode.", 22, HAND))

# ------------------------------------------------------------------- 10 next
sc = cv.scene("10 · Next")
sc.heading("Episode 1: the smallest language model.")
sc.add(box(90, 230, 560, 420, bg=BG_GRAY))
sc.add(text(120, 260, "$ python bigram.py", 26, CODE, GRAY))
sc.add(text(120, 330, "alyra\nmarin\nzalen\nannnava\nkiah", 40, CODE, GREEN))
sc.add(text(120, 580, "(none of these are real names)", 20, HAND, GRAY))
sc.add(text(740, 250, "It has:", 30, HAND))
sc.add(text(740, 310,
            "no neural network\nno attention\nno training loop\n"
            "no gradients\nand a memory of exactly\none character",
            28, HAND, RED))
sc.add(box(740, 610, 740, 190, bg=BG_YELLOW))
sc.add(text(770, 640,
            "It still learns real structure from text,\n"
            "and it fails in ways that explain\n"
            "why everything after it exists.", 28, HAND))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "series_intro.excalidraw")
print(f"series_intro.excalidraw: {cv.save(out)} elements, {cv._n} scenes")
