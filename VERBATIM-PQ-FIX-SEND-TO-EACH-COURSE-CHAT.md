# Send this to each course chat

Copy everything below the line into each course's chat, one at a time.

**Send to (tick as you go):**

- [x] CSC242 Discrete Structures  <-- SENT 2026-07-22
- [x] IFT222 Computer Architecture and Organisation  (101 sites, worst affected)  <-- SENT 2026-07-22
- [ ] TMC221 Personal Development and Capacity Building  (60 sites)
- [ ] CSC241 Python Programming Language I  (59 sites)
- [ ] DTS224 Data Management I  (15 sites)
- [x] COS221 Computer Programming I (Java)  <-- handled in this chat, do not send
- [ ] PHY121 General Physics II  (check whether it references past questions at all)

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
2. **Audit your course.** Count every site where a past question is referenced (`grep -c 'class="marks"'` finds most of them if you use that markup; check your mocks, worked tests and cram sheets separately, and check module prose that cites a paper).
3. **Rewrite each site** into the three-part form. Add an `AS PRINTED` box style and a `BREAK IT DOWN` box style to your CSS if you do not have them.
4. **Write `qa_verbatim.py`** and wire it into `assemble.py` as a hard gate. It proves, in both directions: every quoted question in the book appears in the transcript character-for-character (normalising only whitespace and typographic quotes), and every question in the transcript appears in the book. One direction catches paraphrase, the other catches quietly dropped parts.
5. **Control-test the gate** (non-negotiable 9): change one word in a quoted question, confirm it fails; drop one part from the book, confirm it fails. Green today is not proof.
6. **Re-run your code/line-width gate AFTER inserting the quotes, not before.** Learned the hard way on COS221: I ran it before the last batch of quoted listings went in, so a 123-char line reached a render and scaled the whole book down to 248 pages at 90.9% of design size. Every other gate passed, because a shrunk book is internally consistent. A quoted listing is new code entering the book, and it is the one kind you cannot reflow freely, so it is exactly where this bites.
7. Re-render, re-run **all** your existing gates, and check the page count moved sensibly. Verbatim quotes are longer than paraphrases, so the book should **grow**. If it shrank, that is the shrink, not a saving. **Re-measure the rendered font size against the CSS** (section 2b) and do not trust the page count on its own.
8. If a quoted listing has a line too wide for your panel, **wrap it where the paper wraps it.** Do not reflow it to taste, and do not straighten the paper's own wrapping: on COS221 the offending line was one the paper itself breaks across two printed lines, so quoting it faithfully and fixing the shrink turned out to be the same edit.
9. Report back: sites fixed, gate control-test results, old and new page count, and rendered title size.

**Two more things COS221 hit that you probably will too:**

- **Check what your quoted listings are actually named.** COS221 had renamed five of the paper's classes (`SquareCalc` became `SquareCalcBroken`, `Main` became `MiddleValueBroken`) to avoid a filename clash that could not happen, because every listing compiles in its own temp directory. A renamed class inside an AS PRINTED box is the same defect as a paraphrased sentence, just in code. Check yours before you quote them.
- **Check the quoted listing is the paper's, not your wrapper.** COS221's Q4 B printed a bare fragment with no class and no `main`; the book had wrapped it so it would compile, and that wrapper then sat inside the quotation. Quote the fragment, and keep the wrapper in the answer where it belongs, labelled as yours.

**Do not republish to `FINAL_MANUALS/` until Victor explicitly signs off** with "we are done" or "go to final" for your course. Standing rules still apply: no version suffix on the published name, no em or en dashes in our prose (the quoted paper is exempt), no institution or pedagogy-source names, footer is course plus author only.
