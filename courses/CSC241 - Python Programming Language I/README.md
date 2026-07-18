# CSC241 - Python Programming Language I

Study manual for CSC241, Omega semester, 3 credit units.
Course title on every artefact is the full "CSC241 - Python Programming Language I",
never the bare code (workspace name-and-title rule).

## Status

**SHIPPED 2026-07-18** (first edition, 144 pages). **New edition in progress**, blending
in the real 2025/2026 paper the student supplied on 2026-07-18: a solved-in-full section,
a third mock in the paper's new shape, and the teaching gaps it exposed now filled. Built
to `drafts/` and gate-green; it replaces the `FINAL_MANUALS/` copy in place on the next
explicit sign-off. All four gates green.

Every one of the exam's six questions has a home, on both the 2024/25 and 2025/26 papers:

| 24/25 question | 25/26 question | Topic | Covered by |
| --- | --- | --- | --- |
| One | Two | Control structures | Module Three, Units 1 to 2 |
| Two | Three (c,d) | Data structures, collections | Module Three, Units 3 to 4 |
| Three | Three (a,b), Six | Functions | Module Four, Unit 1 |
| Four | One, Two | Strings | Module Two, Unit 4 |
| Five | Five | File handling | Module Four, Unit 3 |
| Six | Four | Databases, sqlite3 | Module Five, Unit 1 |

Note that **Module Two, Unit 4 (Working with Strings) is ours, not the source's**.
The source manual has no strings unit at all, yet strings are examined heavily, so the
coverage table above would have had a hole in it. It is slotted into Module Two after
Operators, because it needs indexing and slicing from Module Three, Unit 3 only by
analogy, not by dependency.

**The template evolved between the two papers, and the manual now carries both shapes.**
The 2024/2025 paper was rigid: every question five parts, each 3.5 marks, one module per
question. The 2025/2026 paper varies the marks per part (1 to 10.5), varies the number of
parts, and mixes topics inside a question. Neither shape is safe to assume, so the book
teaches to the topics (which did not change) and drills both shapes: Mocks One and Two in
the 24/25 shape, the solved real paper and Mock Three in the 25/26 shape.

**Past Paper 2025/2026, solved in full** is the newest real examination worked end to end,
placed after the modules as the clearest picture of what the question writer now wants.
Every output was captured from a run. It also documents a defect in the paper's own Q6(c)
sample (it prints 10546.90 where `math.pi` gives 10547.79), shown the same way this book
treats every course-material error: run it, show the true figure, state yours.

**Mock One** mirrors the 24/25 paper exactly in shape (six questions, attempt any
four, five subparts at 3.5 marks) with entirely fresh scenarios, so it is practice
rather than a re-read of the real paper. Every answer is executed by the gate: a mock
with a wrong answer is worse than no mock, because it teaches the wrong thing to
somebody with no way to check.

**The Contents** is generated, never typed: 35 rows, every one a working link. Page
numbers are read back out of the rendered book, so they cannot drift from it. See
`build/contents.py`, which carries the reasoning, including why the obvious
implementation is wrong.

Building it paid for itself immediately: it printed the same page number for a module
divider and that module's first unit, which is how a long-standing layout fault
surfaced. Four of the six divider pages were stranding the following unit's heading at
their foot, with the unit's own text overleaf. `.part` now takes `page-break-after`, so
a divider owns its page.

**Mock Two** mirrors the same 24/25 shape with fresh problems throughout, and asks the
parts that caught you in Mock One from the other side: where Mock One's Q1(c) broke the
loop so the `else` was skipped, Mock Two's does not, so it runs.

**Mock Three** is the first mock in the 2025/2026 shape: marks that vary from part to
part, questions that stop at (c), and one question that mixes topics. Fresh scenarios
throughout (a book catalogue, a coding club, a library database, a cylinder-tank sizer),
every answer executed by the gate. It is the practice companion to the solved real paper.

**The whole book had been rendering at the wrong size.** Chromium's print path scales the
entire document to fit its widest box, so one 93-character line in Module Five had been
shrinking every page to 96.9% of design, and Mock Two's three 104-character SQL lines took
it to 87.1%: a 9.6pt body reaching the reader at 8.36pt. Fixing four lines took the book
from 106 pages to its true 127. Nothing else caught it, and nothing else could: after the
shrink nothing overflows, so the layout QA saw a perfect book. There are now two gates for
it, one before the render (`gates.py`, no over-long code line) and one after
(`qa_layout.py`, the body must come back at its designed size).

