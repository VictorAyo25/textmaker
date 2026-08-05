# IFT222 on the drill: build state

The course went on the platform with the 120 past-paper questions only. This
build adds the eight lecture decks, so a reader who has never seen the course
can learn it by testing.

## What the sources are

Eight decks, 413 slides, extracted to
`courses/IFT222 - Computer Architecture and Organisation/sources/extracted/deck_<Key>.txt`:

| Key | Deck | Slides | Content slides |
| --- | --- | --- | --- |
| Intro | General intro and course overview | 57 | 45 |
| Data | Data representation | 73 | 60 |
| ISA | Instruction set architecture | 60 | 38 |
| Mem | Memory hierarchy and cache design | 65 | 53 |
| Cache | Solved examples, cache mapping | 14 | 12 |
| RISC | RISC versus CISC | 36 | 30 |
| Pipe | Improving performance through pipelining | 57 | 43 |
| Rev | Revision class | 51 | 45 |

**326 content slides.** The exclusions, and why each one carries nothing
testable, are written down in `scripts/ift-slides.mjs`, which is the single
source of truth the gate reads.

Provenance refs are `Intro S4`, `Data S15`, `ISA S22`, `Mem S37`, `Cache S2`,
`RISC S9`, `Pipe S13`, `Rev S21`, alongside the existing `Test 1 Q16` shape.

## The ledger

`data/ift222/ledger/*.json`, **600 facts**, at least one per content slide.
`hard: true` means an examiner could take a mark off for it: a number, a name,
a formula, an enumerated list, or a definition that could be quoted back.
`hard: false` is context, narrative, a revision-deck restatement, or a note on
what an exercise asks rather than what its answer is. 524 hard, 76 soft, so the
gate demands **1,124 questions** at a minimum, and the build came to 1,125: every fact once, every hard fact in two
or more styles.

Filenames are for humans only. The gate reads every `.json` in the directory and
groups by the `topic` field, which is why some topics are split across two files
(`topic08-memory.json` and `topic08-cpu.json` feed the same topic from two
different decks).

## Topics

The ten original topics are unchanged. Two are added because the Cache and
Pipelining decks would otherwise have swamped topics 8 and 9:

- **11 Cache Mapping Functions** (Mem S39 onward, the whole Cache deck, Rev S38 to S49)
- **12 Pipelining and Hazards** (the whole Pipe deck, RISC S27, Rev S21 to S36)

Topic 9 is rescoped to *Performance, RISC and CISC*.

Rev S38 to S49 repeat Cache S2 to S13 slide for slide, so topic 11 questions
cite both refs rather than the ledger carrying the same fact twice.

## Question files

Past-paper questions stay in `module1.json` to `module10.json`, untouched, so
the two papers still rebuild themselves by provenance tag. New deck-drilled
questions go in `deck01.json` to `deck12c.json`. A topic whose questions
outgrew one file splits with a letter suffix (`deck08a`, `deck08b`, `deck08c`);
the letter is presentation only, since every question carries its own `module`.

| Topic | Facts | Questions | State |
| --- | --- | --- | --- |
| 1 Architecture versus Organization | 37 | 62 | done |
| 2 ISA and Microarchitecture | 39 | 68 | done |
| 3 Number Systems and Codes | 48 | 88 | done |
| 4 Signed Numbers and Complements | 44 | 83 | done |
| 5 Floating Point and IEEE 754 | 27 | 53 | done |
| 6 Instruction Types and Formats | 29 | 56 | done |
| 7 Addressing Modes | 26 | 52 | done |
| 8 Memory, Buses and CPU Components | 73 | 137 | done |
| 9 Performance, RISC and CISC | 80 | 150 | done |
| 10 Von Neumann, Harvard and Image Data | 22 | 43 | done |
| 11 Cache Mapping Functions | 66 | 129 | done |
| 12 Pipelining and Hazards | 109 | 204 | done |
| **Total** | **600** | **1125** | |

## Done

The bank is 1,245 questions: the 120 past-paper questions untouched in
`module1.json` to `module10.json`, and 1,125 written from the decks in
`deck01.json` to `deck12c.json`. Both papers still rebuild themselves by
provenance tag and both sit to 100 per cent against the key in the built app.

The gate now enforces, for IFT222:

- every one of the 326 content slides is cited by at least one question;
- every one of the 600 ledger facts is tested, and every hard fact in two or
  more styles;
- every deck question names a ledger fact whose own reference it also cites;
- past-paper questions are exempt from that last rule, because the two tests
  range wider than the decks and inventing a deck ref for them would be a lie;
- all six question styles appear somewhere in the bank;
- every option of every option-bearing question carries a verdict.

All seven rules were broken on purpose and each one failed the build.

## Things found in the sources, kept as found

- **Data S11** groups `110101101011101` into `110 1011 0101 1101`, then labels
  the last group "13D=CH" and prints the answer `6B5C`. 13 decimal is hex D, so
  the grouping gives `6B5D`. Fact `t3-015` records both, and questions on it say
  so, because a reader who copies the slide would be marked wrong.
- **Rev S7** prints the two's complement of minus 1023 with seventeen digits in
  a sixteen-bit register. The hex, FC01, is right. Fact `t4-043` records it.
- **Test 1 Q19** is keyed by the examiner as Sign, Mantissa, Exponent, while
  IEEE 754 orders the fields Sign, Exponent, Mantissa. That was already noted on
  the question when the paper was transcribed, and it stays noted.
