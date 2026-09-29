"""Three Episode 03A diagram thumbnails in the series Learn palette."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT/'youtube/thumbnails'
FONT = ROOT/'docs/fonts/Virgil.ttf'
BG, INK, PLUM, ORANGE = '#FFF0D5', '#34233F', '#713C8C', '#C95724'


def text(d, x, y, label, size, color=INK):
    f = ImageFont.truetype(str(FONT), size)
    bounds = d.textbbox((x, y), label, font=f)
    assert bounds[2] < 1250 and bounds[3] < 700, (label, bounds)
    d.text((x, y), label, font=f, fill=color)


def base(title):
    im = Image.new('RGB', (1280, 720), BG)
    d = ImageDraw.Draw(im)
    text(d, 55, 30, 'LLM FROM SCRATCH', 28, PLUM)
    text(d, 1030, 30, 'EP 03A', 28, PLUM)
    text(d, 55, 110, title, 92)
    return im, d


def arrow(d, x, y, end):
    d.line([(x,y),(end,y)], fill=ORANGE, width=8)
    d.line([(end-22,y-20),(end,y),(end-22,y+20)], fill=ORANGE, width=8)


def save(im, name):
    path = OUT/f'episode-03a-{name}.jpg'
    im.save(path, quality=95, subsampling=0)
    assert path.stat().st_size < 2_000_000
    return path


im,d=base('TURN THE WEIGHTS')
for j,(label,knob) in enumerate([('a',280),('n',370),('v',320),('END',540)]):
    y=300+j*80
    text(d,65,y-17,label,34)
    d.line([(180,y),(610,y)],fill=PLUM,width=6)
    d.ellipse((knob-16,y-16,knob+16,y+16),fill=ORANGE)
arrow(d,670,420,810)
text(d,860,280,'LOSS',45,PLUM)
text(d,850,360,'1.386',62)
text(d,850,450,'1.331',62,ORANGE)
text(d,65,640,'ONE CHANGE. MEASURE THE EFFECT.',31,PLUM)
a=save(im,'turn-the-weights')

im,d=base('SCORES TO CHANCES')
for j,(label,h) in enumerate([('a',95),('n',95),('v',95),('END',190)]):
    x=750+j*110
    d.rounded_rectangle((x,570-h,x+72,570),radius=9,fill=ORANGE if j==3 else PLUM)
    text(d,x,590,label,26)
text(d,65,300,'0   0   0   ln 2',43)
text(d,100,400,'SOFTMAX',55,PLUM)
arrow(d,410,440,670)
text(d,750,275,'20%  20%  20%  40%',29,PLUM)
b=save(im,'scores-to-chances')

im,d=base('TOO CONFIDENT?')
text(d,65,265,'Boost END after a',45,PLUM)
for x,label,loss,col in [(80,'ZERO','1.386',PLUM),(475,'ln 2','1.331',PLUM),(865,'ln 100','1.807',ORANGE)]:
    d.rounded_rectangle((x,355,x+320,585),radius=20,outline=col,width=5)
    text(d,x+42,380,label,47,col)
    text(d,x+42,475,loss,62,col)
text(d,65,640,'AVERAGE LOSS ACROSS ALL TARGETS',32,PLUM)
c=save(im,'too-confident')
sheet=Image.new('RGB',(960,870),'#EEE8DF')
for i,p in enumerate([a,b,c]):
    thumb=Image.open(p);thumb.thumbnail((480,270));sheet.paste(thumb,(450,i*290))
    ImageDraw.Draw(sheet).text((25,i*290+115),['A: Turn the weights','B: Scores to chances','C: Too confident?'][i],font=ImageFont.truetype(str(FONT),27),fill=INK)
sheet.save(OUT/'episode-03a-options.jpg',quality=95)
