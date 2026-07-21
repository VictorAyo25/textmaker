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
    ('front.html', 'value = d<sub>n&#8722;1</sub>', 'positional notation'),
    ('module1_unit2.html', '0 to 2<sup>n</sup> &#8722; 1', 'unsigned range'),
    ('module1_unit2.html', "<td>Two's complement</td>", 'signed ranges table'),
    ('module1_unit2.html', 'bits = (width&#215;dpi)', 'image size'),
    ('module1_unit3.html', 'Exponent field = e + 127', 'IEEE encode'),
    ('module1_unit3.html', 'Value = &#177; 1.<i>mantissa</i>', 'IEEE decode'),
    ('module1_unit4.html', 'bytes per instruction = opcode bytes', 'instruction bytes'),
    ('module2.html', 'k = log<sub>2</sub>N', 'addressing capacity'),
    ('module2_unit2.html', 'CPU time = IC &#215; CPI &#215; T', 'CPU time / CPI / MIPS'),
    ('module2_unit2.html', 'S = 1 / ( (1 &#8722; f) + f / s )', "Amdahl's law"),
    ('module2_unit3.html', '(k + n &#8722; 1)', 'pipeline timing'),
    ('module3.html', 'M = 2<sup>n</sup> / K', 'blocks in memory'),
    ('module3.html', 'average = H&#215;T<sub>1</sub>', 'two-level average access'),
    ('module3_unit3.html', 'AMAT = T<sub>cache</sub>', 'AMAT'),
    ('module3_unit3.html', '<b>Tag bits</b>', 'cache field widths'),
    ('module3_unit3.html', 'number of lines &#215; tag bits per line', 'tag directory'),
]

# "Must memorise" boxes that state no formula: they are reference tables or mnemonics.
# Named individually so that adding a real formula box cannot hide among them.
NON_FORMULA_MEM = {
    'Memory hook', 'Hex letters', 'Powers of two',
    'The four formats', 'The hierarchy', 'Example processors',
    'The four-line answer',   # how to lay an answer out, no symbols of its own
}

# Worked examples that compute nothing: they ask for definitions, differences or a
# comparison, so there are no given parameters and no formula to state. Everything else
# must open the way a physics solution does, with Given / Find / Formula.
NON_NUMERIC_WORK = {
    'front.html': {'SLIDE / CLASSWORK / PQ'},          # the box legend, not a question
    'module1.html': {'PQ 25/26 Q1a(i)', 'PQ 25/26 Q1a(ii)',
                     'PQ 24/25 Q3a &middot; PQ 23/24 Q4a'},
    'module1_unit4.html': {'PQ 24/25 Q2c'},            # write a short program
    'module3.html': {'PQ 25/26 Q5c &middot; PQ 24/25 Q2b &middot; PQ 23/24 Q3c'},
    'module3_unit2.html': {'PQ 20/21 Q5b'},            # four differences, DRAM vs SRAM
    'module4.html': {'PQ 24/25 Q4a &middot; PQ 20/21 Q4b &middot; PQ 23/24 Q5c',
                     'PQ 20/21 Q1c'},
}

# A named law must be STATED, not merely used. A formula is a recipe; the law is the
# claim the formula expresses, plus the conditions and the limiting case. The papers ask
# "state Amdahl's law", so a book that only ever computes with it has not taught it.
# (file where the law is taught, text that marks it, the name it must be stated under)
NAMED_LAWS = [
    ('module2_unit2.html', '<span class="tag">Amdahl\'s law</span>', "Amdahl's law."),
    ('module3.html', 'principle of locality of reference',
     'The principle of locality of reference.'),
    ('supplement.html', 'De Morgan', "De Morgan's laws."),
]

BOX_TAG_RE = re.compile(
    r'<div class="box mem"><div class="bar"><span>Must memorise</span>'
    r'<span class="tag">([^<]*)</span>')
WORK_TAG_RE = re.compile(
    r'<div class="box work"><div class="bar"><span>Worked example</span>'
    r'<span class="tag">([^<]*)</span>')


def read(name):
    with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
        return fh.read()


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
        at = text.find(marker)
        if at == -1:
            problems.append(f'{fname}: the {name} formula is gone (looked for {marker!r})')
            continue
        checked += 1
        window = text[max(0, at - BEHIND):at + NEAR]
        if 'wheredef' not in window:
            problems.append(f'{fname}: the {name} formula states no symbol breakdown '
                            f'near it; a reader meets its letters undefined')

    # ---- 2. discovery: no new formula box slips in undefined ----
    scanned = 0
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        for tag, body in boxes(read(fname), BOX_TAG_RE):
            scanned += 1
            if tag in NON_FORMULA_MEM:
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
        at = text.find(marker)
        if at == -1:
            problems.append(f'{fname}: {name} is gone (looked for {marker!r})')
            continue
        laws += 1
        if 'lawstate' not in text[max(0, at - BEHIND):at + NEAR]:
            problems.append(f'{fname}: {name} is used but never stated as a law '
                            f'(add a .lawstate giving the claim in words, its '
                            f'conditions and its limiting case)')
        if f'<span class="lawname">{name}' not in everything:
            problems.append(f'{name} is never written out under a .lawname, so a reader '
                            f'asked to "state" it has no wording to reproduce')

    # ---- 4. the styling the whole rule rests on still exists ----
    with open(os.path.join(HERE, 'manual.css'), encoding='utf-8') as fh:
        css = fh.read()
        if '.lawstate' not in css:
            problems.append('manual.css: .lawstate style is gone, so every law statement '
                            'renders as undifferentiated body text')
        if '.wheredef' not in css:
            problems.append('manual.css: .wheredef style is gone, so every symbol '
                            'breakdown renders as undifferentiated body text')

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


if __name__ == '__main__':
    sys.exit(0 if report() else 1)
