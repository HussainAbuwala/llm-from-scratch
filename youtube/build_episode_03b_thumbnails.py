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


def coding_thumbnail():
    """Match 01B/02B's left headline + right notebook composition."""
    im = Image.new('RGB', (1280, 720), BG)
    d = ImageDraw.Draw(im)
    mono = '/System/Library/Fonts/Menlo.ttc'
    def code(x, y, label, size=23, color=INK):
        font = ImageFont.truetype(mono, size)
        assert d.textbbox((x,y), label, font=font)[2] < 1220
        d.text((x,y), label, font=font, fill=color)
    code(54,37,'LLM FROM SCRATCH',25,PLUM)
    code(950,39,'EP 03B',29,PLUM)
    text(d,54,133,"LET'S CODE",83)
    text(d,54,247,'SOFTMAX',88,PLUM)
    text(d,54,355,'AND LOSS',88)
    d.line([(60,478),(630,472)],fill=ORANGE,width=7)
    d.line([(61,482),(630,474)],fill=ORANGE,width=2)
    d.rounded_rectangle((686,154,1234,510),radius=18,fill='#FFFFFF',outline=PLUM,width=4)
    d.rounded_rectangle((708,175,748,215),radius=8,fill='#F37726')
    code(719,179,'J',28,'#FFFFFF')
    code(760,183,'episode_03.ipynb',23)
    d.line((704,232,1215,232),fill='#D8DCE3',width=2)
    code(718,245,'Run  |  Code',20,'#596579')
    d.rectangle((770,293,1214,457),fill='#F5F7FA',outline='#D6DCE5',width=2)
    d.rectangle((762,293,768,457),fill=PLUM)
    code(700,309,'[1]:',20,PLUM)
    code(785,310,'scores = W[x]',23)
    code(785,355,'p = softmax(scores)',23,PLUM)
    code(785,400,'loss = nll(W, x, y)',23,ORANGE)
    d.rounded_rectangle((865,544,1190,616),radius=16,fill=PLUM)
    text(d,894,559,'LOSS: 1.386',36,BG)
    code(54,650,'SOFTMAX + LOSS / NUMPY',25,PLUM)
    return save(im,'lets-code-softmax-loss')


def main():
    selected = coding_thumbnail()
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
    sheet=Image.new('RGB',(960,1200),'#EEE8DF')
    for i,(path,label) in enumerate([(selected,'Recommended'),(a,'Earlier A'),(b,'Earlier B'),(c,'Earlier C')]):
        # Full thumbnail at half size, with room for its label.
        thumb=Image.open(path).resize((480,270))
        sheet.paste(thumb,(450,i*300+15))
        ImageDraw.Draw(sheet).text((25,i*300+125),label,font=ImageFont.truetype(str(FONT),30),fill=INK)
    sheet.save(OUT/'episode-03b-options.jpg',quality=95)
    print('\n'.join(str(p) for p in [a,b,c]))


if __name__=='__main__':
    main()
