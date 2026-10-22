# Visual edition build

All illustrations are original local vector drawings in `visuals.py`.
The cover is vector PDF plus 300-DPI PNG companions. The interior is
black-and-white vector artwork and embedded text, 120 pages, 8 × 10 inches,
no bleed. No image-generation service, stock purchase or paid API was used.

Rebuild from this folder with Python 3.11+ and ReportLab, Pillow, PyMuPDF
(installed in the workspace `.venv`):

    ../../.venv/bin/python build_book.py

Outputs are created under `output/`. The script uses system DejaVu Sans
and DejaVu Sans Bold TTFs at `/usr/share/fonts/truetype/dejavu/`.
For another environment, install licensed fonts and adjust these paths.
Retain any applicable DejaVu font license with redistributed font files;
font binaries are not included in this package.

Artwork is schematic. Use the text records, not picture size, for puzzle
measurements. No hidden illustration clues have been added. Matching grids
are blank; hints and answers remain in their original sections.

The separate validation report records the local checks performed. It does
not certify KDP acceptance or independent science/editorial approval.
Before upload: compare against the final official 120-page KDP cover
template, review KDP Previewer, and inspect a physical proof if possible.
