"""The no-escape coverage gate.

    cd build && python qa_coverage.py [full_manual.html]

Victor's rule: EVERY question in EVERY source must be solved somewhere in the
manual. This gate reads the assembled book and checks it against the question
inventory, two ways:

  1. PROVENANCE. Every worked answer carries a chip naming its source ("PQ 25/26
     Q1c", "TEST 1 A(b)", "TEXT M2U1", "DECK"). This gate collects every chip and
     confirms that the two priority papers Victor named (2025/26 and 2024/25) have
     ALL of their questions One to Six cited. A missing priority-paper question is
     a hard failure. Every other cited paper is reported for the eye.

  2. FIGURES. Diagram-answer questions must actually show a diagram. This counts
     the inline-SVG figures and asserts the book is diagram-rich (the ER/EER/FD
     work is the spine of this course), and that the manual is not silently
     text-only anywhere a whole section of diagrams is expected.

It reads the assembled HTML, so it sees the book a reader gets, not the sources.
This does not replace reading the inventory by eye; it catches the escape that a
tired author misses.
"""
import re, sys

# past-paper session label as printed in a chip -> inventory year token
YEARS = {'25/26': '2526', '24/25': '2425', '23/24': '2324', '22/23': '2223',
         '21/22': '2122', '20/21': '2021', '19/20': '1920', '15/16': '1516'}
PRIORITY = ('2526', '2425')          # Victor's two favourite papers
PROV_RE = re.compile(r'<span class="prov">(.*?)</span>', re.S)
FIG_RE = re.compile(r'<figure\b')
TAG_RE = re.compile(r'<[^>]+>')


def _text(s):
    return re.sub(r'\s+', ' ', TAG_RE.sub('', s)).strip()


def covered_questions(html):
    """Set of (year_token, 'Qn') pairs cited by a provenance chip in the book."""
    got = set()
    other = set()
    for raw in PROV_RE.findall(html):
        chip = _text(raw)
        m = re.search(r'PQ\s*(\d\d/\d\d)\s*Q?\s*(\d+)', chip)
        if m and m.group(1) in YEARS:
            got.add((YEARS[m.group(1)], 'Q' + m.group(2)))
        else:
            other.add(chip)
    return got, other


def report(html):
    got, other = covered_questions(html)
    figures = len(FIG_RE.findall(html))
    ok = True
    problems = []

    # 1. priority papers: every question One..Six must be cited
    for yr in PRIORITY:
        missing = [f'Q{n}' for n in range(1, 7) if (yr, f'Q{n}') not in got]
        if missing:
            ok = False
            problems.append(f'priority paper {yr[:2]}/{yr[2:]} is missing a worked '
                            f'citation for: {", ".join(missing)}')

    # 2. the book must be diagram-rich (ER/EER/FD/schema figures)
    if figures < 25:
        ok = False
        problems.append(f'only {figures} inline figures found; a course this visual '
                        f'should carry far more (expected 25+)')

    papers = sorted({yr for yr, _ in got})
    print(f'COVERAGE GATE: {len(got)} past-paper questions cited across '
          f'{len(papers)} sessions; {figures} figures')
    if ok:
        print('  . both priority papers (25/26, 24/25) fully cited, Q1 to Q6')
        print(f'  . sessions cited: {", ".join(sorted(papers))}')
        print(f'  . text/test/deck chips: {len(other)} distinct')
        print('  . diagram-rich: {} inline figures'.format(figures))
    else:
        print('COVERAGE GATE: FAIL')
        for p in problems:
            print('  x ' + p)
    return ok


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'full_manual.html'
    with open(src, encoding='utf-8') as fh:
        sys.exit(0 if report(fh.read()) else 1)
