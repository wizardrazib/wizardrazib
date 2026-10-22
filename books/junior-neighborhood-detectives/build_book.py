from pathlib import Path
import json, hashlib, math, itertools
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, black, white
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('Body',FONT));pdfmetrics.registerFont(TTFont('Bold',BOLD))
# Each case supplies all evidence, three activities, graduated hints, and reasoning.
C=[]
def case(title,story,evidence,tasks,answers,hints,boundary,close):
 C.append(dict(id=len(C)+1,title=title,story=story,evidence=evidence,tasks=tasks,answers=answers,hints=hints,boundary=boundary,close=close))
case('The Three Garden Pots',
'The neighborhood fair opens tomorrow. Maya, Sam, and Jo have three pots ready for the garden table. But their name cards are on the floor. “Mine had a circle sticker,” says Maya. “Mine did not have a triangle sticker,” says Sam. “Let’s write that down,” says Jo. Each child owns exactly one pot. Each pot belongs to exactly one child. All three remember correctly.',
['Pot A: circle sticker; height 8 centimeters.','Pot B: triangle sticker; height 12 centimeters.','Pot C: square sticker; height 10 centimeters.','Stickers and heights have not changed. Height is measured from table to rim. A centimeter measures length. Use these recorded numbers.'],
['Match Maya, Sam, and Jo to pots A, B, and C. Write each name and pot letter.', 'Put the pot letters in order from shortest to tallest. Whose pot is tallest? Does it have the triangle sticker?', 'Jo says Sam cannot own A even though it is not a triangle. Why? Choose: A already belongs to Maya / Sam dislikes circles / A is too short. Explain your evidence.'],
['Maya owns A, Sam owns C, and Jo owns B. Maya’s circle fixes A. Sam cannot take B or the already assigned A. Jo gets B.', 'A, C, B: 8 is less than 10, and 10 is less than 12. Jo’s pot is tallest. Yes, it has the triangle.', 'A already belongs to Maya. Shape preferences and required heights were never given.'],
['Start with Maya’s exact sticker.','After A is assigned, Sam must choose between B and C. Which is not a triangle?'],
'Pot height is not plant height. A taller pot does not prove that its plant is older or healthier.',
'The cards fell down. Nobody needed to be blamed. Sam copies the list so the club has a backup.')
case('The Morning Deliveries','Three helpers brought one item each. Jo wants to thank them in the right order. “I wrote the clues,” says Maya. Nobody has to guess.',
['The deliveries were a watering can, a seed bag, and a sign. Each arrived once.','The seed bag arrived after the watering can.','The sign arrived before the watering can.'],
['Write the items in delivery order: first, second, third.','Which arrived just before the seed bag?','Sam says the seed bag arrived first. Which clue rules that out?'],
['Sign, watering can, seed bag. The can must be between the other two items.','The watering can.','The seed bag arrived after the watering can, so it cannot be first.'],['Find the item that has something before it and after it.','Put the can in the middle.'], 'An order tells us before and after. It does not tell us the number of minutes between deliveries.','Jo writes three thank-you notes. Every delivery helped.')
case('Labels in the Seed Tray','The club has three labeled envelopes. The plants have not grown yet. “We can use the labels,” says Sam. “We cannot identify a plant from a bare pot.”',
['Tray positions are left, middle, right. Each holds one envelope: bean, pea, or sunflower.','The bean is not in the middle or on the right.','The pea is immediately to the right of the sunflower.'],
['Place all three envelope names in the tray.','Which envelope is between the other two?','Can these clues tell us which seed will sprout first? Explain.'],
['Left: bean. Middle: sunflower. Right: pea. Bean must be left; the remaining adjacent order is sunflower then pea.','Sunflower.','No. The clues give positions, not germination times or growing conditions.'],['Use both places that bean cannot occupy.','Only middle and right remain for sunflower and pea.'], 'A label is a record. It is not proof that a seed has sprouted.', 'The envelopes stay closed. The club saves planting for a grown-up-led activity.')
case('The Tool Hooks','Three safe garden tools hang on numbered hooks. Their record cards fell off. Maya checks the club notebook.',
['Hooks 1, 2, and 3 each hold exactly one item: brush, scoop, or watering can.','The brush is on an odd-numbered hook. Odd hooks here are 1 and 3.','The watering can is on hook 1.'],
['Match each item to its hook.','Which item is on hook 2?','If the brush were on hook 1, which stated rule would be broken?'],
['Can on 1, scoop on 2, brush on 3. Hook 1 is taken, so brush uses the other odd hook.','Scoop.','Each hook holds one item; hook 1 already holds the can.'],['Assign the watering can first.','Which odd hook is still free?'], 'We can reason from a complete inventory. With an unlisted extra tool, we would need more information.', 'Jo clips the copied record above the hooks.')
case('The Shadow Screen','A grown-up made three shadow tests for the fair. The club reads the records. No lamp or experiment is needed.',
['Only one opaque card was used in each test. Opaque means light does not pass through it.','Test A: circle card. Test B: triangle card. Test C: square card.','In this setup, each card faced the lamp and made the matching outline on the screen.','The saved outline has exactly three straight sides.'],
['Which test made the saved outline?','How many straight sides distinguish the square from the triangle here?','Would this record tell us the real size of the card? Explain.'],
['B. A triangle has three straight sides.','A square has four; a triangle has three. The difference is one side.','No. The record gives shape, not card dimensions or lamp distances.'],['Count sides rather than guessing from a name.','Compare three sides with the shapes listed.'], 'Shadow size depends on the setup. This simplified record establishes shape, not size.', 'The club adds a clear label to the shadow display.')
case('Mirror Messages','Sam invents a paper mirror code. “This is a rule in our notebook,” he says. “You do not need a real mirror.”',
['The code reverses the ORDER of letters, not the shape of each letter.','Example: POT becomes TOP.','The label reads: XOB.','The three storage choices are BOX, BAG, and TIN.'],
['Decode XOB. Which storage choice matches?','Encode BAG with the same rule.','Jo writes POT as OPT. Does that follow the rule? Explain.'],
['BOX. Read XOB from its last letter to its first.','GAB.','No. Reversing all three letters gives TOP, not OPT.'],['Start at the right-hand end.','X is the last letter after decoding.'], 'This is a letter-order code. A real mirror also reverses letter shapes, which this puzzle does not simulate.', 'Maya labels it “reverse-order code” so nobody mistakes it for a real mirror test.')
case('Light Through the Window','Jo compares saved light-test cards. An adult used the same lamp and detector setting each time. The club reads the observations.',
['Card A: clear sheet; lamp clearly visible through it.','Card B: tracing sheet; light patch visible, but lamp outline unclear.','Card C: thick card; lamp light blocked in this test.','For this puzzle: transparent = clear view; translucent = blurred light; opaque = blocks the light.'],
['Match transparent, translucent, and opaque to A, B, and C.','Which card lets light through without a clear view?','Sam wants to claim every thin sheet is transparent. Do these three observations prove that?'],
['A transparent, B translucent, C opaque, using the supplied definitions.','B, the tracing sheet.','No. Thickness alone is not the tested rule, and only these three samples were observed.'],['Use the supplied definitions.','A clear view differs from a patch of light.'], 'Material, thickness, and conditions matter. Describe these samples rather than every possible sheet.', 'The display gets three observation labels instead of a big guess.')
case('A Shadow That Changed','Maya finds three photos of one display. The club does not need to recreate them.',
['Same card, screen, and lamp setting in all three tests. Only the card’s position between lamp and screen changed.','Position A, nearest lamp: recorded shadow height 18 cm.','Position B, middle: 12 cm.','Position C, nearest screen: 6 cm.'],
['Order A, B, and C from smallest recorded shadow to largest.','How much taller is A’s shadow than B’s?','Did the card itself grow between tests? What fact supports your answer?'],
['C, B, A: 6, 12, 18 cm.','6 cm, because 18 minus 12 is 6.','No. The record explicitly says the same card was used and only its position changed.'],['Use the shadow heights, not alphabetical order.','Compare the largest and middle numbers by subtraction.'], 'These results apply to the stated setup. They do not tell clock time or show an object growing.', 'Jo adds “same card” beneath the photos. That detail matters.')
case('The Magnet Record','A grown-up tested three sealed display samples. The children only read the results. “Let’s not guess from the shiny surface,” says Jo.',
['Each sample was tested three times with the same magnet and setup.','Sample A: moved toward magnet in all three tests.','Sample B: did not move in all three tests.','Sample C: moved toward magnet in all three tests.','The mystery card belongs to a sample that did NOT move.'],
['Which sample matches the mystery card?','Which TWO samples behaved alike?','Does a shiny appearance prove a material will move toward this magnet? Explain using the record’s limits.'],
['B is the only sample recorded as not moving.','A and C both moved in all three tests.','No. No appearance comparison was recorded, and not every shiny material behaves alike.'],['Look for NOT move.','Compare all three repeats for each sample.'], 'Do not handle small magnets. These observations do not identify exact metals or prove that all metals are magnetic.', 'The club uses test results rather than sparkle to label the card.')
case('The Mixed-Up Cup Cards','The science table has sealed observation cards, not cups to taste. Sam sorts the results from an adult’s test.',
['All tests used equal water amounts, the same temperature, and one minute of stirring.','Card A: added sugar; no grains visible afterward.','Card B: added sand; grains still visible at the bottom.','Card C: added salt; no grains visible afterward.','The lost label says: “Grains still visible after stirring.”'],
['Which card needs the lost label?','Which cards describe the same visible result?','Can “no grains visible” prove that nothing is in the water? Explain.'],
['B, the sand observation.','A and C.','No. Something can dissolve and still be present even when separate grains are not visible.'],['Read the last line of each test.','Two records say no grains were visible; one says they remained.'], 'Never taste an unknown liquid. The book uses records only; invisible does not mean absent or safe.', 'Jo adds the word “visible” to the display. It makes the observation more careful.')
case('The Paper Bridge','Three paper bridges were tested by an adult. Maya studies the records before choosing a photo for the fair.',
['Same paper size, support gap, and identical small weights. Only fold pattern changed.','A: flat sheet; held 2 weights before bending.','B: zigzag fold; held 8.','C: curved fold; held 5.','For this display, choose the tested pattern that held the MOST weights.'],
['Which pattern should the club show?','How many more weights did B hold than A?','Sam says B will hold the most in every possible bridge test. Is that established?'],
['B, the zigzag fold, held 8, the largest count.','6 more: 8 minus 2.','No. These tests cover only the supplied materials, gap, and weights. Different conditions need testing.'],['Compare 2, 8, and 5.','The choice is about this test, not every bridge.'], 'These are model records, not instructions for a bridge people can stand on.', 'The club shows the conditions beside the winning photo.')
case('The Rolling Record','A grown-up released the same toy car from the same ramp mark onto three labeled surfaces. Jo reads the measured distances.',
['A: 30 cm. B: 18 cm. C: 24 cm.','Same car, ramp mark, measuring method, and no push. Only the surface changed.','The record does not name the surface materials.'],
['Which surface had the longest recorded roll?','Order the surfaces from shortest roll to longest.','Can you identify which surface was carpet from these numbers alone? Explain.'],
['A, with 30 cm.','B, C, A: 18, 24, 30 cm.','No. The materials are not named; a distance does not uniquely identify a material.'],['Longest means the largest distance.','Do not add a material name that is missing from the evidence.'], 'A fair comparison keeps listed conditions alike. A single set of results does not establish every future roll.', 'Sam writes “surface names needed” rather than inventing them.')
case('The Delivery Map','The club’s map is a small square. Maya wants the shortest route on the marked paths. Each path takes one step.',
['Four places: Gate (top left), Library (top right), Garden (bottom left), Hall (bottom right).','Paths: Gate–Library, Gate–Garden, Library–Hall, Garden–Hall. Paths work both ways. No diagonal paths.','The Gate–Library path is closed.','Start at Gate and finish at Hall.'],
['Write the shortest open route.','How many steps does that route take?','Does a route through Library work without first reaching Hall? Explain.'],
['Gate → Garden → Hall.','Two steps. There is no direct Gate–Hall path.','No. The direct Gate–Library path is closed. Reaching Library from Gate requires passing through Hall first.'],['Cross out the closed path.','Gate has just one open exit.'], 'This is a fictional map, not a real travel route. Stay with a trusted adult outdoors.', 'Jo draws the open route on the fair’s delivery card.')
case('The Sticker Chart','Sam made a chart of puzzle votes. Each child voted exactly once. “Read the key first,” says Maya.',
['Key: each star stands for 2 votes. These are full stars only.','Garden puzzles: 3 stars.','Light puzzles: 2 stars.','Map puzzles: 4 stars.'],
['How many votes did each kind receive?','How many votes were cast altogether?','Which kind won, and by how many votes over the runner-up?'],
['Garden 6, Light 4, Map 8. Multiply each star count by 2.','18: 6 + 4 + 8.','Map won with 8, two more than Garden’s 6.'],['One star means two votes, not one.','Runner-up is the second-largest total.'], 'This chart describes these voters only. It does not prove what every child prefers.', 'The club keeps every kind of puzzle. A vote is not a reason to exclude anyone.')
case('The Quiet Setup Slot','The fair helpers need a quiet time together. Jo checks their schedules. All times below are in the morning.',
['Maya is free 9:00–10:00.','Sam is free 9:30–10:30.','Jo is free 9:15–9:45.','They need 15 whole minutes when all three are free.'],
['What is the shared interval when all three are free?','Does 9:15–9:30 work? Why or why not?','Does 9:30–9:45 give all 15 minutes?'],
['9:30–9:45. The latest start is 9:30 and earliest finish is 9:45.','No. Sam is not free until 9:30.','Yes. All three are free throughout that 15-minute interval.'],['Start no earlier than the latest person’s start.','Finish no later than the earliest person’s finish.'], 'This puzzle uses stated schedules. It does not ask you to infer travel time.', 'Maya puts the agreed time on the club card.')
case('The Symbol Key','A box label uses Jo’s invented picture code. Sam has the full key. No outside code knowledge is needed.',
['Circle = B. Triangle = A. Square = G. Star = T.','A sequence is read from left to right.','Label: circle, triangle, square.'],
['Decode the label.','Encode BAT by writing the three symbol names in order.','Does square, triangle, circle spell the same word as the label? Explain.'],
['BAG. Replace each symbol with its key letter.','Circle, triangle, star.','No. It spells GAB. Order changes the result.'],['Replace one symbol at a time.','Do not reverse the sequence.'], 'This is an invented substitution key, not a secret language or a scientific measurement.', 'The club puts the key beside the label so every helper can read it.')
case('The Fair Crate Route','Fair day arrives. A crate of display cards is at the Gate. A helper needs it at the Hall. The club checks the route card.',
['Places in a line: Gate — Garden — Hall — Library.','Only neighboring places are connected. Each path takes one step, both ways.','The Garden–Hall path is open. All other shown paths are also open.','The crate was moved exactly two steps, without turning back, starting at Gate.'],
['Where is the crate now?','Which place did it pass through?','Could it be at Library after only two steps? Show the needed step count.'],
['Hall: Gate to Garden is one, Garden to Hall is two.','Garden.','No. Gate to Library needs three steps along this line.'],['Trace one path for each step.','Count edges, not the number of place names.'], 'Recap for this linked chapter: the display crate is at Hall. Later cases state any facts they need again.', 'The crate is safe at Hall. Next, the club will sort the display cards.')
case('The Three Display Cards','The crate at Hall holds three display cards. Their fronts look alike. The notebook lists test results, so nobody has to open the sealed samples.',
['Red-label card: sample moved toward the magnet.','Blue-label card: sample did not move toward the magnet.','Green-label card: sample moved toward the magnet.','The labels have their color NAMES printed in words.','The fair’s magnet display needs the one card whose sample did NOT move.'],
['Which label belongs on that display?','Which two labels have matching results?','Does this establish that the blue-label sample is plastic? Explain.'],
['Blue-label card. It is the only non-moving result.','Red-label and Green-label.','No. Many materials may give that result. The record does not identify the sample.'],['Use the words moved and did not move.','A behavior can rule out a match without naming the material.'], 'No actual magnets are needed. Label color does not cause the recorded behavior.', 'The blue-label card goes to the display. Its material stays unnamed.')
case('The Missing Name Strip','The Hall table has three finished exhibits. Each child made one. Their name strips slipped into an envelope. Jo reads the notes.',
['Exhibits: bridge, map, shadow. Each belongs to exactly one of Maya, Sam, and Jo.','Maya made the map.','Sam did not make the bridge.','All notes are correct.'],
['Match each child to an exhibit.','Which exhibit belongs to Jo?','Sam says Jo made the shadow. Which two clues together show that cannot work?'],
['Maya: map. Sam: shadow. Jo: bridge.','Bridge.','Maya already has map; Sam cannot have bridge, so Sam must have shadow. One-to-one ownership leaves bridge for Jo.'],['Assign Maya first.','Of bridge and shadow, which can Sam take?'], 'These notes establish ownership for this case. Do not infer skill or preferences from who made an exhibit.', 'The names go back beside the exhibits. Everyone’s work gets credit.')
case('The Fair Can Open','One final delivery card is missing its destination. The club puts together all the facts. Each fact below is enough to check without returning to earlier pages.',
['Stops in order: Gate — Garden — Hall — Library. Each neighboring path is one step, both ways.','The delivery started at Gate and moved exactly two steps without turning back.','The parcel holds the bridge exhibit. Jo made the bridge.','The recorded bridge test held 8 weights; the flat-sheet test held 2 under the same stated setup.'],
['Where is the parcel, and whose exhibit is inside?','How many more weights did the recorded bridge test hold than the flat-sheet test?','Write one conclusion you CAN support and one thing you CANNOT know from this record.'],
['At Hall, with Jo’s bridge. Two steps along the line reach Hall; ownership is explicitly supplied.','6 more: 8 minus 2.','Example supported: the parcel reached Hall. Example unknown: its arrival time. Other answers are valid if they respect the record. This last prompt intentionally allows several explanations.'],['Count from Gate: Garden is one step.','Use only the stated facts. No arrival time appears.'], 'A supported conclusion can be firm while other facts remain unknown. The open explanation task has more than one valid response.', 'The fair opens. Maya, Sam, and Jo thank the helpers. “Best clue today?” asks Sam. “Checking before guessing,” says Jo.')
assert len(C)==20
# Text fits are checked rather than silently clipped.
W,H=576,720
md=[]; page=0; pdf=canvas.Canvas(str(OUT/'interior.pdf'),pagesize=(W,H))
pdf.setTitle('Junior Neighborhood Detectives');pdf.setAuthor('Mira West')
def wrap(text,font,size,width):
 lines=[]
 for para in text.split('\n'):
  line=''
  for word in para.split():
   trial=(line+' '+word).strip()
   if pdfmetrics.stringWidth(trial,font,size)>width:
    if line:lines.append(line)
    line=word
   else:line=trial
  lines.append(line)
 return lines

