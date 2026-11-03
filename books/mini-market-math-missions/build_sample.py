from pathlib import Path
import sys,json,itertools,hashlib,zipfile
import fitz
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import black,white
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'junior-neighborhood-detectives'))
from visuals import star
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
W,H=612,792
P={'Apple':25,'Banana':35,'Carrot':40,'Bread':55}
answers=[65,35,80,20,205,80,('Banana','Carrot'),65]
assert P['Apple']+P['Carrot']==answers[0]
assert 100-answers[0]==answers[1]
assert P['Bread']+P['Apple']==answers[2]
assert 100-answers[2]==answers[3]
assert sum([25]*4+[35]*3)==answers[4]
assert 135-P['Bread']==P['Carrot']*2==answers[5]
pairs=[p for p in itertools.combinations(P,2) if sum(P[k] for k in p)==75]
assert pairs==[answers[6]]
assert 200-135==answers[7] and 135+5+10+50==200
C=None

def text(x,y,s,size=13,bold=False):
 C.setFillColor(black);C.setFont('Bold' if bold else 'Body',size);C.drawString(x,y,s)
def lines(x,y,s,width=500,size=13,leading=19):
 words=s.split();line=''
 for word in words:
  trial=(line+' '+word).strip()
  if pdfmetrics.stringWidth(trial,'Body',size)>width:
   text(x,y,line,size);y-=leading;line=word
  else:line=trial
 if line:text(x,y,line,size);y-=leading
 return y

def obj(kind,x,y,s=60):
 C.saveState();C.translate(x,y);C.scale(s/100,s/100);C.setFillColor(white);C.setStrokeColor(black);C.setLineWidth(3)
 if kind=='Apple':
  p=C.beginPath();p.moveTo(50,22);p.curveTo(3,3,2,80,35,77);p.curveTo(45,73,48,73,50,75);p.curveTo(97,94,99,7,50,22);C.drawPath(p,fill=1,stroke=1)
  C.line(50,75,54,94);C.ellipse(55,82,79,95,fill=1)
 elif kind=='Banana':
  p=C.beginPath();p.moveTo(16,76);p.curveTo(25,17,64,9,87,64);p.curveTo(83,0,10,0,9,66);p.close();C.drawPath(p,fill=1,stroke=1);C.line(10,67,16,76)
 elif kind=='Carrot':
  p=C.beginPath();p.moveTo(26,66);p.lineTo(76,76);p.lineTo(42,7);p.close();C.drawPath(p,fill=1,stroke=1)
  for xx in [35,50,65]:C.line(50,73,xx,97)
  C.line(37,48,52,50);C.line(43,30,52,32)
 else:
  C.roundRect(11,16,78,57,15,fill=1);C.arc(12,45,88,98,0,180)
  for xx in [30,49,68]:C.line(xx,53,xx+7,68)
 # Small friendly face; no clues depend on expression.
 C.circle(39,44,2,fill=1);C.circle(56,44,2,fill=1);C.arc(40,32,55,44,190,155)
 C.restoreState()
def box(x,y,w,h,label):
 C.setFillColor(white);C.setStrokeColor(black);C.setLineWidth(1.5);C.roundRect(x,y,w,h,10,fill=1)
 text(x+13,y+h-22,label,11,True)
 for yy in range(int(y+20),int(y+h-35),24):C.setLineWidth(.5);C.line(x+14,yy,x+w-14,yy)
def header(num,title,sub,left=False):
 global L,R
 L=40 if left else 50;R=50 if left else 40
 text(L,757,'MINI-MARKET MATH MISSIONS  /  MIRA WEST',9,True)
 C.setLineWidth(2);C.line(L,746,W-R,746)
 text(L,711,title,24,True);lines(L,685,sub,W-L-R,12)
 text(L,29,f'REVIEW SAMPLE • PAGE {num} OF 4',9)
 text(W-R-128,29,'Prices include tax.',9)
def shelf(y):
 x0=L;wid=(W-L-R)/4
 for i,(name,price) in enumerate(P.items()):
  x=x0+i*wid
  obj(name,x+wid/2-35,y+33,70)
  C.setLineWidth(2);C.line(x+4,y+30,x+wid-4,y+30)
  C.setFillColor(white);C.roundRect(x+8,y-13,wid-16,38,7,fill=1)
  text(x+16,y+9,name,11,True);text(x+16,y-6,f'{price}¢ each',11)
