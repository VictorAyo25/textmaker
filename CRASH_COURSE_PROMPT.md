# Reusable prompt: build an exam CRASH COURSE for any course

Copy the block below, fill in the four bracketed slots, and send it. It works for any course
in this workspace. The school now puts MCQs on every exam, so the objective test is built in.

The most important slot is the **DESTINATION**: the past question(s) you name become the
target the whole book is designed backwards from.

---

Build me a lean **exam crash course** for **[COURSE CODE + TITLE]**, a separate deliverable
from the full study manual, that takes a complete novice to a perfect score by **[EXAM DATE]**.

**Destination (this is the target the whole book works backwards from):**
- Past paper(s) to treat as the exam: **[e.g. 2025/2026; or name the exact paper(s)/questions]**
- Extra question sets to also solve in full: **[e.g. a revision deck's questions not on that paper; or "none"]**
- The objective / MCQ test(s): **[folder or file of the MCQs — I have dropped them in the workspace; all our exams now have MCQs]**

**How I want it built:**
1. First move any source I dropped into the course's `sources/` folder.
2. Backward design: those destination questions are the goal. Teach every skill needed to
   solve them, and questions like them with different numbers, from zero. Pull in outside
   foundations wherever the course sources gloss over something needed for real understanding.
   Teach the **method, not the answer**, so changed values do not throw me.
3. Cut the crap: organise by **exam skill**, not by the syllabus. Only what the destination needs.
4. **Nothing is used before it is defined, taught or explained.** Order it foundation-first and
   enforce it with the teach-before-use audit.
5. Make every skill a loop I can actually study from: teach it simply, give the method as fixed
   steps and why it works, one worked example, then practice questions with **different numbers
   and the answers hidden** so I cover and redo, plus the real MCQs on that skill.
   **Teach the reason before the rule.** For every hard idea, give one concrete intuition or
   everyday analogy and the "why" first, then the mechanics; a correct but jargon-first wall of
   bullets is still confusing to a novice. (In IFT222: two's complement as an odometer that
   wraps, IEEE-754 as scientific notation in binary, the cache address split as a coat-check
   ticket.) Do not dumb it down, and keep the worked calculations laid out vertically.
6. **Give every test and exam question verbatim, in the examiner's exact words, never
   paraphrased** (the same "as printed" discipline the study manuals use). That covers the MCQ
   stems and options, the destination paper, and any past question a skill shows. Enforce it
   with the verbatim gate so a quote that drifts from the transcript fails the build. **Show the
   examiner's own tables as real ruled tables, like the exam, not as text or pipes** (a "complete
   the table" keeps the columns blank to fill). If a printed part is **struck out** or corrected
   by hand, quote it as printed and note the pen mark, and **still work a struck-out part in
   full** so I am ready whether or not the strike is on my paper; a printed slip corrected in pen
   keeps the printed word in the quote and uses the correction in the working.
7. **Make it feel like the exam hall, and solve every calculation the way I would by hand:**
   outline the **Given** values, state the **formula** before any number goes in, show the
   arithmetic **vertically / stacked** (binary additions, the invert-and-add-one, the cache
   field split, the weighted CPI sum), then the answer. Not squashed into a sentence. **Write the
   definitions in the solutions the way the lecturer states them** ("is defined as ...", echoing
   his own words and his own questions), because that is the phrasing that earns the marks.
8. **Draw the diagrams the paper asks for.** Where a question says "draw" or "include a diagram",
   the solution SHOWS the diagram as it should look on my answer script, and the lesson teaches
   **how to draw it and how to remember it**, not just what it means. Use the **lecturer's own
   figures** from the slides where they exist (redrawn cleanly), so I reproduce what he expects.
9. Solve **every** MCQ (double-check every numeric one), grouped by topic as a self-test bank.
10. Solve the destination paper(s) in full as a final mock: the real paper, verbatim, sat under
    the clock, each question worked in the exam-hall style above. Include the extra question sets.
11. Hold the flawless bar: recompute every worked number independently, no dashes or institution
    names, no shrunk or overflowing pages, an accurate clickable Contents.
12. Build it in the course's `crash/` folder and publish to **`FINAL_CRASH_MANUALS/`** (separate
    from `FINAL_MANUALS/`), and only when I say "we are done" or "go to final".

Tell me you understand, and which past question you are treating as the destination, before you
start building.

---

**Notes for whoever runs this:** the full recipe, the lean gate set, and the traps to avoid are
in the memory `crash-course-methodology.md`. Reuse the IFT222 `crash/` build as the template.
