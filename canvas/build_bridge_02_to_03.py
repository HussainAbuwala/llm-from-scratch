#!/usr/bin/env python3
"""Build only the bridge canvas, offline reader and presenter script."""
import base64
import html
import json
from pathlib import Path
from excalidraw_kit import *
from render_preview import svg_for, FONTS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTENT = ROOT / 'episodes/02_bridge'
notes = json.loads((CONTENT / 'scenes.json').read_text())
cv = Canvas()

def txt(s, x, y, value, size=32, color=BLACK, mono=False):
    s.add(text(x, y, value, size, CODE if mono else HAND, color))

def scene(i, subtitle):
    s = cv.scene(f'{i+1:02} · {notes[i]["title"]}')
    txt(s, 70, 55, notes[i]['title'], 46)
    txt(s, 70, 130, subtitle, 27, GRAY)
    txt(s, 70, 845, 'Building an LLM from scratch  ·  Between Episodes 02 and 03', 21, GRAY)
    txt(s, 1450, 845, f'{i+1:02}', 22, GRAY)
    return s

def takeaway(s, value):
    s.add(box(70, 735, 1460, 80, value, 31, HAND, bg=BG_YELLOW))

def node(s, x, y, w, label, color=BG_BLUE, h=105, size=32):
    s.add(box(x, y, w, h, label, size, HAND, bg=color))

s = scene(0, 'A short pause to connect the steps')
for x,label,color in [(80,'COUNT',BG_GREEN),(580,'LEARN',BG_VIOLET),(1080,'ATTEND',BG_BLUE)]:
    node(s,x,300,400,label,color,h=145,size=43)
s.add(arrow(500,375,560,375));s.add(arrow(1000,375,1060,375))
txt(s,135,490,'We are here',36,GREEN)
txt(s,600,555,'Destination: a small Transformer\nthat we train to generate text.',34)
takeaway(s,'Each stage gives us a reason to learn the next one.')

s = scene(1, 'Bigram: 1 context character    ·    Trigram: 2 context characters')
for x,label,color in [(80,'Context',BG_BLUE),(580,'Probabilities',BG_VIOLET),(1080,'Next character',BG_GREEN)]:
    node(s,x,270,400,label,color,h=130)
s.add(arrow(500,335,560,335));s.add(arrow(1000,335,1060,335))
txt(s,90,435,'Count what followed',29,BLUE)
txt(s,600,435,'Normalize the row',29,VIOLET)
txt(s,1100,435,'Sample one token',29,GREEN)
s.add(arrow(1275,505,1275,600));s.add(arrow(1275,600,275,600));s.add(arrow(275,600,275,505))
txt(s,480,640,'Update the context and repeat',32)
takeaway(s,'We can generate names—and measure predictions on held-out names.')

s = scene(2, 'Our add-k experiment · same names dataset and validation split')
# Real validation curve, selected smoothing per context; explicit truncated y axis.
xs = [230,480,730,980,1230]
values = [2.456622,2.233214,2.126903,2.196154,2.386382]
for value in [2.1,2.3,2.5]:
    y = 595-(value-2.1)/.4*310
    s.add(line([(190,y),(1380,y)],stroke=BG_GRAY))
    txt(s,95,y-18,f'{value:.1f}',25,GRAY,True)
txt(s,190,215,'Validation NLL ↓   (nats per prediction)',28)
ys = [595-(v-2.1)/.4*310 for v in values]
for i in range(4): s.add(line([(xs[i],ys[i]),(xs[i+1],ys[i+1])],stroke=VIOLET,sw=4))
for i,(x,y,v) in enumerate(zip(xs,ys,values)):
    s.add(box(x-8,y-8,16,16,bg=VIOLET,stroke=VIOLET))
    txt(s,x-55,y-47,f'{v:.3f}',27,VIOLET,True)
    txt(s,x-8,620,str(i+1),27,BLACK,True)
