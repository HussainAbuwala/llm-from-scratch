#!/usr/bin/env python3
"""Build Episode 03A's canvas, offline presentation and presenter guide."""
import base64
import html
import json
import math
from pathlib import Path

from excalidraw_kit import (Canvas, text, box, arrow, line, HAND, CODE, BLACK, GRAY,
                           BLUE, VIOLET, RED, BG_BLUE, BG_GREEN, BG_GRAY,
                           BG_RED, BG_VIOLET, BG_YELLOW)
from render_preview import svg_for, FONTS
from episode_03_math import draw_formula

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTENT = ROOT / 'episodes/03_weights'
SCENES = json.loads((CONTENT / 'scenes.json').read_text())


def txt(s, x, y, value, size=32, color=BLACK, mono=False):
    s.add(text(x, y, value, size, CODE if mono else HAND, color))


def panel(s, x, y, w, h, value, bg=BG_BLUE, size=34, mono=False):
    s.add(box(x, y, w, h, value, size, CODE if mono else HAND, bg=bg))


def build():
    cv = Canvas()
    for i, n in enumerate(SCENES):
        s = cv.scene(f'{i+1:02} · {n["title"]}')
        txt(s, 70, 55, n['title'], 46)
        txt(s, 70, 135, n['subtitle'], 27, GRAY)
        kind = n.get('kind', 'steps')
        if kind == 'softmax_explainer':
            for j, value in enumerate(n['items']):
                panel(s, 70, 210+j*170, 745, 150, value,
                      [BG_BLUE, BG_VIOLET, BG_GREEN][j], 28)
            txt(s, 915, 210, 'Vary END’s score only', 31, VIOLET)
            txt(s, 915, 257, 'a, n, v scores stay at 0', 26)
            x0, x1, y0, y1 = 965, 1505, 340, 610
            sx = lambda z: x0+(z+6)/12*(x1-x0)
            sy = lambda p: y1-p*(y1-y0)
            txt(s, 935, 302, 'P(END)', 25)
            for prob, label in [(0, '0%'), (.5, '50%'), (1, '100%')]:
                y = sy(prob)
                s.add(line([(x0,y),(x1,y)], stroke=BG_GRAY, sw=1, roughness=0))
                txt(s, 864, y-16, label, 24, mono=True)
            s.add(line([(x0,y0),(x0,y1),(x1,y1)], stroke=GRAY, sw=1, roughness=0))
            for score in [-6,0,6]:
                x=sx(score)
                s.add(line([(x,y1),(x,y1+6)], stroke=GRAY, sw=1, roughness=0))
                txt(s, x-14, y1+12, str(score), 24, mono=True)
            points=[]
            for j in range(121):
                z=-6+j*.1
                points.append((sx(z),sy(math.exp(z)/(3+math.exp(z)))))
            s.add(line(points, stroke=VIOLET, sw=4, roughness=0))
            # Mark the all-zero starting model: P(END)=1/4.
            x,y=sx(0),sy(.25)
            s.add(box(x-5,y-5,10,10,bg=VIOLET,stroke=VIOLET))
            txt(s, x+18, y+4, '0 gives 25%', 23)
            txt(s, 1080, 662, 'END score (logit)', 27)
            txt(s, 900, 711, 'S-shaped slice; other scores held fixed.', 25)
        elif kind == 'training_compare':
            for col, (title, labels, color) in enumerate([
                ('Count-based bigram', ['Count training transitions', 'Smooth if chosen; normalize rows', 'Evaluate with NLL'], BG_BLUE),
                ('Weight-based bigram', ['Initialize weights', 'Look up rows; softmax; NLL', 'Update from training loss; repeat'], BG_VIOLET)]):
                x = 90+col*760
                txt(s, x+25, 215, title, 35)
                for j, label in enumerate(labels):
                    y = 280+j*130
                    panel(s, x, y, 650, 90, label, color, 29)
                    if j < 2: s.add(arrow(x+325, y+95, x+325, y+122))
            s.add(arrow(1510, 585, 1540, 585))
            s.add(arrow(1540, 585, 1540, 440))
            s.add(arrow(1540, 440, 1510, 440))
            txt(s, 110, 675, 'Validation: choose k', 27)
            txt(s, 870, 675, 'Validation: settings / checkpoint', 27)
            txt(s, 110, 720, 'Today: evaluate the initial weights, then try changes by hand.', 29, VIOLET)
        elif kind == 'all_softmax':
            headers = ['Input', 'Scores', 'Exponentials', 'Row total', 'Probabilities']
            positions = [85, 270, 610, 930, 1150]
            for x, label in zip(positions, headers): txt(s, x, 225, label, 27, VIOLET)
            for j, label in enumerate(['START', 'a', 'n', 'v']):
                y = 295+j*94
                panel(s, 70, y-12, 1460, 76, '', BG_BLUE if j == 1 else BG_GRAY)
                for x, value in zip(positions, [label, '[0,0,0,0]', '[1,1,1,1]', '4', '[¼,¼,¼,¼]']):
                    txt(s, x, y, value, 30, mono=True)
            txt(s, 110, 705, 'Each probability row sums to 1. START is an input; END is an output.', 29)
        elif kind == 'score_name':
            for x, label in [(90,'Step'),(250,'Input row'),(540,'Actual target'),(875,'Probability'),(1190,'Loss = −ln(p)')]:
                txt(s, x, 220, label, 26, VIOLET)
            for j, (context, target) in enumerate(n['transitions']):
                y = 285+j*70
                panel(s, 70, y-10, 1460, 60, '', BG_GREEN if target == 'END' else BG_GRAY)
                for x, value in [(95,str(j+1)),(260,context),(550,target),(920,'1/4'),(1240,'ln 4')]:
                    txt(s, x, y, value, 29, mono=True)
            count = len(n['transitions'])
            panel(s, 100, 675, 1400, 70, f'{n["name"]}: {count} targets; total loss = {count} ln 4', BG_YELLOW, 32)
        elif kind == 'baseline_average':
            panel(s, 100, 225, 1400, 105, 'anna: 5 targets, total 5 ln 4     ava: 4 targets, total 4 ln 4', BG_BLUE, 30)
            panel(s, 100, 365, 1400, 105, 'Combined: 9 targets; total loss = 9 ln 4 ≈ 12.476649 nats', BG_VIOLET, 30)
            s.add(box(100, 505, 1400, 195, bg=BG_GREEN))
            draw_formula(s, 'baseline_average', 100, 607, 1400)
        elif kind == 'chosen_change':
            panel(s, 100, 220, 1400, 90, 'Only the a row changes: [0, 0, 0, ln 2]', BG_VIOLET, 34, True)
            panel(s, 100, 340, 1400, 90, 'After softmax: [1/5, 1/5, 1/5, 2/5]', BG_BLUE, 34, True)
            panel(s, 100, 480, 650, 160, 'Before: all zeros\nTraining NLL: 1.386294', BG_GRAY, 32)
            panel(s, 850, 480, 650, 160, 'After: chosen ln 2\nTraining NLL: 1.331437', BG_GREEN, 32)
            txt(s, 110, 690, 'Same 9 targets: five unchanged; after a, score n, END, v, END.', 29)
        elif kind == 'math_steps':
            for j, name in enumerate(n['formulas']):
                y = 225+j*170
                s.add(box(100, y, 1400, 150, bg=[BG_BLUE, BG_VIOLET, BG_GREEN][j]))
                draw_formula(s, name, 100, y+82, 1400)
            txt(s, 110, 733, n.get('legend', ''), 24, GRAY)
        elif kind == 'row_loss':
            panel(s, 100, 225, 1400, 110, n['items'][0], BG_BLUE, 34, True)
            panel(s, 100, 370, 1400, 110, n['items'][1], BG_VIOLET, 34, True)
            s.add(box(100, 515, 1400, 190, bg=BG_GREEN))
            draw_formula(s, 'row_mean', 100, 610, 1400)
        elif kind == 'matrix_multiply':
            txt(s, 95, 210, 'x: current input a', 29, BLUE)
            panel(s, 80, 280, 340, 85, '[0, 1, 0, 0]', BG_BLUE, 34, True)
            txt(s, 450, 298, '×', 44)
            txt(s, 580, 190, 'W: our original weights', 29, VIOLET)
            s.table(540, 240, ['a', 'n', 'v', 'END'], ['START', 'a', 'n', 'v'],
                    n['cells'], cw=125, ch=64, size=27, hi_row=1)
            txt(s, 95, 420, '1 × 4 input', 27)
            txt(s, 95, 465, '4 × 4 weights', 27)
            txt(s, 95, 510, '1 × 4 result', 27)
            txt(s, 1200, 260, 'One column', 27, VIOLET)
            txt(s, 1200, 310, 'per output', 27, VIOLET)
            txt(s, 110, 580, 'a: 0×0 + 1×0 + 0×0 + 0×0 = 0', 27, mono=True)
            txt(s, 835, 580, 'n: 0×0 + 1×0 + 0×0 + 0×0 = 0', 27, mono=True)
            txt(s, 110, 630, 'v: 0×0 + 1×0 + 0×0 + 0×0 = 0', 27, mono=True)
            txt(s, 835, 630, 'END: 0×0 + 1×ln 2 + 0×0 + 0×0 = ln 2', 27, mono=True)
            panel(s, 100, 695, 1400, 55, 'xW = [0, 0, 0, ln 2] = the a row', BG_GREEN, 31, True)
        elif kind == 'table':
            s.table(170, 235, ['a', 'n', 'v', 'END'], ['START', 'a', 'n', 'v'],
                    n['cells'], cw=230, ch=86, size=32, hi_row=1)
            txt(s, 170, 690, n['caption'], 28, VIOLET)
        elif kind == 'flow':
            colors = [BG_BLUE, BG_VIOLET, BG_GREEN]
            for j, value in enumerate(n['items']):
                panel(s, 80 + j*515, 280, 410, 195, value, colors[j], 35)
                if j < 2:
                    s.add(arrow(505+j*515, 377, 572+j*515, 377))
            txt(s, 100, 580, n['caption'], 33)
        elif kind == 'compare':
            for j, value in enumerate(n['items']):
                panel(s, 80+j*760, 265, 680, 305, value,
                      BG_BLUE if j == 0 else n.get('color', BG_GREEN), 34,
                      n.get('mono', False))
            txt(s, 100, 640, n['caption'], 30)
        elif kind == 'bars':
            for j, (label, value) in enumerate(zip(['a','n','v','END'], n['values'])):
                x = 150+j*345
                h = value*650
                panel(s, x, 650-h, 210, h, '', BG_GREEN if j==3 else BG_BLUE)
                txt(s, x+20, 650-h-60, f'{value:.2f}', 34, mono=True)
                txt(s, x+60, 675, label, 31)
            txt(s, 100, 220, n['caption'], 32, VIOLET)
        else:
            for j, value in enumerate(n['items']):
                panel(s, 100, 235+j*155, 1400, 120, value,
                      [BG_BLUE, BG_VIOLET, BG_GREEN][j], 34, n.get('mono', False))
        panel(s, 70, 770, 1460, 65, n['takeaway'], BG_YELLOW, 29)
        txt(s, 70, 855, 'Building an LLM from scratch  ·  Episode 03A  ·  From counts to weights', 21, GRAY)
        txt(s, 1450, 855, f'{i+1:02}', 22, GRAY)

    frames = [e for e in cv.elements if e['type'] == 'frame']
    by_id = {e['id']: e for e in frames}
    for e in cv.elements:
        if e['type'] == 'frame' or e.get('containerId'):
            continue
        f = by_id[e['frameId']]
        x, y = e['x']-f['x'], e['y']-f['y']
        assert 0 <= x and 0 <= y and x+e['width'] <= 1600 and y+e['height'] <= 900, (f['name'], e)
    cv.save(HERE / 'episode_03_weights.excalidraw')
    FONTS[1] = "'Virgil',cursive"
    sections = []
    for i, (frame, n) in enumerate(zip(frames, SCENES)):
        kids = [e for e in cv.elements if e.get('frameId') == frame['id']]
        notes = html.escape(n['say']) + '<p><b>Cue:</b> ' + html.escape(n['cue']) + '</p>'
        sections.append(f'<section class="slide" id="scene-{i+1}" aria-label="{html.escape(n["title"])}">'
                        + svg_for(frame, kids) + f'<aside>{notes}</aside></section>')
    options = ''.join(f'<option value="{i}">{i+1:02} · {html.escape(n["title"])}</option>'
                      for i, n in enumerate(SCENES))
    template = (CONTENT / 'reader_template.html').read_text()
    font = base64.b64encode((ROOT/'docs/fonts/Virgil.ttf').read_bytes()).decode()
    reader = template.replace('FONT64', font).replace('OPTIONS', options).replace('SECTIONS', ''.join(sections))
    (HERE / 'episode_03_theory.html').write_text(reader)
    words = sum(len(n['say'].split()) for n in SCENES)
    seconds = sum(n['seconds'] for n in SCENES)
    guide = f'''# Episode 03A · Presenter guide

{len(frames)} frames · {words} scripted words · {seconds//60} minutes of rehearsal allocations including pointing, arithmetic and pauses.
These are preparation timings, not final chapters or a runtime cap. Expand the worked
steps naturally; do not rush the softmax motivation or the four-target loss.

Read [the theory](../../EPISODE_03_THEORY.md) first. Open
[the presentation](../../canvas/episode_03_theory.html) for rehearsal.
Arrow keys move between frames; Speaker notes reveals this script; Present
hides controls and notes; Escape restores controls. Save an annotation copy
of the Excalidraw canvas before drawing on it.

## Recording blocks

1. Frames 1–6: task, count-versus-weight workflow, initial table, lookup and softmax motivation.
2. Frames 7–11: all-row softmax, every target in both names, and the overall average.
3. Frames 12–16: chosen ln 2 improvement, ln 100 overshoot, update loop and numerical stability.
4. Frames 17–20: model limits, generation, understanding checks and the next lesson.

Frames 4–11 evaluate the all-zero initial weights; no update occurs during that
walkthrough. Frames 12–13 are hand-set adjustments, not optimizer output.
Every reported full training NLL uses the same 9 targets from anna/ava, including
END. The gradient rule for choosing updates remains Episode 04.

One-hot notation, matrix multiplication, and constructing weights from smoothed
counts are in [optional notes](OPTIONAL_MATH.md), outside the main recording route.

'''
    elapsed = 0
    for i, n in enumerate(SCENES):
        guide += (f'## {i+1:02} · {n["title"]}\n\nRehearsal start {elapsed//60}:{elapsed%60:02} · '
                  f'{n["seconds"]} seconds\n\n{n["say"]}\n\n**Visual cue:** {n["cue"]}\n\n'
                  f'**Basis:** {n["source"]}\n\n')
        elapsed += n['seconds']
    guide += '''## Rehearsal checkpoints

Can you select the a row without saying “the computer understands a”? Can you
explain why zero logits are uniform? Can you score n as well as END after the
same input a? Can you distinguish a hand-set weight from one fitted by an
optimizer? Use the [exercises](EXERCISES.md) and [answers](ANSWERS.md).

The theory reference contains sources and optional details on row-optimum
limits, independent parameters, batches, and the exact held-out ana path.
The canvas is the spoken route, not the whole reference.
'''
    (CONTENT / 'PRESENTER_GUIDE.md').write_text(guide)
    print(f'{len(frames)} frames; {words} words; {seconds} rehearsal seconds')


if __name__ == '__main__':
    build()