def drawpage(title,blocks,space=False):
 global page
 page+=1; inside=45; outside=36
 left=inside if page%2 else outside; right=outside if page%2 else inside
 width=W-left-right; y=H-45
 pdf.setFillColor(black)
 for line in wrap(title,'Bold',21,width):
  pdf.setFont('Bold',21);pdf.drawString(left,y,line);y-=28
 y-=14
 md.append(f'\n## Page {page}: {title}\n')
 for block in blocks:
  md.append(block+'\n')
  for line in wrap(block,'Body',14,width):
   if y<64:raise ValueError(f'Overflow page {page}: {title}')
   pdf.setFont('Body',14);pdf.drawString(left,y,line);y-=21
  y-=15
 if space:
  pdf.setStrokeColor(HexColor('#999999'));pdf.setLineWidth(.6)
  for yy in range(int(y-14),78,-27):pdf.line(left,yy,W-right,yy)
 pdf.setFont('Body',9);pdf.drawString(left,29,'JUNIOR NEIGHBORHOOD DETECTIVES');pdf.drawRightString(W-right,29,str(page))
 pdf.showPage()
front=[('Junior Neighborhood Detectives',['Science Clues & Logic Cases for Ages 7–9','Mira West','Twenty friendly cases. Observe. Check. Explain.']),
('Copyright',['Junior Neighborhood Detectives','Science Clues & Logic Cases for Ages 7–9','Copyright © 2026 Mira West','All rights reserved. Except as permitted by applicable law, no part of this book may be reproduced, stored, or transmitted in any form without prior written permission from the copyright holder.','First edition, 2026.','This is a work of fiction. Names, characters, places, and events are imaginary. Any resemblance to actual persons or events is coincidental.','Activities are intended for educational entertainment. Use the supplied records; no physical experiments are required. Children should ask a trusted adult for help when needed.']),
('Welcome to the club',['A clue is something you can check. A guess is an idea you have not checked yet.','Good detectives use both. They make a guess, look at the clues, and change their minds when they need to.','Maya likes to look closely. Sam likes to try an idea. Jo asks, “Could another answer fit?” You can do all three.','Our club rule: solve the mix-up, not blame a person.']),
('Your detective toolkit',['Use a pencil and an eraser. Write, circle, or draw an answer. Ask a grown-up to read with you if you like.','Each case has four pages: read the story, investigate, check, and explain. Take a break whenever you want.','Hints begin on page 89. Explained answers begin on page 99. Help is not a penalty.','You can skip a case. The final chapter repeats every fact it needs.']),
('Keep investigations safe',['Use the printed records. Do not taste unknown liquids, touch unknown plants, handle small magnets, or test electricity or heat.','Never follow a clue into an unfamiliar place. Stay with a trusted grown-up outdoors.','Some records describe tests done by an adult. You are reading those results, not being asked to do the experiment.','A wrong guess is not a bad person. Check the evidence and try again.']),
('Words that help',['Observe: notice something carefully. Record: save what was observed.','Evidence: information that helps answer a question. Compare: look for differences or similarities.','Eliminate: rule out a choice using a clue. Explain: say why the evidence fits.','A fair comparison changes one thing while keeping the other listed conditions alike.']),
('Try one together',['Two envelopes are marked A and B. One holds a circle card; the other holds a square card. The note says A holds the square.','Question: Where is the circle?','Work it out: A is taken by the square. Each envelope holds just one card. B is the only place left.','Answer: the circle is in B. Notice that we did not guess from envelope size or color. We used the note and the one-card rule.']),
('Your case map',['Garden Mix-Ups: cases 1–4, pages 9–24.','Light on the Clues: cases 5–8, pages 25–40.','Test the Idea: cases 9–12, pages 41–56.','Routes and Records: cases 13–16, pages 57–72.','The Fair Display Mix-Up: cases 17–20, pages 73–88.','Hint desk: 89–98. Answer desk: 99–118. Reflection and feedback: 119–120.'])]
for t,b in front:drawpage(t,b)
for c in C:
 prefix=f'Case {c["id"]}: {c["title"]}'
 drawpage(prefix,[c['story']]+c['evidence'])
 drawpage('Investigate',[f'Case {c["id"]} • Activity 1',c['tasks'][0],'Use this space for your matches, notes, or drawing.'],True)
 drawpage('Check the clues',[f'Case {c["id"]} • Activity 2',c['tasks'][1],'Which number, record, or rule helped you?'],True)
 drawpage('Explain and close',[f'Case {c["id"]} • Activity 3',c['tasks'][2],c['close'],'Think carefully: '+c['boundary']],True)
