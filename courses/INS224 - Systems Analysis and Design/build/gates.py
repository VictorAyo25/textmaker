"""House-style gates for the CSC241 manual. A violation stops the build.

These encode the workspace's hard rules:
  1. No em dash or en dash anywhere. Use commas, colons, periods, parentheses.
     Ranges are written "1 to 4". A true minus sign is fine.
  2. No institution branding, and never name the pedagogy source.
  3. The reserved colour (emerald #059669) means MUST MEMORISE and nothing
     else, so it may not appear as an inline style in content.
  4. Code (SQL, relational algebra listings) must never be set in a proportional
     font. The source manual sets some code proportionally and its alignment
     examples are meaningless as a result; we do not inherit that defect.
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
    'Covenant', 'CCODeL', 'Canaanland', 'Idiroko', 'Ota,',
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
    for m in re.finditer(r'style="[^"]*#059669', html, re.I):
        fails.append('reserved colour #059669 used in an inline style; it belongs '
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
