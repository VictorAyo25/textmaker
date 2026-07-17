"""House-style gates for the CSC241 manual. A violation stops the build.

These encode the workspace's hard rules:
  1. No em dash or en dash anywhere. Use commas, colons, periods, parentheses.
     Ranges are written "1 to 4". A true minus sign is fine.
  2. No institution branding, and never name the pedagogy source.
  3. The reserved colour (Python yellow #ffd43b) means MUST MEMORISE and nothing
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
import re, sys

# Measured, not derived: see the probe recorded in MANUAL_METHODOLOGY.md. At 90
# characters the body still renders at its designed 9.6pt; at 92 it is 9.40pt.
MAX_CODE_COLS = 90

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
    'Covenant', 'CCODeL', 'COV-CSC241', 'Canaanland', 'Idiroko', 'Ota,',
    'Stroud',
]


def _strip_tags(html):
    """Rough text view: drop tags so we test prose, not markup."""
    return re.sub(r'<[^>]+>', ' ', html)


def run_gates(html):
    fails = []
    text = _strip_tags(html)

    # ---- 1. dashes ----
    for ch, name in BANNED_CHARS.items():
        for m in re.finditer(re.escape(ch), html):
            ctx = html[max(0, m.start() - 45):m.start() + 45].replace('\n', ' ')
            fails.append(f'{name} (U+{ord(ch):04X}) found: ...{ctx}...')
    for ent in BANNED_ENTITIES:
        if ent in html:
            i = html.index(ent)
            ctx = html[max(0, i - 45):i + 45].replace('\n', ' ')
            fails.append(f'dash entity {ent} found: ...{ctx}...')

    # ---- 2. branding / pedagogy source ----
    for w in BANNED_WORDS:
        if re.search(re.escape(w), text, re.I):
            m = re.search(re.escape(w), text, re.I)
            ctx = text[max(0, m.start() - 45):m.start() + 45].replace('\n', ' ')
            fails.append(f'banned word "{w}": ...{ctx}...')

    # ---- 3. reserved colour must not be used inline ----
    for m in re.finditer(r'style="[^"]*#ffd43b', html, re.I):
        fails.append('reserved colour #ffd43b used in an inline style; it belongs '
                     'to the MUST MEMORISE box only')

    # ---- 4. code must be monospace ----
    #    catch a <pre>/<code> that has been given a font-family inline
    for m in re.finditer(r'<(pre|code)[^>]*style="[^"]*font-family\s*:\s*([^;"]+)', html, re.I):
        fam = m.group(2).lower()
        if 'mono' not in fam:
            fails.append(f'code set in a non-monospace font: {m.group(2)!r}')

    # ---- 5. no code line wider than the page ----
    for block in CODE_BLOCK.findall(html):
        for line in _html.unescape(re.sub(r'<[^>]+>', '', block)).split('\n'):
            if len(line) > MAX_CODE_COLS:
                fails.append(f'code line is {len(line)} characters, over the '
                             f'{MAX_CODE_COLS} that fit: Chromium would shrink every '
                             f'page in the book to fit it. {line.strip()[:56]!r}')

    # ---- report ----
    checks = [
        'no em/en dashes',
        'no institution branding or pedagogy source named',
        'reserved colour reserved',
        'all code monospace',
        f'no code line over {MAX_CODE_COLS} columns',
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
