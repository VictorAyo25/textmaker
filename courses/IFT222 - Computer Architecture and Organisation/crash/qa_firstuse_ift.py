"""Every load-bearing acronym the manual uses, and where it is first taught.

    cd build && python assemble.py --no-pdf   # writes full_manual.html
    python qa_firstuse_ift.py                  # then audit it

The promise this checks is Victor's: **zero external sources**. A reader must
never need a lecturer, a website, or the official course text. Asserting that is
easy and worthless; it only means something measured, and it is exactly the kind
of claim that silently rots as a book grows past seventy pages.

This is an architecture manual, not a programming one, so it has no code APIs to
track. What it has instead is a vocabulary of acronyms: CPI, AMAT, ISA, RISC,
DRAM, the pipeline stages. The reader meets each as shorthand and is owed its
meaning at or before that moment. Three rules, none of which survives being
asserted rather than measured against the assembled book in reading order:

  1. **Nothing is used before it is taught.** An acronym whose first appearance
     precedes the first place its meaning is written out is a hole: the reader
     meets the shorthand with nothing to unpack it.
  2. **Nothing load-bearing goes untaught.** An acronym used in the book whose
     meaning is written out nowhere leaves the reader with no way to look it up.
  3. **A mock teaches nothing.** A mock paper tests what the modules taught, so
     an acronym whose first appearance in the whole book is inside a mock is one
     the reader is examined on and was never shown.

The glossary below is the ground truth, the analogue of the keyword set the Java
and Python audits hard-code. A curated list can rot, so a mechanical rot-guard
(discover_terms) sweeps the book for anything typeset as a defined acronym --
`Expansion (ACRO)` or `ACRO (expansion)` -- and fails if the book defines a term
the glossary has never heard of. The list cannot fall behind the book in silence.

This reads the ASSEMBLED html, not content/*.html, so it sees the book in the
order a reader does. Run assemble.py first. SVG diagrams are dropped (their text
labels ride on coordinate noise); `<pre>` and `<table>` are kept, because the
pipeline trace tables are exactly where a reader first meets EX, MEM and WB.
"""
import html as _h
import os
import re
import sys

ANCHOR_RE = re.compile(r'id="sec-([A-Z0-9]+)"')
SVG_RE = re.compile(r'<svg.*?</svg>', re.S | re.I)
DROP_RE = re.compile(r'<(style|script)\b.*?</\1>', re.S | re.I)
TAG_RE = re.compile(r'<[^>]+>')

# The vocabulary a reader of THIS book is owed. Each acronym maps to a pattern
# that matches the meaning as the manual actually writes it (verified against the
# assembled text, e.g. "arithmetic and logic unit", not the textbook's
# "arithmetic logic unit"; "Dynamic RAM", not "Dynamic Random Access Memory").
# The five pipeline stages carry lenient meanings on purpose: a reader has met
# fetch/decode/execute/memory/write-back long before the trace tables, so the
# check that matters for them is rule 3, that none debuts inside a mock.
GLOSSARY = {
    'CPI':  r'cycles per instruction',
    'MIPS': r'million[s]?\s+(?:of\s+)?instructions per second',
    'AMAT': r'average memory access time',
    'IC':   r'instruction count',
    'ISA':  r'instruction set architecture',
    'RISC': r'reduced instruction set',
    'CISC': r'complex instruction set',
    'ALU':  r'arithmetic and logic unit',
    'CU':   r'control unit',
    'PC':   r'program counter',
    'IR':   r'instruction register',
    'MAR':  r'memory address register',
    'MDR':  r'memory data register',
    'EA':   r'effective address',
    'SP':   r'stack pointer',
    'DMA':  r'direct memory access',
    'MMU':  r'memory management unit',
    'PIM':  r'processing[\s-]in[\s-]memory',
    'DRAM': r'dynamic ram',
    'SRAM': r'static ram',
    'BCD':  r'binary coded decimal',
    'RAW':  r'read[\s-]after[\s-]write',
    'WAR':  r'write[\s-]after[\s-]read',
    'WAW':  r'write[\s-]after[\s-]write',
    'IF':   r'\bfetch\b',
    'ID':   r'\bdecode\b',
    'EX':   r'\bexecute[sd]?\b',
    'MEM':  r'\bmemory\b',
    'WB':   r'write[\s-]?back',
    # A sixth stage name the reader meets only through the papers: two of them set
    # a five-stage pipeline as IF, ID, OF, EX, WB rather than IF, ID, EX, MEM, WB.
    # It entered the glossary when the verbatim rule brought the examiner's own
    # "Operand Fetch (OF)" into the book, where the rot-guard found it undeclared.
    'OF':   r'operand fetch',
    # Added for the crash edition, which meets these in the RISC/CISC section and
    # the objective-test bank: SIMD is taught where it is first used; ILP is spelled
    # out in CPU Performance before the MCQ bank names the acronym.
    'SIMD': r'single instruction[,]?\s+multiple data',
    'ILP':  r'instruction[\s-]level parallelism',
}

