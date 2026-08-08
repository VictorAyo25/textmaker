# PHY121 on the drill: build state

PHY121 is the first CALCULATION course on the platform. The three earlier
courses are answerable from text and lean on recall; this one is mostly "given
these numbers, find that quantity", so it is built differently.

## Deliverables

Three, not one:

1. **The bank** (in progress, see below)
2. **A crash course** on the platform at `/phy121/learn`
3. **A crash manual PDF** to `FINAL_CRASH_MANUALS/`

## The exam shape

From the two graded computer-based tests in `sources/tests/test1|test2`:

| | Test 1 | Test 2 |
| --- | --- | --- |
| Questions | 15 | 15 |
| Options | **five, a to e** | five, a to e |
| Styles | all MCQ | 12 MCQ + 3 fill-in-the-gap |
| Result | 14 of 15 | 15 of 15 |

Five options rather than four needed no platform change: option letters are
derived from POSITION, so A to E works already.

**The rule for styles**, which mirrors the paper exactly: a calculation is a
five-option MCQ, and fill-in-the-gap is used ONLY for concepts, never for a
number. All three gaps on Test 2 are single conceptual words: symmetry, flux,
distance.

**On Test 2 the correct choice was the first option on all twelve of its
multiple-choice questions.** That is a real property of the paper. The drill
shuffles by default, which removes the crutch.

## Where the content comes from, and why not the slides

**The five slide PDFs are almost entirely images.** Only 109 of their 386 pages
carry any extractable text, against 1,578 embedded images: every formula,
worked example and diagram lives inside a picture.

So the ledger is built from **the 172-page study manual**
(`build/content/*.html`, 220,801 characters of real text), which was itself
blended from those same slides and QA'd. The slides remain the source for
figures.

Extraction is regenerable into `sources/extracted/`:
`slides/*.txt` for the decks and `manual/*.txt` for the manual.

## The ledger

`data/phy121/ledger/reference.json`, **114 facts, 106 hard**, drawn from the
manual's reference part:

| Section | Facts | What it holds |
| --- | --- | --- |
| Ref R.1 | 61 | The constant and formula sheet |
| Ref R.2 | 20 | The must-memorise list, each with its hook |
| Ref R.3 | 8 | The seven-step problem-solving method |
| Ref R.4 | 25 | The glossary |

At one question per soft fact and two per hard fact, the ledger asks for **220
questions**. The ledger gate is therefore NOT yet armed; it would fail. It is
armed once the bank covers every fact, exactly as IFT222 was done.

## Question files

| File | Holds |
| --- | --- |
| `module1.json` to `module10.json` | the 30 past-paper questions, by topic |
| `deck1.json` to `deck9.json` | questions written from the manual, by topic |

## Progress

| | Questions | State |
| --- | --- | --- |
| Both computer-based tests | 30 | done, both sit to 100 per cent |
| Batch 1: constants and the must-memorise list | 51 | done |
| Remaining ledger facts | about 170 | to do |
| Crash course lessons | | to do |
| Crash manual PDF | | to do |

**81 questions so far.**

## Things found in the sources, kept as found

- **Test 1 Q9 cannot be keyed.** Its stem ends at "represented by" with the
  figure missing, and it is the one question the examiner marked wrong, so the
  capture shows the selected option was wrong without revealing the right one.
  It is quoted as printed, keyed to the selected option purely so the paper
  stays answerable, and all five of its verdicts say openly that it cannot be
  judged.
- **Test 1 Q1 is unsolvable as printed.** It asks for the work done on a charge
  moving 50 cm but never gives a field strength. The marked answer follows only
  if E is taken as 1 V/m, and the explanation says so.
- **Test 1 Q2 carries a figure**, the first on the platform. C1 and C2 are in
  series in one branch, in parallel with C3: 5/6 + 8 = 8.8 uF.
