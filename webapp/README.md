# TMC221 Drill

An active-recall testing platform built from the TMC221 study manual in this repo.
**Deployment and account setup live in [SETUP.md](SETUP.md).**

## What it does

- Drill **one module, several, or all five mixed**.
- Set the **easy / medium / hard mix**, either from a preset or by typing the ratio.
- Optionally restrict the paper to questions that hang on **hard specifics**: numbers
  and percentages, names and book titles, ordered lists, or exact slide wording.
- Choose **how many questions**, up to and including every question that matches.
- Sit it **timed or untimed**. The clock auto-submits at zero.
- Answer in all six styles the real test uses: single choice, multiple response,
  true/false, matching dropdowns, cloze dropdowns, and typed short answers.
- Get a **score, a per-module breakdown, and every answer with the slide it came
  from**, plus a one-button **retry of only what you missed**.
- **Retake the real 30-question test** exactly as it was set.

## The bank

597 questions: 567 across the five modules plus the real 30-question test.

| Module | Lecture | Questions |
| --- | --- | --- |
| 1 | Goal Setting and Personal Accomplishment | 122 |
| 2 | Positive Thinking and Creative Problem-Solving | 120 |
| 3 | Personal Branding and Strategic Positioning | 105 |
| 4 | Systems for Sustainable Success | 110 |
| 5 | Overcoming Discouragement and Sustaining Personal Success | 110 |

Every question is written from the lecture slides, carries the slide reference it came
from, and is tagged with a difficulty and its specifics facets.

## The gate

`npm run build` runs `scripts/validate-bank.mjs` first, so a broken bank cannot deploy.
It checks two things.

**Schema.** Unique ids, a key that actually names an existing option, dropdowns that
contain their own answer, no blank without an accepted answer, marker numbering that
matches the blanks defined. A question whose key names a missing option would mark you
wrong forever and look fine doing it, which is the worst failure this thing can have.

**Coverage.** The same forcing function the manual itself uses: every content-bearing
slide of all five decks, 87 of them, must be cited by at least one question. A slide
nothing asks about is a slide you are never tested on. Control-tested by stripping one
slide's citations and confirming the gate names that slide.

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
app/          routes: the page, the NextAuth handler, the attempts API
components/   Setup, Runner, QuestionView, Review, AuthBar
lib/          types, grading, bank selection, supabase client, auth options
data/         courses.ts registry + tmc221/*.json question banks
scripts/      validate-bank.mjs, the build gate
```

## Adding another course later

1. Create `data/<code>/module*.json` in the same shape.
2. Import it in `data/courses.ts` and push one more entry into `COURSES`.
3. Point `REQUIRED` in `scripts/validate-bank.mjs` at the new deck's slide ranges.

No database change, no schema change, no component change.

## A note on dependencies

`npm audit` reports four advisories that have **no upstream fix available**: they are
transitive inside Next's own toolchain (`postcss` and `sharp`, with `next` and
`next-auth` flagged only by association). Everything that did have a fix is patched:
Next is on the 15.5.22 line, `next-auth` on 4.24.15, `@supabase/supabase-js` on
2.111.0. `sharp` is only used by `next/image`, which this app never calls, and the
`postcss` advisories concern processing untrusted CSS at build time, which does not
arise here. Worth re-checking when upstream ships fixes.
