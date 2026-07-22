"""Past questions must be QUOTED, not restated (MANUAL_METHODOLOGY 4c).

    cd build && python qa_verbatim.py            # checks the assembled book
    cd build && python qa_verbatim.py _body.html

The defect this exists to stop: presenting a compressed restatement of a real
examination question in our own voice, formatted as though it were the paper.
The student is training pattern recognition for the hall, and a paraphrase
strips the examiner's phrasing, the real part numbering, the exact mark text and
the ambiguity they must resolve under time pressure. It also launders the
paper's own typos into clean prose, destroying evidence.

The transcripts in sources/exams/transcripts/ are the AUTHORITY. They are read
by eye from photographs, which makes them the one input no machine can check, so
this gate cannot prove the transcript is right. It can only prove the BOOK
matches it, which is why the transcripts carry their own transcriber's notes and
were re-read against the images once before any quote was inserted.

THREE directions, not two:

  1. paraphrase   every quoted run in the book appears in a transcript,
                  character for character.
  2. coverage     every question in a FULL transcript is quoted somewhere in
                  the book. Runs only against transcripts marked SCOPE: FULL:
                  a PARTIAL transcript holds only the fragments the book cites,
                  and demanding the rest be reproduced would be wrong.
  3. citation     in any box that is NOT an AS PRINTED box but cites a paper,
                  every run inside quotation marks must be verbatim too.

Direction 3 is the one that gets forgotten, and directions 1 and 2 are
structurally blind to it: both work from AS PRINTED boxes, and these sites have
none. COS221 shipped two misquotes of exactly this kind.

Two mechanical traps, both guarded below:
  * QUOTE PAIRING. A regex like "([^"]+)" pairs the CLOSING quote of one
    quotation with the OPENING quote of the next and reports the ordinary prose
    between them as a misquote. Five of COS221's seven first reports were
    phantoms from this. Split on the quote character and take odd-indexed runs.
  * CODE IS NOT QUOTATION. Strip <pre> and <table> before scanning prose, or
    every string literal in a listing is read as a claim about the paper.
"""
import html as _html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TDIR = os.path.join(HERE, '..', 'sources', 'exams', 'transcripts')

PAPER_BOX = re.compile(r'<div class="box paper">(.*?)\n  </div>', re.S)
ANY_BOX = re.compile(r'<div class="box ([a-z ]+)">(.*?)\n  </div>', re.S)
QTEXT = re.compile(r'<(p|span|li)[^>]*class="[^"]*qtext[^"]*"[^>]*>(.*?)</\1>', re.S)
ASPRINTED = re.compile(r'<pre class="asprinted">(.*?)</pre>', re.S)
BAR_TAG = re.compile(r'<div class="bar">.*?</div>', re.S)
PRE_OR_TABLE = re.compile(r'<pre\b.*?</pre>|<table\b.*?</table>', re.S)
CITES_PAPER = re.compile(r'20\d\d/20\d\d|\b\d\d/\d\d\b|the paper|the examiner')
# Words that turn a quotation into a claim about what the paper actually says.
# NOT bare "read": "Read < as \"strictly less than\"" instructs the student, it
# does not attribute anything to an examiner. The attributive form is "reads"
# ("the paper reads"), and keeping only that removed the last false positive.
ATTRIBUTES = re.compile(
    r'\b(paper|examiner|printed|prints|reads|states|stated|says|said|asks|'
    r'asked|wording|worded|quoted|question)\b[^.]{0,60}$', re.I)
# a question stem in a transcript: "a) ..." at the start of a line
Q_STEM = re.compile(r'^([a-z])\)\s+(.{12,90})', re.M)

MIN_RUN = 12          # ignore very short quoted runs: "e", "w", "Hi"


def norm(s):
    """Whitespace and typographic quotes ONLY. Never words, never dashes.

    Dashes carry meaning here (the paper's en dash is evidence), so they are
    left exactly as transcribed. Normalising them would hide the very
    difference the gate exists to detect.
    """
    s = _html.unescape(s)
    s = (s.replace('‘', "'").replace('’', "'")
          .replace('“', '"').replace('”', '"'))
    return re.sub(r'\s+', ' ', s).strip()


def text_of(fragment):
    return norm(re.sub(r'<[^>]+>', ' ', fragment))


