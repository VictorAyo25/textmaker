# manual_composer

Workspace for building active-recall study manuals from course slide decks and past tests.

```
manual_composer/
├── README.md                 you are here
├── MANUAL_METHODOLOGY.md     the playbook: how these manuals are designed + built
│                             (course-agnostic — read this first for any new course)
├── FINAL_MANUALS/            ← THE ONLY PUBLISHED OUTPUT. All courses. Signed off only.
│   ├── README.txt
│   └── PHY121_Study_Manual_v3.pdf
└── courses/                  ← one self-contained working folder per course
    └── PHY121/
        ├── README.md         how to rebuild/update THIS course
        ├── build/            code + assets
        ├── sources/          raw inputs, grouped: slides/ tests/ manual_v1/ extracted/
        └── drafts/           work in progress
```

## The two rules that keep this tidy

1. **Every course gets its own folder under `courses/`.** All of its sources,
   code, and drafts stay inside it. Nothing course-specific ever sits at the top
   level. Starting PHY122 means creating `courses/PHY122/` and nothing else moves.
2. **`FINAL_MANUALS/` is central and holds only signed-off PDFs**, one per course
   (versioned, e.g. `_v2`). Work in progress lives in that course's `drafts/`.
   Nothing lands in `FINAL_MANUALS/` until the manual is explicitly approved.

## Working on two courses at once

Two chats building **different** courses is fine. Every path the build touches is
derived from `courses/<COURSE>/`, so PHY121 and PHY122 share no file: separate
code, `content/`, `sources/`, and PDF. `FINAL_MANUALS/` names are per-course too.

Two things to know:

1. **Git is the one shared thing.** Never `git add -A` while another chat is
   working: it would sweep that course's half-finished files into your commit.
   Stage one course at a time:
   ```bash
   tools/commit_course.sh PHY121 "message"        # stages courses/PHY121 only
   tools/commit_course.sh PHY121 "message" MANUAL_METHODOLOGY.md   # + shared file
   ```
   Before pushing, `git pull --rebase` in case the other chat pushed first.
2. **Never build the same course in two chats.** They would overwrite each
   other's `content/` and PDF. `build/.build.lock` now makes that fail loudly
   instead of silently losing work; a lock left by a crashed build is detected as
   stale and taken over automatically.

## Starting a new course

```bash
mkdir -p courses/<COURSE>/{build,drafts}
mkdir -p courses/<COURSE>/sources/{slides,tests,manual_v1,extracted}
# slide decks -> sources/slides/, test screenshots -> sources/tests/,
# any prior manual -> sources/manual_v1/
```
Then read `MANUAL_METHODOLOGY.md` — it carries the pedagogy (the box system,
active recall, traps, "every number recomputed") and the build engineering
(structure-aware PDF extraction, the 2-pass Contents render, the print-CSS
traps). `courses/PHY121/build/` is a working reference implementation to copy from.

## Backup to GitHub

This folder is a git repo. Everything needed to rebuild every manual from
scratch is committed; only regenerable build outputs and drafts are ignored.

First time (one interactive login, then push):

```bash
gh auth login                                   # pick GitHub.com -> HTTPS -> browser
gh repo create study-manuals --private --source=. --remote=origin --push
```

Use `--private`: these are your course materials and carry your name.

After that, whenever you change something:

```bash
tools/commit_course.sh PHY121 "what changed"    # stages that course only
git pull --rebase && git push
```

Use the helper rather than `git add -A`: if another chat is mid-edit on a
different course, `-A` would commit its half-finished work as part of yours.

To restore onto a new machine:

```bash
git clone https://github.com/<you>/study-manuals.git
cd study-manuals/courses/PHY121/build
pip install playwright pymupdf pillow && python -m playwright install chromium
python assemble.py        # rebuilds the full manual
```

## House rules (apply to every course)

- No em dashes or en dashes in any manual.
- Never name the institution, its e-learning platform, or any methodology author.
- Every number is recomputed independently before it is written down.
- A manual reaches `FINAL_MANUALS/` only on explicit sign-off.
