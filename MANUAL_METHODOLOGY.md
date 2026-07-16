# Course Manual Methodology — a living playbook

A reusable process for turning a course's slide decks + past tests into a
powerful, active-recall study manual. Each course keeps its own voice, colours,
and emphasis — this playbook captures what stays constant: the *method*.

> Origin: reverse-engineered from Victor's PHY121 "Complete Study Manual" and
> extended while building its Module 5 update. Update this file as we learn more.

---

## 0. Guiding philosophy (the non-negotiables)

1. **Teach from zero.** Every idea is explained before it is used. Assume the
   reader is shaky on the maths and build the maths first (a "Foundations" part).
2. **A course is ~a dozen ideas reused.** Find them, state them plainly, and make
   everything else hang off them. Three views of that skeleton: a Foundations
   part, a "must-memorise list", and a formula sheet.
3. **Active recall over passive reading** (K. A. Stroud style). Programmed
   frames, constant "cover the answer / now you try", "redo it on blank paper".
   Reading feels productive and teaches almost nothing — force retrieval.
4. **Radical numerical honesty.** Recompute *every* number independently. Where a
   slide rounds differently or slips, state both "what the slide says" and "what
   is true" — never silently correct.
5. **One idea per box.** Never two ideas in one box.
6. **Close the loop.** Solve every classwork item and every past test question,
   then write mock papers weighted to mirror the real tests, cross-referenced
   back to the teaching section (§) that each answer tests.

## 0b. House style (HARD rules for every manual)

These are absolute constraints on manual *output* (not on internal docs):

- **No em dashes (—) or en dashes (–) anywhere.** Use commas, colons, periods, or
  parentheses; write ranges as "1 to 4". Mathematical minus (−, U+2212) in
  equations is fine and stays.
- **Never name the pedagogy source** (e.g. no "K. A. Stroud") in the manual. Use
  the technique; do not cite it.