def load_transcripts():
    out = {}
    if not os.path.isdir(TDIR):
        sys.exit(f'no transcripts directory: {TDIR}')
    for fn in sorted(os.listdir(TDIR)):
        if not fn.endswith('.txt'):
            continue
        raw = open(os.path.join(TDIR, fn), encoding='utf-8').read()
        full = re.search(r'^SCOPE:\s*FULL', raw, re.M) is not None
        partial = re.search(r'^SCOPE:\s*PARTIAL', raw, re.M) is not None
        if not (full or partial):
            full = True          # a transcript with no marker is a whole paper
        # everything after the transcriber's notes is commentary, not the paper
        body = re.split(r"TRANSCRIBER'S NOTES", raw)[0]
        out[fn] = {'norm': norm(body), 'raw': body, 'full': full}
    return out


def quoted_runs(prose):
    """Runs inside double quotes that are ATTRIBUTED to the paper.

    Pairing: split on the quote character and take odd indices. With 2n quotes
    the odd positions are exactly the quoted runs, and the prose between one
    closing quote and the next opening quote lands on an even index where it
    belongs. A regex like "([^"]+)" instead pairs the closing quote of one
    quotation with the opening quote of the next and reports that prose as a
    misquote: five of COS221's seven first reports were this artifact.

    Attribution: being inside a box that cites a paper is not enough. We also
    write "strictly less than" and "and we got all the way through", which are
    our own words in quotation marks and are no claim about any paper. Checking
    those against the transcript reports a misquote that is not one, and a gate
    that cries wolf stops being read. So a run counts only when the prose
    immediately before it attributes it: the paper, the examiner, printed,
    reads, states, asks. Everything else is ordinary emphasis and is skipped.
    """
    parts = prose.split('"')
    if len(parts) % 2 == 0:          # unbalanced quotes: cannot pair reliably
        return []
    out = []
    for k in range(1, len(parts), 2):
        run = parts[k]
        if len(run.strip()) < MIN_RUN:
            continue
        before = parts[k - 1][-90:]
        if ATTRIBUTES.search(before):
            out.append(run)
    return out


def check(book_html):
    T = load_transcripts()
    fails, n_quotes, n_runs = [], 0, 0

    # ---------------------------------------------------------- 1. paraphrase
    for m in PAPER_BOX.finditer(book_html):
        box = m.group(1)
        where = text_of(BAR_TAG.search(box).group(0)) if BAR_TAG.search(box) else '?'
        runs = [text_of(g) for _, g in QTEXT.findall(box)]
        runs += [norm(_html.unescape(g)) for g in ASPRINTED.findall(box)]
        n_quotes += 1
        for r in runs:
            if not r:
                continue
            n_runs += 1
            if not any(r in t['norm'] for t in T.values()):
                fails.append(f'[paraphrase] {where}: quoted text is not in any '
                             f'transcript, character for character:\n        {r[:150]}')

    # ------------------------------------------------------------ 2. coverage
    book_quoted = ' '.join(
        text_of(g) + ' ' + ' '.join(norm(_html.unescape(p))
                                    for p in ASPRINTED.findall(m.group(1)))
        for m in PAPER_BOX.finditer(book_html)
        for _, g in QTEXT.findall(m.group(1)))
    n_cov = 0
    for fn, t in T.items():
        if not t['full']:
            continue
        for letter, stem in Q_STEM.findall(t['raw']):
            n_cov += 1
            probe = norm(stem)[:60]
            if probe not in book_quoted:
                fails.append(f'[dropped part] {fn} has ({letter}) but the book '
                             f'never quotes it:\n        {probe}')

    # ------------------------------------------------------------ 3. citation
    n_cited = 0
    for m in ANY_BOX.finditer(book_html):
        cls, box = m.group(1), m.group(2)
        if 'paper' in cls.split():
            continue                      # direction 1 already owns these
        prose = PRE_OR_TABLE.sub(' ', box)          # code is not quotation
        prose = text_of(prose)
        if not CITES_PAPER.search(prose):
            continue
        n_cited += 1
        for run in quoted_runs(prose):
            r = norm(run)
            n_runs += 1
            if not any(r in t['norm'] for t in T.values()):
                fails.append(f'[prose citation] a box citing a paper quotes text '
                             f'that is not in any transcript:\n        "{r[:150]}"')

    print(f'VERBATIM GATE: {len(T)} transcript(s), {n_quotes} AS PRINTED boxes, '
          f'{n_runs} quoted runs checked')
    if fails:
        print('VERBATIM GATE: FAIL')
        for f in fails:
            print('  x ' + f)
        return False
    print(f'  . every quoted run appears in a transcript, character for character')
    print(f'  . every question in a full transcript is quoted in the book '
          f'({n_cov} checked)')
    print(f'  . {n_cited} boxes cite a paper in prose; every quoted run in them '
          f'is verbatim too')
    return True


def report(book_html):
    return check(book_html)


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else '_body.html'
    with open(os.path.join(HERE, src), encoding='utf-8') as fh:
        sys.exit(0 if check(fh.read()) else 1)
