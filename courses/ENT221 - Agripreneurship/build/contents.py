"""The Contents page: section anchors, the table, and two-pass page numbering.

A page number cannot be known until the book has been rendered, and inserting
the Contents then moves every page after it. So assemble.py renders, reads each
section's page back out of the PDF, rebuilds the Contents from what it found,
and repeats until the numbers stop moving.

The page a section is on is read from the Contents links themselves: an id is
put on each heading, and the renderer resolves each link to a page. That is the
same answer a reader gets by clicking the row, which is the thing being checked,
and it adds nothing to the page. An earlier version instead planted invisible
marker text at each heading and searched for it. Do not go back to it. Any extra
box, however small, is laid out on its own, and a zero-height box at a page
boundary gets painted into the fragment on BOTH sides of the break: the section
is then found on the page before the one it starts on, the Contents numbers it
one page early, and every number is internally consistent while being wrong.

Two different numbers are in play, and confusing them yields a Contents whose
numbers all look right and whose links are all off by one:

  printed number   what the reader sees in the footer. Chromium numbers the
                   body render from 1, so this is the body-relative page.
  link target      the physical page of the merged file. The cover is merged in
                   front of the body, so it is one greater.
"""
import html as _html
import re

# (level, label, kick, title): level 0 = module divider, 1 = front matter, 2 = unit.
#
# The kick and title are quoted from the content HTML exactly. They are the only
# source of truth: the same pair generates both the anchor put on the heading and
# the anchor the Contents row links to, so the two cannot drift apart into a dead
# link. A row naming no heading, or a heading with no row, stops the build.
# CHECKPOINT SCOPE (front + Module One). The full book adds Modules Two to Five,
# the worked Past Paper 2025/2026, and Mock Examinations One to Three, on the plan
# in FULL_TOC_PLAN below. Every row here must match a heading in an assembled
# content file, so rows are added only as their content file is authored.
TOC = [
    (1, 'How to use this manual', 'Before you start', 'How to use this manual'),
    (1, 'The exam at a glance', 'Before you start', 'The Exam at a Glance'),
    (1, 'How the examiner thinks', 'Before you start', 'How the Examiner Thinks'),

    (0, 'Module One · Agriculture and Agripreneurship',
        'Module One', 'Agriculture and<br>Agripreneurship'),
    (2, 'Unit 1 · Understanding Agriculture and Agripreneurship', 'Module One &middot; Unit 1', 'Understanding Agriculture and Agripreneurship'),

    (0, 'Module Two · Fish Farming',
        'Module Two', 'Fish Farming'),
    (2, 'Unit 1 · Fish Farming, Investment and Water Quality', 'Module Two &middot; Unit 1', 'Fish Farming, Investment and Water Quality'),
    (2, 'Unit 2 · Behaviour, the 3M Model and Marketing', 'Module Two &middot; Unit 2', 'Behaviour, the 3M Model and Marketing'),

    (0, 'Module Three · Oil Palm',
        'Module Three', 'Oil Palm'),
    (2, 'Unit 1 · Oil Palm Cultivation', 'Module Three &middot; Unit 1', 'Oil Palm Cultivation'),
    (2, 'Unit 2 · Oil Palm Processing', 'Module Three &middot; Unit 2', 'Oil Palm Processing'),

    (0, 'Module Four · Agribusiness Opportunities and Value Addition',
        'Module Four', 'Agribusiness Opportunities<br>and Value Addition'),
    (2, 'Unit 1 · Identifying Agribusiness Opportunities', 'Module Four &middot; Unit 1', 'Identifying Agribusiness Opportunities'),
    (2, 'Unit 2 · Value Addition and Innovation', 'Module Four &middot; Unit 2', 'Value Addition and Innovation'),
    (2, 'Unit 3 · Production and Operations Management', 'Module Four &middot; Unit 3', 'Production and Operations Management'),

    (0, 'Reference · The Must-Memorise List and Glossary',
        'Reference', 'The Must-Memorise List<br>and Glossary'),
    (2, 'The Must-Memorise Consolidation', 'Reference', 'The Must-Memorise Consolidation'),
    (2, 'Glossary', 'Reference', 'Glossary'),

    (0, 'Solved Test One · Fully Worked (Answers Derived)',
        'Test One', 'Test One, Fully Worked'),
    (2, 'The twenty-nine questions, worked', 'Test One', 'The Twenty-Nine Questions, Worked'),

    (0, 'Solved Test Two · Fully Worked, With the Key',
        'Test Two', 'Test Two, Fully Worked'),
    (2, 'The thirty questions, worked with the confirmed key', 'Test Two', 'The Thirty Questions, Worked'),

    (0, 'Mock CBT One', 'Mock CBT One', 'Forty Questions,<br>Ten Per Module'),
    (2, 'Question Paper', 'Mock CBT One', 'Question Paper'),
    (2, 'Answers', 'Mock CBT One', 'Answers'),

    (0, 'Mock CBT Two', 'Mock CBT Two', 'Forty More,<br>Ten Per Module'),
    (2, 'Question Paper', 'Mock CBT Two', 'Question Paper'),
    (2, 'Answers', 'Mock CBT Two', 'Answers'),

    (0, 'Mock CBT Three', 'Mock CBT Three', 'Halfway House'),
    (2, 'Question Paper', 'Mock CBT Three', 'Question Paper'),
    (2, 'Answers', 'Mock CBT Three', 'Answers'),

    (0, 'Mock CBT Four', 'Mock CBT Four', 'Nearly There'),
    (2, 'Question Paper', 'Mock CBT Four', 'Question Paper'),
    (2, 'Answers', 'Mock CBT Four', 'Answers'),

    (0, 'Mock CBT Five', 'Mock CBT Five', 'The Last One'),
    (2, 'Question Paper', 'Mock CBT Five', 'Question Paper'),
    (2, 'Answers', 'Mock CBT Five', 'Answers'),
]

