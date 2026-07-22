"""Every load-bearing notation the manual uses, and where it is first taught.

    cd build && python assemble.py --no-pdf   # writes full_manual.html
    python qa_firstuse.py                     # then audit it

The promise this checks is Victor's: **zero external sources**. A reader must
never need a lecturer, a website, or the official course text. Asserting that is
easy and worthless; it only means something measured, and it is exactly the kind
of claim that silently rots as a book grows past a hundred pages.

Discrete maths is a NOTATION course. Its vocabulary is not acronyms but symbols:
the reader meets an element sign, a subset sign, a quantifier, a biconditional
arrow, and each is meaningless until it has been named in prose. That is the
declared-notation form of the gate (MANUAL_METHODOLOGY 4b): the author lists the
notation the manual leans on, each with the regex that marks its INTRODUCTION,
and the gate proves each is introduced at all, and introduced outside a mock.
Enumerating the list is the forcing function.

Three rules, none of which survives being asserted rather than measured against
the assembled book in reading order:

  1. **Nothing is used before it is taught.** A symbol whose first appearance
     precedes the first place its meaning is written out is a hole: the reader
     meets the mark with nothing to unpack it.
  2. **Nothing load-bearing goes untaught.** A symbol used in the book whose
     meaning is written out nowhere leaves the reader no way to look it up.
  3. **A mock teaches nothing.** A mock tests what the parts taught, so a
     notation whose first appearance in the whole book is inside a mock is one
     the reader is examined on and was never shown.

This course carries a fourth hazard the others did not. Its official text does
not cover graphs, trees, relation properties, posets or Boolean algebra at all,
so every one of those terms MUST be introduced by this manual: there is no
fallback source for a reader who finds a gap. The GAP_TERMS list below is
checked with the same three rules and cannot be waived.

A curated list can rot, so a mechanical rot-guard (discover_terms) sweeps the
book for anything typeset as a defined abbreviation, `Expansion (ABBR)` or
`ABBR (expansion)`, and fails if the book defines a term the glossary has never
heard of. The list cannot fall behind the book in silence.

This reads the ASSEMBLED html, not content/*.html, so it sees the book in the
order a reader does. Run assemble.py first. SVG diagrams are dropped (their text
labels ride on coordinate noise); `<pre>` and `<table>` are kept, because a
truth table is exactly where a reader first meets a connective.
"""
import html as _h
import os
import re
import sys


def emit(line):
    """Print safely on a cp1252 console.

    This course's notation IS the thing being audited, so every failure message
    contains characters the Windows console cannot encode. A gate that crashes
    while reporting a real failure is worse than no gate.
    """
    enc = getattr(sys.stdout, 'encoding', None) or 'ascii'
    print(line.encode(enc, 'replace').decode(enc))

ANCHOR_RE = re.compile(r'id="sec-([A-Z0-9]+)"')
SVG_RE = re.compile(r'<svg.*?</svg>', re.S | re.I)
DROP_RE = re.compile(r'<(style|script)\b.*?</\1>', re.S | re.I)
TAG_RE = re.compile(r'<[^>]+>')

