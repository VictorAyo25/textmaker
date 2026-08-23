"""Render the objective section, compiling and running every claim first.

NOTHING IS TYPED FROM MEMORY. This is the same rule the rest of this book lives
by, applied to the new section. Every question that shows a program is marked
runs=True, and this generator writes it to a temp directory, compiles it with
javac and runs it with java, exactly as check_code.py does for the 225 listings
in the modules. If the option marked correct is not what the JVM produced, the
section is not written and the mismatch is printed.

Two questions claim a COMPILE ERROR as their answer. Those carry expect_error
instead, naming a phrase javac must produce, and the generator requires the
compile to fail AND the message to contain it. A claim that Java rejects
something is worth no more than a claim about output unless it is run.

    cd build && python gen_objective.py
"""
import html as _html
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'content', 'objective.html')
sys.path.insert(0, HERE)

from objective_bank import Q

LETTERS = 'abcd'

PARTS = [
    ('The Language, the Toolchain and Objects', {1, 2},
     'Foundations, Module One and Module Two'),
    ('Types, Operators, Input and Output', {3}, 'Module Three'),
    ('Control Structures', {4}, 'Module Four'),
    ('Methods', {5}, 'Module Five'),
    ('Object-Oriented Programming', {6}, 'Module Six'),
    ('Strings', {7}, 'Module Seven'),
    ('Arrays', {8}, 'Module Eight'),
    ('Recursion', {9}, 'Module Nine'),
    ('Exceptions and File Input and Output', {10}, 'Module Ten'),
]


def esc(s):
    return _html.escape(s, quote=False)


def compile_and_run(code, cls):
    """(ok, output_or_compiler_message). One temp directory per program."""
    d = tempfile.mkdtemp(prefix='cos221obj_')
    try:
        src = os.path.join(d, cls + '.java')
        with open(src, 'w', encoding='utf-8') as fh:
            fh.write(code)
        c = subprocess.run(['javac', '-encoding', 'UTF-8', src],
                           capture_output=True, text=True, cwd=d)
        if c.returncode != 0:
            return False, (c.stderr or c.stdout)
        r = subprocess.run(['java', '-cp', d, cls],
                           capture_output=True, text=True, cwd=d, timeout=30)
        return True, (r.stdout + r.stderr).replace('\r\n', '\n').strip()
    finally:
        shutil.rmtree(d, ignore_errors=True)


def verify():
    ran, bad = 0, []
    for item in Q:
        if item['expect_error']:
            ran += 1
            ok, msg = compile_and_run(item['code'], item['cls'])
            if ok:
                bad.append((item['id'], 'a compile error', 'it compiled'))
            elif item['expect_error'] not in msg:
                bad.append((item['id'], f'javac to say {item["expect_error"]!r}',
                            msg.strip()[:200]))
            continue
        if not item['runs']:
            continue
        ran += 1
        want = item['options'][item['answer']].strip()
        ok, got = compile_and_run(item['code'], item['cls'])
        if not ok:
            bad.append((item['id'], want, 'it did not compile: ' + got.strip()[:200]))
        elif got != want:
            bad.append((item['id'], want, got))
    return ran, bad


def listing_html(item):
    """The book's own listing markup, produced by the book's own highlighter.

    A listing here must declare its contract in data attributes, exactly as every
    other listing in this book does, so that check_code.py compiles and runs it
    too. That means each of these programs is verified TWICE: once by this
    generator before the section is written, and again by the standing gate over
    the whole book.
    """
    import hl
    if item['expect_error']:
        attrs = (f' data-compile="{item["cls"]}"'
                 f' data-error="{_html.escape(item["expect_error"], quote=True)}"')
    else:
        attrs = f' data-run="{item["cls"]}"'
    return f'<pre class="src nonum"{attrs}>{hl.markup(item["code"])}</pre>'


