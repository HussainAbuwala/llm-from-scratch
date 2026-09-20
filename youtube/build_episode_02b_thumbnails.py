#!/usr/bin/env python3
"""Three reproducible diagram thumbnails for Episode 02B; no private photo assets."""
from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'youtube/thumbnails'; OUT.mkdir(exist_ok=True)
W,H=1280,720
NAVY='#0b1831'; CREAM='#fffbe9'; BLUE='#88d0ff'; GREEN='#6de1a0'; PURPLE='#c9b7ff'; RED='#ff8e90'; INK='#182337'
FONT=ROOT/'docs/fonts/Virgil.ttf'
MONO='/System/Library/Fonts/Menlo.ttc'
rng=random.Random(2)

def text(d,xy,s,size,color=CREAM,font=FONT):
    f=ImageFont.truetype(str(font),size)
    box=d.textbbox(xy,s,font=f)
    assert box[2]<=W-25 and box[3]<=H-12,(s,box)
    d.text(xy,s,font=f,fill=color)

def line(d,points,color=BLUE,width=5):
    d.line(points,fill=color,width=width)
    d.line([(x+rng.randint(-2,2),y+rng.randint(-2,2)) for x,y in points],fill=color,width=2)

def arrow(d,x,y,x2,y2,color=BLUE):
    import math
    line(d,[(x,y),(x2,y2)],color)
    ang=math.atan2(y2-y,x2-x)
    for a in [-.5,.5]:line(d,[(x2,y2),(x2-20*math.cos(ang+a),y2-20*math.sin(ang+a))],color)

def card(d,rect,s,color=BLUE,size=55):
    d.rounded_rectangle(rect,16,fill=color)
    f=ImageFont.truetype(str(FONT),size)
    d.text(((rect[0]+rect[2])/2,(rect[1]+rect[3])/2),s,font=f,fill=INK,anchor='mm')

def base():
    im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
    text(d,(54,37),'LLM FROM SCRATCH',25,BLUE,font=MONO)
    text(d,(950,39),'EP 02B',29,BLUE,font=MONO)
    text(d,(54,650),'TRIGRAMS  /  PYTHON',26,BLUE,font=MONO)
    return im,d

def save(im,name):
    p=OUT/f'episode-02b-{name}.jpg';im.save(p,quality=95,subsampling=0);print(p)
    return p

im,d=base()
text(d,(54,155),"LET'S CODE",91)
text(d,(54,278),'A TRIGRAM',96,GREEN)
line(d,[(60,411),(632,404)],BLUE,7)
text(d,(58,465),'More context. Same Python.',32)
d.rounded_rectangle((710,174,1212,490),radius=18,fill='#162841',outline='#42516a',width=3)
text(d,(739,200),'PYTHON',27,BLUE,font=MONO)
for y,s in [(272,'context = ("a", "n")'),(321,'target = "n"'),(370,'counts[context][target] += 1')]:
 text(d,(739,y),s,23,GREEN if y==370 else CREAM,font=MONO)
card(d,(865,544,1150,616),'an -> n',BLUE,39)
a=save(im,'lets-code-trigram')

im,d=base()
text(d,(54,155),'MORE',105)
text(d,(54,267),'CONTEXT',105,GREEN)
text(d,(54,389),'IN PYTHON',79)
line(d,[(60,491),(591,484)],BLUE,7)
card(d,(798,160,1003,264),'n',BLUE,70)
arrow(d,850,288,765,391,PURPLE);arrow(d,950,288,1070,391,GREEN)
card(d,(691,417,889,544),'an',PURPLE,65)
card(d,(976,417,1174,544),'nn',GREEN,65)
text(d,(711,584),'counts -> probabilities',29)
b=save(im,'more-context-python')

im,d=base()
text(d,(54,158),'DOES',107)
text(d,(54,269),'CONTEXT',99,GREEN)
text(d,(54,389),'HELP?',110)
text(d,(60,542),'Build it. Measure it.',33)
# Actual validation-selected loss values from the committed experiment.
import json
r=json.loads((ROOT/'episodes/02_trigrams/outputs/coding_results.json').read_text())
values=[x['validation']['nll'] for x in r['models']]
xs=[766+96*i for i in range(5)]
ys=[500-(v-2.1)/.4*300 for v in values]
line(d,[(727,150),(727,532),(1193,532)],CREAM,3)
line(d,list(zip(xs,ys)),BLUE,7)
for x,y in zip(xs,ys):d.ellipse((x-9,y-9,x+9,y+9),fill=GREEN)
text(d,(748,124),'VALIDATION LOSS',26,BLUE,font=MONO)
for i,x in enumerate(xs):text(d,(x-8,550),str(i+1),24)
text(d,(828,594),'context characters',28)
c=save(im,'does-context-help')

sheet=Image.new('RGB',(960,3*302),'white');sd=ImageDraw.Draw(sheet)
for i,(p,label) in enumerate([(a,"A - Let's code a trigram"),(b,'B - More context in Python'),(c,'C - Does context help?')]):
 sd.text((14,i*302+7),label,font=ImageFont.truetype(MONO,18),fill=INK)
 sheet.paste(Image.open(p).resize((480,270)),(0,i*302+30))
 sheet.paste(Image.open(p).resize((320,180)),(570,i*302+72))
sheet.save(OUT/'episode-02b-options.jpg',quality=94)
