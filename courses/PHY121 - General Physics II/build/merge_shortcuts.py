"""
merge_shortcuts.py — collect the agent-authored shortcut dicts from the scratchpad,
validate them against the real content (dry-run the injector), check house style,
and write the merged data into shortcuts.py's SHORTCUTS table.

One-time build helper. Run after the authoring agents have written their _sc_*.py
files. It refuses to write if any section fails to inject cleanly or any shortcut
carries an em/en dash.
"""
import io, os, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = (r'C:\Users\victo\AppData\Local\Temp\claude'
           r'\c--Users-victo-OneDrive-Documents-CU-Actual-Coursework-200-Level-200---Omega-Semester-manual-composer'
           r'\8b60518a-6916-4dcf-8f83-7db499d9b20b\scratchpad')

# scratchpad file -> {dict name in that file: section name in SHORTCUTS}
SOURCES = {
  '_sc_exercises.py': {'DATA': 'exercises'},
  '_sc_mod34.py':     {'MODULE3': 'module3', 'MODULE4': 'module4'},
  '_sc_fm12.py':      {'FOUNDATIONS': 'foundations', 'MODULE1': 'module1', 'MODULE2': 'module2'},
  '_sc_mocks.py':     {'DATA': 'mocks'},
  '_sc_mod5.py':      {'BODY': 'module5body', 'ASSESS': 'module5assess'},
}


def _load(path):
    spec = importlib.util.spec_from_file_location('m', path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def _tidy(s):
    """Normalise a shortcut to house conventions: a literal ½ like the rest of the
    manual, and no stray * for multiply."""
    s = s.replace('&amp;frac12;', '½').replace('&frac12;', '½')
    return s


def collect():
    merged = {}
    for fn, mapping in SOURCES.items():
        p = os.path.join(SCRATCH, fn)
        if not os.path.exists(p):
            raise SystemExit(f'missing {fn} (agent not done?)')
        mod = _load(p)
        for dictname, section in mapping.items():
            merged[section] = {k: _tidy(v) for k, v in getattr(mod, dictname).items()}
    return merged


def content_for(section):
    """The HTML a section injects into, as assemble.py would load it."""
    if section in ('module5body', 'module5assess'):
        f = 'module5_body.html' if section == 'module5body' else 'module5_assess.html'
        return io.open(os.path.join(HERE, f), encoding='utf-8').read()
    return io.open(os.path.join(HERE, 'content', section + '.html'), encoding='utf-8').read()


def main():
    import shortcuts
    merged = collect()
    total = sum(len(v) for v in merged.values())
    print(f'collected {total} shortcuts across {len(merged)} sections')

    # 1. house style: no em/en dashes
    bad = []
    for sec, d in merged.items():
        for label, txt in d.items():
            if '\u2014' in txt or '\u2013' in txt:
                bad.append(f'{sec}:{label}')
    if bad:
        print('EM/EN DASHES in:', bad); raise SystemExit('fix dashes first')
    print('house style: no em/en dashes  OK')

    # 1b. surface any stray entities or ASCII * (should be × or a tag) to eyeball
    SAFE = {'&lt;', '&gt;', '&amp;', '&deg;', '&times;', '&minus;', '&pi;'}
    for sec, d in merged.items():
        for label, txt in d.items():
            for ent in re.findall(r'&[a-zA-Z]+;', txt):
                if ent not in SAFE:
                    print(f'  NOTE entity {ent} in {sec}:{label[:30]}')
            if re.search(r'(?<![<>=])\*', txt):
                print(f'  NOTE bare * in {sec}:{label[:30]}')

    # 2. dry-run inject each section against real content
    shortcuts.SHORTCUTS.update(merged)
    for sec, d in merged.items():
        html = content_for(sec)
        shortcuts.inject(sec, html)          # raises on any mismatch
        print(f'  {sec:14s} {len(d):3d} shortcuts inject cleanly')

    # 3. write merged data into shortcuts.py
    lines = ['SHORTCUTS = {']
    for sec in ['foundations', 'module1', 'module2', 'module3', 'module4',
                'exercises', 'mocks', 'module5body', 'module5assess']:
        d = merged.get(sec, {})
        lines.append(f'  {sec!r}: {{')
        for label, txt in d.items():
            lines.append(f'    {label!r}: {txt!r},')
        lines.append('  },')
    lines.append('}')
    block = '\n'.join(lines)

    src = io.open(os.path.join(HERE, 'shortcuts.py'), encoding='utf-8').read()
    # replace via slicing, not re.sub, so backslashes in `block` are not treated
    # as regex replacement escapes
    m = re.search(r'SHORTCUTS = \{.*?\n\}', src, flags=re.S)
    src = src[:m.start()] + block + src[m.end():]
    io.open(os.path.join(HERE, 'shortcuts.py'), 'w', encoding='utf-8').write(src)
    print(f'\nwrote {total} shortcuts into shortcuts.py')


if __name__ == '__main__':
    main()
