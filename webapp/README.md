# CU Drill

An active-recall testing platform built from the study manuals in this repo. The
landing page lists every course loaded; pick one and set up a test.
**Deployment and account setup live in [SETUP.md](SETUP.md).**

| Course | What it is | Bank |
| --- | --- | --- |
| **ENT221** Agripreneurship | Twelve topics from the 88-page course text and all three lecture decks, both computer-based tests, every option explained | 814 |
| **IFT222** Computer Architecture and Organisation | Ten topics, both 60-question objective tests, every option explained, plus a 14-lesson interactive crash course | 120 |
| **TMC221** Personal Development and Capacity Building | Five lectures, six question styles, the real 30-question test. Exam sat, so it sits under "Exams already taken" | 567 + 30 |

## What it does

- Drill **one group, several, or all of them mixed**. TMC221 calls them modules,
  IFT222 and ENT221 call them topics.
- Draw from **the whole bank or only the questions the examiner actually set**. The
  filter appears only where it would change the draw.
- Set the **easy / medium / hard mix**, either from a preset or by typing the ratio.
- Optionally restrict the paper to questions that hang on **hard specifics**. Each
  course words those four facets in its own vocabulary: for TMC221 that is numbers,
  authors, ordered lists and slide wording; for IFT222 it is conversions and
  calculations, named schemes, hierarchies and layouts, and exact distinctions; for
  ENT221 it is figures and thresholds, named species and models, enumerated lists,
  and the exact definitions with the absolutes that mark a wrong option.
- Choose **how many questions**, up to and including every question that matches.
- Sit it **timed or untimed**. The clock auto-submits at zero.
- Be told **at the end, or after every question**. See below.
- Answer in all six styles the tests use: single choice, multiple response,
  true/false, matching dropdowns, cloze dropdowns, typed short answers. The typed
  answer setting only appears where a course actually has blanks.
- Answer short blanks by **typing them, picking from a dropdown, or a mix of the
  two**. Mixed decides per question when the paper starts, so you cannot settle
  into one and it never changes under you mid-question.
- Get a **score, a per-group breakdown, and every answer with the source it came
  from**, plus a one-button **retry of only what you missed**.
- **Retake a real paper** exactly as it was set: the TMC221 test, either IFT222
  objective test, or either ENT221 computer-based test.
- **Take it away as a PDF**, either the marked results or the questions
  themselves. See below.

## Two ways to sit a test

**Mark it at the end** is exam conditions: answer everything, then get the score and
the full review.

**Tell me after every question** is how you learn a course you do not know yet. The
moment an answer is committed the page says right or wrong, gives the answer, prints
every option with its own verdict, and shows the reference it came from. Then the
question locks, because seeing the answer and then changing yours teaches nothing. A
single choice commits when you tap it; anything with several parts waits for **Check
answer**, since a four-blank cloze would otherwise be marked wrong on the first
keystroke. A running tally sits in the progress bar.

The panel is the same component the end-of-test review prints (`components/Feedback.tsx`),
so what you are taught mid-test and what you read afterwards cannot drift apart.

## Taking it away as a PDF

Two routes, both through the browser's own print dialog, so the text stays selectable
and searchable and the bundle carries no PDF library at all.

**Your marked results.** The review screen has a **Save as PDF** button. It prints
exactly what is on screen, so switching to "only what I missed" first gives you a
revision sheet of just your mistakes. Every question keeps its explanation, its
per-option verdicts and its source reference.

**The questions themselves.** Setup has a **Printable sheet** button that takes whatever
you have selected there, one topic, several, or all of them, plus the specifics and past
question filters, and lays out every question in it with its answer, explanation,
verdicts and reference. The difficulty mix and question count do not apply: you get all
of them. For ENT221 with nothing filtered that is all 814.

`@media print` in `globals.css` hides everything you would tap, keeps everything that
teaches, and sets `break-inside: avoid` so a question is never split across a page
boundary. Anything that should never print carries the `noprint` class.

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

**ENT221**, 814 questions across twelve topics, built from the 88-page course text, all
three lecture decks, and both computer-based tests.