# Tokens the rot-guard must not mistake for undefined course terms. A 200-level
# reader owns the first group outright; the operators and Boolean product terms
# are notation, not acronyms; the mnemonics are opcodes taught as operations in
# the ISA unit, not spelled-out abbreviations; the standards are named, never
# expanded, by universal convention.
ASSUMED = {'CPU', 'RAM', 'ROM', 'EEPROM', 'KB', 'MB', 'GB', 'TB', 'PB', 'SSD',
           'HDD', 'USB', 'OS', 'IO'}
OPERATORS = {'AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR', 'XNOR'}
MNEMONICS = {'ADD', 'SUB', 'MUL', 'DIV', 'MOV', 'MOVE', 'LOAD', 'STORE', 'PUSH',
             'POP', 'CALL', 'RET', 'RETURN', 'JUMP', 'JMP', 'BEQ', 'BNE', 'LW',
             'SW', 'NOP', 'CMP', 'INC', 'DEC', 'MULTIPLY', 'DIVIDE', 'SUBTRACT',
             'SHIFT'}
STANDARDS = {'IEEE', 'ASCII', 'EBCDIC', 'ARM', 'SPARC', 'ANSI', 'BCH',
             'VLIW', 'MIPS', 'VAX', 'PDP'}


def clean(chunk):
    """A section's visible prose: tags gone, entities resolved, diagrams dropped."""
    chunk = SVG_RE.sub(' ', chunk)
    chunk = DROP_RE.sub(' ', chunk)
    chunk = TAG_RE.sub(' ', chunk)
    chunk = _h.unescape(chunk)
    chunk = chunk.replace('−', '-').replace(' ', ' ')
    # A meaning split across a line break must read as one phrase, or the audit
    # misses that "millions of instructions per second" is taught at all.
    return re.sub(r'\s+', ' ', chunk)


def sections(html):
    """The book in reading order: [(anchor id, cleaned text), ...]."""
    marks = [(m.group(1), m.start()) for m in ANCHOR_RE.finditer(html)]
    out = []
    for i, (mid, pos) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(html)
        out.append((mid, clean(html[pos:end])))
    return out


def first_positions(secs):
    """For every glossary acronym: (first taught, first used, first-use section).

    A position is (section index, character offset) so it compares in reading
    order across the whole book. The acronym is matched case-sensitively -- 'EX'
    is a stage, 'ex' is nothing -- while its meaning is matched case-insensitively,
    since a heading may capitalise it.
    """
    use_re = {a: re.compile(r'\b' + re.escape(a) + r'\b') for a in GLOSSARY}
    intro_re = {a: re.compile(exp, re.I) for a, exp in GLOSSARY.items()}
    taught, used, used_sec = {}, {}, {}
    for sidx, (mid, text) in enumerate(secs):
        for a in GLOSSARY:
            if a not in taught:
                m = intro_re[a].search(text)
                if m:
                    taught[a] = (sidx, m.start())
            if a not in used:
                m = use_re[a].search(text)
                if m:
                    used[a] = (sidx, m.start())
                    used_sec[a] = mid
    return taught, used, used_sec


