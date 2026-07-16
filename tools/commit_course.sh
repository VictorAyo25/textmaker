#!/usr/bin/env bash
# Commit ONE course's work, plus the shared docs if they changed.
#
# Why this exists: the repo is shared by every course, so `git add -A` from a chat
# working on PHY121 would sweep in whatever another chat has half-finished in
# PHY122 and commit it as if it were yours. This stages one course only.
#
#   tools/commit_course.sh PHY121 "Fix the capacitor worked example"
#
# Pass extra paths after the message to include shared files deliberately:
#   tools/commit_course.sh PHY121 "Update playbook" MANUAL_METHODOLOGY.md
set -euo pipefail

COURSE="${1:-}"; MSG="${2:-}"; shift 2 || true
if [ -z "$COURSE" ] || [ -z "$MSG" ]; then
  echo "usage: tools/commit_course.sh <COURSE> <message> [extra paths...]" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -d "courses/$COURSE" ]; then
  echo "no such course: courses/$COURSE" >&2
  exit 2
fi

git add -- "courses/$COURSE" "$@"

if git diff --cached --quiet; then
  echo "nothing staged for $COURSE"
  exit 0
fi

echo "staging for $COURSE:"
git diff --cached --name-only | sed 's/^/  /'

# Warn if another course has uncommitted work: it is not being committed (good),
# but it means a second chat may be running, so do not push over it blindly.
OTHERS="$(git status --porcelain -- courses | grep -v "courses/$COURSE" | head -3 || true)"
if [ -n "$OTHERS" ]; then
  echo
  echo "note: another course has uncommitted work, left untouched:"
  echo "$OTHERS" | sed 's/^/  /'
fi

git commit -q -m "$MSG"
git log --oneline -1
