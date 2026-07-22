# Send this to each course chat

Copy everything below the line into each course's chat, one at a time.

**Send to (tick as you go):**

- [x] CSC242 Discrete Structures  <-- SENT, and re-sent with the third gate direction. Up to date, no further send needed.
- [x] IFT222 Computer Architecture and Organisation  <-- SENT, and re-sent with the third gate direction. RETROFIT DONE, 138pp -> 185pp, seven gates. Its lessons are folded in below.
- [x] COS221 Computer Programming I (Java)  <-- DONE in this chat. 333pp -> 347pp, published, three gate directions.
- [ ] TMC221 Personal Development and Capacity Building  (60 sites)  <-- OUTSTANDING
- [x] CSC241 Python Programming Language I  <-- SENT 2026-07-22
- [ ] DTS224 Data Management I  (15 sites)  <-- OUTSTANDING, and the only unpublished course: doing it before it ships saves a republish
- [x] PHY121 General Physics II  <-- NOT APPLICABLE (Victor, 2026-07-22). Does not need it; do not send.

Delete this file once the last one is sent.

---

A reader reported a defect that affects every manual we have built, including yours. Read `MANUAL_METHODOLOGY.md` section 4c (just added, it is binding) before you do anything else, then fix your course.

**The defect:** wherever a real past exam question appears in the manual, we restate it in our own compressed words while presenting it as the paper. Example from IFT222 24/25 Q1(a). The paper actually reads:

> Consider three (3) floating point numbers X, Y and Z stored in registers based on the IEEE 754 Single precision floating point format. X = C1400000h, Y = 42100000h, Z = 41400000h. Convert X, Y and Z to decimal numbers and determine which of the following is true. **9mks**

The book said: "X = C1400000H, Y = 42100000H, Z = 41400000H are stored in IEEE-754 single precision. Convert each to decimal and test (i)...". Same substance, different sentence, and the student reads it as the paper.

**Why it matters:** the student is training pattern recognition for the hall. Paraphrasing strips the examiner's phrasing habits, the real part numbering, the exact mark text, the padding words, and the ambiguity they must resolve under time pressure. It hands them the arithmetic having already done the harder half, comprehension, for them. It also silently launders the paper's own typos and contradictions into clean prose, destroying evidence the student needs. They end up revising against a question that does not exist.

**The rule, now non-negotiable 10.** Anywhere a real past question is referenced, anywhere in the book (solved papers, mocks built from real questions, worked tests, cram sheets, a module saying "this was asked in 24/25"), it becomes a three-part unit:

1. **AS PRINTED** — quote it verbatim in a dedicated box, visibly marked as the examiner's words. Exact wording, exact part numbering (`a.`, `i.`, `ii.`), exact casing and symbols (`C1400000h`, not `C1400000H`), exact mark text (`9mks`, not "(9 marks)"). House style yields here: this is a quotation of an external document, not our prose, so the paper's own phrasing stays. Any typo, contradiction or ambiguity **stays in**, with your note *after* the quote flagging it. Never silently repair a paper.
2. **BREAK IT DOWN** — before the answer, unpack it in the student's shoes: what am I given, what is actually being asked (the instruction verb matters, "determine which is true" is not "convert"), what do the marks tell me about expected depth, which unit teaches this, where is the trap.
3. **The answer.** Your existing Given/Find/Formula block belongs here and does **not** substitute for step 2.

**Mocks you invented are different.** They have no transcript, are not quoted, and get no AS PRINTED box. Only mark something AS PRINTED if it genuinely is printed. Where a mock deliberately mirrors a real question's shape, say so and cite the paper rather than implying it is that paper's wording.

**What to do, in order:**

1. **Transcribe each past paper verbatim** into `sources/exams/transcripts/<paper>.txt`. The papers are photographs, so this is by eye and it is the one input no machine can check. Go slowly, re-read the image against your transcript once, and **never tidy while typing**. A transcript you paraphrased into is a gate that certifies your paraphrase, which is the original defect wearing a gate's clothes.
   - **Reject any OCR text layer, even if one exists.** IFT222's 23/24 scan had one, and it read "1½mks" as "12mks", turned truth-table cells into Korean, and scrambled the reading order. Render the pages to images and read them yourself.
   - **Zoom before trusting a glyph.** Count hex digits at high magnification. To tell a hyphen from an en dash, measure it against a known hyphen on the same line. Photos may be rotated.
   - **Do not straighten the paper's own line breaks**, especially inside listings. COS221 flattened superscripts to `^3`, dropped a degree sign, and split a hyphenated word by rewrapping. Its own gate caught all four, but only because the quotes were right and the transcript was wrong; had it been the other way round the gate would have blessed them.
