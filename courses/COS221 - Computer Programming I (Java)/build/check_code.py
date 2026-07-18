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
    <pre class="src" data-frag="1">           loose statements: wrapped in a class+main
                                              before compiling, so they still have to
                                              be valid Java
    <pre class="src" data-member="1">          a method declaration on its own: wrapped
                                              in a class BODY, since Java has no nested
                                              methods and data-frag would make it a
                                              syntax error rather than a check
    <pre class="src" data-question="M.7">     a mock/exam question: it runs, but its
                                              output is WITHHELD on purpose, because
                                              printing it would be printing the answer.
                                              The gate runs it anyway and then proves
                                              the identical source is output-checked in
                                              the named solution section.
    <pre class="src" data-nocheck="why">      excluded, with the reason recorded here
                                              and printed in the report

Anything without one of those attributes is an ERROR: silence must never be the
way a snippet escapes checking.

Why data-question has to exist
------------------------------
A mock paper is the one place the book shows a program and must NOT show what it
prints: the output is the question. But "no output block" is exactly what a
forgotten output block looks like, and data-run with nothing to compare against
only WARNs. So the two cases were indistinguishable, and the honest one was
indistinguishable from the careless one.

Worse, the obvious workaround is worse than the problem: mark the question
data-nocheck and the paper's copy of the code is never compiled at all. The mock
would then be the only unverified code in a book whose whole claim is that every
listing ran, and it would be unverified in the place a reader is most exposed,
sitting a timed paper with no way to check.

So data-question keeps both halves. It compiles and runs the question's code, and
it requires the answer to exist: every line of the question must reappear, in
order, inside some data-run listing whose output IS checked against a real JVM.
Edit one line of the answer and the gate reports that the answer no longer answers
the question that was asked.

