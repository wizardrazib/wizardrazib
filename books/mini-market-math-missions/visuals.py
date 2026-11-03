"""Original local vector artwork. No external assets or image services."""
import math
from reportlab.lib.colors import black,white,HexColor

def path(c,pts,close=False,fill=0):
 p=c.beginPath();p.moveTo(*pts[0])
 for pt in pts[1:]:p.lineTo(*pt)
 if close:p.close()
 c.drawPath(p,stroke=1,fill=fill)

def star(c,x,y,r=22):
 pts=[]
 for i in range(10):
  a=math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*.46
  pts.append((x+rr*math.cos(a),y+rr*math.sin(a)))
 path(c,pts,True)

def icon(c,kind,x,y,size=70,color=False):
 c.saveState();c.translate(x,y);c.scale(size/100,size/100)
 c.setLineWidth(3);c.setLineJoin(1);c.setLineCap(1)
 ink=HexColor('#14354A') if color else black
 c.setStrokeColor(ink);c.setFillColor(HexColor('#FFF8DD') if color else white)
 if kind=='pot':
  path(c,[(18,57),(28,13),(73,13),(83,57)],True,1);c.roundRect(13,57,75,13,4,fill=1)
  c.line(50,70,50,92);c.ellipse(28,77,50,89,fill=1);c.ellipse(50,83,73,95,fill=1)
  c.circle(50,37,11,fill=0)
 elif kind=='can':
  c.roundRect(19,20,50,49,9,fill=1);c.arc(48,35,92,79,-75,260)
  path(c,[(19,33),(2,58),(6,66),(29,48)],False);c.line(30,69,57,69)
  c.circle(36,44,2,fill=1);c.circle(53,44,2,fill=1);c.arc(36,30,54,43,190,160)
 elif kind=='seed':
  c.roundRect(15,8,69,84,5,fill=1);c.line(15,75,84,75)
  c.ellipse(32,28,65,61,fill=0);c.line(48,29,48,57);c.line(48,46,36,51)
  c.setFont('Bold',10);c.drawCentredString(50,13,'SEEDS')
 elif kind=='light':
  path(c,[(16,16),(39,8),(62,67),(39,76)],True,1);path(c,[(35,74),(63,63),(72,79),(44,91)],True,1)
  for a,b in [((73,91),(85,99)),((80,79),(98,83)),((64,97),(68,110))]:c.line(*a,*b)
 elif kind=='mirror':
  c.roundRect(19,37,62,59,16,fill=1);c.roundRect(38,5,24,32,5,fill=1)
  c.line(32,67,49,84);c.line(38,52,66,80)
 elif kind=='window':
  c.roundRect(9,9,82,83,5,fill=1);c.line(50,9,50,92);c.line(9,50,91,50)
  c.line(20,62,39,82);c.line(61,22,81,43)
 elif kind=='magnet':
  c.setLineWidth(16);c.arc(18,9,82,78,180,180);c.line(18,43,18,84);c.line(82,43,82,84)
  c.setLineWidth(3);c.line(9,64,27,64);c.line(73,64,91,64)
  for x in [3,94]:c.line(x,87,x+3,100)
 elif kind=='cup':
  path(c,[(17,82),(26,13),(72,13),(82,82)],True,1);c.line(22,47,77,47)
  for xx,yy in [(36,28),(51,22),(65,30)]:c.circle(xx,yy,2,fill=1)
 elif kind=='bridge':
  c.rect(4,7,19,46,fill=1);c.rect(77,7,19,46,fill=1)
  path(c,[(9,54),(19,65),(29,54),(39,65),(49,54),(59,65),(69,54),(79,65),(89,54)])
  c.rect(38,66,24,15,fill=1);c.rect(41,81,18,12,fill=1)
 elif kind=='car':
  path(c,[(8,45),(23,45),(33,65),(66,65),(79,45),(92,45),(92,24),(8,24)],True,1)
  c.circle(29,25,11,fill=1);c.circle(73,25,11,fill=1);c.line(49,64,49,45)
  c.line(3,6,97,18)
 elif kind=='map':
  path(c,[(4,13),(33,20),(63,9),(96,20),(96,89),(64,80),(33,94),(4,85)],True,1)
  c.setDash(3,4);path(c,[(17,31),(27,64),(48,43),(77,67)]);c.setDash()
  c.circle(17,31,4);c.line(74,63,83,73);c.line(74,73,83,63)
 elif kind=='chart':
  c.roundRect(7,6,86,88,4,fill=1)
  for yy,n in [(75,3),(49,2),(23,4)]:
   for i in range(n):star(c,23+i*18,yy,7)
 elif kind=='clock':
  c.circle(50,54,39,fill=1);c.line(50,54,50,79);c.line(50,54,72,54)
  for a in range(0,360,30):
   t=math.radians(a);c.line(50+32*math.cos(t),54+32*math.sin(t),50+36*math.cos(t),54+36*math.sin(t))
 elif kind=='badge':
  path(c,[(32,36),(23,2),(49,14),(75,2),(65,36)],True,1);star(c,49,61,38)
 elif kind=='foot':
  c.ellipse(24,8,51,56,fill=1);c.ellipse(50,49,76,91,fill=1)
  for xx,yy in [(27,67),(39,78),(64,98)]:c.circle(xx,yy,5,fill=1)
 elif kind=='card':
  c.roundRect(7,11,86,78,7,fill=1);c.circle(27,66,9)
  for yy in [48,33,23]:c.line(23,yy,77,yy)
 else:
  c.circle(44,61,29,fill=1);c.circle(44,61,21);path(c,[(65,39),(87,13),(80,7),(58,33)],True,1)
 c.restoreState()

