"""Every keyword and API the manual uses, and where it first appears.

    cd build && python qa_firstuse.py [full_manual.html]

The promise this checks is "zero external sources": a reader should never need a
lecturer, a website or the official documentation. That means two things, and
neither survives being asserted rather than measured.

  1. Nothing is used without being explained. An API that appears only inside
     code blocks and is never named in the prose is a hole: the reader meets it,
     cannot look it up, and has nowhere to go.
  2. The mock papers teach nothing. A mock is a test of what the modules taught,
     so an API whose first appearance in the whole book is in a mock is an API
     the reader is being examined on and was never shown.

This reads the assembled HTML, not the sources, so it sees the book in the order
a reader does.
"""
import builtins
import keyword
import re
import sys
from collections import OrderedDict

CODE_RE = re.compile(r'<pre class="([^"]*)">(.*?)</pre>', re.S)

# A mock's "identify the error" parts print code that is deliberately wrong. The
# reader is asked to find the fault, and the answer explains it, so such a block
# introduces nothing and must not count as a first use. Q4(b) of Mock One shows
# `surname.lowercase()`, a method that does not exist; without this the audit
# reports it as an API the book uses and never documents, which is the opposite
# of what the question is doing.
BROKEN = 'broken'
ANCHOR_RE = re.compile(r'id="sec-([A-Z0-9]+)"')
TAG_RE = re.compile(r'<[^>]+>')

# Names a reader is not owed a reference card for: they are the reader's own
# choices in the examples, not part of the language.
BUILTIN_NAMES = set(dir(builtins))


def unhtml(s):
    s = TAG_RE.sub('', s)
    for a, b in (('&lt;', '<'), ('&gt;', '>'), ('&amp;', '&'), ('&quot;', '"'),
                 ('&#39;', "'"), ('&middot;', '.'), ('&nbsp;', ' ')):
        s = s.replace(a, b)
    return s


def sections(html):
    """The book in reading order: (anchor id, start, end) per section."""
    marks = [(m.group(1), m.start()) for m in ANCHOR_RE.finditer(html)]
    out = []
    for i, (mid, pos) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(html)
        out.append((mid, pos, end))
    return out


def apis_in(code):
    """Keywords, built-in calls and method calls used in a block of code."""
    found = set()
    for kw in re.findall(r'\b([a-z]+)\b', code):
        if keyword.iskeyword(kw):
            found.add(kw)
    for name in re.findall(r'(?<![\w.])([a-z_][a-z0-9_]*)\s*\(', code):
        if name in BUILTIN_NAMES:
            found.add(name + '()')
    for meth in re.findall(r'\.([a-z_][a-z0-9_]*)\s*\(', code):
        found.add('.' + meth + '()')
    for mod in re.findall(r'(?:^|\n)\s*import\s+([a-z_][a-z0-9_]*)', code):
        found.add('import ' + mod)
    return found


def scan(html):
    secs = sections(html)

    first_code = OrderedDict()   # api -> section of its first use in real code
    first_any = OrderedDict()    # api -> section it is first met in, prose or code
    prose_names = set()          # every api named outside a code block

    for mid, start, end in secs:
        chunk = html[start:end]
        for cls, cb in CODE_RE.findall(chunk):
            if BROKEN in cls:
                continue
            for api in sorted(apis_in(unhtml(cb))):
                first_code.setdefault(api, mid)
                first_any.setdefault(api, mid)

        prose = CODE_RE.sub(' ', chunk)
        here = apis_in(unhtml(prose))
        # Prose names an API in an inline <code> tag and usually without its
        # parentheses ("the strip method"), so record every form of the name.
        for m in re.findall(r'<code>([^<]+)</code>', prose):
            t = unhtml(m).strip()
            base = re.sub(r'\(.*\)$', '', t).lstrip('.')
            for form in (t, t.rstrip('()'), base, base + '()', '.' + base + '()'):
                here.add(form)
        prose_names |= here
        for api in sorted(here):
            first_any.setdefault(api, mid)

    return first_code, first_any, prose_names, [m for m, _, _ in secs]


def named_in(api, prose):
    """Is this API written out anywhere in the prose, in any of its spellings?"""
    if api.startswith('import '):
        return api[7:] in prose or api in prose
    bare = api.rstrip('()').lstrip('.')
    return any(f in prose for f in (api, bare, bare + '()', '.' + bare + '()'))


def report(html):
    first_code, first_any, prose, order = scan(html)
    mock_secs = [m for m in order if m.startswith('MOCK')]

    undocumented, taught_by_mock = [], []
    for api, mid in first_code.items():
        if not named_in(api, prose):
            undocumented.append((api, mid))
        # Judged on where the reader first MEETS it, in prose or in code: a
        # reference table that names an API has taught it, even if no example
        # runs it.
        if first_any.get(api) in mock_secs:
            taught_by_mock.append((api, first_any[api]))

    print(f'FIRST-USE AUDIT: {len(first_code)} distinct keywords and APIs used '
          f'across {len(order)} sections')
    ok = True
    if undocumented:
        ok = False
        print(f'  x {len(undocumented)} used in code but never named in prose, so the '
              f'reader has nowhere to look them up:')
        for api, mid in undocumented:
            print(f'      {api:22} first used in {mid}')
    else:
        print('  . every API used in code is named in the prose somewhere')

    if taught_by_mock:
        ok = False
        print(f'  x {len(taught_by_mock)} appear first in a mock paper, so the reader is '
              f'examined on what was never taught:')
        for api, mid in taught_by_mock:
            print(f'      {api:22} first appears in {mid}')
    else:
        print('  . no API makes its first appearance in a mock paper')
    return ok


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'full_manual.html'
    sys.exit(0 if report(open(src, encoding='utf-8').read()) else 1)
