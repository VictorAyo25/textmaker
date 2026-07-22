"""House-style gates for the CSC242 manual. A violation stops the build.

These encode the workspace's hard rules:
  1. No em dash or en dash anywhere. Use commas, colons, periods, parentheses.
     Ranges are written "1 to 4". A true minus sign is fine.
  2. No institution branding, and never name the pedagogy source.
  3. The reserved colour (crimson #be123c) means MUST MEMORISE and nothing
     else, so it may not appear as an inline style in content.
  4. Code must never be set in a proportional font. The source manual does this
     and its column-alignment examples are meaningless as a result; we do not
     inherit that defect.
  5. No line of code may be wider than the page. Chromium's print path shrinks
     the WHOLE document to fit its widest box, so one long line in one snippet
     silently reduces the body font size of every page in the book. This is not
     hypothetical: a 93-character line in Module Five had been rendering the
     manual at 96.9% of its design size, and three 104-character lines in Mock
     Two took it to 87.1%. Nothing else caught it. Layout QA could not: after the
     shrink, nothing overflows. See qa_layout.py, which checks the rendered size
     as well, and MANUAL_METHODOLOGY.md.
"""
import html as _html
import os
import re, sys

# Measured off the render, not derived. 90 was the old value and it was wrong: it
# was measured against the PAGE, where 90 characters do fit without triggering
# Chromium's shrink. But almost every code block sits inside a teaching box, and a
# box costs its code about 20pt of width, so the line clears the page and still
# runs out past the panel drawn around it. Nothing failed, because nothing left
# the page: two lines printed with their tails hanging over the box edge.
#
# Inside a box the code starts at x=73.7 and the panel ends at x=534.8, which is
# 461.1pt at a measured 5.238pt per character:
#     87 cols -> ends at 529.4  (5.4pt clear)
#     88 cols -> ends at 534.7  (0.1pt clear, which is noise, not room)
#     89 cols -> ends at 539.9  (spills 5.1pt)
# 88 is the geometric limit and 87 is the honest one.
MAX_CODE_COLS = 87

CODE_BLOCK = re.compile(r'<pre class="[^"]*">(.*?)</pre>', re.S)

# Dashes: em (U+2014), en (U+2013), horizontal bar (U+2015), minus-as-dash figure
# dash (U+2012). The maths minus (U+2212) is explicitly allowed.
BANNED_CHARS = {
    '—': 'em dash',
    '–': 'en dash',
    '―': 'horizontal bar',
    '‒': 'figure dash',
}
BANNED_ENTITIES = ['&mdash;', '&ndash;', '&#8212;', '&#8211;', '&#x2014;', '&#x2013;']

BANNED_WORDS = [
    'Covenant', 'CCODeL', 'CCODEL', 'Canaanland', 'Idiroko', 'Ota,',
    'Stroud',
    # This course's own source hazards. The institutional text prints a wrong
    # running header on all 161 pages ("Elementary Differential Equations", a
    # copy-paste from another course) and the papers carry departmental stamps;
    # neither may be quoted into the manual.
    'Elementary Differential Equations', 'COMPUTER & INFORMATION SCIENCES',
    'HEAD OF DEPARTMENT',
]


def _strip_tags(html):
    """Rough text view: drop tags so we test prose, not markup."""
    return re.sub(r'<[^>]+>', ' ', html)


PAPER_OPEN_RE = re.compile(r'<div class="box paper"[^>]*>')
DIV_EDGE_RE = re.compile(r'<div\b|</div>')


def mask_quotes(html):
    """Blank every AS PRINTED box, keeping the text length identical.

    Returns (masked_html, how_many_masked). Replacing the quoted regions with
    spaces rather than deleting them means every reported offset still points at
    the right place in the original. The dash rules are OUR house style; a
    quotation of an external document is exempt from them by MANUAL_METHODOLOGY
    4c, but nothing else is, so the exemption is scoped rather than switched off.
    """
    out = list(html)
    n = 0
    for m in PAPER_OPEN_RE.finditer(html):
        depth, end = 0, len(html)
        for e in DIV_EDGE_RE.finditer(html, m.start()):
            depth += 1 if e.group(0) != '</div>' else -1
            if depth == 0:
                end = e.end()
                break
        for i in range(m.start(), end):
            if out[i] != '\n':
                out[i] = ' '
        n += 1
    return ''.join(out), n


