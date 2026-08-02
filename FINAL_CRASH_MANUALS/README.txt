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
IFT222 - Exam Crash Course - Zero to a Perfect Score.pdf     86 pp   2026-08-02
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

Every teaching section is a step-by-step PROGRAMME: many tiny numbered frames,
each doing one small thing and ending with a task, the next frame opening with
the answer, so you cover the page, work the step, then slide down to check.
Nothing is a wall of prose. To grasp and remember it, the abstract layouts are
DRAWN (a labelled IEEE field strip, the cache address split, the two's-complement
odometer, an instruction-format strip), every section closes with a "Lock it in"
card carrying its one-line mnemonic, and a single-page "The Night Before" map
compresses the whole course to one hook and one formula per skill. Every skill is taught as a method you apply to any
numbers (not an answer to memorise), then practised on fresh numbers with the
answers hidden, so a change of values in the exam does not matter. The harder
ideas are taught intuition first, with the reason before the rule (why two's complement wraps like an
odometer, why floating point is just scientific notation in binary, why a cache
address splits three ways like a coat-check ticket), not as steps to swallow.
Where a question asks for a diagram (Von Neumann versus Harvard, the pipeline
timing and cycle diagrams), it is drawn, taught with a way to remember it, and
shown as it should look on your answer script. Built to the same flawless bar:
every worked number recomputed independently (90 checks), no dashes or institution
names, teach-before-use audited against the assembled book, an accurate
clickable Contents, and the body rendered at its designed size with nothing
scaled. Clickable Contents, real selectable text.

To rebuild:  courses/IFT222 - Computer Architecture and Organisation/crash/
             (cd crash && python assemble.py)
