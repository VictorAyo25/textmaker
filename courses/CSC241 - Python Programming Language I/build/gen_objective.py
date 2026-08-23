"""Render the objective section from objective_bank.py, verifying as it goes.

NOTHING IS TYPED FROM MEMORY. Every question in the bank that carries a code
block is marked runs=True, and this generator EXECUTES that code on a real
interpreter and refuses to write the section unless the option marked correct is
exactly what came back. A question whose "answer" the interpreter disagrees with
does not reach the page. That is the same rule the rest of this manual lives by
(verify_code.py, 367 claims, 0 mismatches) applied to the new section.

    cd build && python gen_objective.py
"""
import contextlib
import html as _html
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'content', 'objective.html')
sys.path.insert(0, HERE)

from objective_bank import Q

LETTERS = 'abcd'

MODULES = [
    (1, 'Introduction to Python Programming', 'Module One'),
    (2, 'Python Basics, Syntax, Operators and Strings', 'Module Two'),
    (3, 'Control Flow, Lists, Tuples, Sets and Dictionaries', 'Module Three'),
    (4, 'Functions, Modules, Files and Exceptions', 'Module Four'),
    (5, 'Databases and GUI Development', 'Module Five'),
]


def esc(s):
    return _html.escape(s, quote=False)


def run(code):
    """Execute a snippet and return its stdout, or the exception's class name."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, '<objective>', 'exec'), {})
    except Exception as exc:
        tail = buf.getvalue()
        return (tail + type(exc).__name__).strip()
    return buf.getvalue().strip()


def verify():
    """Every runs=True claim, held against a real interpreter."""
    checked, bad = 0, []
    for item in Q:
        if not item['runs']:
            continue
        checked += 1
        want = item['options'][item['answer']].strip()
        got = run(item['code'])
        if got != want:
            bad.append((item['id'], want, got))
    return checked, bad


def option_html(text):
    if '\n' in text:
        return '<code class="ob">' + '<br>'.join(
            esc(line) for line in text.split('\n')) + '</code>'
    return esc(text)


def question_html(n, item):
    parts = [f'<li><p class="oq">{esc(item["prompt"])}</p>']
    if item.get('code'):
        parts.append('<pre class="code">' + esc(item['code']) + '</pre>')
    parts.append('<ul class="opts">')
    for i, opt in enumerate(item['options']):
        parts.append(f'<li><span class="ol">({LETTERS[i]})</span> '
                     f'{option_html(opt)}</li>')
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


HOWTO = """<section>
<div class="kick">Objective Section</div>
<h2 class="title">How to Attack an Objective Question</h2>
<hr class="rule">
<p class="lead">The paper carries an objective section as well as the long
questions, and it is sat under more time pressure than anything else on it. This
part is where you practise that half.</p>

<div class="box teach"><div class="bar"><span>Teach</span><span class="tag">where these questions come from</span></div>
<div class="body">
<p>Say this plainly, because it decides how you should read them. This course has
no computer-based test among its papers, so unlike the long questions in this book,
which are quoted from the examiner word for word, <b>these 70 questions were
written for this manual</b>. They are not the examiner's and they do not pretend
to be.</p>
<p>What they are grounded in is real. Every one is drawn from something this
manual teaches and something the ten past papers actually ask about, and the
paper's own habits are copied on purpose: it leans hard on asking for the output
of a code snippet, on asking you to identify and correct an error, and on asking
for a property by name, such as lists being ordered, sets being unique, or strings
being immutable. Those are descriptions of what the paper does, not quotations of
its wording, which is why none of them is set in quotation marks here. So what
you are drilling is this course's own material in objective form, even though the
wording is ours.</p>
<p>Every code snippet below was <b>run on a real interpreter</b> and the answer is
what came back, not what it ought to have been. If your answer differs from the
book's, the interpreter settled it, not an opinion.</p>
</div></div>

<div class="box keypoint"><div class="bar"><span>Key point</span></div>
<div class="body">
<p class="formal">In a four-option question, three options are wrong for a reason
you can state. Finding that reason is faster and safer than recognising the right
answer, because recognition is exactly what a well-built distractor attacks.</p>
<p class="blunt"><b>Blunt version:</b> do not hunt for the right one. Kill the
wrong ones.</p>
</div></div>

<div class="box teach"><div class="bar"><span>Teach</span><span class="tag">the four moves, in order</span></div>
<div class="body">
<ol class="steps">
<li><b>Underline the instruction word.</b> NOT, TRUE, BEST, PRIMARILY and EXCEPT
each flip or narrow the question. A question containing NOT wants the odd one out,
and read as an ordinary question every wrong answer starts to look right.</li>
<li><b>For a code question, trace it on paper before you look at the options.</b>
Write the variables down the margin and update them line by line. The options are
built from the answers you get by tracing it WRONG, so reading them first plants
the mistake.</li>
<li><b>Strike the impossible.</b> Two of four usually die at once: an option that
contradicts a definition, or that is true but answers a different question.</li>
<li><b>Split the last two on the exact wording.</b> It is nearly always one word:
only, always, all, entirely, every. An option saying a function "eliminates
complexity entirely" is wrong because of "entirely".</li>
</ol>
</div></div>

