"""Generate content/objective.html: the objective half of the paper.

WHY THIS SECTION EXISTS. Every paper this semester except the physics one is a
SINGLE paper carrying an objective section and a theory section, confirmed by
the student on 2026-08-09, after this manual had already shipped three times.
The book taught and drilled the theory half beautifully and carried no objective
practice at all, so a reader could work every past question in it and still meet
the first thirty marks of the paper cold.

THE SOURCE. Both computer-based tests, 60 questions each, 120 in all. They were
transcribed from the screenshots in sources/exams/objective_mcq_tests/ during the
drill build and every numeric answer was recomputed rather than trusted; the
transcription plus the per-option reasoning lives in webapp/data/ift222/module*.json,
which is this generator's input. There is no eye-verified transcript FILE for the
tests the way there is for the four written papers, so qa_verbatim.py cannot gate
these stems the way it gates a past paper. That is stated plainly in the section's
own opening rather than papered over.

THE HOUSE RULE THIS OBEYS. Every option is explained, right and wrong alike, and
no explanation names an option by its letter: it names it by its words. Letters
are a property of where an option sits on a page, and the same question drilled
on the platform shuffles them.

Idempotent: re-running rewrites the file from the JSON. Do all transforms here,
never by hand on the output.

    cd build && python gen_objective.py
"""
import html as _html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'content', 'objective.html')
DATA = os.path.abspath(os.path.join(
    HERE, '..', '..', '..', 'webapp', 'data', 'ift222'))

# The ten topics, in the order the manual teaches them. The label is the
# section heading; the "taught" line points the reader back at the unit that
# teaches it, which is what a missed question is supposed to send them to.
TOPICS = [
    (1, 'Architecture versus Organization', 'Module One, Unit 1'),
    (2, 'Instruction Set Architecture and Microarchitecture', 'Module One, Unit 4'),
    (3, 'Number Systems and Codes', 'Foundations F.1 and F.2, and Module One, Unit 2'),
    (4, 'Signed Numbers and Complements', 'Module One, Unit 2'),
    (5, 'Floating Point and IEEE 754', 'Module One, Unit 3'),
    (6, 'Instruction Types and Formats', 'Module One, Unit 4'),
    (7, 'Addressing Modes', 'Module One, Unit 4'),
    (8, 'Memory, Buses and the Processor', 'Module Two Unit 1, and Module Three'),
    (9, 'Performance, RISC and CISC', 'Module Two Unit 2, and Module Four Unit 1'),
    (10, 'Von Neumann, Harvard and Image Data', 'Module One Unit 1, and Module One Unit 2'),
]

LETTERS = 'abcdefgh'


def esc(s):
    """Escape for HTML, then repair the characters the house style allows."""
    return _html.escape(s, quote=False)


def load():
    qs = []
    for name in sorted(os.listdir(DATA)):
        m = re.fullmatch(r'module(\d+)\.json', name)
        if not m:
            continue
        with open(os.path.join(DATA, name), encoding='utf-8') as fh:
            qs.extend(json.load(fh))
    return qs


def check(qs):
    """Refuse to generate from data that cannot satisfy the house rules."""
    bad = []
    for q in qs:
        if q.get('style') != 'mcq':
            bad.append(f"{q['id']}: not an mcq")
        why = q.get('why') or {}
        for o in q['options']:
            if not why.get(o['id']):
                bad.append(f"{q['id']}: option {o['id']} has no explanation")
        if q['answer'] not in {o['id'] for o in q['options']}:
            bad.append(f"{q['id']}: answer {q['answer']} is not one of its options")
        blob = q['prompt'] + ' '.join(o['text'] for o in q['options']) + \
            ' '.join(why.values()) + q.get('explanation', '')
        for ch, nm in (('—', 'em dash'), ('–', 'en dash'),
                       ('―', 'horizontal bar'), ('‒', 'figure dash')):
            if ch in blob:
                bad.append(f"{q['id']}: contains a {nm}")
    if bad:
        print('gen_objective: the source data cannot be published as is:',
              file=sys.stderr)
        for b in bad[:40]:
            print('  x ' + b, file=sys.stderr)
        sys.exit(1)


def source_chip(q):
    """TEST 1 Q16 -> the chip the reader sees, so provenance is never implied."""
    src = (q.get('slides') or ['Test'])[0]
    return esc(src.upper())