def badge(x,y):
 C.setFillColor(white);C.setLineWidth(2);star(C,x+23,y+23,23)
 text(x+56,y+30,'MISSION COMPLETE',12,True);text(x+56,y+10,'Color your star after checking both pages.',10)
def receipt(x,y,items,total=None,answer=False):
 w=218;h=148
 C.setFillColor(white);C.setLineWidth(1.5);C.roundRect(x,y,w,h,8,fill=1)
 text(x+14,y+h-23,'MINI-MARKET RECEIPT',11,True)
 for i,(label,value) in enumerate(items):
  text(x+14,y+h-51-i*24,label,12)
  text(x+w-62,y+h-51-i*24,str(value)+'¢' if value is not None else '___¢',12)
 C.line(x+13,y+40,x+w-13,y+40)
 text(x+14,y+19,'TOTAL',12,True);text(x+w-70,y+19,(str(total)+'¢') if total is not None else '___¢',12,True)

def make():
 global C
 C=canvas.Canvas(str(ROOT/'sample-4-pages.pdf'),pagesize=(W,H));C.setTitle('Mini-Market Math Missions — four-page sample');C.setAuthor('Mira West')
 header(1,'Mission 1: Open the Market!','Read the shelf tags. All prices are for one item.',True)
 shelf(532)
 lines(L,477,'Use cents (¢) for every answer. 100¢ = $1. These pretend prices include tax. There are no extra fees.',W-L-R,12)
 text(L,409,'1  Pack a snack',18,True)
 lines(L,383,'Buy one apple and one carrot. What is the total cost?')
 obj('Apple',L+5,278,64);text(L+88,303,'+',24,True);obj('Carrot',L+124,278,64)
 text(L+220,303,'=  ______ ¢',22,True)
 box(L,167,W-L-R,96,'SHOW YOUR THINKING: ADD THE TWO PRICE TAGS')
 text(L,128,'2  Pay with 100¢',18,True)
 lines(L,102,'Use your total from Puzzle 1. How much change do you get?')
 text(L,62,'100¢ − ______ ¢ = ______ ¢',18,True)
 C.showPage()
 header(2,'Check the Lunch Receipt','The shelf prices are repeated so you can check each clue.')
 shelf(532)
 text(L,480,'3  Finish the receipt',18,True)
 lines(L,454,'Buy one bread loaf and one apple. Fill in the total.')
 receipt(L,268,[('Bread',55),('Apple',25)])
 box(L+238,268,W-L-R-238,148,'MY ADDITION')
 text(L,229,'4  Count the change',18,True)
 lines(L,203,'Pay 100¢ for the receipt in Puzzle 3. How much change comes back? Complete the check below.')
 text(L,134,'Total ______ ¢ + change ______ ¢ = 100¢',16,True)
 badge(L,57);C.showPage()
 header(3,'Mission 2: Stock & Shop','Use the same market prices. Count every item once.',True)
 shelf(532)
 text(L,480,'5  Check the shelf value',18,True)
 lines(L,454,'The shelf below holds 4 apples and 3 bananas. What is their total price? Add the prices once for each item.')
 for i in range(4):obj('Apple',L+12+i*60,333,48)
 for i in range(3):obj('Banana',L+274+i*60,333,48)
 C.setLineWidth(2);C.line(L,328,W-R,328)
 box(L,218,W-L-R,90,'SHELF VALUE: ______ ¢  /  WRITE YOUR SUM HERE')
 text(L,176,'6  Find the missing receipt line',18,True)
 lines(L,150,'A receipt lists 2 carrots and 1 bread loaf. The total is 135¢. What is the carrot line total (both carrots together)?')
 text(L,82,'Carrots ______ ¢ + bread 55¢ = 135¢',17,True)
 C.showPage()
 header(4,'Finish the Shopping Mission','One careful check can catch a mixed-up receipt.')
 shelf(532)
 text(L,480,'7  Find the exact pair',18,True)
 lines(L,454,'Choose exactly TWO DIFFERENT items. Their prices must add to 75¢. Circle them on this shelf, then write their names.')
 text(L,386,'________________ + ________________ = 75¢',16,True)
 box(L,277,W-L-R,86,'CHECK YOUR PAIR: WRITE BOTH PRICES')
 text(L,235,'8  Check the final change',18,True)
 lines(L,209,'For the 135¢ receipt in Puzzle 6, pay 200¢ ($2). How much change comes back?')
 text(L,144,'135¢ + ______ ¢ = 200¢',20,True)
 lines(L,112,'Tip: count up to the next ten, then to 150¢, then to 200¢.',size=11)
 badge(L,51);C.showPage();C.save()
 C=canvas.Canvas(str(ROOT/'sample-answer-key.pdf'),pagesize=(W,H));C.setAuthor('Mira West');C.setTitle('Mini-Market Math Missions — illustrated sample answers')
 for n in [0,1]:
  text(45,752,'MINI-MARKET MATH MISSIONS • SAMPLE ANSWERS',13,True)
  text(45,718,'Mission '+str(n+1)+' • Check the evidence',22,True)
  if n==0:
   obj('Apple',52,596,66);obj('Carrot',135,596,66);text(240,620,'1: 25¢ + 40¢ = 65¢',18,True)
   text(50,555,'2: 100¢ − 65¢ = 35¢ change.',18,True)
   receipt(50,332,[('Bread',55),('Apple',25)],80)
   text(295,443,'3: Total = 80¢.',17,True)
   lines(295,402,'55 + 25 = 80. The receipt has one of each item.',240)
   text(50,278,'4: 100¢ − 80¢ = 20¢ change.',18,True)
   text(50,240,'Check: 80¢ + 20¢ = 100¢.',15)
  else:
   text(50,654,'5: Shelf value = 205¢.',18,True)
   lines(50,620,'Apples: 25 + 25 + 25 + 25 = 100¢. Bananas: 35 + 35 + 35 = 105¢. Together: 100 + 105 = 205¢.')
   receipt(50,394,[('2 carrots',80),('Bread',55)],135)
   lines(295,500,'6: Both carrots cost 80¢. 135 − 55 = 80. Check: 40 + 40 = 80.',235)
   obj('Banana',52,274,68);obj('Carrot',140,274,68)
   text(250,307,'7: Banana + carrot.',17,True);text(250,278,'35¢ + 40¢ = 75¢.',16)
   text(50,224,'8: 65¢ change.',18,True)
   lines(50,190,'Count up: 135 + 5 = 140; + 10 = 150; + 50 = 200. Change: 5 + 10 + 50 = 65¢. Check: 135 + 65 = 200.')
  text(45,58,'Check the math, not the size of the drawings. Prices include tax.',10)
  C.showPage()
 C.save()
