"""Coverage gate (ENT221): no module, unit, or key exam list left out.

    cd build && python qa_coverage.py [full_manual.html]

The methodology's coverage gate is a forcing function: enumerate what the source teaches
and prove the book carries every piece, so nothing is quietly dropped. ENT221's source is
a text, not slides, so this declares two things and checks both against the assembled book:

  1. STRUCTURE: every unit of the course text must appear as a taught section, both real
     tests must be solved, and all three mocks plus the reference must be present.
  2. KEY LISTS: the enumerated lists a CBT feeds on (the 3M model, the five fish-farm
     departments, the three water parameters, the five processing stages, the six
     value-addition types, POCD, and the rest) must each be present. A distinctive phrase
     stands in for each list; if the list is dropped, its phrase vanishes and this fails.

Control test: delete any REQUIRED phrase from its content file and the gate must name it.
Also checks the book stays diagram-rich (figures do not silently drop to text).
"""
import re
import sys

# Course-text units: each must appear as a taught section title.
REQUIRED_UNITS = [
    'Understanding Agriculture and Agripreneurship',
    'Fish Farming, Investment and Water Quality',
    'Behaviour, the 3M Model and Marketing',
    'Oil Palm Cultivation',
    'Oil Palm Processing',
    'Identifying Agribusiness Opportunities',
    'Value Addition and Innovation',
    'Production and Operations Management',
]

# Practice/solved structure the book promises.
REQUIRED_STRUCTURE = {
    'Solved Test One': 'Test One, Fully Worked',
    'Solved Test Two': 'Test Two, Fully Worked',
    'Mock CBT One': 'Forty Questions',
    'Mock CBT Two': 'Forty More',
    'Mock CBT Three': 'Halfway House',
    'Mock CBT Four': 'Nearly There',
    'Mock CBT Five': 'The Last One',
    'Must-Memorise consolidation': 'The Must-Memorise Consolidation',
    'Glossary': 'Glossary',
}

# Key exam lists: a distinctive phrase present iff the list is taught.
REQUIRED_LISTS = {
    'agriculture definition': 'science, art, and practice',
    'value chain definition': 'series of activities and transactions',
    'fish-farm departments': 'Feed mill',
    'three water parameters': 'physical, chemical, and biological',
    'pH range': '6.5 to 8.5',
    'dissolved oxygen range': '5 to 8 mg/L',
    'fish behaviour patterns': 'Slow movement',
    '3M model': 'Make, Manage',
    'ten MAKE principles': 'Fisheries knowledge and manpower',
    '7Ps of marketing': 'physical evidence',
    '4Cs of marketing': 'customer, cost, convenience',
    'SWOT and SMART': 'SWOT',
    'oil palm variety cross': 'Dura',
    'oil palm dormancy': '70 to 80 days',
    'oil palm spacing': '143 palms',
    'oil palm fruit types': 'Nigrescens',
    'five processing stages': 'Clarification',
    'palm by-products (POME)': 'palm oil mill effluent',
    'value-addition types': 'form, place, time',
    'value-addition forms': 'Primary',
    'POCD framework': 'Planning, Organising',
    'agribusiness criteria': 'Scalability',
}

FIG_MIN = 6   # inline SVG <figure> diagrams currently in the book; must not silently drop


def report(html):
    missing = []
    for u in REQUIRED_UNITS:
        if u not in html:
            missing.append(f'course-text unit not taught: "{u}"')
    for name, cue in REQUIRED_STRUCTURE.items():
        if cue not in html:
            missing.append(f'missing section: {name} (cue "{cue}")')
    for name, cue in REQUIRED_LISTS.items():
        if cue not in html:
            missing.append(f'key exam list dropped: {name} (cue "{cue}")')

    figs = len(re.findall(r'<figure\b', html))
    total = len(REQUIRED_UNITS) + len(REQUIRED_STRUCTURE) + len(REQUIRED_LISTS)
    print(f'COVERAGE GATE: {total} required items + at least {FIG_MIN} figures checked')
    if figs < FIG_MIN:
        missing.append(f'only {figs} figures, below the {FIG_MIN} this diagram-rich book needs')
    if missing:
        print('COVERAGE GATE: FAIL')
        for m in missing:
            print('  x ' + m)
        return False
    print(f'  . every course-text unit is taught ({len(REQUIRED_UNITS)} units)')
    print('  . every solved test, mock, and reference section is present')
    print(f'  . every key exam list is present ({len(REQUIRED_LISTS)} lists)')
    print(f'  . {figs} figures, at or above the {FIG_MIN} minimum')
    return True


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'full_manual.html'
    sys.exit(0 if report(open(src, encoding='utf-8').read()) else 1)
