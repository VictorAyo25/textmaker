"""Generate content/objective.html: the objective half of the INS224 paper.

WHY THIS SECTION EXISTS. The student confirmed on 2026-08-09 that this paper now
carries an objective section as well as its written questions, and that the
objective format is the one used in the SECOND class test, which is multi-select:
"which TWO of the following". This manual shipped on 2026-07-23 with no objective
practice at all, so a reader could work both past papers in it and still meet a
third of the paper cold. Worse, the wrong FORM is expensive: a candidate who
knows the topic and stops at one option scores nothing on a which-two question.

THE SOURCE. Both class tests, 30 questions each, 60 in all, transcribed from the
screenshots in sources/ins tests/ during the drill build and held there with an
independently re-transcribed answer key. This generator reads
webapp/data/ins224/test0{1,2}.json. There is no eye-verified transcript FILE for
the tests the way there is for the two written papers, so qa_verbatim.py cannot
gate these stems; the section's opening page says so plainly.

THE THREE FORMS, all of which appear:
  mcq    one answer of four            (test 1 is entirely this)
  multi  which TWO of four             (the form the lecturer named)
  match  pair each item with its definition

THE HOUSE RULE. Every option is explained, right and wrong alike, and an
explanation names an option by its words, never by its letter. A match question
has no options to explain, so its answer is the completed pairing plus the note
that says what separates the pairs.

Idempotent: re-running rewrites the file from the JSON.

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
    HERE, '..', '..', '..', 'webapp', 'data', 'ins224'))

LETTERS = 'abcdefgh'

# The drill numbers its topics after the COURSE TEXT's units. This maps each one
# onto the part of THIS book that teaches it, which is not the same numbering:
# see the front matter's "Whose Module One?" box.
GROUPS = [
    ('Module One, the Analyst, the Life Cycle and Methodologies', {1, 2, 3},
     'Module One. Compulsory Question One.'),
    ('Module Two, Fact-Finding and Use Cases', {4, 5},
     'Module Two. Part of compulsory Question Two.'),
    ('Module Three, Data Flow Diagrams', {6},
     'Module Three. Part of compulsory Question Two.'),
    ('Module Four, the Entity-Relationship Model', {7},
     'Module Four. Part of compulsory Question Two.'),
    ('Module Five, Object Orientation and UML', {8, 9, 10},
     'Module Five. Compulsory Question Three.'),
    ('Module Six, Design, Architecture and Delivery', {11, 12, 13, 14, 15},
     'Module Six. Objective section only: the course text does not carry it.'),
]


def esc(s):
    return _html.escape(s, quote=False)


def load():
    """Both class tests, then the authored questions that fill what they missed.

    The tests stop where the course had got to when they were set: between them
    they never reach entity-relationship diagrams, object orientation or UML, and
    those are compulsory Question Two and compulsory Question Three. The authored
    set covers that gap in the multi-select form the lecturer named, and every one
    of them carries an AUTHORED chip so it can never be mistaken for the paper.
    """
    qs = []
    for name in ('test01.json', 'test02.json'):
        with open(os.path.join(DATA, name), encoding='utf-8') as fh:
            qs.extend(json.load(fh))
    try:
        from objective_extra import E
        qs.extend(E)
    except Exception as exc:                                  # pragma: no cover
        print(f'gen_objective: authored set not loaded ({exc})', file=sys.stderr)
    return qs


def check(qs):
    bad = []
    for q in qs:
        style = q.get('style')
        if style not in ('mcq', 'multi', 'match'):
            bad.append(f"{q['id']}: unknown style {style}")
        if style in ('mcq', 'multi'):
            why = q.get('why') or {}
            for o in q['options']:
                if not why.get(o['id']):
                    bad.append(f"{q['id']}: option {o['id']} has no explanation")
            ans = q['answer'] if isinstance(q['answer'], list) else [q['answer']]
            ids = {o['id'] for o in q['options']}
            for a in ans:
                if a not in ids:
                    bad.append(f"{q['id']}: answer {a} is not one of its options")
            if style == 'multi' and len(ans) != 2:
                bad.append(f"{q['id']}: a which-two question with {len(ans)} answers")
        if style == 'match' and not q.get('pairs'):
            bad.append(f"{q['id']}: a match question with no pairs")
        if not q.get('explanation'):
            bad.append(f"{q['id']}: no explanation")
        blob = q['prompt'] + q.get('explanation', '')
        blob += ''.join(o['text'] for o in q.get('options', []))
        blob += ''.join((q.get('why') or {}).values())
        blob += ''.join(p['left'] + p['right'] for p in q.get('pairs', []))
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


def chip(q):
    return esc((q.get('slides') or ['Test'])[0].upper())


def question_li(q):
    src = f'<span class="qsrc">{chip(q)}</span> '
    if q['style'] == 'match':
        rows = ''.join(
            f'<tr><td>{esc(chr(65 + i))}. {esc(p["left"])}</td>'
            f'<td>{esc(str(i + 1))}. {esc(q["pairs"][(i * 3 + 1) % len(q["pairs"])]["right"])}</td></tr>'
            for i, p in enumerate(q['pairs']))
        return (f'<li>{src}{esc(q["prompt"])} '
                f'<span class="ostyle">match</span>'
                f'<table class="data matchtab">'
                f'<tr><th>Item</th><th>Definitions, shuffled</th></tr>{rows}</table></li>')
    tag = ('<span class="ostyle">which two</span>' if q['style'] == 'multi' else '')
    opts = ' &nbsp; '.join(
        f'({LETTERS[i]}) {esc(o["text"])}' for i, o in enumerate(q['options']))
    return f'<li>{src}{esc(q["prompt"])} {tag} &nbsp; {opts}</li>'


def answer_block(qs):
    rows = []
    for n, q in enumerate(qs, 1):
        if q['style'] == 'match':
            pairs = ''.join(
                f'<li><b>{esc(p["left"])}</b> goes with {esc(p["right"])}</li>'
                for p in q['pairs'])
            rows.append(f'<p class="oq"><b>{n}.</b> The pairing, in full. '
                        f'{esc(q["explanation"])}</p>'
                        f'<ul class="whys match">{pairs}</ul>')
            continue
        ans = q['answer'] if isinstance(q['answer'], list) else [q['answer']]
        keys = [o for o in q['options'] if o['id'] in ans]
        named = ' and '.join(f'<b>{esc(o["text"].rstrip("."))}</b>' for o in keys)
        lead = ('The two answers are ' if len(keys) > 1 else 'The answer is ')
        parts = [f'<p class="oq"><b>{n}.</b> {lead}{named}. '
                 f'{esc(q.get("explanation", ""))}</p>']
        items = []
        for o in q['options']:
            mark = 'ok' if o['id'] in ans else 'no'
            items.append(f'<li class="{mark}"><b>{esc(o["text"].rstrip("."))}.</b> '
                         f'{esc(q["why"][o["id"]])}</li>')
        parts.append('<ul class="whys">' + ''.join(items) + '</ul>')
        rows.append(''.join(parts))
    return '\n'.join(rows)


HOWTO = """<section>
<div class="kick">Objective Section</div>
<h2 class="title">How to Attack an Objective Question</h2>
<hr class="rule">
<p class="lead">The paper carries an objective section as well as its three written
questions, and it is answered under more time pressure than anything else on it.
This part is where you practise that half.</p>