txt(s,485,666,'Context characters (trigram = 2)',28)
takeaway(s,'More context helped at first. Sparse evidence limited this experiment.')
txt(s,80,190,'k selected per context: 0.3 / 0.3 / 0.1 / 0.1 / 0.1 · 21,141 targets incl. END',21,GRAY)

s = scene(3, 'Imagined word example · separate from our character-level names experiment')
node(s,90,255,580,'a cup of\nnext: tea',BG_BLUE,h=145,size=40)
node(s,930,255,580,'a mug of\nnext: ?',BG_VIOLET,h=145,size=40)
txt(s,130,445,'Often observed',35,BLUE)
txt(s,970,445,'Rare context',35,VIOLET)
txt(s,155,575,'Separate rows do not learn that cup and mug behave similarly.',35)
txt(s,155,635,'Even if that relationship appears elsewhere in the training data.',29,GRAY)
takeaway(s,'The limitation: needing evidence for each exact situation separately.')

s = scene(4, 'New exact toy: a cup of tea / a mug of coffee / a bag of rice · final-word transitions only')
headers=['3-word history','2-word history','1-word history']
for x,label in zip([90,600,1110],headers): txt(s,x,220,label,32,VIOLET)
rows=[('a cup of : tea +1','cup of : tea +1','of : tea +1'),
      ('a mug of : coffee +1','mug of : coffee +1','of : coffee +1'),
      ('a bag of : rice +1','bag of : rice +1','of : rice +1')]
for r,row in enumerate(rows):
    for c,value in enumerate(row): node(s,80+c*510,290+r*105,450,value,[BG_VIOLET,BG_BLUE,BG_GREEN][c],h=80,size=28)
node(s,250,630,1100,'The existing of row: tea 1 / coffee 1 / rice 1',BG_GREEN,h=70,size=30)
takeaway(s,'Rows coexist. Each model counts the same observations at its own context length.')

s = scene(5, 'Prediction time · simple missing-row fallback · the training rows stay unchanged')
txt(s,90,205,'1. a mug of: use the exact row',29,VIOLET)
node(s,90,250,430,'a mug of: EXISTS',BG_VIOLET,h=75,size=29)
s.add(arrow(540,288,630,288))
node(s,660,250,850,'STOP. P(coffee) = 1',BG_GREEN,h=75,size=30)
txt(s,90,355,'2. the mug of: drop the, keep mug',29,VIOLET)
node(s,90,400,430,'the mug of: ABSENT',BG_RED,h=75,size=29)
s.add(arrow(540,438,630,438))
node(s,660,400,380,'mug of: EXISTS',BG_BLUE,h=75,size=28)
s.add(arrow(1060,438,1140,438))
node(s,1170,400,340,'STOP. P(coffee) = 1',BG_GREEN,h=75,size=24)
txt(s,90,500,'3. a glass of: both longer rows are absent',29,VIOLET)
node(s,90,545,430,'a glass of: ABSENT',BG_RED,h=95,size=29)
s.add(arrow(540,593,630,593))
node(s,660,545,380,'glass of: ABSENT',BG_RED,h=95,size=28)
s.add(arrow(1060,593,1140,593))
node(s,1170,530,340,'of: EXISTS. STOP.\ntea / coffee / rice\n1/3 each',BG_GREEN,h=125,size=25)
txt(s,90,680,'Query 3 gains pooled evidence, but its prediction no longer uses glass.',30,RED)
takeaway(s,'Backoff selects an existing row. It does not move observations or create counts.')

s = scene(6, 'Query: a mug of · same toy data · equal mixture weights chosen for illustration')
for x,label,body,color in [(80,'a mug of','coffee: 1',BG_VIOLET),
                         (600,'mug of','coffee: 1',BG_BLUE),
                         (1120,'of','tea / coffee / rice\n1/3 each',BG_GREEN)]:
    node(s,x,225,400,label+'\n'+body,color,h=160,size=30)
    txt(s,x+115,410,'weight 1/3',28)
    s.add(arrow(x+200,460,800,515))
