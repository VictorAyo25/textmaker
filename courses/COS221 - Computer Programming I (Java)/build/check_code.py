"""check_code.py — compile and run EVERY code block in the manual.

PHY121's rule was "recompute every number independently before you write it
down". For a programming course the same rule reads: **every snippet is compiled
and run, and every claimed output is captured from a real JVM.** A printed output
that was never executed is not a typo, it is a wrong constant, and a reader who
trusts it and cannot reproduce it loses faith in the whole book.

    python check_code.py            # all content
    python check_code.py module1    # one section

How a CODE box declares its contract, in the HTML:

    <pre class="src" data-run="Hello">        compile as Hello.java, run it, and
                                              compare stdout with the .out block
                                              that follows in the same box
    <pre class="src" data-run="Hello" data-stdin="4&#10;7">   feed stdin
    <pre class="src" data-compile="Broken">   must FAIL to compile (a planted bug);
                                              the gate asserts the failure and, if
                                              data-error is given, that the compiler
                                              message contains it
    <pre class="src" data-frag="1">           a fragment, not a whole program: wrapped
                                              in a class+main before compiling, so it
                                              still has to be valid Java
    <pre class="src" data-nocheck="why">      excluded, with the reason recorded here
                                              and printed in the report

Anything without one of those attributes is an ERROR: silence must never be the
way a snippet escapes checking.
"""
import html as htmllib
import io, os, re, shutil, subprocess, sys, tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

PRE_RE = re.compile(r'<pre class="src(?P<cls>[^"]*)"(?P<attrs>[^>]*)>(?P<body>.*?)</pre>', re.S)
OUT_RE = re.compile(r'<pre class="out"[^>]*>(?P<body>.*?)</pre>', re.S)
ATTR_RE = re.compile(r'data-(?P<k>[a-z]+)="(?P<v>[^"]*)"')


class _Lines(HTMLParser):
    """Pull one Java source line out of each <span class="l">.

    A regex cannot do this: a line's own </span> is indistinguishable from the
    </span> of a syntax role nested inside it (<span class="k">public</span>),
    so a non-greedy match truncates every coloured line at its first nested tag
    and the result does not compile. Track depth instead.
    """
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines = []
        self.depth = 0      # 0 = outside a line span
        self.buf = None

    def handle_starttag(self, tag, attrs):
        if tag != 'span':
            return
        # A duplicate class attribute (class="l" class="bad") is invalid HTML that
        # browsers resolve by keeping the FIRST and dropping the rest, while
        # dict(attrs) keeps the LAST. That disagreement is silent and vicious: the
        # span stops looking like a line, this parser drops it, and the listing
        # compiles and runs MINUS one line, quietly changing its output. It has
        # happened twice. Refuse it instead of guessing.
        if sum(1 for k, _ in attrs if k == 'class') > 1:
            raise ValueError(f'duplicate class attribute in <span {attrs}>: '
                             f'write class="l bad", not class="l" class="bad"')
        cls = dict(attrs).get('class', '').split()
        if self.depth == 0:
            if 'l' in cls:
                self.depth = 1
                self.buf = []
        else:
            self.depth += 1      # a nested role span

    def handle_endtag(self, tag):
        if tag != 'span' or self.depth == 0:
            return
        self.depth -= 1
        if self.depth == 0:
            self.lines.append(''.join(self.buf))
            self.buf = None

    def handle_data(self, data):
        if self.depth:
            self.buf.append(data)


def source_of(pre_body):
    """Reconstruct the Java source from a listing.

    Each line is <span class="l">...</span>; syntax roles nest inside and are
    dropped. convert_charrefs unescapes entities, without which every &amp;&amp;
    stays &amp;&amp; and nothing compiles.
    """
    p = _Lines()
    p.feed(pre_body)
    p.close()
    if p.depth != 0:
        raise ValueError('unbalanced <span> in listing')
    if not p.lines:
        raise ValueError('listing has no <span class="l"> lines')
    return '\n'.join(p.lines)


def claimed_output(box_html, after):
    m = OUT_RE.search(box_html, after)
    if not m:
        return None
    body = re.sub(r'<span class="olabel">.*?</span>', '', m.group('body'), flags=re.S)
    return htmllib.unescape(re.sub(r'<[^>]+>', '', body)).strip('\n')