| Topic | Questions |
| --- | --- |
| 1 Module One: agriculture, its aspects and its importance | 40 |
| 2 Module One: agripreneurship and the agricultural value chain | 68 |
| 3 Module Two: fish farming, departments and investment potential | 61 |
| 4 Module Two: water quality, physical, chemical and biological | 93 |
| 5 Module Two: aquarium management and fish behaviour | 68 |
| 6 Module Two: the 3M model, Make, Manage and Multiply | 56 |
| 7 Module Two: marketing fresh and processed fish | 38 |
| 8 Module Three: oil palm cultivation | 113 |
| 9 Module Three: oil palm processing and its by-products | 69 |
| 10 Module Four: agribusiness opportunities and the value chain | 74 |
| 11 Module Four: value addition and agribusiness innovation | 68 |
| 12 Module Four: production and operations management | 66 |

The three decks Victor supplied are **misnamed**: the file called "oil palm cultivation"
is the processing deck, the one called "oil palm processing" is the Module Four deck, and
the one called "value chain" is the cultivation deck. Every reference in the bank and the
gate names a deck by its **content**, never by its filename: `Cultivation S7`,
`Processing S6`, `Agribusiness S12`.

Both computer-based tests are rebuilt from the bank by provenance tag. Test 1 is 29
questions, not 30: the examiner omitted question 4, and the rebuilt paper has the same
hole in the same place. Test 1 was captured unattempted and carries no printed key, so
its answers are derived from the course text and match the shipped ENT221 manual; Test 2
was captured as a graded 30 out of 30, so every one of its answers is the examiner's own.
Two questions reach outside the course text, and both say so in their review: Test 1 Q8's
1.9 million metric ton import deficit, and Test 1 Q20's total bacterial count threshold.

### The fact ledger

ENT221 carries `data/ent221/ledger/*.json`, an enumeration of **every atomic testable
fact** in its sources: 485 of them, 251 marked hard. This is the leave-no-stone-unturned
check, and the gate bites in three directions:

1. every fact must be named by at least one question;
2. every **hard** fact, meaning anything numeric, named, listed or definitional, must be
   asked in **at least two different styles**, so it cannot be learned as one phrasing
   and then missed when reworded;
3. a question may only name a fact whose own source reference it also cites, which is
   what keeps the reference chip printed under the answer honest.

The ledger never reaches the browser. It exists to be checked.

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
reference outside the two papers. ENT221 carries three coverage rules at once: all 45
sections of the course text, all 41 content slides of the three decks, and all 59
computer-based test questions exactly once each.

**The key.** Every IFT222 and ENT221 answer is cross-checked against a key transcribed
from the original screenshots and held independently inside the gate. Two transcriptions
that disagree fail the build rather than shipping a wrong answer. For fill-in-the-gap
questions the comparison runs through the same normalisation the app marks with.

**The ledger.** For ENT221, every one of the 485 enumerated facts must be tested, and
every hard fact in two or more styles. See above.

**The verdicts.** Every option of every IFT222 and ENT221 question must carry its own
explanation, true and false included.

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
components/   App, Setup, Runner, QuestionView, Feedback, Review, Sheet,
              AuthBar, LessonIndex, LessonView
lib/          types, grading, bank selection, lesson progress, supabase, auth
data/         courses.ts registry, lessons.ts registry, tmc221/*.json,
              ift222/*.json and ent221/*.json banks, ift222/lessons.json,
              ent221/ledger/*.json (gate-only, never bundled)
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

Set `taken: true` on a course once its exam has been sat: it moves to the **Exams
already taken** group on the landing page and stays fully usable for revision.

## A note on dependencies

`npm audit` reports four advisories that have **no upstream fix available**: they are
transitive inside Next's own toolchain (`postcss` and `sharp`, with `next` and
`next-auth` flagged only by association). Everything that did have a fix is patched:
Next is on the 15.5.22 line, `next-auth` on 4.24.15, `@supabase/supabase-js` on
2.111.0. `sharp` is only used by `next/image`, which this app never calls, and the
`postcss` advisories concern processing untrusted CSS at build time, which does not
arise here. Worth re-checking when upstream ships fixes.