# ---------------------------------------------------------------------------
# The notation a reader of THIS book is owed.
#
# Each entry maps a mark, as the assembled text actually renders it (the
# entities are already unescaped by clean(), so these are real characters), to
# the pattern that marks the place the manual NAMES it. The intro cue must key
# on a real definition, never on an objectives-list mention, or the promise
# reads as the teaching (the DTS224 lesson, MANUAL_METHODOLOGY 4b).
# ---------------------------------------------------------------------------
SYMBOLS = {
    '∈': r'\bis an element of\b|\bbelongs to\b|read .{0,12}is (?:an )?element',
    '∉': r'\bis not an element of\b|\bdoes not belong\b',
    '⊆': r'\bis a subset of\b',
    '⊂': r'\bproper subset\b',
    '∪': r'\bunion\b',
    '∩': r'\bintersection\b',
    '∅': r'\bempty set\b|\bnull set\b',
    'ℕ': r'\bnatural numbers\b',
    'ℤ': r'\bthe integers\b|\bset of integers\b',
    'ℝ': r'\breal numbers\b',
    '∀': r'\buniversal quantifier\b|\bfor all\b',
    '∃': r'\bexistential quantifier\b|\bthere exists\b',
    '∧': r'\bconjunction\b|\band\b.{0,24}\bboth\b',
    '∨': r'\bdisjunction\b',
    '¬': r'\bnegation\b',
    '→': r'\bimplication\b|\bconditional\b',
    '↔': r'\bbiconditional\b',
    '≡': r'\blogically equivalent\b',
    '△': r'\bsymmetric difference\b',
    '∑': r'\bsummation\b|\bsigma notation\b',
}

# Abbreviations and named terms. Same three rules, same forcing function.
TERMS = {
    # The multiplication sign is assumed knowledge and is used from Foundations
    # onward for ordinary arithmetic, so the thing worth auditing is the PHRASE
    # "Cartesian product", not the glyph it shares with multiplication.
    'Cartesian product': r'\bCartesian product\b.{0,140}\bordered pair',
    'nCr': r'\bcombination\b',
    'nPr': r'\bpermutation\b',
    'gcd': r'\bgreatest common divisor\b',
    'lcm': r'\blowest common multiple\b|\bleast common multiple\b',
}

# ---------------------------------------------------------------------------
# The gap terms. The official course text teaches NONE of these, so this manual
# is the reader's only source and every one must be defined here. This list is
# not waivable: see the module docstring.
# ---------------------------------------------------------------------------
GAP_TERMS = {
    'vertex':        r'\bvertex\b.{0,80}\b(?:point|node|dot|object)\b|\bvertices\b.{0,60}\bare the\b',
    'edge':          r'\bedge\b.{0,80}\b(?:joins|connects|link)\b',
    'degree':        r'\bdegree of a vertex\b',
    'valency':       r'\bvalency\b',
    'pendant':       r'\bpendant vertex\b',
    'in-degree':     r'\bin-degree\b.{0,80}\b(?:number|arrow|edges)\b',
    'out-degree':    r'\bout-degree\b.{0,80}\b(?:number|arrow|edges)\b',
    'adjacency':     r'\badjacency matrix\b.{0,120}\b(?:row|column|entry|1|one)\b',
    'reflexive':     r'\breflexive\b.{0,120}\b(?:every|each|all)\b',
    'symmetric':     r'\bsymmetric\b.{0,140}\bwhenever\b',
    'antisymmetric': r'\bantisymmetric\b',
    'transitive':    r'\btransitive\b.{0,140}\bwhenever\b',
    'equivalence':   r'\bequivalence relation\b.{0,160}\b(?:reflexive|three)\b',
    'poset':         r'\bpartially ordered set\b',
    'total order':   r'\btotally ordered\b|\btotal order\b',
    'isomorphic':    r'\bisomorphic\b.{0,160}\b(?:one-to-one|bijection|correspondence)\b',
    'Eulerian':      r'\bEuler(?:ian)? (?:circuit|path|graph)\b',
    'Hamiltonian':   r'\bHamilton(?:ian)? (?:circuit|path|cycle)\b',
    # "cross" must be allowed to appear as "crossing": the natural way to write
    # the definition is "drawn with no two edges crossing", and \bcross\b does
    # not match that, so this cue reported a correctly taught term as untaught.
    'planar':        r'\bplanar\b.{0,140}\b(?:without|no).{0,40}\bcross(?:ing)?',
    'Kuratowski':    r"\bKuratowski\b",
    'Handshaking':   r'\bHandshaking\b.{0,200}\b(?:twice|2|sum of the degrees)\b',
    'rooted tree':   r'\brooted tree\b.{0,140}\broot\b',
    'preorder':      r'\bpreorder\b.{0,140}\b(?:root|visit)\b',
    'inorder':       r'\binorder\b.{0,140}\b(?:left|visit)\b',
    'postorder':     r'\bpostorder\b.{0,140}\b(?:left|visit|last)\b',
    'prefix':        r'\bprefix notation\b',
    'postfix':       r'\bpostfix notation\b',
    'm-ary':         r'\bm-ary tree\b',
    'bit string':    r'\bbit string\b.{0,140}\b(?:1|one|position|universal)\b',
    'power set':     r'\bpower set\b.{0,120}\b(?:all|every)\b.{0,40}\bsubset',
    'Boolean':       r'\bBoolean algebra\b',
    'pigeonhole':    r'\bpigeonhole principle\b',
}