make()
for name,count in [('sample-4-pages.pdf',4),('sample-answer-key.pdf',2)]:
 d=fitz.open(ROOT/name);assert len(d)==count
 for p in d:
  assert p.rect.width==612 and p.rect.height==792
  for b in p.get_text('blocks'):assert b[0]>=36 and b[1]>=25 and b[2]<=576 and b[3]<=767,(name,b)
 if count==4:
  from PIL import Image,ImageDraw
  sheet=Image.new('RGB',(612,792),'white')
  for i,p in enumerate(d):
   pix=p.get_pixmap(matrix=fitz.Matrix(.5,.5));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);sheet.paste(im,((i%2)*306,(i//2)*396))
  sheet.save(ROOT/'sample-preview.png')
report={'sample_pages':4,'answer_key_pages':2,'final_book_pages_planned':108,'trim_inches':[8.5,11],'bleed':False,'numbered_puzzles_in_sample':8,'full_book_puzzles_required':100,'expected_answers':[65,35,80,20,205,80,['Banana','Carrot'],65],'unique_pair_verified':pairs,'receipt_totals_verified':[80,135],'integer_cents_only':True,'text_bounds':'PASS','human_educator_review':'pending','competitor_interior_inspection':'unavailable; see RESEARCH.md'}
(ROOT/'validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