def question_html(item):
    parts = [f'<li><p class="oq">{esc(item["prompt"])}</p>']
    if item.get('code'):
        parts.append(listing_html(item))
    parts.append('<ul class="opts">')
    for i, opt in enumerate(item['options']):
        body = ('<code class="ob">' + '<br>'.join(esc(l) for l in opt.split('\n'))
                + '</code>') if '\n' in opt else esc(opt)
        parts.append(f'<li><span class="ol">({LETTERS[i]})</span> {body}</li>')
    parts.append('</ul></li>')
    return '\n'.join(parts)


def answer_html(n, item):
    key = item['options'][item['answer']]
    shown = key.replace('\n', ' then ') if '\n' in key else key
    out = [f'<p class="oa"><b>{n}.</b> The answer is <b>{esc(shown)}</b>. '
           f'{esc(item["explanation"])}</p>', '<ul class="whys">']
    for i, opt in enumerate(item['options']):
        mark = 'ok' if i == item['answer'] else 'no'
        label = opt.replace('\n', ' then ') if '\n' in opt else opt
        out.append(f'<li class="{mark}"><b>{esc(label)}.</b> {esc(item["why"][i])}</li>')
    out.append('</ul>')
    return '\n'.join(out)


HOWTO = """<!-- ============ OBJECTIVE SECTION ============ -->

<section>
  <div class="kick">O.1 &middot; OBJECTIVE &middot; HOW TO ATTACK AN OBJECTIVE QUESTION</div>
  <h2 class="title">How to attack an objective question</h2>
  <hr class="rule"/>

<p class="lead">The paper carries an objective section as well as the long questions,
and it is answered under more time pressure than anything else on it. This part is
where you practise that half.</p>

<div class="box teach"><div class="bar"><span>TEACH &middot; Where these questions came from</span></div>
<div class="body">
<p>Say this plainly, because it decides how to read them. This course has no
computer-based test among its papers, so unlike the forty question parts solved
earlier in this book, which are quoted from the examiner word for word, <b>these
questions were written for this manual</b>. They are not the examiner's and they do
not pretend to be.</p>
<p>What they are grounded in is real. Every one comes from something this book
teaches and something the two past papers actually ask about, and the paper's habits
are copied on purpose: it asks for the output of a fragment, it asks you to find the
error, it asks for a definition with an example, and it asks for the difference
between two things that look alike.</p>
<p>Every program below was <b>compiled with javac and run on a real JVM</b>, and the
answer is what came back. Two questions claim that a program does NOT compile, and
those were checked the same way: the compiler was run and its message read. If your
answer differs from the book's, the JVM settled it, not an opinion.</p>
</div></div>

<div class="box keypoint"><div class="bar"><span>KEY POINT</span></div>
<div class="body">
<p class="formal">In a four-option question, three options are wrong for a reason you
can state. Finding that reason is faster and safer than recognising the right answer,
because recognition is exactly what a well-built distractor attacks.</p>
<p class="blunt"><b>Blunt version:</b> do not hunt for the right one. Kill the wrong
ones.</p>
</div></div>

<div class="box teach"><div class="bar"><span>TEACH &middot; The four moves, in order</span></div>
<div class="body">
<ol class="steps">
<li><b>Underline the instruction word.</b> NOT, TRUE, BEST, PRIMARILY and EXCEPT each
flip or narrow the question. Read a NOT question as an ordinary one and every wrong
answer starts to look right.</li>
<li><b>On a code question, dry run it before you read the options.</b> Variables down
the margin, one row per statement. The options are built from the answers you get by
tracing it WRONG, so reading them first plants the mistake.</li>
<li><b>Strike the impossible.</b> Two of the four usually die at once: an option that
contradicts a definition, or one that is true but answers a different question.</li>
<li><b>Split the last two on the exact wording.</b> It is nearly always one word:
only, always, all, entirely, every.</li>
</ol>
</div></div>

<div class="box trap"><div class="bar"><span>TRAP &middot; The six that decide most output questions</span></div>
<div class="body">
<p>Six facts answer a large share of every what-does-this-print question this course
can set. Know them cold and the tracing gets much shorter.</p>
<ol class="qlist">
<li><b>int divided by int is an int.</b> 7 / 2 is 3, and the fraction is discarded.</li>
<li><b>Java truncates towards zero</b>, so -7 / 2 is -3, and % takes the sign of the
left operand.</li>
<li><b>Once a String is involved, every later plus JOINS.</b> "T: " + 1 + 2 is
"T: 12".</li>
<li><b>== on objects compares references.</b> For strings, always use equals.</li>
<li><b>Strings are immutable.</b> A String method returns a new string and changes
nothing.</li>
<li><b>Java passes by value.</b> Reassigning a parameter never reaches the caller.</li>
</ol>
</div></div>

<div class="box recall"><div class="bar"><span>RECALL &middot; How to use this part</span></div>
<div class="body">
<p>Sit one group at a time, timed at 45 seconds a question, with the answers covered.
Then read the whole answer block for that group, including the questions you got
right: on an objective paper a right answer for the wrong reason is a mark you will
not get twice.</p>
</div></div>
</section>
"""