def norm(s):
    return '\n'.join(line.rstrip() for line in s.strip().replace('\r\n', '\n').split('\n'))


def run_one(src, cls, stdin, workdir):
    p = os.path.join(workdir, cls + '.java')
    io.open(p, 'w', encoding='utf-8').write(src)
    c = subprocess.run(['javac', '-nowarn', p], cwd=workdir,
                       capture_output=True, text=True, timeout=120)
    if c.returncode != 0:
        return False, c.stderr.strip()
    r = subprocess.run(['java', '-cp', workdir, cls], cwd=workdir,
                       input=(stdin or ''), capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return False, (r.stdout + r.stderr).strip()
    return True, r.stdout


def check_file(name, results):
    path = os.path.join(CONTENT, name + '.html')
    doc = io.open(path, encoding='utf-8').read()
    work = tempfile.mkdtemp(prefix='cos221_')
    try:
        for m in PRE_RE.finditer(doc):
            attrs = dict((a.group('k'), htmllib.unescape(a.group('v')))
                         for a in ATTR_RE.finditer(m.group('attrs')))
            where = f'{name}:{doc[:m.start()].count(chr(10)) + 1}'

            if 'nocheck' in attrs:
                results.append(('SKIP', where, attrs['nocheck']))
                continue

            try:
                src = source_of(m.group('body'))
            except ValueError as e:
                results.append(('FAIL', where, str(e)))
                continue

            if 'compile' in attrs:
                cls = attrs['compile']
                ok, msg = run_one(src, cls, None, work)
                if ok:
                    results.append(('FAIL', where,
                                    f'{cls}: declared data-compile (must NOT compile) but it compiled and ran'))
                elif 'error' in attrs and attrs['error'] not in msg:
                    results.append(('FAIL', where,
                                    f'{cls}: failed as intended but the message does not mention '
                                    f'"{attrs["error"]}".\n{msg[:400]}'))
                else:
                    results.append(('OK', where, f'{cls}: fails to compile, as the text claims'))
                continue

            if 'frag' in attrs:
                cls = 'Frag' + re.sub(r'\W', '', where)
                src = (f'public class {cls} {{ public static void main(String[] a) '
                       f'throws Exception {{\n{src}\n}} }}')
                ok, msg = run_one(src, cls, attrs.get('stdin'), work)
                results.append(('OK' if ok else 'FAIL', where,
                                'fragment compiles' if ok else f'fragment does not compile:\n{msg[:400]}'))
                continue

            if 'run' not in attrs:
                results.append(('FAIL', where,
                                'listing declares no contract: add data-run, data-compile, '
                                'data-frag or data-nocheck'))
                continue

            cls = attrs['run']
            ok, got = run_one(src, cls, attrs.get('stdin'), work)
            if not ok:
                results.append(('FAIL', where, f'{cls}: does not compile/run:\n{got[:400]}'))
                continue
            want = claimed_output(doc, m.end())
            if want is None:
                results.append(('WARN', where, f'{cls}: runs, but the box claims no output to check'))
                continue
            if norm(got) == norm(want):
                results.append(('OK', where, f'{cls}: output matches the JVM'))
            else:
                results.append(('FAIL', where,
                                f'{cls}: PRINTED OUTPUT IS WRONG.\n'
                                f'  manual claims: {norm(want)!r}\n'
                                f'  JVM printed  : {norm(got)!r}'))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    if not shutil.which('javac'):
        raise SystemExit('javac not on PATH: the snippet gate cannot run')
    names = sys.argv[1:] or [f[:-5] for f in sorted(os.listdir(CONTENT)) if f.endswith('.html')]
    results = []
    for n in names:
        check_file(n, results)

    for status, where, msg in results:
        if status != 'OK':
            print(f'[{status}] {where}: {msg}')
    n_ok = sum(1 for r in results if r[0] == 'OK')
    n_skip = sum(1 for r in results if r[0] == 'SKIP')
    n_warn = sum(1 for r in results if r[0] == 'WARN')
    n_fail = sum(1 for r in results if r[0] == 'FAIL')
    print(f'\n{len(results)} listings: {n_ok} ok, {n_skip} skipped, {n_warn} warn, {n_fail} FAIL')
    if n_fail:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
