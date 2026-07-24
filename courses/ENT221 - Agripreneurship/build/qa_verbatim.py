"""Verbatim gate (ENT221): a real test question is quoted as it appeared, or not at all.

    cd build && python qa_verbatim.py

Methodology 4c, binding. The defect it guards against is presenting a COMPRESSED
RESTATEMENT of a past question in our own words, formatted as though it were the paper,
so a student revises against wording that never existed. For ENT221 the "papers" are the
two CBT tests, transcribed by eye from the screenshots into
sources/exams/transcripts/test1.txt and test2.txt. THE AUTHORITY IS THE TRANSCRIPT.

The book quotes each real question inside a <div class="asprinted" data-src="testN"
data-q="M"> block (the dark AS PRINTED bar). Module DRILLS are author practice, chipped
"Practice", and quote nothing as the paper, so they are not checked here. An illustrative
example carries data-src="example" and is skipped.

DIRECTIONS (adapted to a many-short-question CBT):
  1. PARAPHRASE (forward). Every asprinted quote must appear in its declared transcript
     question, character for character (normalising only whitespace, quote glyphs and
     superscripts). Reword one word and this fails.
  2. DROPPED (reverse). Both tests are SOLVED_IN_FULL, so every question in each transcript
     must be quoted somewhere in the book.
  3. LINE STRUCTURE. .asprinted renders white-space:pre-wrap, so the option lines in the
     file are the option lines on the page. Each quoted line must appear, in order and
     adjacent, in the transcript's line sequence: joining a stem to its first option, or
     two options, silently changes what the reader trains on.
  4. DISCOVERY / DECLARATION. An asprinted with no data-src is unchecked and fails; every
     (test, q) a box claims must resolve to a transcript question.

Direction 3 of the essay-paper gate (prose citations attributed to "the examiner") is
deliberately omitted: ENT221 makes no such citations, and our prose DOES quote the course
TEXT (e.g. "Total Bacterial Count"), which has no transcript, so running it would cry wolf.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
TRANSCRIPTS = os.path.normpath(os.path.join(HERE, '..', 'sources', 'exams', 'transcripts'))

# Tests whose every question the book undertakes to quote and answer.
SOLVED_IN_FULL = {'test1', 'test2'}

SEP_RE = re.compile(r'^={10,}\s*$', re.M)
QHEAD_RE = re.compile(r'^\s*Q(\d+)\.\s*(.*)$')
TAG_RE = re.compile(r'<[^>]+>')
# an asprinted block; data-q is optional so an undeclared one is still detected
ASPRINTED_RE = re.compile(
    r'<div class="asprinted"[^>]*\bdata-src="([^"]+)"(?:[^>]*\bdata-q="([^"]+)")?[^>]*>(.*?)</div>',
    re.S)
ASPRINTED_ANY_RE = re.compile(r'<div class="asprinted"(?![^>]*\bdata-src=)')
SUP_RE = re.compile(r'<sup>(.*?)</sup>', re.S)

_SUPERSCRIPT = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹',
                             '0123456789')


def norm(s):
    """Normalise ONLY whitespace, quote glyphs and superscript digits. Else is evidence."""
    s = html.unescape(s)
    s = (s.replace('’', "'").replace('‘', "'")
          .replace('“', '"').replace('”', '"')
          .replace(' ', ' ').translate(_SUPERSCRIPT))
    return re.sub(r'\s+', ' ', s).strip()


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def _clean_line(ln):
    """A transcript line reduced to the paper's own words, or None if it is our annotation."""
    s = ln.strip()
    if not s:
        return None
    if s.startswith('ANSWER:') or s.startswith('NOTE:') or s.startswith('[INTENTIONALLY'):
        return None
    if s.startswith('[') and s.endswith(']'):     # a bare tag line, e.g. [fill in the gap]
        return None
    s = re.sub(r'\s*\[CORRECT\]', '', s)
    s = re.sub(r'\s*\[VERIFY GLYPH:[^\]]*\]', '', s)
    return s.strip() or None


def load_transcripts():
    """{test: {qid: paper-words}} plus {(test, qid): [line, ...]} for the structure check."""
    flat, lines = {}, {}
    if not os.path.isdir(TRANSCRIPTS):
        return flat, lines
    for fname in sorted(os.listdir(TRANSCRIPTS)):
        if not fname.endswith('.txt'):
            continue
        test = fname[:-4]
        flat[test] = {}
        for block in SEP_RE.split(read(os.path.join(TRANSCRIPTS, fname))):
            qid = None
            body = []
            started = False
            for ln in block.split('\n'):
                m = QHEAD_RE.match(ln)
                if m and qid is None:
                    qid, started = m.group(1), True
                    continue                       # the header line is not paper words
                if not started:
                    continue
                cl = _clean_line(ln)
                if cl is not None:
                    body.append(cl)
            if qid is not None and body:           # Q4 (intentionally omitted) has no body
                flat[test][qid] = norm('\n'.join(body))
                lines[(test, qid)] = [norm(x) for x in body if norm(x)]
    return flat, lines


