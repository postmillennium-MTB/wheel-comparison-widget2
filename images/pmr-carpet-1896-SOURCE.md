# pmr-carpet-1896-mask.png / pmr-carpet-1896-reference.png

**Source:** US Design Patent No. 25,495 — Eugene A. Crowe, of Brooklyn, New
York, assignor to the E. S. Higgins Carpet Company. "Carpet." Patented May
12, 1896.
https://patentimages.storage.googleapis.com/0f/c9/3c/d7c0d3252498de/USD25495.pdf

**Public domain:** same basis as the sibling USD28,278 pattern already on
this site — an 1890s design patent ran a 3½/7/14-year term, so protection
lapsed within years of grant. This one is 130 years past its filing;
well over a century expired. The scan is the USPTO/Google Patents
reproduction of the drawing, not a rights-managed image.

**Why this one:** the plate carries reference letters (B, B², b, b², b³)
tying the acanthus-scroll motif to the specification, the same convention
that identified the sibling 1898 pattern as a true drawn repeat unit rather
than an illustration that merely looks tileable. Supplied by Jon as a
scanned plate image (not fetched by this session — see the environment
constraint below).

**How the assets were made:**
1. Started from the plate image as supplied (1098×1710px), no PDF re-render
   available this pass — see constraint note below.
2. First pass found the content bounding box by per-row/per-column
   ink-density thresholding (rows/cols above 2% ink): crop (18, 14)–(1022,
   1693), 1004×1679px. **This crop shipped initially and produced a visible
   vertical gap between tiles in production** — the 2%-ink threshold let a
   genuine blank-paper margin (ink density fading from the pattern's typical
   ~35–48% down to ~3–16% over roughly the outer 20px on the left/right
   edges) into the crop, so adjacent tiles abutted a strip of near-empty
   canvas instead of continuous pattern. A full column/row density profile
   (20px bands across the whole crop) made the fade bands visible and
   located the true edge of the repeat content.
3. **Corrected crop**, trimmed inward past the fade bands: (38, 14)–(978,
   1664) from the original supplied image, 940×1650px. Row density was
   already consistent edge-to-edge (no comparable vertical fade), so only
   the left/right/very-bottom margin needed trimming.
4. Verified seamlessness by tiling 3×3 at full resolution: the B/B²/b/b²/b³
   reference-letter clusters rejoin correctly across the boundary with no
   visible seam, matching the sibling pattern's own verification method —
   confirmed again after the crop correction, at the actual 260px header
   tile size and 8% opacity, before shipping the fix.
5. Downscaled to 800px wide (1404px tall, from the corrected crop) with
   Lanczos resampling before thresholding, same as the sibling asset, so
   the fine hachure lines average into clean gray instead of aliasing into
   moiré.
6. Otsu-thresholded (threshold 134 on the downscaled grayscale) with a soft
   ±18-level ramp, written out as a transparent alpha mask — ink opaque,
   paper transparent, RGB left at zero — so any element can tint it via
   `mask-image` + `background-color`.

**Files:**
- `pmr-carpet-1896-mask.png` — the alpha mask, wired into the atlas header
  (`header::before` in `index.html`), replacing the sibling 1898 pattern
  there.
- `pmr-carpet-1896-reference.png` — same crop/mask, composited at near-black
  (`#1a1a1a`) ink on transparent, kept as a plain reference if you want to
  see it without a theme tint.

**Ink coverage:** ~39.5% at the 800px-wide working resolution — dense, same
reasoning as the sibling asset (a real woven-carpet pattern, not drawn to
read as a faint watermark on its own). Applied at low opacity in actual use
(8% in the atlas header) rather than displayed at full strength.

**A known environment constraint, differs from the sibling asset's
derivation:** this session's network egress proxy blocks direct fetches to
`patents.google.com` and the Google Patents PDF storage host used above (see
`CLAUDE.md`'s "A known environment constraint" section), so the plate could
not be re-rendered from the source PDF at a controlled DPI the way the
1898 pattern's mask was. The crop instead started from the image Jon
supplied directly in chat. The patent number, title, date, and assignee
were readable from the OCR text layer/caption visible in that same supplied
image, not independently re-confirmed against the PDF by this session — a
future session with working access to the PDF link above should do that
cross-check if it matters for the record.
