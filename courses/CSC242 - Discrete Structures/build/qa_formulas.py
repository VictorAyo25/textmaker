"""Formula gate: no formula appears without saying what each of its symbols means.

    cd build && python qa_formulas.py

Victor's rule, added after a reader fed back that formulas were stated and used but
their constituents were never spelled out: *at every point a formula is introduced to
solve a problem, outline what each constituent means*. Promising that in prose is
worthless; it rots the moment a new formula is added. So it is measured here.

The check has two halves, because either alone would be a hole:

  1. REGISTRY. Every formula the book is known to teach is listed below with a
     distinctive fragment of how it is written. Each must still be present, AND a
     `.wheredef` block must follow it closely. This catches a formula whose definition
     is deleted, or a formula silently reworded so its definition no longer matches.

  2. DISCOVERY. Every "Must memorise" box is scanned. If it is not one of the named
     reference tables (which state no formula), it must carry a `.wheredef`. This
     catches a NEW formula added later with no symbol breakdown, which the registry
     alone could never see.

The gap between the two matters: the registry proves the formulas we know about are
still explained, and the discovery half proves nobody added one we do not know about.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

# How far after a formula its symbol breakdown may sit. A .wheredef further away than
# this is on the reader's next screen, which is not "at the point it is introduced".
NEAR = 1400

# Some formulas are written INSIDE their own .wheredef, which states the formula and
# defines its letters in one block. That is the rule being satisfied, not dodged, so the
# search window opens slightly before the formula to see the block it sits in. Kept tight
# (a .wheredef opening tag plus its label is about 90 characters) so the window cannot
# reach back and borrow the previous formula's breakdown.
BEHIND = 200

# (file, distinctive fragment of the formula as written, human name)
FORMULA_SITES = [
    # (file, distinctive fragment of the formula as written, human name)
    # Filled in as each part is authored.
    ('foundations.html', 'n! = n &#215; (n &#8722; 1)', 'factorial'),
    ('p2_22.html', 'n(A &#8746; B) = n(A) + n(B) &#8722;', 'two-set counting'),
    ('p2_23.html', 'b<sub>i</sub> = 1 exactly when', 'bit string of a subset'),
    ('p4_43.html', '(f &#8728; g)(x) = f(g(x))', 'composition'),
    ('p5_counting.html', 'n<sub>1</sub> &#215; n<sub>2</sub> &#215;', 'product rule'),
    ('p5_counting.html', 'n<sub>1</sub> + n<sub>2</sub> + ', 'sum rule'),
    ('p5_counting.html', '(number with the property) = (total)', 'subtraction rule'),
    ('p5_52.html', 'P(n, r) = n! / (n &#8722; r)!', 'permutation'),
    ('p5_52.html', 'C(n, r) = n! / (r! (n &#8722; r)!)', 'combination'),
    ('p5_52.html', 'n! / (n<sub>1</sub>! &#215; n<sub>2</sub>!', 'arrangements with repeats'),
    ('p5_53.html', 'n(A &#8746; B &#8746; C) = n(A) + n(B) +',
     'three-set inclusion and exclusion'),
    ('p5_53.html', '&#8968;N / k&#8969;', 'generalised pigeonhole'),
    ('p5_54.html', 'C(n, 0) x<sup>n</sup>', 'binomial theorem'),
    ('p5_54.html', 'C(n, 0) + C(n, 1) + &#8230; + C(n, n)', 'binomial row sum'),
    ('p6_graphs.html', 'A <b>graph</b> G = (V, E)', 'graph as a vertex and edge set'),
    ('p6_graphs.html', 'The <b>order</b> of a graph', 'order and size'),
    ('p6_graphs.html', 'The <b>degree of a vertex</b>', 'degree'),
    ('p6_62.html', 'C(n, 2) = n(n &#8722; 1) / 2', 'edges of a complete graph'),
    ('p6_64.html', 'deg<sup>&#8722;</sup>(v)', 'in-degree and out-degree'),
    ('p6_64.html', '&#931; deg<sup>&#8722;</sup>(v) =', 'digraph handshaking'),
    ('p6_65.html', 'a<sub>ij</sub>', 'adjacency matrix'),
    ('p6_65.html', 'p<sub>ij</sub> = 1', 'path matrix'),
    ('p6_65.html', 'm<sub>ij</sub> = 1', 'relation matrix'),
    ('p6_66.html', 'u and v are adjacent in G exactly when', 'isomorphism'),
    ('p6_67.html', 'e &#8804; 3v &#8722; 6', 'the planar edge bounds'),
    ('p7_trees.html', '<b>e = v &#8722; 1</b>', 'edges of a tree'),
    ('p7_72.html', '<b>n = mi + 1</b>', 'full m-ary counting'),
    ('p7_72.html', 'at most m<sup>h</sup> leaves', 'the height bound on leaves'),
    ('p7_73.html', 'T<sub>1</sub>, T<sub>2</sub>', 'the three traversals'),
    ('p8_boolean.html', 'A &#183; B, or AB', 'the Boolean operations'),
    ('p9_proof.html', 'm = 2k for some integer k', 'even, odd, rational, divides'),
    ('p9_proof.html', 'r &#8743; &#172;r', 'the six proof strategies'),
    ('p9_92.html', 'gives P(n) for every', 'the induction principle'),
    ('p9_93.html', 'a<sub>n</sub> = a + (n &#8722; 1)d', 'arithmetic progression'),
    ('p9_93.html', 'ar<sup>n&#8722;1</sup>', 'geometric progression'),
    ('p9_93.html', 'n(n + 1)(2n + 1) / 6', 'the standard sums'),
    ('p9_94.html', 'f(a<sub>n&#8722;1</sub>', 'recurrence relation'),
    ('p9_94.html', 'c<sub>1</sub>x<sup>k&#8722;1</sup>', 'the characteristic equation'),
    ('p10_stats.html', 'x&#772; = (&#8721; x<sub>i</sub>) /', 'the mean'),
    ('p10_stats.html', '&#963;<sup>2</sup> = (&#8721; (x<sub>i</sub>',
     'variance and standard deviation'),
    ('p10_102.html', 'P(E) = n(E) / n(S)', 'probability of an event'),
    ('p10_102.html', 'P(B | A) = P(A &#8745; B) / P(A)', 'conditional probability'),
    ('p10_102.html', "P(A | B) = P(B | A) &#215; P(A) /", "Bayes' theorem"),
]

# "Must memorise" boxes that state no formula: they are reference tables or mnemonics.
# Named individually so that adding a real formula box cannot hide among them.
NON_FORMULA_MEM = {
    # Must-memorise boxes that state no formula: reference tables and mnemonics.
    # Named individually so a real formula box cannot hide among them.
    #
    # The test applied to each: does the box put letters in front of the reader
    # that it does not itself say the meaning of? A definition box that names its
    # own terms as it introduces them ("the number of elements in a set A is its
    # cardinality, written n(A)") has already done the job a .wheredef does, and
    # bolting one on would restate the sentence above it.
    #
    # Keyed by FILE as well as tag, exactly like NON_NUMERIC_WORK below. Several
    # boxes are simply tagged "Definition", and a bare tag-keyed exemption would
    # have let one word excuse four boxes in four different parts, including any
    # future box someone tags the same way. An exemption should cover the box it
    # was written for and nothing else.
    'foundations.html': {'The five number sets', 'Read these out loud',
                         'Roster and set-builder'},
    'foundations_f2.html': {'English to symbols', 'The four-line answer'},
    # A convention of this book, not mathematics.
    'front.html': {'The reserved colour'},
    # Part One: definitions and reference tables. The laws table opens by saying
    # what T and F mean; the connectives table is a glossary of the symbols.
    'p1_logic.html': {'Definition', 'The connectives',
                      'Three names for a final column'},
    'p1_12.html': {'The one that matters'},
    'p1_13.html': {'Definition', 'The laws of logic'},
    'p1_14.html': {'Predicate versus propositional logic',
                   'Universal and existential'},
    'p1_15.html': {'Validity is about shape, not truth', 'The standard rules'},
    # Part Two: definitions and operation tables.
    'p2_sets.html': {'Set, element, cardinality', 'The nine types, with examples',
                     '&#8838; and &#8834;'},
    'p2_22.html': {'The five operations'},
    # Part Three: property tables and definitions, each stating "R is a relation
    # on a set A" before using either letter.
    'p3_relations.html': {'Definition'},
    'p3_32.html': {'The five properties', 'How to disprove each property'},
    'p3_33.html': {'Equivalence relation', 'Classes and partitions'},
    'p3_34.html': {'Partial order', 'Total order'},
    # Part Four: definitions of correspondence types.
    'p4_functions.html': {'Definition', 'Domain, codomain, range'},
    'p4_42.html': {'One-to-one and onto'},
    'p4_43.html': {'Inverse'},
    # Part Six: a catalogue of named shapes, and a checklist of invariants.
    'p6_62.html': {'The named shapes'},
    'p6_66.html': {'Invariants: how to disprove isomorphism'},
    # Part Seven and Eight: a vocabulary table, a translation table between the
    # three notations, and the law table itself. None introduces a symbol it
    # does not name in its own rows.
    'p7_trees.html': {'The key terminology'},
    'p8_boolean.html': {'The three notations are one subject', 'The laws, and duality'},
    # Part Nine and Ten: a glossary of the words for provable things, and a
    # four-row table naming kinds of event. Neither puts a letter in front of
    # the reader; both are vocabulary, and every term is defined in its own row.
    'p9_proof.html': {'Theorem, lemma, corollary and the rest'},
    'p10_102.html': {'The four kinds of event'},
}

# Worked examples that compute nothing: they ask for definitions, differences or a
# comparison, so there are no given parameters and no formula to state. Everything else
# must open the way a physics solution does, with Given / Find / Formula.
NON_NUMERIC_WORK = {
    # Worked examples that compute nothing (definitions, differences, a proof in
    # words, a drawing). Everything numeric must open Given / Find / Formula.
    #
    # The test applied to each: are any numbers substituted into a formula? A
    # truth table, a translation into symbols, a bit-string encoding and a proof
    # by arbitrary element all produce an answer without ever having a "Given"
    # worth listing. Forcing a .params onto them would print a Formula row
    # reading "none", which teaches nothing and trains the reader to skip the
    # block on the questions where it matters.
    'foundations.html': {'Method',                  # writing sets two ways
                         'PQ 25/26 Q2(a)'},         # five reasons, no arithmetic
    'foundations_f2.html': {'Method'},              # English into symbols
    'front.html': {'PQ 25/26 Q1c'},                 # the specimen box itself
    'p1_12.html': {'PQ 24/25 Q1(a)'},               # converse, inverse, contrapositive
    'p1_14.html': {'PQ 24/25 Q2(a)', 'PQ 24/25 Q4(a)', 'PQ 24/25 Q2(c)'},
    'p1_15.html': {'PQ 25/26 Q4(c)', 'PQ 25/26 Q4(b)'},
    'p1_logic.html': {'PQ 20/21 Q5(a)', 'PQ 24/25 Q1(b) i and ii'},
    'p2_22.html': {'PQ 24/25 Q3(c)'},               # De Morgan by arbitrary element
    'p2_23.html': {'PQ 23/24 Q3(a)', 'PQ 24/25 Q3(d)(ii)', 'PQ 24/25 Q3(a)'},
    'p2_sets.html': {'PQ 25/26 Q1(b)',              # the nine types, as a table
                     'PQ 21/22 Q1(a)'},             # set-builder into roster form
    'p3_32.html': {'PQ 24/25 Q4(b)', 'PQ 20/21 Q5(c)(ii)'},
    'p3_relations.html': {'PQ 20/21 Q5(c)(i)'},     # listing ordered pairs
    'p4_42.html': {'PQ 21/22 Q2(c) &middot; PQ 20/21 Q4(b)',
                   'Method &middot; deciding from a formula'},
    'p4_43.html': {'PQ 24/25 Q2 b(ii)', 'Method'},  # a proof, and an inverse
    'p4_functions.html': {'Method'},                # which relations are functions
    # Part Six: short notes, term distinctions and lists of application areas.
    # Nothing is substituted into anything.
    'p6_graphs.html': {'PQ 25/26 Q1 a) i)',         # degree versus valency
                       'PQ 25/26 Q4(a)(i) and (ii)',
                       'PQ 20/21 Q2(b) &middot; PQ 20/21 Q3(c) &middot; '
                       'PQ 21/22 Q5(a) &middot; PQ 21/22 Q3(b)'},
    'p6_62.html': {'PQ 20/21 Q1(a) &middot; PQ 21/22 Q1(c) &middot; PQ 23/24 Q4(a)'},
    # "State the theorem" is a recall answer: there is nothing given to list.
    'p6_63.html': {'PQ 21/22 Q4(a) &middot; PQ 23/24 Q5(a)'},
    # A short note, and a procedure taught step by step on a figure of our own.
    'p6_64.html': {'PQ 25/26 Q4(a)(iii)',
                   'Method &middot; how to tabulate any digraph'},
    # Term distinctions and an explain-and-discuss answer about storage.
    'p6_65.html': {'PQ 25/26 Q1 a) iv)', 'PQ 25/26 Q1 a) v)', 'PQ 25/26 Q6(a)'},
    # Definitions of isomorphism and of an Eulerian graph.
    'p6_66.html': {'PQ 24/25 Q5(g) &middot; PQ 25/26 Q4(a)(iv)',
                   'PQ 25/26 Q4(a)(v)'},
    # Definitions, a terminology list and a list of application domains.
    'p7_trees.html': {'PQ 20/21 Q2(c) &middot; PQ 21/22 Q3(c)',
                      'PQ 23/24 Q4, third part'},
    'p7_72.html': {'PQ 20/21 Q3(a) &middot; PQ 21/22 Q4(b)'},
    # Algebraic simplification: laws applied to symbols, no given values.
    'p8_boolean.html': {'Method &middot; simplification'},
    # Part Nine's proof workshops. Each is an argument about an arbitrary
    # integer, so there is nothing given to list and no formula to substitute
    # into: a Given row would have to read "an arbitrary integer n" and a
    # Formula row "the definition of odd", which is the first line of the proof
    # itself. The induction examples in 9.2 DO carry .params, because there the
    # claim, the target and the method are three separate things worth naming
    # before the algebra starts.
    'p9_proof.html': {'Method &middot; three direct proofs',
                      'Method &middot; contrapositive',
                      'Method &middot; contradiction',
                      'Method &middot; proof by cases'},
}

# A named law must be STATED, not merely used. A formula is a recipe; the law is the
# claim the formula expresses, plus the conditions and the limiting case. The papers ask
# "state Amdahl's law", so a book that only ever computes with it has not taught it.
# (file where the law is taught, text that marks it, the name it must be stated under)
NAMED_LAWS = [
    # (file where the law is taught, text that marks it, the name it is stated under)
    ("p1_13.html", "De Morgan", "De Morgan's laws"),
    ("p1_14.html", "De Morgan", "De Morgan's laws for quantifiers"),
    ("p2_22.html", "De Morgan", "De Morgan's laws (set form)"),
    ("p5_53.html", "n(A &#8746; B) = n(A) + n(B) &#8722;",
     "The principle of inclusion and exclusion"),
    ("p5_53.html", "k + 1 or more objects", "The pigeonhole principle"),
    ("p6_63.html", "&#931; deg(v) = 2|E|", "The Handshaking theorem"),
    ("p6_66.html", "Euler path", "Euler's theorem on circuits and paths"),
    ("p6_67.html", "v &#8722; e + f = 2", "Euler's formula for planar graphs"),
    ("p6_67.html", "subdivision of K<sub>5</sub>", "Kuratowski's theorem"),
    ("p9_92.html", "principle of mathematical induction",
     "The principle of mathematical induction"),
    # A formula is a recipe; a law is the claim plus its conditions and its
    # limiting case. This course has several the papers ask you to STATE:
    # the Handshaking theorem, De Morgan's laws, Kuratowski's theorem,
    # Euler's formula, the pigeonhole principle, inclusion-exclusion.
]

# The content files are hand-written and indented, so the bar sits on the line
# BELOW the box that opens it. An earlier version of these two patterns ran the
# tags together with no separator, which matches nothing any human would type:
# the gate then scanned zero boxes and reported a pass every single run. A gate
# that cannot fail is not a gate, and this one had been green on a book with
# more than thirty must-memorise boxes in it. Allow whitespace between the tags,
# and never let this file report a pass on a zero count again: see the
# ZERO-SCAN guard at the end of report().
#
# The tag body is deliberately `[^<]*`, so a box whose tag contains markup (a
# <sub>, say) does not parse and is reported by the count guard rather than
# silently skipped. That is the behaviour we want: the tag string is used as a
# dictionary key in NON_FORMULA_MEM and NON_NUMERIC_WORK below, and keys made of
# HTML would be unreadable and impossible to keep in step with the book. A box
# tag is a short human label; keep it plain text. This has fired once, on a 9.4
# tag that carried subscripted variable names.
BOX_TAG_RE = re.compile(
    r'<div class="box mem">\s*<div class="bar">\s*<span>Must memorise</span>'
    r'\s*<span class="tag">([^<]*)</span>')
WORK_TAG_RE = re.compile(
    r'<div class="box work">\s*<div class="bar">\s*<span>Worked example</span>'
    r'\s*<span class="tag">([^<]*)</span>')


def read(name):
    with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
        return fh.read()


DIV_EDGE_RE = re.compile(r'<div\b|</div>')


def _div_end(text, start):
    """Where the div opened at `start` actually closes, counting nested tags.

    Slicing to "the next </div>" stops at the first CHILD's closing tag, which
    for a .lawstate means stopping inside its own name line and losing every
    word of the statement. Count the edges instead.
    """
    depth = 0
    for m in DIV_EDGE_RE.finditer(text, start):
        depth += 1 if m.group(0) != '</div>' else -1
        if depth == 0:
            return m.end()
    return len(text)


def boxes(text, pattern):
    """(tag, body) for each matching box, body running to the next box."""
    out = []
    for m in pattern.finditer(text):
        nxt = text.find('<div class="box ', m.end())
        out.append((m.group(1), text[m.end():nxt if nxt != -1 else len(text)]))
    return out


def report():
    problems = []

    # ---- 1. registry: known formulas still present, and still explained nearby ----
    checked = 0
    for fname, marker, name in FORMULA_SITES:
        text = read(fname)
        # EVERY occurrence, not just the first. A formula is normally written
        # more than once in the section that teaches it: once where it is
        # introduced with its breakdown, and again inside a law statement, a
        # worked example or a recall answer. Checking text.find() alone asked
        # whichever copy happened to come first, so a correctly explained formula
        # could fail because a later restatement was quoted higher up the file.
        # The rule being enforced is "the reader meets a breakdown where this is
        # introduced", and one properly explained site satisfies it.
        sites = [m.start() for m in re.finditer(re.escape(marker), text)]
        if not sites:
            problems.append(f'{fname}: the {name} formula is gone (looked for {marker!r})')
            continue
        checked += 1
        if not any('wheredef' in text[max(0, at - BEHIND):at + NEAR] for at in sites):
            problems.append(f'{fname}: the {name} formula states no symbol breakdown '
                            f'near any of its {len(sites)} appearance(s); a reader '
                            f'meets its letters undefined')

    # ---- 2. discovery: no new formula box slips in undefined ----
    scanned = 0
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        exempt_mem = NON_FORMULA_MEM.get(fname, set())
        for tag, body in boxes(read(fname), BOX_TAG_RE):
            scanned += 1
            if tag in exempt_mem:
                continue
            if 'wheredef' not in body:
                problems.append(f'{fname}: Must-memorise box "{tag}" states a formula '
                                f'but never says what its symbols mean (add a .wheredef, '
                                f'or name it in NON_FORMULA_MEM if it is a reference table)')

    # ---- 3. every numeric worked example opens with its parameters ----
    # A reader should meet the givens, the unknown and the formula before any number is
    # substituted, the way a physics solution is set out.
    worked = 0
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        exempt = NON_NUMERIC_WORK.get(fname, set())
        for tag, body in boxes(read(fname), WORK_TAG_RE):
            worked += 1
            if tag in exempt:
                continue
            if 'class="params"' not in body:
                problems.append(f'{fname}: worked example "{tag}" jumps straight into the '
                                f'solution with no Given / Find / Formula block (add a '
                                f'.params, or name it in NON_NUMERIC_WORK if it computes '
                                f'nothing)')

    # ---- 3b. every named law is stated as a law, not just used ----
    laws = 0
    everything = ''.join(read(f) for f in sorted(os.listdir(CONTENT))
                         if f.endswith('.html'))
    for fname, marker, name in NAMED_LAWS:
        text = read(fname)
        if marker not in text:
            problems.append(f'{fname}: {name} is gone (looked for {marker!r})')
            continue
        laws += 1
        # Find the .lawstate block that carries this name and read it, rather
        # than asking whether the word "lawstate" happens to sit near the first
        # place the law is mentioned. Proximity was the wrong question twice
        # over: a law is normally USED in a table well before it is STATED, so
        # the old check failed correct sections; and it would have passed a
        # .lawstate that named a different law entirely.
        #
        # The tag is a div, not a span. The previous literal looked for
        # '<span class="lawname">', which no content file has ever contained, so
        # every law would have been reported missing the moment this list stopped
        # being empty.
        block = None
        for m in re.finditer(r'<div class="lawstate">', everything):
            chunk = everything[m.start():_div_end(everything, m.start())]
            if f'class="lawname">{name}<' in chunk:
                block = chunk
                break
        if block is None:
            problems.append(f'{name} is never written out under a .lawname, so a reader '
                            f'asked to "state" it has no wording to reproduce')
            continue
        for needed, why in (('The claim', 'the claim in words'),
                            ('Conditions', 'the conditions it holds under'),
                            ('limiting case', 'its limiting case')):
            if needed.lower() not in block.lower():
                problems.append(f'{name}: the law statement does not give {why}, so a '
                                f'reader asked to "state and explain" it is short of an '
                                f'answer')

    # ---- 4. the styling the whole rule rests on still exists ----
    with open(os.path.join(HERE, 'manual.css'), encoding='utf-8') as fh:
        css = fh.read()
        if '.lawstate' not in css:
            problems.append('manual.css: .lawstate style is gone, so every law statement '
                            'renders as undifferentiated body text')
        if '.wheredef' not in css:
            problems.append('manual.css: .wheredef style is gone, so every symbol '
                            'breakdown renders as undifferentiated body text')

    # ---- 5. ZERO-SCAN guard: this gate must never pass on an empty sweep ----
    # The failure this guards against already happened once: a pattern that
    # matched nothing let the gate report success while checking nothing at all.
    # Counting the boxes independently of the patterns that parse them means a
    # broken pattern now shows up as a failure instead of a clean run.
    raw = ''.join(read(f) for f in sorted(os.listdir(CONTENT)) if f.endswith('.html'))
    for literal, count, what in (('<div class="box mem">', scanned, 'must-memorise box'),
                                 ('<div class="box work">', worked, 'worked example')):
        present = raw.count(literal)
        if present and not count:
            problems.append(f'the {what} scanner matched none of the {present} in '
                            f'content/, so this gate checked nothing: its pattern is '
                            f'broken, not the book')
        elif present != count:
            problems.append(f'{what}es: {present} in content/ but {count} parsed; '
                            f'{present - count} slipped past the scanner')

    print(f"FORMULA GATE: {checked} formulas checked, {scanned} must-memorise boxes and "
          f"{worked} worked examples and {laws} named laws scanned")
    if problems:
        print('FORMULA GATE: FAIL')
        for p in problems:
            print('  x ' + p)
        return False
    print('  . every formula states what each of its symbols means, right where it is used')
    print('  . every must-memorise box either defines its symbols or is a named reference table')
    print('  . every numeric worked example opens with Given / Find / Formula')
    print('  . every named law is stated as a law, with its conditions and limit')
    return True


def control():
    """Prove this gate fails on each defect it claims to catch.

    Every test tampers with a real file, re-runs report(), and restores the file
    in a finally block so a crash cannot leave the book edited. A gate nobody has
    tried to break is being trusted on faith (MANUAL_METHODOLOGY item 9), and
    this particular gate had been reporting a pass while scanning zero boxes, so
    faith was misplaced once already.
    """
    import contextlib
    import io

    @contextlib.contextmanager
    def tampered(fname, old, new):
        path = os.path.join(CONTENT, fname)
        original = open(path, encoding='utf-8').read()
        assert old in original, f'control setup: {old!r} not in {fname}'
        try:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(original.replace(old, new, 1))
            yield
        finally:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(original)

    def fails():
        """report() with its output swallowed, so the log stays readable."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ok = report()
        return not ok

    print('CONTROL TESTS for the formula gate')

    print('CONTROL TEST 1: delete a registered formula\'s symbol breakdown')
    with tampered('p5_52.html', '<div class="wheredef"><span class="wlab">Where</span>\n'
                                '      <span class="sym">n</span> is how many distinct',
                  '<div class="gone"><span class="wlab">Where</span>\n'
                  '      <span class="sym">n</span> is how many distinct'):
        print(f'  {"PASS" if fails() else "FAIL"}: P(n, r) with its .wheredef removed '
              f'was {"rejected" if fails() else "ACCEPTED"}')

    print('CONTROL TEST 2: add a NEW formula box the registry has never heard of')
    new_box = ('<div class="box mem">\n    <div class="bar"><span>Must memorise</span>'
               '<span class="tag">Control probe</span></div>\n    <div class="body">'
               '<p>E = mc&#178;</p></div>\n  </div>\n\n  <h3 class="sub">Factorial')
    with tampered('p5_52.html', '<h3 class="sub">Factorial', new_box):
        print(f'  {"PASS" if fails() else "FAIL"}: an unregistered formula box with no '
              f'.wheredef was {"rejected" if fails() else "ACCEPTED"}')

    print('CONTROL TEST 3: strip Given / Find / Formula off a numeric worked example')
    with tampered('p5_52.html', '<dl class="params">\n        <dt>Given</dt><dd>The '
                                'letters S, C, H, O, O, L.',
                  '<dl class="stripped">\n        <dt>Given</dt><dd>The '
                  'letters S, C, H, O, O, L.'):
        print(f'  {"PASS" if fails() else "FAIL"}: the SCHOOL worked example without a '
              f'.params was {"rejected" if fails() else "ACCEPTED"}')

    print('CONTROL TEST 4: remove a named law\'s limiting case')
    with tampered('p5_53.html', '<b>The limiting case.</b> When the sets are disjoint',
                  '<b>A further note.</b> When the sets are disjoint'):
        print(f'  {"PASS" if fails() else "FAIL"}: inclusion and exclusion stated without '
              f'its limiting case was {"rejected" if fails() else "ACCEPTED"}')

    print('CONTROL TEST 5: break the box scanner itself')
    # The failure that actually happened: a pattern matching nothing, so the gate
    # swept an empty book and reported success. The zero-scan guard must turn
    # that into a failure rather than a clean run.
    global BOX_TAG_RE
    keep = BOX_TAG_RE
    try:
        BOX_TAG_RE = re.compile(r'<div class="box mem"><div class="bar">'
                                r'<span>Must memorise</span><span class="tag">([^<]*)</span>')
        caught = fails()
    finally:
        BOX_TAG_RE = keep
    print(f'  {"PASS" if caught else "FAIL"}: a scanner matching zero of the 52 boxes '
          f'was {"reported as broken" if caught else "ACCEPTED AS A PASS"}')

    print('CONTROL: the book is restored; the gate below must be green again')
    print(f'  {"PASS" if report() else "FAIL"}: clean run after tampering')


if __name__ == '__main__':
    if '--control' in sys.argv:
        control()
        sys.exit(0)
    sys.exit(0 if report() else 1)
