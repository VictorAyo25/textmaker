# PHY121 — General Physics II — working folder

Everything needed to rebuild or update the PHY121 study manual lives here.
The finished PDF is published to `../../FINAL_MANUALS/`.

```
PHY121/
├── build/      all code + assets (see below)
├── sources/    the raw inputs, grouped (see sources/README.md)
│   ├── slides/       the 5 lecturer decks, in teaching order
│   ├── tests/        CBT test screenshots (test1/, test2/)
│   ├── manual_v1/    the original manual the blend is rebuilt from
│   └── extracted/    text/images pulled out of the manual, regenerable
└── drafts/     work-in-progress PDFs (never the published copy)
```

## Rebuild the whole manual (one command)

```bash
cd build
python assemble.py          # ~5 min: writes build/full_manual_clean.pdf
```

That file is the finished manual (172 pages). Copy it to `../../FINAL_MANUALS/`
only when it is signed off.

**Requirements:** Python 3 with `playwright` (+ `python -m playwright install chromium`),
`pymupdf`, `pillow`. Fonts are vendored in `build/fonts/` so rendering is
self-contained and reproducible.

## What `assemble.py` does

1. Reads the frozen HTML in `build/content/` for every section. Anything not
   frozen is regenerated from `sources/manual_v1/PHY121_Study_Manual.pdf` with a
   structure-aware extractor.
2. Splices in the new Module 5 content and the inline diagrams.
3. Renders with headless Chromium, **twice**, to resolve Contents page numbers
   (chicken-and-egg: the Contents changes the pagination it is describing).
4. Converts Contents links to real page links, strips invisible helper markers,
   and swaps in the cover.

## What you can edit

**All prose in the book is now editable as plain HTML.** The Modules 1-4 /
Foundations text was "frozen" out of the original PDF into `build/content/`
(see below), so those files are the source of truth and edits survive rebuilds.

| To change | Edit this |
|---|---|
| **Foundations text (F.1-F.9)** | `build/content/foundations.html` |
| **Module 1 / 2 / 3 / 4 text** | `build/content/module1.html` … `module4.html` |
| **Part divider pages** | `build/content/partI.html` … `partIX.html` |
| Module 5 teaching content | `build/module5_body.html` |
| Module 5 exercises (S.7) / mock (M.5) | `build/module5_assess.html` |
| The cover | `build/cover.html` |
| Any colour, box style, page layout | `build/manual.css` |
| Module 5 diagrams | `build/make_svgs.py` -> `python make_svgs.py` |
| Modules 1-4 diagrams | `build/make_module_svgs.py` -> `python make_module_svgs.py` |
| Contents entries / book order | the `TOC` list and `assemble()` in `build/assemble.py` |

After editing any of these, just re-run `python assemble.py`.

### How the freeze works
`assemble.py` prefers `build/content/<name>.html` if it exists, and only falls
back to re-deriving from the PDF if it does not. `freeze.py` created those files
once. **You should not normally run `freeze.py` again** — and never with
`--force`, which re-derives from the PDF and would discard your edits. (It
refuses to clobber existing content without `--force`.)

The frozen build was verified to produce text that is byte-for-byte identical to
the reviewed v2, so freezing changed nothing about the output — it only made the
prose editable.

### Adding a Module 6 later
Copy the Module 5 pattern: write the content in a new `module6_body.html`, add a
`part(...)` + section append inside `assemble()`, add its rows to `TOC`, and add
its formulas to the reference additions. Nothing else needs to change.

## What is still NOT editable

**Exercises, mocks and reference (the back matter), plus the two "how to use this
manual" pages**, are 300-dpi **image crops** of the original v1 pages. Their text
is not selectable and cannot be edited. Changing them requires reconstructing
those pages as HTML (the machinery to do it is already here: see `reconstruct.py`
+ `gen_html.py`, which is exactly how Modules 1-4 were done).

**Never delete `sources/manual_v1/PHY121_Study_Manual.pdf`.** Even with every
section frozen, the build still opens it on every run, and it is the reference
the QA scripts diff against to prove no content was lost.

## House rules enforced (see ../../MANUAL_METHODOLOGY.md)

- No em dashes or en dashes anywhere. `python dedash.py` rewrites them; `qa_final.py` fails the build if any survive.
- No mention of the institution, its e-learning platform, or any methodology author's name.
- Every number recomputed independently before it is written down.

## QA before publishing

```bash
python qa_final.py     # blanks, footer numbering, dashes, banned terms
python verify_links.py # every Contents link resolves
```
All must come back clean. Also eyeball the pages; the automated checks cannot
see a bad diagram or an ugly page break.
