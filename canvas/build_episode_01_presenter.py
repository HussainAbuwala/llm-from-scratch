#!/usr/bin/env python3
"""Generate the recording canvas and matching speaker notes. No dependencies.

Run beside excalidraw_kit.py; --kit-dir supports a separate staging directory.
Existing study canvases are never overwritten.
"""
import argparse
import json
import math
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--kit-dir', type=Path, default=Path(__file__).resolve().parent)
ap.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
args = ap.parse_args()
sys.path.insert(0, str(args.kit_dir))
from excalidraw_kit import *

cv = Canvas()
notes = []
ROWS = ['START', 'a', 'n', 'v']
COLS = ['a', 'n', 'v', 'END']
WORDS = [['START', *w, 'END'] for w in ['anna', 'ava']]
PAIRS = [(wi, i, a, b) for wi, word in enumerate(WORDS)
         for i, (a, b) in enumerate(zip(word, word[1:]))]
COUNTS = [[0 for _ in COLS] for _ in ROWS]
for _, _, a, b in PAIRS:
    COUNTS[ROWS.index(a)][COLS.index(b)] += 1
PROBS = [[v / sum(row) for v in row] for row in COUNTS]


def scene(chapter, title, say, action='', seconds=45):
    number = len(notes) + 1
    sc = cv.scene(f'{number:02d} · {title}')
    sc.add(text(80, 45, chapter.upper(), 26, NORMAL, VIOLET))
    sc.add(text(80, 98, title, 48, HAND))
    sc.add(text(80, 842, f'LLM from first principles  /  01 theory', 24, NORMAL, BLACK))
    sc.add(text(1130, 842, f'{number:02d}', 24, CODE, BLACK))
    notes.append((number, title, say, action, seconds))
    return sc


def txt(sc, x, y, s, size=34, color=BLACK, mono=False):
    sc.add(text(x, y, s, size, CODE if mono else NORMAL, color))


def takeaway(sc, s):
    sc.add(box(80, 724, 1100, 82, s, 32, NORMAL, bg=BG_YELLOW))


def cards(sc, tokens, x=80, y=220, active=(), width=145):
    for i, token in enumerate(tokens):
        bg = BG_YELLOW if i in active else BG_GREEN if token == 'START' else BG_RED if token == 'END' else BG_BLUE
        sc.add(box(x+i*(width+16), y, width, 84, token, 30, CODE, bg=bg))


def matrix(sc, cells, active=None, row=None):
    txt(sc, 290, 338, 'NEXT TOKEN →', 26)
    sc.table(80, 390, COLS, ROWS, cells, cw=148, ch=60, size=30,
             hi_cells=[] if active is None else [active],
             hi_row=row, corner='FROM ↓')


sc = scene('The question', 'Two names. A new possibility.',
    'These are the only two names our model has seen: anna and ava. This tiny table can produce ana. It can also produce this awkward string. Today we build the table, follow its choices, and calculate how well it predicts.',
    'Point to the training names, then ana, then the awkward example. These are possible paths, not claimed recorded program outputs.', 60)
txt(sc, 80, 225, 'TRAINING EXAMPLES', 28)
txt(sc, 80, 285, 'anna    ava', 66, mono=True)
txt(sc, 80, 420, 'POSSIBLE OUTPUTS', 28)
txt(sc, 80, 478, 'ana    annnava', 66, mono=True)
takeaway(sc, 'A small language model. Every number visible.')

sc = scene('The contract', 'Predict chances. Then choose.',
    'Our model assigns a probability to each possible next token. A separate rule chooses one. Today a token is one character, plus special boundary tokens. This is not yet a neural network or a modern LLM.',
    'Trace context → probabilities → choice. The numbers are a preview; counting will explain them.', 70)
sc.add(box(80, 270, 250, 130, 'current: a', 34, CODE, bg=BG_BLUE))
sc.add(arrow(350, 335, 460, 335))
sc.table(500, 235, ['chance'], COLS, [['0.00'],['0.25'],['0.25'],['0.50']], cw=190, ch=75, size=32, corner='next')
txt(sc, 1050, 285, 'choose\none token', 40)
sc.add(arrow(900, 335, 1030, 335))
takeaway(sc, 'The chosen token becomes the next context.')

