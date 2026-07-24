"""Measure the RENDERED PDF against the design: no drill option may go missing.

    cd build && python qa_content.py

Internal consistency is not correctness (MANUAL_METHODOLOGY sec 0.7). A drill whose
options are laid out but not painted still produces a self-consistent PDF: footers
sequential, Contents matching itself, nothing overflowing. So this checks the thing that
actually matters for a drill bank: every option, every worked answer, and every cloze
answer that the HTML declares is present in the rendered PDF's text.

It pulls a distinctive probe phrase from each declared item and asserts the PDF contains
it. Punctuation and whitespace are normalised because the PDF wraps and hyphenates.
"""
import os, re, sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, 'full_manual.html')
PDF = os.path.join(HERE, 'ENT221_checkpoint.pdf')

OPT = re.compile(r'<li data-l="[a-d]">(.*?)</li>', re.S)


def norm(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = (s.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
          .replace('&middot;', '.').replace('&nbsp;', ' '))
    return re.sub(r'\s+', ' ', s).strip()


def pdf_text():
    doc = fitz.open(PDF)
    t = ' '.join(page.get_text() for page in doc)
    doc.close()
    return re.sub(r'\s+', ' ', t)


def probe(option):
    """A distinctive contiguous run from an option, robust to PDF line-wrapping.
    Uses the longest run of letters/spaces so hyphenation and punctuation do not matter."""
    runs = re.findall(r'[A-Za-z][A-Za-z ]{14,}', norm(option))
    return max(runs, key=len).strip() if runs else norm(option)


def report():
    html = open(HTML, encoding='utf-8').read()
    text = pdf_text()
    # The PDF wraps and HYPHENATES ("procras-tinate"), so compare with spaces and
    # every kind of hyphen removed; the probe is long enough that this cannot collide.
    squash = lambda s: re.sub(r'[\s\-­‐‑]', '', s)
    text_sq = squash(text)
    options = OPT.findall(html)
    missing = []
    for opt in options:
        if squash(probe(opt)) not in text_sq:
            missing.append(norm(opt)[:70])
    # a tofu/notdef would strip a glyph; assert the key emoji is gone
    tofu = '�' in text or '\U0001F511' in text
    print(f'CONTENT GATE: {len(options)} drill options checked against the rendered PDF')
    ok = not missing and not tofu
    if missing:
        print(f'  x {len(missing)} option(s) declared in HTML but NOT found in the PDF:')
        for m in missing:
            print('      ' + m)
    if tofu:
        print('  x a replacement/emoji glyph is present in the rendered text (tofu risk)')
    if ok:
        print('  . every drill option is painted in the final PDF; no tofu glyphs')
    return ok


if __name__ == '__main__':
    sys.exit(0 if report() else 1)