# Tokens the rot-guard must not mistake for undefined course terms. A 200-level
# reader owns the first group outright; the single letters are variables, not
# abbreviations; the set names are this course's own notation, introduced in
# Foundations; K5 and K3,3 are named graphs, defined where they are used.
ASSUMED = {'CPU', 'RAM', 'PC', 'OS', 'IO', 'ID', 'PIN', 'ATM', 'CGPA', 'TV',
           'DNA', 'GPS', 'URL', 'HTML', 'CSC', 'BSC'}
NOTATION = {'AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR', 'XNOR', 'IF', 'THEN',
            'TRUE', 'FALSE', 'IFF', 'QED', 'LHS', 'RHS'}
CPP = {'CPP', 'STL', 'IDE', 'GCC', 'INT', 'BOOL', 'VOID', 'MAIN', 'STD',
       'COUT', 'CIN', 'ENDL'}


MENTION_RE = re.compile(r'<span class="mention">.*?</span>', re.S)
# An AS PRINTED box holds the examiner's words, reproduced verbatim under the
# rule in MANUAL_METHODOLOGY 4c. The paper is free to use "reflexive" in a
# question printed long before this book defines it, and rewriting the quote to
# avoid that would be the very defect that rule exists to stop. So quoted text
# does not count as THIS BOOK using a notation. It is still checked, by a
# separate rule below: anything a quote uses must be taught somewhere, or the
# reader meets a word in a past paper with nowhere to look it up.
QUOTE_RE = re.compile(r'<div class="box paper".*?</div>\s*</div>', re.S)


def clean(chunk, drop_quotes=False):
    """A section's visible prose: tags gone, entities resolved, diagrams dropped.

    Text inside <span class="mention"> is stripped first. That marks a place
    where the book NAMES a term rather than using it. The front matter lists the
    vocabulary the official course text is missing ("it contains the word vertex
    zero times"), and counting those as uses reports every gap term as used on
    page three, before anything has been taught.
    """
    chunk = MENTION_RE.sub(' ', chunk)
    if drop_quotes:
        chunk = QUOTE_RE.sub(' ', chunk)
    chunk = SVG_RE.sub(' ', chunk)
    chunk = DROP_RE.sub(' ', chunk)
    chunk = TAG_RE.sub(' ', chunk)
    chunk = _h.unescape(chunk)
    chunk = chunk.replace('−', '-').replace(' ', ' ')
    # A meaning split across a line break must read as one phrase, or the audit
    # misses that "is an element of" is taught at all.
    return re.sub(r'\s+', ' ', chunk)


def sections(html, drop_quotes=False):
    """The book in reading order: [(anchor id, cleaned text), ...]."""
    marks = [(m.group(1), m.start()) for m in ANCHOR_RE.finditer(html)]
    out = []
    for i, (mid, pos) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(html)
        out.append((mid, clean(html[pos:end], drop_quotes)))
    return out


