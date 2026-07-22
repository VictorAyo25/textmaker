"""Verbatim gate: a past question is quoted as the examiner printed it, or not at all.

    cd build && python qa_verbatim.py

Methodology 4c, binding. A reader found that every manual we had shipped
presented a *compressed restatement* of each past question in the author's voice,
formatted as though it were the paper. The 24/25 Q1(a) really opens "Consider
three (3) floating point numbers X, Y and Z stored in registers based on the IEEE
754 Single precision floating point format"; this book had said "X = C1400000H,
Y = 42100000H, Z = 41400000H are stored in IEEE-754 single precision". Same
substance, different sentence, and the student reads it as the paper.

That matters because the student is training pattern recognition for the hall.
Restating strips the examiner's phrasing habits, the real part numbering, the
exact mark text, the padding words and the ambiguity they must resolve under time
pressure. It also launders the paper's own typos into clean prose: this paper
prints "Special Locality", an 11-bit row under a "Use 12 bits" instruction, and
"in using Single Precision IEEE format". Those are evidence, not bugs to fix.

THE AUTHORITY IS THE TRANSCRIPT, NOT THIS BOOK. Each paper was transcribed by eye
from the photographs into sources/exams/transcripts/<paper>.txt before any
solution was written. This gate compares the book against those files. It cannot
tell you the transcript is faithful to the photograph; nothing can except reading
the photograph, which was done twice. What it CAN do is guarantee that no quote in
the book has drifted from the transcript, in either direction:

  1. FORWARD, catches paraphrase. Every <div class="asprinted"> in the book must
     appear in its declared transcript question character for character, after
     normalising only whitespace and quote glyphs. Reword one word and this fails.

  2. REVERSE, catches quietly dropped parts. For the papers the book presents as
     SOLVED IN FULL, every question in the transcript must be quoted, and quoted
     whole. Drop a part and this fails.

The two directions are not redundant. The forward one alone would pass a book that
quoted three of five questions perfectly; the reverse one alone would pass a book
that mentioned all five and paraphrased them all.

Papers the book only cites selectively (23/24, 20/21) are held to the forward
direction and reported for coverage, not failed on it. A book is allowed to weight
itself to recent papers; it is not allowed to misquote the ones it does use.
"""
import html
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
TRANSCRIPTS = os.path.normpath(
    os.path.join(HERE, '..', 'sources', 'exams', 'transcripts'))

# Papers whose every question the book undertakes to reproduce and answer.
# Adding a paper here makes the reverse direction bite on it.
SOLVED_IN_FULL = {'2024-2025', '2025-2026'}

# Scaffolding in the transcripts that is mine, not the examiner's, and so must
# come out before comparing. Each is a shape that cannot occur in printed text.
QID_RE = re.compile(r'^\[\[([A-Za-z0-9]+)\]\]\s*$', re.M)
HAND_RE = re.compile(r'\{\{hand:.*?\}\}', re.S)       # handwritten-alteration note
FIGURE_RE = re.compile(r'^\[Figure.*?\]\s*$', re.S | re.M)  # my description of a drawing
PAREN_NOTE_RE = re.compile(r'^\s{2,}\(.*?\)\s*$', re.M)     # my indented aside
SECTION_RE = re.compile(r'^(={5,}|---).*$', re.M)           # my rules and headers

# The paper prints a block heading, "Question Three (20 marks)", above each of
# the five questions. It belongs to the question it heads, not to the lettered
# part it happens to follow on the page, but the [[Qxx]] markers cut the file
# part by part, so the heading of the NEXT block lands at the tail of the LAST
# part of the previous one. Without this, the book would have to reproduce
# "Question Three (20 marks)" inside the AS PRINTED box for Q2(c) to be counted
# as quoting Q2(c) in full. The heading is not dropped from the book: it is the
# tag on the answer box that opens each question. Matched only when it dangles
# at the very END of a part, so a heading inside a quoted question is untouched.
TRAILING_HEAD_RE = re.compile(
    r'\n[ \t]*Question\s+(?:One|Two|Three|Four|Five)\s*\(\s*\d+\s*[Mm]arks\s*\)\s*\Z',
    re.M)
# Each transcript closes with the transcriber's own commentary ("NOTES ON THE
# PAPER'S OWN DEFECTS", "ENCODING NOTE"). It sits after the last question, so the
# final slice of every paper would otherwise carry a page of my prose and no book
# could ever quote that question "in full". Everything from the first ruled line
# AFTER the questions start is mine; the ruled lines before them (the identity
# block, the rubric) are already dropped with the preamble.
RULE_LINE_RE = re.compile(r'^---.*$', re.M)