The test is an ordered line-subsequence, not equality, because of the file
questions. When a question's program writes a file and prints nothing, its answer
is the file's bytes, and the only way to show those honestly is to run the same
writer and read the file back. The solution's listing is therefore the question's
program with verification lines threaded through it. Equality would reject the one
pattern that proves a file question; a subsequence still pins every line the
question actually asked about.
"""
import html as htmllib
import io, os, re, shutil, subprocess, sys, tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

PRE_RE = re.compile(r'<pre class="src(?P<cls>[^"]*)"(?P<attrs>[^>]*)>(?P<body>.*?)</pre>', re.S)
OUT_RE = re.compile(r'<pre class="out"[^>]*>(?P<body>.*?)</pre>', re.S)
ATTR_RE = re.compile(r'data-(?P<k>[a-z]+)="(?P<v>[^"]*)"')

# Every <pre> in the book must be one of these three, and the reason is that this
# gate only *sees* class="src...". Invent a fourth class and the snippet inside it
# escapes checking completely AND renders unstyled, because manual.css only styles
# these. Both failures are silent. It happened: a class="sig" skeleton slipped
# through both, so the vocabulary is now closed and enforced.
ANY_PRE_RE = re.compile(r'<pre class="(?P<cls>[^"]*)"')
ALLOWED_PRE = {'src', 'src nonum', 'out'}

# No code line may be wider than the panel it renders in. This is the cheap,
# pre-render half of the shrink guard (MANUAL_METHODOLOGY 2b): Chromium scales the
# WHOLE book down to fit its widest box, so one long line shrinks every page's body
# font, silently. The rendered-size check in qa.py is the definitive backstop; this
# one names the file and line before a render is even taken. 87 chars was measured
# to sit inside the panel here; 88 is the ceiling, and the book shipped once at 92.9%
# on two 99-char lines. Re-measure if the code font, margins or gutter change.
MAX_COL = 88


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


def wrap(src, cls, mode):
    """Make a compilable program out of a listing that is not one.

    Two shapes, because the papers use two. `frag` is loose statements, which belong
    inside main. `member` is a method declaration, which does NOT: Java has no nested
    methods, so wrapping `public static int f(int n) {...}` in a main is a syntax
    error rather than a check. It belongs in the class body instead. The dry-run
    questions on both papers are always method-shaped, so without `member` the only
    way to gate them is to not gate them.
    """
    if mode == 'frag':
        return (f'public class {cls} {{ public static void main(String[] a) '
                f'throws Exception {{\n{src}\n}} }}')
    return (f'public class {cls} {{\n{src}\n'
            f'public static void main(String[] a) throws Exception {{ }} }}')


def code_lines(src):
    """The lines of a listing that carry meaning, for matching a question to its answer.

    Blank lines and indentation go: a solution is free to re-space the code it is
    answering. Nothing else is normalised, so a changed literal or a renamed
    variable still counts as a different line, which is the point.
    """
    return [ln.strip() for ln in norm(src).split('\n') if ln.strip()]


def is_subsequence(need, have):
    it = iter(have)
    return all(ln in it for ln in need)


def run_one(src, cls, stdin, workdir):
    """Compile and run one listing in a directory of its own.

    Per-listing isolation is not tidiness, it is correctness. Listings that touch
    files must not see each other's leftovers: a file-writing listing created
    output.txt, and a later listing whose whole point was "output.txt does not
    exist" then found it sitting there and printed its contents instead of its
    catch block. The book would have promised output that a reader running that
    one program in a fresh folder could never reproduce.

    Every listing in this book is a standalone program. It gets a standalone
    world.
    """
    box = tempfile.mkdtemp(prefix='l_', dir=workdir)
    p = os.path.join(box, cls + '.java')
    io.open(p, 'w', encoding='utf-8').write(src)
    c = subprocess.run(['javac', '-nowarn', p], cwd=box,
                       capture_output=True, text=True, timeout=120)
    if c.returncode != 0:
        return False, c.stderr.strip()
    r = subprocess.run(['java', '-cp', box, cls], cwd=box,
                       input=(stdin or ''), capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return False, (r.stdout + r.stderr).strip()
    return True, r.stdout


def check_file(name, results, answered=None, questions=None):
    """Check one content file.

    `answered` and `questions` are the book-wide registries backing data-question:
    a question and its answer live in different files by design, so neither can be
    resolved until every file has been read.
    """
    path = os.path.join(CONTENT, name + '.html')
    doc = io.open(path, encoding='utf-8').read()
    work = tempfile.mkdtemp(prefix='cos221_')
    try:
        for m in ANY_PRE_RE.finditer(doc):
            cls = m.group('cls')
            if cls not in ALLOWED_PRE:
                where = f'{name}:{doc[:m.start()].count(chr(10)) + 1}'
                results.append(('FAIL', where,
                                f'<pre class="{cls}"> is not a listing class. Use "src", '
                                f'"src nonum" or "out": any other class is invisible to '
                                f'this gate and unstyled by manual.css.'))

        for m in PRE_RE.finditer(doc):
            attrs = dict((a.group('k'), htmllib.unescape(a.group('v')))
                         for a in ATTR_RE.finditer(m.group('attrs')))
            where = f'{name}:{doc[:m.start()].count(chr(10)) + 1}'

            # Width first, for EVERY listing including nocheck skeletons: a wide line
            # shrinks the whole book whether or not its output is checked.
            try:
                for ln in source_of(m.group('body')).split('\n'):
                    if len(ln) > MAX_COL:
                        results.append(('FAIL', where,
                                        f'code line is {len(ln)} chars, over the {MAX_COL}-char '
                                        f'panel limit; it would shrink the whole book. Wrap it:\n'
                                        f'  {ln.strip()[:80]}'))
            except ValueError:
                pass                              # reported below by the real check

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

            # data-question is tested BEFORE data-frag/data-member, and the order is
            # load-bearing rather than stylistic. A dry-run question is usually a bare
            # method, so it carries data-member too; if the member branch runs first it
            # returns "member compiles" and the listing never registers as a question,
            # so the requirement that its answer exist quietly evaporates. The gate
            # still reports a clean pass, having checked half of what it claims. That
            # is precisely the failure this contract was added to prevent, so the
            # question branch owns any listing that declares itself one.
            if 'question' in attrs:
                # The question usually prints the METHOD it wants traced, not a whole
                # program, exactly as the papers do. So it composes with frag/member:
                # wrap it to prove it compiles, but register the lines as written,
                # since those are the lines the answer must contain.
                cls = 'Q' + re.sub(r'\W', '', where)
                probe = src
                if 'frag' in attrs or 'member' in attrs:
                    probe = wrap(src, cls, 'frag' if 'frag' in attrs else 'member')
                else:
                    cls = attrs.get('run') or cls
                ok, got = run_one(probe, cls, attrs.get('stdin'), work)
                if not ok:
                    results.append(('FAIL', where,
                                    f'{cls}: a question, but it does not compile/run:\n{got[:400]}'))
                    continue
                if claimed_output(doc, m.end()) is not None:
                    results.append(('FAIL', where,
                                    f'{cls}: declared data-question (output withheld) but an '
                                    f'output block follows it: the paper is printing its own answer'))
                    continue
                if questions is not None:
                    questions.append((where, code_lines(src), attrs['question'], cls))
                continue

            if 'frag' in attrs or 'member' in attrs:
                mode = 'frag' if 'frag' in attrs else 'member'
                cls = mode.capitalize() + re.sub(r'\W', '', where)
                ok, msg = run_one(wrap(src, cls, mode), cls, attrs.get('stdin'), work)
                results.append(('OK' if ok else 'FAIL', where,
                                f'{mode} compiles' if ok else f'{mode} does not compile:\n{msg[:400]}'))
                continue

            if 'run' not in attrs:
                results.append(('FAIL', where,
                                'listing declares no contract: add data-run, data-compile, '
                                'data-frag, data-member, data-question or data-nocheck'))
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
                if answered is not None:
                    answered.append((where, code_lines(src)))
                results.append(('OK', where, f'{cls}: output matches the JVM'))
            else:
                results.append(('FAIL', where,
                                f'{cls}: PRINTED OUTPUT IS WRONG.\n'
                                f'  manual claims: {norm(want)!r}\n'
                                f'  JVM printed  : {norm(got)!r}'))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def resolve_questions(questions, answered, results, partial):
    """Every withheld answer must actually exist, and still match its question.

    A data-question listing proves it runs, but not that the reader can ever find
    out what it printed. That is the half a mock paper is judged on. So the answer
    is required to exist as an output-checked listing of the SAME source, which
    also pins the two copies together: edit the solution's code and the question it
    answers is no longer the question that was asked, and the gate says so.
    """
    for where, need, target, cls in questions:
        if partial:
            results.append(('SKIP', where,
                            f'{cls}: question output withheld; its answer is in {target}, '
                            f'not cross-checked because only some files were checked '
                            f'(run check_code.py bare)'))
            continue
        hits = [w for w, have in answered if is_subsequence(need, have)]
        if not hits:
            results.append(('FAIL', where,
                            f'{cls}: declares its answer is in {target}, but no listing '
                            f'anywhere runs this code with a checked output block. Either '
                            f'the answer is missing, or it was edited and no longer answers '
                            f'the question that was asked.'))
        else:
            results.append(('OK', where,
                            f'{cls}: output withheld here, answered at {", ".join(hits)}'))


def main():
    if not shutil.which('javac'):
        raise SystemExit('javac not on PATH: the snippet gate cannot run')
    all_names = [f[:-5] for f in sorted(os.listdir(CONTENT)) if f.endswith('.html')]
    names = sys.argv[1:] or all_names
    results = []
    answered, questions = [], []
    for n in names:
        check_file(n, results, answered, questions)
    resolve_questions(questions, answered, results, partial=(names != all_names))

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