- **No institution branding** in the manual: no "Covenant University", "CCODeL",
  or similar. Footer is course + author only (PHY121: "PHY121 · General Physics II
  · Victor Ayodeji").
- Voice: reads like a **world-class textbook** yet stays very easy to understand,
  taking a complete novice all the way to a perfect exam score.

Add a QA gate that greps output for `—`, `–`, "stroud", "covenant", "ccodel"
before any render is considered final.

## 1. The box grammar (fixed visual vocabulary)

Seven labelled boxes, each with exactly one job. Navigate by shape and colour.

| Box | Job | PHY121 colour |
|---|---|---|
| TEACH | one idea, plain language | navy `#1b2a4a` / bg `#f4f7fc` |
| FORMULA | boxed result, every symbol + unit defined | navy header / white |
| MUST-MEMORISE | the reserved colour — appears nowhere else; each has a memory hook | magenta `#c2185b` / bg `#fdeef5` |
| WORKED EXAMPLE | numbered steps, reasoning on every line, then "reproduce it"; provenance chip (SLIDE / CLASSWORK / METHOD) | amber `#b45309` / bg `#fdf6ec` |
| RECALL AND CHECK | retrieval question, answer hidden under a dashed rule | slate `#4a5568` / white |
| TRAP | the mistake made every year | red `#b91c1c` / bg `#fdefef` |
| FILL IN THE GAP | active cloze practice + answers | purple `#5b3a8e` / bg `#f4effb` |

Signatures worth keeping: "Now redo it:" tag (amber) after every worked example;
"MEMORY HOOK:" (magenta) in every must-memorise; forward references ("you'll need
this in Module 4"); mock questions that are known traps reversed.

**Per-course customisation:** keep the *structure* fixed but re-pick the palette,
the tone, and which box types dominate (a proof-heavy maths course leans on
WORKED EXAMPLE + TRAP; a descriptive course leans on TEACH + RECALL).

**Colour should match the subject (be intelligent about it).** Choose a palette
that evokes what the course is about, and give the box colours a semantic reading:
- PHY121 (Electricity, Magnetism, Light): deep electric blue = TEACH/fields;
  crimson = TRAP (danger / magnetic pole); amber-gold = WORKED (energy, current);
  vivid magenta = the reserved MUST-MEMORISE (high-voltage accent). Optional thin
  field-line motif on part dividers. This mapping already fits, so keep it.
- Future courses: pick a fitting family (e.g. biology -> greens/earth; chemistry
  -> reagent blues/oranges; pure maths -> restrained ink + one accent). Keep the
  reserved-colour rule: one hue used ONLY for MUST-MEMORISE, nowhere else.

## 2. Build pipeline (technical)

- **Authoring format:** one semantic **HTML** document + a print-**CSS** stylesheet.
- **Renderer:** originally **WeasyPrint** (supports CSS `target-counter` for an
  auto-numbered, linked TOC). On Windows WeasyPrint needs GTK/Pango DLLs — often
  missing. **Fallback that works with no admin rights: Playwright/Chromium**,
  embedding the exact fonts via `@font-face` and drawing the running footer with
  Chromium's `footerTemplate` (`pageNumber`). Compute TOC page numbers ourselves.
- **Fonts:** the PHY121 original used generic `serif`/`sans-serif`/`monospace`,
  which WeasyPrint rendered as **DejaVu Serif / Sans / Mono** (+ DejaVu Math).
  DejaVu ships with **matplotlib** (`mpl-data/fonts/ttf`) — copy those and
  `@font-face` them so any renderer matches.
- **Page:** A4, margins ≈ 18 mm L/R, 19/16 mm T/B; body ≈ 9.6 pt, line-height 1.42,
  justified with `hyphens:auto`.
- **Diagrams:** author as **inline SVG** (vector-sharp, self-contained, renders in
  both engines). Generate curves/geometry programmatically (Python) for accuracy,
  render each SVG to PNG and eyeball it BEFORE embedding.
- Files: `manual.css`, section HTML fragments, an assembler that injects SVGs +
  wraps `<head>`, and `render.py` (Playwright). See the scratchpad `build/` dir.

## 3. Reconstructing an existing manual with no source

If only the PDF exists (no HTML/CSS):
- Extract text with `pymupdf`/`pypdf`. The box **labels appear inline** in the
  extraction ("TEACH · …", "● MUST-MEMORISE · …", "⚠ TRAP · …", "WORKED EXAMPLE ·
  …", "RECALL AND CHECK", "FILL IN THE GAP · …") — parse on these to segment.
- Reverse-engineer style tokens from the PDF: `PdfReader.metadata['/Producer']`
  (renderer), page rect (geometry), span colours (`get_text('dict')`), and box
  header fills by matching a label's position to the drawing rect containing it
  (`page.get_drawings()`).
- **Preserve wording verbatim.** Reuse exact text; only ADD figures / fix real
  errors (flagged). Guarantee fidelity by **auto text-diffing** the re-rendered
  page's extracted text against the original's, normalised — must match.

## 4. QA gates (nothing ships unchecked)

1. **Numbers:** independently recompute EVERY value in a script before writing it.
2. **Diagrams:** render each SVG and visually verify physics + labels + no clipping.
3. **Style fidelity:** pixel/side-by-side diff a rebuilt page vs the original.
4. **Text fidelity:** normalised text-diff of re-render vs original (verbatim parts).
5. **Layout:** render every page to a grid; scan for bad box breaks / overflow.
6. **Whole-document:** page count, TOC page numbers, footer numbering, links.

## 5. Release rule

Work-in-progress stays in scratchpad/build. A finished manual goes to
`FINAL_MANUALS/` **only when Victor says "we are done"** for that course.
Naming: `<COURSE>_Study_Manual_vN.pdf`.

## 6. Per-course intake checklist

- [ ] Collect all slide decks + every past test/CBT (screenshots ok).
- [ ] Confirm course identity: title, code, author name for the footer.
- [ ] Note any deck-numbering quirks (PHY121: lecturer "Module 6" = manual "Module 5").
- [ ] Decide palette + tone + which box types dominate.
- [ ] Identify the ~dozen core ideas → Foundations + must-memorise + formula sheet.
- [ ] List diagrams the course needs (this is where slides usually beat prose).

---

## 12. Rebuilding an existing manual PDF (hard-won engineering notes)

Context: blending a new module into an existing manual when you have **only the
PDF**, not the original HTML source. Proven on PHY121 v2 (163 pages).

### The one trap that governs everything
**Never parse the flat text dump** (`page.get_text()`). It is *jumbled*: a
worked example's step badges are positioned lower on the page, so their text is
extracted *after* later boxes. Reconstructing from that order silently scrambles
content.

**Do this instead — structure-aware extraction.** The manual's own design is the
parser: every box is a coloured header bar + tinted body. So:
1. `page.get_drawings()` -> find header bars (wide rect, height 14-34pt, fill
   matching a known box colour). Colour -> box type.
2. Validate each bar by requiring **white label text** inside it (kills false
   positives from tables/rules).
3. Box body = from bar bottom to the next bar's top. Collect spans by
   containment, order by (y, x). This de-jumbles perfectly.
4. Within a box, classify by span colour/size: grey+small = step note, amber =
   "Now redo it", white-on-magenta circle = step number, etc.

**Identify boxes by bar colour, never by a keyword in the label.** Gating on
"the label starts with TEACH/WORKED/RECALL/..." only holds for the teaching
sections; it silently discarded 54 back-matter boxes labelled "Q4 - POTENTIAL AT
TWO DISTANCES". Colour is what actually distinguishes them: table headers are a
neutral ink and classify to None, every box uses the semantic palette. Enumerate
the palette from the document, do not assume you know it.

### Crop only what is genuinely not text
Reconstruct everything you can: real text is searchable, editable, and reflows.
Crop to an image only for **line art** (framed vector diagrams), which has no
text to recover. Dense tables are *not* an excuse to crop — rebuild them as real
`<table>` (see the sup/sub trap below). Stamp a fresh footer over any crop so
numbering stays global.

Reflowed text is denser than the fixed page images it replaces, so the page count
drops. That is expected; verify content, not page count.

### Fidelity traps that a text-only diff will not catch
Every one of these shipped once, because the check was
`v1.get_text() == v2.get_text()` — which ignores formatting entirely.

- **Formatting lives in span flags**, and dropping them loses meaning:
  bit0(1)=superscript, bit1(2)=italic, bit3(8)=monospace, bit4(16)=bold.
  **Subscripts have no flag** — detect geometrically (smaller size AND lower `y1`
  than the line's baseline). Flatten `8.99 x 10^9` to "8.99 x 109" and you have
  published a wrong constant, not a typo.
- **Some content is drawn, not typed.** Fill-in-the-gap blanks are thin filled
  rects (~62 x 1pt). A text-only pass drops them and the exercise becomes
  unanswerable. Recover them from `get_drawings()` as pseudo-spans.
- **Line-end hyphens come in two kinds and the typesetter marks them.** U+2010 is
  one the hyphenator inserted to break a word ("capa-citor") and must be dropped;
  ASCII '-' belongs to the word ("cross-sectional", "T-joint") and must be kept.
  Do not guess from a dictionary: check the character.
- **Letterspaced labels lose their word breaks.** Tracking wide enough that every
  letter gap beats the extractor's space threshold yields "R E F E R E N C E R . 3".
  Re-emitting that under CSS letter-spacing doubles the tracking and buries the
  real space, printing "REFERENCER.3". Rebuild from `get_text('rawdict')` char
  widths: the word space is measurably wider (3.13pt vs 1.61pt). Only do this to
  labels you know are tracked — in ordinary text ("F = k · q") every space is real
  and the same rule closes them all up.
- **A right-aligned chip is not part of the label.** Reading bar spans in document
  order welds them: "WORKED EXAMPLE - A 2 H INDUCTOR" + chip "TEST 2, Q1" becomes
  "Test 2, q1 worked example - a 2 h inductor". Split on the x-gap.
- **Pages need not contain a box.** Emitting only boxes drops sub-headings, stray
  prose, and any page whose sole content is a heading whose boxes run over onto
  the next page.
- **Wrapped lines must merge.** A note or paragraph emitted one `<p>` per line
  splits mid-word; worse, if steps are flushed as a list at the end, a note's tail
  is printed *above* the whole list, detached from the sentence it ends.
- **A table ends where its own row shading ends** (`table_extent`), not at "the
  next heading" — otherwise the prose after it is swallowed in as rows. A table
  continuing across a page break does not repeat its header: carry the column
  bounds forward.

### Auditing the rebuild honestly
Compare v1 against the rebuild **excluding cropped regions**, and expect two
categories of false positive that are not losses:
1. soft-hyphen fragments ("capa", "citor") that you correctly rejoined;
2. subscripts, if you strip inline tags without a separator ("Q<sub>total</sub>"
   -> "Qtotal" hides the token "total").

Strip **inline** tags with no separator and **block** tags with a space; do it
the other way and the audit invents hundreds of phantom losses. When a residual
will not reconcile, find the specific span and look at it — every one of them was
either a real bug or a flaw in the measurement.

### Page numbers + Contents (the 2-pass dance)
Auto page numbers need a chicken-and-egg fix:
1. Pass 1: render with an empty Contents; locate each section by an invisible
   marker span (`TOCM<id>TOCM`, white, 2px).
2. Read marker -> page map from the render; build the Contents; re-render.
   Loop until page count stops shifting.
3. Chromium emits **named** destinations; many viewers ignore them. Convert every
   Contents link to an explicit `LINK_GOTO` with pymupdf.
4. **Strip the marker text afterwards** via `add_redact_annot(rect, fill=None)` +
   `apply_redactions(images=..._NONE, graphics=..._NONE)` so no junk is left in
   the text layer.
5. Match TOC ids by **exact-then-prefix** — real kickers carry suffixes
   (e.g. `UNIT 4.5 · TEST 2 · NOT IN THE SLIDES` -> id `UNIT45TEST2...`).

### Print-CSS gotchas that cost real time
- `page-break-before` on a full-page image **plus** `page-break-after` on the
  preceding divider = a **blank page** between them. Use one, not both.
- Full-page dividers: don't use `page-break-after`. Give `.part` a
  `min-height:248mm` so following content is naturally pushed off the page (no
  blanks possible).
- Add `page-break-after:avoid` to `.kick`, `.title`, `.rule` or a section kicker
  **orphans** at the foot of the divider page while its title lands overleaf.
- When harvesting text from a source page by a y-window, filter on the span's
  **top**, not its centre — a last line at y=396 has centre ~401 and silently
  vanishes from a `60..400` window. (This truncated a divider blurb mid-sentence.)

### QA gates to run before delivering (all must be zero)
near-blank pages; footer number != page position; unresolved TOC entries;
`TOCM` left in text; em/en dashes; banned terms; Contents links not GOTO.
Plus: recompute **every** number independently, and eyeball a montage of all pages.

**A passing text diff proves almost nothing.** `get_text()` is blind to bold,
italic, monospace, sub/superscript, drawn elements, list structure, and block
order — every fidelity bug listed above survived a clean text diff. Add gates for
what text comparison cannot see:
- a word-level audit against the original, excluding cropped regions, reconciled
  to zero (see "Auditing the rebuild honestly");
- structural counts: `<b>` runs, `<sub>`/`<sup>`, fill-in blanks, list items,
  figures, tables, sub-headings — a drop to zero means a detector broke;
- no `<li>` whose text still starts with its own marker (doubled numbering);
- no mid-word `-</p>` (a paragraph split across a hyphen);
- **look at the rendered pages.** The stranded note tail, the welded kicker, and
  the run-together answers were all invisible to every automated check and
  obvious on sight.