KINDS=['pot','can','seed','can','light','mirror','window','light','magnet','cup','bridge','car','map','chart','clock','card','map','magnet','badge','bridge']
def strip(c,left,bottom,width,height,case_id=None):
 c.saveState();c.setStrokeColor(black);c.setFillColor(white);c.setLineWidth(1.4)
 c.roundRect(left,bottom,width,height,10,fill=1)
 kinds=[KINDS[(case_id-1)%20], 'magnifier','card'] if case_id else ['magnifier','seed','badge']
 if case_id==1:kinds=['pot','pot','pot']
 size=min(115,height-30)
 for i,k in enumerate(kinds):
  xx=left+width*(i+.5)/3-size/2
  icon(c,k,xx,bottom+17,size)
  if case_id==1 and i>0:
   # Replace the generic circle sticker with the exact recorded shape.
   c.saveState();c.translate(xx,bottom+17);c.scale(size/100,size/100)
   c.setFillColor(white);c.setStrokeColor(white);c.circle(50,37,13,fill=1,stroke=0)
   c.setStrokeColor(black);c.setLineWidth(3)
   if i==1:path(c,[(39,28),(61,28),(50,48)],True)
   else:c.rect(40,27,20,20)
   c.restoreState()
  if case_id==1:
   c.setFillColor(black);c.setFont('Bold',9);c.drawCentredString(xx+size/2,bottom+5,['A • CIRCLE • 8 cm','B • TRIANGLE • 12 cm','C • SQUARE • 10 cm'][i])
 # Case 1 plant pots are schematic; sticker variation must match evidence.
 c.restoreState()

def note_box(c,x,y,w,h,solved=False):
 c.saveState();c.setFillColor(white);c.setStrokeColor(black);c.setLineWidth(1.5)
 c.roundRect(x,y,w,h,10,fill=1)
 for yy in range(int(y+20),int(y+h-10),18):c.circle(x+9,yy,2,fill=0)
 c.setFillColor(black);c.setFont('Bold',10);c.drawString(x+24,y+h-19,'DETECTIVE SKETCH & NOTE BOX')
 c.setLineWidth(.55)
 for yy in range(int(y+22),int(y+h-35),24):c.line(x+25,yy,x+w-18,yy)
 if solved:
  c.setFillColor(white);c.roundRect(x+w-145,y+10,132,57,9,fill=1)
  star(c,x+w-122,y+39,16);c.setFillColor(black);c.setFont('Bold',10);c.drawString(x+w-98,y+44,'CASE SOLVED!')
  c.rect(x+w-96,y+24,10,10);c.setFont('Body',8);c.drawString(x+w-82,y+26,'Clues checked')
 c.restoreState()
