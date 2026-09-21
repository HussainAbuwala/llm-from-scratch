#!/usr/bin/env python3
"""The selected diagram thumbnail for Episode 02B; no private photo assets."""
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
text(d,(54,133),"LET'S CODE",83)
text(d,(54,237),'A',88)
text(d,(140,237),'TRIGRAM',88,GREEN)
text(d,(54,341),'LANGUAGE',88)
text(d,(54,445),'MODEL',88)
line(d,[(60,548),(632,541)],BLUE,7)
# Notebook-inspired chrome and a selected code cell.
d.rounded_rectangle((686,154,1234,510),radius=18,fill='#ffffff',outline=BLUE,width=4)
d.rounded_rectangle((708,175,748,215),radius=8,fill='#f37726')
text(d,(719,179),'J',28,'#ffffff',font=MONO)
text(d,(760,183),'episode_02.ipynb',23,INK,font=MONO)
d.line((704,232,1215,232),fill='#d8dce3',width=2)
text(d,(718,245),'Run  |  Code',20,'#596579',font=MONO)
logo=Image.open(ROOT/'youtube/brand-assets/python-logo.png').convert('RGBA')
# Extract the official two-snake symbol, without changing its colors or proportions.
logo=logo.crop((25,9,69,53)).resize((66,66),Image.Resampling.LANCZOS)
im.paste(logo,(1142,167),logo)
d.rectangle((770,293,1214,457),fill='#f5f7fa',outline='#d6dce5',width=2)
d.rectangle((762,293,768,457),fill='#1971c2')
text(d,(700,309),'[1]:',20,'#1971c2',font=MONO)
for y,pieces in [
 (310,[('context',INK),(' = ', '#596579'),('("a", "n")','#a32638')]),
 (355,[('target',INK),(' = ', '#596579'),('"n"','#a32638')]),
 (400,[('counts[context][target]',INK),(' += ', '#7c3aed'),('1','#16713c')])]:
 x=785
 for value,color in pieces:
  text(d,(x,y),value,20,color,font=MONO)
  x+=d.textlength(value,font=ImageFont.truetype(MONO,20))
card(d,(865,544,1150,616),'an -> n',BLUE,39)
save(im,'lets-code-trigram')