<div class="box teach"><div class="bar"><span>Teach</span><span class="tag">what is here, and where it came from</span></div>
<div class="body">
<p>Both class tests are reproduced below, thirty questions each, sixty in all,
grouped by the part of this book that teaches them rather than by which test they
came from, so that a run of questions drills one topic at a time. Every option is
explained, the right one and the wrong ones alike.</p>
<p>The stems and options were read off the test screenshots by eye. That is a
weaker guarantee than the two written papers in this book carry, since those are
held character for character against a transcript by a gate, and it is said here
rather than left for you to assume.</p>
</div></div>

<div class="box trap"><div class="bar"><span>Trap</span><span class="tag">the form that costs marks all by itself</span></div>
<div class="body">
<p>The lecturer named test two's format as the one the examination will use, and
test two is <b>multi-select</b>: a question that asks which <b>TWO</b> of the
options are correct. Test one was single-answer. That difference is worth real
marks on its own, and it is the reason this part exists in the form it does.</p>
<p>On a which-two question, <b>both</b> choices must be right for the mark. A
candidate who knows the topic perfectly and stops at the first correct option
scores nothing. So the habit to build is: read all four options every time, decide
about each one separately, and only then count how many you have marked. If you
have marked one, or three, you have not finished the question.</p>
<p>The other habit is that the two correct options usually do different jobs. A
typical pair is one option that NAMES the thing and one that states its PURPOSE,
as in the balancing question below: one says the practice is called balancing, the
other says why it is done. Looking for that split makes the pair easier to find
than hunting for two statements that both feel true.</p>
</div></div>

<div class="box keypoint"><div class="bar"><span>Key point</span></div>
<div class="body">
<p class="formal">In a four-option question, the options that are wrong are wrong
for a reason you can state. Finding those reasons is faster and safer than
recognising the right answer, because recognition is exactly what a well-built
distractor attacks.</p>
<p class="blunt"><b>Blunt version:</b> do not hunt for the right one. Kill the
wrong ones, and on a which-two, count what is left.</p>
</div></div>

