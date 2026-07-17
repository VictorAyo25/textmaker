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
"""
import re, sys

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

    # ---- report ----
    checks = [
        'no em/en dashes',
        'no institution branding or pedagogy source named',
        'reserved colour reserved',
        'all code monospace',
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
