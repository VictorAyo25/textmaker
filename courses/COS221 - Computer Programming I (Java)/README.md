# COS221 — Computer Programming I (Java) — working folder

Everything needed to build or update the COS221 study manual lives here. The finished
PDF is published to `../../FINAL_MANUALS/` as
`COS221 - Computer Programming I (Java) - Study Manual.pdf`, and only on explicit
sign-off. No version suffix: the published name never changes, so publishing
replaces the file in place. Versions belong on drafts in `drafts/`.

```
COS221 - Computer Programming I (Java)/
├── build/      all code + assets (fonts vendored)
├── sources/    the raw inputs
│   ├── slides/         13 lecturer decks, 408 slides, Modules 1 to 10
│   ├── exams/          exam_2024_25.pdf, exam_2025_26.pdf
│   ├── course_manual/  CCODeL's official 222-page manual (a SOURCE, see below)
│   └── extracted/      transcripts, exam analysis, source survey, page renders
└── drafts/     work in progress (never the published copy)
```

## Status

**Style signed off. All ten modules written. Both papers solved in full.** Front
matter, Foundations F.1 to F.11, Modules 1 to 10, and every question on both the
2024/25 and the 2025/26 papers, worked end to end. Every listing compiles and runs on a
real JVM and every printed output was captured from one; all gates report zero.

The papers are answered **completely**, not to the rubric: 24/25 says attempt four of
six and 25/26 says one question per section, and both are answered whole. A question
you skip is a topic you can be examined on next year, and the 25/26 paper proves it by
re-asking 24/25's file I/O, inheritance and digit-loops in a new costume.

Still to write: mock papers in both formats; the reference section (formula-free, but
an API card, a keyword index, a method reference and a glossary); the keyword/API
before-use gate (gate 2 below, still held by hand).

## Build it

```bash
cd build
python check_code.py        # compile + run EVERY listing        <- do this first
python assemble.py          # ~2 min: writes build/full_manual_clean.pdf
python qa.py                # gate the rendered PDF: every count must be zero
python qa_firstuse.py       # gate the "no external sources" promise
```

`check_code.py` compiles ~90 programs and takes a few minutes; pass a section name
(`python check_code.py module6`) while authoring, and run it bare before a build.

## Authoring a listing: write real Java, then generate the markup

Do **not** hand-write the `<span class="l">` markup. Author the snippet as a real
`.java` file, compile and run it, and let `hl.py` produce the markup:

```bash
python hl.py Foo.java --run Foo                      # a program with checked output
python hl.py Bad.java --compile Bad --error "..."    # must FAIL to compile
python hl.py Frag.java --frag                        # a fragment, still must compile
python hl.py Skel.java --nocheck "why not checked"   # a skeleton
```

Mark a line by putting `/*@good*/` or `/*@bad*/` anywhere on it; the marker is
stripped from the emitted source, and being a comment it never reaches javac either.

This is not convenience, it is the fidelity rule. Generating the markup from the file
that actually ran makes "the source in the book is the source that ran" true by
construction rather than by care. Hand-writing it produced the same silent bug four
times: `class="l" class="bad"` is a duplicate attribute, browsers keep the first and
`dict(attrs)` keeps the last, so the line vanished from the compiled source and the
listing ran minus one line with quietly different output.

**Requirements:** Python 3 with `playwright` (+ `python -m playwright install
chromium`) and `pymupdf`; a **JDK** on PATH (built against Temurin 17) for
`check_code.py`. Fonts are vendored in `build/fonts/`, so a render never depends on
what happens to be installed on the machine.

## This manual is AUTHORED, not rebuilt

The important difference from PHY121. PHY121 had `sources/manual_v1/`, a prior manual
**of ours**, so its build reproduced that manual verbatim and needed structure-aware
extraction plus a word-level fidelity audit to prove nothing was lost.

COS221 has no such thing. The 222-page manual in `course_manual/` is the
institution's, i.e. an input to learn from, not an artifact to reproduce. So:

- **Do not** port `reconstruct.py`, `struct_extract.py`, `recon_back.py`, `freeze.py`
  or the fidelity audits from PHY121. There is nothing to be faithful to, and nothing
  to reconstruct from: `build/content/*.html` **is** the manual, written by hand.
- **Ported instead:** Chromium render, vendored DejaVu fonts, the 2-pass Contents
  resolve, named-to-GoTo link conversion, marker stripping, and the QA gates.

## What assemble.py does

1. Concatenates `content/*.html` in the `ORDER` list at the top of the file.
2. Injects an invisible marker before every part and section heading.
3. Renders, reads back which page each marker landed on, rebuilds the Contents with
   real page numbers, and re-renders until pagination stops moving. The Contents
   changes the pagination it describes, so this iterates to a fixed point.
4. Converts Contents links to real page links (Chromium emits *named* destinations,
   which many viewers ignore), strips the markers out of the text layer, and swaps the
   cover into page 1.

Two things worth knowing:

- The Contents is **derived from the headings**, never hand-listed, so it cannot drift
  from the content. Add a section and it appears; `assemble.py` fails loudly if an
  entry cannot be resolved to a page.
- Page 1 is rendered as an empty **cover slot** and swapped for `cover.pdf` at the end.
  The slot must exist *during* the render: splicing the cover in afterwards shifts
  every body page down by one, so each footer reads one less than the page it sits on,
  and the Contents is off by one to match. That bug shipped once here and the gate now
  catches it.

## The render barrier (read before touching render.py)

`render.py` waits for `document.fonts.status === 'loaded'` before taking the PDF, and
then **verifies the faces actually loaded**. Do not weaken this to `networkidle`.

