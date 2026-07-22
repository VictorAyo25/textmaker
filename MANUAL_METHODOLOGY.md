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
7. **Internal consistency is not correctness.** Two silent failures shipped
   defective books from this workspace, and both passed every gate that only asks
   whether the PDF agrees with itself: fonts measured in fallback metrics (the
   pagination lottery, §2), and Chromium scaling the whole book down to fit its
   widest box (the shrink, §2b, which shipped COS221 at 92.9% and PHY121 v2 at 64
   pages instead of 148). Always measure the RENDERED artifact against the DESIGN,
   the font size it came back at, the page count's plausibility, not just against
   itself. And re-measure after *any* change that can move layout, including after
   sign-off: the shrink was found in a book already in FINAL_MANUALS.
8. **Measure every claim, not just every number** (item 4, generalised, and it
   bites hardest on a code course). Compiler error counts, rounding, operator
   semantics and library behaviour are all folklore-ridden. Run it. COS221 found
   the printf half-up rounding rule, `Math.pow`'s supposed inexactness, the sign of
   `%` on negatives, and "a Swing program hangs without `System.exit(0)`" all differ
   from what is commonly taught and often from what the course's own slides assert.
   A claim you did not execute is a guess wearing a fact's clothes.
9. **A gate you have not tried to break is one you are trusting on faith.** Every
   gate here first shipped with a blind spot found only by feeding it known-bad
   input: the before-use audit was blind to strings, comments and `catch` clauses;
   the reference audit would have passed a table of pure invention until it was
   control-tested in both directions. When you write or change a gate, prove it
   FAILS on the defect it claims to catch, not merely that it passes today.
10. **A past question is QUOTED, never restated.** Wherever a real exam question
    appears, anywhere in the book, it is reproduced in the examiner's exact words
    and then broken down before it is answered. See §4c, which is binding.

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

### 2b. Chromium shrinks the WHOLE book to fit its widest box

The most expensive bug found in this workspace, and the quietest. Chromium's
print path scales the entire document down so its widest box fits the paper. One
over-long line, in one code block, on one page, therefore reduces the body font
size of **every page in the book**.

CSC241 was rendering at **96.9%** of its design size because of a single
93-character line in Module Five, and dropped to **87.1%** when Mock Two added
three 104-character lines. The manual asks for a 9.6pt body; readers would have
got 8.36pt. Nobody would have noticed: there is no error, no warning, and the
page looks perfectly proportioned, because *everything* shrank together. Fixing
the four lines took the book from 106 pages to its true 127.

**Every other gate is blind to it.** A layout check for content outside the
content box cannot see it: after the shrink, nothing overflows. That is the
trap. The scale is the fingerprint, so measure the scale:

- **Cheap and precise, before rendering:** no code line may exceed the measured
  column limit. For an A4 page with 18mm side margins and `pre` at 8.7pt DejaVu
  Sans Mono, the page allows **90 characters** (measured: 90 renders at 9.60pt,
  92 at 9.40pt, 93 at 9.31pt, 104 at 8.36pt). Re-measure it if the page geometry,
  the code font size, or the box padding changes.
- **Model-free, after rendering:** assert the body text came back at the size the
  CSS asks for. This catches any cause, not just long code, and it is the check
  that actually matters.

**But the page is the wrong thing to measure against, and 90 is a trap.** Almost
no code sits on the page: it sits in a teaching box, which costs it about 20pt of
width. Measured in CSC241, code inside a box starts at x=73.7 and its panel ends
at x=534.8, which is 461.1pt, or **87 characters** at 5.238pt each. 88 clears by
0.1pt, which is noise rather than room. So there are two different limits and the
smaller one governs:

| | Limit | What breaks past it |
| --- | --- | --- |
| Code inside a box | **87** | the line hangs over the panel edge |
| Code at page width | 90 | Chromium shrinks all 134 pages |

Between 88 and 90 a line clears every margin, triggers no shrink, and still
prints with its tail outside the box drawn around it. CSC241 shipped two such
lines and every gate passed them, because each was looking at the page. Cap code
at the box limit, and **check the rendered code against its panel, not against
the page**: the column count is only a proxy for that.

