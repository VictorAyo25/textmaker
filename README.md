# manual_composer

Workspace for building active-recall study manuals from course slide decks and past tests.

```
manual_composer/
├── README.md                 you are here
├── MANUAL_METHODOLOGY.md     the playbook: how these manuals are designed + built
│                             (course-agnostic — read this first for any new course)
├── FINAL_MANUALS/            ← THE ONLY PUBLISHED OUTPUT. All courses. Signed off only.
│   ├── README.txt
│   └── PHY121 - General Physics II - Study Manual v4.pdf
└── courses/                  ← one self-contained working folder per course
    ├── PHY121 - General Physics II/
    │   ├── README.md         how to rebuild/update THIS course
    │   ├── build/            code + assets
    │   ├── sources/          raw inputs: slides/ tests/ manual_v1/ extracted/
    │   └── drafts/           work in progress
    └── COS221 - Computer Programming I (Java)/
        ├── README.md
        └── sources/          slides/ exams/ course_manual/ extracted/
```

## The three rules that keep this tidy

1. **Every course gets its own folder under `courses/`.** All of its sources,
   code, and drafts stay inside it. Nothing course-specific ever sits at the top
   level. Starting PHY122 means creating its folder and nothing else moves.
2. **`FINAL_MANUALS/` is central and holds only signed-off PDFs**, one per course
   (versioned, e.g. `_v2`). Work in progress lives in that course's `drafts/`.
   Nothing lands in `FINAL_MANUALS/` until the manual is explicitly approved.
3. **Name-and-title rule.** A course folder and its produced manual both carry the
   course **code and title**, never the bare code:

   ```
   courses/COS221 - Computer Programming I (Java)/
   FINAL_MANUALS/COS221 - Computer Programming I (Java) - Study Manual v1.pdf
   ```

   A bare code is unreadable a year later, and course titles do drift (COS221 was
   "Object-Oriented Programming (Java)" in 2024/25 and "Computer Programming I
   (Java)" in 2025/26), so the title in the name records which one the manual was
   built for. PHY121 was renamed to match on 2026-07-17; the rule is universal, with
   no grandfathered exceptions.

   Folder names contain spaces, so **quote paths** in the shell:
   `cd "courses/PHY121 - General Physics II/build"`.

## Working on two courses at once

Two chats building **different** courses is fine. Every path the build touches is
derived from the course's own folder, so two courses share no file: separate
code, `content/`, `sources/`, and PDF. `FINAL_MANUALS/` names are per-course too.

Two things to know:

1. **Git is the one shared thing.** Never `git add -A` while another chat is
   working: it would sweep that course's half-finished files into your commit.
   Stage one course at a time:
   ```bash
   tools/commit_course.sh "PHY121 - General Physics II" "message"   # that course only
   tools/commit_course.sh "PHY121 - General Physics II" "message" MANUAL_METHODOLOGY.md
   ```
   Before pushing, `git pull --rebase` in case the other chat pushed first.
2. **Never build the same course in two chats.** They would overwrite each
   other's `content/` and PDF. `build/.build.lock` now makes that fail loudly
   instead of silently losing work; a lock left by a crashed build is detected as
   stale and taken over automatically.

## Starting a new course

```bash
C="courses/<CODE> - <Course Title>"       # name-and-title rule, see above
mkdir -p "$C"/{build,drafts}
mkdir -p "$C"/sources/{slides,exams,extracted}
# slide decks     -> sources/slides/
# past papers/CBTs -> sources/exams/
# a lecturer's or institution's manual is a SOURCE -> sources/course_manual/
# a prior manual OF OURS that we rebuild verbatim  -> sources/manual_v1/
```

That last distinction decides the whole architecture. If `manual_v1/` exists, the
job is a **rebuild**: preserve wording verbatim and audit fidelity (PHY121). If the
only manual is someone else's, it is a **source** and the job is to **author** from
zero (COS221), so skip the extraction and fidelity machinery entirely.

Then read `MANUAL_METHODOLOGY.md` — it carries the pedagogy (the box system,
active recall, traps, "every number recomputed") and the build engineering
(structure-aware PDF extraction, the 2-pass Contents render, the print-CSS
traps). `courses/PHY121 - General Physics II/build/` is a working reference
implementation to copy from.

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
tools/commit_course.sh "PHY121 - General Physics II" "what changed"   # that course only
git pull --rebase && git push
```

Use the helper rather than `git add -A`: if another chat is mid-edit on a
different course, `-A` would commit its half-finished work as part of yours.

To restore onto a new machine:

```bash
git clone https://github.com/<you>/study-manuals.git
cd "study-manuals/courses/PHY121 - General Physics II/build"
pip install playwright pymupdf pillow && python -m playwright install chromium
python assemble.py        # rebuilds the full manual
```

## House rules (apply to every course)

- No em dashes or en dashes in any manual.
- Never name the institution, its e-learning platform, or any methodology author.
- Every number is recomputed independently before it is written down. For a
  programming course the same rule reads: every snippet is compiled and run, and
  every claimed output is captured from a real run, never asserted from reading.
- **Zero to perfect score, zero external sources.** A manual must carry a complete
  novice to a perfect exam score on its own. The reader must never need a lecturer,
  a website, or official docs, so the manual teaches its own toolchain and documents
  every API it uses. Nothing may appear before it has been introduced.
- Course folders and published manuals both carry the course code and title.
- A manual reaches `FINAL_MANUALS/` only on explicit sign-off.
