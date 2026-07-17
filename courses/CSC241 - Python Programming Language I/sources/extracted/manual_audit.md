# Audit of the 224-page course manual (the source)

The 224-page `COV-CSC241` manual is the institution's, i.e. a source we author from,
not a manual of ours. This file records what it contains, where it is wrong, and
what it fails to teach. **Its outputs cannot be trusted**: see the verification
results below.

## Unit index

`PDF page = printed page + 3` throughout (the cover and front matter are unnumbered).
Text extracts cleanly from every page except the cover image (page 1). Full text is
in `manual_text/`, one file per PDF page plus `_full.txt`.

| Module | Unit | Title | Printed p | PDF p |
| --- | --- | --- | --- | --- |
| One | 1 | Overview of Python | 2 | 5 |
| One | 2 | Setting Up Python | 8 | 11 |
| Two | 1 | Python Language Syntax | 15 | 18 |
| Two | 2 | Python Variables and Data Types | 28 | 31 |
| Two | 3 | Python Operators | 40 | 43 |
| Three | 1 | Decision Making in Python | 66 | 69 |
| Three | 2 | Repetitive Structure: Loops and Branching | 83 | 86 |
| Three | 3 | Python Data Structures | 94 | 97 |
| Three | 4 | Data Structures: Sets and Dictionaries | 115 | 118 |
| Four | 1 | Functions in Python | 131 | 134 |
| Four | 2 | Modules and Packages | 144 | 147 |
| Four | 3 | File Handling in Python | 153 | 156 |
| Four | 4 | Exception Handling in Python | 161 | 164 |
| Five | 1 | Python and Databases | 169 | 172 |
| Five | 2 | Python GUI Programming | 188 | 191 |

Back matter: answers to self-assessment questions from printed p203 (PDF 206),
glossary from printed p217 (PDF 220).

## Verification of the manual's REPL transcripts

The manual contains 86 `>>>` statements, 48 of which state an output. Each was
extracted and executed against a real Python 3.13 interpreter, one isolated session
per page.

| Result | Count |
| --- | --- |
| Output matches a real interpreter | 42 |
| **Genuinely wrong or misleading** | **4** |
| Harness artefacts (my per-statement stdout buffering broke the `end=` examples) | 2 |

**42 of 48 are correct.** But the four failures matter, because they establish that
these transcripts were **typed by hand, not captured from a real session**. Any
output in this manual is a claim, not evidence.

### Confirmed defect 1: a fabricated float (printed p61, PDF p64)

The manual prints:

```
>>> INTEREST_RATE = 0.069
>>> balance = 10000
>>> amount = balance * INTEREST_RATE
>>> amount
690.0
```

A real interpreter prints **`690.0000000000001`**. Verified by execution and
confirmed visually against the page image.

This is the single most instructive defect in the source. The transcript immediately
following it (`INTEREST_RATE = 0.072` giving `720.0`) **is** correct, which is what
makes it dangerous: the section reads as a captured session. It also means the
manual silently skips the single most confusing thing a Python beginner meets,
binary floating-point representation, at the exact moment it appears on the page.

**Consequence for our manual:** we teach this head on. Float imprecision must be
introduced before any float output is claimed, or the reader will type our example,
see a different answer, and lose trust in the book.

### Confirmed defect 2: outputs replaced by comments (printed p46, PDF p49)

The manual prints, under "Determine if a number is even or odd":

```
>>> 10 % 2
# Even
>>> 7 % 2
# Odd
```

The actual outputs, `0` and `1`, **are missing entirely**. A comment sits where the
result should be. Confirmed visually. A beginner typing this into the REPL sees `0`
and cannot reconcile it with the book. Worse, `# Even` looks like output, teaching
that Python answers `# Even`. This is a notation-before-use failure in the source:
`#` as a comment marker is being used inside a transcript where the reader has no
way to know it is an annotation rather than a result.

### Confirmed defect 3: alignment taught in a proportional font (printed p58, PDF p61)

The field-width and column-alignment section sets its code and output in a
**proportional font**, not monospace:

```
>>> print(f"{'Item':<10} {'Price':>10}")
Item           Price
```

The entire purpose of `:<10` and `:>10` is to align columns. In a proportional font
that alignment is invisible, so the example cannot demonstrate the thing it exists to
demonstrate. The extracted gap (11 spaces) also disagrees with a real interpreter
(12 spaces), but that difference is unverifiable from a proportional rendering and
is moot next to the presentational failure.

The manual is **inconsistent** about this: the p61 interest-rate transcript is set in
proper monospace. So code font varies page to page.

**Consequence for our manual:** every code block and every transcript is set in
DejaVu Sans Mono (already vendored in `build/fonts/`), with no exceptions. Alignment
examples get a ruler or column guides.

### Note: the manual's keystroke convention

Several transcripts read `>>> print(x) Enter` or `>>> 12 + 2 Enter`, where `Enter`
denotes the keypress rather than code. This is a typographic convention, not a
defect, but it parses as a syntax error and would confuse a novice who types it
literally. Our manual uses a distinct visual key glyph, never an inline word that
could be mistaken for code.

## What the source fails to teach (gap list against the zero-external-sources bar)

Cross-referenced against the idiom inventory the exam actually requires (see the end
of `exam_analysis.md`):

1. **Float imprecision.** Never mentioned, and actively hidden by the p61 defect.
   Required, because `average` in the 2024/25 Q2 program and the BMI comparisons in
   Q3 both produce non-clean floats.
2. **`for`/`else`.** The 2024/25 Q1(c) turns on it. Not taught in Module Three.
   Needs a full introduction before the mock reproduces that question.
3. **The `done` sentinel loop and the split-and-convert loop.** The two idioms that
   carry every part (e) on the 2024/25 paper, worth a quarter of the attemptable
   marks. The manual has no worked treatment of either.
4. **Reading the traceback.** The exam's "identify and fix the errors" parts are
   half the code marks, and the fastest route to them is reading what Python already
   tells you. The manual shows one ValueError in passing (printed p36) and never
   teaches traceback anatomy.
5. **Error ordering.** 2024/25 Q5(b) has a SyntaxError masking a second bug: the
   interpreter never reaches it. Nothing in the manual explains that syntax errors
   precede runtime errors, so a candidate listing "both bugs" cannot explain why
   only one is reported.

Items 1 to 5 are additions our manual must make. They are not padding: each is
directly load-bearing for a specific question on the paper Victor will sit.

## How to reproduce this audit

The REPL extractor and per-page runner live in the session scratchpad; the durable
version belongs in `build/` once authoring starts. The method, which is the part
worth keeping:

1. Extract page text with PyMuPDF to `manual_text/pNNN.txt` plus `_full.txt` with
   `=== PDF PAGE n ===` separators.
2. Parse `>>>` and `...` lines into (statement, claimed output) pairs per page.
3. Execute each page's statements as one session in a **subprocess with a timeout**
   (the manual contains input-driven and loop code that will otherwise hang) and
   with stdin at devnull.
4. Compare only the **first** line of claimed output. Anything beyond it is prose
   the extractor swallowed, not a disagreement.
5. Confirm every surviving disagreement **visually** against a cropped render of the
   page before calling it a defect. Two of the six first-line disagreements were my
   own harness's fault, and one more was a font issue invisible in the text layer.
