"""qa_firstuse.py — every keyword and API the manual uses, and where it first appears.

    cd build && python assemble.py     # writes full_manual.html
    python qa_firstuse.py              # then audit it

The promise being checked is Victor's: **zero external sources**. A reader must
never need a lecturer, a website, or Oracle's documentation. Asserting that is
easy and worthless; it only means something if it is measured, and it is exactly
the kind of claim that silently rots as a book grows past two hundred pages.

Two rules, and neither survives being asserted:

  1. **Nothing is used without being named.** An API that appears only inside
     code listings and is never written in the prose is a hole: the reader meets
     it, cannot look it up, and has nowhere to go.
  2. **A mock teaches nothing.** A mock paper is a test of what the modules
     taught. So an API whose first appearance in the whole book is inside a mock
     is one the reader is being examined on and was never shown. Same for the
     solved past papers: they answer an exam, they do not introduce Java.

This reads the ASSEMBLED html, not content/*.html, so it sees the book in the
order a reader does. Run assemble.py first.

Deliberately broken code introduces nothing
-------------------------------------------
A `data-compile` listing is a planted bug: the reader is shown code that does not
work so the text can explain why, and the corrected version follows. Counting the
bug as an API's first use is backwards. Those listings are skipped, exactly as
their `data-error` contract says they are not real Java.
"""
import io
import os
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))

PRE_RE = re.compile(r'<pre class="(?P<cls>[^"]*)"(?P<attrs>[^>]*)>(?P<body>.*?)</pre>', re.S)
ANCHOR_RE = re.compile(r'id="sec-([A-Z0-9]+)"')
TAG_RE = re.compile(r'<[^>]+>')
CODE_TAG_RE = re.compile(r'<code>([^<]+)</code>')

KEYWORDS = {
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
    'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
    'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
    'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new',
    'package', 'private', 'protected', 'public', 'return', 'short', 'static',
    'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
    'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null',
}

# Not APIs the reader is owed a card for: they are this book's own example names,
# invented on the page and explained where they are invented. `new Student` is not
# an API the reader must look up; it is a class the listing declares four lines up.
OWN_METHOD_RE = re.compile(
    r'\b(?:public|private|protected|static|final)[\w\s\[\]<>,]*?\b([a-z]\w*)\s*\(')
OWN_CLASS_RE = re.compile(r'\b(?:class|interface|enum)\s+([A-Z]\w*)')


LINE_SPAN_RE = re.compile(r'<span class="l[ "]')
BLOCK_RE = re.compile(r'</?(?:p|div|li|td|th|tr|pre|h[1-6]|br|caption)\b[^>]*>')


def unhtml(s):
    """Tags out, entities decoded, and line boundaries preserved.

    Getting the boundaries right matters twice, in opposite directions.

    Delete the tags outright and every listing line welds to the next, because a
    listing is `<span class="l">line</span>` repeated with no separator: the end of
    one comment runs into the next line as "...the very top of the
    fileJOptionPane.showMessageDialog(", and the \\b in every pattern below then
    cannot see JOptionPane at all. That made this audit report JOptionPane as first
    met in a solved paper when F.11 plainly introduces it, and it hid every
    `class Foo` whose declaration happened to follow a comment.

    Replace *every* tag with a space and the opposite breaks: syntax colouring
    wraps type names, so `<span class="t">Double</span>.parseDouble(` becomes
    "Double .parseDouble(" and the Type.method() pattern stops matching, inventing
    a bare .parseDouble() that no prose names.

    So: break at line and block boundaries, and nowhere else.
    """
    s = LINE_SPAN_RE.sub(r'\n\g<0>', s)
    s = BLOCK_RE.sub('\n', s)
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
    """Keywords and library APIs used in a chunk of Java."""
    found = set()
    for kw in re.findall(r'\b([a-z]+)\b', code):
        if kw in KEYWORDS:
            found.add(kw)
    # Type.method(...)  ->  a static call, or a call on a class like System.out
    for typ, meth in re.findall(r'\b([A-Z]\w*)\.(\w+)\s*\(', code):
        found.add(f'{typ}.{meth}()')
    # System.out.println is spelled through a field; catch it explicitly
    for meth in re.findall(r'\bSystem\.out\.(\w+)\s*\(', code):
        found.add(f'System.out.{meth}()')
    # .method(...) on anything else
    for meth in re.findall(r'(?<!\w)\.(\w+)\s*\(', code):
        found.add(f'.{meth}()')
    # a bare constant like Math.PI, no brackets
    for typ, fld in re.findall(r'\b([A-Z]\w*)\.([A-Z_]{2,})\b', code):
        found.add(f'{typ}.{fld}')
    for t in re.findall(r'\bnew\s+([A-Z]\w*)\s*[\(\[]', code):
        found.add(f'new {t}')
    # An import contributes the CLASS, not the import line. Tracking the line makes
    # `import java.io.PrintWriter;` a different thing from PrintWriter, so a module
    # that teaches PrintWriter behind `import java.io.*;` looks like it never taught
    # it, and the audit blames the solved paper that happens to import it by name.
    # What the reader must have met is the class. A wildcard names no class.
    for imp in re.findall(r'\bimport\s+([\w.*]+)\s*;', code):
        cls = imp.rsplit('.', 1)[-1]
        if cls != '*':
            found.add(cls)
    return found