sc = scene('Tokens and boundaries', 'Give each name a beginning and an end.',
    'We split anna into character tokens. START selects the first-character distribution. END is a target: the model must learn when to stop. Our ordinary vocabulary is a, n, v; allowed predictions are a, n, v, END. START is only a context here.',
    'Point to both boundaries. Explain START and END are each one special token.', 90)
cards(sc, WORDS[0])
txt(sc, 80, 385, 'START → how a name begins', 40)
txt(sc, 80, 470, 'END → when a name finishes', 40)
txt(sc, 80, 590, 'Character vocabulary:  a   n   v', 36)
takeaway(sc, 'Four letters → five next-token predictions.')

running = [[0]*4 for _ in ROWS]
for step in range(10):
    if step:
        wi, i, a, b = PAIRS[step-1]
        running[ROWS.index(a)][COLS.index(b)] += 1
    else:
        wi, i, a, b = 0, 0, None, None
    title = 'Turn adjacent pairs into counts.' if step == 0 else f'Count {step} of 9:  {a} → {b}'
    say = ('Each training pair has a current token and the next token we observed. Bigram means two tokens in the pair, but only one token of context. Rows are current tokens; columns are next tokens.' if not step else
           f'In {"anna" if wi == 0 else "ava"}, {b} follows {a}. Add one to row {a}, column {b}. The count is now {running[ROWS.index(a)][COLS.index(b)]}.')
    sc = scene('Train / count', title, say,
        'The next frame advances the window and updates one cell. Pause before revealing the final a→END count.' if step else 'Explain the empty matrix before advancing.',
        55 if not step else 18)
    cards(sc, WORDS[wi], active=() if not step else (i,i+1))
    if step:
        sc.add(box(80+i*161-6, 214, 306+12, 96, stroke=ORANGE, sw=4, bg=BG_NONE))
    matrix(sc, running, None if not step else (ROWS.index(a), COLS.index(b)))
    txt(sc, 900, 407, f'{step} / 9\nobservations', 40)
    if step:
        txt(sc, 900, 565, '+1', 70, color=GREEN, mono=True)
    takeaway(sc, 'a → n and n → a are different observations.')

sc = scene('Train / normalize', 'What followed a?',
    'Across the two names, a has four outgoing observations. One n, one v, two ENDs. Ask how often a ended a name before revealing the probabilities.',
    'Count all four tickets. The two END tickets are two observations of the same outcome.', 60)
cards(sc, ['n','v','END','END'], y=240, width=180)
sc.table(80, 410, COLS, ['count'], [COUNTS[1]], cw=190, ch=85, size=36)
takeaway(sc, 'Four observations. END owns two of them.')

sc = scene('Train / normalize', 'Divide by the row total.',
    'Each probability is its count divided by four. A zero, one quarter, one quarter, and one half. They sum to one. Normalization preserves the proportions.',
    'Trace counts to fractions to probabilities. Read the denominator out loud.', 80)
sc.table(80, 235, COLS, ['count','divide','chance'], [COUNTS[1],['0/4','1/4','1/4','2/4'],['0.00','0.25','0.25','0.50']], cw=210, ch=95, size=36)
takeaway(sc, 'P(next = n | current = a) = 0.25')

sc = scene('The model', 'Training is finished.',
    'Do the same normalization for every row. This probability table, its token labels, and the boundary rules are the finished model. Counting and normalization fitted it; there is no hidden neural network.',
    'Read one entry from the n row so the later generation step is familiar.', 55)
matrix(sc, [[f'{p:.2f}' for p in r] for r in PROBS])
txt(sc, 900, 250, 'Token labels\nBoundary rules\nProbability table', 40)
takeaway(sc, 'Generation and evaluation use this fixed table.')