for i in range(0,20,2):
 blocks=[]
 for c in C[i:i+2]:blocks += [f'Case {c["id"]}: {c["title"]}', 'Hint 1: '+c['hints'][0], 'Hint 2: '+c['hints'][1]]
 drawpage('Hint desk',blocks)
for c in C:
 drawpage(f'Answers • Case {c["id"]}',[c['title']]+[f'Activity {i+1}: {a}' for i,a in enumerate(c['answers'])]+['Careful thinking: '+c['boundary']])
drawpage('Your detective reflection',['Which case made you change your mind? What clue helped?','Which did you enjoy most: matching, measurement, maps, codes, or testing an explanation?','Draw yourself checking a clue. You do not need a badge to think carefully.'],True)
drawpage('A note for grown-ups',['Read instructions together if helpful. Praise a clear explanation, not speed. Accept equivalent answers supported by the evidence.','The last case includes an open explanation task. The answer desk gives an example, not the only valid response.','Ask: What do you know? What are you guessing? What evidence would change your mind?','For development feedback, note the case number, confusing instruction, assistance needed, and any other answer that fits. Do not record identifying child information in a shared file.','Thank you for helping a young detective think with care.'])
assert page==120
pdf.save()
(OUT/'manuscript.md').write_text('# Junior Neighborhood Detectives\n\nMira West\n\n'+ '\n'.join(md))
(OUT/'cases.json').write_text(json.dumps(C,indent=2,ensure_ascii=False))
# Full-wrap cover: locally drawn original vector art, no stock or image service.
spine=120*.002252; cw=16.25+spine; ch=10.25
cv=canvas.Canvas(str(OUT/'cover-full-wrap.pdf'),pagesize=(cw*72,ch*72));cv.setTitle('Junior Neighborhood Detectives — cover');cv.setAuthor('Mira West')
navy=HexColor('#133449');teal=HexColor('#187F83');gold=HexColor('#F7CB57')
cv.setFillColor(navy);cv.rect(0,0,cw*72,ch*72,fill=1,stroke=0)
fx=(.125+8+spine)*72
cv.setFillColor(teal);cv.rect(fx,0,8.125*72,ch*72,fill=1,stroke=0)
cv.setFillColor(gold);cv.roundRect(fx+32,590,512,100,12,fill=1,stroke=0)
cv.setFillColor(navy);cv.setFont('Bold',30)
cv.drawString(fx+47,650,'JUNIOR NEIGHBORHOOD');cv.drawString(fx+47,610,'DETECTIVES')
cv.setFillColor(white);cv.setFont('Bold',19);cv.drawString(fx+42,550,'Science Clues & Logic Cases')
cv.setFont('Body',17);cv.drawString(fx+42,520,'FOR AGES 7–9')
# original notebook and three clue cards
cv.setFillColor(HexColor('#FFF9E8'));cv.roundRect(fx+70,165,360,290,14,fill=1,stroke=0)
cv.setStrokeColor(teal);cv.setLineWidth(2)
for yy in range(210,420,35):cv.line(fx+105,yy,fx+395,yy)
cv.setFillColor(navy);cv.setFont('Bold',23);cv.drawString(fx+110,410,'LOOK. CHECK. EXPLAIN.')
cv.setStrokeColor(gold);cv.setLineWidth(14);cv.circle(fx+360,305,62,fill=0,stroke=1);cv.line(fx+403,260,fx+470,190)
cv.setFillColor(teal);cv.circle(fx+150,320,18,fill=1,stroke=0)
cv.rect(fx+200,300,35,35,fill=1,stroke=0)
p=cv.beginPath();p.moveTo(fx+125,235);p.lineTo(fx+145,270);p.lineTo(fx+165,235);p.close();cv.drawPath(p,fill=1,stroke=0)
cv.setFillColor(white);cv.setFont('Bold',24);cv.drawString(fx+42,80,'MIRA WEST')
cv.setFont('Bold',24);cv.drawString(40,650,'Small mix-ups. Big thinking.')
back=['A name card falls. A record gets mixed up.','A fair display needs one final clue.','Join Maya, Sam, and Jo for twenty friendly','cases about a neighborhood getting ready','for its community fair.','Use maps, measurement records, simple codes,','and logic to work out what happened.','All the evidence is on the page.','No experiments or special supplies needed.','Includes optional hints and explained answers.']
cv.setFont('Body',17)
for i,line in enumerate(back):cv.drawString(40,590-i*29,line)
cv.setFillColor(gold);cv.setFont('Bold',18);cv.drawString(40,205,'Solve the mix-up. Not blame a person.')
# Unprinted white barcode zone, to be confirmed against final official template.
cv.setFillColor(white);cv.rect(6*72, .375*72,2*72,1.2*72,fill=1,stroke=0)
cv.save()
# 300-DPI front and full-wrap raster companions, using the installed local renderer.
import fitz
with fitz.open(OUT/'cover-full-wrap.pdf') as rendered:
 rendered[0].get_pixmap(dpi=300).save(str(OUT/'cover-full-wrap-300dpi.png'))
