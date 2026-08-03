# CU Drill

An active-recall testing platform built from the study manuals in this repo. The
landing page lists every course loaded; pick one and set up a test.
**Deployment and account setup live in [SETUP.md](SETUP.md).**

| Course | What it is | Bank |
| --- | --- | --- |
| **TMC221** Personal Development and Capacity Building | Five lectures, six question styles, the real 30-question test | 567 + 30 |
| **IFT222** Computer Architecture and Organisation | Ten topics, both 60-question objective tests, every option explained, plus a 14-lesson interactive crash course | 120 |

## What it does

- Drill **one group, several, or all of them mixed**. TMC221 calls them modules,
  IFT222 calls them topics.
- Set the **easy / medium / hard mix**, either from a preset or by typing the ratio.
- Optionally restrict the paper to questions that hang on **hard specifics**. Each
  course words those four facets in its own vocabulary: for TMC221 that is numbers,
  authors, ordered lists and slide wording; for IFT222 it is conversions and
  calculations, named schemes, hierarchies and layouts, and exact distinctions.
- Choose **how many questions**, up to and including every question that matches.
- Sit it **timed or untimed**. The clock auto-submits at zero.
- Answer in all six styles the TMC221 test uses: single choice, multiple response,
  true/false, matching dropdowns, cloze dropdowns, typed short answers. The typed
  answer setting only appears where a course actually has blanks.
- Get a **score, a per-group breakdown, and every answer with the source it came
  from**, plus a one-button **retry of only what you missed**.
- **Retake a real paper** exactly as it was set: the TMC221 test, or either IFT222
  objective test.

## Every option, and why

An IFT222 review does not stop at the key. Each question prints all four options with
its own verdict: why the answer is the answer, and what is wrong with each of the other
three. Getting a question right for the wrong reason scores nothing next time, and the
distractors on this paper are built out of specific, nameable mistakes: the one's
complement when the question asked for the two's, the effective address when the
question asked for the operand, the single precision figure when the question said
double. Those are worth naming.

The bank gate enforces it: where a course explains its options, a question that
explains only some of them fails the build.

## The crash course

`/ift222/learn` is the crash manual turned into something you do rather than read.

The manual teaches in **programmed frames**: a small step, a question, and the answer
at the head of the next frame, with the instruction "cover the page with a card and
slide it down". On paper that asks the reader to be honest. Here the app holds the
card. A frame's check does not exist in the page until you ask for it, so you cannot
skim the answer and feel taught.

Every other kind of box became the thing it was always trying to be:

| In the manual | In the app |
| --- | --- |
| Programmed frames, 181 of them | Revealed one at a time, progress saved, resumable |
| Worked example, 15 | The problem, then the working on request |
| The 25/26 paper as printed, 18 questions | The examiner's words, with the model answer hidden until you have attempted it |
| Your turn, 20 recalls | The answer hidden behind a self-mark, "I got it" or "I missed it" |
| Must do, Trap, Lock it in | Reference cards, kept in view |

Each skill ends by handing you the real questions on it: **Drill it: Number Systems and
Codes (16 Q)** opens the drill with that topic already selected.

The lessons are **converted, not retyped**. `scripts/import-crash.mjs` parses the crash
manual's authored HTML and writes `data/ift222/lessons.json`. That text has already been
house-styled, numerically verified and gated in the manual build, so retyping it would
put every one of those checks at risk for nothing. Run the importer by hand when the
manual changes:

```bash
node scripts/import-crash.mjs      # reads ../courses/IFT222 .../crash/content
```

It refuses to write if it meets any markup it does not recognise, so a new kind of box
in the manual stops the import instead of being silently dropped.

## The banks

**TMC221**, 597 questions: 567 across the five modules plus the real 30-question test.

| Module | Questions |
| --- | --- |
| 1 Goal Setting and Personal Accomplishment | 122 |
| 2 Positive Thinking and Creative Problem-Solving | 120 |
| 3 Personal Branding and Strategic Positioning | 105 |
| 4 Systems for Sustainable Success | 110 |
| 5 Overcoming Discouragement and Sustaining Personal Success | 110 |

Every question is written from the lecture slides, carries the slide reference it came
from, and is tagged with a difficulty and its specifics facets.

**IFT222**, 120 questions: every objective question from both computer-based tests,
transcribed from the captured papers and their verified answer key. Each carries its
provenance as "Test 1 Q16", so the two papers are rebuilt from the bank by filtering on
that tag rather than storing the questions twice.