path = ['START','a','n','a','END']
for step in range(5):
    title = 'Begin at START.' if step == 0 else f'Choose {path[step]} from the {path[step-1]} row.'
    say = ('We will follow one possible sampling path. Sampling means drawing according to the probabilities: imagine the four tickets from the a row, selecting one at random, then replacing it before the next draw. It is selected for explanation; the path is not predetermined by the table.' if not step else
           f'Look up {path[step-1]}. Select {path[step]} with probability {PROBS[ROWS.index(path[step-1])][COLS.index(path[step])]:.2f}. '+('END stops generation; the printed name is ana.' if step==4 else 'The selected token becomes the next current token.'))
    sc = scene('Generate / possible sampling path', title, say,
        'Advance once per choice; the table stays fixed. At a, explain that END is more likely but n remains possible.', 35)
    cards(sc, path[:step+1], active=(step,))
    matrix(sc, [[f'{p:.2f}' for p in r] for r in PROBS],
           None if not step else (ROWS.index(path[step-1]),COLS.index(path[step])))
    txt(sc, 900, 407, 'OUTPUT', 28)
    txt(sc, 900, 465, ''.join(path[1:min(step+1,4)]) or '—', 64, mono=True)
    takeaway(sc, 'No answer key. Each selection continues the sequence.')

sc = scene('Generate / choosing rule', 'Greedy takes the largest probability.',
    'From START we get a. At a, END has probability one half, the largest. Greedy therefore produces a. Sampling can take the quarter-probability branch to n. Neither rule retrains the model. Code will use a maximum-length guard and mark truncation.',
    'Ask what greedy chooses after a before pointing at END.', 70)
txt(sc, 80, 240, 'GREEDY', 30)
cards(sc, ['START','a','END'], y=300)
txt(sc, 80, 435, 'SAMPLING: ONE POSSIBLE PATH', 30)
cards(sc, path, y=495)
takeaway(sc, 'Same probabilities. Different selection rule.')

sc = scene('Evaluate / the question', 'A nice sample is not a score.',
    'A single nice output can be cherry-picked. We need to measure probabilities on text that did not contribute to training. Ana is a preselected worked evaluation example, not a benchmark proving quality.',
    'Pause at the question before advancing.', 50)
txt(sc, 80, 260, 'ana', 94, mono=True)
txt(sc, 80, 450, 'Did the model predict well,\nor did we pick a nice example?', 48)
takeaway(sc, 'Score held-out text with the table frozen.')

sc = scene('Evaluate / answer key', 'This time, the text supplies the targets.',
    'Training used anna and ava. We score the separate example ana. We do not sample here. At each position, look up the probability of the actual next token, using the actual preceding token. This is four predictions including END.',
    'Point to training versus held-out labels, then read all four probabilities.', 80)
txt(sc, 80, 207, 'TRAIN: anna, ava       SCORE: ana', 34, mono=True)
sc.table(80, 305, ['current','target','P(target)'], ['1','2','3','4'],
         [['START','a','1.00'],['a','n','0.25'],['n','a','0.50'],['a','END','0.50']], cw=250, ch=78, size=34)
takeaway(sc, 'Evaluation measures the model. It does not update it.')

sc = scene('Evaluate / likelihood', 'Every step must happen.',
    'The whole sequence requires all four conditional choices, so we multiply. This is the chain rule of probability with our one-token context assumption. We are not assuming the successive characters are independent.',
    'Point to each arrow and read its probability.', 65)
cards(sc, path, y=250, width=175)
for i,p in enumerate(['1.00','0.25','0.50','0.50']):
    txt(sc, 160+i*191, 365, p, 34, mono=True)
txt(sc, 80, 505, 'P(ana + END) = 1 × ¼ × ½ × ½', 44)
takeaway(sc, 'Sequence probability = 1/16 = 0.0625')

sc = scene('Evaluate / likelihood', 'A one-in-sixteen path.',
    'If we independently sample many times, this exact complete name occurs with probability one sixteenth. Out of sixteen attempts, the expected number is one, not a guarantee of exactly one. Each factor keeps a fraction of the remaining matching paths.',
    'Walk through expected matching counts from left to right.', 55)
for i,(n,p) in enumerate([('16','× 1'),('16','× ¼'),('4','× ½'),('2','× ½'),('1','')]):
    sc.add(box(80+i*285, 300, 185, 140, n, 62, CODE, bg=BG_BLUE if i<4 else BG_GREEN))
    if p:
        txt(sc, 80+i*285, 495, p, 38)
txt(sc, 80, 215, 'EXPECTED MATCHING ATTEMPTS', 28)
takeaway(sc, 'Expected counts, not guaranteed sampling results.')

