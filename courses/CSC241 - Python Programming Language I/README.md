# CSC241 - Python Programming Language I

Study manual for CSC241, Omega semester, 3 credit units.
Course title on every artefact is the full "CSC241 - Python Programming Language I",
never the bare code (workspace name-and-title rule).

## Status

**Modules One to Three authored**, rendered to `build/CSC241_checkpoint.pdf`
(47 pages: cover plus 46). Voice and palette approved. Modules Four and Five remain.

Module Three is the heaviest: it carries exam questions One (control structures) and
Two (data structures), and it holds the two patterns that decide part (e) of every
question, the `done` sentinel loop and the split-and-convert loop.

## Sources

Everything under `sources/` is raw input. Nothing here is ours.

| Path | What it is |
| --- | --- |
| `sources/course_manual/` | The institution's official 224-page course manual (`COV-CSC241`). Five modules, 15 units, self-assessment answers, glossary. |
| `sources/exams/` | Nine past papers, sessions 2014/15 through 2024/25, renamed `exam_<session>.pdf`. |
| `sources/extracted/` | Derived and regenerable. See below. |

There are **no lecturer slide decks** for this course. The course manual plus the
nine papers are the entire source base, so the manual's 15 units define scope.

### Derived artefacts (`sources/extracted/`)

- `exam_pages/` - every exam page rasterised to PNG at 200 dpi. Regenerate with the
  snippet in "Rebuilding" below.
- `exam_text/<session>.txt` - raw text layer, for the four papers that have one
  (2015/16, 2020/21, 2021/22, 2022/23).
- `exam_text/<session>_transcript.md` - verified Markdown transcripts. **Five of the
  nine papers are scans with no text layer** (2014/15, 2018/19, 2019/20, 2023/24,
  2024/25) and were transcribed by reading the page images.
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
   every API the manual leans on gets an in-manual reference card. Script this as a
   first-use table over the built HTML; do not eyeball it. The 2024/25 transcript
   ends with the full list of idioms the exam actually requires.

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

`assemble.py` concatenates `content/*.html` in book order, runs both gates, and
renders. The cover is full bleed with no running footer, so it is rendered on its
own and merged in front of the body.

**Both gates stop the build on failure. Neither is advisory.**

- `verify_code.py` executes **every output the manual claims** against a real
  interpreter and fails on any mismatch (141 claims through Module Three). This is the
  course's analogue of PHY121's "recompute every number". It exists because the
  source manual's own transcripts were typed rather than captured: see
  `sources/extracted/manual_audit.md`. Where the manual shows spaces as dots, the
  gate derives the dot string from a real run and requires that exact string to be
  present in the page, so a hand-miscounted dot fails the build. Sets are compared as
  sets, never by printed order: Python randomises string hashing per process, so a
  set of strings prints in a different order every run, and only `len()` and
  `sorted()` are reproducible.
- `gates.py` enforces house style: no em or en dashes, no institution branding, the
  pedagogy source unnamed, the reserved colour used only by MUST MEMORISE, and all
  code monospace.

`build/` also holds `manual.css` (the CSC241 palette and box grammar), `render.py`
(Chromium via Playwright, footer via `footerTemplate`), `buildlock.py`, and vendored
`fonts/`.

Only one chat may build this course at a time; `build/.build.lock` enforces it.
Stage commits with `tools/commit_course.sh` from the workspace root, never
`git add -A`.
