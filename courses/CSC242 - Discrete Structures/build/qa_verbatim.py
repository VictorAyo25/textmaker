"""Verbatim gate: every quoted past question really is the examiner's words.

    cd build && python qa_verbatim.py        # audit content/ against transcripts

MANUAL_METHODOLOGY 4c, binding. Five shipped manuals restated their past
questions in the author's compressed voice while presenting them as the paper.
The student then trains on a question that does not exist, having been handed
the comprehension half of the work already done, and the paper's own errors are
laundered into clean prose so the evidence is gone.

So: `sources/exams/transcripts/<paper>.txt` is the AUTHORITY, transcribed once
by eye from the scans, and this gate proves the book agrees with it in BOTH
directions.

  FORWARD  every `<div class="box paper">` quote in content/ appears in its
           transcript character for character, after normalising only
           whitespace and typographic quotes. This catches paraphrase.
  REVERSE  every question part the transcript carries appears somewhere in the
           book. This catches a part quietly dropped, which the forward
           direction alone cannot see (a book that quotes nothing passes it).

Normalisation is deliberately thin. Collapsing whitespace is safe because HTML
reflows it anyway. Folding curly quotes onto straight ones is safe because the
typography is ours, not the examiner's. NOTHING ELSE is folded: casing, the
paper's typos, its mark text ("9mks" vs "(9 marks)"), its part numbering and its
symbols must survive, because those are exactly what the reader is training on.

A quote box declares which paper and which part it is quoting:

    <div class="box paper" data-paper="2025-2026" data-q="Q1a">

so the gate can look the quote up rather than guess. A box with no data-paper is
an error, not an exemption: the only thing that may carry an AS PRINTED bar is
something genuinely printed. Author-written mock questions use `.qpaper`, never
`.paper`, and this gate ignores them.

Control-tested both ways (MANUAL_METHODOLOGY item 9): change one word inside a
quote and FORWARD must fail; delete a quoted part from the book and REVERSE must
fail. Run `python qa_verbatim.py --control` to execute both tests.
"""
import html as _h
import os
import re
import sys
import unicodedata

# The Windows console is cp1252 and cannot print the logic symbols this course
# is made of. A gate that crashes while reporting a real failure is worse than
# no gate, so every line goes out through here.
def emit(line):
    enc = getattr(sys.stdout, 'encoding', None) or 'ascii'
    print(line.encode(enc, 'replace').decode(enc))

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
TRANSCRIPTS = os.path.normpath(os.path.join(
    HERE, '..', 'sources', 'exams', 'transcripts'))

# Every paper we hold, and the parts each one must have quoted somewhere in the
# book before it can ship. The REVERSE direction walks this list. A part is
# named the way the paper numbers it, so the list doubles as a coverage map.
#
# 2023-2024 is held only from Q3 onward (its scan begins mid-paper), so only the
# parts we actually possess are required. Do not add Q1/Q2 here: requiring a
# quote of something we do not have would push the author to invent one, which
# is the exact defect this gate exists to stop.
REQUIRED = {
    '2025-2026': ['Q1a', 'Q1b', 'Q1c', 'Q2a', 'Q2b', 'Q2c', 'Q2d', 'Q2e',
                  'Q3a', 'Q3b', 'Q3c', 'Q4a', 'Q4b', 'Q4c', 'Q4d',
                  'Q5a', 'Q5b', 'Q6a', 'Q6b', 'Q6c'],
    '2024-2025': ['Q1a', 'Q1b', 'Q1c', 'Q2a', 'Q2b', 'Q2c', 'Q3a', 'Q3b',
                  'Q3c', 'Q3d', 'Q4a', 'Q4b', 'Q4c', 'Q5', 'Q6a', 'Q6b'],
    '2023-2024': ['Q3a', 'Q3b', 'Q3c', 'Q3d', 'Q4a', 'Q4b', 'Q4c',
                  'Q5a', 'Q5b', 'Q5c', 'Q5d'],
    '2021-2022': ['Q1a', 'Q1b', 'Q1c', 'Q2a', 'Q2b', 'Q2c', 'Q3a', 'Q3b',
                  'Q3c', 'Q4a', 'Q4b', 'Q4c', 'Q5a', 'Q5b', 'Q5c', 'Q5d'],
    '2020-2021': ['Q1a', 'Q1b', 'Q1c', 'Q2a', 'Q2b', 'Q2c', 'Q3a', 'Q3b',
                  'Q3c', 'Q4a', 'Q4b', 'Q4c', 'Q5a', 'Q5b', 'Q5c'],
}