def build():
    ran, bad = verify()
    if bad:
        print('gen_objective: the JVM disagrees with the bank, nothing written:',
              file=sys.stderr)
        for qid, want, got in bad:
            print(f'  x {qid}: the answer says {want!r}, the JVM gives {got!r}',
                  file=sys.stderr)
        sys.exit(1)

    by_mod = {}
    for item in Q:
        by_mod.setdefault(item['module'], []).append(item)

    out = [HOWTO]
    n_sec = 1
    for label, mods, taught in PARTS:
        group = [it for m in sorted(mods) for it in by_mod.get(m, [])]
        if not group:
            continue
        n_sec += 1
        # This book's Contents is DERIVED from its headings: a section is a
        # <div class="kick">PLAIN TEXT</div> followed by an <h2 class="title">,
        # and a box bar wraps its label in a span. Emitting anything else gives a
        # section the Contents cannot see.
        out.append(f'<section>\n  <div class="kick">O.{n_sec} &middot; OBJECTIVE '
                   f'&middot; {esc(label.upper())}</div>\n'
                   f'  <h2 class="title">{esc(label)}</h2>\n  <hr class="rule"/>')
        out.append(f'<p class="lead">{len(group)} questions, from {esc(taught)}. '
                   f'Cover the answers, sit the whole set, then read every line of '
                   f'the answer block.</p>')
        out.append('<ol class="qlist objq">')
        out.extend(question_html(it) for it in group)
        out.append('</ol>')
        out.append('<div class="box obj"><div class="bar"><span>ANSWERS &middot; '
                   'and why every option is what it is</span></div>\n'
                   '<div class="body">')
        out.extend(answer_html(i, it) for i, it in enumerate(group, 1))
        out.append('</div></div>\n</section>')

    text = '\n'.join(out) + '\n'
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(text)

    widest = max((len(l) for it in Q if it.get('code')
                  for l in it['code'].split('\n')), default=0)
    print(f'gen_objective: {len(Q)} questions -> content/objective.html '
          f'({len(text)} chars)')
    print(f'  programs compiled and run on a real JVM: {ran}, mismatches: 0')
    print(f'  options explained: {sum(len(it["options"]) for it in Q)}')
    print(f'  widest code line: {widest} columns')
    letters = re.compile(r'\b(?:option|choice|answer)\s+[a-d]\b', re.I)
    blocks = re.findall(r'<ul class="whys">.*?</ul>', text, re.S)
    named = [b for b in blocks if letters.search(b)]
    print(f'  answer blocks: {len(blocks)}, naming an option by its letter: '
          f'{len(named)}')
    if named:
        sys.exit(1)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build()
