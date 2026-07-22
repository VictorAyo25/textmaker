"""Verbatim gate: a past question is quoted as the examiner printed it, or not at all.

    cd build && python qa_verbatim.py

Methodology 4c, binding. A reader found that every manual we had shipped presented a
COMPRESSED RESTATEMENT of each past question in the author's voice, formatted as though
it were the paper. This book did it too. Two examples found while transcribing:

  * 25/26 Q6(b) prints SIX functional dependencies, fd1 to fd6, and names the targets of
    fd1 in the order "iTime, comments, staffNo, sName, carReg". Module Four printed four
    of them and reordered fd1's targets. A student revising the dropped fd5/fd6 (the two
    candidate keys) would never have met them.
  * 25/26 Q1(c) prices salaries in Naira, "greater than ₦100,000". The book wrote
    "salary > 100000", dropping the currency the examiner actually printed.

That matters because the student is training pattern recognition for the hall.
Restating strips the examiner's phrasing habits, the real part numbering, the exact mark
text and the ambiguity they must resolve under time pressure. It also launders the
paper's own defects into clean prose: 24/25 Q5(b) says "answer questions (i-vii)" and
then prints EIGHT parts; its Table 1 has no sName column though three of its FDs
determine sName. Those are evidence, not bugs to fix.

THE AUTHORITY IS THE TRANSCRIPT, NOT THIS BOOK. Each paper is transcribed by eye from
the photographs into sources/exams/transcripts/<paper>.txt. This gate compares the book
against those files. It cannot tell you a transcript is faithful to the photograph;
nothing can except reading the photograph, which was done twice per paper.

FOUR DIRECTIONS. Two is the obvious design and it is not enough, because directions 1
and 2 both work from the AS PRINTED boxes and so are structurally blind to a teaching
site that cites a paper and carries no such box.

  1. PARAPHRASE (forward). Every <div class="asprinted"> must appear in its declared
     transcript question character for character, normalising only whitespace and quote
     glyphs. Reword one word and this fails.

  2. DROPPED PART (reverse). For papers the book presents as SOLVED IN FULL, every
     question in the transcript must be quoted, and quoted whole.

  3. PROSE CITATION. In any flag note under a quote, every run inside quotation marks
     that is ATTRIBUTED to the paper must be verbatim too. Scoped by an attribution cue
     because we also write "candidate key" and "in good order" in quotation marks as our
     own words, and a gate that cries wolf stops being read (CSC241's lesson). Bare
     "read" is excluded: `Read the mark text as ...` instructs the student.

  4. LINE STRUCTURE. Directions 1 to 3 all compare whitespace-collapsed text, so all
     three are blind to a quoted LISTING whose lines were joined or re-split: every word
     is still present and in order. The reader is not blind to it, and .asprinted renders
     white-space:pre-wrap, so the structure in the file IS the structure on the page.
     Where a paper numbers the lines of a table or a listing, joining two lines silently
     renumbers the expected answer.

Plus DISCOVERY: a box that CLAIMS a past question must show that question's words.

PENDING_TRANSCRIPT is the visible register of papers this book cites but has not yet
transcribed. It is printed loudly on every run and the count is never allowed to be
silent. The book must not be published while it is non-empty.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
TRANSCRIPTS = os.path.normpath(
    os.path.join(HERE, '..', 'sources', 'exams', 'transcripts'))

# Papers whose every question the book undertakes to reproduce and answer.
# Adding a paper here makes direction 2 bite on it.
SOLVED_IN_FULL = {'2025-2026'}

# Papers the book cites but has NOT yet transcribed. Every one is outstanding
# work under methodology 4c: until a paper is here-to-empty, sites citing it are
# reported every run and the book may not be published.
PENDING_TRANSCRIPT = set()      # all seven papers are transcribed

# chip label ("PQ 25/26 Q4a") -> transcript file stem
YEAR_TO_PAPER = {
    '25/26': '2025-2026', '24/25': '2024-2025', '23/24': '2023-2024',
    '21/22': '2021-2022', '20/21': '2020-2021', '19/20': '2019-2020',
    '15/16': '2015-2016',
}

QID_RE = re.compile(r'^\[\[([A-Za-z0-9()]+)\]\]\s*$', re.M)
HAND_RE = re.compile(r'\{\{hand:.*?\}\}', re.S)
FIGURE_RE = re.compile(r'^\[Figure.*?\]\s*$', re.S | re.M)
# my aside about how the paper SETS something (underlining, italics) rather than
# what it says. One line, always closed, so it can never swallow a question.
NOTE_RE = re.compile(r'^\s*\[note:.*?\]\s*$', re.M)
# NOTE: there is deliberately NO "indented parenthetical" stripper here. An earlier
# version had one, and it silently ate the papers' own sub-parts, because a line like
# "     (i)     Relational model                    (1 mark)" is indented and ends in
# a bracket. It truncated 24/25 Q1a to its stem. It was invisible to direction 1,
# because the book quote and the transcript were sliced by the SAME rule, so a
# truncated quote matched a truncated transcript and the gate blessed it. My asides
# use the explicit [note: ...] marker instead, which cannot collide with a question.
SECTION_RE = re.compile(r'^(={5,}).*$', re.M)
RULE_LINE_RE = re.compile(r'^---.*$', re.M)

ASPRINTED_RE = re.compile(
    r'<div class="asprinted"[^>]*\bdata-src="([^"]+)"[^>]*>(.*?)</div>', re.S)
ASPRINTED_ANY_RE = re.compile(r'<div class="asprinted"(?![^>]*\bdata-src=)')
TAG_RE = re.compile(r'<[^>]+>')

FLAG_RE = re.compile(r'<p class="flag">(.*?)</p>', re.S)
NOTPAPER_RE = re.compile(r'<span class="notpaper">.*?</span>', re.S)
STRIP_BLOCK_RE = re.compile(r'<(pre|table|svg)\b.*?</\1>', re.S)
PROV_RE = re.compile(r'<span class="prov">(.*?)</span>', re.S)
# a box bar, so discovery can walk boxes in order
BOX_BAR_RE = re.compile(
    r'<div class="box (work|qpaper|ans)">\s*<div class="bar">(.*?)</div>', re.S)

# direction 3: only a run introduced by one of these is a claim about the paper.
# "read" alone is excluded on purpose (CSC241): `Read < as "less than"` teaches.
ATTRIB_RE = re.compile(
    r'(the paper|the examiner|as printed|is printed|prints|printed|reads|'
    r'states|asks|says|wording|instruction)\W+$', re.I)

_quote_lines = {}


def norm(s):
    """Normalise ONLY whitespace and quote glyphs. Everything else is evidence."""
    s = html.unescape(s)
    s = (s.replace('’', "'").replace('‘', "'")
          .replace('“', '"').replace('”', '"')
          .replace(' ', ' '))
    return re.sub(r'\s+', ' ', s).strip()


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def _slice(text):
    """Cut a transcript into {qid: body}, dropping my scaffolding and commentary."""
    first = QID_RE.search(text)
    if first:
        tail = RULE_LINE_RE.search(text, first.end())
        if tail:
            text = text[:tail.start()]
    text = HAND_RE.sub(' ', text)
    text = FIGURE_RE.sub(' ', text)
    text = NOTE_RE.sub(' ', text)
    parts = QID_RE.split(text)
    return {parts[i]: SECTION_RE.sub(' ', parts[i + 1])
            for i in range(1, len(parts) - 1, 2)}


def load_transcripts():
    out, lines = {}, {}
    if not os.path.isdir(TRANSCRIPTS):
        return out, lines
    for fname in sorted(os.listdir(TRANSCRIPTS)):
        if not fname.endswith('.txt'):
            continue
        paper = fname[:-4]
        sliced = _slice(read(os.path.join(TRANSCRIPTS, fname)))
        out[paper] = {q: norm(b) for q, b in sliced.items()}
        for q, b in sliced.items():
            lines[(paper, q)] = [l for l in (norm(x) for x in b.split('\n')) if l]
    return out, lines


def _contiguous(haystack, needle):
    """Is `needle` a run of consecutive entries of `haystack`?

    The first and last quoted lines may be a partial copy of the paper's line, so a
    site can quote from mid-sentence, but every line BETWEEN them must match whole.
    That is what makes a joined-up listing fail while a partial quote still passes.
    """
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
    quotes, undeclared = [], []
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        text = read(os.path.join(CONTENT, fname))
        if ASPRINTED_ANY_RE.search(text):
            undeclared.append(fname)
        for m in ASPRINTED_RE.finditer(text):
            src, inner = m.group(1), m.group(2)
            paper, qid = (src.split(':', 1) + [''])[:2] if ':' in src else (src, '')
            quotes.append((fname, paper, qid, norm(TAG_RE.sub(' ', inner))))
            _quote_lines[(fname, paper, qid)] = [
                TAG_RE.sub(' ', l) for l in html.unescape(inner).split('\n')]
    return quotes, undeclared


def report():
    problems, pending_hits = [], []
    _quote_lines.clear()
    tx, tx_lines = load_transcripts()
    if not tx:
        print('VERBATIM GATE: FAIL')
        print(f'  x no transcripts found in {TRANSCRIPTS}')
        return False

    quotes, undeclared = book_quotes()
    for f in sorted(set(undeclared)):
        problems.append(f'{f}: an "asprinted" quote carries no data-src, so nothing '
                        f'checks it against a transcript')

    # ---- 1. forward: every quote in the book is in the transcript, exactly ----
    for fname, paper, qid, quote in quotes:
        if paper not in tx:
            problems.append(f'{fname}: quote declares paper "{paper}", which has no '
                            f'transcript in sources/exams/transcripts/')
            continue
        if qid not in tx[paper]:
            problems.append(f'{fname}: quote declares {paper}:{qid}, which is not a '
                            f'question in that transcript')
            continue
        if quote not in tx[paper][qid]:
            problems.append(
                f'{fname}: the quote for {paper}:{qid} is NOT what the paper prints. '
                f'This is the paraphrase defect. Fix the quote, never the transcript.\n'
                f'      book : {quote[:140]}\n'
                f'      paper: {tx[paper][qid][:140]}')

    # ---- 2. reverse: nothing quietly dropped from a paper solved in full ----
    for paper in sorted(SOLVED_IN_FULL):
        if paper not in tx:
            problems.append(f'{paper} is declared SOLVED_IN_FULL but has no transcript')
            continue
        got = {}
        for _f, p, q, quote in quotes:
            if p == paper:
                got.setdefault(q, []).append(quote)
        for qid, want in sorted(tx[paper].items()):
            if qid not in got:
                problems.append(f'{paper}:{qid} is in the paper but is quoted nowhere '
                                f'in the book, though this paper is presented as '
                                f'solved in full')
            elif not any(g == want for g in got[qid]):
                longest = max(got[qid], key=len)
                problems.append(
                    f'{paper}:{qid} is quoted but not in full ({len(want) - len(longest)} '
                    f'characters of the printed question are absent). A student reading '
                    f'only the book would never meet the dropped part.')

    # ---- 4. the paper's own line breaks survive ----
    for fname, paper, qid, _flat in quotes:
        if paper not in tx or qid not in tx[paper]:
            continue
        raw = tx_lines.get((paper, qid), [])
        book = [l for l in (norm(x) for x in _quote_lines.get((fname, paper, qid), [])) if l]
        if book and raw and not _contiguous(raw, book):
            problems.append(
                f'{fname}: the quote for {paper}:{qid} keeps the words but not the '
                f"paper's own line breaks. Lines have been joined or re-split. On a "
                f'listing or a table the break is part of the question.')

    # ---- 3. attributed quotations in our flag notes are the paper's words too ----
    everything = ' || '.join(v for p in tx.values() for v in p.values())
    n_runs = n_notpaper = 0
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        text = STRIP_BLOCK_RE.sub(' ', read(os.path.join(CONTENT, fname)))
        for m in FLAG_RE.finditer(text):
            body = m.group(1)
            n_notpaper += len(NOTPAPER_RE.findall(body))
            body = NOTPAPER_RE.sub(' ', body)
            seg = norm(TAG_RE.sub('', body))
            # split on the quote char and take odd runs: a "([^"]+)" regex would pair
            # one quotation's CLOSING quote with the next one's OPENING quote and
            # report the ordinary prose between them (five phantoms of seven on COS221)
            chunks = seg.split('"')
            for i in range(1, len(chunks), 2):
                run = chunks[i].strip()
                if len(run.split()) < 2 or '...' in run:
                    continue
                if not ATTRIB_RE.search(chunks[i - 1]):
                    continue                      # our own words, not a claim
                n_runs += 1
                if run not in everything:
                    problems.append(
                        f'{fname}: a flag note attributes "{run[:70]}" to the examiner, '
                        f'but no transcript prints that. Quote it exactly, or mark it '
                        f'<span class="notpaper"> if it is deliberately not the paper.')

    # ---- discovery: every box that CLAIMS a past question shows its words ----
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        text = read(os.path.join(CONTENT, fname))
        prev = 0
        for m in BOX_BAR_RE.finditer(text):
            bar, span = m.group(2), text[prev:m.start()]
            prev = m.end()
            chips = ' '.join(TAG_RE.sub('', c) for c in PROV_RE.findall(bar))
            years = {YEAR_TO_PAPER[y] for y in re.findall(r'(\d\d/\d\d)', chips)
                     if y in YEAR_TO_PAPER}
            if not years:
                continue
            if 'class="asprinted"' in span:
                continue
            live = years - PENDING_TRANSCRIPT
            if live:
                problems.append(
                    f'{fname}: a box chipped "{chips.strip()}" presents a real exam '
                    f'question but no quote of it stands above the solution. A reader '
                    f'meets the question only in our words.')
            else:
                pending_hits.append(f'{fname}: {chips.strip()}')

    # ---- the styling the rule depends on ----
    css = read(os.path.join(HERE, 'manual.css'))
    for cls in ('.asprinted', '.paper .flag', '.unpack'):
        if cls not in css:
            problems.append(f'manual.css: {cls} style is gone, so quoted paper text no '
                            f'longer looks different from our own prose')
    if quotes and not any('As printed' in read(os.path.join(CONTENT, f))
                          for f in sorted(os.listdir(CONTENT)) if f.endswith('.html')):
        problems.append('the book quotes a paper but carries no visible "As printed" '
                        'bar, so a reader cannot tell the examiner\'s words from ours')

    papers_seen = sorted({p for _f, p, _q, _t in quotes})
    print(f'VERBATIM GATE: {len(quotes)} quoted questions across {len(papers_seen)} '
          f'papers, checked against {len(tx)} transcripts')
    for paper in sorted(tx):
        have = len({q for _f, p, q, _t in quotes if p == paper})
        mark = 'solved in full' if paper in SOLVED_IN_FULL else 'cited selectively'
        print(f'  . {paper}: {have}/{len(tx[paper])} questions quoted ({mark})')

    if PENDING_TRANSCRIPT:
        print(f'  ! {len(PENDING_TRANSCRIPT)} papers are NOT YET TRANSCRIBED: '
              f'{", ".join(sorted(PENDING_TRANSCRIPT))}')
        print(f'  ! {len(pending_hits)} sites cite them and still show the question in '
              f'OUR words. This book MUST NOT be published until that is zero:')
        for h in pending_hits:
            print(f'      - {h}')

    if problems:
        print('VERBATIM GATE: FAIL')
        for p in problems:
            print('  x ' + p)
        return False
    print('  . every quoted question matches its transcript character for character')
    print('  . every question of every paper solved in full is quoted, and quoted whole')
    print("  . every quote keeps the paper's own line breaks, so a listing is not reflowed")
    print(f'  . {n_runs} attributed quotations in flag notes are the paper\'s own words '
          f'({n_notpaper} marked notpaper)')
    print('  . every site citing a TRANSCRIBED paper shows that paper\'s words')
    return True


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    sys.exit(0 if report() else 1)
