#!/usr/bin/env python3
"""Theory canvas for Episode 1: the count-based character bigram model.

This video explains the complete mechanism by hand. The following episode
implements the same pipeline in code. Worked example throughout:

    training corpus = {anna, ava}
    held-out example = ana
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
sc.add(text(110, 480, "Episode 1  ·  Understand It Before We Code It", 26, HAND, GRAY))
sc.add(box(110, 560, 700, 260, bg=BG_GRAY))
sc.add(text(140, 590, "training examples", 22, HAND, GRAY))
sc.add(text(140, 635, "anna     ava", 34, CODE))
sc.add(text(140, 700, "possible samples", 22, HAND, GRAY))
sc.add(text(140, 744, "a     ana     ava     annnava", 32, CODE, GREEN))
sc.add(box(900, 560, 590, 260, bg=BG_YELLOW, dash="dashed"))
sc.add(text(930, 590,
            "This video:\nunderstand every number by hand.\n\n"
            "Next video:\nimplement the same concepts on\na larger, realistic dataset.",
            26, HAND))

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
sc.add(text(110, 800,
            "Worked example: {a, n, v} plus <START> and <END>. "
            "Possible next tokens: a, n, v, <END>.",
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
    "From the TRAINING examples only.",
    "Our held-out word 'ana' contains only known characters,",
    "so this episode can focus on the language model itself.",
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

# ====================================================== 11 one generation trace
sc = cv.scene("11 · Generate one example")
sc.heading("Generation queries the same fixed table repeatedly.",
           "No correct target is supplied. Each sampled token becomes the next context.")

tokens = ["<START>", "a", "n", "a", "<END>"]
xs = [90, 390, 690, 990, 1290]
for x, token in zip(xs, tokens):
    colour = BG_GREEN if token == "<START>" else BG_RED if token == "<END>" else BG_BLUE
    sc.add(box(x, 235, 210, 90, token, 25, CODE, bg=colour))
for i, p in enumerate(["1.00", "0.25", "0.50", "0.50"]):
    sc.add(arrow(xs[i] + 215, 280, xs[i + 1] - 10, 280, stroke=GRAY))
    sc.add(text(xs[i] + 218, 225, p, 20, CODE, GRAY))

sc.add(text(90, 370, "What happened at each step", 26, HAND, GRAY))
steps = [
    ("current = <START>", "only a has probability 1.00", BG_GREEN),
    ("current = a", "sample n from [a:0, n:.25, v:.25, END:.50]", BG_YELLOW),
    ("current = n", "sample a from [a:.50, n:.50, v:0, END:0]", BG_VIOLET),
    ("current = a", "sample END; generation stops", BG_RED),
]
for i, (current, decision, colour) in enumerate(steps):
    y = 420 + i * 92
    sc.add(box(90, y, 330, 70, current, 20, CODE, bg=BG_GRAY, sw=1))
    sc.add(box(450, y, 900, 70, decision, 20, CODE, bg=colour, sw=1))

sc.add(box(90, 810, 1260, 60, "sampled output:  ana", 28, CODE, bg=BG_GREEN))
sc.note(1390, 500, "Every number on this frame\ncame from scenes 8 and 9.")

# =============================================== 12 greedy versus sampling
sc = cv.scene("12 · Greedy versus sampling")
sc.heading("The probability table is fixed. Only the choosing rule changes.")

sc.add(box(90, 220, 680, 500, bg=BG_BLUE))
sc.add(text(120, 250, "GREEDY", 32, HAND))
sc.add(text(120, 310, "always choose the largest probability", 22, HAND, GRAY))
sc.add(text(120, 390, "<START> → a", 30, CODE))
sc.add(text(120, 450, "a → <END>     0.50 is the largest", 26, CODE))
sc.add(text(120, 540, "output:  a", 40, CODE, RED))
sc.add(text(120, 620, "deterministic · reproducible · no variety", 21, HAND))

sc.add(box(830, 220, 680, 500, bg=BG_GREEN))
sc.add(text(860, 250, "SAMPLING", 32, HAND))
sc.add(text(860, 310, "treat the probabilities as odds", 22, HAND, GRAY))
sc.add(text(860, 390, "<START> → a → n → a → <END>", 27, CODE))
sc.add(text(860, 450, "the 0.25 branch can still be selected", 24, HAND))
sc.add(text(860, 540, "output:  ana", 40, CODE, GREEN))
sc.add(text(860, 620, "weighted randomness · seed makes a run repeatable", 20, HAND))

sc.add(box(90, 765, 1420, 90, bg=BG_YELLOW))
sc.add(text(120, 790,
            "Both methods need a maximum length. If <END> never appears, stop and mark the sample truncated.",
            23, HAND))

# ========================================================== 13 lucky or good?
sc = cv.scene("13 · Lucky, or good?")
sc.heading("Eyeballing samples is not evaluation.")
sc.add(box(120, 230, 460, 200, bg=BG_GREEN))
sc.add(text(150, 258, "the one I'd tweet", 24, HAND, GRAY))
sc.add(text(150, 310, "ana", 60, CODE))
sc.add(box(680, 230, 720, 380, bg=BG_RED))
sc.add(text(710, 258, "other samples from the same toy table", 24, HAND, GRAY))
sc.add(text(710, 310, "a\nava\navava\nannnava\nannnnnnava", 34, CODE))
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
sc.add(text(100, 200, "held-out word:  \"ana\"", 28, CODE))
rows = [("<START>", "a", 1.00), ("a", "n", 0.25),
        ("n", "a", 0.50), ("a", "<END>", 0.50)]
sc.add(text(100, 260, "input", 22, HAND, GRAY))
sc.add(text(320, 260, "true target", 22, HAND, GRAY))
sc.add(text(600, 260, "probability the model gave it", 22, HAND, GRAY))
for i, (a, b, p) in enumerate(rows):
    y = 310 + i * 92
    sc.add(box(100, y, 180, 64, a, 24, CODE, bg=BG_GRAY, sw=1))
    sc.add(box(320, y, 180, 64, b, 24, CODE, bg=BG_GREEN, sw=1))
    sc.add(box(600, y, max(20, 460 * p), 64, bg=BG_YELLOW, sw=1))
    sc.add(text(600 + max(20, 460 * p) + 16, y + 18, f"{p:.2f}", 22, CODE, GRAY))
sc.note(1180, 300, "exact values from the\n{anna, ava} table")
sc.add(box(100, 730, 660, 120, bg=BG_BLUE))
sc.add(text(125, 752, "same path, different activity", 24, HAND))
sc.add(text(125, 792, "Scene 11 sampled this path with no answer key.\n"
                      "Here, held-out text tells us which targets to score.",
            19, HAND))
sc.add(box(800, 730, 700, 120, bg=BG_VIOLET))
sc.add(text(825, 752, "evaluation never changes the model", 24, HAND))
sc.add(text(825, 792, "no counts move, no probability updates. We are taking a "
                      "measurement.", 19, HAND))

# ================================================================= 15 funnel
sc = cv.scene("15 · Why the probabilities multiply")
sc.heading("The whole word happens only if every transition happens.")
sc.add(text(100, 200, "P(\"ana\") = 1.00 × 0.25 × 0.50 × 0.50 = 0.0625", 34, CODE))
stages = [("16 attempts", 420, BG_GRAY, ""),
          ("16", 420, BG_BLUE, "× 1.00   choose a"),
          ("4", 260, BG_BLUE, "× 0.25   choose n"),
          ("2", 180, BG_VIOLET, "× 0.50   choose a"),
          ("1", 100, BG_GREEN, "× 0.50   choose <END>")]
y = 280
for label, w, colour, op in stages:
    sc.add(box(100 + (420 - w) / 2, y, w, 72, label, 26, CODE, bg=colour))
    if op:
        sc.add(text(580, y + 20, op, 24, CODE, GRAY))
    y += 108
sc.add(text(100, 820, "1 of every 16 attempts follows exactly that path on average",
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
            "ln(1.00)  =   0.00\nln(0.25)  ≈  -1.39\n"
            "ln(0.50)  ≈  -0.69\nln(0.50)  ≈  -0.69\n"
            "----------------------\nsum       ≈  -2.77", 30, CODE))
sc.add(text(790, 570, "and directly:", 22, HAND, GRAY))
sc.add(text(790, 620, "ln(0.0625) ≈ -2.77", 30, CODE, GREEN))
sc.add(box(780, 700, 620, 140, bg=BG_GREEN))
sc.add(text(805, 726, "Probabilities live in (0, 1],", 24, HAND))
sc.add(text(805, 770, "so their logs are always ≤ 0. Hold that thought.",
            24, HAND))

# ==================================================================== 17 NLL
sc = cv.scene("17 · Negative log-likelihood")
sc.heading("Negative log-likelihood turns the path into a loss.",
           "Higher probability on the true target means a smaller penalty.")
sc.table(90, 230, ["P(target)", "−ln P(target)"],
         ["START → a", "a → n", "n → a", "a → END"],
         [["1.00", "0.000"], ["0.25", "1.386"],
          ["0.50", "0.693"], ["0.50", "0.693"]],
         cw=260, ch=82, corner="transition")
sc.add(box(90, 650, 700, 170, bg=BG_YELLOW))
sc.add(text(120, 676, "average NLL for 'ana'", 28, HAND))
sc.add(text(120, 730, "(0 + 1.386 + 0.693 + 0.693) ÷ 4", 27, CODE))
sc.add(text(120, 778, "= 0.693 nats per transition", 27, CODE, GREEN))
sc.panel(880, 230, 630, 240, "Read NLL as surprise", [
    "100% on the target  →  penalty 0",
    "50% on the target   →  penalty 0.693",
    "25% on the target   →  penalty 1.386",
    "lower is better",
], bg=BG_BLUE, size=22)
sc.panel(880, 510, 630, 210, "Why average?", [
    "Total penalty grows with the amount of text.",
    "Divide by the number of evaluated transitions",
    "so datasets and words of different lengths can",
    "be compared on a per-prediction basis.",
], bg=BG_GREEN, size=21)
sc.add(text(880, 770, "generation creates text · evaluation measures text",
            21, HAND, GRAY))

# ============================================================== 18 baselines
sc = cv.scene("18 · Lower than what?")
sc.heading("Is 0.693 good? Compare it with simpler models.",
           "Use the same training corpus, held-out word, vocabulary and metric.")
sc.add(box(90, 240, 440, 280, bg=BG_GRAY))
sc.add(text(115, 266, "UNIFORM", 30, HAND, GRAY))
sc.add(text(115, 320, "4 allowed next tokens\neach gets 1 / 4", 22, CODE))
sc.add(text(115, 420, "eval NLL = ln(4)\n         = 1.386", 26, CODE, RED))
sc.add(box(560, 240, 440, 280, bg=BG_BLUE))
sc.add(text(585, 266, "UNIGRAM", 30, HAND))
sc.add(text(585, 320, "training target counts\n[a:4, n:2, v:1, END:2]", 21, CODE))
sc.add(text(585, 420, "eval NLL for ana\n= 1.158", 26, CODE))
sc.add(box(1030, 240, 470, 280, bg=BG_GREEN))
sc.add(text(1055, 266, "BIGRAM", 30, HAND))
sc.add(text(1055, 320, "one character\nof context", 22, CODE))
sc.add(text(1055, 420, "eval NLL for ana\n= 0.693", 26, CODE, GREEN))
sc.add(arrow(530, 365, 560, 365, stroke=GRAY))
sc.add(arrow(1000, 365, 1030, 365, stroke=GRAY))
sc.add(box(90, 575, 1410, 230, bg=BG_YELLOW))
sc.add(text(120, 602, "The comparison answers three different questions:", 28, HAND))
sc.add(text(120, 654,
            "uniform: did we beat guessing?\n"
            "unigram: did knowing character frequency help?\n"
            "bigram: did one character of context help?", 24, CODE))
sc.add(text(120, 770,
            "For this toy evaluation:  0.693 < 1.158 < 1.386.  Context helped.",
            23, HAND, GREEN))

# ======================================================= 19 unseen transition
sc = cv.scene("19 · The zero")
sc.heading("Both v and n are known. The transition v → n was never observed.")
sc.table(90, 220, ["a", "n", "v", "<END>"], ["count", "P"],
         [[1, 0, 0, 0], ["1.00", "0.00", "0.00", "0.00"]], cw=150, ch=76,
         corner="v → next", hi_cells={(0, 1), (1, 1)})
sc.add(text(90, 468, "held-out example:  avna", 26, CODE))
sc.add(box(90, 512, 760, 150, bg=BG_RED))
sc.add(text(115, 534,
            "P(\"avna\") = 1.00 × 0.25 × 0.00 × 0.50 × 0.50 = 0",
            24, CODE))
sc.add(text(115, 590, "one zero destroys the complete sequence probability",
            21, HAND))
sc.add(box(90, 686, 760, 145, bg=BG_RED))
sc.add(text(115, 708, "−log(0) = ∞", 34, CODE))
sc.add(text(115, 772, "the evaluation loss becomes infinite", 21, HAND))
sc.add(box(920, 220, 580, 300, bg=BG_YELLOW))
sc.add(text(950, 250, "Zero is a very strong claim.", 30, HAND))
sc.add(text(950, 305,
            "It says v → n is impossible.\n\n"
            "But our evidence was only two names.\n"
            "Not observing a possible transition is\n"
            "not proof that it can never happen.", 22, HAND))
sc.note(920, 570,
        "This is an unseen TRANSITION, not an\nunseen token: v and n already have IDs,\nrows and columns.")

# =============================================================== 20 smoothing
sc = cv.scene("20 · Add-k smoothing")
sc.heading("Give every allowed transition a small head start.",
           "Use k = 1 here so the arithmetic stays visible.")
sc.add(text(90, 200, "observed v row", 22, HAND, GRAY))
sc.table(90, 240, ["a", "n", "v", "<END>"], ["count"], [[1, 0, 0, 0]],
         cw=130, ch=70, corner="")
sc.add(arrow(300, 400, 300, 460, stroke=GREEN, sw=3))
sc.add(text(320, 405, "+1 to all 4 allowed cells", 22, HAND, GREEN))
sc.add(text(90, 480, "smoothed v row", 22, HAND, GRAY))
sc.table(90, 520, ["a", "n", "v", "<END>"], ["count", "P"],
         [[2, 1, 1, 1], ["0.40", "0.20", "0.20", "0.20"]],
         cw=130, ch=70, corner="")
sc.add(text(95, 744, "new total = 1 + (1 × 4) = 5", 24, CODE, RED))
sc.add(text(95, 800, "P(n | v): 0.00 → 0.20", 24, CODE, GREEN))
sc.add(box(880, 200, 630, 210, bg=BG_YELLOW))
sc.add(text(905, 228, "count(v → next) + k", 30, CODE))
sc.add(line([(905, 285), (1330, 285)], stroke=BLACK, sw=3))
sc.add(text(905, 300, "total(v) + k × 4", 30, CODE))
sc.add(text(905, 355, "4 = {a, n, v, <END>}", 20, CODE))
sc.add(box(880, 440, 630, 180, bg=BG_RED))
sc.add(text(905, 466, "nothing is free", 26, HAND))
sc.add(text(905, 510,
            "P(a | v) fell from 1.00 to 0.40.\n"
            "Probability reserved for unseen transitions\n"
            "comes from transitions we did observe.", 20, HAND))
sc.add(box(880, 650, 630, 190, bg=BG_VIOLET))
sc.add(text(905, 676, "What carries into the coding episode", 24, HAND))
sc.add(text(905, 720,
            "Use a smaller configurable k. Choose it with validation data.\n"
            "Smoothing fixes unseen pairs; it cannot invent a token\n"
            "missing from the vocabulary.", 19, HAND))

# ========================================================= 21 context collapse
sc = cv.scene("21 · Limitation 1: it forgets")
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

# =========================================================== 22 local vs global
sc = cv.scene("22 · Limitation 2: locally fine, globally nonsense")
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

# ================================================================= 23 the wall
sc = cv.scene("23 · The obvious fix, and why it fails")
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

# =================================================================== 24 bridge
sc = cv.scene("24 · Next: implement the same concepts")
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
sc.add(text(140, 812,
            "Next video: build the count-based model on a larger names dataset. "
            "Same concepts, new numbers.\nAfter that: replace counting with learned weights.",
            24, HAND, ORANGE))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "episode_01_bigram.excalidraw")
print(f"episode_01_bigram.excalidraw: {cv.save(out)} elements, {cv._n} scenes")