ASPRINTED_RE = re.compile(
    r'<div class="asprinted"[^>]*\bdata-src="([^"]+)"[^>]*>(.*?)</div>', re.S)
# an asprinted that forgot its data-src, which would silently escape the gate
ASPRINTED_ANY_RE = re.compile(r'<div class="asprinted"(?![^>]*\bdata-src=)', re.S)
TAG_RE = re.compile(r'<[^>]+>')

# filled by book_quotes(): {(file, paper, qid): [raw line, ...]}, used by check 2b
_quote_lines = {}

# check 2d: glyphs whose loss changes meaning and which a transcriber flattens
# without noticing. Sub/superscript digits, degree, micro, plus-minus, fractions.
MEANINGFUL_GLYPHS = (
    [chr(c) for c in range(0x2070, 0x20A0)] + ['°', 'µ', '±', '¼', '½', '¾'])
# "I looked at the photograph; the paper does not print this; the OCR layer
# invented it." Per paper, so the exemption is specific and reviewable.
GLYPH_VERIFIED_ABSENT = {}
_SRC_PDFS = {'2023-2024': '2023-2024.pdf', '2020-2021': '2020-2021.pdf'}


def _source_glyphs():
    """{paper: set of meaningful glyphs present in that PDF's text layer}

    Only papers supplied as PDFs can be probed; the photographed ones (24/25,
    25/26) have no layer at all and are covered only by reading them twice.
    """
    out = {}
    exams = os.path.normpath(os.path.join(HERE, '..', 'sources', 'exams'))
    try:
        import fitz
    except ImportError:
        return out
    for paper, fname in _SRC_PDFS.items():
        path = os.path.join(exams, fname)
        if not os.path.exists(path):
            continue
        try:
            with fitz.open(path) as doc:
                text = ''.join(p.get_text() for p in doc)
        except Exception:
            continue
        found = {c for c in text if c in MEANINGFUL_GLYPHS}
        if found:
            out[paper] = found
    return out


# check 2c: our note under a quote, where every quotation is a claim about the paper
FLAG_RE = re.compile(r'<p class="flag">(.*?)</p>', re.S)
# a run we deliberately show as NOT the paper's words (a bad restatement, a wrong
# mark format). Named so the exemption is visible and countable, never silent.
NOTPAPER_RE = re.compile(r'<span class="notpaper">.*?</span>', re.S)
# listings and tables carry string literals and cell text that are not claims
STRIP_BLOCK_RE = re.compile(r'<(pre|table)\b.*?</\1>', re.S)


def norm(s):
    """Normalise ONLY whitespace and quote glyphs. Everything else is evidence.

    Case, dashes, digits, spacing inside numbers, mark text ("9mks" vs
    "9 marks"), stray apostrophes and the paper's typos all survive, because
    every one of them is something the student must recognise in the hall.
    """
    s = html.unescape(s)
    s = (s.replace('’', "'").replace('‘', "'")
          .replace('“', '"').replace('”', '"')
          .replace(' ', ' '))
    return re.sub(r'\s+', ' ', s).strip()


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def load_transcripts():
    """{paper: {qid: normalised question text}}"""
    out = {}
    if not os.path.isdir(TRANSCRIPTS):
        return out
    for fname in sorted(os.listdir(TRANSCRIPTS)):
        if not fname.endswith('.txt'):
            continue
        paper = fname[:-4]
        text = read(os.path.join(TRANSCRIPTS, fname))
        first = QID_RE.search(text)
        if first:
            tail = RULE_LINE_RE.search(text, first.end())
            if tail:                       # drop my closing commentary
                text = text[:tail.start()]
        text = HAND_RE.sub(' ', text)
        text = FIGURE_RE.sub(' ', text)
        text = PAREN_NOTE_RE.sub(' ', text)
        parts = QID_RE.split(text)
        # parts = [preamble, qid, body, qid, body, ...]
        qs = {}
        for i in range(1, len(parts) - 1, 2):
            body = SECTION_RE.sub(' ', parts[i + 1])
            body = TRAILING_HEAD_RE.sub(' ', body)
            qs[parts[i]] = norm(body)
        out[paper] = qs
    return out