**The body was later grown from 9.6pt to 10.5pt** for readability, once the shrink bug was
gone and the size the book prints at could be trusted. The stylesheet is a 9.6pt-base scale
grown by 10.5/9.6, with the code specimens (the `pre` blocks, trace tables and answer boxes)
held at their old size *and* padding, so a code line keeps its width. Code that sits inside a
teaching box has a hair less room than before, because the box padding around it did grow
with the scale, so the box-nested column limit tightened; every current line still clears it,
and `qa_layout.py`'s panel check is the post-render proof that nothing hangs past its box.
Prose grew, code stayed put, which also reads better: the code now sits as a distinct,
slightly smaller register instead of nearly the same size as the prose around it. It took the
book from 132 body pages to 142. See the SCALE NOTE at the top of `manual.css`; to rescale,
re-run the base sheet through the scale rather than hand-editing the values.

**Still to build:** nothing outstanding. Five modules, the solved 2025/2026 paper, three
mocks, the Contents and the full gate suite are in.

## Sources

Everything under `sources/` is raw input. Nothing here is ours.

| Path | What it is |
| --- | --- |
| `sources/course_manual/` | The institution's official 224-page course manual (`COV-CSC241`). Five modules, 15 units, self-assessment answers, glossary. |
| `sources/exams/` | Ten past papers, sessions 2014/15 through 2025/26, renamed `exam_<session>.pdf`. The 2025/26 paper's raw phone photos are kept under `sources/exams/2025_26_source_photos/`. |
| `sources/extracted/` | Derived and regenerable. See below. |

There are **no lecturer slide decks** for this course. The course manual plus the
ten papers are the entire source base, so the manual's 15 units define scope. The
2025/2026 paper arrived last (2026-07-18, seven phone photos from the student) and is
the newest and most predictive of the set.

### Derived artefacts (`sources/extracted/`)

- `exam_pages/` - every exam page rasterised to PNG at 200 dpi. Regenerate with the
  snippet in "Rebuilding" below.
- `exam_text/<session>.txt` - raw text layer, for the four papers that have one
  (2015/16, 2020/21, 2021/22, 2022/23).
- `exam_text/<session>_transcript.md` - verified Markdown transcripts. **Six of the
  ten papers are scans with no text layer** (2014/15, 2018/19, 2019/20, 2023/24,
  2024/25, 2025/26) and were transcribed by reading the page images.
- `exam_analysis.md` - cross-year question-shape analysis. This drives authoring.

## This manual is AUTHORED, not rebuilt

There is no prior manual of ours for CSC241. The 224-page document is the
institution's, i.e. a *source*. So the structure-aware extraction and word-level
fidelity machinery built for PHY121 does not apply here. Reuse only the build
pipeline: Chromium render, vendored DejaVu fonts, two-pass Contents, GoTo links,
house-style and layout gates.

## Design decisions

- **Palette:** Python blue and yellow. Steel blue TEACH, green CODE, amber WORKED,
  red TRAP, slate DRY RUN. **Reserved must-memorise hue: Python yellow `#ffd43b`.**
  Chosen to evoke the subject and to stay visually distinct from COS221's terminal
  dark-ink and cyan.
- **Delivery:** author Modules One and Two, render a checkpoint PDF for sign-off on
  voice and palette, then the remaining three modules.

## QA gates

The house rules in the workspace README and methodology playbook all apply. Two
gates matter most for this course:

1. **Every snippet actually runs.** This course's analogue of PHY121's "recompute
   every number". A claimed output that was never executed on a real interpreter is
   a wrong constant. Capture output from the run, never type it by hand.
2. **Keyword/API-before-use audit.** Zero external sources means every keyword,
   symbol, built-in, and library call is introduced before first appearance, and
   every API the manual leans on gets an in-manual reference card. This is
   `qa_firstuse.py`, and it is scripted rather than eyeballed for a reason: it found
   two holes on its first run, in a manual that had been asserted clean.
   - `.isalpha()` was used in a Mock One answer and taught nowhere in the book. It
     was not a mock problem. The manual teaches counting **vowels**
     (`ch in "aeiou"`, no letter test needed) while the exam asks for
     **consonants**, which needs the one idea the book never gave: how to tell a
     letter from a space. Module Two Unit 4 now teaches it.
   - `.keys()` was demonstrated in Module Three Unit 4 but never named, so a reader
     could see it work and had nothing to look up. It now has a reference row
     beside `values()` and `items()`.

