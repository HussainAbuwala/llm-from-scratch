#!/usr/bin/env python3
"""Canvas for Episode 1: the count-based character bigram model.

Scene order follows the beat sheet in EPISODE_01_VIDEO_PLAN.md.
Worked example throughout: the two-word dataset {anna, ava}.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from excalidraw_kit import *  # noqa: F401,F403

cv = Canvas()

# ================================================================== 01 title
sc = cv.scene("01 · Cold open")
sc.add(text(110, 200, "The Smallest", 92, HAND))
sc.add(text(110, 310, "Language Model", 92, HAND, BLUE))
sc.add(line([(114, 440), (860, 440)], stroke=ORANGE, sw=4))
sc.add(text(110, 480, "Episode 1  ·  Building an LLM From Scratch", 26, HAND, GRAY))
sc.add(box(110, 560, 700, 260, bg=BG_GRAY))
sc.add(text(140, 585, "$ python bigram.py", 22, CODE, GRAY))
sc.add(text(140, 640, "alyra    marin    zalen    annnava", 34, CODE, GREEN))
sc.add(text(140, 700, "It has no neural network,", 24, HAND))
sc.add(text(140, 740, "and it remembers exactly one character.", 24, HAND, RED))
sc.add(box(900, 560, 590, 260, bg=BG_YELLOW, dash="dashed"))
sc.add(text(930, 590,
            "That sounds almost useless.\n\n"
            "It is also the smallest thing\nthat is honestly a language model —\n"
            "which makes it the only place\nto start.", 26, HAND))

# ======================================================== 02 what a LM outputs
sc = cv.scene("02 · What a language model outputs")
sc.heading("A language model does not output text.",
           "It outputs a probability for every token that could come next.")
sc.add(box(80, 250, 260, 110, "context:  \"a\"", 26, CODE, bg=BG_GRAY))
sc.add(arrow(350, 305, 450, 305))
sc.add(box(460, 235, 220, 140, "MODEL", 32, HAND, bg=BG_VIOLET))
sc.add(arrow(690, 305, 780, 305))
sc.bars(800, 230, [("n", 0.25), ("v", 0.25), ("<END>", 0.50)],
        maxw=300, label_w=110)
sc.add(box(800, 420, 460, 70, "these must add to 1.00", 24, HAND,
           bg=BG_GREEN))
sc.add(text(80, 430, "Then, and only then, do we pick one:", 24, HAND))
sc.add(box(80, 490, 600, 280, bg=BG_NONE, dash="dashed"))
sc.add(text(110, 515,
            "current token\n     ↓\nprobability row\n     ↓\nchoose one\n     ↓\n"
            "that becomes the current token", 24, CODE))
sc.note(760, 560,
        "Choosing is a separate decision\nfrom predicting.\n\n"
        "We'll make it two different ways\nlater in this episode, from the\n"
        "same numbers.")

# ========================================================= 04 what vocabulary is
sc = cv.scene("03 · What \"vocabulary\" means")
sc.heading("Vocabulary: the set of token types.",
           "Not the names — those are the data. The vocabulary is what the model is allowed to emit.")

# The same word, tokenised three ways. Only the tokens change; the definition
# does not. This is the scene that stops "vocabulary" meaning "the words I know".
sc.add(box(80, 196, 440, 448, bg=BG_NONE, stroke=BLUE, sw=2))
sc.add(text(106, 216, "CHARACTERS", 26, CODE, BLUE))
sc.cards(106, 264, ["n", "o", "a", "h"], w=88, h=80, gap=10, size=30)
sc.add(text(106, 374, "vocabulary =\nevery letter that appears,\nplus <START> and <END>",
            21, HAND))
sc.add(text(106, 486, "short vocabulary,\nlong sequences", 21, HAND, GRAY))
sc.add(box(106, 566, 300, 56, "this episode", 22, HAND, bg=BG_BLUE))

sc.add(box(580, 196, 440, 448, bg=BG_NONE, stroke=GREEN, sw=2))
sc.add(text(606, 216, "WORDS", 26, CODE, GREEN))
sc.cards(606, 264, ["noah"], w=200, h=80, size=30, bg=BG_GREEN)
sc.add(text(606, 374, "vocabulary =\nevery distinct word\nyou have ever seen", 21, HAND))
sc.add(text(606, 486, "one step per word — but\n\"noahs\" shares nothing with it", 21, HAND, GRAY))
sc.add(box(606, 566, 300, 56, "a word-level model", 22, HAND, bg=BG_GREEN))

sc.add(box(1080, 196, 440, 448, bg=BG_NONE, stroke=VIOLET, sw=2))
sc.add(text(1106, 216, "SUBWORD PIECES", 26, CODE, VIOLET))
sc.cards(1106, 264, ["no", "ah"], w=140, h=80, size=30, bg=BG_VIOLET)
sc.add(text(1106, 374, "vocabulary =\n~50,000 learned pieces", 21, HAND))
sc.add(text(1106, 486, "the compromise that\nevery real LLM uses", 21, HAND, GRAY))
sc.add(box(1106, 566, 340, 56, "episode 13", 22, HAND, bg=BG_VIOLET))

sc.add(box(80, 682, 1440, 150, bg=BG_YELLOW))
sc.add(text(110, 706, "The definition never changes: the vocabulary is the set of "
                      "distinct token types.", 28, HAND))
sc.add(text(110, 754, "Only the tokens change.", 28, HAND))
sc.add(text(110, 800, "Ours: the letters in the name list, plus two boundary tokens. "
                      "26 letters + <END> = 27 things that can come next.",
            21, HAND, RED))

# ============================================================== 04 vocab / ids
sc = cv.scene("04 · Vocabulary and integer IDs")
sc.heading("The model never sees a letter.",
           "Characters become integers, because integers are row and column numbers.")
sc.add(text(120, 210, "vocabulary", 28, HAND, GRAY))
sc.add(text(120, 250, "every distinct CHARACTER — not the names", 19, HAND, RED))
pairs = [("<START>", 0), ("<END>", 1), ("a", 2), ("n", 3), ("v", 4)]
for i, (ch, i_) in enumerate(pairs):
    y = 292 + i * 90
    sc.add(box(120, y, 220, 74, ch, 26, CODE, bg=BG_BLUE))
    sc.add(arrow(350, y + 37, 430, y + 37, stroke=GRAY))
    sc.add(box(440, y, 100, 74, str(i_), 28, CODE, bg=BG_YELLOW))
sc.add(text(620, 274, "Two mappings, both needed:", 26, HAND))
sc.add(text(620, 328, "stoi   \"string to int\"    character → id", 24, CODE))
sc.add(text(620, 362, "itos   \"int to string\"    id → character", 24, CODE))
sc.add(text(620, 404, "one for the way in, one for the way out.", 22, HAND, GRAY))
sc.panel(620, 460, 880, 180, "Where does the vocabulary come from?", [
    "From the TRAINING split only — never the whole file.",
    "If held-out data contains a character we never trained on, we have no row",
    "for it. We report that rather than hide it. (Real fix: <UNK>, or bytes.)",
], bg=BG_RED, size=20, title_color=RED)
sc.note(620, 690,
        "<START> and <END> are not characters in any name.\n"
        "They are tokens we invent, and the model has to learn them\n"
        "like everything else. Next scene explains why they exist.")
sc.add(text(120, 742, "so what the model is actually handed:", 20, HAND, GRAY))
sc.add(text(120, 780, "\"anna\"   →   [2, 3, 3, 2]", 30, CODE, RED))

# =============================================================== 05 boundaries
sc = cv.scene("05 · Boundaries")
sc.heading("Two invented tokens do two specific jobs.")
sc.cards(180, 250, ["<START>", "a", "n", "n", "a", "<END>"], w=170, h=100,
         size=26,
         colors=[BG_GREEN, BG_BLUE, BG_BLUE, BG_BLUE, BG_BLUE, BG_RED])
sc.add(arrow(265, 420, 265, 500, stroke=GREEN))
sc.add(box(120, 510, 400, 170, bg=BG_GREEN))
sc.add(text(145, 535, "<START>", 26, CODE))
sc.add(text(145, 580, "lets the model learn\nwhich characters begin\na name",
            22, HAND))
sc.add(arrow(1085, 420, 1085, 500, stroke=RED))
sc.add(box(940, 510, 440, 170, bg=BG_RED))
sc.add(text(965, 535, "<END>", 26, CODE))
sc.add(text(965, 580, "lets the model learn\nwhen a name is finished",
            22, HAND))
sc.add(box(120, 716, 1380, 150, bg=BG_YELLOW))
sc.add(text(150, 738, "<END> is not decoration.", 28, HAND))
sc.add(text(150, 784,
            "Without it the model can only answer \"what comes next?\" — never "
            "\"that's the whole name.\"", 22, HAND))
sc.add(text(150, 820,
            "P(\"anna\") would then mean P(anything starting with \"anna\") — "
            "annabelle included.", 22, HAND, RED))

# ============================================================== 06 the window
sc = cv.scene("06 · The sliding window")
sc.heading("Training data is not text. It is ordered pairs.",
           "Slide a two-token window across the sequence and write down what you see.")
sc.cards(140, 200, ["<START>", "a", "n", "n", "a", "<END>"], w=140, h=88,
         gap=12, size=22, bg=BG_GRAY)
for i in range(5):
    x = 140 + i * 152
    y = 320 + i * 66
    sc.add(box(x, y, 292, 54, bg=BG_NONE, stroke=ORANGE, sw=3, dash="dashed"))
pairs_anna = ["<START> → a", "a → n", "n → n", "n → a", "a → <END>"]
sc.add(box(1090, 300, 420, 350, bg=BG_NONE, stroke=GRAY, dash="dotted"))
sc.add(text(1130, 320, "\n\n".join(pairs_anna), 28, CODE))
sc.add(text(1090, 662, "5 transitions from a 4-letter name", 22, HAND, GRAY))
# The word "bigram" is used from the file name onward but was never defined.
# This is where the pairs first exist, so this is where it belongs.
sc.add(box(1000, 700, 520, 164, bg=BG_YELLOW))
sc.add(text(1024, 718, "bigram = a pair of adjacent tokens", 24, HAND))
sc.add(text(1024, 758, "bi = two. Each window frames one.", 19, HAND, GRAY))
sc.add(text(1024, 790, "unigram 1  ·  bigram 2  ·  trigram 3", 19, CODE, GRAY))
sc.add(text(1024, 822, "So the context is one token, not two.", 19, HAND, RED))

sc.add(box(140, 700, 820, 164, bg=BG_RED))
sc.add(text(170, 726, "Direction is the whole point.", 28, HAND))
sc.add(text(170, 776, "a -> n  and  n -> a  are different observations,\n"
                      "stored in different cells. Never merge them.", 22, HAND))

# ================================================================ 07 tallies
sc = cv.scene("07 · Counting")
sc.heading("Training, for this model, is counting.",
           "No optimiser. No gradients. No repeated passes. One walk through the data.")
sc.add(text(90, 210, "anna", 30, CODE, GRAY))
sc.add(text(90, 260, "<START> → a\na → n\nn → n\nn → a\na → <END>", 26, CODE))
sc.add(text(440, 210, "ava", 30, CODE, GRAY))
sc.add(text(440, 260, "<START> → a\na → v\nv → a\na → <END>", 26, CODE))
sc.add(arrow(760, 340, 860, 340))
sc.add(text(770, 285, "merge", 20, HAND, GRAY))
rows = [("<START> → a", 2), ("a → n", 1), ("a → v", 1), ("a → <END>", 2),
        ("n → n", 1), ("n → a", 1), ("v → a", 1)]
for i, (t, c) in enumerate(rows):
    y = 200 + i * 74
    sc.add(box(890, y, 300, 60, t, 24, CODE, bg=BG_NONE, sw=1))
    sc.add(box(1200, y, 80, 60, str(c), 24, CODE, bg=BG_YELLOW, sw=1))
sc.note(1320, 300,
        "Every occurrence of\nevery character produces\nexactly one outgoing\n"
        "transition — because\nof <END>.")
sc.add(box(90, 620, 620, 230, bg=BG_GREEN))
sc.add(text(120, 648, "Look only at what leaves 'a':", 26, HAND))
sc.add(text(120, 700, "a → n        once\na → v        once\na → <END>    twice",
            26, CODE))
sc.add(text(120, 810, "four observations total -> 1/4, 1/4, 2/4", 22, HAND, GREEN))

# ============================================================== 08 the matrix
sc = cv.scene("08 · The count matrix")
sc.heading("Same counts, arranged as a table.",
           "Row = the token we are standing on. Column = the token that came next.")
sc.add(text(430, 195, "next token", 24, HAND, GRAY))
sc.table(300, 230, ["a", "n", "v", "<END>"], ["<START>", "a", "n", "v"],
         [[2, 0, 0, 0], [0, 1, 1, 2], [1, 1, 0, 0], [1, 0, 0, 0]],
         cw=120, ch=76, hi_row=1, corner="")
sc.add(text(110, 400, "current\ntoken", 24, HAND, GRAY))
sc.add(text(300, 570, "each cell:  how many times did the column token follow the row token?",
            22, HAND, GRAY))
sc.panel(90, 640, 700, 210, "The rows and columns are NOT the same set", [
    "<START>  is a row, never a column   — nothing is followed BY a start",
    "<END>    is a column, never a row   — nothing follows an end",
    "ordinary characters are both",
], bg=BG_RED, size=20, title_color=RED)
sc.panel(830, 640, 680, 210, "So the shape is (V+1) × (V+1)", [
    "and — this matters in a minute — every cell in it is a",
    "transition that is at least POSSIBLE.",
    "When we add pseudo-counts, those are the cells we add to.",
], bg=BG_VIOLET, size=20, title_color=VIOLET)
sc.note(1130, 230, "highlighted row:\nwhat followed 'a'")

# ============================================================ 09 normalisation
sc = cv.scene("09 · Counts → probabilities")
sc.heading("Counts are not probabilities. Divide by the row total.")
sc.add(text(100, 220, "row for 'a'", 26, HAND, GRAY))
sc.table(100, 260, ["a", "n", "v", "<END>"], ["counts"],
         [[0, 1, 1, 2]], cw=130, ch=76, corner="")
sc.add(text(760, 285, "total = 4", 30, CODE, RED))
sc.add(arrow(300, 430, 300, 500, stroke=GREEN, sw=3))
sc.add(text(320, 440, "÷ 4", 26, CODE, GREEN))
sc.table(100, 510, ["a", "n", "v", "<END>"], ["P"],
         [["0.00", "0.25", "0.25", "0.50"]], cw=130, ch=76, corner="")
sc.add(box(760, 510, 300, 76, "adds to 1.00", 24, HAND, bg=BG_GREEN))
sc.add(text(100, 660, "four tickets in a bag:", 24, HAND))
sc.tickets(100, 700, [("n", BG_BLUE), ("v", BG_VIOLET),
                      ("<END>", BG_RED), ("<END>", BG_RED)],
           tw=110, th=90, size=22)
sc.add(text(620, 720, "<END> owns two of the four tickets,\n"
                      "so P(<END> | a) = 0.50", 24, HAND, GRAY))
sc.note(1150, 260,
        "Normalising rescales but\npreserves proportion:\n"
        "<END> happened twice as\noften as n, and stays\ntwice as likely.")
sc.add(box(1150, 640, 360, 200, bg=BG_YELLOW, dash="dashed"))
sc.add(text(1175, 665, "This is the\nmaximum-likelihood\nestimate.", 26, HAND))
sc.add(text(1175, 780, "Remember that phrase —\nwe come back to it.", 20, HAND, GRAY))

# ============================================================ 10 the artefact
sc = cv.scene("10 · What the model IS")
sc.heading("Stop. This is the finished model.",
           "There is nothing else. No network is hiding behind it.")
things = [
    ("① the vocabulary", "stoi / itos\ncharacter ↔ integer", BG_BLUE),
    ("② the convention", "wrap every example in\n<START> ... <END>", BG_GREEN),
    ("③ the table", "one probability row for\nevery current token", BG_VIOLET),
]
for i, (name, desc, colour) in enumerate(things):
    x = 90 + i * 490
    sc.add(box(x, 240, 440, 240, bg=colour))
    sc.add(text(x + 28, 270, name, 30, HAND))
    sc.add(text(x + 28, 330, desc, 22, CODE))
sc.add(box(90, 540, 1420, 130, "P( next token  |  current token )", 46, CODE,
           bg=BG_YELLOW))
sc.add(text(90, 710, "Saving this model means saving a table of numbers. "
                     "Loading it means loading a table of numbers.", 24, HAND, GRAY))
sc.add(text(90, 780, "Every model in this series is a better answer to the same "
                     "question this table already answers.", 24, HAND, ORANGE))

# ================================================================= 11 greedy
sc = cv.scene("11 · Greedy decoding")
sc.heading("Generation, attempt one: always take the biggest number.")
sc.cards(100, 220, ["<START>", "a", "n", "a", "n"], w=150, h=90, size=24,
         bg=BG_GRAY)
for i in range(4):
    x = 250 + i * 164
    sc.add(text(x, 330, "↓ max", 18, CODE, GRAY))
sc.add(text(100, 400, "output:", 24, HAND))
sc.add(text(240, 392, "a n a n a n a n a n ...", 38, CODE, RED))
sc.add(box(100, 470, 640, 230, bg=BG_RED))
sc.add(text(130, 496, "It gets stuck.", 30, HAND))
sc.add(text(130, 546,
            "If  a -> n  is the biggest thing after a,\n"
            "and n -> a  is the biggest thing after n,\n"
            "then there is no way out. Ever.", 22, HAND))
sc.add(text(130, 660, "-> generation needs a maximum length", 22, HAND, RED))
sc.panel(800, 470, 700, 230, "Greedy is not wrong, it is short-sighted", [
    "It picks the best next token, which is not the",
    "same as the best sequence. It will never take a",
    "lower-probability exit like  a -> <END>,  even when",
    "that exit is the only sane move.",
    "",
    "It is deterministic and reproducible, which is",
    "genuinely useful — just not here.",
], bg=BG_BLUE, size=20)
sc.note(980, 232, "(illustration — a constructed\nloop, so the trap is visible)")

# =============================================================== 12 sampling
sc = cv.scene("12 · Sampling")
sc.heading("Generation, attempt two: let the probabilities be odds.")
sc.add(text(100, 210, "if the row says", 24, HAND, GRAY))
sc.bars(100, 250, [("a", 0.60), ("b", 0.30), ("c", 0.10)], maxw=300,
        label_w=60)
sc.add(text(100, 430, "then draw one ticket from a bag of 100:", 24, HAND))
sc.add(box(100, 480, 360, 60, bg=BG_BLUE))
sc.add(text(115, 495, "60 × a", 22, CODE))
sc.add(box(470, 480, 180, 60, bg=BG_VIOLET))
sc.add(text(485, 495, "30 × b", 22, CODE))
sc.add(box(660, 480, 60, 60, bg=BG_YELLOW))
sc.add(text(730, 495, "10 × c", 22, CODE))
sc.add(text(100, 570, "weighted randomness — not equal randomness", 22, HAND, RED))
sc.panel(800, 200, 700, 250, "Same table, four seeds", [
    "seed 1:   alyra",
    "seed 2:   marin",
    "seed 3:   annnava",
    "seed 4:   zalen",
], bg=BG_GREEN, size=26)
sc.add(box(800, 480, 700, 260, bg=BG_YELLOW, dash="dashed"))
sc.add(text(830, 505, "Sampling shows you the model you actually built.",
            26, HAND))
sc.add(text(830, 560,
            "Greedy shows you one path through it. Sampling exposes\n"
            "the whole distribution — including the parts that are wrong.\n\n"
            "Fix the seed and any single run becomes reproducible.\n\n"
            "(temperature, top-k, top-p: later. Same idea, more dials.)",
            21, HAND))

# ========================================================== 13 lucky or good?
sc = cv.scene("13 · Lucky, or good?")
sc.heading("Eyeballing samples is not evaluation.")
sc.add(box(120, 230, 460, 200, bg=BG_GREEN))
sc.add(text(150, 258, "the one I'd tweet", 24, HAND, GRAY))
sc.add(text(150, 310, "marin", 60, CODE))
sc.add(box(680, 230, 720, 380, bg=BG_RED))
sc.add(text(710, 258, "the rest of that run", 24, HAND, GRAY))
sc.add(text(710, 310, "annnnav\nvvva\nn\nzzzzzzzn\naaaaaaaaaaa", 34, CODE))
sc.add(box(120, 480, 460, 130, "cherry-picking", 34, HAND, bg=BG_YELLOW))
sc.add(box(120, 680, 1280, 160, bg=BG_NONE, dash="dashed"))
sc.add(text(150, 706, "We need one number that we cannot flatter ourselves with.",
            30, HAND))
sc.add(text(150, 762,
            "It has to be computed on text the model never trained on, and it has to "
            "consider every\nprediction — not the four I happened to like.", 22, HAND, GRAY))

# ============================================================ 14 answer key
sc = cv.scene("14 · The answer key")
sc.heading("Held-out text tells us what SHOULD have come next.",
           "Generation has no correct answer. Evaluation does — the data supplies it.")
sc.add(text(100, 200, "held-out word:  \"anna\"", 28, CODE))
rows = [("<START>", "a", 0.62), ("a", "n", 0.25), ("n", "n", 0.31),
        ("n", "a", 0.44), ("a", "<END>", 0.50)]
sc.add(text(100, 260, "input", 22, HAND, GRAY))
sc.add(text(320, 260, "true target", 22, HAND, GRAY))
sc.add(text(600, 260, "probability the model gave it", 22, HAND, GRAY))
for i, (a, b, p) in enumerate(rows):
    y = 300 + i * 82
    sc.add(box(100, y, 180, 64, a, 24, CODE, bg=BG_GRAY, sw=1))
    sc.add(box(320, y, 180, 64, b, 24, CODE, bg=BG_GREEN, sw=1))
    sc.add(box(600, y, max(20, 460 * p), 64, bg=BG_YELLOW, sw=1))
    sc.add(text(600 + max(20, 460 * p) + 16, y + 18, f"{p:.2f}", 22, CODE, GRAY))
sc.note(1180, 300, "(illustrative numbers)")
sc.add(box(100, 730, 660, 120, bg=BG_BLUE))
sc.add(text(125, 752, "note row 2:", 24, HAND))
sc.add(text(125, 792, "greedy would have said <END> here. We do not care.\n"
                      "We record what it gave to the token that actually occurred.",
            19, HAND))
sc.add(box(800, 730, 700, 120, bg=BG_VIOLET))
sc.add(text(825, 752, "evaluation never changes the model", 24, HAND))
sc.add(text(825, 792, "no counts move, no probability updates. We are taking a "
                      "measurement.", 19, HAND))

# ================================================================= 15 funnel
sc = cv.scene("15 · Why the probabilities multiply")
sc.heading("The whole word happens only if every transition happens.")
sc.add(text(100, 200, "P(\"ana\") = 0.80 × 0.50 × 0.25 × 0.40 = 0.04", 34, CODE))
stages = [("100 attempts", 420, BG_GRAY, ""),
          ("80", 340, BG_BLUE, "× 0.80   choose a"),
          ("40", 260, BG_BLUE, "× 0.50   choose n"),
          ("10", 180, BG_VIOLET, "× 0.25   choose a"),
          ("4", 100, BG_GREEN, "× 0.40   choose <END>")]
y = 280
for label, w, colour, op in stages:
    sc.add(box(100 + (420 - w) / 2, y, w, 72, label, 26, CODE, bg=colour))
    if op:
        sc.add(text(580, y + 20, op, 24, CODE, GRAY))
    y += 108
sc.add(text(100, 820, "≈ 4 of every 100 attempts follow exactly that path",
            24, HAND, GREEN))
sc.panel(900, 230, 610, 300, "This is the chain rule of probability", [
    "P(A then B)  =  P(A) × P(B | A)",
    "",
    "We are NOT multiplying unrelated numbers.",
    "Every factor is conditional on where the",
    "previous step left us.",
    "",
    "Bigram model = chain rule + Markov assumption:",
    "keep the product, but let each factor see",
    "only one token back.",
], bg=BG_VIOLET, size=20, title_color=VIOLET)
sc.note(900, 570,
        "Each multiplication takes a\nfraction of whatever survived\nthe step before it.\n\n"
        "Which is exactly why long\nsequences end up with\nabsurdly small numbers.")

# =================================================================== 16 logs
sc = cv.scene("16 · Logarithms, and why we need them")
sc.heading("First the problem, then the tool.")
sc.add(box(90, 210, 620, 180, bg=BG_RED))
sc.add(text(115, 236, "0.1 × 0.1 × 0.1 × ... a thousand times", 26, CODE))
sc.add(text(115, 296, "= 1e-1000\n= 0.0, as far as your computer is concerned",
            24, CODE))
sc.add(text(115, 360, "numerical underflow", 20, HAND, RED))
sc.add(text(90, 430, "A logarithm asks: what exponent produces this number?",
            26, HAND))
sc.add(box(90, 480, 620, 150, bg=BG_BLUE))
sc.add(text(115, 505, "10³ = 1000        →        log₁₀(1000) = 3", 28, CODE))
sc.add(text(115, 570, "ln uses base e ≈ 2.718. Base changes the scale,\n"
                      "never which model wins.", 20, HAND))
sc.add(box(90, 670, 620, 170, bg=BG_YELLOW))
sc.add(text(115, 696, "the one rule that matters:", 22, HAND))
sc.add(text(115, 742, "log(a × b × c) = log a + log b + log c", 25, CODE))
sc.add(text(115, 795, "an unstable product becomes a manageable sum", 20, HAND))
sc.add(text(790, 210, "\"ana\", the same number twice", 28, HAND, GRAY))
sc.add(text(790, 270,
            "ln(0.80)  ≈  -0.22\nln(0.50)  ≈  -0.69\n"
            "ln(0.25)  ≈  -1.39\nln(0.40)  ≈  -0.92\n"
            "----------------------\nsum       ≈  -3.22", 30, CODE))
sc.add(text(790, 570, "and directly:", 22, HAND, GRAY))
sc.add(text(790, 620, "ln(0.04) ≈ -3.22", 30, CODE, GREEN))
sc.add(box(780, 700, 620, 140, bg=BG_GREEN))
sc.add(text(805, 726, "Probabilities live in (0, 1],", 24, HAND))
sc.add(text(805, 770, "so their logs are always ≤ 0. Hold that thought.",
            24, HAND))

# ==================================================================== 17 NLL
sc = cv.scene("17 · Negative log-likelihood")
sc.heading("Flip the sign, and you have a loss where lower is better.")
sc.add(box(90, 210, 700, 120, "NLL  =  − log P(correct token)", 36, CODE,
           bg=BG_YELLOW))
sc.add(text(90, 370, "read it as surprise:", 28, HAND))
sc.table(90, 420, ["− log penalty"], ["100%", "50%", "10%", "1%"],
         [["0.00"], ["0.69"], ["2.30"], ["4.61"]], cw=230, ch=76,
         corner="P on target")
sc.add(text(90, 800, "confident and right -> nearly free.   "
                     "confident and wrong -> expensive.", 24, HAND, GREEN))
sc.panel(880, 210, 630, 250, "Why negate at all?", [
    "Because 'higher likelihood is better' and",
    "'lower loss is better' are the same statement,",
    "and every optimiser we meet from episode 3",
    "onwards is built to push a number DOWN.",
], bg=BG_BLUE, size=21)
sc.panel(880, 490, 630, 200, "Why average?", [
    "Total NLL grows with the amount of text.",
    "1000 predictions accrue ~10× the penalty of 100",
    "at identical quality. Divide by the number of",
    "transitions and lengths become comparable.",
], bg=BG_GREEN, size=21)
sc.add(text(880, 720, "avg NLL = total penalty ÷ transitions", 26, CODE))
sc.add(text(880, 780, "\"on a typical prediction, how surprised was it?\"",
            22, HAND, GRAY))

# ============================================================== 18 baselines
sc = cv.scene("18 · Lower than what?")
sc.heading("An average NLL of 2.4 is meaningless on its own.",
           "A loss only means something next to a reference point. So build two bad models.")
sc.add(box(90, 240, 440, 250, bg=BG_GRAY))
sc.add(text(115, 266, "UNIFORM", 30, HAND, GRAY))
sc.add(text(115, 320, "every allowed token\ngets 1 / (V+1)", 22, CODE))
sc.add(text(115, 400, "NLL = ln(V+1)\n    = ln(27) ≈ 3.30", 26, CODE, RED))
sc.add(box(560, 240, 440, 250, bg=BG_BLUE))
sc.add(text(585, 266, "UNIGRAM", 30, HAND))
sc.add(text(585, 320, "overall frequency only,\ncontext ignored", 22, CODE))
sc.add(text(585, 400, "knows 'a' is common\nand 'q' is not", 22, HAND))
sc.add(box(1030, 240, 470, 250, bg=BG_GREEN))
sc.add(text(1055, 266, "BIGRAM", 30, HAND))
sc.add(text(1055, 320, "ours: one character\nof context", 22, CODE))
sc.add(text(1055, 400, "must beat unigram,\nor context bought\nus nothing", 22, HAND))
sc.add(arrow(530, 365, 560, 365, stroke=GRAY))
sc.add(arrow(1000, 365, 1030, 365, stroke=GRAY))
sc.add(box(90, 550, 1410, 130, bg=BG_YELLOW))
sc.add(text(120, 578, "The uniform baseline is also a test.", 28, HAND))
sc.add(text(120, 622, "Build the model with an enormous smoothing value and it must "
                      "land on ln(V+1). If it doesn't, the code is wrong.", 21, HAND))
sc.add(text(90, 730, "Two names for this same number, which you'll meet everywhere:",
            24, HAND, GRAY))
sc.add(text(90, 780, "cross-entropy = average NLL in nats        "
                     "perplexity = exp(average NLL)", 26, CODE))

# ========================================================== 19 counting = MLE
sc = cv.scene("19 · What counting already did")
sc.heading("Now look at what counting already did.")
sc.add(box(120, 250, 620, 240, bg=BG_GREEN))
sc.add(text(150, 280, "counts ÷ row total", 32, CODE))
sc.add(text(150, 340, "is not just *a* reasonable\nway to get probabilities.\n\n"
                      "It is the EXACT minimiser of\naverage NLL on the training set.",
            24, HAND))
sc.add(text(120, 520, "No bigram table scores better on this training data.\n"
                      "We found it in one pass, with no optimiser.", 24, HAND, GREEN))
sc.add(arrow(760, 370, 860, 370, sw=3))
sc.add(box(880, 250, 620, 240, bg=BG_VIOLET))
sc.add(text(910, 280, "episode 3 onwards", 32, HAND))
sc.add(text(910, 340, "a neural network starts from\nrandom numbers and crawls\n"
                      "toward that same loss,\none gradient step at a time.",
            24, HAND))
sc.add(box(120, 640, 1380, 190, bg=BG_YELLOW, dash="dashed"))
sc.add(text(150, 668, "So here is the test that ties this series together:", 28, HAND))
sc.add(text(150, 718,
            "when we train the neural bigram model in episode 3, it should converge to "
            "roughly the number\nwe just got for free. If it doesn't, the training code "
            "is broken — and we'll know, because\ntoday gave us the answer key.", 21, HAND))

# ============================================================== 20 zero probs
sc = cv.scene("20 · The zero")
sc.heading("x is in the vocabulary. It just never followed a.")
sc.table(90, 220, ["n", "v", "<END>", "x"], ["count", "P"],
         [[1, 1, 2, 0], ["0.25", "0.25", "0.50", "0.00"]], cw=150, ch=76,
         corner="", hi_cells={(0, 3), (1, 3)})
sc.add(text(90, 468, "now suppose held-out data contains  a -> x", 26, HAND))
sc.add(box(90, 512, 700, 150, bg=BG_RED))
sc.add(text(115, 534, "P(word) = 0.6 × 0.2 × 0.00 × 0.4  =  0", 26, CODE))
sc.add(text(115, 590, "one zero anywhere destroys the entire sequence —\n"
                      "that's what multiplying means", 21, HAND))
sc.add(box(90, 686, 700, 145, bg=BG_RED))
sc.add(text(115, 708, "− log(0)  =  ∞", 34, CODE))
sc.add(text(115, 772, "the loss is not large. it is undefined. the metric breaks.",
            21, HAND))
sc.add(box(880, 220, 620, 300, bg=BG_YELLOW))
sc.add(text(910, 250, "Zero is a very strong claim.", 30, HAND))
sc.add(text(910, 305,
            "The model is asserting that  a -> x  is\nIMPOSSIBLE, on the evidence of "
            "a\nfew hundred names.\n\nNot observing something in a small\nsample is not "
            "proof it can't happen.", 22, HAND))
sc.note(880, 570,
        "This is the maximum-likelihood\nestimate being too confident.\n\n"
        "Which means the fix has to\ndeliberately move AWAY from\nthe maximum-likelihood "
        "estimate.")

# =============================================================== 21 smoothing
sc = cv.scene("21 · Add-k smoothing")
sc.heading("Give every possible transition a small head start.")
sc.add(text(90, 200, "observed", 22, HAND, GRAY))
sc.table(90, 240, ["n", "v", "<END>", "x"], ["count"], [[1, 1, 2, 0]],
         cw=130, ch=70, corner="")
sc.add(arrow(300, 400, 300, 460, stroke=GREEN, sw=3))
sc.add(text(320, 405, "+1 to every allowed cell", 22, HAND, GREEN))
sc.add(text(90, 480, "smoothed", 22, HAND, GRAY))
sc.table(90, 520, ["n", "v", "<END>", "x"], ["count", "P"],
         [[2, 2, 3, 1], ["0.250", "0.250", "0.375", "0.125"]],
         cw=130, ch=70, corner="")
sc.add(text(95, 744, "new total = 8", 24, CODE, RED))
sc.add(text(95, 800, "x is now unlikely, instead of impossible — "
                     "and the row still adds to 1.", 24, HAND, GREEN))
sc.add(box(880, 200, 630, 210, bg=BG_YELLOW))
sc.add(text(905, 228, "count(a → next) + k", 30, CODE))
sc.add(line([(905, 285), (1330, 285)], stroke=BLACK, sw=3))
sc.add(text(905, 300, "total(a) + k × A", 30, CODE))
sc.add(text(905, 355, "A = number of ALLOWED next tokens (V + 1)", 20, HAND))
sc.add(box(880, 440, 630, 180, bg=BG_RED))
sc.add(text(905, 466, "the k × A is not optional", 26, HAND))
sc.add(text(905, 510, "We added k to A cells, so the total grew by k × A.\n"
                      "Forget it and your rows won't sum to 1 — this is the\n"
                      "first thing to check when a table misbehaves.", 20, HAND))
sc.add(box(880, 650, 630, 190, bg=BG_VIOLET))
sc.add(text(905, 676, "nothing is free", 26, HAND))
sc.add(text(905, 720, "P(<END> | a) fell from 0.500 to 0.375.\n"
                      "Probability given to the unseen has to be\n"
                      "taken from the seen. That is the trade.", 20, HAND))

# ================================================================ 22 the dial
sc = cv.scene("22 · k is a dial, and it costs you")
sc.heading("Smoothing makes training loss WORSE. On purpose.")
sc.add(box(90, 210, 640, 120, bg=BG_BLUE))
sc.add(text(115, 236, "k = 0", 28, CODE))
sc.add(text(115, 282, "pure counts · unbeatable on training data · zeros everywhere",
            20, HAND))
sc.add(box(90, 360, 640, 120, bg=BG_RED))
sc.add(text(115, 386, "k → very large", 28, CODE))
sc.add(text(115, 432, "counts drowned by pseudo-counts · every row -> uniform",
            20, HAND))
sc.add(text(90, 520, "k = 0 wins on training data BY CONSTRUCTION.", 26, HAND, RED))
sc.add(text(90, 570, "So training loss cannot be the thing we tune k against.\n"
                     "Only held-out data can see the trade-off.", 24, HAND))
sc.panel(90, 660, 640, 180, "Which is the whole field, in one line", [
    "The setting that makes training loss lowest",
    "is not the setting that generalises best.",
], bg=BG_YELLOW, size=24)
# --- the curve
ox, oy, w, h = 880, 250, 560, 420
sc.add(line([(ox, oy), (ox, oy + h), (ox + w, oy + h)], stroke=BLACK, sw=3))
sc.add(text(ox - 60, oy + h / 2 - 30, "NLL", 22, HAND, GRAY))
sc.add(text(ox + w / 2 - 20, oy + h + 20, "k", 24, CODE, GRAY))
sc.add(line([(ox + 20, oy + 340), (ox + 140, oy + 300), (ox + 300, oy + 210),
             (ox + 480, oy + 90)], stroke=BLUE, sw=3))
sc.add(text(ox + 380, oy + 110, "training", 22, HAND, BLUE))
sc.add(line([(ox + 20, oy + 40), (ox + 100, oy + 200), (ox + 200, oy + 275),
             (ox + 320, oy + 250), (ox + 480, oy + 170)], stroke=GREEN, sw=3))
sc.add(text(ox + 190, oy + 310, "validation", 22, HAND, GREEN))
sc.add(text(ox + 10, oy + 10, "∞ (a zero was hit)", 18, HAND, RED))
sc.add(arrow(ox + 230, oy + 380, ox + 210, oy + 300, stroke=ORANGE))
sc.add(text(ox + 180, oy + 390, "pick k here", 22, HAND, ORANGE))
sc.add(text(ox, oy + 470, "sweep k, plot both. best experiment in the episode.",
            20, HAND, GRAY))

# ====================================================== 23 transition vs token
sc = cv.scene("23 · Two different problems")
sc.heading("Smoothing fixes one of these. It cannot touch the other.")
sc.add(box(90, 230, 660, 360, bg=BG_GREEN))
sc.add(text(120, 260, "UNSEEN TRANSITION", 30, HAND))
sc.add(text(120, 320, "a  is in the vocabulary\nx  is in the vocabulary\n"
                      "a → x  was never observed", 26, CODE))
sc.add(text(120, 460, "The row exists. The column exists.\n"
                      "The cell is simply 0.", 22, HAND))
sc.add(text(120, 540, "-> smoothing works", 26, HAND, GREEN))
sc.add(box(850, 230, 660, 360, bg=BG_RED))
sc.add(text(880, 260, "UNSEEN TOKEN", 30, HAND))
sc.add(text(880, 320, "ø  is not in the vocabulary\nat all", 26, CODE))
sc.add(text(880, 460, "There is no row, no column,\nand no integer ID.\n"
                      "There is nothing to smooth.", 22, HAND))
sc.add(text(880, 560, "-> that's a tokenizer problem", 26, HAND, RED))
sc.add(box(90, 650, 1420, 190, bg=BG_YELLOW))
sc.add(text(120, 678, "What smoothing actually changes is a belief:", 28, HAND))
sc.add(text(120, 730, "from   \"unseen means impossible\"\n"
                      "to     \"unseen means unlikely, but possible\"", 28, CODE))
sc.note(1150, 810, "(better methods exist: backoff,\ninterpolation, Kneser-Ney — later)")

# ========================================================= 24 context collapse
sc = cv.scene("24 · Limitation 1: it forgets")
sc.heading("Every history ending in 'a' is the same history.",
           "The model has no way to tell them apart.")
hist = ["ma", "pa", "za", "The cat sat on the ma"]
for i, hh in enumerate(hist):
    y = 230 + i * 100
    sc.add(box(90, y, 620, 76, hh, 26, CODE, bg=BG_GRAY))
    sc.add(arrow(720, y + 38, 860, y + 38, stroke=GRAY))
sc.add(box(880, 330, 480, 180, "P( next | a )", 40, CODE, bg=BG_RED))
sc.add(text(880, 540, "one row. same row. always.", 26, HAND, RED))
sc.add(box(90, 650, 1420, 190, bg=BG_YELLOW))
sc.add(text(120, 678, "The model cannot know:", 28, HAND))
sc.add(text(120, 728, "how it arrived at 'a'   ·   where it is in the word   ·   "
                      "whether it already repeated itself   ·\nwhat the word is about",
            24, HAND))
sc.note(1150, 196, "20 characters of context and\n2 characters of context are\n"
                   "indistinguishable to this model.")

# =========================================================== 25 local vs global
sc = cv.scene("25 · Limitation 2: locally fine, globally nonsense")
sc.heading("Every adjacent pair below was observed in training.")
sc.add(text(90, 210, "trained on:", 24, HAND, GRAY))
sc.add(text(90, 255, "anna     ava", 34, CODE))
sc.add(text(90, 330, "learned transitions:", 24, HAND, GRAY))
sc.add(text(90, 380, "a → n     n → n     n → a\na → v     v → a     a → <END>",
            28, CODE))
sc.add(arrow(700, 400, 820, 400))
sc.add(box(850, 330, 640, 150, "annnnavannava", 46, CODE, bg=BG_RED))
sc.add(text(850, 500, "not a name. not close to a name.", 24, HAND, RED))
sc.add(box(90, 570, 1420, 270, bg=BG_YELLOW))
sc.add(text(120, 598, "This is the real lesson of episode 1.", 30, HAND))
sc.add(text(120, 655,
            "The model can make every neighbouring pair plausible and still produce "
            "something with no\nshape at all. Local correctness does not compose into "
            "global coherence — and it never will,\nfor a model whose entire memory "
            "is one character wide.", 24, HAND))
sc.add(text(120, 790, "It also has no representation of meaning, and cannot transfer "
                      "anything it learns about 'a' to 'e'.", 22, HAND, GRAY))

# ================================================================= 26 the wall
sc = cv.scene("26 · The obvious fix, and why it fails")
sc.heading("\"Fine — remember two characters.\"",
           "A trigram model can tell 'ma' from 'pa'. Now count the rows you need.")
rows = [("1 character of context", "30", BG_GREEN),
        ("2 characters", "30 × 30 = 900", BG_YELLOW),
        ("3 characters", "30 × 30 × 30 = 27,000", BG_RED),
        ("10 characters", "590,000,000,000,000", BG_RED)]
for i, (label, val, colour) in enumerate(rows):
    y = 230 + i * 110
    sc.add(box(90, y, 460, 84, label, 26, HAND, bg=BG_GRAY))
    sc.add(arrow(560, y + 42, 640, y + 42, stroke=GRAY))
    sc.add(box(660, y, 540, 84, val, 26, CODE, bg=colour))
sc.add(text(90, 690, "vocabulary of 30 characters", 20, HAND, GRAY))
sc.add(box(90, 730, 1420, 110, bg=BG_RED))
sc.add(text(115, 752, "Almost every one of those rows would be empty or near-empty. "
                      "More context makes the table\nsparser and the zeros worse. "
                      "Counting cannot be the answer.", 22, HAND))
sc.note(1250, 250, "(and this is characters.\nimagine words.)")

# =================================================================== 27 bridge
sc = cv.scene("27 · The question for episode 2")
sc.heading("So we need something counting cannot give us.")
sc.add(box(140, 260, 1320, 200, bg=BG_YELLOW))
sc.add(text(175, 300,
            "How can a model use MORE context, and share what it learns between\n"
            "similar contexts, without storing a separate number for every\n"
            "possible history?", 34, HAND))
sc.add(text(140, 520, "Two things we need that a count table structurally cannot do:",
            26, HAND, GRAY))
sc.add(box(140, 580, 620, 200, bg=BG_BLUE))
sc.add(text(170, 606, "① generalise", 28, HAND))
sc.add(text(170, 656, "learning that  a -> n  is common\nshould say something about  "
                      "e -> n.\nEvery row is currently learned alone.", 21, HAND))
sc.add(box(840, 580, 620, 200, bg=BG_VIOLET))
sc.add(text(870, 606, "② compress", 28, HAND))
sc.add(text(870, 656, "represent context with a handful of\nnumbers instead of one "
                      "row per\npossible history.", 21, HAND))
sc.add(text(140, 820, "That is what learned parameters buy us. "
                      "Next: replace counting with weights.", 26, HAND, ORANGE))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "episode_01_bigram.excalidraw")
print(f"episode_01_bigram.excalidraw: {cv.save(out)} elements, {cv._n} scenes")
