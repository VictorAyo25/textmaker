FINAL_MANUALS — signed-off study manuals only. One per course.
Work in progress belongs in that course's drafts/ folder, never here.

Published names carry NO version suffix: one current manual per course, one
filename that never changes, so publishing replaces it in place and no link or
printout goes stale. Version numbers (v2, v4) are for drafts/ only. The history
below records what changed; git holds every superseded copy.

-------------------------------------------------------------------------------
INS224 - Systems Analysis and Design - Study Manual.pdf   101 pp   published 2026-07-23
-------------------------------------------------------------------------------
INS224 Systems Analysis and Design, a complete manual for the current three-hour
paper: answer ONE question in Section A and ANY THREE in Section B. Course lineage
CSC317 -> INS224 (older papers and the 24/25 Alpha sitting are printed as CSC317).

Contents: How-to + Exam-at-a-Glance, Modules One to Six (the analyst and the life
cycle; requirements and use cases; data flow diagrams; entity-relationship
diagrams; UML class, object-oriented concepts, activity and sequence diagrams;
design, architecture and delivery), a Reference part (a one-page notation legend
and the must-memorise list), BOTH the 2025/2026 and 2024/2025 papers fully worked
(each question quoted As Printed, then Broken Down, then answered), and Mock
Examinations One to Three (question paper + answers), each built to the exact shape
of the 25/26 paper with fresh scenarios. About 15 hand-drawn inline diagrams plus
ten module dividers.

