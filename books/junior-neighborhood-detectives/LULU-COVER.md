# Junior Neighborhood Detectives — Lulu cover

`lulu-cover-full-wrap.pdf` is the print cover, created from the existing vector design using the user-supplied Lulu dimensions. No changes were made to the KDP cover or interior.

- Document: **17.58 × 11.25 inches** (1265.76 × 810 PDF points).
- Trim: **8.5 × 11 inches** per panel, **120 pages**.
- Spine: **0.33 inch**. No spine text.
- Bleed: **0.125 inch** around outer document edges.
- All original panel text, badges and illustrations fitted proportionally inside rectangles **0.5 inch inside each trim edge**, including each spine fold. Background colors extend through bleed.
- Barcode reserve: **3.622 × 1.26 inches**, unprinted solid white, at lower-right of back. Right and bottom clearances are **0.5 inch from trim**, or **0.625 inch from the outer document edge**.
- Barcode document coordinates (bottom-left origin), inches: x=4.503, y=0.625, width=3.622, height=1.26.
- Inch measurements are authoritative; the supplied millimeter figures were rounded.
- Vector text/artwork retained. Raster companion: **5274 × 3375 pixels at 300 DPI**.

The original smaller cover art was inset rather than stretched, so no face, letter or object proportions changed. The old KDP barcode reserve was covered and replaced by Lulu's larger reserve. No printer marks or template guidelines appear in the upload PDF.

## Important interior mismatch

The existing `interior.pdf` is **8 × 10 inches**, not 8.5 × 11. This cover matches the supplied Lulu dimensions, but the existing interior must be reformatted separately before using that trim size. Do not upload this cover and the old interior as a matching book package.

## Verification

Exact page size, text safety rectangles, barcode dimensions/clearances and blank-white barcode interior were checked locally. A rendered cover preview was inspected. No actual Lulu template PDF was supplied, and Lulu upload/preflight acceptance has not been tested. Validate the final book against Lulu's current template and preview before ordering.

Rebuild: Python 3.11+, PyMuPDF and Pillow; run `python build_lulu_cover.py` beside `cover-full-wrap.pdf`. The source KDP cover must remain present. See `lulu-cover-validation.json` for machine-readable geometry.
