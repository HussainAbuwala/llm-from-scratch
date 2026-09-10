#!/usr/bin/env python3
"""Build the Episode 02 theory recording canvas, reader, and presenter guide."""
import base64
import html
import json
from pathlib import Path
import sys

from excalidraw_kit import *
from render_preview import svg_for, FONTS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'episodes/02_trigrams'))
from lab import CountModel, windows, START, END

toy = CountModel(['anna', 'ava'], 2)
cv = Canvas()
notes = []


def txt(sc, x, y, s, size=30, color=BLACK, mono=False):
    sc.add(text(x, y, s, size, CODE if mono else HAND, color))


def scene(title, subtitle, prompt):
    n = len(notes) + 1
    sc = cv.scene(f'{n:02} · {title}')
    txt(sc, 70, 38, 'EPISODE 02  /  THEORY', 21, VIOLET)
    txt(sc, 70, 86, title, 46)
    txt(sc, 70, 152, subtitle, 26, GRAY)
    txt(sc, 70, 852, 'LLM from scratch   ·   S = START   ·   E = END', 20, GRAY)
    txt(sc, 1400, 848, f'{n:02}', 26, GRAY, True)
    notes.append({'title': title, 'prompt': prompt})
    return sc


def takeaway(sc, s):
    sc.add(box(70, 745, 1460, 78, s, 30, HAND, bg=BG_YELLOW))


def card(sc, x, y, label, color=BG_BLUE, w=130, h=90, size=36):
    sc.add(box(x, y, w, h, label, size, CODE, bg=color))


def context_name(context):
    return ','.join('S' if c == START else c for c in context)


sc = scene('One more character of memory.', 'The model still predicts one next token.',
           'For the prefix ann, what context does each model use?')
txt(sc, 130, 250, 'BIGRAM', 30, BLUE)
card(sc, 170, 325, 'n')
sc.add(arrow(335, 370, 490, 370))
card(sc, 530, 325, '?', BG_GREEN)
txt(sc, 150, 470, '1 context + 1 target', 28)
txt(sc, 900, 250, 'TRIGRAM', 30, VIOLET)
card(sc, 890, 325, 'n'); card(sc, 1040, 325, 'n')
sc.add(arrow(1200, 370, 1300, 370))
card(sc, 1340, 325, '?', BG_GREEN)
txt(sc, 880, 470, '2 context + 1 target', 28)
txt(sc, 130, 600, 'Training names stay the same:', 32)
txt(sc, 880, 585, 'anna   ava', 50, BLUE, True)
takeaway(sc, 'Trigram counts three tokens in the window, not three tokens to predict.')

sc = scene('Split one row into two questions.', 'Training examples: anna and ava. Counts shown before smoothing.',
           'Why can the trigram distinguish an from nn when the bigram cannot?')
card(sc, 90, 330, 'n', w=180)
sc.add(arrow(295, 375, 390, 375))
sc.add(box(420, 265, 340, 220, 'next n: 1/2\nnext a: 1/2', 34, CODE, bg=BG_GRAY))
txt(sc, 90, 565, 'After either an or nn,\nthe bigram uses this row.', 32)
sc.add(arrow(800, 365, 900, 265, stroke=VIOLET))
sc.add(arrow(800, 385, 900, 540, stroke=VIOLET))
sc.add(box(930, 220, 540, 115, '(a,n) -> n : 1/1', 34, CODE, bg=BG_BLUE))
sc.add(box(930, 480, 540, 115, '(n,n) -> a : 1/1', 34, CODE, bg=BG_GREEN))
takeaway(sc, 'More specific questions. Fewer observations behind each answer.')

sc = scene('Two START pads. One END target.', 'Pads supply context; they are never predicted.',
           'How many predictions does anna contribute? Why does extra padding not change that?')
for i, token in enumerate(['S','S','a','n','n','a','E']):
    card(sc, 220+i*165, 275, token, BG_GRAY if token=='S' else BG_RED if token=='E' else BG_BLUE)
sc.add(box(207, 258, 322, 125, bg=BG_NONE, stroke=VIOLET, sw=4))
txt(sc, 220, 435, 'initial context', 30, VIOLET)
txt(sc, 600, 435, 'four characters + one END', 32)
txt(sc, 220, 570, 'Reset to (S,S) at the start of every name.', 36)
takeaway(sc, 'anna still contributes 5 predictions; ava contributes 4. Total = 9.')

for step, (context, target) in enumerate(windows('anna', 2)):
    sc = scene(f'Slide the window: anna, step {step+1} of 5.',
               'Blue cards are the context. The green card is the observed target.',
               'Before advancing, predict the next context and target.')
    tokens = ['S','S','a','n','n','a','E']
    for i, token in enumerate(tokens):
        color = BG_GREEN if i==step+2 else BG_BLUE if step<=i<step+2 else BG_GRAY
        card(sc, 220+i*165, 270, token, color)
    sc.add(box(212+step*165, 257, 310, 117, bg=BG_NONE, stroke=BLUE, sw=4))
    sc.add(arrow(750, 405, 750, 490, stroke=GRAY))
    label = 'E' if target==END else target
    sc.add(box(370, 520, 830, 115, f'({context_name(context)}) -> {label}     count +1', 40, CODE, bg=BG_VIOLET))
    takeaway(sc, 'Stop after predicting END.' if target==END else 'Move forward one position. Keep the last two tokens as context.')