def _contiguous(haystack, needle):
    """Is `needle` a run of consecutive lines of `haystack` (first/last may be partial)?"""
    if not needle:
        return True
    n = len(needle)
    for i in range(len(haystack) - n + 1):
        w = haystack[i:i + n]
        if n == 1:
            if needle[0] in w[0]:
                return True
            continue
        if (needle[0] in w[0] and needle[-1] in w[-1]
                and all(a == b for a, b in zip(needle[1:-1], w[1:-1]))):
            return True
    return False


def book_quotes():
    """(fname, test, qid, flat-quote, [line, ...]) for every declared asprinted; + undeclared."""
    quotes, undeclared = [], []
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        text = read(os.path.join(CONTENT, fname))
        if ASPRINTED_ANY_RE.search(text):
            undeclared.append(fname)
        for m in ASPRINTED_RE.finditer(text):
            src, qid, inner = m.group(1), m.group(2) or '', m.group(3)
            if src == 'example':
                continue
            unsup = SUP_RE.sub(r'\1', inner)       # 10<sup>5</sup> -> 105, no phantom space
            stripped = TAG_RE.sub(' ', unsup)
            qlines = [norm(x) for x in html.unescape(unsup).split('\n')]
            quotes.append((fname, src, qid, norm(stripped), [l for l in qlines if l]))
    return quotes, undeclared


def report():
    problems = []
    tx, tx_lines = load_transcripts()
    if not tx:
        print('VERBATIM GATE: FAIL')
        print(f'  x no transcripts found in {TRANSCRIPTS}')
        return False

    quotes, undeclared = book_quotes()
    for f in sorted(set(undeclared)):
        problems.append(f'{f}: an "asprinted" quote carries no data-src, so nothing checks '
                        f'it against a transcript')

    # ---- 1. forward: every quote is in its transcript question, exactly ----
    for fname, test, qid, quote, _ql in quotes:
        if test not in tx:
            problems.append(f'{fname}: quote declares test "{test}", which has no transcript')
        elif qid not in tx[test]:
            problems.append(f'{fname}: quote declares {test} Q{qid}, not a question in that transcript')
        elif quote not in tx[test][qid]:
            problems.append(
                f'{fname}: the quote for {test} Q{qid} is NOT what the test prints (paraphrase '
                f'defect). Fix the quote, never the transcript.\n'
                f'      book : {quote[:130]}\n'
                f'      test : {tx[test][qid][:130]}')

    # ---- 2. reverse: nothing dropped from a test solved in full ----
    for test in sorted(SOLVED_IN_FULL):
        if test not in tx:
            problems.append(f'{test} is declared SOLVED_IN_FULL but has no transcript')
            continue
        got = {q for _f, t, q, _s, _l in quotes if t == test}
        for qid in sorted(tx[test], key=int):
            if qid not in got:
                problems.append(f'{test} Q{qid} is in the test but quoted nowhere, though '
                                f'{test} is presented as solved in full')

    # ---- 3. line structure: the option lines are not joined or re-split ----
    for fname, test, qid, _quote, qlines in quotes:
        if test in tx and qid in tx[test]:
            raw = tx_lines.get((test, qid), [])
            if qlines and raw and not _contiguous(raw, qlines):
                problems.append(
                    f'{fname}: the quote for {test} Q{qid} keeps the words but not the test\'s '
                    f'own line breaks (stem and options joined or re-split).')

    # ---- the styling the rule depends on ----
    css = read(os.path.join(HERE, 'manual.css'))
    for cls in ('.asprinted', '.paper', '.unpack'):
        if cls not in css:
            problems.append(f'manual.css: {cls} style is gone, so quoted test text no longer '
                            f'looks different from our prose')

    print(f'VERBATIM GATE: {len(quotes)} quoted questions checked against {len(tx)} transcripts')
    for test in sorted(tx):
        have = len({q for _f, t, q, _s, _l in quotes if t == test})
        print(f'  . {test}: {have}/{len(tx[test])} questions quoted (solved in full)')

    if problems:
        print('VERBATIM GATE: FAIL')
        for p in problems:
            print('  x ' + p)
        return False
    print('  . every quoted question matches its transcript character for character')
    print('  . every question of both tests is quoted (nothing dropped)')
    print("  . every quote keeps the test's own line breaks (options not reflowed)")
    return True


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    sys.exit(0 if report() else 1)