def load_transcript_lines():
    """{(paper, qid): [normalised line, ...]} keeping the paper's own line breaks.

    Same slicing as load_transcripts(), but the lines are kept apart instead of
    being flattened, so check 2b can compare layout as well as wording.
    """
    out = {}
    if not os.path.isdir(TRANSCRIPTS):
        return out
    for fname in sorted(os.listdir(TRANSCRIPTS)):
        if not fname.endswith('.txt'):
            continue
        paper = fname[:-4]
        text = read(os.path.join(TRANSCRIPTS, fname))
        first = QID_RE.search(text)
        if first:
            tail = RULE_LINE_RE.search(text, first.end())
            if tail:
                text = text[:tail.start()]
        text = HAND_RE.sub(' ', text)
        text = FIGURE_RE.sub(' ', text)
        text = PAREN_NOTE_RE.sub(' ', text)
        parts = QID_RE.split(text)
        for i in range(1, len(parts) - 1, 2):
            body = SECTION_RE.sub('\n', parts[i + 1])
            body = TRAILING_HEAD_RE.sub('\n', body)
            lines = [norm(l) for l in body.split('\n')]
            out[(paper, parts[i])] = [l for l in lines if l]
    return out


def _contiguous(haystack, needle):
    """Is `needle` a run of consecutive entries of `haystack`?

    Allows the first and last quoted lines to be a partial copy of the paper's
    line, since a site may legitimately quote from mid-sentence, but every line
    BETWEEN them must match whole. That is what makes a joined-up listing fail
    while a genuine partial quote still passes.
    """
    if not needle:
        return True
    n = len(needle)
    for i in range(len(haystack) - n + 1):
        window = haystack[i:i + n]
        if n == 1:
            if needle[0] in window[0]:
                return True
            continue
        if (needle[0] in window[0] and needle[-1] in window[-1]
                and all(a == b for a, b in zip(needle[1:-1], window[1:-1]))):
            return True
    return False


def book_quotes():
    """[(file, paper, qid, normalised quote)] plus any quote missing its data-src"""
    quotes, undeclared = [], []
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        text = read(os.path.join(CONTENT, fname))
        for m in ASPRINTED_ANY_RE.finditer(text):
            undeclared.append(fname)
        for m in ASPRINTED_RE.finditer(text):
            src = m.group(1)
            inner = m.group(2)
            body = norm(TAG_RE.sub(' ', inner))
            if ':' in src:
                paper, qid = src.split(':', 1)
            else:
                paper, qid = src, ''
            quotes.append((fname, paper, qid, body))
            # keep the quote's own line structure for check 2b. Tags are dropped
            # per line, not across the block, so a <span> never merges two lines.
            _quote_lines[(fname, paper, qid)] = [
                TAG_RE.sub(' ', l) for l in html.unescape(inner).split('\n')]
    return quotes, undeclared