sc = scene('Add ava. Combine identical observations.', 'Each context is a separate row. Columns are possible next tokens.',
           'Why does row (S,a) total two, while row (a,n) totals one?')
contexts = list(toy.counts)
cells = [[toy.counts[c].get(t, 0) for t in toy.outcomes] for c in contexts]
sc.table(75, 220, ['a','n','v','E'], [context_name(c) for c in contexts], cells,
         cw=142, ch=59, size=28, hi_row=1)
txt(sc, 870, 240, 'ava adds these four:', 32)
for i, (c, t) in enumerate(windows('ava', 2)):
    txt(sc, 900, 320+i*72, f'({context_name(c)}) -> {"E" if t==END else t}', 32, BLUE, True)
takeaway(sc, '7 observed context rows contain all 9 training observations.')

sc = scene('Divide each row by its own total.', 'The denominator is the evidence for this context, not for the whole dataset.',
           'Explain 1/2 and 1 without referring to the word normalization.')
sc.add(box(90, 240, 640, 100, '(S,a):   n=1   v=1', 34, CODE, bg=BG_BLUE))
sc.add(box(880, 240, 600, 100, '(a,n):   n=1', 34, CODE, bg=BG_BLUE))
txt(sc, 150, 410, 'row total = 2', 34, GRAY, True)
txt(sc, 930, 410, 'row total = 1', 34, GRAY, True)
sc.add(box(90, 505, 640, 120, 'P(n | S,a) = 1/2', 40, CODE, bg=BG_GREEN))
sc.add(box(880, 505, 600, 120, 'P(n | a,n) = 1', 38, CODE, bg=BG_GREEN))
takeaway(sc, 'Every observed row becomes its own probability distribution.')

sc = scene('Follow both possible generation paths.', 'Unsmoothed toy model. Every arrow after the branch has probability 1.',
           'Why do these convincing samples say little about unseen names?')
sc.add(box(80, 345, 230, 110, '(S,S)', 38, CODE, bg=BG_BLUE))
sc.add(arrow(330, 400, 470, 400)); txt(sc, 350, 345, 'a: 1', 25, GRAY, True)
sc.add(box(490, 345, 230, 110, '(S,a)', 38, CODE, bg=BG_BLUE))
sc.add(arrow(745, 380, 915, 285)); txt(sc, 780, 260, 'n: 1/2', 26, BLUE, True)
sc.add(arrow(745, 420, 915, 555)); txt(sc, 780, 565, 'v: 1/2', 26, VIOLET, True)
sc.add(box(940, 220, 550, 140, 'n -> a -> E\nanna: P = 1/2', 32, CODE, bg=BG_GREEN))
sc.add(box(940, 500, 550, 140, 'a -> E\nava:  P = 1/2', 32, CODE, bg=BG_GREEN))
takeaway(sc, 'On this tiny corpus, the trigram generates only the two training names.')

sc = scene('Now ask it to score ana.', 'Evaluation follows the supplied name. It does not sample.',
           'Which exact prediction makes the complete name probability zero?')
for i, (ctx, target, p) in enumerate([('S,S','a','1'),('S,a','n','1/2'),('a,n','a','0'),('n,a','E','1')]):
    x = 90+i*380
    sc.add(box(x, 275, 330, 180, f'({ctx}) -> {target}\nP = {p}', 32, CODE, bg=BG_RED if p=='0' else BG_BLUE))
    if i<3: txt(sc, x+342, 335, '×', 32)
txt(sc, 130, 540, 'BIGRAM\nP(ana) = 1/16', 36, BLUE, True)
txt(sc, 880, 540, 'TRIGRAM\nP(ana) = 0', 36, RED, True)
takeaway(sc, 'A better training fit can reject a held-out spelling. Trigram NLL is infinite here.')

sc = scene('An empty cell is not an unseen row.', 'All these characters are known. What is missing is training evidence.',
           'Which case is 0/1, and which is 0/0? Can a row of zeros sum to one?')
sc.table(90, 275, ['a','n','v','E'], ['a,n'], [[0,1,0,0]], cw=130, ch=90, size=32, hi_cells=[(0,0)])
sc.add(box(890, 275, 560, 180, '(v,n)\nno observations at all', 34, HAND, bg=BG_RED, dash='dashed'))
txt(sc, 110, 510, 'P(a | a,n) = 0/1 = 0', 31, RED, True)
txt(sc, 910, 510, '0/0: row unspecified', 30, RED, True)
txt(sc, 110, 610, 'The context was seen.\nThis target was not.', 30)
txt(sc, 910, 610, 'Counting supplies no\npreferred distribution.', 30)
takeaway(sc, 'Zero in a known row is different from having no distribution for the row.')

sc = scene('Smoothing gives every outcome a ticket.', 'Add k=1. There are four outcomes: a, n, v, E.',
           'Why is an entirely unseen row uniform for any positive k?')
txt(sc, 95, 240, 'OBSERVED (a,n)', 30, BLUE)
sc.cards(95, 325, ['a','n','n','v','E'], w=105, h=100, gap=15, size=38,
         colors=[BG_YELLOW,BG_BLUE,BG_YELLOW,BG_YELLOW,BG_YELLOW])
