# Side quest: the Quira challenge

**The book:** *Towards Mental Exploits* by David Oyedepo, 79 pages, 11 chapters.
**The app:** Quira, exhibiting at AYAC 2026. Upload a document, get quizzed.
**The prize:** 500,000.
**Judged on:** speed and accuracy.
**Where to practise:** `/quira` on the drill platform.

---

## What was built

| Piece | Where | What it is |
|---|---|---|
| Sources | `sources/` | The book PDF, and the ten screenshots of quiz 1 with its answer key |
| Quiz 1 transcript | `sources/quiz1/QUIZ1_TRANSCRIPT.md` | All 30 questions and answers, plus the analysis of how their AI sets questions |
| UI spec | `ui of the app/UI_SPEC.md` | Every design token and screen, read off the 14 app screenshots |
| Fact ledger | `webapp/data/quira/ledger/*.json` | **803 atomic facts** covering all 79 pages, in 14 passages |
| Question bank | `webapp/data/quira/topic*.json` | **419 questions**, every option explained |
| The trainer | `webapp/app/quira/` + `webapp/components/quira/` | The app, skinned to look and feel like Quira |
| The gate | `webapp/scripts/validate-quira.mjs` | Eight checks; runs on every build |

## How their AI sets questions

Deduced from 40 real questions across two quizzes.

1. **Passage framing.** "The passage argues / claims / defines / cites", "According
   to the teaching", "as noted in the material". The answer is always *in* the text.
2. **Definition recall** — the book's own definition, near verbatim.
3. **Named people** — every proper name is a target, and so is what they said.
   T. L. Osborn, Abraham Lincoln, Anthony Robbins, Oswald J. Smith, Norman Vincent
   Pearle, Kenneth E. Hagin, Smith Wigglesworth, Zig Ziglar, E. W. Kenyon, Bill
   Gates, Isaac Newton, David Yonggi Cho, Frederick K. C. Price, Benson Idahosa,
   Bishop Abioye.
4. **Numbers** — 700 books, age 93, 96 years, 72 years, 1974, 5%/15%/80%, 26 months,
   3,000 converts, 700 wives and 300 concubines, 16 and 10 million naira, 64 years,
   36 years, two kilometres, May 1981.
5. **Scripture citations**, both directions: "which verse says X" and "what does
   Ephesians 1:17-18 ask for".
6. **Verbatim quotes** — as stems and as answers.
7. **Metaphors and analogies** — the building, the divine deposit, the engine oil,
   the poultry farm, debt-pressure.
8. **Contrasts and outcomes** — carnal vs spiritual, knowledge vs understanding.
9. **Cause and reason** — "Why does the passage claim...".

## The one rule that decides the prize

Both questions missed in quiz 1 were missed the same way: a **plausible generic
self-help answer** was chosen over **what the book literally says**.

- Q26 asked for the metaphor about using the mind. "The mind is a garden that needs
  watering" is a real metaphor, just not this book's. The book says **"every divine
  deposit multiplies with use"**, from the parable of the talents.
- Q21 asked what people who stop learning do. "Focusing on technical manuals rather
  than wisdom" sounds exactly like this book. What it actually says is they **"read
  the conclusion and probably the introduction, and then close the book"**.

> **When two options both sound right, the one carrying the book's own vocabulary is
> the key.** The distractors are written by an LLM that has read a lot of self-help,
> so they arrive smooth and familiar. The book's own phrasing is blunter, more
> scriptural, or oddly specific: *youngen*, *divine think-tank*, *wisdom knockouts*,
> *sweatless triumph*, *the 700-in-one man*, *debt-pressure*.

The bank is built around this. Wherever a familiar-sounding wrong answer exists, it
is *in the options*, and the review says why it is wrong.

## The pace to beat

The app reported **02:54 for ten questions**, which is **17.4 seconds each**,
including reading four options. The trainer times every question and grades the pace
against that benchmark on the completion screen.

Quiz lengths seen: **10 and 30**. Grade A+ is awarded at **100%**.

## Using the trainer

    cd webapp && npm run dev      # then open /quira

- **Exam mode** behaves like the real thing: answer everything, then mark.
- **Coach mode** marks each question the moment you commit and shows why each of the
  other three is wrong. This is where the traps get learned.
- **Study** lists every question with its key, reason and page reference.
- Anything missed is **weighted to the front of the next paper** until it is cold.
- Options are **shuffled every time**, so nothing can be memorised by position.

## What the gate enforces

Run with `npm run validate:quira`; it also runs on every `npm run build`.

1. **Schema** — unique ids, keys that point at real options, four options on every
   MCQ, gap choices that contain the answer.
2. **Ledger** — all 803 facts asked about, no invented fact ids.
3. **Provenance** — a question may only name a fact whose page it also cites.
4. **Verdicts** — every option of every MCQ and TF carries a reason.
5. **No letters** — no explanation may name an option by letter or position.
6. **Topic spread** — all 14 passages carry real coverage.
7. **Renderable** — enough of the bank is drawable as four-option single-select.
8. **The key** — cross-checked against all **40 answers Quira itself marked
   correct**. An independent second copy of the key; disagreement fails the build.

All eight were **control-tested**: each was deliberately broken, confirmed to fail,
and restored.

## Coverage

```
topic  1  Understanding the Mind ................ 82 facts   Intro + Ch1, pp 3-8
topic  2  Learning and Knowledge ................ 62 facts   Ch2, pp 9-12
topic  3  Understanding and Meditation .......... 37 facts   Ch2, pp 12-14
topic  4  Reasoning ............................. 37 facts   Ch2, pp 14-17
topic  5  Imagination ........................... 40 facts   Ch2, pp 17-20
topic  6  Supernatural Mentality ................ 44 facts   Ch3, pp 21-25
topic  7  Seat of Wisdom ........................ 87 facts   Ch4, pp 26-34
topic  8  Products of Divine Wisdom ............. 64 facts   Ch5, pp 35-40
topic  9  Wisdom Can Be Lost .................... 43 facts   Ch5, pp 41-45
topic 10  The Place of Inspiration .............. 49 facts   Ch6, pp 46-50
topic 11  Creating the Right Atmosphere ......... 45 facts   Ch7, pp 51-54
topic 12  Exercising the Mind ................... 82 facts   Ch8, pp 55-64
topic 13  Obstacles to Mental Excellence ........ 84 facts   Ch9, pp 65-73
topic 14  Mental Revolution / Now You Know ...... 47 facts   Ch10-11, pp 74-79
                                                 ---------
                                                 803 facts, all tested
```

## Two things worth confirming before tomorrow

1. **Is the challenge definitely on this book?** Everything here assumes it is. If
   they hand out a different document on the day, the bank is worthless and what
   carries over is the technique: their question grammar, the generic-answer trap,
   and the 17.4s pace.
2. **Is it definitely Multiple Choice?** The app also does flashcards, and the
   results screen labels the type "Multiple Choice", which implies other types
   exist. The bank holds 16 gap-fill and 2 matching questions for that case, but the
   trainer's paper is single-select only, matching what has been seen.
