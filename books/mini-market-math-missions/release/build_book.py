"""Original local, deterministic vector book build. Python 3.11+, ReportLab, Pillow, PyMuPDF."""
from pathlib import Path
from itertools import combinations
import json,math,hashlib,zipfile
import pymupdf as fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black,white,HexColor
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'release';OUT.mkdir(exist_ok=True)
TITLE='Mini-Market Math Missions';SUB='100 Fun Math & Logic Puzzles for Kids Ages 7-9';AUTHOR='Mira West'
for n,f in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
W,H=612,792; C=None;PAGE=0;LOG=[];MAN=[]
DEPTS=[('Fruit & Veggie Stand',['Apple','Banana','Carrot','Pear']),('Bakery Corner',['Bread','Muffin','Cookie','Pretzel']),('Dairy & Snacks',['Milk carton','Yogurt','Cheese','Cracker pack']),('Toy & Sticker Stall',['Toy car','Sticker sheet','Ball','Robot']),('School Supply Counter',['Pencil','Notebook','Eraser','Crayons']),('Juice Bar',['Apple juice','Berry juice','Orange juice','Lemonade'])]
def shape(pts,fill=True):
 p=C.beginPath();p.moveTo(*pts[0])
 for v in pts[1:]:p.lineTo(*v)
 p.close();C.drawPath(p,fill=int(fill),stroke=1)
def star(x,y,r=20):
 shape([(x+(r if i%2==0 else r*.47)*math.cos(math.pi/2+i*math.pi/5),y+(r if i%2==0 else r*.47)*math.sin(math.pi/2+i*math.pi/5)) for i in range(10)])
def doodle(kind,x,y,s=65,color=False):
 C.saveState();C.translate(x,y);C.scale(s/100,s/100);C.setLineWidth(2.5);C.setLineJoin(1);C.setLineCap(1)
 C.setStrokeColor(HexColor('#173348') if color else black);C.setFillColor(HexColor('#FFF9E4') if color else white)
 face=(50,45)
 if kind in ['Apple','Pear']:
  p=C.beginPath();p.moveTo(50,18)
  if kind=='Apple':p.curveTo(5,1,4,80,34,77);p.curveTo(46,70,48,74,50,76);p.curveTo(97,94,98,2,50,18)
  else:p.curveTo(8,8,8,48,30,66);p.curveTo(34,96,66,96,70,66);p.curveTo(94,48,91,7,50,18)
  C.drawPath(p,fill=1,stroke=1);C.line(50,78,53,94);C.ellipse(55,81,76,94,fill=1)
 elif kind=='Banana':
  p=C.beginPath();p.moveTo(16,78);p.curveTo(35,45,65,39,85,78);p.curveTo(89,37,58,9,29,31);p.curveTo(15,42,9,63,16,78);C.drawPath(p,fill=1,stroke=1)
  C.line(13,79,19,85);C.line(83,79,88,86);face=(51,43)
 elif kind=='Carrot':
  shape([(23,77),(77,77),(50,9)])
  for xx in [32,50,68]:C.line(50,78,xx,96)
  C.line(29,65,38,65);C.line(61,57,67,57);face=(50,61)
 elif kind=='Bread':
  C.roundRect(13,18,74,62,17,fill=1)
  for xx in [30,48,66]:C.line(xx,63,xx+5,72)
 elif kind=='Muffin':
  shape([(22,52),(31,15),(71,15),(80,52)]);C.roundRect(13,49,76,32,13,fill=1);face=(50,63)
 elif kind=='Cookie':
  C.circle(50,51,36,fill=1)
  for xx,yy in [(29,68),(68,68),(27,35),(73,34),(50,78)]:C.circle(xx,yy,3,fill=0)
 elif kind=='Pretzel':
  C.setLineWidth(11);C.ellipse(19,29,52,78);C.ellipse(48,29,81,78);C.line(32,31,69,63);C.line(68,31,31,63);face=None
 elif kind=='Milk carton':
  shape([(25,17),(75,17),(75,71),(62,89),(38,89),(25,71)]);C.line(25,71,75,71);C.line(38,89,38,72)
 elif kind=='Yogurt':
  shape([(19,73),(29,16),(71,16),(81,73)]);C.roundRect(14,73,72,11,4,fill=1)
 elif kind=='Cheese':
  shape([(14,23),(85,23),(85,73),(14,58)]);C.line(14,58,85,73)
  for xx,yy in [(28,40),(73,36),(70,59)]:C.circle(xx,yy,4)
 elif kind=='Cracker pack':
  C.roundRect(16,12,68,77,6,fill=1);C.line(16,79,84,79);C.line(16,23,84,23)
 elif kind=='Toy car':
  shape([(9,29),(9,53),(25,53),(36,75),(65,75),(77,53),(91,53),(91,29)])
  C.circle(28,28,11,fill=1);C.circle(73,28,11,fill=1);C.line(50,74,50,55);face=(51,42)
 elif kind=='Sticker sheet':
  C.roundRect(13,12,74,79,5,fill=1)
  for xx,yy in [(30,72),(69,72),(30,29),(69,29)]:C.circle(xx,yy,8)
 elif kind=='Ball':
  C.circle(50,51,36,fill=1);C.arc(18,15,55,88,-80,160);C.arc(48,15,85,88,100,160);face=(50,52)
 elif kind=='Robot':
  C.roundRect(22,33,56,48,7,fill=1);C.line(50,81,50,93);C.circle(50,95,3)
  C.rect(32,14,36,18,fill=1);face=(50,57)
 elif kind=='Pencil':
  shape([(30,26),(30,86),(69,86),(69,26),(50,8)]);C.line(30,74,69,74);C.line(30,26,69,26);face=(50,49)
 elif kind=='Notebook':
  C.roundRect(20,12,63,79,6,fill=1)
  for yy in [25,42,59,76]:C.line(12,yy,29,yy)
 elif kind=='Eraser':
  C.roundRect(13,24,75,53,9,fill=1);C.line(65,24,65,77);face=(39,50)
 elif kind=='Crayons':
  C.rect(19,13,63,47,fill=1)
  for xx in [22,43,64]:shape([(xx,60),(xx,81),(xx+8,94),(xx+16,81),(xx+16,60)])
  face=(50,37)
 else:
  shape([(21,75),(29,15),(72,15),(80,75)]);C.line(16,78,85,78);C.line(58,78,67,96);C.line(67,96,82,96)
  # Flavor symbol remains outside the face area.
  if kind=='Orange juice':C.circle(50,64,7)
  elif kind=='Berry juice':
   for xx in [43,52,61]:C.circle(xx,65,3)
  elif kind=='Lemonade':C.ellipse(37,58,62,70)
  else:C.line(39,65,61,65)
  face=(50,39)
 if face:
  xx,yy=face
  # Safe compact face: eye spacing 10 units; no whiskers or side marks.
  C.setFillColor(HexColor('#173348') if color else black);C.circle(xx-5,yy+3,1.8,fill=1,stroke=0);C.circle(xx+5,yy+3,1.8,fill=1,stroke=0)
  C.arc(xx-5,yy-7,xx+5,yy+1,190,160)
 C.restoreState()
