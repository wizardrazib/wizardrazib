# Mini-Market Math Missions — complete print-formatted edition

**Title:** Mini-Market Math Missions  
**Subtitle:** 100 Fun Math & Logic Puzzles for Kids Ages 7-9  
**Author:** Mira West

## Main files

- `interior.pdf`: complete 108-page, 8.5 × 11-inch, black-and-white, no-bleed interior with embedded DejaVu text and original vector drawings.
- `cover-full-wrap.pdf`: print master, back + spine + front, with 0.125-inch outer bleed and clear 2 × 1.2-inch back barcode reserve.
- `cover-full-wrap-300dpi.png`: 5248 × 3375-pixel companion at 300 DPI.
- `cover-front-300dpi.png`: 2550 × 3300-pixel trim-only front companion at 300 DPI.
- `answer-key.pdf`: the full 50-page key extracted from the interior, for separate reference. This is NOT an additional part to upload: the key is already inside the 108 pages.
- `METADATA.md`: copy-ready KDP title, subtitle, HTML description, keyword fields and suggested categories.
- `puzzles.json`: all mission price records, 100 questions, expected answers and explanations.
- `manuscript.md`: searchable question/answer handoff; the PDF is the complete edition including all front/back matter.
- `validation.json`: actual local checks and outstanding external checks.
- `build_book.py`, `requirements.txt`: local rebuild source and installed package versions. A rebuild writes to a `release/` subfolder relative to the script location.
- `interior-contact-sheet.jpg`, `preview-page-*.png`, `cover-preview.png`: inspection companions, not upload files.

## Pagination

7 front-matter pages + 50 activity pages + 50 illustrated answer pages + 1 closing page = 108 pages.

The 25 two-page missions run from even page 8 to odd page 57, so each is a true left/right facing spread. Four distinct numbered puzzles per mission = exactly 100. Six departments and 24 product illustrations. A Mission Complete color-in star appears on every mission's right-hand page. Front matter and solutions are not counted as additional puzzles.

## Cover dimensions

White paper / black ink assumption: spine = 108 × 0.002252 = 0.243216 inch.
Width = 8.5 + 8.5 + 0.243216 + 0.25 = 17.493216 inches.
Height = 11 + 0.25 = 11.25 inches.
Vector PDFs have no fixed DPI; raster companions are exported at 300 DPI. No spine text is used. Confirm these assumptions against the current official KDP cover template before upload.

## Local validation

All 108 pages rendered; all text bounds checked. Arithmetic, repeated sums, receipt totals, missing receipt lines, exact-pair uniqueness, budget limits and change values checked with independent typed calculations. Every answer value also checked against text extracted from its correct answer-key page. Exactly 100 puzzle labels in the activity pages and the same 100 in the key. Copyright page and absence of review/development labels checked. Representative interior pages, answer pages, and cover were visually inspected.

These checks do not constitute independent educator/child-reader review, physical print inspection or retailer acceptance. KDP Previewer, a final official cover-template comparison and a physical proof remain outstanding. No account upload or publication was performed.

## Local build and costs

No stock art, paid image service, model API, or outside production purchase was used. All artwork is original vector geometry generated locally. Install the Python packages from `requirements.txt` and run `python build_book.py`. Requires local DejaVu Sans regular/bold at the paths in the script. Fonts are embedded in the PDF; standalone TTF files are not distributed here. Adjust paths for another operating system.

This book uses AI-generated text and images. Disclose both accurately to KDP. Confirm rights and authority to publish. A copyright notice is not a legal determination of protection for AI-generated portions. No ISBN was invented.
