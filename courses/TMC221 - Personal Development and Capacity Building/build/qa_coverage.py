"""No-slide-left-behind coverage gate.

    cd build && python qa_coverage.py [full_manual.html]

Victor's standing instruction for this course: "ensure no single idea, concept,
acronym, data etc is left out from the decks; cover every single thing; test every
single area, using any style except theory, of every slide."

The forcing function that keeps that honest is a provenance chip. Every drill and
every teaching box that draws on a slide carries a chip naming the slide, e.g.
`<span class="prov">L1 S4</span>` (Lecture 1, Slide 4). This gate collects every
chip in the assembled book and proves that EVERY content-bearing slide of all five
decks is cited at least once (Lecture Five was added by the lecturer after the first
edition shipped, and it entered the manual through this same gate). A slide with no chip is a slide whose ideas never made
it into the manual, which is exactly the escape the instruction forbids.

Pure title and "Thank You" slides carry no testable content and are excluded by the
REQUIRED map below. Everything else, including the class exercises, must be covered.

Control test: delete a chip (say L2 S8, the SWITCH protocol) and the gate must fail
naming that slide. Proven before trusting it.
"""
import re
import sys

# Content slides that MUST be cited (title slides and closing "Thank You" slides
# excluded). Ranges are inclusive.
REQUIRED = {
    'L1': list(range(2, 21)),   # S2..S20 (S1 title)
    'L2': list(range(2, 20)),   # S2..S19 (S1 title, S20/S21 thanks)
    'L3': list(range(2, 16)),   # S2..S15 (S1 title, S16 thanks)
    'L4': list(range(2, 20)),   # S2..S19 (S1 title, S20 thanks)
    'L5': list(range(2, 20)),   # S2..S19 (S1 title, S20 thanks)
}

# A chip names one lecture then one or more slides, e.g. "L1 S13, S14" or "L4 S3".
GROUP = re.compile(r'L([1-5])((?:\s*S\d{1,2}\s*,?)+)')
SLIDE = re.compile(r'S(\d{1,2})')


def report(html):
    covered = set()
    for m in GROUP.finditer(html):
        lec = f'L{m.group(1)}'
        for s in SLIDE.findall(m.group(2)):
            covered.add((lec, int(s)))
    missing = []
    total = 0
    for lec, slides in REQUIRED.items():
        for s in slides:
            total += 1
            if (lec, s) not in covered:
                missing.append(f'{lec} S{s}')
    print(f'SLIDE-COVERAGE GATE: {total} content slides required across 5 decks')
    if missing:
        print(f'  x {len(missing)} slide(s) never cited by any provenance chip:')
        print('      ' + ', '.join(missing))
        return False
    extra = sorted(covered - {(l, s) for l, ss in REQUIRED.items() for s in ss})
    print(f'  . every content slide of all five decks is cited at least once')
    if extra:
        print(f'  . ({len(extra)} chips also cite title/closing slides, which is fine)')
    return True


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'full_manual.html'
    sys.exit(0 if report(open(src, encoding='utf-8').read()) else 1)
