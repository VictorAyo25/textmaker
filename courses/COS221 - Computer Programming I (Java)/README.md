# COS221 — Computer Programming I (Java) — working folder

Everything needed to build or update the COS221 study manual lives here. The finished
PDF is published to `../../FINAL_MANUALS/` as
`COS221 - Computer Programming I (Java) - Study Manual v1.pdf`, and only on explicit
sign-off.

```
COS221 - Computer Programming I (Java)/
├── build/      all code + assets (fonts vendored)
├── sources/    the raw inputs
│   ├── slides/         13 lecturer decks, 408 slides, Modules 1 to 10
│   ├── exams/          exam_2024_25.pdf, exam_2025_26.pdf
│   ├── course_manual/  CCODeL's official 222-page manual (a SOURCE, see below)
│   └── extracted/      transcripts + page renders, regenerable
└── drafts/     work in progress (never the published copy)
```

## Status

Intake complete. Both papers transcribed and verified; exam analysis written. Build
not yet started. Next: port the build pipeline from PHY121, then author Modules 1 to 2
as a style checkpoint.

## This manual is AUTHORED, not rebuilt

The important difference from PHY121. PHY121 had `sources/manual_v1/`, a prior manual
**of ours**, so its build reproduced that manual verbatim and needed structure-aware
extraction plus a word-level fidelity audit to prove nothing was lost.

COS221 has no such thing. The 222-page manual in `course_manual/` is the
institution's, i.e. an input to learn from, not an artifact to reproduce. So:

- **Do not** port `reconstruct.py`, `struct_extract.py`, `recon_back.py`, `freeze.py`
  or the fidelity audits from PHY121. There is nothing to be faithful to.
- **Do** port the build pipeline: Chromium render, vendored DejaVu fonts, the 2-pass
  Contents resolve, named-to-GoTo link conversion, marker stripping, and the QA gates
  for house style and layout.

## Course facts

- Lecturer: Mr. Otavie Okuoyo. Omega semester, 3 credit units, 3-hour written exam.
- Deck numbering matches the course manual exactly: 13 decks = 13 units over Modules 1
  to 10. No PHY121-style off-by-one quirk. (Verified, not assumed.)
- The course was retitled between sessions: "Object-Oriented Programming (Java)" in
  2024/25, "Computer Programming I (Java)" in 2025/26. Same code, COS221.

## The exam (see `sources/extracted/exam_analysis.md`)

The format changed between years but the skills did not. Both papers are 70 marks over
3 hours and test exactly four things: **define**, **debug**, **dry run**, **write a
program**. Teach the four skills, not a paper format, and write mocks in both shapes.

The 25/26 paper is written long-form with Sections A/B/C (attempt one from each). It is
**not** a CBT multiple-choice test, so the manual must train writing Java on paper,
tracing code by hand, and finding bugs, not recognising right answers.

## Hard QA gates for this course

1. **Every snippet compiles and runs.** JDK 17 (Temurin) is installed. Claimed outputs
   are captured from a real JVM, never asserted from reading. This is the local form of
   the house rule "recompute every number".
2. **Keyword/API before use.** The manual must be sufficient with no external sources,
   so every keyword, symbol, and library call is introduced before first appearance and
   every API used gets an in-manual reference card. Script this check over the built
   HTML; do not eyeball it.
3. Plus the house gates: no em/en dashes, no institution or methodology names, no
   near-blank pages, footer numbering, resolved Contents links.

## Rebuild

Not yet wired. Will be `cd build && python assemble.py` once the pipeline is ported.