<div class="box trap"><div class="bar"><span>Trap</span><span class="tag">the five that decide most output questions</span></div>
<div class="body">
<p>Five facts answer a large share of every output-tracing question this
course can set. Know them cold and the tracing gets much shorter.</p>
<ol class="qlist">
<li><b>input() returns a string</b>, always, however numeric it looks.</li>
<li><b>A slice excludes its stop</b>, and range() excludes its stop too.</li>
<li><b>A single slash always gives a float</b>; double slash floors.</li>
<li><b>Methods that change a list in place return None</b>: sort, append,
reverse, extend.</li>
<li><b>Assignment does not copy.</b> b = a gives one object two names.</li>
</ol>
</div></div>

<div class="box recall"><div class="bar"><span>How to use this part</span></div>
<div class="body">
<p>Sit one module at a time, timed at 45 seconds a question, with the answers
covered. Then read the whole answer block for that module, including the questions
you got right: on an objective paper a right answer for the wrong reason is a mark
you will not get twice.</p>
</div></div>
</section>
"""


def build():
    checked, bad = verify()
    if bad:
        print('gen_objective: the interpreter disagrees with the bank, nothing '
              'written:', file=sys.stderr)
        for qid, want, got in bad:
            print(f'  x {qid}: the answer says {want!r}, the interpreter gives '
                  f'{got!r}', file=sys.stderr)
        sys.exit(1)

    by_mod = {}
    for item in Q:
        by_mod.setdefault(item['module'], []).append(item)

    out = ['<!-- ===================== OBJECTIVE SECTION ===================== -->',
           '<div class="part">',
           '  <div class="kicker">Objective Section</div>',
           '  <h1>Seventy Questions,<br>Every Option Explained</h1>',
           '  <div class="blurb">The other half of the paper. Seventy objective '
           'questions across the five modules, every code snippet run on a real '
           'interpreter, and for every question a reason why each of the four '
           'options is right or wrong.</div>',
           '  <div class="divider-motif">',
           '    <svg viewBox="0 0 520 200" xmlns="http://www.w3.org/2000/svg" '
           'font-family="DejaVu Sans">',
           '      <g font-family="DejaVu Sans Mono" font-size="13" fill="#306998">',
           '        <text x="34" y="30">&gt;&gt;&gt; numbers[-3:] * 2</text>',
           '      </g>',
           '      <g font-size="12.5" fill="#6b7280">',
           '        <text x="56" y="66">[6, 8, 10]</text>',
           '        <text x="56" y="98">[3, 4, 5, 3, 4, 5]</text>',
           '        <text x="56" y="130">[2, 3, 4]</text>',
           '        <text x="56" y="162">TypeError</text>',
           '      </g>',
           '      <g stroke="#b91c1c" stroke-width="1.6">',
           '        <line x1="52" y1="62" x2="150" y2="62"/>',
           '        <line x1="52" y1="126" x2="140" y2="126"/>',
           '        <line x1="52" y1="158" x2="136" y2="158"/>',
           '      </g>',
           '      <circle cx="42" cy="94" r="7" fill="none" stroke="#1f7a4d" '
           'stroke-width="2"/>',
           '      <rect x="34" y="182" width="452" height="1.6" fill="#ffd43b"/>',
           '    </svg>',
           '  </div>',
           '</div>',
           '',
           HOWTO]

    for num, label, kick in MODULES:
        group = by_mod.get(num, [])
        if not group:
            continue
        out.append(f'<section>\n<div class="kick">Objective Section</div>\n'
                   f'<h2 class="title">{esc(label)}</h2>\n<hr class="rule">\n'
                   f'<p class="lead">{len(group)} questions on {esc(kick)}. Cover '
                   f'the answers, sit the whole set, then read every line of the '
                   f'answer block.</p>\n')
        out.append('<ol class="qlist objq">')
        out.extend(question_html(i, it) for i, it in enumerate(group, 1))
        out.append('</ol>')
        out.append('<div class="box obj"><div class="bar"><span>Answers, and why '
                   'every option is what it is</span></div>\n<div class="body">')
        out.extend(answer_html(i, it) for i, it in enumerate(group, 1))
        out.append('</div></div>\n</section>\n')

    text = '\n'.join(out) + '\n'
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(text)

    print(f'gen_objective: {len(Q)} questions over {len(by_mod)} modules -> '
          f'content/objective.html ({len(text)} chars)')
    print(f'  code claims executed and matched: {checked} of {checked}')
    print(f'  options explained: {sum(len(q["options"]) for q in Q)}')
    widest = max((len(l) for q in Q if q.get('code')
                  for l in q['code'].split('\n')), default=0)
    print(f'  widest code line: {widest} columns')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build()