sc = scene('Evaluate / logarithms', 'Long products become tiny.',
    'A thousand factors of one tenth gives ten to the minus one thousand. Ordinary floating-point arithmetic cannot store that tiny result. We need to accumulate evidence without multiplying it into zero.',
    'Let the exponent land; introduce the next frame as a tool for this problem.', 45)
txt(sc, 80, 270, '0.1 × 0.1 × 0.1 × …', 66, mono=True)
txt(sc, 80, 405, '1,000 factors → 10⁻¹⁰⁰⁰', 54)
txt(sc, 80, 540, 'Too small for ordinary floating point.', 40)
takeaway(sc, 'Use logs to turn the product into a sum.')

sc = scene('Evaluate / logarithms', 'A logarithm asks for the exponent.',
    'Ten cubed is one thousand, so log base ten of one thousand is three. We use natural log, ln, with base e about 2.718. The useful rule is log of a product equals the sum of the logs. No calculus is needed here.',
    'Read the top equation forwards and the second backwards.', 85)
txt(sc, 80, 245, '10³ = 1000', 66)
txt(sc, 80, 360, 'log₁₀(1000) = 3', 66)
txt(sc, 80, 500, 'ln uses base e ≈ 2.718', 38)
takeaway(sc, 'ln(a × b) = ln(a) + ln(b)')

for stage in range(3):
    sc = scene('Evaluate / negative log-likelihood',
        ['Turn each probability into a log.', 'Negate: unlikely targets cost more.', 'Average over all four predictions.'][stage],
        ['The logs are zero, minus 1.386, minus 0.693, and minus 0.693. Adding gives minus 2.773 after rounding; this equals the log of one sixteenth. We sum logs directly, rather than forming a tiny product first.',
         'For positive probabilities at most one, logs are non-positive. Negating gives a nonnegative penalty. High probability on the actual target gives a small penalty; low probability gives a large penalty.',
         'Add the negative log penalties and divide by four predictions, including END. The result is 0.693 nats per prediction. Nats means we used natural logs. For a dataset, sum all transition penalties and divide by all transitions, not by the number of names.'][stage],
        'Use the same rows throughout. Only the right-hand column changes or the average appears.', [80,65,80][stage])
    vals = ['0.000','−1.386','−0.693','−0.693'] if stage==0 else ['0.000','1.386','0.693','0.693']
    sc.table(80, 225, ['transition','P','ln P' if stage==0 else '−ln P'], ['1','2','3','4'],
        [[a,p,v] for a,p,v in zip(['START→a','a→n','n→a','a→END'],['1.00','0.25','0.50','0.50'],vals)], cw=270,ch=85,size=34)
    takeaway(sc, ['ln(1/16) ≈ −2.773', 'Negative log-likelihood: lower penalty is better.', '(0 + 1.386 + 0.693 + 0.693) / 4 ≈ 0.693 nats'][stage])

sc = scene('Evaluate / baselines', 'Lower than what?',
    'Uniform gives each of our four allowed outcomes one quarter. Unigram uses overall training target frequencies and ignores the current character: a four, n two, v one, END two, nine in total. The bigram uses context. All three score the same held-out ana with the same vocabulary and END convention. One character of context helped on this example; we need more held-out data to judge generalization.',
    'Read the unigram counts before the score. Do not claim these numbers establish real-world quality.', 100)
sc.table(80, 235, ['model','uses','NLL'], ['1','2','3'],
         [['uniform','equal chances','1.386'],['unigram','frequency','1.158'],['bigram','last character','0.693']], cw=320,ch=100,size=34)
txt(sc, 80, 675, 'Unigram targets: a:4, n:2, v:1, END:2', 30, mono=True)
takeaway(sc, 'Same held-out example. Same vocabulary. Same metric.')

sc = scene('Smoothing / the failure', 'Known characters. An unseen pair.',
    'Here is a constructed stress example: avna. V and n are known characters, but v followed by n never appeared in training. One zero makes the complete path probability zero. As probability approaches zero, negative log loss grows without bound. This is an unseen pair, not an unknown token.',
    'Ask what one zero does to the product. Then point to the zero cell.', 75)
