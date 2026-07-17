#!/usr/bin/env bash
# Commit ONE course's work, plus the shared docs if they changed.
#
# Why this exists: the repo is shared by every course, so `git add -A` from a chat
# working on PHY121 would sweep in whatever another chat has half-finished in
# PHY122 and commit it as if it were yours. This stages one course only.
#
#   tools/commit_course.sh "PHY121 - General Physics II" "Fix the capacitor example"
#
# Course folders carry code AND title, so they contain spaces: always quote.
#
# Pass extra paths after the message to include shared files deliberately:
#   tools/commit_course.sh "PHY121 - General Physics II" "Update playbook" MANUAL_METHODOLOGY.md
set -euo pipefail

COURSE="${1:-}"; MSG="${2:-}"; shift 2 || true
if [ -z "$COURSE" ] || [ -z "$MSG" ]; then
  echo "usage: tools/commit_course.sh <COURSE> <message> [extra paths...]" >&2
  echo "       tools/commit_course.sh <COURSE> -F <msgfile> [extra paths...]" >&2
  exit 2
fi

# -F <file> for long messages. A multi-line message passed inline is a trap: any
# double quote inside it ends the shell's quoting, and the rest of the prose is
# then handed to git as pathspecs ("fatal: pathspec 'anticlockwise' did not
# match any files").
MSGFILE=''
if [ "$MSG" = "-F" ]; then
  MSGFILE="${1:-}"; shift || true
  if [ ! -f "$MSGFILE" ]; then echo "no such message file: $MSGFILE" >&2; exit 2; fi
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ ! -d "courses/$COURSE" ]; then
  echo "no such course: courses/$COURSE" >&2
  exit 2
fi

# git serialises on .git/index.lock. That is momentary, but with several chats
# committing at once one of them can land on it, so retry rather than fail.
git_retry() {
  local n=0
  until git "$@"; do
    n=$((n+1))
    if [ "$n" -ge 5 ]; then
      echo "git $1 failed after $n attempts" >&2
      return 1
    fi
    echo "  git index busy (another chat is committing), retry $n..." >&2
    sleep 1
  done
}

git_retry add -- "courses/$COURSE" "$@"

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

if [ -n "$MSGFILE" ]; then
  git_retry commit -q -F "$MSGFILE"
else
  git_retry commit -q -m "$MSG"
fi
git log --oneline -1
