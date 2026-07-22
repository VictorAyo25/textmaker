#!/usr/bin/env python
"""qa_verbatim.py -- every quoted past question really is the examiner's words.

MANUAL_METHODOLOGY 4c. A past question is QUOTED, never restated. This gate holds
every AS PRINTED box in the book against a plain-text transcript of the real paper
and fails in BOTH directions:

  paraphrase   a quoted line that is not in the transcript. This is the defect the
               rule exists for: a compressed restatement presented as the paper.
  dropped part a question in the transcript that appears nowhere in the book. A
               solved paper that quietly skips a part looks complete, because
               nothing in the PDF disagrees with anything else in the PDF.

Only ONE direction would be worthless on its own. Checking the book against the
transcript alone would pass a book that quotes one question perfectly and omits
five. Checking the transcript against the book alone would pass a book that quotes
accurately and then adds an invented question. Both, or neither.

The transcript is eye-typed from a scan (the papers have no text layer). That makes
it the one input here no machine can verify, so it is the authority ONLY because it
was typed slowly and re-read against the image. A transcript paraphrased while
typing turns this gate into a rubber stamp for the paraphrase. See 4c.

Run standalone, or as a hard gate from assemble.py.
"""
import io, os, re, sys, unicodedata
import html as htmllib

# The papers print glyphs (the naira sign) that a cp1252 console cannot encode.
# A gate that crashes while reporting a defect is a gate that hides it.
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
TRANSCRIPTS = os.path.normpath(os.path.join(HERE, '..', 'sources', 'exams', 'transcripts'))

# Question text lives in .qtext paragraphs inside a <div class="box paper">.
PAPER_BOX_RE = re.compile(r'<div class="box paper">(?P<body>.*?)\n\s*</div>\s*\n\s*</div>', re.S)
QTEXT_RE = re.compile(r'<p class="qtext[^"]*">(?P<t>.*?)</p>', re.S)
TAG_RE = re.compile(r'<[^>]+>')
BAR_RE = re.compile(r'<span>AS PRINTED &middot;\s*(?P<t>[^<]*)</span>')

# A quoted line short enough to be a fragment of layout rather than a claim about
# the paper (a bare "Example", a lone bullet marker) is not worth matching on.
MIN_LEN = 12
# How much of a paper part must be found in the book for it to count as covered.
PART_HEAD = 45


def norm(s, tags=True):
    """Whitespace and typography only. Never words.

    `tags=False` for plain-text input (the transcripts). Stripping HTML tags from
    plain text is not a no-op, it is destructive: once the paper is joined into
    one line, the tag pattern happily matches from a "<" inside one listing to a
    ">" inside a later one and deletes everything between them. That silently
    removes real questions from the haystack and reports them as paraphrased.

    Collapsing runs of space and unifying quote glyphs is safe: neither changes
    what the examiner asked. Anything beyond that would start forgiving exactly
    the paraphrase this gate exists to catch, so nothing beyond that is done.

    Tags are stripped BEFORE unescaping, never after. The paper writes literal
    angle brackets ("Vehicle speed: <speed> km/h"), which the HTML holds as
    &lt;speed&gt;. Unescaping first turns that into <speed>, and the tag stripper
    then eats it, so the quote silently loses a word and the gate reports a
    paraphrase that is not there. Found exactly that way on 24/25 Q5 D.
    """
    if tags:
        s = TAG_RE.sub('', s)
    s = htmllib.unescape(s)
    s = unicodedata.normalize('NFKC', s)
    s = (s.replace('“', '"').replace('”', '"')
          .replace('‘', "'").replace('’', "'")
          .replace('−', '-').replace('–', '-').replace('—', '-')
          .replace('→', '->').replace('≥', '>=').replace('≤', '<=')
          .replace(' ', ' ').replace('•', '*'))
    return re.sub(r'\s+', ' ', s).strip()


def strip_marker(s):
    """Drop a part label ('A.', 'iii.', 'a.') and any mark annotation.

    The mark allocation is printed in the paper's right margin, and the book
    carries it in its own span rather than inline, so its POSITION differs on the
    two sides even when the wording is identical. It is metadata about the
    question, not the question, so it is removed from both sides rather than
    being allowed to manufacture false paraphrase reports.
    """
    s = re.sub(r'[\[(]\s*\d+(?:\.\d+)?\s*marks?\s*[\])]', ' ', s, flags=re.I).strip()
    s = re.sub(r'^\[?\d+(\.\d+)?\s*marks?\]?\s*', '', s, flags=re.I)
    s = re.sub(r'^\[[^\]]*marks?\]\s*', '', s, flags=re.I)
    s = re.sub(r'^(?:[A-Za-z]{1,4}|[ivxIVX]{1,5})[.)]\s*', '', s)
    s = re.sub(r'^[*\-]\s*', '', s)
    return s.strip()


def load_transcripts():
    out = {}
    if not os.path.isdir(TRANSCRIPTS):
        return out
    for fn in sorted(os.listdir(TRANSCRIPTS)):
        if not fn.endswith('.txt'):
            continue
        raw = io.open(os.path.join(TRANSCRIPTS, fn), encoding='utf-8').read()
        # transcriber's notes are not the paper
        raw = re.sub(r'<<.*?>>', ' ', raw, flags=re.S)
        out[fn[:-4]] = raw
    return out


# A part label at the start of a line: "A.", "iii.", "b.", "*", "Part 1:".
MARKER_RE = re.compile(r'^\s*(?:[A-Za-z]{1,4}[.)]|[*]|Part\s+\d+:)\s+')
# Lines that are code, not prose. The transcript prints listings as the paper does.
CODE_RE = re.compile(r'[{};]\s*$|^\s*(?:public|private|int|double|for|while|if|else|'
                     r'return|import|System|}|\{)\b|^\s*\d+\s+\S')