def report():
    problems = []
    _quote_lines.clear()
    tx = load_transcripts()
    tx_lines = load_transcript_lines()
    if not tx:
        print('VERBATIM GATE: FAIL')
        print(f'  x no transcripts found in {TRANSCRIPTS}')
        return False

    quotes, undeclared = book_quotes()
    for fname in sorted(set(undeclared)):
        problems.append(f'{fname}: an "asprinted" quote carries no data-src, so '
                        f'nothing checks it against a transcript')

    # ---- 1. forward: every quote in the book is in the transcript, exactly ----
    for fname, paper, qid, quote in quotes:
        if paper not in tx:
            problems.append(f'{fname}: quote declares paper "{paper}", which has '
                            f'no transcript in sources/exams/transcripts/')
            continue
        if qid not in tx[paper]:
            problems.append(f'{fname}: quote declares {paper}:{qid}, which is not '
                            f'a question in that transcript')
            continue
        if quote not in tx[paper][qid]:
            problems.append(
                f'{fname}: the quote for {paper}:{qid} is NOT what the paper '
                f'prints. This is the paraphrase defect. Fix the quote, never '
                f'the transcript.\n'
                f'      book: {quote[:150]}\n'
                f'      paper: {tx[paper][qid][:150]}')

    # ---- 2. reverse: nothing quietly dropped from a paper we solve in full ----
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
                problems.append(f'{paper}:{qid} is in the paper but is quoted '
                                f'nowhere in the book, though this paper is '
                                f'presented as solved in full')
            elif not any(g == want for g in got[qid]):
                longest = max(got[qid], key=len)
                missing = len(want) - len(longest)
                problems.append(
                    f'{paper}:{qid} is quoted but not in full ({missing} '
                    f'characters of the printed question are absent). A student '
                    f'reading only the book would never meet the dropped part.')

    # ---- 2b. the paper's own line breaks survive ----
    # Checks 1 and 2 compare text with whitespace collapsed, so they cannot see a
    # quote whose lines have been joined up or re-split. That matters because
    # .asprinted renders with white-space:pre-wrap, so the line structure a reader
    # sees IS the structure in the file. Straightening a paper's wrapping is the
    # same class of edit as rewording it: on an instruction listing or a table row
    # the line break carries the meaning. (Methodology 4c, and the COS221 lesson:
    # wrap a too-wide quoted listing where the PAPER wraps it, never to taste.)
    #
    # So every non-empty line of a quote must appear, in order and adjacent, in the
    # transcript's own line sequence for that question.
    for fname, paper, qid, _flat in quotes:
        if paper not in tx or qid not in tx[paper]:
            continue                      # already reported by check 1
        raw = tx_lines.get((paper, qid), [])
        book = [norm(l) for l in _quote_lines.get((fname, paper, qid), [])]
        book = [l for l in book if l]
        if not book or not raw:
            continue
        if not _contiguous(raw, book):
            problems.append(
                f'{fname}: the quote for {paper}:{qid} keeps the words but not the '
                f'paper\'s own line breaks. Lines have been joined or re-split. '
                f'Quote the layout as printed; on a listing or a table the break '
                f'is part of the question.')

    # ---- 2c. quoted runs inside our own flag notes are the paper's words too ----
    # Found on COS221, which shipped with a two-direction gate and still carried two
    # misquotes: prose that cited a paper inside quotation marks while teaching, at
    # sites with no AS PRINTED box for either gate to work from. IFT222 had eight of
    # them, all in flag notes, mostly a silently capitalised first letter ("Show all
    # necessary work..." for the paper's "show all...", "Any 2" for "any 2") and two
    # compressed rewordings. Small, and exactly the defect in miniature: a sentence
    # in quotation marks that the examiner did not write.
    #
    # The flag note is the right scope because it exists solely to comment on the
    # paper's wording, so every quotation in it is a claim about that wording. The
    # break-it-down rows are NOT checked: they legitimately quote model answers and
    # bad answers to warn against, which are ours.
    #
    # Two mechanical traps, both hit on COS221 and avoided here:
    #   * a regex like "([^"]+)" pairs one quotation's closing quote with the next
    #     one's opening quote and reports the prose between them as a misquote. Split
    #     on the quote character and take the odd indices instead.
    #   * strip <pre> and <table> first, or every string literal inside a listing
    #     reads as a claim about the paper.
    # Deliberate counter-examples (showing what the paper does NOT say) are wrapped
    # in <span class="notpaper">, which is named, styled and counted, so the
    # exemption is visible rather than a silent hole.
    everything_q = ' || '.join(v for p in tx.values() for v in p.values())
    n_runs = n_notpaper = 0
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        text = STRIP_BLOCK_RE.sub(' ', read(os.path.join(CONTENT, fname)))
        for m in FLAG_RE.finditer(text):
            body = m.group(1)
            n_notpaper += len(NOTPAPER_RE.findall(body))
            body = NOTPAPER_RE.sub(' ', body)      # our words, deliberately shown
            seg = norm(TAG_RE.sub('', body))
            for run in seg.split('"')[1::2]:       # odd indices, never the between
                run = run.strip()
                if len(run.split()) < 2 or '...' in run:
                    continue                        # a term, or an elided quote
                n_runs += 1
                if run not in everything_q:
                    problems.append(
                        f'{fname}: a flag note puts "{run[:80]}" in quotation marks '
                        f'as the examiner\'s words, but no paper prints that. Quote '
                        f'it exactly, or mark it <span class="notpaper"> if it is '
                        f'deliberately not the paper.')

    # ---- 2d. did the TRANSCRIBER flatten a glyph the paper actually prints? ----
    # The one hole nothing else can reach. Every other check proves the book agrees
    # with the transcript; none can prove the transcript agrees with the photograph,
    # so a transcript that quietly flattened something is a gate that blesses the
    # error. COS221 hit this exactly: superscripts flattened to ^3, a dropped degree
    # sign, a hyphenated word split by rewrapping, all four invisible to its gate.
    # This book had one, found by the check below: the 23/24 paper sets its code
    # converter's variables as X and Y with TRUE subscript digits, and the first
    # pass typed them as X1, X0, Y3 ... which would have been blessed forever.
    #
    # Where a source PDF carries a text layer we do not otherwise trust (the 23/24
    # OCR turns truth-table cells into Korean), the PRESENCE of a meaningful glyph
    # is still a reliable signal of where one sits on the page. So: if the layer
    # contains a script, degree, micro or fraction character and the transcript for
    # that paper contains none of that character at all, stop and make a human look
    # at the photograph. Recording it in GLYPH_VERIFIED_ABSENT is how you say "I
    # looked, the paper does not print it, the layer hallucinated it".
    for paper, chars in sorted(_source_glyphs().items()):
        if paper not in tx:
            continue
        body = ''.join(tx[paper].values())
        for ch in sorted(chars):
            if ch in GLYPH_VERIFIED_ABSENT.get(paper, ''):
                continue
            if ch not in body:
                problems.append(
                    f'{paper}: the source PDF\'s text layer contains {ch!r} '
                    f'(U+{ord(ch):04X}, {unicodedata.name(ch, "?")}) but the '
                    f'transcript contains no such character anywhere. Look at the '
                    f'photograph: either the transcript flattened it, which no '
                    f'other check can catch, or the layer invented it, in which '
                    f'case add it to GLYPH_VERIFIED_ABSENT[{paper!r}].')

    # ---- 3. discovery: every site that CLAIMS a past question shows its words ----
    # Checks 1 and 2 both work from the quotes that exist. Neither notices a site
    # that has no quote at all. The control test proved it: deleting the quote from
    # a module worked example was NOT caught, because papers.html still quoted that
    # question, so the paper was still covered "somewhere". But the teaching site
    # had quietly gone back to presenting an exam question with no examiner's words
    # anywhere near it, which is the original defect returning by the back door.
    #
    # So: any worked example whose chip cites a year (PQ 25/26 Q1b) must have a
    # quote between it and the previous worked example. Chips citing only a class
    # test are exempt, because no test has a transcript and inventing one would be
    # worse than omitting it.
    WORK_BAR = re.compile(
        r'<div class="box work"><div class="bar"><span>Worked example</span>'
        r'<span class="tag">([^<]*)</span>')
    YEAR = re.compile(r'\d\d/\d\d')
    for fname in sorted(os.listdir(CONTENT)):
        if not fname.endswith('.html'):
            continue
        text = read(os.path.join(CONTENT, fname))
        prev = 0
        for m in WORK_BAR.finditer(text):
            tag = m.group(1)
            span = text[prev:m.start()]
            prev = m.end()
            if not YEAR.search(tag):
                continue
            if 'class="asprinted"' not in span:
                problems.append(
                    f'{fname}: the worked example chipped "{tag}" presents a real '
                    f'exam question but no quote of it stands above the solution. '
                    f'A reader meets the question only in our words.')

    # ---- 4. the styling and the visible marking the rule depends on ----
    css = read(os.path.join(HERE, 'manual.css'))
    for cls in ('.asprinted', '.paper .flag', '.unpack'):
        if cls not in css:
            problems.append(f'manual.css: {cls} style is gone, so quoted paper '
                            f'text no longer looks different from our own prose')
    for fname, paper, qid, _q in quotes:
        text = read(os.path.join(CONTENT, fname))
        if 'As printed' not in text:
            problems.append(f'{fname}: quotes a paper but carries no visible '
                            f'"As printed" bar, so a reader cannot tell the '
                            f'examiner\'s words from ours')
            break

    papers_seen = sorted({p for _f, p, _q, _t in quotes})
    covered = sum(1 for _f, p, _q, _t in quotes)
    print(f'VERBATIM GATE: {covered} quoted questions across {len(papers_seen)} '
          f'papers, checked against {len(tx)} transcripts')
    for paper in sorted(tx):
        have = len({q for _f, p, q, _t in quotes if p == paper})
        total = len(tx[paper])
        mark = 'solved in full' if paper in SOLVED_IN_FULL else 'cited selectively'
        print(f'  . {paper}: {have}/{total} questions quoted ({mark})')

    if problems:
        print('VERBATIM GATE: FAIL')
        for p in problems:
            print('  x ' + p)
        return False
    print('  . every quoted question matches the transcript character for character')
    print('  . every question of every paper solved in full is quoted, and quoted whole')
    print("  . every quote keeps the paper's own line breaks, so a listing is not reflowed")
    print("  . every site citing a paper shows that paper's words, not ours")
    print(f"  . {n_runs} quotations inside our flag notes are the paper's own words "
          f"({n_notpaper} marked notpaper, shown deliberately as what it does not say)")
    return True


if __name__ == '__main__':
    # a failure message can name the very glyph that was flattened, and this
    # console is cp1252 by default, which cannot encode it
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    sys.exit(0 if report() else 1)