def question_li(q):
    opts = ' &nbsp; '.join(
        f'({LETTERS[i]}) {esc(o["text"])}' for i, o in enumerate(q['options']))
    return (f'<li><span class="qsrc">{source_chip(q)}</span> '
            f'{esc(q["prompt"])} &nbsp; {opts}</li>')


def answer_block(qs):
    """Every option accounted for, and the key named by its words not its letter."""
    rows = []
    for n, q in enumerate(qs, 1):
        key = next(o for o in q['options'] if o['id'] == q['answer'])
        why = q['why']
        parts = [f'<p class="oq"><b>{n}.</b> The answer is '
                 f'<b>{esc(key["text"].rstrip("."))}</b>. {esc(q.get("explanation", ""))}</p>']
        items = []
        for o in q['options']:
            verdict = why[o['id']]
            # The stored verdict opens with "Correct." or "Wrong."; keep that word
            # as the visual cue and set the option's own words beside it.
            mark = 'ok' if o['id'] == q['answer'] else 'no'
            items.append(f'<li class="{mark}"><b>{esc(o["text"].rstrip("."))}.</b> '
                         f'{esc(verdict)}</li>')
        parts.append('<ul class="whys">' + ''.join(items) + '</ul>')
        rows.append(''.join(parts))
    return '\n'.join(rows)


HOWTO = """<section>
<div class="kick">Objective Section</div>
<h2 class="title">How to Attack an Objective Question</h2>
<hr class="rule">
<p class="lead">Thirty of these decide the first third of the paper, and they are
answered under more time pressure than anything in the theory half. This part is
where you practise them.</p>

<div class="box teach"><div class="bar"><span>Teach</span></div>
<div class="body">
<p>An objective question is not a smaller version of a theory question. It is a
different task: you are not producing an answer, you are eliminating three wrong
ones. That changes the method, and the method is worth marks on its own.</p>
<p>Every question below came from one of the two computer-based tests actually
set on this course. Both are reproduced whole, 60 questions each, grouped by
topic rather than by test so that a run of questions drills one skill at a time.
The stems and options were read off the test screenshots by eye. That is a
weaker guarantee than the four written papers in this book carry, since those are
held character for character against a transcript by a gate, and it is said here
rather than left for you to assume.</p>
</div></div>

<div class="box keypoint"><div class="bar"><span>Key point</span></div>
<div class="body">
<p class="formal">In a four-option question, three options are wrong for a
statable reason. Finding the reason is faster and safer than recognising the
right answer, because recognition is exactly what a well-written distractor
attacks.</p>
<p class="blunt"><b>Blunt version:</b> do not look for the right one. Kill the
wrong ones.</p>
</div></div>

<div class="box teach"><div class="bar"><span>Teach</span></div>
<div class="body">
<p>The four moves, in order, on every question:</p>
<ol class="steps">
<li><b>Read the stem twice and underline the instruction word.</b> NOT, BEST,
MOST DIRECTLY, PRIMARILY and EXCEPT each flip or narrow the question, and each
one appears on these tests. A question containing NOT wants the odd one out,
and reading it as a normal question makes every wrong answer look right.</li>
<li><b>Answer it before you read the options where you can.</b> If you know that
organization is the construction and architecture is the blueprint, decide that
first. Then the options are a lookup, not a suggestion.</li>
<li><b>Strike the impossible.</b> Two of the four usually die immediately: an
option that contradicts a definition, names the wrong layer, or is true but
answers a different question. Cross them out physically.</li>
<li><b>Choose between the last two on the exact wording.</b> This is where the
mark is won or lost, and it is nearly always one word: only, always, all,
determines, eliminates. A distractor that says "eliminates hardware complexity
entirely" is wrong because of "entirely", not because of hardware complexity.</li>
</ol>
</div></div>

<div class="box trap"><div class="bar"><span>Trap</span></div>
<div class="body">
<p>The longest option is right more often than chance on these two tests, because
a fully qualified statement takes more words than a slogan. Do not turn that into
a rule. It is a tiebreaker for a question you cannot otherwise split, and nothing
more. Several questions here punish it deliberately.</p>
</div></div>

<div class="box trap"><div class="bar"><span>Trap</span></div>
<div class="body">
<p>One question on Test 1 asks how a floating point number is stored and its
marked answer is Sign, Mantissa, Exponent. The true IEEE 754 field order, the one
Module One Unit 3 teaches and the one every other question in this book uses, is
Sign, Exponent, Mantissa. Learn the true order, and know that this particular
question was marked the other way. Both facts are worth carrying: one is correct,
the other is what the marking scheme did.</p>
</div></div>

<div class="box recall"><div class="bar"><span>How to use this part</span></div>
<div class="body">
<p>Sit one topic at a time, timed at 45 seconds a question, with the answers
covered. Then read the answer block for that topic in full, including the
explanations for the questions you got right: on an objective paper, a right
answer for a wrong reason is a mark you will not get twice.</p>
</div></div>
</section>
"""