SKIP_RE = re.compile(r'^\s*(?:\[\[page|={5,}|TRANSCRIPT OF|Conventions used|'
                     r'COVENANT|CANAANLAND|P\.M\.B|B\.Sc|COLLEGE:|SESSION:|COURSE|'
                     r'DEPARTMENT:|SEMESTER:|CREDIT|TIME:|Time Allowed|TITLE OF|'
                     r'INSTRUCTIONS?:|Instructions:|Question\s|SECTION\s|Index\s|Amount\s)')


def transcript_blob(raw):
    """The whole paper as one normalised string, for containment tests.

    The transcript hard-wraps long questions to stay readable next to the scan,
    so a quoted sentence routinely spans two or three transcript lines. Comparing
    line against line therefore reports paraphrase everywhere and is useless. The
    paper is one stream of words; treat it as one.
    """
    return norm(' '.join(raw.split('\n')), tags=False)


def transcript_parts(raw):
    """The paper's instruction parts, each rejoined from its wrapped lines.

    Used only for the coverage direction: is any part of the paper quoted
    nowhere? Continuation lines are folded into the part they belong to, and
    code listings are excluded, because a listing is quoted as a listing, not as
    a .qtext line.
    """
    parts, cur = [], None
    for ln in raw.split('\n'):
        if not ln.strip():
            cur = None
            continue
        if SKIP_RE.match(ln) or CODE_RE.search(ln):
            cur = None
            continue
        if MARKER_RE.match(ln):
            if cur:
                parts.append(cur)
            cur = strip_marker(norm(ln, tags=False))
        elif cur is not None:
            cur += ' ' + norm(ln, tags=False)
    if cur:
        parts.append(cur)
    parts = [strip_marker(p) for p in parts]
    verb = re.compile(r'\b(define|describe|state|write|debug|dry run|identify|find|'
                      r'create|determine|explain|what is|what will|design|implement|'
                      r'prompt|using|use|ensure|scan|display|show|convert|change|'
                      r'retain|call|read|handle|loop|deposit|perform|demonstrate)\b', re.I)
    return [p for p in parts if len(p) >= MIN_LEN and verb.search(p)]


def collect_quotes():
    """Every .qtext line in every AS PRINTED box, with where it came from."""
    quotes = []
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.endswith('.html'):
            continue
        doc = io.open(os.path.join(CONTENT, fn), encoding='utf-8').read()
        for box in PAPER_BOX_RE.finditer(doc):
            body = box.group('body')
            bar = BAR_RE.search(body)
            title = norm(bar.group('t')) if bar else '?'
            line_no = doc[:box.start()].count('\n') + 1
            for qm in QTEXT_RE.finditer(body):
                t = strip_marker(norm(qm.group('t')))
                if len(t) >= MIN_LEN:
                    quotes.append((f'{fn[:-5]}:{line_no}', title, t))
    return quotes


def main():
    fails, notes = [], []
    trans = load_transcripts()
    if not trans:
        print('FAIL: no transcripts in ' + TRANSCRIPTS)
        print('      A past question cannot be gated against nothing. Transcribe each')
        print('      paper verbatim first (MANUAL_METHODOLOGY 4c).')
        return 1

    blob = {k: transcript_blob(v) for k, v in trans.items()}
    parts = {k: transcript_parts(v) for k, v in trans.items()}

    quotes = collect_quotes()
    if not quotes:
        print('FAIL: no <div class="box paper"> quotations found in content/.')
        print('      Either no past question is quoted, or the box class changed and')
        print('      this gate has gone blind. Both are failures.')
        return 1

    # ---- direction 1: everything the book QUOTES must be in a transcript --------
    for where, title, q in quotes:
        if not any(q in b for b in blob.values()):
            fails.append((where, title, q))

    # ---- direction 2: every question in a transcript must appear in the book ----
    # Coverage, not wording: direction 1 already proved the wording. A part counts
    # as present if a recognisable opening run of it was quoted somewhere, which
    # tolerates the book splitting one long part across several .qtext lines.
    qblob = ' | '.join(q for _, _, q in quotes)
    for paper, plist in parts.items():
        for p in plist:
            head = p[:PART_HEAD]
            if head not in qblob:
                notes.append((paper, p))

    print('=' * 72)
    print('qa_verbatim: quoted past questions vs the transcripts of the real papers')
    print('=' * 72)
    print(f'transcripts   : {", ".join(sorted(trans))}')
    print(f'quoted lines  : {len(quotes)} in AS PRINTED boxes')
    print()

    if fails:
        print(f'FAIL: {len(fails)} quoted line(s) are NOT in any transcript.')
        print('      A line here is presented to the student as the examiner\'s words')
        print('      but is not what the paper says. Fix the quote, not the transcript.')
        for where, title, q in fails[:40]:
            print(f'  [{where}] {title}')
            print(f'      {q[:150]}')
    else:
        print('PASS: every quoted line appears verbatim in a transcript.')

    print()
    if notes:
        print(f'FAIL: {len(notes)} instruction line(s) in the papers are quoted nowhere.')
        print('      A dropped part is invisible: the book still agrees with itself.')
        for paper, ln in notes[:40]:
            print(f'  [{paper}] {ln[:150]}')
    else:
        print('PASS: every instruction line in every transcript is quoted in the book.')

    print()
    bad = len(fails) + len(notes)
    print(f'{"FAIL" if bad else "OK"}: {len(fails)} paraphrased, {len(notes)} dropped.')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