All three checks live in CSC241's `gates.py` and `qa_layout.py`. PHY121 is clean
at scale 1.0000 (physics has no long code lines). COS221 was found rendering at
**92.9%** on two 99-character lines, **after it had already shipped** at 298 pages:
the shrink is invisible, so every gate then in place passed the defective render and
it went to FINAL_MANUALS looking perfect. It was caught only because CSC241, working
the same bug in its own book, measured COS221's render in passing and left a note.
Fixed by wrapping every code line to <=88 chars (the panel limit here; re-measured,
not inherited from CSC241's 87 at its own font size), which returned it to full size
and its true **333 pages**. COS221 now carries both guards inline: a pre-render
column cap in `check_code.py`, and a rendered-font-size plus panel-overflow check in
`qa.py`. Any course with code, and especially SQL or Java, should be checked.
**Measure the rendered font size of a finished manual before believing it is the
size you designed** -- and measure it again after any change that adds a line of
code, because a passing gate suite is exactly what a shrunk book looks like.

### 2c. The type size is pinned by the code, not chosen

A related consequence, worth knowing before anyone proposes to make a manual more
readable by enlarging it. In CSC241 the prose was tested at 10.5pt and 11pt:

- **Scaling the whole sheet up does nothing at all.** At 11pt the code font goes
  with it, the 90-column lines stop fitting, and Chromium shrinks the document
  straight back: the render came back at 9.61pt and 132 pages, indistinguishable
  from the 9.6pt original. The code width, not the prose, fixes the book's scale.
- **Prose can grow only if the code is held.** Scaling every pt except the mono
  sizes gives a clean 10.5pt body at 141 pages (+9). At 11pt something overflows
  again and it shrinks, so 10.5 is the ceiling for this geometry.

So a code-bearing manual cannot be enlarged the way a prose one can. The lever is
prose-only, the ceiling is measured rather than chosen, and the price is paid in
pages.

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

## 4b. The first-use audit (script it; do not assert it)

"Sufficient on its own" is the promise that is easiest to believe and hardest to
keep, because the author already knows everything in the book. Measure it:
walk the **assembled** HTML in reading order and record, for every keyword, API
and method, the section where the reader first meets it. Two things must hold.

1. **Nothing is used that is never named in prose.** An API that lives only
   inside code blocks is a hole: the reader meets it, cannot look it up, and has
   nowhere to go. Being demonstrated is not the same as being documented.
2. **The mocks teach nothing.** A mock tests what the modules taught, so an API
   whose first appearance in the whole book is in a mock is one the reader is
   examined on and was never shown.

Judge (2) on where the reader first **meets** the name, in prose or in code: a
reference table that names an API has taught it, even if no example runs it.
Judging on first *code* use instead reports every entry that a table introduced,
which is noise.

Exclude the deliberately broken code in "identify the error" questions, or the
audit reports the planted fault as an undocumented API, which is the exact
opposite of what the question is doing. Tag those blocks in the markup
(`<pre class="code broken">`) rather than keeping a list of exceptions.

CSC241 ran this over a manual that had been asserted clean and it found two
holes immediately, one of them costly: the book taught counting **vowels**
(`ch in "aeiou"`, which needs no letter test) while the exam asks for
**consonants**, which needs `isalpha()` to tell a letter from a space. The mock's
own answer used `isalpha()`; the manual had never mentioned it. The gap was in
the teaching, not the mock, and no amount of rereading was going to surface it.
**A mock answer reaching for something the modules never taught is a signal the
modules have a hole, not a signal to rewrite the answer.**

**Make it a standing gate, not a one-off, and make it course-agnostic.** The
first version scanned Python keywords and methods and was dead weight for a course
whose notation is SQL, relational algebra, and ER/EER drawing, where a blanket
all-caps sweep is pure noise (`STAFF`, `SELECT`, `SSN` are not abbreviations to
expand). The durable form inverts the burden the way the coverage gate does: the
author **declares** the notations the manual leans on (a `NOTATIONS` table of
abbreviations, symbols, and named terms, each with the regex that marks its
*introduction*), and the gate proves each is (1) introduced at all, and (2)
introduced **outside** a mock. Enumerating the list is the forcing function.
The two escapes this reliably catches on a non-programming course are the ones
DTS224 actually had: an **abbreviation used but never expanded** (schema listings
wrote `PK`/`FK` for pages with no "primary key (PK)" anywhere), and a **term
promised in a unit's objectives but defined only in a late mock answer** (the
"subtype discriminator", defined 2,000 lines after it was first promised). The
intro cue must key on a real definition, never on the objectives-list mention, or
the promise reads as the teaching. This gate is `qa_firstuse.py`, wired into
`assemble.py` as a hard gate from DTS224 on; **a new course ports it and rewrites
`NOTATIONS` for its own notation set** as part of standing up the pipeline. Like
every gate here, control-test it: strip an intro and confirm it fails (proven for
DTS224 on `PK`, `FK`, and the discriminator).

