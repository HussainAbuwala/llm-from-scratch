"""Episode 03B alternatives using the established code-drawn Learn identity."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'youtube/thumbnails'
FONT = ROOT / 'docs/fonts/Virgil.ttf'
BG, INK, PLUM, ORANGE = '#FFF0D5', '#34233F', '#713C8C', '#C95724'


def text(d, x, y, label, size, color=INK):
    font = ImageFont.truetype(str(FONT), size)
    box = d.textbbox((x, y), label, font=font)
    assert box[2] <= 1230 and box[3] <= 690, (label, box)
    d.text((x, y), label, font=font, fill=color)


def base(title):
    im = Image.new('RGB', (1280, 720), BG)
    d = ImageDraw.Draw(im)
    text(d, 55, 30, 'LLM FROM SCRATCH', 28, PLUM)
    text(d, 1030, 30, 'EP 03B', 28, PLUM)
    text(d, 55, 110, title, 72 if len(title) > 22 else 86)
    return im, d


def save(im, name):
    OUT.mkdir(exist_ok=True)
    p = OUT / f'episode-03b-{name}.jpg'
    im.save(p, quality=95, subsampling=0)
    assert p.stat().st_size < 2_000_000
    return p


def arrow(d, start, end, y):
    d.line([(start, y), (end, y)], fill=ORANGE, width=8)
    d.line([(end-20,y-18),(end,y),(end-20,y+18)], fill=ORANGE, width=8)


def main():
    im, d = base('BUILD IT IN NUMPY')
    d.rounded_rectangle((55,260,645,570), radius=22, fill=INK)
    text(d,85,295,'scores = W[x]',45,BG)
    text(d,85,375,'p = softmax(scores)',40,BG)
    text(d,85,455,'loss = -log(p)',45,'#FFBD85')
    arrow(d,680,755,415)
    text(d,830,275,'TARGET LOSS',34,PLUM)
    text(d,825,355,'1.386',75)
    text(d,830,455,'9 predictions',32,PLUM)
    text(d,55,630,'WEIGHTS  →  PROBABILITIES  →  LOSS',33,PLUM)
    a=save(im,'build-it-in-numpy')

    im,d=base('WHY LOSS EXPLODES')
    for left,label,value,color in [(65,'SOFTMAX + LOG','inf',ORANGE),(735,'LOG-SOFTMAX','2000',PLUM)]:
        d.rounded_rectangle((left,285,left+465,565),radius=20,outline=color,width=5)
        text(d,left+30,315,label,35,color)
        text(d,left+90,390,value,100,color)
    arrow(d,565,695,425)
    text(d,65,625,'SAME SCORES. FINITE LOSS.',36,PLUM)
    b=save(im,'why-loss-explodes')

    im,d=base('ONE WEIGHT. THREE LOSSES.')
    text(d,65,250,'Change the END score after a',37,PLUM)
    for left,label,value,color in [(65,'ZERO','1.386',PLUM),(470,'ln 2','1.331',PLUM),(875,'ln 100','1.807',ORANGE)]:
        d.rounded_rectangle((left,335,left+340,575),radius=20,outline=color,width=5)
        text(d,left+35,365,label,47,color)
        text(d,left+35,455,value,67,color)
    text(d,65,630,'A BIGGER SCORE CAN HURT',36,PLUM)
    c=save(im,'one-weight-three-losses')
    sheet=Image.new('RGB',(960,900),'#EEE8DF')
    for i,(path,label) in enumerate([(a,'A · NumPy build'),(b,'B · Underflow'),(c,'C · Overshoot')]):
        # Full thumbnail at half size, with room for its label.
        thumb=Image.open(path).resize((480,270))
        sheet.paste(thumb,(450,i*300+15))
        ImageDraw.Draw(sheet).text((25,i*300+125),label,font=ImageFont.truetype(str(FONT),30),fill=INK)
    sheet.save(OUT/'episode-03b-options.jpg',quality=95)
    print('\n'.join(str(p) for p in [a,b,c]))


if __name__=='__main__':
    main()