def txt(x,y,s,size=13,bold=False):
 C.setFillColor(black);C.setFont('Bold' if bold else 'Body',size);C.drawString(x,y,s)
def paragraph(x,y,s,width=510,size=13,leading=19):
 line=''
 for word in s.split():
  v=(line+' '+word).strip()
  if pdfmetrics.stringWidth(v,'Body',size)>width:txt(x,y,line,size);line=word;y-=leading
  else:line=v
 if line:txt(x,y,line,size);y-=leading
 return y

def base(title,sub=''):
 global PAGE,L,R
 PAGE+=1;L=48 if PAGE%2 else 40;R=40 if PAGE%2 else 48
 txt(L,757,TITLE.upper()+'  /  '+AUTHOR.upper(),8,True)
 C.setStrokeColor(black);C.setLineWidth(1.4);C.line(L,746,W-R,746)
 txt(L,712,title,22,True)
 if sub:paragraph(L,685,sub,W-L-R,12)
 txt(L,28,'MIRA WEST',8);C.setFont('Body',9);C.drawRightString(W-R,28,str(PAGE))

def shelf(m,y=530):
 wid=(W-L-R)/4
 for i,(name,price) in enumerate(m['prices'].items()):
  x=L+i*wid;doodle(name,x+wid/2-34,y+36,68)
  C.setLineWidth(2);C.line(x+4,y+31,x+wid-4,y+31);C.setFillColor(white);C.roundRect(x+6,y-12,wid-12,37,5,fill=1)
  txt(x+13,y+10,name,10,True);txt(x+13,y-5,f'{price}¢ each',11)
def response(y,h=70,label='SHOW YOUR THINKING'):
 C.setFillColor(white);C.setStrokeColor(black);C.setLineWidth(1.3);C.roundRect(L,y,W-L-R,h,8,fill=1)
 txt(L+13,y+h-19,label,10,True)
 for yy in range(int(y+17),int(y+h-31),22):C.setLineWidth(.5);C.line(L+14,yy,W-R-14,yy)