def build():
    qs = load()
    check(qs)
    by_topic = {}
    for q in qs:
        by_topic.setdefault(q['module'], []).append(q)

    out = ['<!-- ===================== OBJECTIVE SECTION (divider) ==================== -->',
           '<div class="part">',
           '  <div class="kicker">Objective Section</div>',
           '  <h1>Both Tests,<br>Every Option Explained</h1>',
           '  <div class="blurb">All 120 questions from the two computer-based tests, '
           'grouped by topic and answered in full. Not only why the answer is the answer: '
           'why each of the other three is not. Sit a topic, then read every line of its '
           'answer block.</div>',
           '  <div class="divider-motif">',
           '    <svg viewBox="0 0 520 210" xmlns="http://www.w3.org/2000/svg" '
           'font-family="DejaVu Sans">',
           '      <g font-size="13" fill="#33566e">',
           '        <text x="34" y="30">Which analogy best represents computer '
           'organization?</text>',
           '      </g>',
           '      <g font-size="12.5" fill="#67707a">',
           '        <text x="52" y="66">the owner of the building</text>',
           '        <text x="52" y="98">the cost estimate</text>',
           '        <text x="52" y="130">the construction process implementing the '
           'design</text>',
           '        <text x="52" y="162">the building design</text>',
           '      </g>',
           '      <g stroke="#b91c1c" stroke-width="1.6">',
           '        <line x1="48" y1="62" x2="250" y2="62"/>',
           '        <line x1="48" y1="94" x2="196" y2="94"/>',
           '        <line x1="48" y1="158" x2="216" y2="158"/>',
           '      </g>',
           '      <circle cx="38" cy="126" r="7" fill="none" stroke="#15803d" '
           'stroke-width="2"/>',
           '      <rect x="34" y="186" width="452" height="1.6" fill="#c9b6f2"/>',
           '      <text x="34" y="204" font-size="9.6" fill="#8a919b" '
           'letter-spacing="2.4">KILL THE WRONG ONES</text>',
           '    </svg>',
           '  </div>',
           '</div>',
           '',
           HOWTO]

    for num, label, taught in TOPICS:
        group = by_topic.get(num, [])
        if not group:
            continue
        out.append(f'<section>\n<div class="kick">Objective Section</div>\n'
                   f'<h2 class="title">{esc(label)}</h2>\n<hr class="rule">\n'
                   f'<p class="lead">{len(group)} questions. Taught in {esc(taught)}. '
                   f'Cover the answers before you start.</p>\n')
        out.append('<ol class="qlist objq">')
        out.extend(question_li(q) for q in group)
        out.append('</ol>')
        out.append('<div class="box obj"><div class="bar"><span>Answers, and why '
                   'every option is what it is</span></div>\n<div class="body">')
        out.append(answer_block(group))
        out.append('</div></div>\n</section>\n')

    text = '\n'.join(out) + '\n'
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(text)

    # Self-checks, printed every run so a silent regression is visible.
    total = sum(len(v) for v in by_topic.values())
    print(f'gen_objective: {total} questions, {len(by_topic)} topics -> '
          f'content/objective.html ({len(text)} chars)')
    # The house rule is that an explanation names an option by its WORDS, never
    # by its letter, because the same question shuffles its options on the drill.
    # Checked against the generated answer blocks only: the question lists above
    # them are supposed to carry letters.
    letters = re.compile(
        r'\b(?:option|choice|answer)\s+[a-h]\b|\bchoosing\s+[a-h]\b', re.I)
    blocks = re.findall(r'<ul class="whys">.*?</ul>', text, re.S)
    named = [b for b in blocks if letters.search(b)]
    print(f'  answer blocks: {len(blocks)}, naming an option by its letter: '
          f'{len(named)}')
    if named:
        print('  x an explanation names a letter: '
              + letters.search(named[0]).group(0), file=sys.stderr)
        sys.exit(1)
    print(f'  every option explained: yes, {sum(len(q["options"]) for q in qs)} '
          f'options across {total} questions')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build()