def discover_terms(secs):
    """Every token the book itself typesets as a defined acronym.

    Two typographies say "this is a term I am defining": `Expansion (ACRO)` and
    `ACRO (expansion...)`. Whatever the book flags this way, the glossary must
    know about, or the audit is measuring against a list that has fallen behind.
    """
    full = ' '.join(t for _, t in secs)
    found = set(re.findall(r'\(\s*([A-Z][A-Za-z0-9]*[A-Z0-9])\s*\)', full))
    found |= set(re.findall(r'\b([A-Z][A-Z0-9]{1,})\b\s*\([a-z]', full))
    return found


def is_ignorable(tok):
    """Not an undefined course term: a number, notation, opcode, or known name."""
    if tok in GLOSSARY or tok in ASSUMED or tok in OPERATORS:
        return True
    if tok in MNEMONICS or tok in STANDARDS:
        return True
    if re.fullmatch(r'[0-9A-F]+H?', tok) and (any(c.isdigit() for c in tok)
                                              or tok.endswith('H')):
        return True                       # hex literal, e.g. FF4A, C3E22000H, D6H
    if re.fullmatch(r'[A-F]{2,6}', tok):
        return True                       # pure-letter hex value, e.g. FF, AE, EBB,
                                          # which are MCQ answer options in the number
                                          # section (the inline "(a) FF (b) FE" layout
                                          # makes each look like a defined acronym)
    if re.fullmatch(r'[A-D]{2,4}', tok):
        return True                       # Boolean product / register, e.g. AB, ABC
    if re.fullmatch(r'R\d+', tok):
        return True                       # a register operand in an example, e.g. R1
    if re.fullmatch(r'[QI]\d+', tok):
        # A label, not an acronym. "Q1(a)" and "I2 (forwarding covers this)" both match
        # the ACRO(expansion) typography by accident: Q numbers a question and I numbers
        # an instruction in a pipeline listing. Neither is a term anyone must define.
        return True
    return False


def report(html):
    secs = sections(html)
    order = [mid for mid, _ in secs]
    taught, used, used_sec = first_positions(secs)

    untaught, before, in_mock = [], [], []
    for a in GLOSSARY:
        if a not in used:
            continue                       # the book never uses it; nothing owed
        if a not in taught:
            untaught.append(a)
            continue
        # Judged by section, as the Java and Python audits are: a unit that
        # defines a term it opened with is self-contained, and the reader is
        # never sent to another page. Only a meaning taught in a LATER section
        # than its first use leaves a real gap.
        if used[a][0] < taught[a][0]:
            before.append((a, order[used[a][0]], order[taught[a][0]]))
        if used_sec[a].startswith('MOCK'):
            in_mock.append((a, used_sec[a]))

    unlisted = sorted(t for t in discover_terms(secs) if not is_ignorable(t))

    used_n = sum(1 for a in GLOSSARY if a in used)
    print(f'FIRST-USE AUDIT: {used_n} of {len(GLOSSARY)} glossary acronyms used '
          f'across {len(order)} sections')
    ok = True

    if before:
        ok = False
        print(f'  x {len(before)} used before their meaning is written out:')
        for a, u, t in before:
            print(f'      {a:6} first used in {u}, first taught only in {t}')
    else:
        print('  . every acronym used is written out at or before its first use')

    if untaught:
        ok = False
        print(f'  x {len(untaught)} used but their meaning is written out nowhere, so '
              f'the reader cannot look them up:')
        for a in untaught:
            print(f'      {a:6} used in {used_sec[a]}')
    else:
        print('  . every acronym used has its meaning written out somewhere')

    if in_mock:
        ok = False
        print(f'  x {len(in_mock)} appear first in a mock paper, so the reader is '
              f'examined on what was never shown:')
        for a, mid in in_mock:
            print(f'      {a:6} first appears in {mid}')
    else:
        print('  . no acronym makes its first appearance in a mock paper')

    if unlisted:
        ok = False
        print(f'  x {len(unlisted)} typeset as defined acronyms but missing from the '
              f'glossary, so they are used but never audited:')
        for t in unlisted:
            print(f'      {t}')
    else:
        print('  . every acronym the book defines is in the glossary and audited')

    return ok


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'full_manual.html')
    sys.exit(0 if report(open(src, encoding='utf-8').read()) else 1)