im=Image.open(OUT/'cover-full-wrap-300dpi.png')
im.save(OUT/'cover-full-wrap-300dpi.png',dpi=(300,300))
x=round((.125+8+spine)*300); y=round(.125*300)
im.crop((x,y,x+2400,y+3000)).save(OUT/'cover-front-300dpi.png',dpi=(300,300))
# Optional alternate renderer.
import shutil,subprocess
if shutil.which('pdftoppm'):
 subprocess.run(['pdftoppm','-r','300','-singlefile','-png',str(OUT/'cover-full-wrap.pdf'),str(OUT/'cover-full-wrap-300dpi')],check=True)
 im=Image.open(OUT/'cover-full-wrap-300dpi.png'); im.save(OUT/'cover-full-wrap-300dpi.png',dpi=(300,300))
 x=round((.125+8+spine)*300); y=round(.125*300)
 im.crop((x,y,x+2400,y+3000)).save(OUT/'cover-front-300dpi.png',dpi=(300,300))
# Verify determinate assignments and key arithmetic, not all prose or scientific validity.
assert [p for p in itertools.permutations('ABC') if p[0]=='A' and p[1]!='B']==[('A','C','B')]
assert 18-12==6 and 8-2==6 and 6+4+8==18
report={'interior_pages_generated':page,'trim_inches':[8,10],'interior_bleed':False,'cover_inches':[cw,ch],'spine_inches':spine,'core_activities':60,'case_count':20,'raster_cover_created':(OUT/'cover-full-wrap-300dpi.png').exists(),'checks':'Pagination, text block vertical fit, selected logic and arithmetic assertions passed. Not an independent editorial/science review.','release_status':'Copyright page finalized. Local print formatting checked; independent review, official cover-template verification, KDP Previewer and physical proof remain required.'}
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
