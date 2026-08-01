===============================================================================
FINAL_CRASH_MANUALS
===============================================================================
Lean, exam-survival "crash course" editions: novice to a perfect score in days,
built backwards from a named exam. Separate from FINAL_MANUALS (the full study
manuals). Each crash course targets one exam's actual surface, teaches only the
skills that answer it, and drills them with active recall and the real MCQs.

How they are built and the reusable prompt for new ones: see
CRASH_COURSE_PROMPT.md in the workspace root.

-------------------------------------------------------------------------------
IFT222 - Exam Crash Course - Zero to a Perfect Score.pdf     60 pp   2026-08-01
-------------------------------------------------------------------------------
Computer Architecture and Organisation. Takes a reader who has not opened the
course from zero to solving the 2025/2026 paper, the revision deck's extra
questions, and every objective (MCQ) question from both practice tests.

Every test and exam question is given VERBATIM, in the examiner's exact words
(gated against the eye-verified transcripts, so a quote that drifts fails the
build). The whole 2025/2026 paper is sat as a final mock, and each answer is
laid out the way you write it in the hall: the given values, the formula, then
the arithmetic worked VERTICALLY, stacked and column-aligned (binary additions,
the invert-and-add-one, cache field splits, weighted CPI sums), then the answer.

Organised by exam skill, not the syllabus, and foundation-first so nothing is
used before it is taught:
  - Part A, Foundations and Data: the big picture (architecture vs organization,
    ISA, Von Neumann and Harvard, CPU parts, buses), number systems and codes,
    signed numbers, IEEE-754 floating point, image sizing.
  - Part B, The Machine: instruction sets and formats, addressing modes, CPU
    performance (CPI, Amdahl), pipelining and hazards, memory and cache.
  - Part C, Prove It: RISC vs CISC and the rest, then the MCQ bank (all 120
    objective questions grouped by topic with hidden answers), then the whole
    2025/2026 paper as a final mock.

Every skill is taught as a method you apply to any numbers (not an answer to
memorise), then practised on fresh numbers with the answers hidden, so a change
of values in the exam does not matter. Built to the same flawless bar: every
worked number recomputed independently (80 checks), no dashes or institution
names, teach-before-use audited against the assembled book, an accurate
clickable Contents, and the body rendered at its designed size with nothing
scaled. Clickable Contents, real selectable text.

To rebuild:  courses/IFT222 - Computer Architecture and Organisation/crash/
             (cd crash && python assemble.py)
