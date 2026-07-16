# manual_composer

Workspace for building active-recall study manuals from course slide decks and past tests.

```
manual_composer/
├── README.md                 you are here
├── MANUAL_METHODOLOGY.md     the playbook: how these manuals are designed + built
│                             (course-agnostic — read this first for any new course)
├── FINAL_MANUALS/            ← THE ONLY PUBLISHED OUTPUT. All courses. Signed off only.
│   ├── README.txt
│   └── PHY121_Study_Manual_v2.pdf
└── courses/                  ← one self-contained working folder per course
    └── PHY121/
        ├── README.md         how to rebuild/update THIS course
        ├── build/            code + assets
        ├── sources/          raw inputs (slides, tests, prior manual)
        └── drafts/           work in progress
```

## The two rules that keep this tidy

1. **Every course gets its own folder under `courses/`.** All of its sources,
   code, and drafts stay inside it. Nothing course-specific ever sits at the top
   level. Starting PHY122 means creating `courses/PHY122/` and nothing else moves.
2. **`FINAL_MANUALS/` is central and holds only signed-off PDFs**, one per course
   (versioned, e.g. `_v2`). Work in progress lives in that course's `drafts/`.
   Nothing lands in `FINAL_MANUALS/` until the manual is explicitly approved.

## Starting a new course

```bash
mkdir -p courses/<COURSE>/{build,sources,drafts}
# put the slide decks / tests / any prior manual in courses/<COURSE>/sources/
```
Then read `MANUAL_METHODOLOGY.md` — it carries the pedagogy (the box system,
active recall, traps, "every number recomputed") and the build engineering
(structure-aware PDF extraction, the 2-pass Contents render, the print-CSS
traps). `courses/PHY121/build/` is a working reference implementation to copy from.

## House rules (apply to every course)

- No em dashes or en dashes in any manual.
- Never name the institution, its e-learning platform, or any methodology author.
- Every number is recomputed independently before it is written down.
- A manual reaches `FINAL_MANUALS/` only on explicit sign-off.