## 4c. Past questions are QUOTED VERBATIM, then broken down (BINDING)

Added 2026-07-22 after a reader reported it across every shipped manual. Five
books were affected: IFT222 (101 sites), TMC221 (60), CSC241 (59), DTS224 (15),
COS221 (its own markup). It is now a hard rule and a gate.

**The defect.** Solved papers and mocks presented a *compressed restatement* of
each question in the author's voice, formatted as though it were the paper. The
2024/25 IFT222 Q1(a) really reads:

> Consider three (3) floating point numbers X, Y and Z stored in registers based
> on the IEEE 754 Single precision floating point format. X = C1400000h,
> Y = 42100000h, Z = 41400000h. Convert X, Y and Z to decimal numbers and
> determine which of the following is true. **9mks**

The book said: "X = C1400000H, Y = 42100000H, Z = 41400000H are stored in
IEEE-754 single precision. Convert each to decimal and test (i)...". Same
substance, different sentence. That is not the paper, but the student reads it
as the paper, and revises against a question that does not exist.

**Why it matters more than it looks.** The student is training pattern
recognition for the hall. Restating strips exactly what they must learn to read:
the examiner's phrasing habits, the real numbering, whether marks sit per-part or
per-question, the padding words, the ambiguity they will have to resolve under
time pressure. A paraphrase is the author having already done the hardest half of
the work (comprehension) and handing over only the arithmetic. It also silently
launders the paper's own errors and oddities into clean prose, destroying the
evidence the student needs.

**The rule.** Anywhere a real past question is referenced, ANYWHERE (solved
papers, mocks built from real questions, worked tests, cram sheets, a module
citing "this was asked in 24/25"):