txt(sc, 95, 475, '1 real ticket + 4 added tickets', 30)
txt(sc, 95, 555, 'P(a | a,n) = 1/5', 34, BLUE, True)
txt(sc, 885, 240, 'UNSEEN (v,n)', 30, VIOLET)
sc.cards(885, 325, ['a','n','v','E'], w=115, h=100, gap=18, size=38, bg=BG_YELLOW)
txt(sc, 885, 475, '0 real tickets + 4 added tickets', 28)
txt(sc, 885, 555, 'P(a | v,n) = 1/4', 32, VIOLET, True)
takeaway(sc, 'Yellow = pseudo-counts, not extra training observations.')

sc = scene('Recompute the whole path after smoothing.', 'Every row changes, including rows that already gave positive probabilities.',
           'Why would fixing only the zero step give the wrong sequence probability?')
for i, (ctx, target, p) in enumerate([('S,S','a','3/6'),('S,a','n','2/6'),('a,n','a','1/5'),('n,a','E','2/5')]):
    x=90+i*380
    sc.add(box(x, 260, 330, 160, f'({ctx}) -> {target}\n{p}', 32, CODE, bg=BG_GREEN))
    if i<3: txt(sc, x+342, 315, '×', 32)
txt(sc, 155, 490, 'P(ana) = 1/75', 46, BLUE, True)
txt(sc, 155, 590, 'NLL = ln(75) / 4 ≈ 1.079372', 42, VIOLET, True)
takeaway(sc, 'Finite now. The denominator remains four predictions, including END.')


sc = scene('100% can rest on one observation.', 'Original training names: anna and ava. No smoothing here.',
           'More certainty in the estimate does not mean more evidence.')
sc.add(box(90,250,570,130,'n -> n     n -> a',37,CODE,bg=BG_BLUE))
txt(sc,110,435,'Bigram: 2 matching observations',31)
txt(sc,110,510,'P(a | n) = 1/2',36,BLUE,True)
sc.add(arrow(700,315,840,315))
sc.add(box(890,225,570,115,'(a,n) -> n : once',34,CODE,bg=BG_VIOLET))
sc.add(box(890,380,570,115,'(n,n) -> a : once',34,CODE,bg=BG_VIOLET))
txt(sc,915,550,'P(a | n,n) = 1',36,VIOLET,True)
takeaway(sc,'A count estimate of 100% describes the sample. It is not a universal rule.')

sc = scene('What if we add a third context token?', 'Separate constructed corpus: anna, enna, inna, onna. 20 predictions in total.',
           'Four observations become four singleton rows; the predicted target stays the same.')
evidence_names=['anna','enna','inna','onna']
evidence_tri=CountModel(evidence_names,2)
evidence_four=CountModel(evidence_names,3)
sc.add(box(90,285,550,170,'(n,n) -> a\n4 observations',38,CODE,bg=BG_BLUE))
txt(sc,125,510,'2 context characters',32,BLUE)
sc.add(arrow(680,370,830,370))
for i,prefix in enumerate('aeio'):
    c=(prefix,'n','n')
    count=evidence_four.counts[c]['a']
    sc.add(box(890,225+i*110,600,85,f'({prefix},n,n) -> a : {count}',34,CODE,bg=BG_VIOLET))
txt(sc,950,690,'3 context characters',28,VIOLET)
takeaway(sc,'Same target probabilities here. Each longer-context row now has less support.')

sc = scene('A longer query can have no matching row.', 'Same separate corpus: anna, enna, inna, onna. Query a supplied history ending nnn.',
           'This is a local query, not a claim that the model generated nnn.')
sc.cards(100,240,['n','n','n'],w=130,h=90,gap=16,size=40,bg=BG_GRAY)
txt(sc,660,265,'Predict the next token after this history.',32)
sc.add(box(90,440,640,180,'TRIGRAM uses (n,n)\na followed it 4 times',33,CODE,bg=BG_BLUE))
sc.add(box(890,440,610,180,'4-GRAM uses (n,n,n)\n0 observations',32,CODE,bg=BG_RED))
takeaway(sc,'Known letters can form an unseen context. The unsmoothed row is unspecified.')

sc = scene('Each extra position multiplies possibilities.', 'Counting illustration only: alphabet a, n, v. Ignore boundaries for this frame.',
           'Three choices in each position give 3, 9, then 27 combinations.')
