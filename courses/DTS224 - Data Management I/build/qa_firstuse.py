"""Teach before use: every notation is introduced before the reader meets it.

    cd build && python qa_firstuse.py [full_manual.html]

The promise is "zero external sources": a reader should never need a lecturer, a
website, or the official documentation. A symbol or abbreviation the book uses but
never introduces breaks that promise, and so does one the book only introduces in a
mock, because a mock tests what the modules taught and must teach nothing new.

An earlier version of this gate read Python keywords and methods and was useless for
a course whose notation is SQL, relational algebra, and ER/EER drawing. This version
is COURSE-AGNOSTIC. It does not try to guess what a notation is (a database course
writes STAFF and SELECT in capitals, so an all-caps sweep is all noise). Instead the
author DECLARES the notations the manual leans on, exactly as the coverage gate has
the author declare the priority papers, and this gate proves two things about each:

  1. It is INTRODUCED. Its intro cue matches somewhere in the book. A missing intro is
     the classic escape: an abbreviation used in schema listings but never spelled out
     (PK, FK), or a term promised in a unit's objectives but never actually defined.
  2. It is introduced OUTSIDE a mock. If the first place the intro cue matches is a mock
     paper, the reader is examined on what was never taught. This is the escape that
     caught "subtype discriminator": defined only inside a mock answer.

It also WARNS (does not fail) when a notation is used, in an earlier section, before the
section that introduces it. That one is advisory because a preface legitimately previews
terms it has not defined yet; the author reads the warning and judges.

Declaring the list is the point. Enumerating every symbol and abbreviation the manual
uses is the forcing function that makes "teach before use" a default, not an afterthought.
A NEW COURSE ports this file and rewrites NOTATIONS for its own notation set.
"""
import re
import sys

# ---- per-course declaration: notation -> the regex that marks its INTRODUCTION ----
# The intro cue must match the real teaching point (a spelled-out abbreviation, a
# definition table row, a bolded term), NOT a promissory mention in an objectives list.
# Keep cues tolerant of markup but specific enough that they cannot match by accident.
NOTATIONS = {
    # abbreviations: the intro is the expansion, written once as "Words (ABBR)"
    'PK':   r'[Pp]rimary key \(PK\)',
    'FK':   r'[Ff]oreign key \(FK\)',
    'ER':   r'entity-relationship \(E-?R\)',
    'ERD':  r'\(ERD\)',
    'EER':  r'[Ee]nhanced E',
    'DDL':  r'\(DDL\)',
    'DML':  r'\(DML\)',
    'DBA':  r'\(DBA\)',
    'DBMS': r'\(Database Management System\)',
    'FD':   r'[Ff]unctional dependenc',
    'BCNF': r'Boyce.?Codd',
    '1NF':  r'[Ff]irst normal form',
    '2NF':  r'[Ss]econd normal form',
    '3NF':  r'[Tt]hird normal form',
    # relational-algebra symbols: the intro is the operation named beside the symbol
    '&#963;':  r'&#963; \(sigma\)',
    '&#960;':  r'&#960; \(pi\)',
    '&#8746;': r'[Uu]nion.{0,60}&#8746;',
    '&#8722;': r'[Ss]et difference.{0,60}&#8722;',
    '&#215;':  r'Cartesian product.{0,60}&#215;',
    '&#8904;': r'[Jj]oin.{0,60}&#8904;',
    '&#961;':  r'rename.{0,60}&#961;',
    '&#247;':  r'division.{0,60}&#247;',
    # notation and terms the paper asks for by name
    '&rarr;':  r'written A &rarr; B',                       # the FD arrow
    'subtype discriminator': r'<b>subtype discriminator</b>',
}

# how each notation is spelled where it is USED (for the ordering warning). Defaults to
# a word-boundary match on the token; symbols and phrases match literally.
MARKER = re.compile(r'<!-- =====\s*(\S+?)\s*===== -->')


def chunks(html):
    """The book as ordered (name, start, end) content parts, by the assembler's markers."""
    marks = [(m.group(1), m.start()) for m in MARKER.finditer(html)]
    out = []
    for i, (name, pos) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(html)
        out.append((name, pos, end))
    return out


def chunk_of(pos, parts):
    for idx, (name, start, end) in enumerate(parts):
        if start <= pos < end:
            return idx, name
    return -1, '(front matter)'


def mask(html):
    """Blank out spans that do not count as a USE: figures, code, objectives lists.

    Replace with spaces of equal length so every other offset is preserved.
    """
    def blank(m):
        return ' ' * (m.end() - m.start())
    for pat in (r'<svg\b.*?</svg>', r'<pre\b.*?</pre>',
                r'<p class="lo">.*?</p>'):
        html = re.sub(pat, blank, html, flags=re.S)
    return html


def use_pattern(tok):
    if re.fullmatch(r'[A-Z0-9]+', tok):          # an abbreviation: whole word only
        return re.compile(r'\b' + re.escape(tok) + r'\b')
    return re.compile(re.escape(tok))            # a symbol or phrase: literal


def report(html):
    parts = chunks(html)
    mocks = {i for i, (n, _, _) in enumerate(parts) if n.lower().startswith('mock')}
    used = mask(html)

    problems, warnings, ok_intro = [], [], []
    for tok, cue in NOTATIONS.items():
        m = re.search(cue, html, re.S)
        if not m:
            problems.append(f'{tok!r} is never introduced (cue /{cue}/ matched nothing) '
                            f'- a reader meets it with nowhere to look it up')
            continue
        i_idx, i_name = chunk_of(m.start(), parts)
        if i_idx in mocks:
            problems.append(f'{tok!r} is first introduced inside {i_name}, a mock: the '
                            f'reader is examined on what the modules never taught')
            continue
        ok_intro.append((tok, i_name))
        # advisory: is it used in an earlier part than the one that introduces it?
        # A preface (front.html) legitimately previews terms, so it is not a "use".
        um = use_pattern(tok).search(used)
        if um and um.start() < m.start():
            u_idx, u_name = chunk_of(um.start(), parts)
            if u_idx != -1 and u_idx < i_idx and u_name.lower() != 'front.html':
                warnings.append(f'{tok!r} is used in {u_name} but not introduced until '
                                f'{i_name}')

    print(f'FIRST-USE AUDIT: {len(NOTATIONS)} declared notations checked against the '
          f'assembled book')
    ok = not problems
    if problems:
        print(f'  x {len(problems)} not taught before use:')
        for p in problems:
            print('      ' + p)
    else:
        print(f'  . every declared notation is introduced before use, none first in a mock')
    for w in warnings:
        print('  ? ' + w)
    return ok


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'full_manual.html'
    sys.exit(0 if report(open(src, encoding='utf-8').read()) else 1)