1. **Quote it verbatim.** The examiner's exact words, exact part numbering
   (`a.`, `i.`, `ii.`), exact symbols and casing (`C1400000h`, not `C1400000H`),
   exact mark text (`9mks`, not "(9 marks)"), exact line breaks where meaningful.
   House style yields here: the paper's own dashes and phrasing stay, because
   this is a quotation of an external document, not our prose. (Transcribe the
   character; do not import a literal em dash if the paper's glyph is a hyphen.)
2. **Mark it visibly as the examiner's words**, in a dedicated box (`box paper`)
   with an "AS PRINTED" bar, so it cannot be confused with commentary. Any typo,
   contradiction or ambiguity in the original stays IN, with a note *after* the
   quote flagging it. Never silently repair a paper. (COS221's 24/25 Q6 D
   contradicts itself; that contradiction is now evidence, not a bug to fix.)
3. **Break it down before answering.** Between the quote and the solution, a
   BREAK IT DOWN step in the student's shoes: what am I given, what is actually
   being asked (the instruction verb, "determine which is true" is not
   "convert"), what do the marks tell me about expected depth, which unit teaches
   it, and where the trap sits. Only then the worked answer.

So every past question is a three-part unit: **AS PRINTED, then BREAK IT DOWN,
then the answer.** The existing Given/Find/Formula block is part 3's opening, not
a substitute for part 2.

**The gate needs THREE directions, not two.** Both obvious directions work from the
AS PRINTED boxes, so both are structurally blind to a module that cites a past
question while teaching, which has no such box. COS221 published with two misquotes
of exactly that kind (one dropped "(from i onward)" from inside quotation marks,
one lowercased the paper's own quoted term) and had to republish; IFT222 hit the
same gap from the other side, where a teaching site lost its quote while the
solved-papers section still covered the question. So add a third: in any box whose
provenance chip cites a paper, every run inside quotation marks must be verbatim
too (COS221's form), or every worked example whose chip cites a paper must carry a
quote (IFT222's form). Pick whichever suits the book, but do not ship with two.

Two mechanical warnings on that third check. **Quote pairing:** a regex like
`"([^"]+)"` pairs the CLOSING quote of one quotation with the OPENING quote of the
next and reports the prose between as a misquote, which produced five phantoms out
of seven reports on COS221. Split on the quote character and take odd-indexed runs.
**Code is not quotation:** strip `<pre>` and `<table>` first, or every Java string
literal in a listing is read as a claim about the paper.

**The gate: `qa_verbatim.py`.** Transcribe each paper once into
`sources/exams/transcripts/<paper>.txt`, a plain-text faithful copy, and treat it
as the authority. The gate then proves every quoted question in the book appears
in the transcript character-for-character (normalising only whitespace and
typographic quotes), and that every question in the transcript appears in the
book. Both directions, like the reference audit: one direction catches
paraphrase, the other catches quietly dropped parts.

Transcription is by eye from photographs (the papers are `.jpg` scans), so it is
the one input here that cannot be machine-verified. Do it slowly, re-read the
image against the transcript once, and never "tidy" while typing. **A transcript
you paraphrased into is a gate that certifies your paraphrase**, which is the
whole defect wearing a gate's clothes. Control-test it: alter one word in a
quoted question and confirm the gate fails.

**Run the width gate AFTER the quotes go in, not before.** Proven on COS221, which
had every guard from 2b already in place and still shipped a render at 90.9%: the
column check was run before the last batch of quoted listings was inserted, so a
123-char line reached the renderer and scaled the whole book from 347 pages down
to 248. Every other gate passed, because a shrunk book is internally consistent
(0.7). Quoted listings are the sharpest case of this, because they are new code
entering the book that you are NOT free to reflow. When one is too wide, **wrap it
where the paper wraps it**: on COS221 the offending line was one the paper itself
breaks across two printed lines, so quoting it faithfully and curing the shrink
were the same edit. Never straighten the paper's own wrapping while transcribing.

**Two fidelity traps that live in the code, not the prose.** Both were found only
by quoting COS221 part by part, and both had passed every gate for months:
- **Renamed classes.** Five listings had a `Broken` suffix bolted on
  (`SquareCalc` -> `SquareCalcBroken`, `Main` -> `MiddleValueBroken`) to dodge a
  filename clash that cannot occur, since every listing compiles in its own temp
  directory. A renamed class inside a quotation is a paraphrase in code.
- **Our wrapper quoted as the paper's.** One question printed a bare fragment with
  no class and no `main`; the book had wrapped it so it would compile, and the
  wrapper ended up inside the quotation. Quote the fragment; keep the wrapper in
  the answer, labelled as yours.

**Mocks are different.** A mock question the author invented has no transcript,
so it is not quoted and needs no AS PRINTED box; it is our question. Only mark
something AS PRINTED if it genuinely is. Mark author-written questions clearly as
practice, and where a mock deliberately mirrors a real question's shape, say so
and cite the paper rather than implying it is that paper's wording.

## 5. Release rule

Work-in-progress stays in that course's `build/` and `drafts/`. A finished manual
goes to `FINAL_MANUALS/` **only when Victor says "we are done"** for that course.

Naming: `<CODE> - <Course Title> - Study Manual.pdf`, with **no version suffix**.
One current manual per course, one filename that never changes, so publishing
replaces it in place and no link or printout goes stale. Versions (`v2`, `v4`)
are for `drafts/` only. Record what changed in `FINAL_MANUALS/README.txt`; git
keeps the superseded copies.

## 6. Per-course intake checklist

- [ ] Collect all slide decks + every past test/CBT (screenshots ok).
- [ ] Confirm course identity: title, code, author name for the footer.
- [ ] Note any deck-numbering quirks (PHY121: lecturer "Module 6" = manual "Module 5").
- [ ] Decide palette + tone + which box types dominate.
- [ ] Identify the ~dozen core ideas → Foundations + must-memorise + formula sheet.
- [ ] List diagrams the course needs (this is where slides usually beat prose).
- [ ] **Transcribe every past paper verbatim** into
      `sources/exams/transcripts/<paper>.txt` BEFORE writing any solution, so the
      quote is the thing you solve from, not something reconstructed afterwards
      from your own summary. §4c.

### Before you ship (every course, every re-publish)

The gates below all passed on books that shipped defective, because each failure is
invisible to a PDF-agrees-with-itself check. Run these against the RENDERED artifact,
and run them again after the last change you make, not just after the last gate pass.

- [ ] `render.py` waits on `document.fonts.status === 'loaded'` AND verifies the
      faces loaded (grep `fonts.status`). A new course copies `render.py` from the
      last and can lose this in the port. §2.
- [ ] The rendered body/title font size equals what the CSS asks (measure it; do not
      trust the page count). A book at 92.9% looks perfect. §2b.
- [ ] No code line exceeds the measured panel column limit (re-measure the limit per
      course; it depends on the code font size, margins and gutter, so CSC241's 87 is
      not COS221's 88). §2b. **Run this check LAST, after the final content edit.**
      Running it before one more listing goes in is how COS221 rendered at 90.9%
      with the guard already written and passing. §4c.
- [ ] For a code/SQL course: every listing compiled and run, every printed output
      captured from the real engine, and every behavioural CLAIM executed (§0.8).
- [ ] Every gate control-tested: it FAILS on the defect it claims to catch, proven by
      feeding it a known-bad input, not merely green today (§0.9).
- [ ] **Every past question quoted verbatim, marked AS PRINTED, and broken down
      before it is answered**, with `qa_verbatim.py` green in both directions
      (no paraphrase, no dropped part). §4c.
- [ ] Published name carries no version suffix; versions live on `drafts/` (§5).

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
1. Put an `id` on each heading element that is already on the page. Pass 1:
   render with the links real and the numbers blank.
2. Read each section's page back from the **link destinations Chromium
   resolved** (`page.get_links()`), build the Contents, re-render. Loop until a
   render agrees with the Contents it was built from.
3. Chromium emits **named** destinations; many viewers ignore them, and a merge
   will not renumber them. Convert every Contents link to an explicit
   `LINK_GOTO` with pymupdf, then merge. `fitz.Document.insert_pdf` shifts GOTO
   targets for you; named destinations it leaves pointing at the old page.

**Do not locate sections with invisible marker text.** PHY121 did (a 2px white
`TOCM<id>TOCM` span) and CSC241 inherited it, at a cost worth recording:

- Any extra element, however small, is laid out in its own right. A zero-height
  box sitting at a page boundary gets painted into the fragment on **both** sides
  of the break, so the marker is found on the page *before* the heading starts.
  The Contents then numbers that section one page early and links to the same
  wrong page. Every number agrees with every link: the book is internally
  consistent and wrong, which is the failure mode that survives review.
- `display:block` + `break-after:avoid` does not save it (it fragmented on 4 of
  25 headings). `position:absolute` inside the heading does not either.
- Making the marker inline instead moves the bug rather than fixing it: it then
  shifts the heading text sideways by the marker's own width.
- The anchor approach has none of this, because it adds no box. It is also the
  better check: a link destination is *exactly* what a reader gets by clicking,
  so it is the thing you wanted to verify anyway.

**Do not find a section by searching for its heading text either.** The Contents
page lists every heading in the book, so a naive search finds each one on the
Contents itself. (Also: a letterspaced kicker extracts as `M O D U L E  O N E`
and will not match at all. Search the title, which is not letterspaced.)

**Two page numbers are in play; do not confuse them.** With a cover merged in
front of the body, the number printed in the Contents is the **footer** number
(Chromium numbers the body render from 1), while the link target is the
**physical** page, which is one greater. Confusing them yields a Contents whose
numbers are all right and whose links are all off by one.

**The pymupdf link dict key is `nameddest`, not `name`.** Reading the wrong key
returns nothing and looks exactly like "the renderer emitted no links".

### Verify the Contents against the book, never against itself
Follow every link and assert, per row: the page it lands on carries that
section's heading, and the number the row prints equals the number that page's
own **footer** prints. Consistency checks pass happily on a Contents that is
uniformly one page out. Pair rows to sections **by anchor name** while the names
still exist (before the GOTO conversion), not by position on the page.

### Print-CSS gotchas that cost real time
- `page-break-before` on a full-page image **plus** `page-break-after` on the
  preceding divider = a **blank page** between them. Use one, not both.
- Full-page dividers: **`min-height` does not reserve the page.** `min-height:248mm`
  in a 262mm content box leaves 14mm, and 14mm is enough for the next section's
  kicker and title to squeeze in. They then sit stranded at the foot of the
  divider while their own text starts overleaf. This is not hypothetical: it was
  live on 4 of 6 dividers in CSC241, inherited from this very note, and was only
  caught when a generated Contents printed the same page number for a module and
  its first unit. Give `.part` a `page-break-after:always` so a divider owns its
  page. Reach for `min-height` only to place the divider's own motif.
  - PHY121, where this note came from, is clean on all 9 dividers **by luck**:
    its field-lines motif is tall enough to push the divider past the content box
    on its own. CSC241 copied the rule with a small REPL motif in place of the
    SVG and the gap opened. The rule never worked; one manual's artwork was
    hiding it. So do not "fix" PHY121, and do not trust `min-height` again.
  - `page-break-after:always` here is safe **only if** the following section does
    not also force a break-before, which is the blank-page case above. Check what
    actually follows the divider before adding it.
- `page-break-after:avoid` on `.kick` binds a kicker to its title, but the pair
  still moves as a unit. It stops the kicker being orphaned *from its title*; it
  does not stop the pair being stranded on a page they do not belong to.
- When harvesting text from a source page by a y-window, filter on the span's
  **top**, not its centre — a last line at y=396 has centre ~401 and silently
  vanishes from a `60..400` window. (This truncated a divider blurb mid-sentence.)

### QA gates to run before delivering (all must be zero)
near-blank pages; footer number != page position; unresolved TOC entries;
em/en dashes; banned terms; Contents links not GOTO.
Plus: recompute **every** number independently, and eyeball a montage of all pages.

**A box is one idea, so never let one be cut across a page turn.** Set
`break-inside:avoid` on every box and leave it there. The temptation is to relax
it to `auto` for the long boxes (a whole exam question, a worked answer) on the
theory that something taller than a page cannot be kept together anyway. That
reasoning is wrong twice: `avoid` is best effort, so a box that genuinely cannot
fit is still split by the engine, and the relaxation applies to every box and not
just the long ones. Measured on CSC241, `auto` cut **30 boxes that would have
fitted whole** and exactly **1 that had to split**. The cost of `avoid` was 7
pages of white space in a 134-page book. Gate it: a box that runs off the bottom
of one page and resumes at the top of the next has been cut, and if the two
halves together fit on a page, the cut was avoidable.

A "short page" gate cries wolf unless it knows *why* a page is short. A box is
never split, so a page legitimately ends early whenever the next box is taller
than the room left, and the page before a forced section break is short by
design. Report the free space and the height of the next block alongside the
flag: a short page whose successor **would** have fit is the real defect, and
that number tells the two apart at a glance. A check that flags known-good pages
on every run is a check that gets ignored.

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