# Where a bare name collides with another sense, the USE pattern is narrowed to
# the phrase that carries the technical meaning being audited. Without this the
# gate reports homonyms as forward references. Measured on this book, all four of
# these fired falsely: "symmetric difference" is a set operation and has nothing
# to do with a symmetric RELATION; the "transitive property" of subsets in 2.1 is
# not the transitivity of a relation; "logical equivalence" in 1.3 is not an
# "equivalence relation"; and the multiplication sign in Foundations is not the
# Cartesian product.
USE_OVERRIDE = {
    'symmetric':   r'\bsymmetric\b(?!\s+difference)',
    'equivalence': r'\bequivalence relation\b',
    'transitive':  r'\btransitive\b(?!\s+property)',
    # "degree" is a graph term here, but it is also an academic qualification
    # (Logic 1.1 uses "a degree or five years of experience" to illustrate the
    # inclusive or) and a unit of temperature. Require the graph sense.
    'degree':      (r'\bdegree\s+of\s+(?:a\s+|the\s+|every\s+)?(?:vertex|node)'
                    r'|\b(?:vertex|vertices|node|nodes)\b[^.]{0,40}\bdegree\b'
                    r'|\bdegree\s+\d'
                    r'|\b(?:even|odd|in|out)-?\s?degree\b'),
    # "adjacency" the gap term is the MATRIX of section 6.5. The bare word also
    # names the plain vertex-to-vertex relation, which section 6.1 defines
    # alongside incidence and is entitled to use. Require the matrix sense.
    'adjacency':   r'\badjacency (?:matrix|matrices|list)\b',
}


def all_entries():
    """Everything audited: symbols, terms, and the unwaivable gap terms."""
    out = {}
    for k, v in SYMBOLS.items():
        out[k] = ('symbol', v, USE_OVERRIDE.get(k, re.escape(k)))
    for k, v in TERMS.items():
        out[k] = ('term', v, USE_OVERRIDE.get(k, r'\b' + re.escape(k) + r'\b'))
    for k, v in GAP_TERMS.items():
        out[k] = ('gap', v, USE_OVERRIDE.get(k, r'\b' + re.escape(k) + r'\b'))
    return out


def first_positions(secs, entries):
    """For every entry: (first taught, first used, first-use section).

    A position is (section index, character offset) so it compares in reading
    order across the whole book. A symbol is matched exactly; a term and its
    meaning are matched case-insensitively, since a heading may capitalise it.
    """
    use_re = {k: re.compile(pat, re.I) for k, (_, _, pat) in entries.items()}
    intro_re = {k: re.compile(exp, re.I) for k, (_, exp, _) in entries.items()}
    taught, used, used_sec = {}, {}, {}
    for sidx, (mid, text) in enumerate(secs):
        for k in entries:
            if k not in taught:
                m = intro_re[k].search(text)
                if m:
                    taught[k] = (sidx, m.start())
            if k not in used:
                m = use_re[k].search(text)
                if m:
                    used[k] = (sidx, m.start())
                    used_sec[k] = mid
    return taught, used, used_sec


def discover_terms(secs):
    """Every token the book itself typesets as a defined abbreviation."""
    full = ' '.join(t for _, t in secs)
    found = set(re.findall(r'\(\s*([A-Z][A-Za-z0-9]*[A-Z0-9])\s*\)', full))
    found |= set(re.findall(r'\b([A-Z][A-Z0-9]{1,})\b\s*\([a-z]', full))
    return found


def is_ignorable(tok):
    """Not an undefined course term: a label, a variable, or a known name."""
    if tok in ASSUMED or tok in NOTATION or tok in CPP:
        return True
    if re.fullmatch(r'K\d+(,\d+)?', tok):
        return True                       # a named complete/bipartite graph, K5, K3,3
    if re.fullmatch(r'[A-Z]\d*', tok):
        return True                       # a set or vertex name: A, B, R1, S, V2
    if re.fullmatch(r'[QP]\d+[A-Z]?', tok):
        return True                       # a question label, Q1, Q4B
    if re.fullmatch(r'[A-Z]{1,3}\d{2,4}', tok):
        return True                       # a course code, CSC242, PQ2526
    return False


