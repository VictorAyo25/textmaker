FINAL_MANUALS — signed-off study manuals only. One per course.
Work in progress belongs in that course's drafts/ folder, never here.

Published names carry NO version suffix: one current manual per course, one
filename that never changes, so publishing replaces it in place and no link or
printout goes stale. Version numbers (v2, v4) are for drafts/ only. The history
below records what changed; git holds every superseded copy.

-------------------------------------------------------------------------------
COS221 - Computer Programming I (Java) - Study Manual.pdf   333 pp   updated 2026-07-17
-------------------------------------------------------------------------------
COS221 Computer Programming I (Java), complete manual, Modules 1 to 10.

Contents: Foundations F.1-F.11, Modules 1 to 10, both past papers solved in full
(2024/25 six-of-which-attempt-four, and 2025/26 three-sections), mock papers in
both of those shapes (Mock A and Mock B) with solutions, and reference R.1-R.4
(exam API card, method reference by class, keyword index, glossary). 126 clickable
Contents links, real selectable text throughout.

Unlike PHY121 this manual was AUTHORED, not rebuilt: there was no prior manual of
ours to reproduce, so content/*.html is the book, written by hand. Every one of the
216 code listings was compiled and run on a real JVM (Temurin 17), and every printed
output was captured from that JVM, never typed. Withheld-answer listings on the mock
papers still run: the gate proves each one's answer exists and matches, elsewhere in
the book.

Four scripted gates, all green at publish:
  - check_code.py: every listing compiles and runs; every claimed output diffed
    against the JVM. 216 listings, 0 failures.
  - qa_firstuse.py: the "no external sources" promise, measured not asserted. Nothing
    is used before the prose names it, and no API is first met inside an exam.
  - qa_reference.py: the reference and the book agree both ways. Everything the
    listings use is documented; nothing documented goes unused.
  - qa.py: no em/en dashes, no institution or platform or methodology-author names,
    footer numbering sequential, all 126 Contents links resolve, no near-blank pages,
    nothing outside the margins, no orphaned headings, the body renders at its design
    size (the shrink guard, below), and no code spills past its panel.

Where the course's own materials were wrong, the book shows the run rather than
repeating the error: the int-limit table that printed the overflow value as the
limit, the printf half-up rounding folklore (disproved against 99,999 values), the
Math.pow inexactness myth, and the "Swing hangs without System.exit" myth were each
tested on the JVM and corrected with the measurement in view.

What changed from the first render of the same day (298 pp): THE SHRINK. Chromium
scales the whole document down to fit its widest box, so two 99-character
System.out.println lines were forcing the render to 92.9% of its design size: the
body came back at 8.91pt where the CSS asks 9.6pt, on every one of the 298 pages.
Nothing overflowed after the shrink, so every gate then in place passed it. The
over-long lines were wrapped (verified to compile and print identically), the book
returned to full size and to its true 333 pages, and two guards were added so this
cannot recur silently: a pre-render column cap in check_code.py that names the file
and line, and a rendered-font-size plus panel-overflow check in qa.py that catches
any cause. The 298 pp render was superseded the same day; git holds it.

To rebuild or update:  see "courses/COS221 - Computer Programming I (Java)/README.md"
                       (cd build && python assemble.py)

-------------------------------------------------------------------------------
CSC241 - Python Programming Language I - Study Manual.pdf   182 pp   updated 2026-07-18
-------------------------------------------------------------------------------
CSC241 Python Programming Language I, complete manual, Modules 1 to 5.

Contents: Modules 1 to 5 (fifteen units plus a Strings unit the course lacked but
the exam needs), self-assessment answers, the real 2025/2026 paper solved in full,
and three mock examinations solved in full. Every one of the exam's six questions
has a home in the coverage table, on both the 2024/25 and 2025/26 papers. 35
clickable Contents links, real selectable text throughout.

Like COS221 this manual was AUTHORED, not rebuilt: the 224-page course manual is
the institution's, a source, so content/*.html is the book, written by hand. Every
claimed output was produced by a real Python interpreter and captured from the run,
never typed: 367 claims, 0 mismatches. Set-valued outputs are compared as sets, not
by printed order, because Python randomises string hashing per process.

What changed from the first render of the same day (144 pp): THE REAL 2025/2026 PAPER.
The student supplied it (seven phone photos) after the first edition shipped, and it
broke the shape the manual was built around. The 2024/2025 paper was rigid: five parts
a question, each 3.5 marks, one module per question. The 2025/2026 paper varies the
marks per part (1 to 10.5), varies the number of parts, and mixes topics inside a
question. So the manual now teaches to the topics (unchanged) and drills both shapes:
Mocks One and Two in the 24/25 shape, and the newly added solved real paper plus Mock
Three in the 25/26 shape. The paper also carries a defect in its own Q6(c) sample (it
prints 10546.90 where math.pi gives 10547.79); the solved section shows the run and
states the true figure, the way this book treats every course-material error. Filling
the paper's demands added SQL UPDATE/DELETE/COUNT/MAX/AVG and executemany, lists inside
lists, the del keyword, and a fifth benefit of modularizing. The 144 pp render was
superseded the same day; git holds it.

Four scripted gates, all green at publish:
  - verify_code.py: every claimed output diffed against a real interpreter. 367
    claims, 0 failures.
  - gates.py: no em/en dashes, no institution or methodology-author names, the
    reserved colour used only by MUST MEMORISE, all code monospace, and no code
    line over the width that fits (a longer one shrinks every page in the book).
  - qa_firstuse.py: the "no external sources" promise, measured not asserted.
    Nothing is used before the prose names it, and no API is first met in a mock
    (this caught executemany on its first run, which is why Module Five now teaches it).
  - qa_layout.py: the body renders at its designed size (not silently scaled to
    fit an over-wide line), nothing outside the margins, no box cut by a page break
    that would have fitted whole, the Contents links resolve to the pages they name.

The Contents is generated, never typed: its page numbers are read back out of the
rendered book, so they cannot drift from it. Building it surfaced a layout fault
that had stranded four of six module-divider pages, now fixed.

To rebuild or update:  see "courses/CSC241 - Python Programming Language I/README.md"
                       (cd build && python assemble.py)

-------------------------------------------------------------------------------
DTS224 - Data Management I - Study Manual.pdf       85 pp   updated 2026-07-18
-------------------------------------------------------------------------------
DTS224 Data Management I (a databases course), complete manual, Modules 1 to 5.

Contents: How-to (box legend), Module 1 Information Management and Database Systems,
Module 2 Conceptual Models (ER, EER, XML/JSON, worked models), Module 3 Logical
Design (relational model, keys, integrity, ER-to-logical mapping), Module 4
Functional Dependencies and Normalization (1NF to BCNF), Module 5 Relational Algebra
and SQL, the real 2025/2026 paper solved in full, and three mock examinations solved
in full. Around 30 hand-drawn inline diagrams (crow's-foot ER, EER specialization
with the four completeness/disjointness cases, FD diagrams, schema listings, and
architecture figures). 29 clickable Contents links, real selectable text throughout.

Like CSC241 this manual was AUTHORED, not rebuilt: the 182-page course manual is the
institution's, a source, so content/*.html is the book, written by hand. DTS224 is
the renamed CSC214, so all seven CSC214 past papers (2015/16 through 2025/26) are
valid practice and every one is drilled; the two priority papers (2024/25 and
2025/26) have all six questions cited in the coverage table. Content the older "High
Performance" papers carry but the 12-unit syllabus does not (data mining, concurrency
and locking, ODBC, NoSQL, hash-file organisation, partitioning) is still solved and
taught enough to pass, with both the content AND the question labelled "Not in
syllabus". Every normalization, relational-algebra expression, and SQL result was
worked independently, never copied from the source, whose own answers are unverified.

No question escapes: every past-paper question, every test, the practice deck, and
every in-text self-assessment is solved in the book, each carrying a provenance chip
naming its source, and the coverage gate fails the build on any priority-paper
question left uncited.

Five scripted gates, all green at publish:
  - gates.py: no em/en dashes, no institution or methodology-author names, the
    reserved colour (emerald) used only by MUST MEMORISE, all code monospace, and no
    code line over the width that fits (a longer one shrinks every page in the book).
  - qa_coverage.py: the no-escape rule, measured not asserted. Both priority papers
    fully cited Q1 to Q6, the book diagram-rich; control-tested to fail on a removed
    citation.
  - qa_firstuse.py: teach before use. Every declared notation (abbreviations like
    PK/FK/DBMS, the relational-algebra symbols, named EER terms) is introduced before
    the reader meets it, and none is first introduced inside a mock. This pass caught
    two real gaps: PK/FK were used in schema listings but never spelled out, and the
    "subtype discriminator" was promised in a unit's objectives but defined only in a
    mock answer; both are fixed. Control-tested to fail when an introduction is removed.
  - contents.py: the generated Contents, its page numbers read back out of the
    rendered book so they cannot drift, every row's link resolving to the page it names.
  - qa_layout.py: the body renders at its designed 10.5pt (not silently scaled to fit
    an over-wide line), nothing outside the margins, no box cut by a page break that
    would have fitted whole.

To rebuild or update:  see "courses/DTS224 - Data Management I/README.md"
                       (cd build && python assemble.py)

-------------------------------------------------------------------------------
PHY121 - General Physics II - Study Manual.pdf      148 pp   updated 2026-07-17
-------------------------------------------------------------------------------
PHY121 General Physics II, complete manual, Modules 1 to 5.

Contents: Foundations F.1-F.11, Modules 1 to 5 (eighteen units), full solutions
S.1-S.7, mock papers M.1-M.5, reference R.1-R.4. Module 5 is Maxwell's Equations
and Electromagnetic Waves. 55 clickable Contents links, real selectable text
throughout including every table.

What changed from the previous edition (16 July, 150 pp): PHYSICS ERRORS.

That edition reproduced the original manual's wording faithfully, and the
original was wrong in places. Reproducing an error faithfully still ships the
error. A full audit of the teaching text, the solutions, the mocks and the
reference sections found and fixed:

  - Dipole potential energy printed U = pE cos(theta), missing its minus sign.
    As printed, an aligned dipole sits at maximum energy, contradicting the
    box's own note. It is U = -pE cos(theta).
  - Faraday's law example computed the flux change as initial minus final and
    landed on -120 V. The flux fell, so the change is -0.06 Wb and the emf is
    +120 V. This was the only example exercising the minus sign the manual
    devotes a MUST-MEMORISE box to, and it taught the sign backwards.
  - Both Kirchhoff examples said "anticlockwise traverse" while their diagrams
    and every sign in their working were clockwise. A student following the word
    instead of the working gets every sign inverted.
  - Total charge given as 26.6 uC, from carrying a rounded 2.22 uF forward. The
    exact 20/9 uF gives 26.7 uC. This is the early-rounding mistake the manual's
    own trap box warns against.
  - The EM spectrum chart put radio at 10^4 Hz; c/lambda gives 10^5.
  - Smaller reasoning and reference defects: an equipotential described as
    "V = 0 along it" (V is constant, not zero), a path width quoting the radius
    as the diameter, a stationary charge explained by "sin 0 = 0" when the issue
    is that v = 0, a phantom "CASE 5", and four formulas missing from R.1.

The three loop-arrow diagrams were redrawn as vector art. Their arrowheads were
rotated ~80 degrees off the arc tangent, pointing across the loop instead of
along it, which hid the clockwise/anticlockwise contradiction above.

Every correction is recorded in build/corrections.py with its rationale, applied
at freeze time so it cannot be lost by re-deriving from the original.

Verified: no blank pages; footer numbering sequential; all 55 Contents links
resolve; every number recomputed independently; no em/en dashes; no institution
or methodology-author names. Structural gates (bold, sub/superscript, blanks,
lists, tables, figures) all above floor. Every correction was then independently
re-checked by an adversarial pass, which caught two that had fixed the answer
while leaving the working beneath it describing the old one.

The two preceding editions were both withdrawn as defective: the 16 July one for
the physics errors above, and the one before it (163 pp) for missing fill-in
blanks and dropped bold. Both remain in git history if a copy is ever needed
(the 163 pp edition at commit 2312940).

To rebuild or update:  see "courses/PHY121 - General Physics II/README.md"
                       (cd build && python assemble.py)