# The intended full structure, for reference as content is authored. Rows are added
# to TOC above only as their content file is authored (check_toc requires a heading
# for every row and a row for every heading), so this is the plan, not the state.
FULL_TOC_PLAN = """
  Before you start   How to use this manual, The Exam at a Glance, How the Examiner Thinks
  Module One   Agriculture and Agripreneurship: U1 Understanding Agriculture and Agripreneurship
  Module Two   Fish Farming: U1 Fundamentals, Investment and Water Quality; U2 Behaviour,
               the 3M Model and Marketing
  Module Three Oil Palm: U1 Cultivation; U2 Processing
  Module Four  Agribusiness Opportunities and Value Addition: U1 Identifying Opportunities,
               U2 Value Addition and Innovation, U3 Production and Operations Management
  Reference    The Must-Memorise Consolidation and the Glossary
  Worked Test One (29 Q) and Worked Test Two (30 Q, keyed), fully worked
  Mock CBT One / Two / Three (question paper + answers), all four modules equally weighted
"""

ANCHOR = 'sec-'

# Sections that begin on a fresh page whatever is above them. Every module
# divider does (.part in manual.css); these two ask for it in their own markup.
# The page before one of these is short by design, which is something the layout
# QA has to know or it reports the gap as a fault every time it runs.
FORCED_BREAK = {'BEFOREYOUSTARTHOWTOUSETHISMANUAL',
                'MOCKCBTONEANSWERS', 'MOCKCBTTWOANSWERS', 'MOCKCBTTHREEANSWERS',
                'MOCKCBTFOURANSWERS', 'MOCKCBTFIVEANSWERS'}


def forced_ids():
    """Anchor ids of every section that starts on a page of its own."""
    return FORCED_BREAK | {mkid(k, t) for lvl, _, k, t in TOC if lvl == 0}

UNIT_RE = re.compile(r'(<div class="kick">)(.*?)(</div>\s*<h2 class="title">)(.*?)(</h2>)', re.S)
PART_RE = re.compile(r'(<div class="kicker">)(.*?)(</div>\s*<h1>)(.*?)(</h1>)', re.S)