MID-BUILD, the lecturer replaced the 86-page course text with a 117-page one that
now covers ERD, class, UML, activity and sequence diagrams and the object-oriented
concepts. The manual was reconciled to it: the "Not in the course text" chip was
removed everywhere except Module Six (client-server tiers, hardware architecture,
system acquisition, interface design, relational database design), which the text
still does not carry. One notation mismatch is flagged throughout: the text draws
ERDs in Chen style (diamonds and ovals) while the exam asks for the Information
Engineering style (the crow's foot); the manual teaches both and says which the
paper wants.

AUTHORED, not rebuilt: the institutional text is a source, content/*.html is the
book, written by hand. Both worked papers are photograph scans with no reliable
text layer and were transcribed BY EYE into sources/exams/transcripts/, read twice;
the paper's own typos ("Categories UML diagrams", "describe it function", mixed
"Marks/marks/Mark" mark tokens) are kept in as evidence, never silently repaired.

Six scripted gates, all green at publish, each control-tested:
  - gates.py: no em/en dashes in our prose (24 quoted-paper regions exempt by
    masking, not by disabling), no institution or pedagogy-source names, the
    reserved emerald reserved to MUST-MEMORISE only, no code line over 87 columns.
  - qa_verbatim.py: every past question is quoted as the examiner printed it or not
    at all. 12 of 12 questions across the two papers match their transcripts
    character for character, quoted whole, with the paper's own line breaks kept.
    Control-tested: a one-word paraphrase fails it.
  - qa_coverage.py: both priority papers (25/26 and 24/25) cite every question One
    to Six via a worked-answer chip, and the book stays diagram-rich (15 inline
    figures, floor 13). Control-tested both ways: a dropped citation and a hidden
    figure each fail it.
  - qa_firstuse.py: teach before use. All 14 declared notations (SDLC, RAD, OOD,
    DFD, ERD, PK, FK, UML, OOP, ...) are introduced before use and none first in a
    mock.
  - contents.py: all 38 Contents rows resolve to a page carrying that heading and
    the printed number matches that page's own footer, through the cover merge.
  - qa_layout.py: body renders at its design size (10.50 pt, no Chromium shrink),
    nothing outside the margins, no box cut by a page break that could have fitted
    whole, and every short page is a forced divider break.

Palette: indigo for teaching, a reserved emerald for MUST-MEMORISE, an amber chip
marking the topics the course text does not carry, and a graphite As-Printed bar
for the examiner's own words.

KNOWN LIMIT at publish, recorded honestly: the gates cover house style, notation
order, verbatim quotation, priority-paper coverage, Contents and page geometry.
They do not read prose; a full end-to-end read for repetition, tonal drift and
concept-level gaps has NOT been done on this edition. The 2025/2026 and 2024/2025
papers are the two solved in full; the older CSC317 papers (2018/2019 to 2022/2023)
and the two CBT tests are drawn on for teaching and mocks but are not each solved
verbatim end to end.

To rebuild or update:  cd "courses/INS224 - Systems Analysis and Design/build"
                       && python assemble.py

-------------------------------------------------------------------------------
TMC221 - Personal Development and Capacity Building - Study Manual.pdf   89 pp   updated 2026-07-19
-------------------------------------------------------------------------------
TMC221 Personal Development and Capacity Building, complete manual across the
four lecture decks: Goal Setting, Positive Thinking and Creative Problem-Solving
(the W.I.S.E. Model), Personal Branding and Strategic Positioning, and Systems
for Sustainable Success (the seven Kits).

This is a non-computational RECALL course, so the manual is a drill bank. Brief
from Victor: cover every single idea, concept, acronym and datum from the decks,
and test every area of every slide in any style except plain theory. The five
drill boxes mirror the real computer-based test exactly: Fill in the Gap,
Match-up, Pick (single and multiple response), True or False, and Cloze scenario.

Contents: How-to + course-at-a-glance, Modules One to Four (teach every slide
fact, then drill it), the real 30-question TMC test solved in full, three mock
examinations (20 questions each, all five styles, weighted across the four
lectures, fully answered), and a Master Cram Sheet. About 110 practice questions
plus hundreds of inline drills. 29 clickable Contents links, real selectable text.

AUTHORED, not rebuilt: the decks are a source, content/*.html is the book,
written by hand. The two image-only decks were read slide by slide from rendered
images; the exam format and verified answer key were transcribed from the real
test screenshots.

Six scripted gates, all green at publish:
  - gates.py: no em/en dashes, no institution/platform/lecturer names (the book
    authors Oyedepo, Leaf, Peale, de Bono, Young are subject matter and kept),
    the reserved gold reserved to MUST-MEMORISE only.
  - qa_coverage.py: no slide left behind. Every content-bearing slide of all four
    decks (69 of them) must be cited by a provenance chip; control-tested.
  - qa_firstuse.py: teach before use. Every declared acronym (SMART+ER, OKR, KR,
    WOOP, WISE, SWITCH, Po, Mindshare and more) is introduced before use and never
    first inside a mock.
  - contents.py + assemble.py: all 29 Contents links resolve to the right page and
    the printed number matches that page's footer.
  - qa_layout.py: body renders at its design size (10.50 pt, no Chromium shrink),
    footer numbering sequential, no near-blank pages, nothing outside the margins,
    no box cut by a page break that could have fitted whole.
  - qa_content.py: every one of the 208 drill options is actually painted in the
    rendered PDF (measured against the artifact, not the HTML), and no tofu glyphs.

Palette: forest green (growth) with a reserved gold for MUST-MEMORISE. Two render
bugs were found and fixed before publish: the key emoji used on every gold hook is
absent from DejaVu and printed as tofu (replaced with a diamond), and the option
markers were refactored off page-boundary-fragile absolute positioning onto flow
layout. The content gate above was added to catch either class automatically.

To rebuild or update:  cd "courses/TMC221 - Personal Development and Capacity
                       Building/build" && python assemble.py

-------------------------------------------------------------------------------
COS221 - Computer Programming I (Java) - Study Manual.pdf   347 pp   updated 2026-07-22
-------------------------------------------------------------------------------
COS221 Computer Programming I (Java), complete manual, Modules 1 to 10.

Contents: Foundations F.1-F.11, Modules 1 to 10, both past papers solved in full
(2024/25 six-of-which-attempt-four, and 2025/26 three-sections), mock papers in
both of those shapes (Mock A and Mock B) with solutions, and reference R.1-R.4
(exam API card, method reference by class, keyword index, glossary). 126 clickable
Contents links, real selectable text throughout.

Unlike PHY121 this manual was AUTHORED, not rebuilt: there was no prior manual of
ours to reproduce, so content/*.html is the book, written by hand. Of the 225 code
listings, all 183 that are runnable programs were compiled and run on a real JVM
(Temurin 17), and every printed output was captured from that JVM, never typed. The
other 42 are deliberate non-programs: syntax skeletons, fragments, code quoted from
the papers, and loops that would never terminate. Each carries a written reason. Withheld-answer listings on the mock
papers still run: the gate proves each one's answer exists and matches, elsewhere in
the book.

Five scripted gates, all green at publish:
  - check_code.py: every listing compiles and runs; every claimed output diffed
    against the JVM. 225 listings, 0 failures. Also caps every listing's line
    width before the render, which is the shrink guard below.
  - qa_verbatim.py: every past question quoted in the book is the examiner's exact
    words, held against an eye-typed transcript of the real paper. Fails in both
    directions, on a paraphrase and on a quietly dropped part.
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

What changed on 2026-07-22 (333 pp -> 347 pp): PAST QUESTIONS ARE NOW QUOTED, NOT
RESTATED. A reader pointed out that the solved papers presented each question in a
compressed restatement in the author's voice, formatted as though it were the
paper. All 40 question parts across both papers are now a three-part unit: AS
PRINTED (the examiner's exact words, including the paper's own typos and its one
self-contradicting example), then BREAK IT DOWN (what is given, what is actually
being asked, what the marks imply, where the trap is, which unit teaches it), then
the answer. Both papers were transcribed by eye from the scans into
sources/exams/transcripts/, since the exam PDFs carry no text layer.

Three fidelity faults surfaced while doing it, none of them visible before: 21
answer-box restatements had drifted from the paper (one read "above 8 degrees C"
where the paper prints 8C); five listings had been quietly renamed (SquareCalc to
SquareCalcBroken, Main to MiddleValueBroken) to dodge a filename clash that cannot
happen; and one question quoted the book's own class wrapper around what the paper
prints as a bare fragment. All corrected.

A new gate, qa_verbatim.py, holds every quotation against the transcripts in both
directions (paraphrase, and quietly dropped parts) and runs as a pre-flight inside
assemble.py. It is control-tested both ways, and it caught four of the
transcriber's own shortcuts: superscripts flattened to ^3, a dropped degree sign,
and a hyphenated word split by line wrapping. Those were fixed in the transcript
against the scans, never in the quotes.

THE SHRINK RECURRED, and was caught: a 123-character line in a newly quoted
listing took the render to 248 pages at 90.9% of design size. The guards added on
2026-07-17 did their job; the mistake was running the column check before the last
listings went in. The paper itself wraps that line, so quoting it faithfully and
curing the shrink turned out to be the same edit. The methodology now says to run
that check last, after the final content edit.

Republished the same day, still 347 pp: the two-direction gate above turned out to
have a blind spot, and it was found by comparing notes with the IFT222 retrofit.
Both directions work from the AS PRINTED boxes, so neither can see a module that
cites a past question while TEACHING, which has no such box. Two such misquotes
were sitting in the modules: one dropped "(from i onward)" from inside quotation
marks, and one lowercased the paper's own quoted term and swallowed its internal
quotes. Both corrected, and qa_verbatim.py gained a third direction: inside any box
whose provenance chip cites a paper, every run in quotation marks must be verbatim.
Control-tested on its own. Quotation marks are a promise, and the gate now keeps it
everywhere in the book, not only in the solved papers.

To rebuild or update:  see "courses/COS221 - Computer Programming I (Java)/README.md"
                       (cd build && python assemble.py)

-------------------------------------------------------------------------------
CSC241 - Python Programming Language I - Study Manual.pdf   200 pp   updated 2026-07-22
-------------------------------------------------------------------------------
CSC241 Python Programming Language I, complete manual, Modules 1 to 5.

What changed from the 182 pp edition (18 July): PAST QUESTIONS ARE NOW QUOTED.

A reader reported the defect across every manual here. This book restated each
real examination question in our own compressed words while presenting it as the
paper, and in the solved 2025/2026 section it was worse: the question was never
shown at all, only an "Answer" box with a summarising chip. A student revising
from it was training on a question that does not exist, with the comprehension
half already done for them, and the paper's own errors quietly tidied away.

Every one of the 24 sites is now a three-part unit: AS PRINTED (the examiner's
exact words, in a box marked as a quotation), BREAK IT DOWN (what is given, what
is actually asked, what the marks say about expected depth, where the trap sits),
then the worked answer. 23 sites are the 2025/2026 paper; the 24th is a Module
Four teaching box citing the 2024/2025 paper. The three mocks are ours, so they
carry no AS PRINTED box and say "same shape as" rather than implying they are the
paper's wording.

The paper's defects are preserved as evidence, each flagged in a note AFTER the
quote and never silently repaired: the singular "[3.5 mark]" where every other
part says marks, "Strings are Immutable. Explain and with reasons.", a part
printed without its question mark, a listing that opens with a double quote and
closes with a single one, and a Sample Interaction that prints 10546.90 where
math.pi gives 10547.79.

The transcripts in sources/exams/transcripts/ are the authority, read by eye from
the seven photographs (the 2024/2025 scan carries no text layer at all, so there
was no OCR to reject). qa_verbatim.py proves the book matches them in three
directions, each control-tested to fail on its own: paraphrase, dropped part, and
prose citation. The third is the one the other two are structurally blind to,
since both work from AS PRINTED boxes and a citing teaching box has none.

Page fill held at 74.8% against 75.7%, and the body still renders at its designed
10.50pt: the column gate was re-run AFTER the quoted listings went in, not before.
The 182 pp render was superseded; git holds it.

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
DTS224 - Data Management I - Study Manual.pdf      119 pp   updated 2026-07-22
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

What changed on 2026-07-22 (85 pp -> 119 pp): PAST QUESTIONS ARE NOW QUOTED, NOT
RESTATED. A reader reported that the solved paper and the module teaching boxes
presented each past question as a compressed restatement in the author's voice,
formatted as though it were the paper. All SEVEN past papers (2015/16 through
2025/26, 114 question parts) were transcribed by eye into
sources/exams/transcripts/ and every one of the 64 sites that cites a real question
is now a three-part unit: AS PRINTED (the examiner's exact words, line breaks, part
numbering and mark text), then BREAK IT DOWN on the fully worked 2025/2026 paper,
then the answer. 93 quoted questions in all. The quotes are generated FROM the
transcripts, never retyped, so no hand-typing can drift.

None of the seven papers had a usable text layer: three are image-only scans and
four are photographs, and the three PDFs that DO carry a layer are OCR of a scan
(one renders the paper's own "COURSE TITLE" as "COURSE TrTLE"). Every line was read
off the pixels, twice.

Quoting them exposed real errors this manual had been teaching:
  - 25/26 Q6(b) prints SIX functional dependencies; the book showed four and had
    reordered fd1's targets. The two dropped ones are the candidate keys.
  - 25/26 Q1(c) prices salaries in Naira; the book had dropped the currency.
  - The book told the reader the paper is "Two hours". It prints TIME: 3 HOURS.
The papers' own defects are now preserved as evidence rather than tidied away: the
struck-through "Show the prim" in 25/26 Q2(d), 24/25 Q5(b) promising "(i-vii)" and
printing eight parts, its Table 1 having no sName column though three of its FDs
determine sName, 21/22 Q2(c) declaring four attributes ABCD then depending on F,
and 15/16 labelling two consecutive parts "(a)". Each carries a note AFTER the
quote saying so.

A sixth gate, qa_verbatim.py, now enforces this in FOUR directions, every one
control-tested to fail on its own defect and on nothing else:
  - paraphrase: reword one word of a quote and it fails;
  - dropped part: delete the only copy of a question and it fails;
  - prose citation: reword a quotation attributed to the examiner in a note;
  - line structure: join two lines of a quoted listing, leaving every word intact
    and in order, and it still fails. The first three compare whitespace-collapsed
    text and are all blind to that.
Plus discovery: a box that cites a paper but shows no quote is a failure, which is
what caught the 48 module sites. Two bugs were found by control-testing rather than
by reading: a scaffolding regex that silently ate the papers' own indented
sub-parts (and which the gate would have blessed, since book and transcript were
sliced by the same rule), and an entity double-escape that printed "&#8594;" where
the paper prints an arrow.

To rebuild or update:  see "courses/DTS224 - Data Management I/README.md"
                       (cd build && python assemble.py)

-------------------------------------------------------------------------------
IFT222 - Computer Architecture and Organisation - Study Manual.pdf   185 pp   updated 2026-07-22
-------------------------------------------------------------------------------
IFT222 Computer Architecture and Organisation, complete manual: Foundations,
Modules 1 to 4, a Digital Logic supplement, a Reference part, both priority past
papers solved in full, and three mock examinations.

VERBATIM PAST-QUESTION EDITION (2026-07-22). A reader reported that every manual
we had shipped restated each real past question in the author's compressed words
while presenting it as the paper, and this book was the worst affected of the
five. A restatement strips the examiner's phrasing habits, the real part
numbering, the exact mark text and the ambiguity a student must resolve under
time pressure, and it launders the paper's own mistakes into clean prose, so the
student ends up revising against a question that does not exist.

All four papers were first transcribed by eye from the photographs into
sources/exams/transcripts/. The 2023/24 scan carries an OCR text layer; it was
rejected, not used, because it reads "1 1/2mks" as "12mks" and turns truth-table
cells into Korean characters, and a transcript seeded from it would simply have
certified the paraphrase. Every past question in the book is now a three-part
unit: AS PRINTED (the examiner's exact words, in a paper-toned box), BREAK IT
DOWN (what is given, what is actually asked, what the marks imply, where the
trap is), then the answer. 68 sites, 77 quoted questions; the 2024/25 and
2025/26 papers are quoted and answered in full, question by question.

The papers' own defects are preserved as evidence and flagged in a note beneath
each quote, never silently repaired. Among them: "Special Locality" in one year
and "Spacial Locality" in another, neither of which is spatial; "Use 12 bits"
printed above a row holding only 11; "State Amdahl's law'" with a stray
apostrophe in two separate years, so it is copied forward; a pipeline question
naming a "PO stage" that is not one of the five stages its own sentence defines,
struck through in pen to EX on the sheet; and a data-hazard pair whose two
instructions share no register at all, so that as printed it shows no hazard
though its position makes WAW the evident intention. The three mock papers are
author-written, carry no AS PRINTED bar, and now say so explicitly.

Page count rose from 77 to 185 across this and the two earlier passes; verbatim
quotes are longer than restatements, and the growth is content, with median page
fill improving from 80.1% to 81.8%.

Contents: Foundations, Module 1 (with three further units), Module 2 (with two
further units), Module 3 (with two further units), Module 4, a Digital Logic
supplement, and two mock examinations solved in full. Diagram-rich (datapaths,
memory hierarchy, addressing, number-format and logic-gate figures as inline
SVG). Clickable Contents links and real selectable text throughout.

Like the other Omega manuals this was AUTHORED, not rebuilt: IFT222 is the renamed
CSC227, so those past papers are valid practice, and the lecture decks are sources,
so content/*.html is the book, written by hand. A four-deck slide-coverage audit
blended every substantive slide item the past papers did not already force into the
teaching, so nothing examinable is left to the decks alone. The two priority papers
(2024/25 and 2025/26) are weighted most heavily and drilled in the mocks. Every
numeric result (base conversions, two's-complement and IEEE-754 encodings, addressing
arithmetic, cache and performance calculations) was recomputed independently, never
copied from a deck whose figures are unverified.

Seven scripted gates, all green at publish:
  - verify_numbers.py: every number in the book recomputed and diffed, not trusted
    as printed. 221 checks, 0 mismatches.
  - qa_verbatim.py: a past question is quoted as the examiner printed it, or not at
    all. Five mechanisms, each control-tested by feeding it a known-bad book and
    requiring it to fail: no reworded quote, no dropped part of a paper presented as
    solved in full, no teaching site left citing a paper it does not quote, no
    quoted listing re-wrapped away from the paper's own line breaks, and no
    misquotation inside our own commentary beside a correct quote. The last of those
    was added after comparing notes with the COS221 retrofit, which shipped with a
    narrower gate and still carried two misquotes in its teaching prose; the same
    check found eight here, mostly a silently capitalised first letter.
  - qa_formulas.py: no formula appears without saying what each of its symbols
    means, every numeric worked example opens with Given / Find / Formula, and every
    named law is stated as a law, with its conditions and its limiting case.
  - gates.py: no em/en dashes, no institution or methodology-author names, the
    reserved colour (electric violet) used only by MUST MEMORISE, all code monospace,
    and no code line over the width that fits (a longer one shrinks every page).
  - qa_firstuse_ift.py: teach before use, measured not asserted. Every notation and
    term is introduced before the reader meets it, with a first-use audit run live
    against the assembled book, and none is first introduced inside a mock.
  - contents.py: the generated Contents, its page numbers read back out of the
    rendered book so they cannot drift, every row's link resolving to the page it names.
  - qa_layout.py: the body renders at its designed size (not silently scaled to fit
    an over-wide line), nothing outside the margins, no box cut by a page break that
    would have fitted whole.

To rebuild or update:  see "courses/IFT222 - Computer Architecture and Organisation/"
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

-------------------------------------------------------------------------------
CSC242 - Discrete Structures - Study Manual.pdf      451 pp   updated 2026-07-22
-------------------------------------------------------------------------------
CSC242 Discrete Structures, complete manual, and the largest in this folder.

THE DEFINING FACT, and the reason this course was scoped differently from every
other manual here: the official 161-page course text does not teach the exam.
All 184k characters of it were probed. Occurrence counts: reflexive 0,
antisymmetric 0, vertex 0, vertices 0, adjacency 0, handshaking 0, Euler 0,
planar 0, Kuratowski 0, poset 0, Hasse 0, isomorph 0, preorder 0, Cartesian 0,
bit string 0. Yet graph theory, trees, relation properties and posets are about
40% of the marks on every paper. So those topics are taught here from zero, each
carrying a visible "not in the course text" chip, rather than merely drilled.
Scope was taken from the papers, not from the text. Two further defects in that
text are flagged in the book where they matter: its "Module One: Descriptive
Statistics" contains no statistics at all (its subject is propositional logic
from the first line to the last), and its probability module calls independence
"mutually exclusive or disjoint" and gives the disjoint addition rule for
non-disjoint events, contradicting its own correct rule three paragraphs later.

Lineage confirmed from the exam banners: CSC311 (2020/21), CSC416 (2021/22 and
2024/25), CSC242 (2023/24 and 2025/26). Same title, same department, so all five
papers are valid practice. The format CHANGED partway: the two oldest are any
THREE in 2 hours; the current shape, and the one the mocks imitate, is ANY FOUR
of six questions, 17.5 marks each, 70 total, 3 hours.

Contents: How to use it, Foundations F.1 to F.2, Logic 1.1 to 1.5, Sets 2.1 to
2.3, Relations 3.1 to 3.4, Functions 4.1 to 4.3, Counting 5.1 to 5.4, Graph
Theory 6.1 to 6.8, Trees 7.1 to 7.3, Boolean Algebra 8.1, Proof, Induction,
Sequences and Recurrences 9.1 to 9.4, Statistics and Probability 10.1 to 10.2,
C++ 11.1 to 11.2, Reference R.1 to R.3, all five past papers solved end to end,
and three mock examinations with full answers. 73 clickable Contents rows.

Every past question is quoted AS PRINTED in the examiner's exact words, broken
down, and then answered. 81 quoted questions, verified in three directions
against eye-made transcripts of all five papers. Paper defects are preserved
inside the quotations and flagged underneath, never silently corrected: 25/26
Q3a names the same language twice, which makes 7 marks unanswerable exactly as
written; 25/26 Q1a prints "Prepositional logic" and "Path Matrice"; 24/25 Q4b
asks the same thing twice; 20/21 Q5a prints "Contigency". Two readings that are
genuinely unresolvable at scan resolution are marked as such rather than guessed.

Reconciling the printed marks question by question turned up three things worth
knowing before the exam: 2023/2024 is 23.5 marks a question, not 17.5, so three
answers give 70.5; 2021/2022 Q4 totals 24 while its other four total 23.5; and
2020/2021 Q5 totals 22.5 while its other four total 23.5. The manual prints all
three and tells the reader to add the marks up in the first minute, because a
question whose parts do not total what its neighbours do has a part you have
not noticed.

Eight scripted gates, all green at publish:
  - verify_numbers.py: 762 worked values and 5 printed grids recomputed
    independently, each pinned to the one file that prints it, with every table
    row built FROM the recomputation so the value and the check are one object.
  - verify_code.py: 7 complete C++ programs and 6 teaching fragments EXTRACTED
    from the book itself, compiled at /W4 where any diagnostic fails, run on the
    question's own input, and compared line for line with the output panel the
    book prints. C++ is taught from zero here because the papers set 19 marks of
    it and the course text does not contain the word "program".
  - qa_verbatim.py: every quoted question matches its transcript character for
    character, every question part we hold is quoted somewhere, and every run in
    quotation marks in paper-citing prose is either verbatim or plainly our own
    gloss. That third direction caught two real misquotes in this book.
  - qa_formulas.py: 43 formulas each state what every symbol means at the point
    of use; 112 must-memorise boxes and 110 worked examples scanned; 10 named
    laws each stated with conditions and limiting case.
  - qa_firstuse.py: nothing is used before it is introduced, all 32 gap topics
    are introduced, and no notation makes its first appearance inside a mock.
  - gates.py: no em or en dashes in our prose (82 quoted questions exempt by
    masking, not by disabling the check), no institution or pedagogy-source
    names, the reserved crimson reserved, no code line over 87 columns.
  - contents.py: all 73 Contents rows resolve to a page carrying that heading and
    the printed number matches that page's own footer.
  - qa_layout.py: body renders at its design size (10.50 pt across 334360
    characters, no Chromium shrink), nothing outside the margins, no box cut by a
    page break that could have fitted whole, no code hanging past its panel.

Palette: indigo for teaching with a reserved crimson for MUST-MEMORISE, plus a
teal chip marking the topics the course text does not carry.

AUTHORED, not rebuilt: the institutional text is a source, content/*.html is the
book, written by hand. The two oldest papers are image-only with no text layer
and were read by eye from renders at 170 dpi; the newest was read from phone
photographs, one of them rotated.

KNOWN LIMIT at publish, recorded honestly: the gates above cover numbers, code,
quotations, notation order, house style and page geometry. They do not read
prose. A full end-to-end read for repetition, tonal drift and concept-level gaps
has NOT been done on this edition. Roughly 23 of its 451 pages also sit under a
quarter full, which is the price of the rule that a box is never split across a
page turn; the solved-papers part has the same character.

To rebuild or update:  cd "courses/CSC242 - Discrete Structures/build"
                       && python assemble.py