def run_gates(html):
    fails = []
    text = _strip_tags(html)

    # ---- 1. dashes, on OUR prose only ----
    prose, n_masked = mask_quotes(html)
    for ch, name in BANNED_CHARS.items():
        for m in re.finditer(re.escape(ch), prose):
            ctx = html[max(0, m.start() - 45):m.start() + 45].replace('\n', ' ')
            fails.append(f'{name} (U+{ord(ch):04X}) found: ...{ctx}...')
    for ent in BANNED_ENTITIES:
        for m in re.finditer(re.escape(ent), prose):
            ctx = html[max(0, m.start() - 45):m.start() + 45].replace('\n', ' ')
            fails.append(f'dash entity {ent} found: ...{ctx}...')

    # ---- 2. branding / pedagogy source ----
    for w in BANNED_WORDS:
        if re.search(re.escape(w), text, re.I):
            m = re.search(re.escape(w), text, re.I)
            ctx = text[max(0, m.start() - 45):m.start() + 45].replace('\n', ' ')
            fails.append(f'banned word "{w}": ...{ctx}...')

    # ---- 3. reserved colour must not be used inline ----
    for m in re.finditer(r'style="[^"]*#be123c', html, re.I):
        fails.append('reserved colour #be123c used in an inline style; it belongs '
                     'to the MUST MEMORISE box only')

    # ---- 4. code must be monospace ----
    #    catch a <pre>/<code> that has been given a font-family inline
    for m in re.finditer(r'<(pre|code)[^>]*style="[^"]*font-family\s*:\s*([^;"]+)', html, re.I):
        fam = m.group(2).lower()
        if 'mono' not in fam:
            fails.append(f'code set in a non-monospace font: {m.group(2)!r}')

    # ---- 5. no code line wider than the box it sits in ----
    for block in CODE_BLOCK.findall(html):
        for line in _html.unescape(re.sub(r'<[^>]+>', '', block)).split('\n'):
            if len(line) > MAX_CODE_COLS:
                fails.append(f'code line is {len(line)} characters, over the '
                             f'{MAX_CODE_COLS} that fit inside a teaching box: it would '
                             f'hang over the panel edge, and past about 90 Chromium '
                             f'shrinks every page in the book. {line.strip()[:56]!r}')

    # ---- 6. the stylesheet's own glyph escapes are intact ----
    #
    # Every marker this book draws with CSS `content` is an escape like "\25C6".
    # Two ways that silently turns into garbage on the page, both of which have
    # actually happened in this workspace:
    #
    #   * The escape gets mangled while editing. Writing the rule from a Python
    #     string, "\\25C6" reads \25 as an OCTAL escape and emits U+0015 followed
    #     by the literal text "C6", so the reader sees a control character and
    #     stray letters instead of a diamond. That shipped into this book's first
    #     render and was invisible in every gate.
    #   * The character is fine but the FONT has no glyph for it, so it prints as
    #     tofu. TMC221 shipped a key emoji DejaVu does not carry.
    #
    # So check both: no control characters in the sheet, and every codepoint a
    # `content` rule asks for exists in the body font.
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manual.css')
    if os.path.exists(css_path):
        with open(css_path, encoding='utf-8') as fh:
            css = fh.read()
        for i, ch in enumerate(css):
            if ord(ch) < 32 and ch not in '\n\t\r':
                fails.append(f'manual.css has a control character U+{ord(ch):04X} at '
                             f'offset {i}: a CSS escape was mangled while editing, '
                             f'and it will print as garbage. Context: '
                             f'{css[max(0, i - 30):i + 10]!r}')
        wanted = set()
        for m in re.finditer(r'content\s*:\s*"([^"]*)"', css):
            for esc in re.findall(r'\\([0-9A-Fa-f]{2,6})', m.group(1)):
                wanted.add(int(esc, 16))
            for ch in re.sub(r'\\[0-9A-Fa-f]{2,6}\s?', '', m.group(1)):
                if ord(ch) > 126:
                    wanted.add(ord(ch))
        if wanted:
            try:
                from fontTools.ttLib import TTFont
                fonts = ['fonts/DejaVuSans.ttf', 'fonts/DejaVuSerif.ttf']
                have = set()
                for f in fonts:
                    fp = os.path.join(os.path.dirname(css_path), f)
                    if os.path.exists(fp):
                        have |= set(TTFont(fp).getBestCmap())
                for cp in sorted(wanted - have):
                    fails.append(f'manual.css draws U+{cp:04X} with a content rule, '
                                 f'but no bundled font has that glyph: it will print '
                                 f'as tofu, an empty box, on every box that uses it.')
            except ImportError:
                pass          # fontTools absent: skip rather than fail the build

    # ---- report ----
    checks = [
        'no em/en dashes',
        'no institution branding or pedagogy source named',
        'reserved colour reserved',
        'all code monospace',
        f'no code line over {MAX_CODE_COLS} columns',
        'every CSS content glyph is intact and present in the bundled fonts',
        f'dash rules applied to our prose, {n_masked} quoted question(s) exempt',
    ]
    if fails:
        print('HOUSE-STYLE GATE: FAIL')
        for f in fails:
            print('  x ' + f)
        return False
    print('HOUSE-STYLE GATE: pass')
    for c in checks:
        print('  . ' + c)
    return True


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'full_manual.html'
    with open(src, encoding='utf-8') as fh:
        sys.exit(0 if run_gates(fh.read()) else 1)