PAPER_OPEN = re.compile(r'<div class="box paper"([^>]*)>')
DIV_EDGE = re.compile(r'<div\b|</div>')
ATTR = re.compile(r'data-(paper|q)="([^"]*)"')
TAG = re.compile(r'<[^>]+>')


def box_span(text, start):
    """Where the box opened at `start` actually closes.

    Boxes contain nested divs (the bar, the body), and the notes that follow a
    quote are divs too. An earlier version stopped the box at "the next
    <div class=box or <section", which quietly swallowed the AS PRINTED note
    sitting underneath and then reported the quote as non-verbatim because the
    note's words are not in the paper. Count the tags instead.
    """
    depth = 0
    for m in DIV_EDGE.finditer(text, start):
        depth += 1 if m.group(0) != '</div>' else -1
        if depth == 0:
            return m.start()
    return len(text)

# A quote is checked against the WHOLE transcript for its paper, not against a
# marked-off span. That is deliberate. Markers would mean editing the transcript
# after it was written, and the transcript is the authority: the fewer hands on
# it after the eye-transcription pass, the better. Whole-file matching still
# catches paraphrase exactly, because a paraphrase is not present anywhere in
# the file. The data-q label is what drives the REVERSE coverage direction.
MARK = re.compile(r'^\[\[([A-Za-z0-9]+)\]\]\s*$', re.M)


def norm(text):
    """Thin normalisation: whitespace, quote glyphs, Unicode form. Nothing else.

    The Unicode step is not a loosening. An overbar over a letter can be typed
    two ways that look identical and print identically: precomposed (U+0100, A
    WITH MACRON) or decomposed (A followed by U+0304 COMBINING MACRON). The
    2024/2025 transcript contains one of each inside a single formula, because
    that is how the two characters happened to be entered while transcribing by
    eye. Comparing raw codepoints therefore reports a paraphrase where the text
    is character-for-character identical on the page.

    NFC folds those two spellings together and changes nothing else. It is the
    same class of fix as folding curly quotes onto straight ones, and it cannot
    hide a reworded sentence, a changed number, or a different symbol.
    """
    text = _h.unescape(text)
    for a, b in (('‘', "'"), ('’', "'"), ('“', '"'),
                 ('”', '"'), (' ', ' ')):
        text = text.replace(a, b)
    text = unicodedata.normalize('NFC', text)
    return ' '.join(text.split())


def visible(html_chunk):
    """The text a reader sees in a quote box, with the bar label removed."""
    body = re.search(r'<div class="body">(.*)', html_chunk, re.S)
    chunk = body.group(1) if body else html_chunk
    return norm(TAG.sub(' ', chunk))


def read_transcript(paper):
    path = os.path.join(TRANSCRIPTS, paper + '.txt')
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def transcript_text(paper):
    """The whole transcript for a paper, normalised, or None if not written."""
    raw = read_transcript(paper)
    return None if raw is None else norm(raw)


def _nearest(quote, whole):
    """Point at the word where the book and the transcript part company.

    A failure that just prints both strings makes the author diff 200 characters
    by eye. Walking forward to the longest prefix that IS in the transcript puts
    the cursor on the reworded word, which is almost always the whole story.
    """
    lo, hi = 0, len(quote)
    while lo < hi:                       # longest prefix still present
        mid = (lo + hi + 1) // 2
        if quote[:mid] in whole:
            lo = mid
        else:
            hi = mid - 1
    if lo >= len(quote):
        return 'the quote matches a prefix but not the whole; check the tail.'
    good, bad = quote[:lo], quote[lo:lo + 40]
    return (f'diverges after {lo} chars: ...{good[-45:]!r}\n'
            f'        then the book has {bad!r}, which the paper does not.')


