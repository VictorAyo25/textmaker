# Quira UI, read off the fourteen screenshots

## Screens seen

1. **Quiz runner** (8 shots, questions 01-10)
2. **Quiz Complete** (the trophy screen)
3. **Quiz Results** (summary card + Question Breakdown)
4. **Quiz History** (Overview tiles + Recent practice + bottom tab bar)

## Runner

- White header. Back chevron left in muted blue. Centre title is the counter,
  bold, in the form `01 of 10` (zero padded).
- Progress bar directly under the header: full-width rounded pill, track
  #E0E0E0, fill the primary blue, animating one tenth per question.
- Page body sits on a very light grey (#F7F8FA), header stays white, so there
  is a visible seam under the progress bar.
- `Question 01` in muted slate, zero padded, regular weight.
- Stem in heavy geometric sans, about 26px, tight leading, black.
- Four option cards. White, radius ~14, 1px #E5E7EB border, roomy padding,
  text left aligned, medium weight, wraps to two or three lines.
- Selected option: background #E8EEFC, border #A9C0F5. No radio dot, no letter.
  **The options carry no A/B/C/D labels at all.**
- Bottom bar, white, three slots: `Previous` (grey, disabled on Q1), a
  four-square blue grid glyph in the centre (jump to any question), and the
  primary action right: `Next`, which becomes `Submit` on question 10.

## Quiz Complete

- Blue trophy with a white star.
- `Quiz Complete!` in primary blue, heavy.
- Sub: `Here's how you performed on this session.`
- Three stat tiles side by side, each a coloured header strip over a white body:
  - `Grade A+` header in light blue, body `100%`
  - `Score` header in primary blue, body `10/10`
  - `Time spent` header in dark navy, body `02:54`
- Buttons stacked full width: `Continue Practice` (blue), `Review Mistakes`
  (dark navy), `Save as flashcards` (blue), then `Go Home` as a plain text link.

## Quiz Results

- Faint blue page tint (#F2F7FD), not the runner's grey.
- Back chevron sits in a rounded light-blue square. Blue hexagon top right.
- Summary card: `Multiple Choice` left, `20 Aug 2026  17:40` right, then a large
  `10 /10`, a green circle pill showing `100%`, and a green progress bar.
- Tip banner, pale indigo, lightbulb glyph: `Excellent work! You scored 10.0 out of 10.`
- `Question Breakdown` heading, then one card per question:
  - green check circle (or red cross), `Question N`, and a `100%` / `0%` pill
  - stem in bold
  - divider
  - `Your answer:` then the text
  - `Correct answer:` in green
  - `Feedback:` `Correct!` or `Incorrect. The correct answer was: ...`

## Quiz History

- `Overview` with a 2x2 grid of tiles: `2 Quizzes`, `40 Questions`,
  `97% Average Score`, `100% Best Score`. The first two use blue glyphs, the
  score tiles a gold trophy.
- `Recent practice` with `View all` on the right, then cards showing the
  document title truncated (`Towards Mental E...`), the type `Multiple Choice`,
  a big `10`/`10`, and a blue progress bar.
- Bottom tab bar: Home, Study, a raised blue circular mascot, Quiz History,
  Profile. Active tab in blue.

## Tokens

| role | value |
|---|---|
| primary blue | #1652F0 |
| blue hover/light | #2F6BFF |
| selected option fill | #E8EEFC |
| selected option border | #A9C0F5 |
| dark navy | #0F2942 |
| page grey (runner) | #F7F8FA |
| page tint (results) | #F2F7FD |
| card border | #E5E7EB |
| muted label | #7A8B99 |
| correct green | #22A45D |
| correct pill bg | #E6F5EC |
| wrong red | #E5484D |
| wrong pill bg | #FDECEC |
| card radius | 14-16px |

Headings are a geometric sans with a single storey `g` (Poppins). Option and
body text is a neutral grotesque (Inter).

## Intel that changes how we drill

- **Quiz lengths seen: 10 and 30.** History says `2 Quizzes / 40 Questions`.
- **Ten questions took 02:54.** That is 17.4 seconds a question including
  reading four options. Speed is half the judging, so the drill must run a
  clock and hold a per question pace, not just a total.
- **Grade A+ is awarded at 100%.** Nothing below is the target.
- **Four options, single select, no letters.** So an answer can never be
  memorised as "the third one"; the drill must shuffle and must never name an
  option by position.
- The quiz type is labelled **Multiple Choice**, implying other types exist
  (the app also does flashcards), so a different type may appear on the day.
