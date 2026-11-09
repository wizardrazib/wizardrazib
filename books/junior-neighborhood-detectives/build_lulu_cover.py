"""Create Lulu cover from existing vector cover, preserving original source files.
Run with Python + PyMuPDF + Pillow. Supplied inch dimensions are authoritative;
metric figures in the user template are rounded equivalents.
"""
from pathlib import Path
import json,hashlib
import pymupdf as fitz
from PIL import Image
R=Path(__file__).resolve().parent
INCH=72
WIDTH,HEIGHT=17.58*72,11.25*72
BLEED=.125*72;TRIM_W=8.5*72;TRIM_H=11*72;SPINE=.33*72;SAFE=.5*72
assert abs(WIDTH-(2*TRIM_W+SPINE+2*BLEED))<1e-7
source=fitz.open(R/'cover-full-wrap.pdf');s=source[0]
navy=(20/255,53/255,74/255);teal=(25/255,185/255,176/255)
# Paint over the old KDP barcode reserve before vector placement. Original file
# remains unchanged. PDF's top-left coordinate system requires y conversion.
s.draw_rect(fitz.Rect(430,s.rect.height-115.4,578,s.rect.height-25),color=None,fill=navy,overlay=True)
old_front_x=(.125+8+120*.002252)*72
back_clip=fitz.Rect(9,9,585,s.rect.height-9)
front_clip=fitz.Rect(old_front_x,9,old_front_x+576,s.rect.height-9)
back_trim=fitz.Rect(BLEED,BLEED,BLEED+TRIM_W,BLEED+TRIM_H)
front_x=BLEED+TRIM_W+SPINE
front_trim=fitz.Rect(front_x,BLEED,front_x+TRIM_W,BLEED+TRIM_H)
back_safe=fitz.Rect(back_trim.x0+SAFE,back_trim.y0+SAFE,back_trim.x1-SAFE,back_trim.y1-SAFE)
front_safe=fitz.Rect(front_trim.x0+SAFE,front_trim.y0+SAFE,front_trim.x1-SAFE,front_trim.y1-SAFE)
doc=fitz.open();p=doc.new_page(width=WIDTH,height=HEIGHT)
p.draw_rect(p.rect,color=None,fill=navy)
p.draw_rect(fitz.Rect(front_x,0,WIDTH,HEIGHT),color=None,fill=teal)
# Keep the original vector text and graphics at fixed aspect ratio. All original
# panel content is inset inside Lulu's conservative 0.5-inch safe rectangles.
p.show_pdf_page(back_safe,source,0,clip=back_clip,keep_proportion=True)
p.show_pdf_page(front_safe,source,0,clip=front_clip,keep_proportion=True)
# Cover fine source-form clipping seams with matching panel color; all content
# sits well inside these sub-point perimeter strips.
for safe,fill in [(back_safe,navy),(front_safe,teal)]:
    fitted_h=540*720/576
    rect=fitz.Rect(safe.x0,safe.y0+(safe.height-fitted_h)/2,safe.x1,safe.y1-(safe.height-fitted_h)/2)
    for edge in [fitz.Rect(rect.x0-.5,rect.y0-.5,rect.x0+.7,rect.y1+.5),fitz.Rect(rect.x1-.7,rect.y0-.5,rect.x1+.5,rect.y1+.5),fitz.Rect(rect.x0-.5,rect.y0-.5,rect.x1+.5,rect.y0+.7),fitz.Rect(rect.x0-.5,rect.y1-.7,rect.x1+.5,rect.y1+.5)]:
        p.draw_rect(edge,color=None,fill=fill,overlay=True)
# New clean, actual-size barcode reserve, lower-right back cover, at least
# 0.5 inch from BOTH trim edges (0.625 inch from outer document/bleed edges).
BW,BH=3.622*72,1.26*72
barcode=fitz.Rect(back_trim.x1-SAFE-BW,HEIGHT-(BLEED+SAFE+BH),back_trim.x1-SAFE,HEIGHT-(BLEED+SAFE))
p.draw_rect(barcode,color=None,fill=(1,1,1),overlay=True)
p.set_trimbox(fitz.Rect(BLEED,BLEED,WIDTH-BLEED,HEIGHT-BLEED))
p.set_bleedbox(p.rect)
doc.set_metadata({'title':'Junior Neighborhood Detectives — Lulu Full-Wrap Cover','author':'Mira West','subject':'120 pages; 8.5 x 11 inch trim; supplied Lulu cover geometry'})
output=R/'lulu-cover-full-wrap.pdf';doc.save(output,garbage=4,deflate=True)
# Reopen final file for verification and exports.
check=fitz.open(output);page=check[0]
assert len(check)==1 and abs(page.rect.width-WIDTH)<.001 and abs(page.rect.height-HEIGHT)<.001
for b in page.get_text('blocks'):
 rect=fitz.Rect(b[:4])
 assert back_safe.contains(rect) or front_safe.contains(rect),(rect,'text outside safe panel')
 assert not rect.intersects(barcode),(rect,'barcode overlap')
assert barcode.x0>=36 and HEIGHT-barcode.y1>=36
assert abs(barcode.width/72-3.622)<1e-7 and abs(barcode.height/72-1.26)<1e-7
# Ensure that the printed barcode zone is truly blank white, not merely a label.
pix=page.get_pixmap(clip=barcode+(1,1,-1,-1),colorspace=fitz.csRGB)
assert all(v==255 for v in pix.samples)
page.get_pixmap(dpi=300).save(R/'lulu-cover-full-wrap-300dpi.png')
im=Image.open(R/'lulu-cover-full-wrap-300dpi.png');im.save(R/'lulu-cover-full-wrap-300dpi.png',dpi=(300,300))
page.get_pixmap(matrix=fitz.Matrix(.75,.75)).save(R/'lulu-cover-preview.png')
report={'document_inches':[17.58,11.25],'document_points':[WIDTH,HEIGHT],'trim_inches':[8.5,11],'page_count_for_template':120,'spine_inches':.33,'bleed_inches':.125,'minimum_important_content_inset_inches':.5,'back_safe_rect_points':list(back_safe),'front_safe_rect_points':list(front_safe),'barcode_inches':[3.622,1.26],'barcode_pdf_top_left_rect_points':list(barcode),'barcode_bottom_and_right_trim_clearance_inches':.5,'barcode_bottom_document_clearance_inches':.625,'barcode_zone_blank_white_verified':True,'text_safe_rect_check':'PASS','vector_source_preserved':True,'fonts_embedded_from_source':True,'raster_companion_dpi':300,'raster_pixels':list(im.size),'interior_unchanged':True,'interior_mismatch':'Existing interior is 8 x 10 inches; supplied Lulu cover is for 8.5 x 11 inches. A matching interior is required.','lulu_upload_acceptance':'Not tested; no actual template file or account upload supplied.'}
(R/'lulu-cover-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
