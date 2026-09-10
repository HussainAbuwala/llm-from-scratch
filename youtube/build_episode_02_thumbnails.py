#!/usr/bin/env python3
"""Three reproducible diagram thumbnails for Episode 02A; no private photo assets."""
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
    text(d,(950,39),'EP 02A',29,BLUE,font=MONO)
    text(d,(54,650),'TRIGRAMS  /  THEORY',26,BLUE,font=MONO)
    return im,d

def save(im,name):
    p=OUT/f'episode-02a-{name}.jpg';im.save(p,quality=95,subsampling=0);print(p)
    return p

im,d=base()
text(d,(54,155),'MORE',113)
text(d,(54,272),'CONTEXT,',105)
text(d,(54,390),'BETTER?',110,GREEN)
line(d,[(60,519),(550,510)],BLUE,7)
card(d,(728,142,907,246),'n',BLUE)
arrow(d,817,268,817,329)
card(d,(690,350,822,451),'a',PURPLE)
card(d,(849,350,981,451),'n',BLUE)
arrow(d,1001,403,1060,403)
text(d,(1090,336),'?',115,RED)
text(d,(728,502),'more detail',33)
text(d,(728,549),'enough evidence?',33,RED)
a=save(im,'more-context')

im,d=base()
text(d,(54,153),'WHERE',110)
text(d,(54,274),'COUNTS',110,GREEN)
text(d,(54,395),'RUN OUT',99)
line(d,[(60,519),(570,509)],BLUE,7)
# A deliberately schematic sparse table, not measured data.
for row in range(7):
 for col in range(9):
  x=716+col*51;y=183+row*51
  filled=(row,col) in {(0,0),(0,3),(1,2),(3,5),(5,1),(6,7)}
  d.rounded_rectangle((x,y,x+41,y+41),6,fill=BLUE if filled else NAVY,outline=BLUE if filled else '#42516a',width=2)
text(d,(730,565),'same data. more rows.',31,RED)
b=save(im,'counts-run-out')

im,d=base()
text(d,(54,147),'ONE MORE',105)
text(d,(54,263),'LETTER',122,GREEN)
line(d,[(60,407),(620,394)],BLUE,7)
text(d,(57,459),'Changes the question.',37)
card(d,(791,150,995,262),'n',BLUE,75)
arrow(d,841,288,760,380,PURPLE)
arrow(d,945,288,1064,380,GREEN)
card(d,(682,408,877,534),'an',PURPLE,66)
card(d,(965,408,1160,534),'nn',GREEN,66)
text(d,(707,561),'separate patterns',31)
c=save(im,'one-more-letter')

sheet=Image.new('RGB',(960,3*302),'#ffffff');sd=ImageDraw.Draw(sheet)
for i,(p,label) in enumerate([(a,'A - More context, better?'),(b,'B - Where counts run out'),(c,'C - One more letter')]):
 sd.text((14,i*302+7),label,font=ImageFont.truetype(MONO,18),fill=INK)
 sheet.paste(Image.open(p).resize((480,270)),(0,i*302+30))
 # Feed-size comparison makes readability easy to assess.
 sheet.paste(Image.open(p).resize((320,180)),(570,i*302+72))
sheet.save(OUT/'episode-02a-options.jpg',quality=94)
