# Alert: this manual is currently rendering at 92.9% of its designed size

Left by the CSC241 chat on 2026-07-17. Measured, not suspected. Nothing here was
changed for you: your build files were in flight, so this is a note, not a fix.

## What is wrong

`build/full_manual.pdf` and `build/full_manual_clean.pdf` (212pp) come back with a
body of **8.91pt**. `manual.css:48` asks for **9.6pt**. Every page in the book is
being scaled to **92.9%**.

The 33-page checkpoint in `drafts/` measures a clean 9.60pt, so this crept in with
the later modules rather than being there from the start.

## Why it happens

Chromium's print path scales the **entire document** down to fit its widest box. One
code line too wide for the content area shrinks all 212 pages, including every page
that has no code on it.

It is silent by design. After the shrink nothing overflows, so the layout looks
perfect to every other check: no clipping, no bleed, no warning. The only way to see
it is to measure the rendered font size and compare it to the CSS.

## The two lines doing it

Found by looking for code lines pinned to the content edge in the rendered PDF:

| Page in `full_manual.pdf` | Width |
| --- | --- |
| 36 | 99 chars |
| 167 | 99 chars |

Both are long `System.out.println(...)` string-concatenation lines. At 92.9% a
99-char line exactly fills the box, which puts the full-size limit at roughly **92
characters** for this course's code font (8.4pt mono). Measure it rather than trust
that number: CSC241's limit is 90 at its own settings, and the two courses do not
share a code font size.

Splitting each line in two is the whole fix. In CSC241 the equivalent repair was to
assign the long string to a variable first, then pass the variable.

Expect the page count to **rise** afterwards. CSC241 went from 106 pages to its true
127 once unshrunk. That is the book arriving at its real length, not a regression.

## Worth adding two gates

CSC241 ended up with one on each side of the render, and both earn their place:

1. **Before:** in `gates.py`, no code line over the measured column limit. Catches
   the usual cause precisely, and names the file and line.
2. **After:** in `qa_layout.py`, the body must come back at 9.6pt. Catches the
   effect whatever the cause, which is the one that actually matters, since a
   shrunk book passes every other test.

See `MANUAL_METHODOLOGY.md` section 2b, and `courses/CSC241 - Python Programming
Language I/build/qa_layout.py` for a working version of the second check.

Delete this file once the render measures 9.6pt.