def complete(y=52):
 C.setFillColor(white);C.setStrokeColor(black);C.setLineWidth(1.7);star(L+22,y+21,21)
 txt(L+55,y+27,'MISSION COMPLETE',12,True);txt(L+55,y+8,'Color the star after checking both pages.',10)
def receipt(x,y,entries,total=None,w=230):
 C.setStrokeColor(black);C.setFillColor(white);C.setLineWidth(1.3);C.roundRect(x,y,w,122,8,fill=1)
 txt(x+12,y+103,'MINI-MARKET RECEIPT',10,True)
 for i,(label,val) in enumerate(entries):
  txt(x+12,y+80-i*20,label,11)
  C.setFont('Body',11);C.drawRightString(x+w-12,y+80-i*20,f'{val}¢' if val is not None else '____¢')
 C.line(x+12,y+32,x+w-12,y+32);txt(x+12,y+14,'TOTAL',11,True)
 C.setFont('Bold',11);C.drawRightString(x+w-12,y+14,f'{total}¢' if total is not None else '____¢')

MISSIONS=[];PUZZLES=[]
def puzzle(typ,question,answer,reason,terms,items):
 p={'id':len(PUZZLES)+1,'type':typ,'question':question,'answer':answer,'explanation':reason,'terms':terms,'items':items};PUZZLES.append(p);return p
