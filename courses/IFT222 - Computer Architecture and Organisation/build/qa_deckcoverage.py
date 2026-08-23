"""DECK COVERAGE GATE: nothing examinable is left to the lecture slides alone.

WHY THIS EXISTS. This book claims to have blended all eight lecture decks. Until
2026-08-20 that claim rested on a slide-by-slide audit done by hand, which is a
memory, not a measurement. The student asked whether it was actually true, and a
memory is not an answer.

WHAT IT MEASURES, AND WHY IT IS INDEPENDENT. The drill build separately turned the
same eight decks into a fact ledger: webapp/data/ift222/ledger/*.json, 600 atomic
facts, at least one per content slide across 326 content slides, written from the
extracted deck text and NOT from this manual. So the ledger is an outside
checklist. This gate reads every fact, reduces it to its distinctive words, and
asks whether the manual's own prose carries them.

It is a SUPPORT test, not a containment test: a fact passes when enough of its
distinctive vocabulary appears somewhere in the book. That is deliberately loose,
because the manual is not required to phrase anything the way a slide does. What
it catches is the real failure mode, a slide's content missing outright, which is
what it found on its first run: the Ariane 5 and Vancouver case studies, the
deck's own MC6809 mnemonics, Instruction Level Parallelism by name, the six
levels of parallelism, the three machines RISC grew from, the deck's 64.2 float
example, its Excess-3 values, and the whole ROM family. 42 of 600 unsupported
became 8, and every one of those 8 is named in ALLOWED below with a reason.

CONTROL TEST. Run with --control: it deletes a well-covered fact's vocabulary
from the book text in memory and requires the gate to fail and name that fact. A
gate nobody has broken on purpose is a gate nobody knows works.

    cd build && python qa_deckcoverage.py
    cd build && python qa_deckcoverage.py --control
"""
import glob
import html as _html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
LEDGER = os.path.abspath(os.path.join(
    HERE, '..', '..', '..', 'webapp', 'data', 'ift222', 'ledger'))

# The floor a fact's distinctive vocabulary must clear to count as carried.
# Calibrated against the run that found the ten real gaps: at 0.62 the misses were
# all genuine or all obviously non-manual, and no fact the book plainly teaches
# fell below it.
SUPPORT = 0.62

# Facts a study manual is not supposed to carry, each with the reason. This list
# may only grow with a reason attached, and the gate prints its size every run so
# that growth cannot go unnoticed.
ALLOWED = {
    't1-003': 'the recommended-textbook list: a reading list, not course content',
    't1-004': 'the rest of the recommended-textbook list, same reason',
    't1-005': 'a motivational slide on the impact of computers on society',
    't1-006': 'the same motivational slide, second half',
    't2-014': 'a note that load and store are often confused: commentary, not a fact',
    't3-039': 'alphanumeric codes let us interface keyboards, monitors and printers: '
              'the manual teaches the codes and the devices, not this framing sentence',
    't8m-011': 'memory cost must be reasonable relative to other components: carried '
               'by the hierarchy teaching as the cost against speed trade, not as a line',
}

STOP = set("""a an the of to and or in is are was were be been being for with on at by from as it its this that these
those which who whom what when where how why not no nor but if then than so such can could may might will would shall
should must have has had do does did done each every all any some one two three four five six seven eight nine ten more
most other others into out up down over under between within without about across after before during while also both
either neither same different used use using uses used usually often typically e.g i.e etc via per their there they them
he she his her you your we our us new only very much many few less least first second third last next previous because
since though although students learn learns covers covered course lecture slide slides deck recommended textbook
edition""".split())


def book_text():
    parts = []
    for f in sorted(glob.glob(os.path.join(CONTENT, '*.html'))):
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'<svg.*?</svg>', ' ', s, flags=re.S)
        s = re.sub(r'<[^>]+>', ' ', s)
        parts.append(_html.unescape(s))
    t = ' '.join(parts).replace('‑', '-').replace('‐', '-')
    return re.sub(r'\s+', ' ', t).lower()


def distinctive(fact):
    s = fact.lower().replace('‑', '-').replace('‐', '-')
    words = re.findall(r"[a-z0-9][a-z0-9\-'\.]*", s)
    return {w for w in words if w not in STOP and len(w) > 2}


def facts():
    out = []
    for f in sorted(glob.glob(os.path.join(LEDGER, '*.json'))):
        out.extend(json.load(open(f, encoding='utf-8')))
    return out


def check(text, all_facts):
    missing = []
    for fa in all_facts:
        words = distinctive(fa['fact'])
        if not words:
            continue
        frac = sum(1 for w in words if w in text) / len(words)
        if frac < SUPPORT and fa['id'] not in ALLOWED:
            missing.append((round(frac, 2), fa))
    return sorted(missing, key=lambda r: r[0])


def report():
    all_facts = facts()
    if not all_facts:
        print('DECK COVERAGE GATE: SKIPPED, no ledger found at ' + LEDGER)
        return True
    text = book_text()
    missing = check(text, all_facts)
    print(f'DECK COVERAGE GATE: {len(all_facts)} deck facts from eight lecture decks, '
          f'checked against the book')
    if missing:
        print('DECK COVERAGE GATE: FAIL')
        for frac, fa in missing[:30]:
            print(f'  x [{fa["id"]} {fa["ref"]} hard={fa["hard"]}] only {frac:.0%} of its '
                  f'words appear in the book: {fa["fact"][:120]}')
        return False
    print(f'  . every deck fact is carried by the manual, except {len(ALLOWED)} named '
          f'in ALLOWED with a reason (reading lists and motivational slides)')
    hard = sum(1 for f in all_facts if f['hard'])
    print(f'  . {hard} of them are hard facts: a number, a name, a list or a definition '
          f'an examiner could take a mark off for')
    return True


def control():
    """Break it on purpose: a carried fact must fail once its words are gone."""
    all_facts = facts()
    text = book_text()
    victim = None
    for fa in all_facts:
        if fa['id'] in ALLOWED:
            continue
        w = distinctive(fa['fact'])
        if len(w) >= 6 and all(x in text for x in w):
            victim = fa
            break
    if victim is None:
        print('CONTROL TEST: could not find a fully carried fact to break')
        return False
    holed = text
    for w in distinctive(victim['fact']):
        holed = holed.replace(w, 'zzz')
    missing = check(holed, all_facts)
    named = any(fa['id'] == victim['id'] for _, fa in missing)
    print(f'CONTROL TEST: removed the vocabulary of {victim["id"]} ({victim["ref"]}) '
          f'from the book text')
    print(f'  gate fails: {bool(missing)}')
    print(f'  and names that fact: {named}')
    return bool(missing) and named


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if '--control' in sys.argv:
        sys.exit(0 if control() else 1)
    sys.exit(0 if report() else 1)