node(s,245,545,1110,'Mixture: tea 1/9 / coffee 7/9 / rice 1/9',BG_YELLOW,h=90,size=34)
txt(s,90,650,'Tradeoff: trust a rare specific row, or give more influence to a broad row?',30,RED)
takeaway(s,'Mixing rows does not itself learn which words play similar roles.')

s = scene(7, 'Word-token illustration · query: a mug of')
for x,label,color in [(80,'a mug of',BG_VIOLET),(600,'mug of',BG_BLUE),(1120,'of',BG_GREEN)]:
    node(s,x,225,400,label,color,h=110,size=38)
    s.add(arrow(x+200,355,800,435))
node(s,540,465,520,'Our mixture',BG_YELLOW,h=100,size=36)
node(s,85,580,410,'a cup of',BG_GRAY,h=95,size=36)
txt(s,545,600,'Exists, but is not directly consulted.',32)
takeaway(s,'The rule chooses shorter endings of the query, not related words.')

s = scene(8, 'Same toy observations · the longer rows still exist')
node(s,80,245,520,'cup of: tea +1',BG_BLUE,h=110,size=36)
node(s,80,445,520,'bag of: rice +1',BG_GRAY,h=110,size=36)
s.add(arrow(625,300,865,350));s.add(arrow(625,500,865,440))
node(s,900,255,610,'The of row\ntea: 1\ncoffee: 1\nrice: 1',BG_GREEN,h=330,size=34)
txt(s,105,640,'This pooled row does not record which container supplied each count.',32)
takeaway(s,'It cannot favor tea because that observation came from a cup.')

s = scene(9, 'A capability to learn from a larger training dataset · not a result from our tiny toy')
node(s,370,205,860,'Predict after: a mug of ...',BG_VIOLET,h=95,size=39)
txt(s,150,345,'Illustrative examples that could appear in training:',29,GRAY)
node(s,120,395,650,'drink from a cup\npour tea into a cup',BG_BLUE,h=125,size=32)
node(s,830,395,650,'drink from a mug\npour tea into a mug',BG_BLUE,h=125,size=32)
s.add(arrow(445,540,445,580));s.add(arrow(1155,540,1155,580))
node(s,120,600,1360,'Can patterns learned from these examples help with our mug query?',BG_GREEN,h=90,size=31)
takeaway(s,'Use related experience, while still letting mug influence the prediction.')

s = scene(10, 'To train a more flexible prediction rule, we need numbers we can adjust.')
for x,label in [(90,'PIECE'),(470,'WHAT IT ENABLES'),(1050,'WHERE WE LEARN IT')]:
    txt(s,x,245,label,26,VIOLET)
rows=[('Weights','Adjustable numbers that\nchange our predictions.','EP 03 · Bigram\nWeights + softmax',BG_VIOLET),
      ('A training method','Decide how to change weights\nto improve predictions.','EP 04–06 · Bigram training\nGradients, autograd, PyTorch',BG_BLUE),
      ('A structure that\nreuses weights','An update from one example\ncan affect other inputs too.','EP 07 · Embeddings\n+ a small network (MLP)',BG_GREEN)]
for i,(piece,purpose,episode,color) in enumerate(rows):
    y=305+i*135
    node(s,80,y,340,piece,color,h=112,size=29)
    txt(s,470,y+20,purpose,29)
    txt(s,1050,y+20,episode,27)
takeaway(s,'Next: learn weights on familiar character bigrams. Useful sharing comes later.')

frames=[e for e in cv.elements if e['type']=='frame']
by_id={e['id']:e for e in frames}
for e in cv.elements:
    if e['type']=='frame' or e.get('containerId'): continue
    f=by_id[e['frameId']]
    x,y=e['x']-f['x'],e['y']-f['y']
    if e['type'] in ('arrow', 'line'):
        assert all(0<=x+px<=1600 and 0<=y+py<=900 for px,py in e['points'])
    else:
        assert x>=0 and y>=0 and x+e['width']<=1600 and y+e['height']<=900, (f['name'],e.get('text'))