for mi in range(25):
 di=min(mi//4,5);dept,names=DEPTS[di];off=mi*2
 vals=([15,30,50,85] if mi<8 else [25,45,75,120] if mi<16 else [45,70,110,165]);prices=dict(zip(names,[v+off for v in vals]));a,b,c,d=names;pa,pb,pc,pd=[prices[k] for k in names]
 m={'mission':mi+1,'department':dept,'prices':prices,'puzzles':[]};q=m['puzzles']
 if mi<4:
  total=pa+pc;pay=100 if total<=100 else 200
  q.append(puzzle('sum',f'Buy one {a.lower()} and one {c.lower()}. What is their total cost?',total,f'{pa} + {pc} = {total}¢. Add one price for each item.',[pa,pc],[a,c]))
  q.append(puzzle('change',f'Buy the same two items for {total}¢. Pay {pay}¢. How much change comes back?',pay-total,f'{pay} − {total} = {pay-total}¢. Check: {total} + {pay-total} = {pay}.',[pay,total],[a,c]))
  total2=pb+pd
  q.append(puzzle('receipt',f'The receipt lists one {b.lower()} and one {d.lower()}. Fill in the total.',total2,f'{pb} + {pd} = {total2}¢. Both receipt lines are included.',[pb,pd],[b,d]))
  target=pb+pc;matches=[pair for pair in combinations(names,2) if sum(prices[n] for n in pair)==target];assert matches==[(b,c)]
  q.append(puzzle('pair',f'Choose exactly TWO DIFFERENT items that cost {target}¢ altogether. Write both names.',f'{b} + {c}',f'{pb} + {pc} = {target}¢. No other pair of different items on this shelf has that sum.',[target],[b,c]))
 elif mi<8:
  qty=2+(mi%2);total=qty*pa+pb;pay=500
  q.append(puzzle('stock',f'One shelf holds {qty} {a.lower()} items and one {b.lower()}. What is their total value?',total,f'{" + ".join([str(pa)]*qty)} + {pb} = {total}¢. Count each item once.',[pa]*qty+[pb],[a,b]))
  q.append(puzzle('change',f'Buy that shelf group for {total}¢. Pay {pay}¢ ($5). Find the change.',pay-total,f'{pay} − {total} = {pay-total}¢. Add the change to {total} to check.',[pay,total],[a,b]))
  line=pc*2;rt=line+pd
  q.append(puzzle('missing',f'A receipt lists TWO {c.lower()} items and one {d.lower()}. Total: {rt}¢. Find the combined price of BOTH {c.lower()} items.',line,f'{rt} − {pd} = {line}¢. Check the missing line: {pc} + {pc} = {line}¢.',[rt,pd,pc],[c,d]))
  diff=(pc+pd)-(pa+pb)
  q.append(puzzle('compare',f'Basket A: one {a.lower()} and one {b.lower()}. Basket B: one {c.lower()} and one {d.lower()}. How much cheaper is Basket A?',diff,f'Basket A: {pa+pb}¢. Basket B: {pc+pd}¢. Difference: {pc+pd} − {pa+pb} = {diff}¢.',[pa,pb,pc,pd],names))
 elif mi<12:
  total=pa+pb+pc;pay=500
  q.append(puzzle('sum',f'Buy one {a.lower()}, one {b.lower()}, and one {c.lower()}. Find the total.',total,f'{pa} + {pb} + {pc} = {total}¢. Add all three prices.',[pa,pb,pc],[a,b,c]))
  q.append(puzzle('change',f'Your three-item group costs {total}¢. Pay {pay}¢. What change should you receive?',pay-total,f'{pay} − {total} = {pay-total}¢. Check: {total} + {pay-total} = {pay}.',[pay,total],[a,b,c]))
  target=pa+pd;matches=[pair for pair in combinations(names,2) if sum(prices[n] for n in pair)==target];assert matches==[(a,d)]
  q.append(puzzle('pair',f'Find TWO DIFFERENT items whose prices add to {target}¢. Write both names.',f'{a} + {d}',f'{pa} + {pd} = {target}¢. Checking all six possible pairs gives only this match.',[target],[a,d]))
  total=3*pb
  q.append(puzzle('stock',f'Three {b.lower()} items are on a shelf. What is their total value? You may use repeated addition.',total,f'{pb} + {pb} + {pb} = {total}¢. There are three items, not one.',[pb,pb,pb],[b]))
 elif mi<16:
  line=2*pa;rt=line+pc
  q.append(puzzle('missing',f'A receipt has TWO {a.lower()} items and one {c.lower()}. Total: {rt}¢. Find the line total for BOTH {a.lower()} items.',line,f'{rt} − {pc} = {line}¢. Check: {pa} + {pa} = {line}¢.',[rt,pc,pa],[a,c]))
  diff=(pb+pd)-(pa+pc)
  q.append(puzzle('compare',f'Basket A has one {a.lower()} and one {c.lower()}. Basket B has one {b.lower()} and one {d.lower()}. How much cheaper is A?',diff,f'A costs {pa+pc}¢; B costs {pb+pd}¢. {pb+pd} − {pa+pc} = {diff}¢.',[pa,pc,pb,pd],[a,c,b,d]))
  budget=pa*3+pa//2
  q.append(puzzle('budget',f'You have {budget}¢. Buy only {a.lower()} items at {pa}¢ each. What is the GREATEST number you can afford?',3,f'Three cost {3*pa}¢, within {budget}¢. Four cost {4*pa}¢, too much. So the greatest number is 3.',[budget,pa],[a]))
  total=pb+pd;pay=500
  q.append(puzzle('change',f'Buy one {b.lower()} and one {d.lower()} for {total}¢. Pay {pay}¢. Find the change.',pay-total,f'{pay} − {total} = {pay-total}¢. Check: {total} + {pay-total} = {pay}.',[pay,total],[b,d]))
 elif mi<20:
  total=2*pb+pc
  q.append(puzzle('stock',f'Buy TWO {b.lower()} items and one {c.lower()}. How much do they cost altogether?',total,f'{pb} + {pb} + {pc} = {total}¢. Include both repeated items.',[pb,pb,pc],[b,c]))
  q.append(puzzle('quantity',f'A receipt lists ONLY {a.lower()} items at {pa}¢ each. Total: {4*pa}¢. How many items were bought?',4,f'{pa} + {pa} + {pa} + {pa} = {4*pa}¢. That is four equal prices.',[4*pa,pa],[a]))
  target=pb+pd;matches=[pair for pair in combinations(names,2) if sum(prices[n] for n in pair)==target];assert matches==[(b,d)]
  q.append(puzzle('pair',f'Choose exactly TWO DIFFERENT items for a total of {target}¢. What are they?',f'{b} + {d}',f'{pb} + {pd} = {target}¢. It is the only different-item pair that fits.',[target],[b,d]))
  pay=1000
  q.append(puzzle('change',f'Buy the {total}¢ group from the first puzzle on this spread. Pay {pay}¢ ($10). Find your change.',pay-total,f'{pay} − {total} = {pay-total}¢. Check: {total} + {pay-total} = {pay}.',[pay,total],[b,c]))
 else:
  total=pa+2*pb+pc
  q.append(puzzle('receipt3',f'Finish this receipt: one {a.lower()}, TWO {b.lower()} items, and one {c.lower()}. What is the total?',total,f'{pa} + {2*pb} + {pc} = {total}¢. The middle line includes TWO items: {pb} + {pb} = {2*pb}.',[pa,2*pb,pc],[a,b,c]))
  line=2*pc;rt=pa+line+pd
  q.append(puzzle('missing3',f'A receipt lists one {a.lower()}, TWO {c.lower()} items, and one {d.lower()}. Total: {rt}¢. Find the line total for BOTH {c.lower()} items.',line,f'Known lines: {pa} + {pd} = {pa+pd}¢. {rt} − {pa+pd} = {line}¢. Check: {pc} + {pc} = {line}¢.',[rt,pa,pd,pc],[a,c,d]))
  diff=2*pd-(pa+pb+pc)
  q.append(puzzle('compare',f'Basket A: one each of {a.lower()}, {b.lower()}, and {c.lower()}. Basket B: TWO {d.lower()} items. How much cheaper is A?',diff,f'A: {pa} + {pb} + {pc} = {pa+pb+pc}¢. B: {pd} + {pd} = {2*pd}¢. Difference: {diff}¢.',[pa,pb,pc,pd,pd],[a,b,c,d]))
  pay=1000
  q.append(puzzle('change',f'Buy the receipt group for {total}¢ from this spread’s first puzzle. Pay {pay}¢. How much change comes back?',pay-total,f'{pay} − {total} = {pay-total}¢. Count up or subtract. Check: {total} + {pay-total} = {pay}.',[pay,total],[a,b,c]))
 MISSIONS.append(m)
assert len(PUZZLES)==100
# Independent validators use shelf records and task type, not rendered answer text.
for m in MISSIONS:
 pr=m['prices']
 for p in m['puzzles']:
  a=p['answer'];t=p['terms'];typ=p['type']
  if typ in ['sum','stock','receipt','receipt3']:expected=sum(t)
  elif typ=='change':expected=t[0]-t[1];assert a>=0 and a+t[1]==t[0]
  elif typ=='missing':expected=t[0]-t[1];assert expected==2*t[2]
  elif typ=='missing3':expected=t[0]-t[1]-t[2];assert expected==2*t[3]
  elif typ=='budget':expected=t[0]//t[1]
  elif typ=='quantity':expected=t[0]//t[1];assert t[0]%t[1]==0
  elif typ=='compare':
   expected=sum(t[2:])-sum(t[:2]) if len(t)==4 else sum(t[3:])-sum(t[:3])
  elif typ=='pair':
   options=[v for v in combinations(pr,2) if sum(pr[k] for k in v)==t[0]];assert len(options)==1
   expected=' + '.join(options[0])
  assert a==expected,(p['id'],a,expected)
  if isinstance(a,int):assert a>=0

C=canvas.Canvas(str(OUT/'interior.pdf'),pagesize=(W,H));C.setTitle(TITLE);C.setAuthor(AUTHOR);C.setSubject(SUB)
front=[(TITLE,[SUB,AUTHOR,'Welcome to a market full of friendly number missions!','100 numbered puzzles • Six departments • Explained answers']),('Copyright',['Copyright © 2026 Mira West','All rights reserved. Except as permitted by applicable law, no part of this book may be reproduced or transmitted in any form without prior written permission from the copyright holder.','First edition, 2026.','This is a fictional market. Names, prices, receipts, and shopping situations are invented for educational entertainment. They are not real product offers or financial advice.','Children may ask a trusted adult for help reading the instructions. No purchases or internet access are needed.']),('Welcome, Market Helper!',['The stalls are open, and the price tags are ready. Can you help check the shopping?','Read the shelf tags, work out a plan, then explain your answer. A pencil and eraser are all you need.','Some puzzles have several steps. Slow down. You can circle prices, draw items, or use repeated addition.','A mistake is a chance to check a clue. Careful thinking matters more than speed.']),('Your Money Toolkit',['All prices use US cents, shown by ¢. 100¢ = $1. 200¢ = $2. 500¢ = $5. 1000¢ = $10.','All fictional prices include tax. There are no extra fees, discounts, or hidden costs. Each shelf tag gives the price of ONE item unless a receipt line says otherwise.','A total adds all purchased items. Change is the amount paid minus the total. A budget is the most money available to spend.','TWO DIFFERENT items means two different shelf products, one of each. A line total for BOTH items includes both copies.']),('Try a Worked Example',['A pretend roll costs 20¢. A pretend pear costs 30¢. Neither is a price tag for the later missions.','Total: 20 + 30 = 50¢. Pay 100¢. Change: 100 − 50 = 50¢.','Check the change by adding: 50¢ total + 50¢ change = 100¢ paid.','Three 20¢ rolls cost 20 + 20 + 20 = 60¢. You can use repeated addition instead of multiplication.','For the greatest number you can afford, test one more item. If three fit the budget but four do not, the answer is three.']),('Plan, Solve, Check',['1. Look at the current shelf. Prices may change in each mission. Read the tags on your spread, not a previous one.','2. Read the quantity. TWO items at 40¢ each cost 40 + 40 = 80¢. A receipt line for both items is 80¢, not 40¢.','3. Write or draw your thinking in the box. Repeated addition is always welcome.','4. Check the explanation at the back when you are ready. Each spread has a Mission Complete star to color.','Teachers and parents: this is supplementary practice, not a complete or certified Grade 2–3 curriculum. Read together and adjust the pace to the child.']),('Your Market Map',['Fruit & Veggie Stand: missions 1–4, pages 8–15.','Bakery Corner: missions 5–8, pages 16–23.','Dairy & Snacks: missions 9–12, pages 24–31.','Toy & Sticker Stall: missions 13–16, pages 32–39.','School Supply Counter: missions 17–20, pages 40–47.','Juice Bar: missions 21–25, pages 48–57.','Explained answer key: pages 58–107. Final celebration: page 108.'])]
for title,blocks in front:
 base(title);y=650
 for b in blocks:y=paragraph(L,y,b,W-L-R,14,22)-17
 if PAGE not in (2,7):
  for j,k in enumerate(['Apple','Banana','Carrot','Bread']):doodle(k,L+18+j*122,87,90)
 C.showPage()
for m in MISSIONS:
 for half in range(2):
  base(f'Mission {m["mission"]}: '+('Shop & Solve' if half==0 else 'Check & Finish'),m['department']+' • Use this spread’s price tags. All prices include tax.')
  shelf(m)
  for idx,p in enumerate(m['puzzles'][half*2:half*2+2]):
   top=470 if idx==0 else 260
   txt(L,top,f'Puzzle {p["id"]}',18,True)
   y=paragraph(L,top-27,p['question'],W-L-R,13,19)
   if idx==0 and p['type'] in ('receipt','receipt3','missing','missing3'):
    names=p['items'];pr=m['prices'];typ=p['type']
    if typ=='receipt':entries=[(names[0],pr[names[0]]),(names[1],pr[names[1]])];tot=None
    elif typ=='receipt3':entries=[(names[0],pr[names[0]]),('2 × '+names[1],2*pr[names[1]]),(names[2],pr[names[2]])];tot=None
    elif typ=='missing':entries=[('2 × '+names[0],None),(names[1],pr[names[1]])];tot=p['terms'][0]
    else:entries=[(names[0],pr[names[0]]),('2 × '+names[1],None),(names[2],pr[names[2]])];tot=p['terms'][0]
    receipt(L,292,entries,tot,w=254)
    doodle(names[-1],W-R-156,306,100)
   else:
    bottom=294 if idx==0 else (89 if half else 70)
    h=min(92,y-bottom-8)
    assert h>=48,(PAGE,p['id'],h)
    response(bottom,h,'MY ANSWER: ____________________  /  THINK IT THROUGH')
   LOG.append({'page':PAGE,'puzzle':p['id'],'question_bottom':y})
  if half:complete(45)
  C.showPage()
assert PAGE==57
for m in MISSIONS:
 for half in range(2):
  base(f'Answers: Mission {m["mission"]}',m['department']+' • Match the puzzle number before checking.')
  for idx,p in enumerate(m['puzzles'][half*2:half*2+2]):
   top=638 if idx==0 else 357
   answer=str(p['answer'])+('¢' if isinstance(p['answer'],int) and p['type'] not in ('quantity','budget') else (' items' if p['type'] in ('quantity','budget') else ''))
   txt(L,top,f'Puzzle {p["id"]}',17,True)
   y=paragraph(L,top-30,'Answer: '+answer,W-L-R,16,23)
   y=paragraph(L,y-8,p['explanation'],W-L-R,13,20)
   # Price-tag pictures are a cross-check using this mission's data.
   chosen=list(dict.fromkeys(p['items']))[:3];pr=m['prices']
   for j,k in enumerate(chosen):
    xx=L+12+j*160;doodle(k,xx,top-207,70)
    txt(xx+78,top-169,k,9,True);txt(xx+78,top-187,f'{pr[k]}¢ each',10)
   C.setStrokeColor(black);C.setLineWidth(.7);C.line(L,top-229,W-R,top-229)
  C.showPage()
assert PAGE==107
base('You Are a Market Math Helper!')
for y,s in [(650,'You checked prices, read receipts, and solved 100 puzzles.'),(610,'Which department was your favorite?'),(570,'Which puzzle made you try a different plan?'),(530,'What helped most: drawing, adding, or counting up?')]:paragraph(L,y,s,size=14)
C.setFillColor(white);C.setLineWidth(2);star(W/2,390,68)
response(160,110,'DRAW YOUR OWN MARKET HELPER BADGE')
paragraph(L,121,'Grown-ups: celebrate careful reasoning, thoughtful questions, and the courage to try again. Every checked answer is progress.',size=13)
C.showPage();assert PAGE==108;C.save()
(OUT/'puzzles.json').write_text(json.dumps(MISSIONS,indent=2,ensure_ascii=False))
# Markdown handoff contains every puzzle, answer and the approved metadata.
md=[f'# {TITLE}',SUB,AUTHOR]
for m in MISSIONS:
 md += [f'## Mission {m["mission"]}: {m["department"]}', 'Shelf: '+', '.join(f'{k} {v}¢' for k,v in m['prices'].items())]
 for p in m['puzzles']:md += [f'### Puzzle {p["id"]}',p['question'],'Answer: '+str(p['answer']),p['explanation']]
(OUT/'manuscript.md').write_text('\n\n'.join(md))
# Original bright vector full-wrap cover.
spine=108*.002252;cw=17.25+spine;ch=11.25;fx=(.125+8.5+spine)*72
C=canvas.Canvas(str(OUT/'cover-full-wrap.pdf'),pagesize=(cw*72,ch*72));C.setTitle(TITLE);C.setAuthor(AUTHOR);C.setSubject(SUB)
navy=HexColor('#16354C');teal=HexColor('#25C3B4');gold=HexColor('#FFD449');coral=HexColor('#FF7762')
C.setFillColor(navy);C.rect(0,0,cw*72,ch*72,fill=1,stroke=0)
C.setFillColor(teal);C.rect(fx,0,8.625*72,ch*72,fill=1,stroke=0)
# Front title cartouche: exact wording, no keyword additions.
C.setFillColor(navy);C.roundRect(fx+33,540,548,227,23,fill=1,stroke=0)
C.setFillColor(gold);C.roundRect(fx+25,548,548,227,23,fill=1,stroke=0)
C.setFillColor(navy);C.setFont('Bold',43);C.drawCentredString(fx+299,706,'Mini-Market');C.setFont('Bold',43);C.drawCentredString(fx+299,651,'Math Missions')
C.setFont('Bold',19);C.drawCentredString(fx+299,606,'100 Fun Math & Logic Puzzles');C.drawCentredString(fx+299,578,'for Kids Ages 7-9')
# Cute market stall with striped awning and shelf product art.
C.setFillColor(HexColor('#FFF9E4'));C.setStrokeColor(navy);C.setLineWidth(3);C.roundRect(fx+76,172,450,323,18,fill=1)
for i in range(9):
 C.setFillColor(coral if i%2==0 else gold);C.rect(fx+70+i*51,463,51,48,fill=1,stroke=0)
 C.wedge(fx+70+i*51,438,fx+121+i*51,489,180,180,fill=1,stroke=0)
C.setStrokeColor(navy);C.setLineWidth(3);C.line(fx+70,512,fx+529,512)
C.setFillColor(navy);C.setFont('Bold',16);C.drawCentredString(fx+300,422,'WELCOME TO THE MINI-MARKET!')
for j,k in enumerate(['Apple','Banana','Carrot','Bread']):
 x=fx+90+j*102;doodle(k,x,300,88,True)
 C.setFillColor(gold);C.roundRect(x+9,282,70,22,5,fill=1,stroke=0)
 C.setFillColor(navy);C.setFont('Bold',11);C.drawCentredString(x+44,289,['25¢','35¢','40¢','55¢'][j])
C.setStrokeColor(navy);C.line(fx+91,279,fx+509,279)
for j,k in enumerate(['Milk carton','Toy car','Notebook']):doodle(k,fx+100+j*124,185,79,True)
C.setFillColor(coral);C.roundRect(fx+84,118,429,40,12,fill=1,stroke=0)
C.setFillColor(navy);C.setFont('Bold',15);C.drawCentredString(fx+299,132,'SHOP • SOLVE • CHECK • CELEBRATE')
C.setFont('Bold',28);C.drawCentredString(fx+299,67,AUTHOR)
# Back cover clear hierarchy, short sales copy and barcode reserve.
C.setFillColor(gold);C.setFont('Bold',27);C.drawString(39,744,'Big smiles. Smart shopping.')
C.setFillColor(white);C.setFont('Body',17)
back=['Step into a market full of friendly puzzles!','Explore six stalls with price tags, receipts,','budget clues, and cheerful market helpers.','Add prices. Check totals. Work out change.','Then color a Mission Complete star.']
for i,s in enumerate(back):C.drawString(39,685-i*30,s)
for yy,k,head,sub in [(409,'Carrot','100 NUMBERED PUZZLES','Build skills one mission at a time.'),(292,'Notebook','EXPLAINED ANSWERS','Check the steps, not just the result.')]:
 C.setFillColor(HexColor('#FFF9E4'));C.roundRect(38,yy,523,96,12,fill=1,stroke=0);doodle(k,53,yy+9,75,True)
 C.setFillColor(navy);C.setFont('Bold',18);C.drawString(148,yy+59,head);C.setFont('Body',14);C.drawString(148,yy+29,sub)
C.setFillColor(gold);C.setFont('Bold',15);C.drawString(39,249,'For curious kids ages 7-9 • Grades 2-3')
C.setFillColor(white);C.setFont('Body',13);C.drawString(39,215,'All activities use fictional US-cent prices.');C.drawString(39,193,'No shopping trips or special supplies needed.')
doodle('Apple',43,46,91,True);doodle('Pencil',158,46,91,True)
# KDP barcode clear area, 2 × 1.2 inches, 0.375 inch above trim's bottom.
C.setFillColor(white);C.rect((.125+8.5-.375-2)*72,(.125+.375)*72,144,86.4,fill=1,stroke=0)
C.save()
with fitz.open(OUT/'cover-full-wrap.pdf') as d:
 d[0].get_pixmap(dpi=300).save(OUT/'cover-full-wrap-300dpi.png')
 d[0].get_pixmap(matrix=fitz.Matrix(.7,.7)).save(OUT/'cover-preview.png')
im=Image.open(OUT/'cover-full-wrap-300dpi.png');im.save(OUT/'cover-full-wrap-300dpi.png',dpi=(300,300))
x=round((.125+8.5+spine)*300);y=round(.125*300)
im.crop((x,y,x+2550,y+3300)).save(OUT/'cover-front-300dpi.png',dpi=(300,300))
# Every page is rendered, all text bounds checked, distinct puzzle labels counted.
d=fitz.open(OUT/'interior.pdf');assert len(d)==108
alltext=[]
for i,page in enumerate(d):
 assert page.rect.width==612 and page.rect.height==792
 for b in page.get_text('blocks'):assert b[0]>=36 and b[1]>=24 and b[2]<=576 and b[3]<=770,(i+1,b)
 s=page.get_text();alltext.append(s)
 assert not any(t in s.lower() for t in ['review sample','development feedback','beta testing','development edition'])
 page.get_pixmap(matrix=fitz.Matrix(.25,.25))
assert 'Copyright © 2026 Mira West' in alltext[1]
activity='\n'.join(alltext[7:57]);key='\n'.join(alltext[57:107])
for p in PUZZLES:
 assert activity.splitlines().count(f'Puzzle {p["id"]}')==1
 assert key.splitlines().count(f'Puzzle {p["id"]}')==1
 assert str(p['answer']) in key
assert activity.count('MISSION COMPLETE')==25
# Contact sheet for manual inspection.
selection=[0,1,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,89,106,107]
contact=Image.new('RGB',(612,math.ceil(len(selection)/3)*264),'white')
for i,n in enumerate(selection):
 pix=d[n].get_pixmap(matrix=fitz.Matrix(1/3,1/3));contact.paste(Image.frombytes('RGB',(pix.width,pix.height),pix.samples),((i%3)*204,(i//3)*264))
contact.save(OUT/'interior-contact-sheet.jpg')
for n in [7,8,47,56,57]:d[n].get_pixmap().save(OUT/f'preview-page-{n+1}.png')
report={'pages':108,'activity_pages':50,'answer_pages':50,'front_pages':7,'closing_pages':1,'puzzles':100,'missions':25,'departments':6,'unique_illustrated_products':24,'mission_stars':25,'trim_inches':[8.5,11],'bleed':False,'safe_margins_points':{'inside':48,'outside':40},'cover_inches':[cw,ch],'spine_inches':spine,'cover_raster_pixels':list(im.size),'arithmetic_all_tasks':'PASS independent typed validators','pair_uniqueness':'PASS all pair tasks','page_text_bounds':'PASS all 108 pages','all_pages_rendered':True,'copyright_page':'PASS','retail_text_scan':'PASS','answer_key_numbers':'PASS exactly 1–100','human_educator_review':'not performed','kdp_previewer_and_template':'not performed','physical_proof':'not performed'}
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