Network-quiet is not fonts-loaded. Without the barrier, Chromium measures every line
in fallback metrics, so it wraps differently and the whole book paginates differently.
Rendering identical HTML four times gave **117, 166, 166, 166** pages. The page count
was a lottery.

The reason this is worth a section: a corrupted render **passes every gate**. It comes
out *shorter* (fallback text is narrower), with sequential footers, no blank pages, and
a Contents that agrees with itself. The PDF is internally consistent; it is just
consistently wrong. `qa.py` cannot see it, because `qa.py` only asks whether the PDF
agrees with itself. This is exactly how PHY121 v2 shipped at 64 pages instead of 148.

PHY121 learned this and has the barrier. Each new course copies `render.py` from the
last, so the fix does not propagate itself: **COS221 lost it in the port** (restored
2026-07-17). Grep a new course's `render.py` for `fonts.status` before believing any
page count it prints.

## Course facts

- Lecturer: Mr. Otavie Okuoyo. Omega semester, 3 credit units, 3-hour written exam.
- Deck numbering matches the course manual exactly: 13 decks = 13 units over Modules 1
  to 10. No PHY121-style off-by-one quirk. Verified from the decks' own title slides,
  not from filenames.
- The course was retitled between sessions: "Object-Oriented Programming (Java)" in
  2024/25, "Computer Programming I (Java)" in 2025/26. Same code, COS221.
- Where the course manual and the decks disagree (Operators/Operations, Parameter
  Passing/Testing, Strings/Data Structures), **the deck wins**. The course manual's own
  contents page has a broken bookmark: it is a fallible source.

## The exam (see `sources/extracted/exam_analysis.md`)

The format changed between years but the skills did not. Both papers are 70 marks over
3 hours and test exactly four things: **define**, **debug**, **dry run**, **write a
program**. Teach the four skills, not a paper format, and write mocks in both shapes.

- 24/25: "attempt any four (4)", six questions at 17.5 marks.
- 25/26: three sections, one question from each, 20 + 25 + 25.

The 25/26 paper is written long-form, **not** a CBT multiple-choice test, so the manual
trains writing Java on paper, tracing by hand, and finding bugs, not recognising right
answers. Recurring obsessions: `JOptionPane` for all I/O, nested if-else insisted on
over separate ifs, no collection classes, parallel arrays, loop conversion.

**Every question on both papers gets solved in full**, including the ones a candidate
would skip in the hall: a question you skip is still a topic you can be examined on.

## Decisions worth not re-litigating

- **Module numbers follow the lecturer**, 1 to 10, so this book and the course always
  mean the same Module 4.
- **The lecturer's order is not a teach-from-zero order.** Arrays are Module 8, yet both
  Section A questions are array problems and arrays are the natural vehicle for loops in
  Module 4; `JOptionPane` is demanded from Section B but is a method call on a library
  class. Since nothing may be used before it is taught, **Foundations** carries those
  concepts early and honestly (F.10 arrays, F.11 JOptionPane), each pointing at the
  module that develops it in full. Modules then deepen, never re-introduce.
- **Palette:** terminal dark-ink. Cyan `#0891b2` is **reserved for MUST-MEMORISE** and
  appears nowhere else, ever.
- **"Dry run" is the lecturer's own term**, which is why the trace-table box is called
  DRY RUN, and why F.9 teaches the technique before any module needs it.

## Hard QA gates for this course

1. **Every snippet compiles and runs** (`check_code.py`). This is the local form of the
   house rule "recompute every number independently". A printed output nobody executed
   is a wrong constant, not a typo. Every listing must declare a contract:

   | Attribute | Meaning |
   |---|---|
   | `data-run="Cls"` | compile as `Cls.java`, run, compare stdout with the box's `.out` block |
   | `data-run` + `data-stdin="..."` | as above, feeding stdin |
   | `data-compile="Cls"` | must **fail** to compile (a planted bug); `data-error="..."` asserts the message |
   | `data-frag="1"` | a fragment: wrapped in a class + main, must still compile |
   | `data-nocheck="reason"` | excluded, and the reason is printed in the report |

   Silence is never a way out: a listing with no attribute is a failure.

   The same gate closes the vocabulary of `<pre>` classes to exactly `src`,
   `src nonum` and `out`. It only *sees* `class="src..."`, so inventing a fourth
   class lets the snippet inside escape checking entirely **and** render unstyled,
   because `manual.css` styles only these. Both failures are silent, and it happened
   once (a `class="sig"` skeleton), so the set is now enforced.

2. **Keyword/API before use** (`qa_firstuse.py`, run after `assemble.py`). The manual
   must be sufficient with **no external sources**, and that promise is worthless
   asserted: it is the kind of claim that silently rots as a book passes 200 pages. Two
   rules, both measured against the *assembled* HTML, so the audit reads the book in
   the order a reader does:

   - **Nothing is used without being named.** An API that appears only inside listings
     and is never written in the prose is a hole: the reader meets it, cannot look it
     up, and has nowhere to go.
   - **A mock teaches nothing.** A mock, or a solved past paper, *tests* what the
     modules taught. So an API whose first appearance in the whole book is there is one
     the reader is examined on and was never shown.

   It found ten real holes on first run, including `Files.write()` and
   `Integer.MAX_VALUE` used in listings but named nowhere in the prose. `data-compile`
   listings are skipped: a planted bug introduces nothing.

3. **`qa.py`**: no em/en dashes, no institution or platform or methodology names, no
   marker text left behind, footer numbering, Contents accuracy, no near-blank pages,
   no text outside the margins, no orphaned section headings. Every count zero.

See `sources/extracted/` for the paper transcripts, the cross-year exam analysis, and
the source survey.
