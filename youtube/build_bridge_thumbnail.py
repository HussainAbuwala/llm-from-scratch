"""Native diagram thumbnail; uses the existing series palette and local font."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent.parent
im=Image.new('RGB',(1280,720),'#0b1831'); d=ImageDraw.Draw(im)
FONT=ROOT/'docs/fonts/Virgil.ttf'
def t(x,y,s,size,color='#fffbe9'):
 f=ImageFont.truetype(str(FONT),size)
 bounds=d.textbbox((x,y),s,font=f)
 assert bounds[2]<1250 and bounds[3]<700,(s,bounds)
 d.text((x,y),s,font=f,fill=color)
t(60,42,'LLM FROM SCRATCH',30,'#88d0ff')
t(60,140,'WHAT COMES',91)
t(60,244,'AFTER COUNTS?',91)
# Count table flows into adjustable-number controls.
for r in range(3):
 for c in range(3):
  x,y=100+c*76,420+r*60
  d.rectangle((x,y,x+66,y+50),outline='#88d0ff',width=3)
  t(x+23,y+4,str((r+c)%4),30,'#88d0ff')
d.line([(415,510),(645,510)],fill='#6de1a0',width=8)
d.line([(615,485),(645,510),(615,535)],fill='#6de1a0',width=8)
for j in range(3):
 y=435+j*70
 d.line([(755,y),(1160,y)],fill='#c9b7ff',width=5)
 x=[870,1050,945][j]
 d.ellipse((x-15,y-15,x+15,y+15),fill='#c9b7ff')
t(90,630,'COUNTS',32,'#88d0ff'); t(805,630,'WEIGHTS',32,'#c9b7ff')
p=ROOT/'youtube/thumbnails/bridge-02-to-03.jpg'
im.save(p,quality=95,subsampling=0)
print(p)

# B: the central question, using the same cup/mug illustration as the episode.
im=Image.new('RGB',(1280,720),'#0b1831'); d=ImageDraw.Draw(im)
t(60,42,'LLM FROM SCRATCH',30,'#88d0ff')
t(60,150,'CAN IT SHARE',94)
t(60,255,'WHAT IT LEARNS?',82)
for x,label,col in [(75,'CUP','#88d0ff'),(825,'MUG','#c9b7ff')]:
 d.rounded_rectangle((x,430,x+365,580),radius=18,outline=col,width=5)
 f=ImageFont.truetype(str(FONT),66)
 d.text((x+182,505),label,font=f,fill=col,anchor='mm')
d.line([(475,505),(775,505)],fill='#6de1a0',width=8)
d.line([(745,475),(775,505),(745,535)],fill='#6de1a0',width=8)
t(610,425,'?',60,'#6de1a0')
t(65,650,'THE QUESTION AFTER TRIGRAMS',30,'#88d0ff')
im.save(ROOT/'youtube/thumbnails/bridge-02-to-03-sharing.jpg',quality=95,subsampling=0)

# C: orient returning viewers in the series.
im=Image.new('RGB',(1280,720),'#0b1831'); d=ImageDraw.Draw(im)
t(60,42,'LLM FROM SCRATCH',30,'#88d0ff')
t(60,145,'WHERE WE',104)
t(60,257,'GO NEXT',104,'#6de1a0')
for x,label,col in [(65,'COUNTS','#88d0ff'),(460,'WEIGHTS','#c9b7ff'),(855,'ATTENTION','#6de1a0')]:
 d.rounded_rectangle((x,470,x+345,580),radius=14,outline=col,width=4)
 f=ImageFont.truetype(str(FONT),43)
 d.text((x+172,525),label,font=f,fill=col,anchor='mm')
for x in [425,820]:
 d.line([(x,525),(x+23,525)],fill='#fffbe9',width=5)
 d.line([(x+12,514),(x+23,525),(x+12,536)],fill='#fffbe9',width=4)
t(140,615,'DONE',29,'#88d0ff');t(555,615,'NEXT',29,'#c9b7ff');t(960,615,'LATER',29,'#6de1a0')
im.save(ROOT/'youtube/thumbnails/bridge-02-to-03-roadmap.jpg',quality=95,subsampling=0)

# Review sheet; not an upload thumbnail.
sheet=Image.new('RGB',(960,3*300),'#e9ecef')
sd=ImageDraw.Draw(sheet)
for i,(name,label) in enumerate([
 ('bridge-02-to-03.jpg','A · What comes after counts?'),
 ('bridge-02-to-03-sharing.jpg','B · Can it share what it learns?'),
 ('bridge-02-to-03-roadmap.jpg','C · Where we go next')]):
 thumb=Image.open(ROOT/'youtube/thumbnails'/name);thumb.thumbnail((480,270))
 sheet.paste(thumb,(450,i*300+15))
 sd.text((25,i*300+120),label,font=ImageFont.truetype(str(FONT),25),fill='#0b1831')
sheet.save(ROOT/'youtube/thumbnails/bridge-02-to-03-options.jpg',quality=95)