## Rebuilding

Regenerate the exam page images and text dumps:

```bash
cd "courses/CSC241 - Python Programming Language I"
python -c "
import fitz, os, glob
out='sources/extracted/exam_pages'; os.makedirs(out, exist_ok=True)
txt='sources/extracted/exam_text'; os.makedirs(txt, exist_ok=True)
for f in sorted(glob.glob('sources/exams/*.pdf')):
    tag=os.path.basename(f).replace('exam_','').replace('.pdf','')
    d=fitz.open(f)
    total=sum(len((p.get_text() or '').strip()) for p in d)
    for i,p in enumerate(d):
        p.get_pixmap(dpi=200).save(f'{out}/{tag}_p{i+1}.png')
    if total>=200:
        open(f'{txt}/{tag}.txt','w',encoding='utf-8').write(
            '\n'.join(f'--- PAGE {i+1} ---\n'+(p.get_text() or '') for i,p in enumerate(d)))
    d.close()
"
```

Build the manual itself:

```bash
cd "courses/CSC241 - Python Programming Language I/build"
python assemble.py            # gates, then HTML, then PDF
python assemble.py --no-pdf   # gates and HTML only, skips Chromium
```

`assemble.py` concatenates `content/*.html` in book order, runs the gates, and renders.
The cover is full bleed with no running footer, so it is rendered on its own and merged
in front of the body. The body is rendered twice: the Contents cannot be written until
the book has been rendered, and writing it moves the pages it names, so `assemble.py`
repeats until a render agrees with the Contents it was built from.

**Every gate stops the build on failure. None is advisory.**

- `verify_code.py` executes **every output the manual claims** against a real
  interpreter and fails on any mismatch (343 claims, including every mock answer). This is the
  course's analogue of PHY121's "recompute every number". It exists because the
  source manual's own transcripts were typed rather than captured: see
  `sources/extracted/manual_audit.md`. Where the manual shows spaces as dots, the
  gate derives the dot string from a real run and requires that exact string to be
  present in the page, so a hand-miscounted dot fails the build. Sets are compared as
  sets, never by printed order: Python randomises string hashing per process, so a
  set of strings prints in a different order every run, and only `len()` and
  `sorted()` are reproducible.
- `gates.py` enforces house style: no em or en dashes, no institution branding, the
  pedagogy source unnamed, the reserved colour used only by MUST MEMORISE, all code
  monospace, and **no code line over 87 columns**. There are two limits and the smaller
  one governs: 90 is where Chromium shrinks the book (see above), but 87 is where a line
  starts hanging over the teaching box it sits in, and almost all code sits in a box.
- The **Contents gate** (in `assemble.py`) follows all 35 links and checks each against
  the book rather than against itself: the page it lands on must carry that section's
  heading, and the number the row prints must be the number that page's own footer
  prints. Checking the Contents for internal consistency is not enough, because a
  Contents can be uniformly wrong and perfectly consistent with itself.
- `qa_layout.py` looks at every page: **the body must render at its designed 10.5pt**, no
  text outside the content box, nothing in the bottom margin but the running footer, **no
  box cut by a page break that would have fitted whole**, **no code line hanging past the
  panel drawn around it**, and no page left short without a reason (a section that must
  start fresh, or a next block too tall to fit).
  - The panel rule exists because staying inside the page is not enough. Two
    `cursor.execute("CREATE TABLE ...")` lines, at 89 and 90 columns, cleared every margin,
    triggered no shrink, and printed with their tails outside the box. Every gate passed
    them, because every gate was measuring against the page. Found by eye, on a spread
    rendered for an unrelated question.
  - The box rule found 30 answer boxes being cut mid-idea, because `.ans` and `.qpaper`
    had been given `break-inside:auto` on the theory that a box taller than a page cannot
    be kept together anyway. Measured, that relaxation cut 30 boxes that would have fitted
    whole to save 1 that had to split. They now inherit `avoid`, which the engine
    overrides by itself for the one genuinely oversized box. It cost 7 pages of white
    space and is worth it: a box is one idea.

`build/` also holds `manual.css` (the CSC241 palette and box grammar), `render.py`
(Chromium via Playwright, footer via `footerTemplate`), `contents.py`, `buildlock.py`,
and vendored `fonts/`.

Only one chat may build this course at a time; `build/.build.lock` enforces it.
Stage commits with `tools/commit_course.sh` from the workspace root, never
`git add -A`.
