# The Bible reading plan generator

Builds `BIBLE_PLAN_AUG_NOV_2026.md` and `BIBLE_PLAN_LINES.txt` at the repo root.

```bash
cd tools/bible_plan && python make_plan.py
```

## Why it is a program and not a spreadsheet

The requirement was that **no day ever stops in the middle of a context**. That
turns "divide 1,158 chapters by 99 days" into a different problem: the cut points
are not free, they are drawn from a fixed list of real section boundaries (the end
of the flood narrative, the end of the Sermon on the Mount, the end of Paul's
argument in Romans 9 to 11). Choosing which of those to use, so the daily loads
come out as even as they can, is an exact partition problem. `make_plan.py` solves
it with dynamic programming rather than walking forward and hoping.

`bible_data.py` holds the legal break points for all 66 books. That file is the
substance; the solver is 40 lines.

Two further decisions worth keeping:

- **Load is counted in verses, not chapters.** A Psalms chapter averages 16 verses
  and a Kings chapter over 30, so an even split by chapter count would have made
  some days twice the reading of others.
- **Finishing a book earns a small bonus**, so where two cuts score equally the
  plan prefers the one that ends the book.

## The shape, and why it is not strict alternation

The plan alternates whole days between the testaments rather than mixing them,
which is deliberate: the standard criticism of the M'Cheyne and Grant Horner
systems is that reading four or ten places at once fragments the text, and
whole-session reading of large units is the better-supported approach.

But the Old Testament is 22,230 verses against the New Testament's 7,957. Strict
one-to-one alternation therefore gives 394 to 500 verses one day and 96 to 223 the
next, a **4.2x** swing, 18 minutes against 76. A two-OT-to-one-NT cycle brings that
to **2.1x**, 32 to 67 minutes, while still putting the New Testament in view every
third day. A three-to-one cycle is flatter again (2.0x) but drops the New
Testament to every fourth day, which is the wrong trade during Leviticus.

Change the cycle by editing the `build([...])` call at the bottom.

## Verification

`emit.verify()` runs BEFORE anything is written and raises rather than writing, so
a bad plan cannot reach the repo root. It checks three things, and each one is a
failure that would otherwise be invisible in the output: a dropped chapter looks
like a shorter day, and an illegal break looks like a normal one.

1. All 898 Old Testament and 260 New Testament chapters appear exactly once, in
   order.
2. Every day ends on a chapter declared as a section boundary.
3. The dates run unbroken and the Proverbs chapter equals the day of the month.

Control-tested by feeding it known-bad plans and requiring each to fail, since a
gate nobody has broken on purpose is a gate nobody knows works. Four mutations, all
caught and all naming the offending day: a dropped chapter, a wrong Proverbs
chapter, a gap in the calendar, and a day stopping mid-section. The last needed
care: the obvious way to write that test also made the plan incomplete, so it was
passing for the wrong reason until the mutation was isolated to a single defect.