<div class="box teach"><div class="bar"><span>Teach</span><span class="tag">the four moves, in order</span></div>
<div class="body">
<ol class="steps">
<li><b>Read the stem twice and underline the instruction.</b> NOT, BEST, TWO,
PRIMARILY and EXCEPT each flip or narrow the question. A stem asking which two is a
different question from one asking which one, and the paper mixes both.</li>
<li><b>Answer it before you read the options where you can.</b> If you know a black
hole is a process with inputs and no outputs, decide that first, then read the
options as a lookup rather than as a suggestion.</li>
<li><b>Strike the impossible.</b> On these tests two of the four usually die at
once: an option that names a different concept, or one that is true of the subject
but does not answer the question asked.</li>
<li><b>On the last two, split on the exact wording.</b> It is nearly always one
word: only, all, every, eliminates, requires. An option saying a context diagram
"eliminates the need for" something is almost always the distractor.</li>
</ol>
</div></div>

<div class="box recall"><div class="bar"><span>How to use this part</span></div>
<div class="body">
<p>Sit one group at a time, timed at 45 seconds a question, with the answers
covered. Then read the whole answer block for that group, including the questions
you got right: on an objective paper a right answer for the wrong reason is a mark
you will not get twice.</p>
</div></div>
</section>
"""


def build():
    qs = load()
    check(qs)
    seen = set()
    groups = []
    for label, mods, taught in GROUPS:
        group = [q for q in qs if q['module'] in mods]
        seen.update(q['id'] for q in group)
        if group:
            groups.append((label, taught, group))
    leftover = [q for q in qs if q['id'] not in seen]
    if leftover:
        groups.append(('Across the Whole Course', 'Mixed topics.', leftover))

    out = ['<!-- ===================== OBJECTIVE SECTION ==================== -->',
           '<div class="part">',
           '  <div class="kicker">Objective Section</div>',
           '  <h1>Both Class Tests,<br>Every Option Explained</h1>',
           '  <div class="blurb">All sixty questions from the two class tests, grouped '
           'by the part of this book that teaches them, and answered in full. Not only '
           'why the answer is the answer: why each of the others is not. The which-two '
           'form is the one the examination uses, so it is the one to practise.</div>',
           '  <div class="divider-motif">',
           '    <svg viewBox="0 0 520 210" xmlns="http://www.w3.org/2000/svg" '
           'font-family="DejaVu Sans">',
           '      <text x="34" y="30" font-size="13" fill="#1d4ed8">Which TWO statements '
           'describe this practice and its purpose?</text>',
           '      <g font-size="12.5" fill="#5b6b73">',
           '        <text x="58" y="70">this practice is called gray-holing</text>',
           '        <text x="58" y="104">its purpose is to remove the context diagram</text>',
           '        <text x="58" y="138">this practice is called balancing</text>',
           '        <text x="58" y="172">its purpose is to keep parent and child '
           'consistent</text>',
           '      </g>',
           '      <g stroke="#b91c1c" stroke-width="1.6">',
           '        <line x1="54" y1="66" x2="290" y2="66"/>',
           '        <line x1="54" y1="100" x2="352" y2="100"/>',
           '      </g>',
           '      <g fill="none" stroke="#0e7490" stroke-width="2">',
           '        <circle cx="42" cy="134" r="7"/><circle cx="42" cy="168" r="7"/>',
           '      </g>',
           '    </svg>',
           '  </div>',
           '</div>',
           '',
           HOWTO]

    for label, taught, group in groups:
        out.append(f'<section>\n<div class="kick">Objective Section</div>\n'
                   f'<h2 class="title">{esc(label)}</h2>\n<hr class="rule">\n'
                   f'<p class="lead">{len(group)} questions. {esc(taught)} Cover the '
                   f'answers before you start.</p>\n')
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

    import collections
    styles = collections.Counter(q['style'] for q in qs)
    print(f'gen_objective: {len(qs)} questions in {len(groups)} groups -> '
          f'content/objective.html ({len(text)} chars)')
    print(f'  styles: {dict(styles)}')
    letters = re.compile(r'\b(?:option|choice|answer)\s+[a-h]\b|\bchoosing\s+[a-h]\b',
                         re.I)
    blocks = re.findall(r'<ul class="whys">.*?</ul>', text, re.S)
    named = [b for b in blocks if letters.search(b)]
    print(f'  answer blocks: {len(blocks)}, naming an option by its letter: {len(named)}')
    if named:
        print('  x an explanation names a letter', file=sys.stderr)
        sys.exit(1)
    print(f'  options explained: '
          f'{sum(len(q.get("options", [])) for q in qs)}')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build()