2. **Audit your course.** Count every site where a past question is referenced (`grep -c 'class="marks"'` finds most of them if you use that markup; check your mocks, worked tests and cram sheets separately, and check module prose that cites a paper).
3. **Rewrite each site** into the three-part form. Add an `AS PRINTED` box style and a `BREAK IT DOWN` box style to your CSS if you do not have them.
4. **Write `qa_verbatim.py`** and wire it into `assemble.py` as a hard gate. It needs **four** directions. Two is the obvious design and it is not enough:
   - **paraphrase** — every quoted question in the book appears in the transcript character-for-character (normalise only whitespace and typographic quotes, never words);
   - **dropped part** — every question in the transcript is quoted somewhere in the book;
   - **prose citation** — in any teaching box whose provenance chip cites a paper, every run inside quotation marks is verbatim too;
   - **line structure** — every quoted LISTING matches the paper line for line. All three checks above compare whitespace-collapsed text, so all three are blind to a listing whose lines were joined or re-split: every word is still present and in order. The reader is not blind to it, and where a paper NUMBERS the lines of a snippet and asks which line is wrong, a joined line silently renumbers the expected answer. COS221 and IFT222 found this independently.
   Directions 3 and 4 are the ones you will not think of. Directions 1 and 2 both work from the AS PRINTED boxes, so both are structurally blind to a teaching site that cites a paper but has no such box. COS221 published with two misquotes of exactly this kind, one dropping "(from i onward)" from inside quotation marks and one lowercasing the paper's own quoted term, then republished. IFT222 hit the same gap from the other side and added a discovery check: a worked example whose chip cites a paper must have a quote above it. Take whichever fits your book; do not ship with only two.
5. **Control-test the gate, each direction separately** (non-negotiable 9): change one word in a quoted question; drop one part from the book; change one word inside a prose citation; join two adjacent lines of a quoted listing leaving every word intact. Confirm each fails on its own. Note that most questions end up quoted **twice** (once where taught, once in the solved paper), so deleting one copy does not test coverage: pick a question quoted exactly once to fire the dropped-part check.
5b. **Watch for quote-pairing artifacts** when you scan prose for quotation marks. A regex like `"([^"]+)"` pairs the CLOSING quote of one quotation with the OPENING quote of the next and reports the ordinary prose between them as a misquote. Five of COS221's seven initial reports were phantoms from this. Split the text on the quote character and take the odd-indexed runs instead.
6. **Re-run your code/line-width gate AFTER inserting the quotes, not before.** Learned the hard way on COS221: I ran it before the last batch of quoted listings went in, so a 123-char line reached a render and scaled the whole book down to 248 pages at 90.9% of design size. Every other gate passed, because a shrunk book is internally consistent. A quoted listing is new code entering the book, and it is the one kind you cannot reflow freely, so it is exactly where this bites.
7. Re-render, re-run **all** your existing gates, and check the page count moved sensibly. Verbatim quotes are longer than paraphrases, so the book should **grow**. If it shrank, that is the shrink, not a saving. **Re-measure the rendered font size against the CSS** (section 2b) and do not trust the page count on its own.
8. If a quoted listing has a line too wide for your panel, **wrap it where the paper wraps it.** Do not reflow it to taste, and do not straighten the paper's own wrapping: on COS221 the offending line was one the paper itself breaks across two printed lines, so quoting it faithfully and fixing the shrink turned out to be the same edit.
9. Report back: sites fixed, gate control-test results, old and new page count, and rendered title size.

**Two more things COS221 hit that you probably will too:**

- **Check what your quoted listings are actually named.** COS221 had renamed five of the paper's classes (`SquareCalc` became `SquareCalcBroken`, `Main` became `MiddleValueBroken`) to avoid a filename clash that could not happen, because every listing compiles in its own temp directory. A renamed class inside an AS PRINTED box is the same defect as a paraphrased sentence, just in code. Check yours before you quote them.
- **Check the quoted listing is the paper's, not your wrapper.** COS221's Q4 B printed a bare fragment with no class and no `main`; the book had wrapped it so it would compile, and that wrapper then sat inside the quotation. Quote the fragment, and keep the wrapper in the answer where it belongs, labelled as yours.

**Two more, from IFT222's retrofit (138pp to 184pp):**

- **Scope the house-style dash exemption by masking, not by disabling.** The quoted paper may contain em or en dashes, which our prose may not. Blank out the declared quote regions (replace with spaces, so error offsets still line up), run the dash checks on what remains, and print the exempt count every run. Branding stays global: you may transcribe a paper's institution identity block into the transcript for provenance, but it must never reach the book.
- **CSS trap for the AS PRINTED box.** A hanging-indent label (`padding-left` plus a negative `text-indent`) needs `text-indent:0` on the inline-block label itself. `text-indent` inherits, and an inline-block is a block container, so the label takes the negative indent a second time and renders outside the page margin.
- Expect roughly **+33% pages** (IFT222), though it varies a lot with how much of your book is past papers (COS221 grew 4%). Page FILL should improve or hold, not worsen. Check it.

**Do not republish to `FINAL_MANUALS/` until Victor explicitly signs off** with "we are done" or "go to final" for your course. Standing rules still apply: no version suffix on the published name, no em or en dashes in our prose (the quoted paper is exempt), no institution or pedagogy-source names, footer is course plus author only.
