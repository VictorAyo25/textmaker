"""qa_reference.py -- the reference at the back must describe the book in front of it.

    cd build && python assemble.py     # writes full_manual.html
    python qa_reference.py             # then audit it

A reference section is a promise with two halves, and both rot silently.

  1. **Everything the book uses is in it.** The reader meets `newLine()` on page 190,
     forgets it, and turns to the back. If it is not there, the reference is a
     decoration and the "no external sources" promise has a hole in it exactly where
     the reader went looking.
  2. **Nothing in it is unused.** An entry for an API this book never touches is not
     generosity, it is a claim the book never made and cannot support: the reader has
     no page to turn to, no listing that ran it, and no reason to trust the entry.

Neither half survives being asserted. Both are cheap to measure, because
qa_firstuse.py already knows exactly which APIs and keywords the listings use, and it
knows it from the code rather than from anybody's memory. So this gate is the same
inventory, compared against what the reference actually documents.

How an entry is declared
------------------------
A row of a `<table class="data ref">` whose first cell is a `<code>`. That is the
whole contract:

    <tr><td><code>Math.pow(a, b)</code></td><td>a to the power b, as a double</td></tr>

Nothing else in the reference counts, so the prose around the tables is free to
mention whatever it likes without accidentally satisfying the audit.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import qa_firstuse as q

# a reference table, and the first <code> of each of its rows
REF_TABLE_RE = re.compile(r'<table class="data ref">(.*?)</table>', re.S)
ROW_RE = re.compile(r'<tr>(.*?)</tr>', re.S)
FIRST_CODE_RE = re.compile(r'<code>(.*?)</code>', re.S)

# the sections that make up the reference
REF_SEC_RE = re.compile(r'^R\d')


def entry_names(text):
    """Every spelling an entry offers, so a lookup can find it by any of them.

    `Math.pow(a, b)` is offered as Math.pow and as pow; `substring(from, to)` as
    substring. The parameter list is documentation, not identity.
    """
    t = q.unhtml(text).strip()
    t = re.sub(r'\(.*$', '', t)          # drop the parameter list
    t = re.sub(r'^import\s+', '', t)     # `import javax.swing.JOptionPane;`
    t = t.rstrip(';').strip()            # ... whose tail was `JOptionPane;`, not JOptionPane
    t = t.replace('new ', '').strip()
    t = t.lstrip('.')
    out = {t}
    if '.' in t:
        out.add(t.rsplit('.', 1)[-1])    # Math.pow -> pow, javax.swing.JOptionPane -> JOptionPane
    return {n for n in out if n}


def documented(html):
    """Everything the reference declares, and the raw first-cell text of each row."""
    names, rows = set(), []
    for sec_id, start, end in q.sections(html):
        if not REF_SEC_RE.match(sec_id):
            continue
        for tbl in REF_TABLE_RE.finditer(html[start:end]):
            for row in ROW_RE.finditer(tbl.group(1)):
                m = FIRST_CODE_RE.search(row.group(1))
                if not m:
                    continue            # a header row, or prose: not an entry
                raw = q.unhtml(m.group(1)).strip()
                rows.append((raw, sec_id))
                names |= entry_names(m.group(1))
    return names, rows


def wanted(api):
    """Every spelling that would satisfy a use of `api`."""
    if api.startswith('new '):
        return {api[4:]}
    if api.startswith('.'):
        return {api[1:-2]}
    base = api[:-2] if api.endswith('()') else api
    out = {base}
    if '.' in base:
        out.add(base.rsplit('.', 1)[-1])
    return out


def report(html):
    first_code, _, _, order = q.scan(html)
    names, rows = documented(html)

    used_apis = sorted(k for k in first_code if k not in q.KEYWORDS)
    used_kw = sorted(k for k in first_code if k in q.KEYWORDS)

    print(f'REFERENCE AUDIT: {len(rows)} entries against {len(used_apis)} APIs and '
          f'{len(used_kw)} keywords the listings actually use')
    ok = True

    if not rows:
        print('  x the reference declares no entries at all. Entries are rows of a '
              '<table class="data ref"> whose first cell is a <code>. If that markup '
              'changed, this gate is now checking nothing while reporting a pass.')
        return False

    missing = [a for a in used_apis if not (wanted(a) & names)]
    if missing:
        ok = False
        print(f'\n  x {len(missing)} used by the book but absent from the reference, so '
              f'a reader who looks them up finds nothing:')
        for a in missing:
            print(f'      {a:30} used in {first_code[a]}')
    else:
        print('  . every API the listings use is documented in the reference')

    missing_kw = [k for k in used_kw if k not in names]
    if missing_kw:
        ok = False
        print(f'\n  x {len(missing_kw)} keywords used but not in the keyword index:')
        for k in missing_kw:
            print(f'      {k:30} used in {first_code[k]}')
    else:
        print('  . every keyword the listings use is in the keyword index')

    # The other direction: an entry for something the book never touches.
    #
    # "Touches" has to mean more than "runs in a listing". The book handles
    # ArrayIndexOutOfBoundsException by discussing it at length and never once writing
    # its name in code, and an entry for it is earned. So a mention in the PROSE
    # counts too.
    #
    # But only prose from outside the reference. Every entry's own row is prose, and
    # its first cell is the very <code> being checked, so counting the reference's own
    # text would let all 142 entries vouch for themselves and this rule would pass on
    # anything, forever, including a table of pure invention.
    all_used = set()
    for a in list(used_apis) + list(used_kw):
        all_used |= wanted(a)
    body = []
    for sec_id, start, end in q.sections(html):
        if not REF_SEC_RE.match(sec_id):
            body.append(q.unhtml(html[start:end]))
    body = ' '.join(body)
    dead = sorted({raw for raw, _ in rows
                   if not (entry_names(raw) & all_used)
                   and not any(re.search(r'(?<![\w.])%s(?![\w])' % re.escape(n), body)
                               for n in entry_names(raw))})
    if dead:
        ok = False
        print(f'\n  x {len(dead)} documented but never used anywhere in the book, so the '
              f'reference is making promises the book does not keep:')
        for raw in dead:
            print(f'      {raw}')
    else:
        print('  . the reference documents nothing the book never uses')

    return ok


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'full_manual.html')
    if not os.path.exists(src):
        raise SystemExit(f'no {src}: run assemble.py first')
    if not report(io.open(src, encoding='utf-8').read()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
