#!/usr/bin/env python3
"""Build the Episode 1 technical handout and 40-page vector canvas reading copy.

Dependencies: reportlab, matplotlib, Pillow. Optional Virgil.ttf in docs/fonts
preserves the canvas handwriting; otherwise use the included matplotlib fonts.
The editable .excalidraw is authoritative for Excalidraw-specific rough strokes.
"""
import hashlib
import html
import io
import json
import math
import re
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
from matplotlib import mathtext
from matplotlib.font_manager import FontProperties
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
FONTS=Path(matplotlib.get_data_path())/'fonts/ttf'
for name,file in [('Text','DejaVuSans.ttf'),('TextBold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTS/file)))
pdfmetrics.registerFontFamily('Text',normal='Text',bold='TextBold',italic='Text',boldItalic='TextBold')
hand=HERE/'fonts/Virgil.ttf'
if hand.exists():pdfmetrics.registerFont(TTFont('Hand',str(hand)))
else:pdfmetrics.registerFont(TTFont('Hand',str(FONTS/'DejaVuSans.ttf')))

INK=colors.HexColor('#182337');ACCENT=colors.HexColor('#4b4f95');PALE=colors.HexColor('#f1f3f8')
body=ParagraphStyle('body',fontName='Text',fontSize=10,leading=15.6,textColor=INK,spaceAfter=9)
h1=ParagraphStyle('h1',parent=body,fontName='TextBold',fontSize=30,leading=35,spaceAfter=22)
h2=ParagraphStyle('h2',parent=body,fontName='TextBold',fontSize=19,leading=25,spaceAfter=17)
h3=ParagraphStyle('h3',parent=body,fontName='TextBold',fontSize=11.5,leading=16,spaceBefore=10,spaceAfter=7,textColor=ACCENT)
small=ParagraphStyle('small',parent=body,fontSize=8.5,leading=12)
code=ParagraphStyle('code',parent=body,fontName='Mono',fontSize=9.3,leading=15,backColor=PALE,borderPadding=10,spaceBefore=5,spaceAfter=12)
quote=ParagraphStyle('quote',parent=body,fontName='TextBold',fontSize=10.4,leading=16,backColor=PALE,borderPadding=12,spaceBefore=9,spaceAfter=14)

def markup(s):
    s=html.escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`(.+?)`',r'<font name="Mono">\1</font>',s)
    s=re.sub(r'(https://[^\s<]+)',lambda m:f'<link href="{m.group(1)}" color="#4b4f95">{m.group(1)}</link>',s)
    return s

def equation(src):
    buf=io.BytesIO()
    mathtext.math_to_image('$'+src+'$',buf,prop=FontProperties(size=15),dpi=300,format='png',color='#182337')
    buf.seek(0);img=PILImage.open(buf);w,h=img.size
    scale=min(72/300,475/w)
    return Image(buf,width=w*scale,height=h*scale,hAlign='LEFT')

def table(lines):
    rows=[[x.strip() for x in line.strip().strip('|').split('|')] for line in lines]
    rows=[row for row in rows if not all(re.fullmatch(r':?-+:?',x) for x in row)]
    n=len(rows[0]);width=475
    if n==2:widths=[width*.30,width*.70]
    elif n==5:widths=[width*.32]+[width*.17]*4
    else:widths=[width/n]*n
    cells=[[Paragraph(markup(c),ParagraphStyle('cell',parent=small,fontName='TextBold' if i==0 else 'Text',spaceAfter=0)) for c in row] for i,row in enumerate(rows)]
    t=Table(cells,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('LINEBELOW',(0,0),(-1,0),.8,ACCENT),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d8dce5')),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('VALIGN',(0,0),(-1,-1),'TOP')]))
    return t

def footer(c,doc):
    c.saveState();w,h=doc.pagesize
    c.setStrokeColor(colors.HexColor('#d8dce5'));c.line(60,48,w-60,48)
    c.setFillColor(INK);c.setFont('Text',8)
    c.drawString(60,32,'Hussain Abuwala  /  LLM from Scratch  /  Episode 01')
    c.drawRightString(w-60,32,str(doc.page));c.restoreState()

def theory():
    lines=(HERE/'episode-01-theory.md').read_text().splitlines();story=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line=='<!-- pagebreak -->':story.append(PageBreak());i+=1;continue
        if line.startswith('$$'):
            story.extend([Spacer(1,5),equation(line[2:-2]),Spacer(1,14)]);i+=1;continue
        if line.startswith('```'):
            block=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
            story.append(Paragraph('<br/>'.join(html.escape(x).replace(' ','&#160;') for x in block),code));i+=1;continue
        if line.startswith('|'):
            block=[]
            while i<len(lines) and lines[i].strip().startswith('|'):block.append(lines[i]);i+=1
            story.extend([table(block),Spacer(1,12)]);continue
        if line.startswith('### '):story.append(Paragraph(markup(line[4:]),h3));i+=1;continue
        if line.startswith('## '):story.append(Paragraph(markup(line[3:]),h2));i+=1;continue
        if line.startswith('# '):story.append(Paragraph(markup(line[2:]),h1));i+=1;continue
        if line.startswith('> '):story.append(Paragraph(markup(line[2:]),quote));i+=1;continue
        if line.startswith('- '):story.append(Paragraph('• '+markup(line[2:]),body));i+=1;continue
        story.append(Paragraph(markup(line),body));i+=1
    dest=HERE/'episode-01-theory.pdf'
    SimpleDocTemplate(str(dest),pagesize=(595.276,841.89),leftMargin=60,rightMargin=60,topMargin=54,bottomMargin=66,title='The Smallest Language Model - Episode 01',author='Hussain Abuwala').build(story,onFirstPage=footer,onLaterPages=footer)
    print(dest)

def color(s):return colors.HexColor(s) if s and s!='transparent' else None

def draw_text_line(c, x, y, value, font, size, centered=False):
    """Draw one line, falling back for arrows missing from Virgil."""
    if font != 'Hand' or '→' not in value:
        (c.drawCentredString if centered else c.drawString)(x, y, value)
        return
    pieces=re.split('(→)',value)
    widths=[pdfmetrics.stringWidth(piece,'Text' if piece=='→' else font,size) for piece in pieces]
    cursor=x-sum(widths)/2 if centered else x
    for piece,width in zip(pieces,widths):
        c.setFont('Text' if piece=='→' else font,size)
        c.drawString(cursor,y,piece)
        cursor+=width

def canvas_pdf(source=None, destination=None, title='Episode 01 - Presentation Canvas'):
    source=Path(source) if source else ROOT/'canvas/episode_01_presenter.excalidraw'
    doc=json.loads(source.read_text());els=doc['elements']
    frames=sorted([e for e in els if e['type']=='frame'],key=lambda e:e['x'])
    dest=Path(destination) if destination else HERE/'episode-01-canvas.pdf';c=canvas.Canvas(str(dest),pagesize=(1600,900),pageCompression=1)
    c.setTitle(title);c.setAuthor('Hussain Abuwala')
    for fi,f in enumerate(frames):
        kids=[e for e in els if e.get('frameId')==f['id'] and not e.get('isDeleted')];byid={e['id']:e for e in kids}
        c.bookmarkPage(str(fi));c.addOutlineEntry(f['name'],str(fi),0)
        for e in kids:
            x=e['x']-f['x'];y=e['y']-f['y'];w=e['width'];h=e['height'];stroke=color(e.get('strokeColor'));fill=color(e.get('backgroundColor'))
            c.saveState()
            c.setStrokeColor(stroke or colors.black);c.setFillColor(fill or colors.white);c.setLineWidth(e.get('strokeWidth',2))
            if e.get('strokeStyle')=='dashed':c.setDash(12,8)
            if e.get('strokeStyle')=='dotted':c.setDash(2,6)
            if e['type']=='rectangle':c.roundRect(x,900-y-h,w,h,8 if e.get('roundness') else 0,stroke=int(stroke is not None),fill=int(fill is not None))
            elif e['type']=='ellipse':c.ellipse(x,900-y-h,x+w,900-y,stroke=int(stroke is not None),fill=int(fill is not None))
            elif e['type'] in ['line','arrow']:
                pts=[(x+a,900-y-b) for a,b in e['points']];p=c.beginPath();p.moveTo(*pts[0])
                for pt in pts[1:]:p.lineTo(*pt)
                c.drawPath(p)
                if e['type']=='arrow' and e.get('endArrowhead'):
                    a,b=pts[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);size=18
                    for sign in [-1,1]:c.line(*b,b[0]-size*math.cos(ang+sign*.45),b[1]-size*math.sin(ang+sign*.45))
            elif e['type']=='text':
                font={1:'Hand',2:'Text',3:'Mono'}.get(e.get('fontFamily'),'Text');size=e['fontSize'];c.setFont(font,size);c.setFillColor(stroke or INK)
                lines=e['text'].split('\n');lh=size*e.get('lineHeight',1.25)
                if e.get('containerId'):
                    container=byid[e['containerId']];cx=container['x']-f['x']+container['width']/2;cy=900-(container['y']-f['y']+container['height']/2)
                    ascent=pdfmetrics.getAscent(font)*size/1000;descent=pdfmetrics.getDescent(font)*size/1000
                    first=cy+(len(lines)-1)*lh/2-(ascent+descent)/2
                    for j,line in enumerate(lines):draw_text_line(c,cx,first-j*lh,line,font,size,centered=True)
                else:
                    ascent=pdfmetrics.getAscent(font)*size/1000
                    for j,line in enumerate(lines):draw_text_line(c,x,900-y-ascent-j*lh,line,font,size)
            c.restoreState()
        c.showPage()
    c.save();print(dest)

if __name__=='__main__':theory();canvas_pdf()