cv.save(HERE/'bridge_02_to_03.excalidraw')
FONTS[1]="'Virgil',cursive"
sections=[]
for i,frame in enumerate(frames):
    kids=[e for e in cv.elements if e.get('frameId')==frame['id']]
    n=notes[i]
    sections.append(f'<section class="slide" id="scene-{i+1}" aria-label="{html.escape(frame["name"],quote=True)}">'+svg_for(frame,kids)+f'<aside class="speaker-notes"><b>Say:</b> {html.escape(n["say"])}<br><b>Cue:</b> {html.escape(n["cue"])}<br><b>Source:</b> {html.escape(n["source"])}</aside></section>')
options=''.join(f'<option value="{i}">{i+1:02} · {html.escape(n["title"])}</option>' for i,n in enumerate(notes))

READER_TEMPLATE = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bridge — Counting to learning</title>\n<style>\n@font-face{font-family:Virgil;src:url(data:font/ttf;base64,FONT64) format(\'truetype\')}\n*{box-sizing:border-box}body{margin:0;background:#eeece7;color:#20242a;font:16px system-ui,sans-serif}\nheader{padding:12px 20px;background:#20242a;color:#fff;display:flex;align-items:center;gap:12px;flex-wrap:wrap}\nheader strong{margin-right:auto}button,select,a{font:inherit}button,select{padding:8px 12px;border:1px solid #a6afbd;border-radius:7px;background:white;color:#20242a;cursor:pointer}select{max-width:min(100%,460px)}button:disabled{opacity:.4;cursor:default}\nmain{max-width:1450px;margin:18px auto;padding:0 18px}.slide{display:none;background:white;border:1px solid #d5d1c8;border-radius:10px;overflow:hidden}.slide.active{display:block}.slide svg{max-height:calc(100vh - 150px)}.speaker-notes{display:none;border-top:1px solid #dedbd5;padding:16px 24px;font-size:17px;line-height:1.5;background:#fff8df}.notes-visible .speaker-notes{display:block}\nfooter{text-align:center;padding:8px 20px 18px;color:#515963;font-size:13px}footer a{color:#375bb0}.overview{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.overview .slide{display:block;cursor:pointer}.overview svg{max-height:none}\n.recording header,.recording footer,.recording .speaker-notes{display:none}.recording{background:white}.recording main{margin:0;padding:0;max-width:none}.recording .slide{border:0;border-radius:0}.recording .slide svg{width:100vw;height:100vh;max-height:none}\n@media(max-width:750px){.overview{grid-template-columns:1fr}header{padding:10px}header strong{width:100%}.slide svg{max-height:none}}\n@media print{header,footer,.speaker-notes{display:none!important}main{margin:0;padding:0;max-width:none}.slide,.overview .slide{display:block;break-after:page;border:0}.slide svg{max-height:none}.overview{display:block}}\n</style></head><body><header><strong>Bridge · Counting to learning</strong><button id="prev" aria-label="Previous scene">←</button><select id="jump" aria-label="Choose scene">OPTIONS</select><button id="next" aria-label="Next scene">→</button><button id="overview" aria-pressed="false">All scenes</button><button id="notes" aria-pressed="false">Speaker notes</button><button id="record">Present</button></header><main>SECTIONS</main><footer>← / → to navigate · Home / End to jump · Present hides controls; Escape restores them.<br><a href="bridge_02_to_03.excalidraw" download>Editable canvas</a> · <a href="../episodes/02_bridge/PRESENTER_GUIDE.md">Script</a> · <a href="../episodes/02_bridge/THEORY.md">Learning notes & sources</a> · Offline SVG approximation.</footer><script>\nconst slides=[...document.querySelectorAll(\'.slide\')],main=document.querySelector(\'main\'),jump=document.querySelector(\'#jump\');let index=0,grid=false;\nfunction show(i){index=Math.max(0,Math.min(slides.length-1,Math.trunc(i)));slides.forEach((s,j)=>s.classList.toggle(\'active\',j===index));jump.value=index;document.querySelector(\'#prev\').disabled=index===0;document.querySelector(\'#next\').disabled=index===slides.length-1;history.replaceState(null,\'\',\'#scene-\'+(index+1));}\nfunction overview(value){grid=value;main.classList.toggle(\'overview\',grid);document.querySelector(\'#overview\').textContent=grid?\'One scene\':\'All scenes\';document.querySelector(\'#overview\').setAttribute(\'aria-pressed\',grid);}\ndocument.querySelector(\'#prev\').onclick=()=>show(index-1);document.querySelector(\'#next\').onclick=()=>show(index+1);jump.onchange=()=>show(Number(jump.value));document.querySelector(\'#overview\').onclick=()=>overview(!grid);\ndocument.querySelector(\'#notes\').onclick=()=>{const shown=document.body.classList.toggle(\'notes-visible\');document.querySelector(\'#notes\').setAttribute(\'aria-pressed\',shown);};\ndocument.querySelector(\'#record\').onclick=()=>{overview(false);document.body.classList.add(\'recording\');document.activeElement.blur();};\nslides.forEach((s,i)=>s.onclick=()=>{if(grid){overview(false);show(i);window.scrollTo(0,0);}});\ndocument.addEventListener(\'keydown\',e=>{if(e.key===\'Escape\'){document.body.classList.remove(\'recording\');return;}if([\'SELECT\',\'INPUT\',\'TEXTAREA\'].includes(document.activeElement.tagName))return;if([\'ArrowRight\',\'ArrowLeft\',\'Home\',\'End\'].includes(e.key)){e.preventDefault();show(e.key===\'Home\'?0:e.key===\'End\'?slides.length-1:index+(e.key===\'ArrowRight\'?1:-1));}});\nconst initial=Number(location.hash.replace(\'#scene-\',\'\'));show(Number.isFinite(initial)&&initial>0?initial-1:0);\n</script></body></html>'
font64=base64.b64encode((ROOT/'docs/fonts/Virgil.ttf').read_bytes()).decode()
reader=READER_TEMPLATE.replace('FONT64',font64).replace('OPTIONS',options).replace('SECTIONS',''.join(sections))
(HERE/'bridge_02_to_03.html').write_text(reader)
words=sum(len(n['say'].split()) for n in notes)
guide=f'''# Bridge presenter script

{len(frames)} frames · {words} spoken words · clarity takes priority over runtime.
Timings below are rehearsal allocations, not recorded chapter timestamps.

Use [the presentation](../../canvas/bridge_02_to_03.html). Start on camera, then
use the existing canvas style. Read [the learning notes](THEORY.md) first.
Frames 4–10 use word-level illustrations, including an exact three-sentence toy; distinguish them from
our measured character-level experiment. Avoid introducing softmax arithmetic.
Pause at each distinction. The earlier 3–5 minute cap has been removed.
The allocations are rehearsal aids, not deadlines; let the examples make sense.

'''
elapsed=0
for i,n in enumerate(notes):
    guide+=f'## {i+1:02} · {n["title"]}\n\nRehearsal start {elapsed//60}:{elapsed%60:02} · {n["seconds"]} seconds\n\n{n["say"]}\n\n**Visual cue:** {n["cue"]}\n\n**Source:** {n["source"]}\n\n'
    elapsed+=n['seconds']
guide+='''## Before recording

Check you can explain: backoff pools suffix evidence; interpolation mixes
predictions; learned representations offer a different kind of sharing; a
bigram weight table alone does not yet do that. The experiment compared add-k
models, not all count-based techniques. Keep the claims at that scope.

For the next episode's short independent opening, see [README](README.md).
'''
(CONTENT/'PRESENTER_GUIDE.md').write_text(guide)
print(f'{len(frames)} frames; {words} spoken words; {elapsed} seconds allocated')
