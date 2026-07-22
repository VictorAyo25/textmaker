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
TOC = [
    (1, 'How to use this manual', 'Before you start', 'How to use this manual'),
    (0, 'Foundations · The Language of Discrete Maths', 'Foundations', 'The Language of<br>Discrete Maths'),
    (2, 'F.1 · Numbers, Symbols and Notation', 'Foundations &middot; F.1', 'Numbers, Symbols and Notation'),
    (2, 'F.2 · Reading and Writing Mathematics', 'Foundations &middot; F.2', 'Reading and Writing Mathematics'),
    (0, 'Part One · Logic', 'Part One', 'Logic: The Grammar<br>of Reasoning'),
    (2, '1.1 · Propositions and Truth Tables', 'Part One &middot; 1.1', 'Propositions and Truth Tables'),
    (2, '1.2 · Implication, Converse, Inverse, Contrapositive', 'Part One &middot; 1.2', 'Implication, Converse, Inverse, Contrapositive'),
    (2, '1.3 · Logical Equivalence and the Laws', 'Part One &middot; 1.3', 'Logical Equivalence and the Laws'),
    (2, '1.4 · Predicate Logic and Quantifiers', 'Part One &middot; 1.4', 'Predicate Logic and Quantifiers'),
    (2, '1.5 · Rules of Inference and Valid Arguments', 'Part One &middot; 1.5', 'Rules of Inference and Valid Arguments'),
    (0, 'Part Two · Sets', 'Part Two', 'Sets and Their<br>Operations'),
    (2, '2.1 · Sets, Membership and the Nine Types', 'Part Two &middot; 2.1', 'Sets, Membership and the Nine Types'),
    (2, '2.2 · Set Operations and Venn Diagrams', 'Part Two &middot; 2.2', 'Set Operations and Venn Diagrams'),
    (2, '2.3 · Bit Strings, Power Sets and Cartesian Products', 'Part Two &middot; 2.3', 'Bit Strings, Power Sets and Cartesian Products'),
    (0, 'Part Three · Relations', 'Part Three', 'Relations, Matrices<br>and Ordered Sets'),
    (2, '3.1 · Relations and Their Representations', 'Part Three &middot; 3.1', 'Relations and Their Representations'),
    (2, '3.2 · The Five Properties of a Relation', 'Part Three &middot; 3.2', 'The Five Properties of a Relation'),
    (2, '3.3 · Equivalence Relations and Partitions', 'Part Three &middot; 3.3', 'Equivalence Relations and Partitions'),
    (2, '3.4 · Partial and Total Orders', 'Part Three &middot; 3.4', 'Partial and Total Orders'),
    (0, 'Part Four · Functions', 'Part Four', 'Functions and<br>Correspondence'),
    (2, '4.1 · Functions, Domain and Range', 'Part Four &middot; 4.1', 'Functions, Domain and Range'),
    (2, '4.2 · The Five Correspondence Types', 'Part Four &middot; 4.2', 'The Five Correspondence Types'),
    (2, '4.3 · Composition and Inverse Functions', 'Part Four &middot; 4.3', 'Composition and Inverse Functions'),
    (0, 'Part Five · Counting', 'Part Five', 'Counting, Permutations<br>and Combinations'),
    (2, '5.1 · The Product and Sum Rules', 'Part Five &middot; 5.1', 'The Product and Sum Rules'),
    (2, '5.2 · Permutations and Combinations', 'Part Five &middot; 5.2', 'Permutations and Combinations'),
    (2, '5.3 · Inclusion, Exclusion and the Pigeonhole Principle', 'Part Five &middot; 5.3', 'Inclusion, Exclusion and the Pigeonhole Principle'),
    (2, '5.4 · The Binomial Theorem', 'Part Five &middot; 5.4', 'The Binomial Theorem'),
    (0, 'Part Six · Graph Theory', 'Part Six', 'Graph Theory:<br>Vertices and Edges'),
    (2, '6.1 · Graphs, Vertices, Edges and Degree', 'Part Six &middot; 6.1', 'Graphs, Vertices, Edges and Degree'),
    (2, '6.2 · The Types of Undirected Graph', 'Part Six &middot; 6.2', 'The Types of Undirected Graph'),
    (2, '6.3 · The Handshaking Theorem', 'Part Six &middot; 6.3', 'The Handshaking Theorem'),
    (2, '6.4 · Directed Graphs, In-degree and Out-degree', 'Part Six &middot; 6.4', 'Directed Graphs, In-degree and Out-degree'),
    (2, '6.5 · Adjacency, Path and Relation Matrices', 'Part Six &middot; 6.5', 'Adjacency, Path and Relation Matrices'),
    (2, '6.6 · Isomorphism, Euler and Hamilton', 'Part Six &middot; 6.6', 'Isomorphism, Euler and Hamilton'),
    (2, '6.7 · Planarity, Euler’s Formula and Kuratowski', 'Part Six &middot; 6.7', 'Planarity, Euler’s Formula and Kuratowski'),
    (2, '6.8 · Shortest Routes and the Travelling Salesman', 'Part Six &middot; 6.8', 'Shortest Routes and the Travelling Salesman'),
    (0, 'Part Seven · Trees', 'Part Seven', 'Trees and Their<br>Traversals'),
    (2, '7.1 · Trees and Rooted-Tree Terminology', 'Part Seven &middot; 7.1', 'Trees and Rooted-Tree Terminology'),
    (2, '7.2 · m-ary and Balanced Trees', 'Part Seven &middot; 7.2', 'm-ary and Balanced Trees'),
    (2, '7.3 · Traversals and Expression Trees', 'Part Seven &middot; 7.3', 'Traversals and Expression Trees'),
    (0, 'Part Eight · Boolean Algebra', 'Part Eight', 'Boolean Algebra<br>and Logic Circuits'),
    (2, '8.1 · Boolean Algebra and Its Laws', 'Part Eight &middot; 8.1', 'Boolean Algebra and Its Laws'),
    (0, 'Part Nine · Proof and Recursion', 'Part Nine', 'Proof, Induction<br>and Recursion'),
    (2, '9.1 · Proof Techniques', 'Part Nine &middot; 9.1', 'Proof Techniques'),
    (2, '9.2 · Mathematical Induction', 'Part Nine &middot; 9.2', 'Mathematical Induction'),
    (2, '9.3 · Sequences, Series and Progressions', 'Part Nine &middot; 9.3', 'Sequences, Series and Progressions'),
    (2, '9.4 · Recurrence Relations', 'Part Nine &middot; 9.4', 'Recurrence Relations'),
    (0, 'Part Ten · Statistics and Probability', 'Part Ten', 'Descriptive Statistics<br>and Discrete Probability'),
    (2, '10.1 · Descriptive Statistics', 'Part Ten &middot; 10.1', 'Descriptive Statistics'),
    (2, '10.2 · Discrete Probability', 'Part Ten &middot; 10.2', 'Discrete Probability'),
    (0, 'Part Eleven · C++ for Discrete Structures', 'Part Eleven', 'C++ for Discrete<br>Structures'),
    (2, '11.1 · Enough C++ to Answer the Question', 'Part Eleven &middot; 11.1', 'Enough C++ to Answer the Question'),
    (2, '11.2 · The Four Examined Programs', 'Part Eleven &middot; 11.2', 'The Four Examined Programs'),
    (0, 'Reference · Formulas, Notation and Exam Craft', 'Reference', 'Formulas, Notation<br>and Exam Craft'),
    (2, 'R.1 · Formula and Notation Reference', 'Reference &middot; R.1', 'Formula and Notation Reference'),
    (2, 'R.2 · Exam Day Strategy', 'Reference &middot; R.2', 'Exam Day Strategy'),
    (2, 'R.3 · Trap Index and Cram Sheet', 'Reference &middot; R.3', 'Trap Index and Cram Sheet'),
    (0, 'Past Papers · All Five, Solved in Full', 'Past Papers', 'All Five Papers,<br>Solved in Full'),
    (2, '2025/2026 Solved in Full', 'Past Paper', '2025/2026 Solved in Full'),
    (2, '2024/2025 Solved in Full', 'Past Paper', '2024/2025 Solved in Full'),
    (2, '2023/2024 Solved in Full', 'Past Paper', '2023/2024 Solved in Full'),
    (2, '2021/2022 Solved in Full', 'Past Paper', '2021/2022 Solved in Full'),
    (2, '2020/2021 Solved in Full', 'Past Paper', '2020/2021 Solved in Full'),
    (0, 'Mock Examination One', 'Mock Examination One', 'Sit This Paper<br>Under Exam Conditions'),
    (2, 'Question Paper', 'Mock Examination One', 'Question Paper'),
    (2, 'Answers', 'Mock Examination One', 'Answers'),
    (0, 'Mock Examination Two', 'Mock Examination Two', 'Sit This One<br>After the First'),
    (2, 'Question Paper', 'Mock Examination Two', 'Question Paper'),
    (2, 'Answers', 'Mock Examination Two', 'Answers'),
    (0, 'Mock Examination Three', 'Mock Examination Three', 'The Hardest of<br>the Three'),
    (2, 'Question Paper', 'Mock Examination Three', 'Question Paper'),
    (2, 'Answers', 'Mock Examination Three', 'Answers'),
]


ANCHOR = 'sec-'

# Sections that begin on a fresh page whatever is above them. Every module
# divider does (.part in manual.css). The page before one of these is short by
# design, which the layout QA has to know or it reports the gap as a fault.
FORCED_BREAK = {'MOCKEXAMINATIONONEANSWERS', 'MOCKEXAMINATIONTWOANSWERS',
                'MOCKEXAMINATIONTHREEANSWERS'}


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
