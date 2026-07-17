"""hl.py — turn a real .java file into the manual's listing markup.

Why this exists
---------------
Every listing in this book is written as hand-rolled markup:

    <span class="l"><span class="k">public class</span> <span class="t">X</span> {</span>

Hand-writing that is slow and, worse, it is *quietly* dangerous. Writing
`class="l" class="bad"` instead of `class="l bad"` produces a duplicate class
attribute: browsers keep the first, `dict(attrs)` keeps the last, so the line
vanishes from the compiled source and the listing runs MINUS one line, silently
changing its output. That bug bit four separate times before check_code.py
learned to refuse it.

The gate refusing a bug is good. Not being able to write the bug is better.
So: author the Java as a real .java file, compile and run it, and let this
script emit the markup. The source in the book is then, by construction, the
source that ran.

Usage
-----
    python hl.py Foo.java --run Foo
    python hl.py Bad.java --compile Bad --error "has private access"
    python hl.py Frag.java --frag
    python hl.py Foo.java --run Foo --stdin "4\n7"

Marking a line
--------------
Put /*@good*/ or /*@bad*/ anywhere on the line. The marker is stripped from the
emitted source (and it is a comment, so it never reaches javac either):

    double sum = 0;   /*@good*/ // fix 2      ->  <span class="l good">...

Conventions this script follows, because the existing 100+ listings do
-----------------------------------------------------------------------
  * `System` is never type-spanned. It is a class, but the book has always left
    it plain, and consistency across the book beats pedantry inside one file.
  * Keywords -> .k, capitalised identifiers -> .t, strings/chars -> .s,
    comments -> .c, everything else plain.
"""
import argparse
import html
import io
import re
import sys

KEYWORDS = {
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
    'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
    'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
    'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new',
    'package', 'private', 'protected', 'public', 'return', 'short', 'static',
    'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
    'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null',
    'var', 'record', 'yield',
}

# Capitalised identifiers that the book leaves plain. See the module docstring.
NOT_A_TYPE = {'System'}

TOKEN = re.compile(r'''
    (?P<c>//[^\n]*|/\*.*?\*/)
  | (?P<s>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<w>[A-Za-z_$][A-Za-z0-9_$]*)
  | (?P<o>.)
''', re.X | re.S)

MARKER = re.compile(r'\s*/\*@(good|bad)\*/')


def classify(kind, text):
    if kind == 'c':
        return 'c'
    if kind == 's':
        return 's'
    if kind == 'w':
        if text in KEYWORDS:
            return 'k'
        if text[0].isupper() and text not in NOT_A_TYPE:
            return 't'
    return None


def spans_for(line):
    """Tokenise one line into (css_class_or_None, text) runs, merging neighbours."""
    runs = []
    for m in TOKEN.finditer(line):
        kind = m.lastgroup
        text = m.group()
        cls = classify(kind, text)
        if runs and runs[-1][0] == cls:
            runs[-1][1] += text
        else:
            runs.append([cls, text])
    out = []
    for cls, text in runs:
        esc = html.escape(text, quote=False)
        out.append(f'<span class="{cls}">{esc}</span>' if cls else esc)
    return ''.join(out)


def markup(src):
    lines = []
    for raw in src.replace('\r\n', '\n').rstrip('\n').split('\n'):
        mark = MARKER.search(raw)
        cls = 'l'
        if mark:
            cls = 'l ' + mark.group(1)
            raw = MARKER.sub('', raw)
        lines.append(f'<span class="{cls}">{spans_for(raw)}</span>')
    return ''.join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('java')
    ap.add_argument('--run')
    ap.add_argument('--compile')
    ap.add_argument('--error')
    ap.add_argument('--frag', action='store_true')
    ap.add_argument('--stdin')
    ap.add_argument('--nocheck')
    a = ap.parse_args()

    src = io.open(a.java, encoding='utf-8').read()

    attrs = ''
    if a.run:
        attrs += f' data-run="{a.run}"'
    if a.compile:
        attrs += f' data-compile="{a.compile}"'
    if a.error:
        attrs += f' data-error="{html.escape(a.error, quote=True)}"'
    if a.frag:
        attrs += ' data-frag="1"'
    if a.stdin:
        enc = a.stdin.replace('\\n', '&#10;')
        attrs += f' data-stdin="{enc}"'
    if a.nocheck:
        attrs += f' data-nocheck="{html.escape(a.nocheck, quote=True)}"'
    if not attrs:
        sys.exit('hl.py: a listing must declare a contract '
                 '(--run/--compile/--frag/--nocheck)')

    sys.stdout.write(f'<pre class="src"{attrs}>{markup(src)}</pre>\n')


if __name__ == '__main__':
    main()