cards(sc, ['START','a','v','n','a','END'], active=(2,3))
sc.table(80, 390, COLS, ['v →'], [['1.00','0.00','0.00','0.00']],cw=195,ch=90,size=36,hi_cells=[(0,1)])
txt(sc, 80, 625, 'P(avna + END) = 1 × ¼ × 0 × ½ × ½ = 0', 36)
takeaway(sc, 'Zero probability means an infinite NLL penalty.')

for stage in range(2):
    sc = scene('Smoothing / add one', ['Add one to every allowed outcome.', 'Normalize again. Probability moves.'][stage],
        ['Add one pseudo-count to all four allowed outcomes, not just the troublesome n cell. The v row changes from one, zero, zero, zero to two, one, one, one. Total five. Apply this same rule to every row when building the smoothed model.',
         'Divide by five: point four, point two, point two, point two. The unseen v to n now gets a chance. That chance comes from observed v to a, which falls from one to point four. Smoothing redistributes probability; it cannot add a missing token to the vocabulary.'][stage],
        'Trace all four columns. The denominator changes because every cell received one.', 70)
    sc.table(80, 225, COLS, ['observed','add 1','new count']+(['chance'] if stage else []),
        [[1,0,0,0],['+1','+1','+1','+1'],[2,1,1,1]]+([['0.40','0.20','0.20','0.20']] if stage else []), cw=215,ch=85,size=34)
    takeaway(sc, 'New total: 1 + 4 = 5' if not stage else 'P(n | v): 0 → 0.20     P(a | v): 1 → 0.40')

sc = scene('Smoothing / the strength', 'One is a choice. We can add k.',
    'Instead of adding one, we can add a smaller positive value k to every allowed cell. The denominator increases by four k because there are four outcomes in each row. Zero means the original unsmoothed table. We will compare choices on validation data in the build video.',
    'Point to k in the numerator and four k in the denominator. Explain both before reading the expression.', 55)
txt(sc, 80, 255, 'observed count + k', 52)
sc.add(line([(80,345),(1060,345)],sw=3))
txt(sc, 80, 390, 'row total + 4 × k', 52)
txt(sc, 80, 550, 'k = 0: no smoothing     k = 1: add one', 36)
takeaway(sc, 'Add k to all four outcomes, then normalize.')

sc = scene('Smoothing / the tradeoff', 'A safer guess can score worse.',
    'The original ana score was point 693. With add one applied to every row, it becomes about 1.040: worse. Meanwhile the previously zero-probability avna path becomes possible. Smoothing is protection against limited evidence, not a guaranteed improvement on every example. In code we will compare smoothing strengths on validation data; the test set is saved for final evaluation.',
    'Explicitly say the whole table is smoothed for this comparison.', 75)
sc.table(80, 260, ['model','NLL on ana'], ['1','2'], [['unsmoothed','0.693'],['add one','1.040']], cw=370,ch=115,size=38)
txt(sc, 80, 640, 'Smoothed across every row, including START.', 34)
takeaway(sc, 'Choose smoothing strength using validation data.')

sc = scene('The limitation', 'Different histories. The same last character.',
    'The history could be a, ana, or ava. Each ends in a, so each queries exactly the same row. This model has no way to use how it got there. Giving it more examples does not change its one-character memory.',
    'Trace all three histories into the same row.', 70)
for y,h in [(230,'a'),(385,'ana'),(540,'ava')]:
    sc.add(box(80,y,250,95,h,44,CODE,bg=BG_BLUE))
    sc.add(arrow(350,y+47,640,432,stroke=VIOLET))
sc.add(box(660,365,690,135,'P(next | a)',52,CODE,bg=BG_VIOLET))
takeaway(sc, 'The model remembers one character, not the journey.')

sc = scene('The limitation', 'Every pair fits. The whole string can fail.',
    'Return to the awkward opening example annnava. Every neighboring transition, including boundaries, is supported by the training table. That local support does not ensure a convincing complete name. It has no additional knowledge that the whole sequence should look like a name.',
    'Point out the repeated n→n transition and the familiar a→v transition.', 65)
txt(sc, 80, 235, 'annnava', 92, mono=True)
txt(sc, 80, 395, 'a→n   n→n   n→a   a→v   v→a', 42, mono=True)
txt(sc, 80, 535, 'All observed. Still an awkward result.', 42)
takeaway(sc, 'Local plausibility is not global coherence.')