sc.cards(100,260,['a','n','v'],w=105,h=85,gap=15,size=38)
txt(sc,120,405,'1 position: 3',31,BLUE)
for i,pair in enumerate(['aa','an','av','na','nn','nv','va','vn','vv']):
    sc.add(box(660+(i%3)*145,240+(i//3)*100,120,75,pair,32,CODE,bg=BG_VIOLET))
txt(sc,650,570,'2 positions: 3 × 3 = 9',32,VIOLET)
txt(sc,140,655,'3 positions: 3 × 3 × 3 = 27',38,BLACK,True)
takeaway(sc,'Each extra position multiplies the ordinary-context count by the alphabet size.')

sc = scene('Include the valid START contexts.', 'Capacity calculation: A = 26 letters. Two context positions; 27 next-token outcomes.',
           'START occurs only as a prefix. END is a target, not a context.')
for x,label,count,color in [(90,'(S,S)','1',BG_GRAY),(590,'(S,letter)','26',BG_BLUE),(1090,'(letter,letter)','676',BG_VIOLET)]:
    sc.add(box(x,240,420,160,label+'\n'+count,32,CODE,bg=color))
txt(sc,155,465,'1 + 26 + 26² = 703 possible rows',38,BLUE,True)
txt(sc,155,555,'703 rows × 27 outcomes = 18,981 cells',34,BLACK,True)
takeaway(sc,'Do not count (letter,S): START cannot appear after a letter.')

sc = scene('Possible rows multiply. Data does not.', 'Calculated capacities for 26 letters; these are not experiment results.',
           'The number of observations depends on the corpus, not the context length.')
for i,m in enumerate([1,2,3,4,5]):
    rows=sum(26**power for power in range(m+1))
    y=245+i*80
    txt(sc,110,y,f'{m} context '+('character' if m==1 else 'characters'),28)
    txt(sc,635,y,f'{rows:,} rows',31,VIOLET,True)
sc.add(box(1150,270,370,320,bg=BG_BLUE))
txt(sc,1180,300,'Original toy:',28)
txt(sc,1180,360,'(4+1)+(3+1)',28,BLUE,True)
txt(sc,1180,415,'= 9',44,BLUE,True)
txt(sc,1180,505,'predictions at\nevery context size',26)
takeaway(sc,'More possible groups for the same evidence; not every group will be observed.')

sc = scene('Sparse storage saves space, not evidence.', 'Illustrative grid. Store only counts that occurred during training.',
           'Missing entries can be treated as zero when computing smoothed probabilities.')
for row in range(7):
    for col in range(10):
        active=(row,col) in {(0,0),(0,1),(1,2),(2,3),(2,4),(4,7),(6,1),(6,8)}
        sc.add(box(100+col*53,245+row*53,43,43,bg=BG_BLUE if active else BG_GRAY,sw=1))
txt(sc,110,650,'Store only the blue cells.',29,BLUE)
sc.add(arrow(680,425,840,425))
sc.add(box(890,250,580,130,'STORAGE\nSkip empty entries.',33,HAND,bg=BG_GREEN))
sc.add(box(890,475,580,155,'EVIDENCE\nMissing observations\nare still missing.',32,HAND,bg=BG_RED))
takeaway(sc,'Smoothing can be calculated when needed; it does not add real observations.')

sc = scene('Three immediate responses, each with a limit.', 'The issue is context detail relative to available representative data.',
           'No option guarantees better held-out predictions; compare choices on validation.')
for x,title,help_,limit,color in [(90,'MORE DATA','More matching\nobservations','Long contexts can\nstill be unseen.',BG_BLUE),
 (590,'SHORTER CONTEXT','Pool more evidence\ninto each row','Some useful detail\nmay be lost.',BG_VIOLET),
 (1090,'SMOOTHING','Give known outcomes\npositive probability','An empty row still\nhas no preference.',BG_GREEN)]:
    sc.add(box(x,240,420,430,bg=color))
    txt(sc,x+25,265,title,28)
    txt(sc,x+25,355,help_,29)
    txt(sc,x+25,540,limit,28)
takeaway(sc,'More data, less specific questions, and smoothing address different parts of the problem.')

sc = scene('Backoff: consult a shorter history.', 'Back to anna and ava. Illustration: fall back when the entire context is unseen.',
           'Whole-row fallback is normalized, but still allows zero-probability targets.')
sc.add(box(90,275,540,155,'(v,n)\nno observations',36,CODE,bg=BG_RED))
sc.add(arrow(670,350,850,350));txt(sc,675,275,'use suffix',25,GRAY)
sc.add(box(890,245,580,225,'n -> n : 1/2\nn -> a : 1/2\nv and END : 0',32,CODE,bg=BG_BLUE))
txt(sc,130,565,'A simple fallback can reuse evidence we already have.',34)
takeaway(sc,'This rule only repairs absent rows. It does not repair every unseen continuation.')

sc = scene('Interpolation: let both histories contribute.', 'Original toy. Both component models use k=1; mixture weights are one-half.',
           'This changes one probability; it does not establish a better whole-model score.')
sc.add(box(90,250,610,150,'TRIGRAM\nP(a | a,n) = 1/5',34,CODE,bg=BG_BLUE))
sc.add(box(890,250,610,150,'BIGRAM\nP(a | n) = 1/3',34,CODE,bg=BG_VIOLET))
sc.add(arrow(400,430,630,525,stroke=BLUE));sc.add(arrow(1190,430,970,525,stroke=VIOLET))
sc.add(box(380,545,850,115,'1/2 × 1/5 + 1/2 × 1/3 = 4/15',33,CODE,bg=BG_GREEN))
takeaway(sc,'Mix defined probability rows with nonnegative weights that sum to one.')

sc = scene('Learn to share information across contexts.', 'Later in the series: shared representations. They still need data and good training.',
           'Episode 03 introduces learned bigram weights; embeddings and the MLP arrive in Episode 07.')
for x,title,body,color in [(90,'EPISODE 02','Separate count rows\nUseful context\nSparse evidence',BG_BLUE),
 (590,'EPISODE 03','Same bigram task\nWeights + softmax\nLearn probabilities',BG_VIOLET),
 (1090,'EPISODE 07','Embeddings + MLP\nShared parameters\nAcross contexts',BG_GREEN)]:
    sc.add(box(x,255,420,350,bg=color));txt(sc,x+30,285,title,29);txt(sc,x+30,380,body,28)
sc.add(arrow(530,425,575,425));sc.add(arrow(1030,425,1075,425))
takeaway(sc,'A bigram weight table alone does not solve the longer-context sparsity problem.')

sc = scene('The tradeoff is context versus evidence.', 'A larger context can help when the data supports the distinctions it makes.',
           'Avoid claiming that all longer-context models must perform worse.')
for i,(a,b) in enumerate([('MORE CONTEXT','Distinguish situations that a shorter history merges.'),
 ('FIXED DATA','Each more specific row has at most the suffix row’s evidence.'),
 ('POSSIBLE IMPACT','Uncertain estimates, zeros, or entirely missing rows.'),
 ('PRACTICAL RESPONSE','Gather evidence, pool it, smooth, or share information.')]):
    y=240+i*110
    sc.add(box(80,y,350,80,a,25,HAND,bg=BG_BLUE));txt(sc,465,y+24,b,28)
takeaway(sc,'The model can look certain while its estimate rests on very little evidence.')

sc = scene('Next: build it and test the tradeoff.', 'The coding companion uses the larger names dataset from Episode 01.',
           'The experiment tests these ideas. It does not assume a preferred outcome.')
for i,(label,question) in enumerate([('BUILD','Counts, smoothing, evaluation, generation.'),
 ('COMPARE','How do training and held-out loss change?'),
 ('INSPECT','Which contexts are rare or entirely unseen?')]):
    y=260+i*140
    sc.add(box(100,y,300,95,label,32,HAND,bg=BG_VIOLET));txt(sc,455,y+30,question,32)
takeaway(sc,'Will more context help on real data? We will measure it in the coding video.')

sc = scene('The foundations behind this episode.', 'Established n-gram methods; our own small examples and teaching sequence.',
           'Sources support the methods, not an endorsement of this series.')
for y,title,detail in [(240,'Jurafsky & Martin · Speech and Language Processing','Chapter 3: N-gram Language Models  /  web.stanford.edu/~jurafsky/slp3'),
 (395,'Chen & Goodman · ACL 1996','An Empirical Study of Smoothing Techniques  /  aclanthology.org/P96-1041'),
 (550,'Bengio et al. · JMLR 2003','A Neural Probabilistic Language Model  /  jmlr.org/papers/v3/bengio03a.html')]:
    txt(sc,90,y,title,32,VIOLET);txt(sc,90,y+60,detail,24)
takeaway(sc,'Tiny examples reveal the mechanism; held-out experiments measure practical performance.')

# Check editable element bounds before writing. Labels use their container bounds.
frames={e['id']:e for e in cv.elements if e['type']=='frame'}
for element in cv.elements:
    if element['type']=='frame' or element.get('containerId'):
        continue
    f=frames[element['frameId']]
    x,y=element['x']-f['x'],element['y']-f['y']
    assert x>=0 and y>=0 and x+element['width']<=1600 and y+element['height']<=900, (f['name'],element.get('text'),x,y,element['width'])

# Narration is kept outside the audience canvas. Durations include pointing pauses.
script = [
(55, "Our first model remembered one character. Today we give it two. Both models still predict one next token: trigram means two context tokens plus the target. We will build a tiny table by hand, see what the extra context buys us, and see why the data matters as we keep extending that context.", "Point to one blue card, then two; keep the green question mark as the same task."),
(55, "In anna, n is followed once by n and once by a. The bigram merges those observations into one row. The trigram can distinguish an from nn. That is a useful new capability. But notice that each more specific row now has only one observation behind it.", "Trace the shared n row into the two context rows. Do not say either estimate is a universal rule."),
(45, "S means START, and E means END. Two START pads supply the first context. We predict the four letters of anna, then END: five predictions. We reset before ava, which adds four more. Padding does not add prediction targets.", "Count the five targets after the two pads."),
(20, "Our first context is START, START. The observed next character is a. Add one to that context's a count.", "Point to the blue window, then the green target, then count plus one."),
(20, "Slide one place. The context is now START, a. The observed target is n. This is a new row.", "Move attention one card to the right."),
(20, "Now a, n predicts the next n. This is the observation that will matter when we later try to score ana.", "Emphasize that the target is the second n."),
(20, "Now n, n is followed by a. The trigram keeps this evidence separate from the preceding a, n row.", "Contrast the blue pair with the preceding frame."),
(20, "Finally n, a is followed by END. We count that target and stop; we do not produce a new training window after END.", "Point to E, then pause before moving to the combined table."),
(70, "Ava adds four windows. The initial START, START to a observation repeats, so that cell becomes two. START, a gains a v alongside its n. The a, v and v, a rows are new. Seven context rows now hold all nine observations. Read each cell as a count, not yet a probability.", "Read the S,a row aloud, then check the total count is nine."),
(55, "Normalize within each row. START, a has two observations, one n and one v, giving one-half each. The a, n row has one observation, an n, giving probability one to n. Different rows have different denominators because they represent different groups of evidence.", "Follow count to row total to fraction."),
(60, "Generation begins at START, START, so a is forced. At START, a, choose n or v with equal probability. Taking n has already written an; the remaining targets are n, a, END. Taking v has written av; the remaining targets are a, END. Each complete name therefore has probability one-half. This particular unsmoothed toy table only generates its training names.", "Trace both branches. The targets written on each right-hand box come after its branch token."),
(70, "Now evaluate the supplied name ana. We follow its real characters, not a sample. The third prediction asks for a after a, n. That row only saw n, so it assigns a zero. Multiplying the path gives zero probability and infinite NLL. The old bigram assigned this name one-sixteenth. The toy shows a possible generalization failure, not that every trigram is worse.", "Stop at the red third box before multiplying the path."),
(65, "Two things can be missing. In a, n, the row exists, but its a cell is zero: zero divided by one is zero. For v, n, the entire row is unseen: zero divided by zero gives no defined distribution. An all-zero row would not sum to one. We need a policy for the missing evidence.", "Read the two denominators separately. Do not call zero over zero a probability of zero."),
(70, "Add-one smoothing adds one pseudo-count to every allowed outcome, not just to zeros. The observed a, n row has one real ticket plus four added tickets; a gets one out of five. The unseen v, n row has only the four added tickets, so it becomes uniform. Pseudo-counts are a modeling convention, not extra training observations.", "Count the five left tickets and four right tickets. State the original toy has four outcomes."),
(60, "After smoothing, recompute every step. Ana gets three-sixths, times two-sixths, times one-fifth, times two-fifths: one-seventy-fifth. Its average NLL is about 1.079372 nats per prediction, divided by four including END. Smoothing fixes the zero but also redistributes probability away from observed outcomes.", "Point through all four factors. Read the displayed decimal as approximately."),
(60, "Let's name the evidence issue. The bigram had two matching observations after n. The trigram separates them into two rows with one observation each. Both new rows look completely certain. But one hundred percent from one example says what happened in the sample, not what must happen in the population. Whether the extra distinction is useful depends on the data we want to predict.", "Contrast the evidence counts before and after splitting."),
(80, "For this next demonstration, replace the corpus with four constructed strings: anna, enna, inna, onna. Do not mix these counts with the original toy. A two-character context n, n pools four observations, all followed by a. With three context characters, we split that row into ann, enn, inn, and onn, each seen once. The probabilities are still one for a here; nothing became wrong automatically. What decreased is the support for each estimate. The corpus still supplies twenty predictions.", "Read the new corpus before touching the rows. Call a row with total count one a singleton."),
(65, "Stay with those four strings. Suppose a supplied history ends in nnn, and we ask for the next token. The trigram uses its last two tokens, nn, and has four observations. The 4-gram uses all three, nnn, and has none. This is a local query, not a generated sample. The letters are known; their longer combination is unseen. A more specific question can need a distribution that counting has never estimated.", "Point to the supplied three tokens, then compare suffix lengths. Do not reuse the original four-outcome smoothing denominator; this corpus has six outcomes."),
(55, "For the counting calculation, use just a, n, v and temporarily ignore boundaries. One position has three choices. For every first letter, the second has three choices, giving nine pairs. A third position multiplies by three again. In general, A choices in each of m positions gives A to the power m. We count possible combinations, not equally likely events.", "Scan one row of pairs, then all three rows; show the third-position multiplication."),
(65, "Now calculate capacity for 26 ordinary letters. Valid two-token contexts are START, START; START plus one letter; or two letters. That is one plus twenty-six plus six hundred seventy-six, or seven hundred three rows. Each row has twenty-seven outcomes, because END is a target and START is not. The full table would contain eighteen thousand nine hundred eighty-one cells.", "Point to the three valid context families, then multiply rows by outcomes."),
(60, "Increasing context length makes the possible row count grow quickly. These are capacity calculations, not measured experimental results. The training observation count does not grow with the context: each original toy name still supplies its letters plus one END, nine in total. We create more possible groups for the same evidence. Some longer rows may stay well supported; others are singletons or absent.", "Contrast the growing left column with the fixed nine on the right."),
(60, "We do not have to allocate every possible cell. Sparse storage keeps only observed counts. Missing entries can act as zero counts in the smoothing formula, calculated when needed. That saves space, but it adds no observations. A model can be small enough to store and still lack evidence for many contexts.", "Point to the observed blue cells, then distinguish storage from evidence."),
(80, "There are several responses. More representative data can provide more matching examples, though not every long context will be covered. A shorter context pools evidence but may lose useful distinctions. Smoothing prevents zeros for known outcomes but cannot discover a preference in an empty row. These are tools with different tradeoffs. We use held-out validation to choose settings; we do not assume any one choice always wins.", "Read the benefit and limitation of each column together."),
(80, "Return to anna and ava. The unseen v, n context has a suffix we do know: n. A simple rule is to use an observed trigram row, otherwise use the bigram for its last token, with a normalized further fallback if necessary. Here that gives half to n and half to a. This whole-row fallback is only an introductory example. It still leaves zero probabilities: in a known a, n row, a remains zero. Formal backoff smoothing has more careful probability allocation.", "Trace v,n to n. Say explicitly that missing-row fallback does not fix every missing target."),
(65, "Interpolation combines the rows instead of choosing only one. Both toy models here use add-one smoothing. For a after a, n, the trigram gives one-fifth and the bigram gives one-third. Equal weights give four-fifteenths. The full mixture remains normalized because its component distributions are normalized and its weights sum to one. This helps this one continuation; it is not proof that the whole model has a better score. One-half is just our teaching weight.", "Read the two component probabilities; optionally omit the arithmetic aloud and emphasize combining evidence."),
(60, "Later we will learn shared representations so that related contexts can inform one another through shared parameters. Episode 03 first learns a familiar bigram table with weights and softmax; it introduces parameter learning, not the full sparsity solution. Embeddings and the MLP arrive in Episode 07. They also need suitable data and training. We are building toward our small decoder-only Transformer step by step.", "Follow the series progression; do not skip the coding companion in the next frame's handoff."),
(60, "The tradeoff is not that more context is bad. More context distinguishes situations, but each more specific row can use only a subset of the observations available to its suffix. That can expose useful patterns or leave unreliable estimates and missing rows. We can gather evidence, pool it, smooth, or share information. A model's apparent certainty needs to be read alongside the evidence behind it.", "Summarize one benefit, one risk, and one response."),
(50, "In the coding companion, we will implement these models on the larger names dataset. We will compare training and held-out loss and inspect rare and unseen contexts. Does more context help, and when does it stop helping for those choices? We will measure that rather than build the conclusion into the experiment. Theory explains a mechanism; the experiment tests its practical consequences.", "Finish on the question. Do not disclose the measured best context or curve here."),
(15, "The methods come from established n-gram literature and neural language-model research. The examples and presentation sequence are ours. Full references are in the companion theory document.", "Use as an end card; do not read URLs aloud."),
]
assert len(script)==len(notes), (len(script),len(notes))
for note,(seconds,say,cue) in zip(notes,script):
    note.update(seconds=seconds,say=say,cue=cue)

canvas_path=HERE/'episode_02_trigrams.excalidraw'
cv.save(canvas_path)
FONTS[1]="'Virgil',cursive"
font64=base64.b64encode((ROOT/'docs/fonts/Virgil.ttf').read_bytes()).decode()
sections=[]
for i,frame in enumerate(frames.values()):
    kids=[e for e in cv.elements if e.get('frameId')==frame['id']]
    sections.append(f'<section class="slide" id="scene-{i+1}" aria-label="{html.escape(frame["name"],quote=True)}">'+
                    svg_for(frame,kids)+f'<aside class="speaker-notes"><b>Say:</b> {html.escape(notes[i]["say"])}<br><b>Point:</b> {html.escape(notes[i]["cue"])}</aside></section>')
reader='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Episode 02 — Theory presentation</title>
<style>
@font-face{font-family:Virgil;src:url(data:font/ttf;base64,FONT64) format('truetype')}
*{box-sizing:border-box}body{margin:0;background:#eeece7;color:#20242a;font:16px system-ui,sans-serif}
header{padding:12px 20px;background:#20242a;color:#fff;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
header strong{margin-right:auto}button,select,a{font:inherit}button,select{padding:8px 12px;border:1px solid #a6afbd;border-radius:7px;background:white;color:#20242a;cursor:pointer}select{max-width:min(100%,460px)}button:disabled{opacity:.4;cursor:default}
main{max-width:1450px;margin:18px auto;padding:0 18px}.slide{display:none;background:white;border:1px solid #d5d1c8;border-radius:10px;overflow:hidden}.slide.active{display:block}.slide svg{max-height:calc(100vh - 150px)}.speaker-notes{display:none;border-top:1px solid #dedbd5;padding:16px 24px;font-size:17px;line-height:1.5;background:#fff8df}.notes-visible .speaker-notes{display:block}
footer{text-align:center;padding:8px 20px 18px;color:#515963;font-size:13px}footer a{color:#375bb0}.overview{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.overview .slide{display:block;cursor:pointer}.overview svg{max-height:none}
.recording header,.recording footer,.recording .speaker-notes{display:none}.recording{background:white}.recording main{margin:0;padding:0;max-width:none}.recording .slide{border:0;border-radius:0}.recording .slide svg{width:100vw;height:100vh;max-height:none}
@media(max-width:750px){.overview{grid-template-columns:1fr}header{padding:10px}header strong{width:100%}.slide svg{max-height:none}}
@media print{header,footer,.speaker-notes{display:none!important}main{margin:0;padding:0;max-width:none}.slide,.overview .slide{display:block;break-after:page;border:0}.slide svg{max-height:none}.overview{display:block}}
</style></head><body><header><strong>Episode 02 · Trigrams & the sparsity wall</strong><button id="prev" aria-label="Previous scene">←</button><select id="jump" aria-label="Choose scene">OPTIONS</select><button id="next" aria-label="Next scene">→</button><button id="overview" aria-pressed="false">All scenes</button><button id="notes" aria-pressed="false">Speaker notes</button><button id="record">Present</button></header><main>SECTIONS</main><footer>← / → to navigate · Home / End to jump · Present hides controls; Escape restores them.<br><a href="episode_02_trigrams.excalidraw" download>Editable canvas</a> · <a href="../docs/episode-02-theory.pdf">Theory companion PDF</a> · <a href="../docs/episode-02-canvas.pdf">Canvas PDF</a> · <a href="EPISODE_02_CANVAS_GUIDE.md">Presenter guide & sources</a> · Offline SVG approximation of the Excalidraw frames.</footer><script>
const slides=[...document.querySelectorAll('.slide')],main=document.querySelector('main'),jump=document.querySelector('#jump');let index=0,grid=false;
function show(i){index=Math.max(0,Math.min(slides.length-1,Math.trunc(i)));slides.forEach((s,j)=>s.classList.toggle('active',j===index));jump.value=index;document.querySelector('#prev').disabled=index===0;document.querySelector('#next').disabled=index===slides.length-1;history.replaceState(null,'','#scene-'+(index+1));}
function overview(value){grid=value;main.classList.toggle('overview',grid);document.querySelector('#overview').textContent=grid?'One scene':'All scenes';document.querySelector('#overview').setAttribute('aria-pressed',grid);}
document.querySelector('#prev').onclick=()=>show(index-1);document.querySelector('#next').onclick=()=>show(index+1);jump.onchange=()=>show(Number(jump.value));document.querySelector('#overview').onclick=()=>overview(!grid);
document.querySelector('#notes').onclick=()=>{const shown=document.body.classList.toggle('notes-visible');document.querySelector('#notes').setAttribute('aria-pressed',shown);};
document.querySelector('#record').onclick=()=>{overview(false);document.body.classList.add('recording');document.activeElement.blur();};
slides.forEach((s,i)=>s.onclick=()=>{if(grid){overview(false);show(i);window.scrollTo(0,0);}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.body.classList.remove('recording');return;}if(['SELECT','INPUT','TEXTAREA'].includes(document.activeElement.tagName))return;if(['ArrowRight','ArrowLeft','Home','End'].includes(e.key)){e.preventDefault();show(e.key==='Home'?0:e.key==='End'?slides.length-1:index+(e.key==='ArrowRight'?1:-1));}});
const initial=Number(location.hash.replace('#scene-',''));show(Number.isFinite(initial)&&initial>0?initial-1:0);
</script></body></html>'''
options=''.join(f'<option value="{i}">{i+1:02} · {html.escape(n["title"])}</option>' for i,n in enumerate(notes))
reader=reader.replace('FONT64',font64).replace('OPTIONS',options).replace('SECTIONS',''.join(sections))
(HERE/'episode_02_theory.html').write_text(reader)
# Keep earlier links working without preserving outdated study-only content.
(HERE/'episode_02_study.html').write_text(reader)
total_seconds=sum(n['seconds'] for n in notes)
guide=f'''# Episode 02 · Theory presenter guide

Recording sequence: **{len(notes)} frames**, approximately **{round(total_seconds/60)} minutes**
including pauses. Timing is a rehearsal estimate, not a promised video length.
The sources frame can be held silently as an end card.

Open [the theory canvas](episode_02_trigrams.excalidraw) in Excalidraw. Select a
frame and use Shift+2 to zoom to it; advance left to right. For annotations,
save a copy named `episode_02_trigrams.RECORDING.excalidraw` before drawing.

[The offline theory reader](episode_02_theory.html) follows the same sequence.
Speaker notes are hidden by default. “Speaker notes” reveals narration for
rehearsal; “Present” hides controls and notes. Arrow keys advance; Escape exits
presentation mode. The reader is an SVG approximation; Excalidraw supplies the
original editable rendering. The old `episode_02_study.html` link opens this
same updated presentation.

## Audience release copies

[Theory companion guide (PDF)](../docs/episode-02-theory.pdf) ·
[Canvas PDF: all 29 frames](../docs/episode-02-canvas.pdf).
The recorded video is about 43:44; timings below remain rehearsal estimates.

## Recording route

| Frames | Theory section | Purpose |
|---|---|---|
| 01–10 | 1–3 | Context, boundaries, every anna window, counts and normalization |
| 11–15 | 3–4 | Generation, ana failure, missing evidence and smoothing |
| 16–22 | 5 | Evidence splitting beyond trigrams, capacity and sparse storage |
| 23 | 6 | Practical responses and their limits |
| 24–25 | 7 | Shorter histories: backoff and interpolation |
| 26–29 | 8 | Shared representations, recap, coding handoff and references |

The full real-data experiment stays in the coding video: no measured loss curves,
smoothing sweeps, generated batches, or empirical winning context appear here.
Frame 21 contains mathematical capacities only. Keep the phrases “can” and
“may” when discussing generalization; theory does not predict a universal
point at which performance must worsen.

## Three context switches to say out loud

1. Frames 01–16: `anna`, `ava`; four next-token outcomes.
2. Frames 17–18: separate constructed corpus `anna`, `enna`, `inna`, `onna`;
   twenty predictions and six next-token outcomes. The supplied `nnn` query
   is not a claimed generated sample.
3. Frames 19–21: capacity calculations, first with three letters, then 26.
   These are not training datasets or experiment results. Frame 24 explicitly
   returns to the original two-name toy.

Keep the K−1 free-parameter detail in the theory document's appendix. It is
not needed in the spoken path. Frame 25's arithmetic can be shortened aloud;
retain the distinction between fallback and weighted combination.

## Frame-by-frame narration

'''
elapsed=0
for i,n in enumerate(notes):
    guide+=f'### {i+1:02} · {n["title"]}\n\nSuggested start {elapsed//60:02}:{elapsed%60:02} · about {n["seconds"]} seconds\n\n**Say:** {n["say"]}\n\n**Point / cue:** {n["cue"]}\n\n'
    elapsed+=n['seconds']
guide+='''## Evidence and correctness

All hand-worked examples and capacities are checked by
`episodes/02_trigrams/test_lesson_material.py`; the original lab tests remain in
place. See [the correctness review](../EPISODE_02_REVIEW.md) for verification
and limits. No new real-data experiment is required for this theory revision.

Primary and authoritative references: [Jurafsky and Martin, Chapter 3](https://web.stanford.edu/~jurafsky/slp3/3.pdf),
[Chen and Goodman (1996)](https://aclanthology.org/P96-1041/), and
[Bengio et al. (2003)](https://jmlr.org/papers/v3/bengio03a.html).
See [the theory reference](../EPISODE_02_THEORY.md) for equations and source scope.

## Regenerate

From the repository root, run `python3 canvas/build_episode_02.py`.
This overwrites the generated canvas, reader, and this presenter guide. Edit
narration and scene content in the builder before regenerating; keep recording
annotations in a separate copy.
'''
(HERE/'EPISODE_02_CANVAS_GUIDE.md').write_text(guide)
print(f'Built {len(notes)} theory frames; narration estimate {total_seconds/60:.1f} minutes.')