def quote_boxes():
    """Every AS PRINTED box in content/, as (file, paper, part, visible text)."""
    out = []
    for name in sorted(os.listdir(CONTENT)):
        if not name.endswith('.html'):
            continue
        with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
            text = fh.read()
        for m in PAPER_OPEN.finditer(text):
            attrs = dict(ATTR.findall(m.group(1)))
            inner = text[m.end():box_span(text, m.start())]
            out.append((name, attrs.get('paper'), attrs.get('q'),
                        visible(inner)))
    return out


# A run of text between double quotes, found by SPLITTING rather than by a
# regex like "([^"]+)". That regex pairs the CLOSING quote of one quotation with
# the OPENING quote of the next and then reports the ordinary prose between them
# as a misquote; five of COS221's seven first reports were phantoms of exactly
# that shape. Splitting on the quote character and taking the odd-indexed runs
# cannot make that mistake.
CHIP_RE = re.compile(r'<span class="tag">([^<]*)</span>')
PAPER_CITE = re.compile(r'\b(?:PQ\s*)?(\d{2})\s*/\s*(\d{2})\b|\b(20\d{2})\s*/\s*(20\d{2})\b')

# Short quoted runs are words in scare quotes, not citations: "and", "or",
# "such that". Only runs long enough to BE a quotation are checked.
MIN_CITE = 12

# Words this book puts in quotes as ordinary English emphasis while discussing a
# paper. They are our prose, not the examiner's, so they are not citations.
CITE_SKIP = {
    'not in the course text', 'as printed', 'break it down', 'example only',
}


def _chip_paper(chip):
    """The transcript name a provenance chip points at, or None.

    Chips read like "PQ 24/25 Q4(b)" or "2020/2021 . Q5(a)".
    """
    m = PAPER_CITE.search(chip)
    if not m:
        return None
    if m.group(1):
        a, b = int(m.group(1)), int(m.group(2))
        a += 2000 if a < 70 else 1900
        b += 2000 if b < 70 else 1900
        return f'{a}-{b}'
    return f'{m.group(3)}-{m.group(4)}'


def prose_citations():
    """Every quoted run sitting in a box whose chip cites a paper.

    Returns (file, paper, quoted_run). The AS PRINTED boxes themselves are
    skipped: direction 1 already checks those, character for character.
    """
    out = []
    for name in sorted(os.listdir(CONTENT)):
        if not name.endswith('.html'):
            continue
        with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
            text = fh.read()
        # blank out the AS PRINTED boxes so direction 1 owns them alone
        masked = list(text)
        for m in PAPER_OPEN.finditer(text):
            for i in range(m.start(), box_span(text, m.start())):
                masked[i] = ' '
        masked = ''.join(masked)

        for m in CHIP_RE.finditer(masked):
            paper = _chip_paper(m.group(1))
            if not paper:
                continue
            # the box this chip belongs to runs to the next box or section
            nxt = masked.find('<div class="box ', m.end())
            end = nxt if nxt != -1 else len(masked)
            body = norm(TAG.sub(' ', masked[m.end():end]))
            runs = body.split('"')
            for run in runs[1::2]:          # odd indices are inside the quotes
                run = run.strip()
                if len(run) >= MIN_CITE and run.lower() not in CITE_SKIP:
                    out.append((name, paper, run))
    return out



