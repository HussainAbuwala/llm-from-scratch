"""Editable diagram thumbnails: the Count-to-Learn bridge uses both stage palettes."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'youtube/thumbnails'
FONT=ROOT/'docs/fonts/Virgil.ttf'
W,H=1280,720
# Count keeps the established navy. Learn is warm paper; Attend is deep plum.
COUNT='#0B1831'; LEARN='#FFF0D5'; INK='#34233F'; PLUM='#713C8C'
ORANGE='#C95724'; PAPER='#FFFBE9'; BLUE='#88D0FF'
def text(d,x,y,s,size,color=INK):
 f=ImageFont.truetype(str(FONT),size)
 b=d.textbbox((x,y),s,font=f)
 assert b[2]<1250 and b[3]<705,(s,b)
 d.text((x,y),s,font=f,fill=color)
def base():
 im=Image.new('RGB',(W,H),LEARN);d=ImageDraw.Draw(im)
 # A small inherited Count region transitions into the new Learn background.
 d.polygon([(0,0),(355,0),(285,H),(0,H)],fill=COUNT)
 text(d,35,35,'COUNT',31,BLUE)
 text(d,925,35,'LEARN WEIGHTS',28,PLUM)
 return im,d
def arrow(d,start,end,color=ORANGE):
 x,y=start;u,v=end
 d.line([start,end],fill=color,width=8)
 d.line([(u-25,v-23),end,(u-25,v+23)],fill=color,width=8)
def save(im,name):
 p=OUT/name;im.save(p,quality=95,subsampling=0)
 assert p.stat().st_size<2_000_000
 print(p)
# A: explicit transition, using a count table and a dial for adjustable weights.
im,d=base()
text(d,400,133,'NEXT',115)
text(d,400,251,'CHAPTER',115,PLUM)
for r in range(3):
 for c in range(3):
  x,y=35+c*76,420+r*60
  d.rectangle((x,y,x+65,y+49),outline=BLUE,width=3)
  text(d,x+22,y+3,str((r+c)%4),29,BLUE)
arrow(d,(370,510),(670,510))
d.arc((820,410,1080,650),195,345,fill=PLUM,width=9)
d.line([(950,555),(1025,463)],fill=ORANGE,width=12)
d.ellipse((934,539,966,571),fill=PLUM)
text(d,380,635,'COUNTS TO ADJUSTABLE WEIGHTS',34,INK)
save(im,'bridge-02-to-03.jpg')
# B: lighter wording around an adjustable model, without claiming instant sharing.
im,d=base()
text(d,395,135,'GIVE IT',112)
text(d,395,250,'A DIAL',112,PLUM)
for r in range(3):
 for c in range(3):
  x,y=35+c*76,420+r*60
  d.rectangle((x,y,x+65,y+49),outline=BLUE,width=3)
  text(d,x+22,y+3,str((r+c)%4),29,BLUE)
arrow(d,(370,510),(670,510))
for j in range(3):
 y=440+j*65;d.line([(760,y),(1160,y)],fill=PLUM,width=6)
 x=[850,1050,940][j];d.ellipse((x-15,y-15,x+15,y+15),fill=ORANGE)
text(d,395,640,'OUR NEXT LANGUAGE MODEL',33,INK)
save(im,'bridge-02-to-03-sharing.jpg')
# C: a bridge about connecting the lessons, with an explicit Count -> Learn route.
im,d=base()
text(d,390,135,'CONNECT',100)
text(d,390,245,'THE DOTS',100,PLUM)
for x,y,col in [(170,525,BLUE),(530,525,PLUM),(920,525,ORANGE)]:
 d.ellipse((x-24,y-24,x+24,y+24),fill=col)
arrow(d,(320,525),(475,525));arrow(d,(585,525),(860,525),PLUM)
text(d,53,592,'COUNTS',40,BLUE)
text(d,405,592,'WHAT WE KNOW',30,PLUM)
text(d,820,592,'WHAT’S NEXT',33,INK)
save(im,'bridge-02-to-03-roadmap.jpg')
# Review contact sheet.
sheet=Image.new('RGB',(960,900),'#EEE8DF');sd=ImageDraw.Draw(sheet)
for i,(name,label) in enumerate([('bridge-02-to-03.jpg','A · Next chapter'),('bridge-02-to-03-sharing.jpg','B · Give it a dial'),('bridge-02-to-03-roadmap.jpg','C · Connect the dots')]):
 thumb=Image.open(OUT/name);thumb.thumbnail((480,270));sheet.paste(thumb,(450,i*300+15))
 sd.text((25,i*300+120),label,font=ImageFont.truetype(str(FONT),29),fill=INK)
sheet.save(OUT/'bridge-02-to-03-options.jpg',quality=95)
