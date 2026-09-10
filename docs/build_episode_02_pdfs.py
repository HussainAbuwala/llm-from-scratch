#!/usr/bin/env python3
"""Build Episode 02A's audience guide and 29-page vector canvas PDF.

Install docs/requirements.txt, then run from the repository root.
"""
import html
import re
from pathlib import Path
import build_pdfs as base
from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle, SimpleDocTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def markup(value):
    value = html.escape(value)
    value = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', value)
    value = re.sub(r'`(.+?)`', r'<font name="Mono">\1</font>', value)
    value = re.sub(r'(https://[^\s<]+)', lambda m: f'<link href="{m.group(1)}" color="#4b4f95">{m.group(1)}</link>', value)
    return value

body = ParagraphStyle('ep02body', parent=base.body, fontSize=10, leading=14, spaceAfter=7)
heading = ParagraphStyle('ep02heading', parent=base.h2, fontSize=20, leading=24, spaceAfter=12, keepWithNext=True)
subheading = ParagraphStyle('ep02subheading', parent=base.h3, spaceBefore=7, spaceAfter=6, keepWithNext=True)

def table(lines):
    rows = [[s.strip() for s in line.strip('|').split('|')] for line in lines]
    rows = [row for row in rows if not all(re.fullmatch(r':?-+:?',s) for s in row)]
    n=len(rows[0]); width=475
    widths = {2:[180,295],3:[110,175,190],4:[120,118,118,119],5:[90,90,100,95,100],6:[100,75,75,75,75,75]}[n]
    cell=ParagraphStyle('ep02cell',parent=body,fontSize=9,leading=12,spaceAfter=0)
    cells=[[Paragraph(markup(('**'+s+'**') if i==0 else s),cell) for s in row] for i,row in enumerate(rows)]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),base.PALE),('LINEBELOW',(0,0),(-1,0),.8,base.ACCENT),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d8dce5')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    return t

def footer(c,doc):
    c.saveState(); w,h=doc.pagesize
    c.setStrokeColor(colors.HexColor('#d8dce5'));c.line(60,48,w-60,48)
    c.setFillColor(base.INK);c.setFont('Text',8)
    c.drawString(60,32,'Hussain Abuwala  /  LLM from Scratch  /  Episode 02A')
    c.drawRightString(w-60,32,str(doc.page));c.restoreState()

def theory():
    lines=(HERE/'episode-02-theory.md').read_text().splitlines(); story=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1;continue
        if line=='<!-- pagebreak -->':story.append(PageBreak());i+=1;continue
        if line.startswith('$$'):
            story.extend([Spacer(1,4),base.equation(line[2:-2]),Spacer(1,12)]);i+=1;continue
        if line.startswith('```'):
            block=[];i+=1
            while not lines[i].startswith('```'):block.append(lines[i]);i+=1
            story.append(Paragraph('<br/>'.join(html.escape(s).replace(' ','&#160;') for s in block),base.code));i+=1;continue
        if line.startswith('|'):
            block=[]
            while i<len(lines) and lines[i].startswith('|'):block.append(lines[i]);i+=1
            story.extend([table(block),Spacer(1,10)]);continue
        for prefix,style in [('### ',subheading),('## ',heading),('# ',base.h1),('> ',base.quote),('- ',body)]:
            if line.startswith(prefix):
                story.append(Paragraph(('• ' if prefix=='- ' else '')+markup(line[len(prefix):]),style));break
        else:story.append(Paragraph(markup(line),body))
        i+=1
    dest=HERE/'episode-02-theory.pdf'
    SimpleDocTemplate(str(dest),pagesize=(595.276,841.89),leftMargin=60,rightMargin=60,topMargin=52,bottomMargin=66,title='Trigrams and the Sparsity Wall - Episode 02A',author='Hussain Abuwala').build(story,onFirstPage=footer,onLaterPages=footer)
    print(dest)

if __name__=='__main__':
    theory()
    base.canvas_pdf(ROOT/'canvas/episode_02_trigrams.excalidraw',HERE/'episode-02-canvas.pdf','Episode 02A - Trigrams and the Sparsity Wall')