| Topic | Questions |
| --- | --- |
| 1 Architecture versus Organization | 12 |
| 2 ISA and Microarchitecture | 13 |
| 3 Number Systems and Codes | 16 |
| 4 Signed Numbers and Complements | 14 |
| 5 Floating Point and IEEE 754 | 10 |
| 6 Instruction Types and Formats | 8 |
| 7 Addressing Modes | 9 |
| 8 Memory, Buses and CPU Components | 26 |
| 9 Performance, Pipelining, RISC and CISC | 7 |
| 10 Von Neumann, Harvard and Image Data | 5 |

Test 1 Q19 is keyed as the examiner keyed it, Sign, Mantissa, Exponent, though the true
IEEE 754 field order is Sign, Exponent, Mantissa. The review says both, because you need
the mark in the test and the truth in a theory answer.

## The gate

`npm run build` runs `scripts/validate-bank.mjs` first, so a broken bank cannot deploy.
It runs per course.

**Schema.** Unique ids, a key that actually names an existing option, dropdowns that
contain their own answer, no blank without an accepted answer, marker numbering that
matches the blanks defined. A question whose key names a missing option would mark you
wrong forever and look fine doing it, which is the worst failure this thing can have.

**Coverage.** The same forcing function the manuals use. For TMC221: every
content-bearing slide of all five decks, 87 of them, cited by at least one question,
because a slide nothing asks about is a slide you are never tested on. For IFT222: all
120 objective questions present, **exactly once each**, no gap, no duplicate, no stray
reference outside the two papers.

**The key.** Every IFT222 answer is cross-checked, letter by letter, against the answer
key transcribed from the original screenshots and held independently inside the gate.
Two transcriptions that disagree fail the build rather than shipping a wrong answer.

**The verdicts.** Every option of every IFT222 question must carry its own explanation.

**The crash course.** No lesson may lose its blocks in conversion, no programmed frame
may ask a question that nothing answers, and **every drill topic must be taught by some
lesson**: a topic with questions and no lesson is a hole a reader falls into.

**House style.** No em dashes, no en dashes, anywhere in any bank or lesson. The one
exemption is an AS PRINTED exam question, which is evidence and is quoted exactly.

## Marking

Every question is worth 1 mark.

- Single choice, true/false: right or wrong.
- Multiple response: **all or nothing**, exactly as the real test warns.
- Matching, cloze, short answer: **part marks**, the fraction of parts you got right,
  so 3 of 4 blanks scores 0.75.
- Typed answers are marked leniently on form and strictly on content: case,
  punctuation and spacing are ignored, so "2:30 a.m.", "2:30am" and "2.30 AM" all pass,
  but a wrong word still fails. Each blank tells you the expected format.

## Layout

```
app/          / lists the courses, /[course] drills one, /[course]/learn/[slug]
              teaches one, plus the auth and attempts APIs
components/   App, Setup, Runner, QuestionView, Review, AuthBar,
              LessonIndex, LessonView
lib/          types, grading, bank selection, lesson progress, supabase, auth
data/         courses.ts registry, lessons.ts registry, tmc221/*.json and
              ift222/*.json banks, ift222/lessons.json
scripts/      validate-bank.mjs (the build gate), import-crash.mjs (run by hand)
```

`data/lessons.ts` is deliberately not imported by `data/courses.ts`: the lesson bodies
are a few hundred kilobytes of teaching HTML, and keeping them out of the registry means
the drill never ships them and a lesson page ships only its own lesson.

Attempt history is stored per course, both in the browser and in Supabase, so one
course's results never appear under another.

## Adding another course later

1. Create `data/<code>/module*.json` in the same shape.
2. Import it in `data/courses.ts` and push one more entry into `COURSES`, with its own
   tagline, blurb, module noun and facet wording.
3. Add an entry to `COURSES` in `scripts/validate-bank.mjs` with that course's
   provenance pattern and coverage rule.

The landing page, the router and every component pick it up from the registry. No
database change, no schema change, no component change.

## A note on dependencies

`npm audit` reports four advisories that have **no upstream fix available**: they are
transitive inside Next's own toolchain (`postcss` and `sharp`, with `next` and
`next-auth` flagged only by association). Everything that did have a fix is patched:
Next is on the 15.5.22 line, `next-auth` on 4.24.15, `@supabase/supabase-js` on
2.111.0. `sharp` is only used by `next/image`, which this app never calls, and the
`postcss` advisories concern processing untrusted CSS at build time, which does not
arise here. Worth re-checking when upstream ships fixes.