def own_names(html):
    """Every method and class this book declares in its own listings."""
    methods, classes = set(), set()
    for m in PRE_RE.finditer(html):
        if 'src' not in m.group('cls'):
            continue
        body = unhtml(m.group('body'))
        methods |= set(OWN_METHOD_RE.findall(body))
        classes |= set(OWN_CLASS_RE.findall(body))
    return methods, classes


def scan(html):
    secs = sections(html)
    mine, my_classes = own_names(html)

    first_code = OrderedDict()   # api -> section of its first use in real code
    first_any = OrderedDict()    # api -> section the reader first MEETS it
    prose_names = set()
    prose_text = []              # the raw words, so "the substring method" counts

    for mid, start, end in secs:
        chunk = html[start:end]

        for m in PRE_RE.finditer(chunk):
            if 'src' not in m.group('cls'):
                continue
            if 'data-compile' in m.group('attrs'):
                continue                      # a planted bug teaches nothing
            for api in sorted(apis_in(unhtml(m.group('body')))):
                first_code.setdefault(api, mid)
                first_any.setdefault(api, mid)

        prose = PRE_RE.sub(' ', chunk)
        prose_text.append(unhtml(prose))
        here = apis_in(unhtml(prose))
        # Prose names an API inside <code> and usually without its brackets
        # ("the substring method"), so record every spelling of it.
        for raw in CODE_TAG_RE.findall(prose):
            t = unhtml(raw).strip()
            base = re.sub(r'\(.*\)$', '', t).lstrip('.')
            for form in (t, t.rstrip('()'), base, base + '()', '.' + base + '()'):
                here.add(form)
        prose_names |= here
        for api in sorted(here):
            first_any.setdefault(api, mid)

    # drop this book's own example names: .evens() and `new Student` are not APIs
    for d in (first_code, first_any):
        for k in list(d):
            if k.startswith('.') and k[1:-2] in mine:
                del d[k]
            elif k.startswith('new ') and k[4:] in my_classes:
                del d[k]

    return first_code, first_any, (prose_names, ' '.join(prose_text)), [m for m, _, _ in secs]


def named_in(api, prose):
    """Is this API written out in the prose, in any spelling a human would use?

    Checked against BOTH the set of names the prose marks up as <code>, and the
    raw prose text: a book that says "wrap it in a BufferedReader" in a sentence
    has named it, even with no <code> tags around it.
    """
    names, text = prose
    def seen(f):
        return f in names or f in text
    if api.startswith('import '):
        return seen(api) or seen(api[7:]) or seen(api[7:].split('.')[-1])
    if api.startswith('new '):
        return seen(api) or seen(api[4:])
    bare = api.rstrip('()').lstrip('.')
    tail = bare.split('.')[-1]
    return any(seen(f) for f in (api, bare, bare + '()', '.' + bare + '()',
                                 tail, tail + '()', '.' + tail + '()'))


def report(html):
    first_code, first_any, prose, order = scan(html)
    # ^S<digit> is a solved-paper section (S.1, S.14). A bare startswith('S')
    # also matches STARTHEREHOWTOUSETHISBOOK, which is the front matter and does
    # teach; that false positive reported every keyword in the book as exam-taught.
    exam_secs = [m for m in order
                 if m.startswith('MOCK') or re.match(r'^S\d', m)]

    undocumented, taught_by_exam = [], []
    for api, mid in first_code.items():
        if not named_in(api, prose):
            undocumented.append((api, mid))
        if first_any.get(api) in exam_secs:
            taught_by_exam.append((api, first_any[api]))

    print(f'FIRST-USE AUDIT: {len(first_code)} distinct keywords and APIs across '
          f'{len(order)} sections')
    ok = True

    if undocumented:
        ok = False
        print(f'\n  x {len(undocumented)} used in code but never named in the prose, so '
              f'the reader has nowhere to look them up:')
        for api, mid in undocumented:
            print(f'      {api:26} first used in {mid}')
    else:
        print('  . every API used in code is named somewhere in the prose')

    if taught_by_exam:
        ok = False
        print(f'\n  x {len(taught_by_exam)} first appear in a solved paper or a mock, '
              f'which test rather than teach:')
        for api, mid in taught_by_exam:
            print(f'      {api:26} first met in {mid}')
    else:
        print('  . nothing is first met in a solved paper or a mock')

    return ok


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'full_manual.html')
    if not os.path.exists(src):
        raise SystemExit(f'no {src}: run assemble.py first')
    if not report(io.open(src, encoding='utf-8').read()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