def report(html):
    entries = all_entries()
    # Our own prose, with the examiner's quoted words removed: this is what the
    # before-use ordering applies to.
    secs = sections(html, drop_quotes=True)
    order = [mid for mid, _ in secs]
    taught, used, used_sec = first_positions(secs, entries)

    # The whole book including quotes, used only to find notations that appear
    # in a past question. Those need not be taught BEFORE the quote, but they
    # must be taught somewhere or the reader is stranded.
    with_quotes = sections(html)
    _, q_used, q_sec = first_positions(with_quotes, entries)
    quoted_untaught = [(k, q_sec[k]) for k in entries
                       if k in q_used and k not in taught]

    untaught, before, in_mock = [], [], []
    for k, (kind, _, _) in entries.items():
        if k not in used:
            continue                       # the book never uses it; nothing owed
        if k not in taught:
            untaught.append((k, kind))
            continue
        # Judged by section: a unit that defines a term it opened with is
        # self-contained and never sends the reader elsewhere. Only a meaning
        # taught in a LATER section than its first use is a real gap.
        if used[k][0] < taught[k][0]:
            before.append((k, kind, order[used[k][0]], order[taught[k][0]]))
        if used_sec[k].startswith('MOCK'):
            in_mock.append((k, kind, used_sec[k]))

    unlisted = sorted(t for t in discover_terms(with_quotes)
                      if not is_ignorable(t) and t not in entries)

    used_n = sum(1 for k in entries if k in used)
    print(f'FIRST-USE AUDIT: {used_n} of {len(entries)} declared notations used '
          f'across {len(order)} sections')
    ok = True

    if before:
        ok = False
        print(f'  x {len(before)} used before their meaning is written out:')
        for k, kind, u, t in before:
            emit(f'      {k!r:14} ({kind}) first used in {u}, first taught only in {t}')
    else:
        print('  . every notation used is introduced at or before its first use')

    if untaught:
        ok = False
        print(f'  x {len(untaught)} used but introduced nowhere, so the reader '
              f'cannot look them up:')
        for k, kind in untaught:
            emit(f'      {k!r:14} ({kind}) used in {used_sec[k]}')
    else:
        print('  . every notation used is introduced somewhere')

    if quoted_untaught:
        ok = False
        print(f'  x {len(quoted_untaught)} appear in a quoted past question but '
              f'are taught nowhere in the book:')
        for k, mid in quoted_untaught:
            emit(f'      {k!r:14} quoted in {mid}')
    else:
        print('  . every notation a past question uses is taught somewhere')

    if in_mock:
        ok = False
        print(f'  x {len(in_mock)} appear first in a mock, so the reader is '
              f'examined on what was never shown:')
        for k, kind, mid in in_mock:
            emit(f'      {k!r:14} ({kind}) first appears in {mid}')
    else:
        print('  . no notation makes its first appearance in a mock')

    if unlisted:
        ok = False
        print(f'  x {len(unlisted)} typeset as defined abbreviations but missing '
              f'from the declared list, so they are used but never audited:')
        for t in unlisted:
            emit(f'      {t}')
    else:
        print('  . the declared list has not fallen behind the book')

    gap_used = sum(1 for k in GAP_TERMS if k in used)
    gap_taught = sum(1 for k in GAP_TERMS if k in taught)
    print(f'  . gap topics: {gap_taught} of {len(GAP_TERMS)} introduced '
          f'({gap_used} used); the course text teaches none of these')

    print('FIRST-USE AUDIT: ' + ('pass' if ok else 'FAIL'))
    return ok


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'full_manual.html'
    with open(src, encoding='utf-8') as fh:
        sys.exit(0 if report(fh.read()) else 1)