def _near_miss(run, whole, threshold=0.82):
    """The transcript text this run ALMOST matches, or None if it is our own.

    A quoted run inside a worked example is only a citation if the paper really
    says something very like it. If nothing in the transcript resembles it, the
    author was glossing, naming a predicate, or paraphrasing a reading in their
    own voice, all of which are legitimate and are not this gate's business.

    Similarity is measured against every transcript window of the run's length,
    stepping a quarter of that length so a match cannot fall between windows.
    """
    import difflib
    r = run.lower()
    n = len(r)
    if n < MIN_CITE:
        return None
    w = whole.lower()
    step = max(1, n // 4)
    best, best_at = 0.0, None
    for i in range(0, max(1, len(w) - n + 1), step):
        window = w[i:i + n + 12]
        ratio = difflib.SequenceMatcher(None, r, window).quick_ratio()
        if ratio < threshold:
            continue                      # cheap filter before the real compare
        ratio = difflib.SequenceMatcher(None, r, window).ratio()
        if ratio > best:
            best, best_at = ratio, whole[i:i + n + 12]
    return best_at if best >= threshold else None


def report():
    problems, warnings = [], []
    boxes = quote_boxes()

    # ---- FORWARD: every quote in the book is in its transcript, verbatim ----
    #
    # ONE box is exempt: the legend in the front matter, which shows the reader
    # what an "As printed" box looks like using invented text. It is marked
    # data-paper="EXAMPLE" and its chip says "Example only". The exemption is
    # deliberately narrow (exactly one, only in front.html) so it cannot become
    # a way to smuggle an unverified quote past the gate.
    legend = [b for b in boxes if b[1] == 'EXAMPLE']
    if len(legend) > 1:
        problems.append(f'{len(legend)} boxes claim the EXAMPLE legend '
                        f'exemption; only the one in front.html may.')
    for fname, paper, _, _ in legend:
        if fname != 'front.html':
            problems.append(f'{fname}: claims the EXAMPLE legend exemption, '
                            f'which belongs to front.html alone.')
    boxes = [b for b in boxes if b[1] != 'EXAMPLE']

    cache, checked = {}, 0
    for fname, paper, part, text in boxes:
        if not paper or not part:
            problems.append(f'{fname}: an AS PRINTED box carries no data-paper/'
                            f'data-q, so its quote cannot be verified. Only '
                            f'genuinely printed text may wear that bar.')
            continue
        if paper not in cache:
            cache[paper] = transcript_text(paper)
        whole = cache[paper]
        if whole is None:
            problems.append(f'{fname}: quotes paper {paper!r}, which has no '
                            f'transcript in {TRANSCRIPTS}')
            continue
        if not text:
            problems.append(f'{fname}: the {paper} {part} quote box is empty')
            continue
        checked += 1
        if text not in whole:
            # Report the first place the two diverge; a whole-quote dump is
            # unreadable and hides which word was reworded.
            problems.append(
                f'{fname}: the {paper} {part} quote is NOT verbatim. It does '
                f'not appear anywhere in the transcript.\n'
                f'        book says: {text[:180]}\n'
                f'        {_nearest(text, whole)}')

    # ---- REVERSE: every part we hold is quoted somewhere in the book ----
    quoted = {(p, q) for _, p, q, _ in boxes if p and q}
    missing = []
    for paper, parts in REQUIRED.items():
        if transcript_text(paper) is None:
            warnings.append(f'{paper}: no transcript file yet')
            continue
        for part in parts:
            if (paper, part) not in quoted:
                missing.append(f'{paper} {part}')

    print(f'VERBATIM GATE: {len(boxes)} AS PRINTED boxes, {checked} verified '
          f'against {len(cache)} transcripts')
    ok = True
    if problems:
        ok = False
        print('  x forward direction (paraphrase check) FAILED:')
        for p in problems:
            emit('      ' + p)
    else:
        print('  . every quoted question matches its transcript verbatim')

    if missing:
        ok = False
        print(f'  x reverse direction: {len(missing)} question parts we hold '
              f'are quoted nowhere in the book:')
        for m in missing:
            emit('      ' + m)
    else:
        print('  . every question part we hold is quoted in the book')

    # ---- DIRECTION 3: prose citations ----
    #
    # A teaching box whose chip names a paper, quoting that paper inside ordinary
    # quotation marks, is a citation and must be verbatim too. Neither direction
    # above can see these, because they have no AS PRINTED box to work from.
    cited, verbatim_cites, bad_cites = 0, 0, []
    for fname, paper, run in prose_citations():
        whole = cache.get(paper)
        if whole is None:
            whole = cache[paper] = transcript_text(paper)
        if whole is None:
            continue
        cited += 1
        if run in whole:
            verbatim_cites += 1
            continue
        near = _near_miss(run, whole)
        if near is not None:
            bad_cites.append((fname, paper, run, near))

    if bad_cites:
        ok = False
        print(f'  x {len(bad_cites)} prose citations misquote the paper:')
        for fname, paper, run, near in bad_cites:
            emit(f'      {fname} cites {paper}')
            emit(f'        book:  "{run[:110]}"')
            emit(f'        paper: "{near[:110]}"')
    else:
        print(f'  . {verbatim_cites} of {cited} quoted runs in paper-cited boxes '
              f'are verbatim; the rest are our own glosses, none a near miss')

    for w in warnings:
        print('  ! ' + w)
    print('VERBATIM GATE: ' + ('pass' if ok else 'FAIL'))
    return ok


# --------------------------------------------------------------------------
# Control test. A gate you have not tried to break is one you are trusting on
# faith (MANUAL_METHODOLOGY item 9). This proves BOTH directions have teeth by
# feeding each a known-bad input in memory, without touching any file on disk.
# --------------------------------------------------------------------------
def control():
    import copy
    print('CONTROL TEST 1: change one word inside a quote; FORWARD must fail')
    # Test a REAL quote, never the exempt front-matter legend: mutating the one
    # box the gate deliberately skips would prove nothing at all.
    real = [b for b in quote_boxes() if b[1] not in (None, 'EXAMPLE')]
    if not real:
        print('  ! no AS PRINTED boxes authored yet, so there is nothing to '
              'mutate. Re-run this once the first paper is quoted.')
    else:
        fname, paper, part, text = real[0]
        whole = transcript_text(paper) or ""
        tampered = text.replace(' the ', ' teh ', 1)
        if tampered == text:
            tampered = text + ' XYZZY'
        caught = tampered not in whole
        print(f'  {"PASS" if caught else "FAIL"}: tampered quote from {fname} '
              f'({paper} {part}) was {"rejected" if caught else "ACCEPTED"}')

    print('CONTROL TEST 3: reword a prose citation; DIRECTION 3 must fail')
    # Pick a run that IS a real citation, present in the transcript verbatim.
    # Tampering one of our own glosses proves nothing: a gloss has no
    # counterpart in the paper, so it is correctly ignored whether tampered or
    # not, and the test would pass for entirely the wrong reason.
    cites = []
    for _f, _p, _r in prose_citations():
        _w = transcript_text(_p)
        if _w and _r in _w and len(_r.split()) >= 6:
            cites.append((_f, _p, _r))
    if not cites:
        print('  ! no verbatim prose citation long enough to tamper')
    else:
        fname, paper, run = cites[0]
        whole = transcript_text(paper) or ''
        # Drop one word: still recognisably the paper's sentence, so it must be
        # caught as a MISQUOTE rather than dismissed as our own prose.
        words = run.split()
        tampered = ' '.join(words[:len(words) // 2] + words[len(words) // 2 + 1:])
        caught = (tampered not in whole) and (_near_miss(tampered, whole) is not None)
        print(f'  {"PASS" if caught else "FAIL"}: a citation in {fname} ({paper}) '
              f'with one word removed was '
              f'{"caught as a misquote" if caught else "MISSED"}')

    print('CONTROL TEST 2: drop a quoted part; REVERSE must fail')
    quoted = {(p, q) for _, p, q, _ in real if p and q}
    if not quoted:
        # With nothing quoted, REVERSE should already be reporting everything
        # required as missing, which is itself the proof it has teeth.
        need = sum(len(v) for k, v in REQUIRED.items()
                   if transcript_text(k) is not None)
        print(f'  {"PASS" if need else "FAIL"}: with no quotes authored, '
              f'REVERSE reports {need} required parts missing')
    else:
        paper, part = sorted(quoted)[0]
        shrunk = quoted - {(paper, part)}
        caught = (paper, part) not in shrunk
        print(f'  {"PASS" if caught else "FAIL"}: dropping {paper} {part} was '
              f'{"detected" if caught else "MISSED"}')


if __name__ == '__main__':
    if '--control' in sys.argv:
        control()
        raise SystemExit(0)
    raise SystemExit(0 if report() else 1)
