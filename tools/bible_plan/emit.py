"""Emit and verify the plan. Imported by make_plan.py, which does the solving.

verify() runs BEFORE emit() and raises rather than writing, so a plan that drops a
chapter or stops in the middle of a section can never reach the repo root. Those
are the two failures that would be invisible in the output: a missing chapter
looks like a shorter day, and a bad break looks like a normal one.
"""
import datetime
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', '..'))

HEADER = """# Bible reading plan, 24 August to 30 November 2026

99 days, the whole Bible, plus the Proverbs chapter that matches the date.
Two Old Testament days to one New Testament day, so no day is four times the
reading of the next. Every reading ends at a real section boundary, never
halfway through a narrative, a discourse or an argument.

About 32 to 67 minutes a day, most days near 45.

Three things that make it stick: write ONE sentence a day on what you saw;
listen to audio while reading on the heavy days; and know that Leviticus, days
13 to 16 (5 to 8 September), is where almost everyone quits. Defend that week.
"""


def line(r):
    return f"Study {r['ref']} and Proverbs {r['prov']}"


def expand(ref, _re=re):
    """'Genesis 1 to 9; Exodus 1' -> [(Genesis,1)...(Genesis,9),(Exodus,1)]."""
    out = []
    for part in ref.split('; '):
        m = _re.match(r'^(.+?) (\d+) to (\d+)$', part)
        if m:
            out += [(m.group(1), c)
                    for c in range(int(m.group(2)), int(m.group(3)) + 1)]
            continue
        m = _re.match(r'^(.+?) (\d+)$', part)
        out.append((m.group(1), int(m.group(2))) if m else (part, 1))
    return out


def verify(rows, OT, NT, start):
    brk = {n: set(b) for n, _, _, b in OT + NT}
    bad = []
    for kind, books in (('OT', OT), ('NT', NT)):
        got = [x for r in rows if r['kind'] == kind for x in expand(r['ref'])]
        want = [(n, c) for n, nc, _, _ in books for c in range(1, nc + 1)]
        if got != want:
            missing = set(want) - set(got)
            bad.append(f'{kind} is not complete and in order '
                       f'({len(got)} chapters, {len(missing)} missing)')
    for r in rows:
        bk, ch = expand(r['ref'])[-1]
        if ch not in brk.get(bk, ()):
            bad.append(f"{r['date']} stops mid-section, at {bk} {ch}")
    d = start
    for r in rows:
        if r['date'] != d.isoformat() or r['prov'] != d.day:
            bad.append(f"{r['date']}: date or Proverbs chapter is wrong")
        d += datetime.timedelta(days=1)
    if bad:
        for b in bad[:20]:
            print('  x ' + b, file=sys.stderr)
        raise SystemExit(f'verify: {len(bad)} problem(s); nothing written')
    print(f'verify: {len(rows)} days, both testaments complete and in order, '
          f'every day ends on a section boundary, Proverbs matches the date')


def emit(rows):
    md, cur = [HEADER], None
    for r in rows:
        d = datetime.date.fromisoformat(r['date'])
        m = d.strftime('%B %Y')
        if m != cur:
            md += ['', f'## {m}', '']
            cur = m
        md += [f"**{d.strftime('%a %d %b')}**", '```', line(r), '```', '']
    with open(os.path.join(ROOT, 'BIBLE_PLAN_AUG_NOV_2026.md'), 'w',
              encoding='utf-8') as fh:
        fh.write('\n'.join(md).strip() + '\n')
    with open(os.path.join(ROOT, 'BIBLE_PLAN_LINES.txt'), 'w',
              encoding='utf-8') as fh:
        fh.write('\n'.join(line(r) for r in rows) + '\n')
    print(f'wrote BIBLE_PLAN_AUG_NOV_2026.md and BIBLE_PLAN_LINES.txt '
          f'({len(rows)} days)')