sc = scene('What comes next', 'First, make the code prove it.',
    'Today we counted, normalized, generated, and scored. Next video: code this exact tiny example and verify the same numbers, then run the pipeline on a larger names dataset. Chapter two tries two-character context. Chapter three changes from counts to weights; richer shared representations come later.',
    'End on the concrete coding promise. No new combinatorics lesson here.', 60)
txt(sc, 80, 230, 'NEXT VIDEO', 28, color=VIOLET)
txt(sc, 80, 290, '1. Reproduce this exact table and score.\n2. Run it on a larger names dataset.', 42)
txt(sc, 80, 515, 'THEN: TWO CHARACTERS OF MEMORY', 28, color=VIOLET)
txt(sc, 80, 565, 'Can more context fix what we just saw?', 40)
takeaway(sc, 'Count → normalize → generate → evaluate')

# Center bound labels in saved geometry as well as in the editor.
by_id = {e['id']: e for e in cv.elements}
for e in cv.elements:
    if e['type']=='text' and e.get('containerId'):
        c=by_id[e['containerId']]
        e['x']=c['x']+(c['width']-e['width'])/2
        e['y']=c['y']+(c['height']-e['height'])/2

args.output_dir.mkdir(parents=True, exist_ok=True)
canvas_path=args.output_dir/'episode_01_presenter.excalidraw'
cv.save(str(canvas_path))
guide = '''# Episode 1 — presenter guide

Open `episode_01_presenter.excalidraw` for the theory recording. The older
`episode_01_bigram.excalidraw` remains the detailed reference canvas.

This canvas contains staged reveal frames, not one new subject per frame.
The ten count frames and five generation frames are continuous demonstrations.
Advance as you explain each step; do not spend a minute on every frame.

## Recording

- Use the frame names in numerical order. Select a frame and zoom to selection
  (Shift+2 in the current setup). Cut navigation between frames from the recording.
- All calculations are already staged. You can present without drawing or editing
  objects live. Optional circles or underlines are enough; do not read every label.
- Work from a duplicate if adding annotations. The generator overwrites this
  presenter canvas and these notes when rerun.
- The region x=1240–1600, y=650–900 is clear in every frame for a small face bubble.
  Keep the bubble entirely inside that region, or hide it for full-screen diagrams.
- Important content uses 30–94 px text; chapter/footer labels use 24–28 px.
  Record a short sample and check actual phone playback before the full session.
- Rehearse once with these notes on a separate screen. Timings are guidance;
  pause for viewer predictions and speak the fractions slowly.
- Mathematical examples are deliberate worked paths. Do not call them random
  recorded runs or a representative test benchmark.

## Teaching conventions

Tokens are characters plus START and END. START is a context only; END is an
outcome only. The compact table has row labels [START,a,n,v] and column labels
[a,n,v,END]. Numeric indexing belongs in the coding video, with separate maps
if using this compact table. START→END remains an allowed outcome; smoothing
can therefore generate an empty name. Mention that if it appears in code.

The shown NLL averages predictions including END. The `ana` path is held out
from counts but hand-selected for explanation. Add-one comparisons smooth every
row. Tune k on validation data; final test data does not choose k.

The following build video should first reproduce this exact toy example, then
use the larger dataset. Chapter 2 is trigrams; Chapter 3 is learned bigram weights.

## Sources

- Jurafsky and Martin, n-gram language models:
  https://web.stanford.edu/~jurafsky/slp3/3.pdf
- Karpathy, makemore (educational reference):
  https://github.com/karpathy/makemore

## Frame cues

'''
elapsed=0
for n,title,say,action,seconds in notes:
    guide+=f'### {n:02d} · {title}\n\nApproximate start: {elapsed//60:02d}:{elapsed%60:02d} · {seconds} seconds\n\n{say}\n\n**Present:** {action}\n\n'
    elapsed+=seconds
guide+=f'Estimated spoken sequence: {elapsed//60} minutes {elapsed%60} seconds, before additional pauses.\n'
(args.output_dir/'EPISODE_01_PRESENTER_GUIDE.md').write_text(guide)
print(f'{len(notes)} frames; estimated {elapsed/60:.1f} minutes; {canvas_path}')