def strip_tags(t):
    return re.sub(r'<[^>]+>', ' ', t)


def plain(t):
    """The heading as the reader sees it: no markup, no entities, tidy spaces."""
    return ' '.join(_html.unescape(strip_tags(t)).split())


def heading_text(title):
    """The first rendered line of a title, for searching a page for it."""
    return plain(re.split(r'<br\s*/?>', title)[0])


def mkid(kick, title):
    """Anchor id for a heading: its kick and title, letters and digits only."""
    return re.sub(r'[^A-Za-z0-9]', '', plain(kick) + plain(title)).upper()


def inject_anchors(html_text):
    """Put a link anchor on every section heading in the book.

    The anchor goes on the heading element that is already there. Nothing is
    added to the page: see the note at the top of this file for why anything
    added, however small, gets the page number wrong at a break.

    Returns the marked-up HTML and the (id, kick, title) of everything found.
    """
    found = []

    def sub(m):
        mid = mkid(m.group(2), m.group(4))
        found.append((mid, m.group(2), m.group(4)))
        opener = m.group(1)[:-1] + f' id="{ANCHOR}{mid}">'
        return opener + m.group(2) + m.group(3) + m.group(4) + m.group(5)

    out = UNIT_RE.sub(sub, html_text)
    out = PART_RE.sub(sub, out)
    return out, found


def check_toc(found):
    """The Contents and the book must name exactly the same set of headings.

    A row with no heading is a dead link; a heading with no row is a section the
    reader cannot find. Both are silent, so both stop the build.
    """
    want = {mkid(k, t): lbl for _, lbl, k, t in TOC}
    ids = [mid for mid, _, _ in found]
    problems = []

    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f'two headings share the anchor {dup}; the second is unreachable')
    for mid, lbl in want.items():
        if mid not in ids:
            problems.append(f'Contents row "{lbl}" matches no heading in the book')
    for mid, kick, title in found:
        if mid not in want:
            problems.append(f'heading "{plain(kick)} / {plain(title)}" has no Contents row')
    return problems


def link_pages(pdf_path):
    """Body-relative page (1-based) of each section, per the renderer.

    Read from the Contents links, keyed by the anchor each one names, so a row
    is matched to its section by name and never by position on the page.
    """
    import fitz
    doc = fitz.open(pdf_path)
    pages = {}
    for i in range(doc.page_count):
        for lk in doc[i].get_links():
            name = lk.get('nameddest') or ''
            if name.startswith(ANCHOR) and lk.get('page', -1) >= 0:
                pages[name[len(ANCHOR):]] = lk['page'] + 1
    doc.close()
    return pages


def build_contents(pages=None):
    """The Contents page.

    On the first pass no page is known yet, so the numbers are left blank and
    only the links are real. Rendering that is what reveals the numbers.
    """
    if pages is not None:
        missing = [lbl for _, lbl, k, t in TOC if mkid(k, t) not in pages]
        if missing:
            raise SystemExit('BUILD STOPPED: the renderer resolved no page for these '
                             'sections, so their Contents row would be a dead link:\n  '
                             + '\n  '.join(missing))

    rows = ['<div class="toc-head">Contents</div>',
            '<p class="toc-note">Every line is a link. The page numbers are read back '
            'from the rendered book, never typed by hand.</p>']
    for lvl, label, kick, title in TOC:
        mid = mkid(kick, title)
        cls = {0: 'toc-part', 1: 'toc-l1', 2: 'toc-l2'}[lvl]
        pg = pages[mid] if pages is not None else ''
        rows.append(f'<a class="{cls} toc-link" href="#{ANCHOR}{mid}">'
                    f'<span class="toc-label">{label}</span>'
                    f'<span class="toc-dots"></span>'
                    f'<span class="toc-pg">{pg}</span></a>')
    return '<div class="contents-page">\n' + '\n'.join(rows) + '\n</div>\n'
