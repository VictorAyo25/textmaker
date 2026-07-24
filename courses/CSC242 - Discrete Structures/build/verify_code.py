"""Code gate: every C++ listing in the book compiles, runs, and prints what the
book says it prints.

    cd build && python verify_code.py
    cd build && python verify_code.py --control    # prove it fails on each defect

Two papers set 19 marks of written programming, and the course text's only code
is one worked example (an inclusion-exclusion count, given in both C++ and
Python3) that resembles none of the four examined questions. So Part Eleven is
effectively the reader's only source for them. It teaches both languages, because
the guidance this semester is to answer coding questions in Python while the
older papers set C++, so every examined program is given both ways. A manual that
prints a listing which does not run has taught the reader to write it, and unlike
a wrong number in a worked example there is nothing on the page to give the error
away: broken code and working code look identical.

Python is interpreted, so its "compile" step is a parse (py_compile): a fragment
is parsed, a full program is parsed and then run and its output compared. That is
the exact shape of the C++ path, where a fragment is compiled but not run.

Asserting "compiled and run" in prose is worthless, and so is compiling a file
that sits beside the book rather than in it. The listing a reader copies is the
one INSIDE the HTML, so that is the one this gate extracts, compiles and runs.
It is the CSC241 and COS221 verify_code lineage, adapted from Python to C++.

What it does, per registered listing:

  1. EXTRACT the source out of `content/<file>.html`, from the `<pre class="code">`
     that follows the `.codelabel` naming it. Syntax-highlighting spans are
     stripped and entities are resolved, so what is written out is exactly the
     text a reader would retype.
  2. COMPILE it with warnings turned up. Any diagnostic at all is a failure:
     a warning in a teaching listing is a lesson in bad practice.
  3. RUN it with the input the question specifies.
  4. COMPARE the captured output with the `<pre class="out">` panel printed
     beneath it in the book, line for line.

Step 4 is the one that earns the gate its keep. Steps 1 to 3 prove the code is
real; step 4 proves the book is not quietly showing output from an older version
of it, which is the way these two drift apart in practice.
"""
import html as _h
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

# (content file, the .codelabel above the listing, the stdin for each run)
#
# A listing with several runs carries several input strings, and the book's
# output panel is the runs joined by a blank line, which is how the two
# isPerfectSquare calls are printed.
# (content file, the .codelabel above the listing, the stdin for each run, lang)
#
# Every examined program and every mock program is given twice, once in Python
# and once in C++, and both are run on the SAME input and must print the SAME
# panel. Registering the two side by side is what proves the book's claim that
# the two languages produce the same answer line for line.
LISTINGS = [
    ('p11_112.html', 'powerset.py', ['3\n1 2 3\n'], 'py'),
    ('p11_112.html', 'powerset.cpp', ['3\n1 2 3\n'], 'cpp'),
    ('p11_112.html', 'bitstrings.py',
     ['3\n3\n3 4 5\n4\n1 3 6 10\n6\n2 3 4 7 8 9\n'], 'py'),
    ('p11_112.html', 'bitstrings.cpp',
     ['3\n3\n3 4 5\n4\n1 3 6 10\n6\n2 3 4 7 8 9\n'], 'cpp'),
    ('p11_112.html', 'perfectsquare.py', ['49\n', '50\n'], 'py'),
    ('p11_112.html', 'perfectsquare.cpp', ['49\n', '50\n'], 'cpp'),
    ('p11_112.html', 'degrees.py', [''], 'py'),
    ('p11_112.html', 'degrees.cpp', [''], 'cpp'),
    # The three mock papers each set one program. A mock answer that does not run
    # is worse than a taught listing that does not, because the reader meets it
    # while marking their own attempt and has no prose around it to suggest the
    # fault is the book's.
    ('mock1_answers.html', 'divisors.py', ['28\n'], 'py'),
    ('mock1_answers.html', 'divisors.cpp', ['28\n'], 'cpp'),
    ('mock2_answers.html', 'apsum.py', ['4 3 20\n'], 'py'),
    ('mock2_answers.html', 'apsum.cpp', ['4 3 20\n'], 'cpp'),
    ('mock3_answers.html', 'majority.py', ['1 0 1\n'], 'py'),
    ('mock3_answers.html', 'majority.cpp', ['1 0 1\n'], 'cpp'),
]

# The teaching snippets of 11.1 are fragments, not programs: they have no main,
# or they use a variable the surrounding prose introduced. They are still
# COMPILED, because a reader retypes them exactly as printed and a typo in a
# teaching snippet is worse than one in a finished listing. Each declares the
# scaffolding it needs to stand up, and that scaffolding is OURS: it is not
# printed in the book and it is not part of what the fragment teaches.
#
# Fragments are compiled but not run. Some of them deliberately do nothing (the
# while-loop skeleton has an empty body), and one would not terminate.
MAIN_OPEN = '#include <iostream>\nusing namespace std;\nint main() {\n'
MAIN_CLOSE = 'return 0;\n}\n'

FRAGMENTS = [
    # (file, label, prelude, postlude, lang)
    # C++ fragments are wrapped in a main and any #include is hoisted above it.
    ('p11_cpp.html', 'The smallest complete program', '', '', 'cpp'),
    ('p11_cpp.html', 'Reading a number and testing it', MAIN_OPEN, MAIN_CLOSE, 'cpp'),
    ('p11_cpp.html', 'A for loop: use it when you know how many times',
     MAIN_OPEN + 'int n = 3;\n', MAIN_CLOSE, 'cpp'),
    ('p11_cpp.html', 'A while loop: use it when you stop on a condition',
     MAIN_OPEN + 'int low = 1, high = 0;\n', MAIN_CLOSE, 'cpp'),
    ('p11_cpp.html', 'Declaring, filling and reading a vector',
     MAIN_OPEN, MAIN_CLOSE, 'cpp'),
    ('p11_cpp.html', 'Definition, then use',
     '#include <iostream>\nusing namespace std;\n', '', 'cpp'),
    # Python fragments need no wrapper: each parses on its own, which is the
    # analogue of the C++ compile step. They are parsed, not run, because one is
    # a bare while-loop skeleton whose body is a `pass`.
    ('p11_py.html', 'The smallest complete program', '', '', 'py'),
    ('p11_py.html', 'Reading a number and testing it', '', '', 'py'),
    ('p11_py.html', 'A for loop: use it when you know how many times', '', '', 'py'),
    ('p11_py.html', 'A while loop: use it when you stop on a condition', '', '', 'py'),
    ('p11_py.html', 'Declaring, filling and reading a list', '', '', 'py'),
    ('p11_py.html', 'One line of numbers into a list', '', '', 'py'),
    ('p11_py.html', 'Definition, then use', '', '', 'py'),
]

TAG_RE = re.compile(r'<[^>]+>')
INCLUDE_RE = re.compile(r'^\s*#\s*include\b.*$', re.M)


def find_vcvars():
    """The Visual Studio environment script, or None.

    Searched rather than hard-coded so a version bump does not silently turn
    this gate off. Returning None is reported as a FAILURE, never as a pass:
    "no compiler, so nothing was checked" is exactly the vacuous-gate shape
    that qa_formulas already taught this workspace to distrust.
    """
    roots = [r'C:\Program Files\Microsoft Visual Studio',
             r'C:\Program Files (x86)\Microsoft Visual Studio']
    for root in roots:
        if not os.path.isdir(root):
            continue
        for year in sorted(os.listdir(root), reverse=True):
            for edition in ('Community', 'Professional', 'Enterprise',
                            'BuildTools'):
                bat = os.path.join(root, year, edition, 'VC', 'Auxiliary',
                                   'Build', 'vcvars64.bat')
                if os.path.exists(bat):
                    return bat
    return None


def read(name):
    with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
        return fh.read()


def extract(html, label):
    """(source, output panel) for the listing sitting under `label`.

    The listing is the first `<pre class="code">` after the label, and its
    output panel is the first `<pre class="out">` after that. Both are returned
    with highlighting stripped and entities resolved, which is the text a reader
    would actually retype off the page.
    """
    at = html.find(f'<div class="codelabel">{label}</div>')
    if at == -1:
        return None, None
    m = re.search(r'<pre class="code">(.*?)</pre>', html[at:], re.S)
    if not m:
        return None, None
    src = _h.unescape(TAG_RE.sub('', m.group(1)))
    after = at + m.end()
    o = re.search(r'<pre class="out">(.*?)</pre>', html[after:], re.S)
    out = _h.unescape(TAG_RE.sub('', o.group(1))) if o else None
    return src, out


def wrap(fragment, prelude, postlude):
    """A fragment made into a translation unit, with its #includes hoisted.

    A fragment may print its own `#include` line, because that IS part of what
    it teaches (the vector snippet would be a lie without one). An include
    cannot sit inside a function body, so it is lifted above the prelude. The
    hoist is a whole-line move, so nothing else about the fragment changes.
    """
    includes = INCLUDE_RE.findall(fragment)
    body = INCLUDE_RE.sub('', fragment)
    return '\n'.join(includes) + '\n' + prelude + body + '\n' + postlude


def wrap_py(fragment, prelude, postlude):
    """A Python fragment made into a parseable unit. Usually a no-op.

    Unlike C++, a Python fragment needs no surrounding main and has no #include to
    hoist, so prelude and postlude are almost always empty. They exist only so the
    two languages share one FRAGMENTS shape.
    """
    return prelude + fragment + '\n' + postlude


def run_python(workdir, name, source, stdins, compile_only=False):
    """Write `source`, parse it, and unless compile_only run it once per stdin.

    Python is interpreted, so the analogue of the C++ compile is a parse. A
    SyntaxError is caught here; a NameError or a logic bug surfaces only when the
    program is run, which is why full programs are run and their output compared
    and fragments are merely parsed, mirroring the C++ side exactly.
    """
    py = os.path.join(workdir, name)
    with open(py, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(source)
    chk = subprocess.run(
        [sys.executable, '-c',
         'import py_compile, sys; py_compile.compile(sys.argv[1], doraise=True)',
         py],
        capture_output=True, text=True)
    if chk.returncode != 0:
        tail = [ln for ln in (chk.stdout + chk.stderr).splitlines() if ln.strip()]
        return None, [f'{name} does not parse:'] + tail[-4:]
    if compile_only:
        return '', []

    chunks = []
    for data in stdins:
        run = subprocess.run([sys.executable, py], input=data,
                             capture_output=True, text=True, cwd=workdir)
        if run.returncode != 0:
            tail = [ln for ln in run.stderr.splitlines() if ln.strip()]
            return None, [f'{name} exited with status {run.returncode}'] + tail[-3:]
        chunks.append(norm(run.stdout))
    return '\n\n'.join(chunks), []


def norm(text):
    """Trailing whitespace and line endings are not the thing being checked."""
    return '\n'.join(line.rstrip() for line in text.replace('\r\n', '\n')
                     .strip('\n').split('\n'))


def msvc_env(vcvars):
    """The environment vcvars64.bat sets up, captured once.

    Chaining `call vcvars && cl ...` through `cmd /c` looked like the obvious
    way to do this and silently failed: cmd's own quote stripping mangled the
    compound command and every listing came back as "did not compile" with no
    diagnostic at all, which is the most misleading failure a gate can give.
    Running the script once, reading its environment out with `set`, then
    calling cl.exe directly is both correct and much faster, since vcvars is
    slow and there is no reason to pay for it four times.
    """
    r = subprocess.run(f'"{vcvars}" >nul 2>&1 && set', shell=True,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    env = dict(os.environ)
    for line in r.stdout.splitlines():
        if '=' in line:
            key, _, value = line.partition('=')
            env[key] = value
    return env


def build_and_run(env, workdir, name, source, stdins):
    """Compile `source` and run it once per stdin. Returns (output, errors)."""
    cpp = os.path.join(workdir, name)
    exe = os.path.splitext(cpp)[0] + '.exe'
    with open(cpp, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(source)

    # Windows resolves an executable name against the PARENT's PATH, not the
    # PATH inside `env`, so cl.exe is located explicitly. Passing 'cl' and
    # hoping raised a bare CreateProcess error with no hint of the cause.
    cl = shutil.which('cl', path=env.get('PATH', ''))
    if cl is None:
        return None, ['cl.exe is not on the compiler environment PATH']
    r = subprocess.run([cl, '/nologo', '/EHsc', '/W4', '/std:c++17',
                        name, f'/Fe:{exe}'],
                       cwd=workdir, env=env, capture_output=True, text=True)
    # cl echoes the file name it is compiling; anything beyond that is a
    # diagnostic, and a teaching listing may not carry even a warning.
    noise = [ln for ln in (r.stdout + r.stderr).splitlines()
             if ln.strip() and ln.strip() != name]
    if r.returncode != 0 or noise:
        return None, [f'{name} did not compile cleanly:'] + noise[:8]

    chunks = []
    for data in stdins:
        run = subprocess.run([exe], input=data, capture_output=True, text=True,
                             cwd=workdir)
        if run.returncode != 0:
            return None, [f'{name} exited with status {run.returncode}']
        chunks.append(norm(run.stdout))
    return '\n\n'.join(chunks), []


def report(listings=LISTINGS, fragments=FRAGMENTS):
    problems = []
    checked = fragged = 0

    # The C++ compiler is only needed if something registered is C++. Guarding on
    # that keeps the Python arm alive on a machine without Visual Studio, and
    # keeps this gate honest: it only demands a tool it is about to use.
    needs_cpp = (any(l[3] == 'cpp' for l in listings)
                 or any(f[4] == 'cpp' for f in fragments))
    env = None
    if needs_cpp:
        vcvars = find_vcvars()
        if vcvars is None:
            print('CODE GATE: FAIL')
            print('  x no C++ compiler found, so no C++ listing in Part Eleven '
                  'was compiled or run. This gate does not pass on an empty '
                  'sweep: install the Visual Studio build tools, or the book '
                  'ships code nobody has ever built.')
            return False
        env = msvc_env(vcvars)
        if env is None:
            print('CODE GATE: FAIL')
            print(f'  x {vcvars} would not run, so no C++ listing was compiled')
            return False

    work = tempfile.mkdtemp(prefix='csc242_code_')
    try:
        for fname, label, stdins, lang in listings:
            html = read(fname)
            src, shown = extract(html, label)
            if src is None:
                problems.append(f'{fname}: no listing found under the label '
                                f'{label!r}; the gate checked nothing for it')
                continue
            if shown is None:
                problems.append(f'{fname}: {label} has no <pre class="out"> '
                                f'panel, so what it prints is unverified')
                continue
            checked += 1
            if lang == 'py':
                got, errs = run_python(work, label, src, stdins)
            else:
                got, errs = build_and_run(env, work, label, src, stdins)
            if errs:
                problems.extend('  ' + e for e in errs)
                continue
            if norm(got) != norm(shown):
                problems.append(
                    f'{fname}: {label} runs, but its output panel is not what '
                    f'it printed')
                a, b = norm(shown).split('\n'), norm(got).split('\n')
                for i in range(max(len(a), len(b))):
                    x = a[i] if i < len(a) else '(nothing)'
                    y = b[i] if i < len(b) else '(nothing)'
                    if x != y:
                        problems.append(f'      line {i + 1} book: {x!r}')
                        problems.append(f'      line {i + 1} real: {y!r}')

        for i, (fname, label, prelude, postlude, lang) in enumerate(fragments):
            src, _ = extract(read(fname), label)
            if src is None:
                problems.append(f'{fname}: no fragment found under the label '
                                f'{label!r}; the gate checked nothing for it')
                continue
            fragged += 1
            if lang == 'py':
                _, errs = run_python(work, f'fragment{i}.py',
                                     wrap_py(src, prelude, postlude), [],
                                     compile_only=True)
            else:
                _, errs = build_and_run(env, work, f'fragment{i}.cpp',
                                        wrap(src, prelude, postlude), [])
            if errs:
                problems.append(f'{fname}: the snippet "{label}" does not '
                                f'{"parse" if lang == "py" else "compile"}, and '
                                f'a reader will retype it exactly as printed')
                problems.extend('      ' + e for e in errs[1:])
    finally:
        shutil.rmtree(work, ignore_errors=True)

    # ZERO-SCAN guard, the qa_formulas lesson: every listing in content/ must be
    # registered here, or a new one could be added and never compiled.
    present = sum(read(f).count('<pre class="code">')
                  for f in sorted(os.listdir(CONTENT)) if f.endswith('.html'))
    if present != len(listings) + len(fragments):
        problems.append(f'content/ holds {present} code listings but this gate '
                        f'registers {len(listings)} programs and '
                        f'{len(fragments)} fragments; the difference is never '
                        f'compiled. Add them to LISTINGS or to FRAGMENTS.')

    print(f'CODE GATE: {checked} complete programs (Python and C++) and '
          f'{fragged} teaching fragments extracted from the book, run and '
          f'compared (C++ compiled at /W4)')
    if problems:
        print('CODE GATE: FAIL')
        for p in problems:
            print('  x ' + p)
        return False
    print('  . every listing the book prints parses, and every C++ one compiles '
          'with no diagnostics')
    print('  . every complete program runs on the question\'s own input')
    print('  . every output panel is what the program actually printed')
    print('  . the Python and C++ twin of each program print the same panel')
    print('  . every teaching fragment parses inside a declared wrapper')
    print('  . every listing in content/ is registered here')
    return True


def control():
    """Prove this gate fails on each defect it claims to catch.

    Each case tampers with a real content file and restores it in a finally, so
    a crash cannot leave the book edited.
    """
    # Each case names the file it tampers, so the Python and C++ arms are both
    # exercised. The bit-string output panel is identical in both languages and
    # the Python one is printed first, so tampering it tests the Python run and
    # compare path; the two `cout` cases are C++ source and test that arm.
    cases = [
        ('p11_112.html', 'a C++ listing that no longer compiles',
         '&lt;&lt; n;                 <span class="c">// 2^n subsets</span>',
         '&lt;&lt; n                 <span class="c">// 2^n subsets</span>'),
        ('p11_112.html', 'a Python output panel that disagrees with the run',
         'Set 1 bit string: 0011100000', 'Set 1 bit string: 0011100001'),
        ('p11_112.html', 'a C++ listing whose logic changed but whose panel did not',
         '(first) cout &lt;&lt; <span class="s">" "</span>;',
         '(false) cout &lt;&lt; <span class="s">" "</span>;'),
    ]
    # Fragments are parsed but never run, so only the parse step can catch a
    # defect in one. One case per language proves that step is live for both.
    frag_cases = [
        ('p11_cpp.html', 'a C++ teaching fragment with a typo in it',
         'cin &gt;&gt; n;                        <span class="c">',
         'cin &gt;&gt; nn;                       <span class="c">'),
        ('p11_py.html', 'a Python teaching fragment with a typo in it',
         'larger(a, b):', 'larger(a, b)'),
    ]
    passed = 0
    for ffile, what, old, new in cases + frag_cases:
        fpath = os.path.join(CONTENT, ffile)
        foriginal = read(ffile)
        try:
            assert old in foriginal, f'control setup: {old!r} not in {ffile}'
            with open(fpath, 'w', encoding='utf-8') as fh:
                fh.write(foriginal.replace(old, new, 1))
            ok = report()
            print(f'CONTROL [{what}]: '
                  f'{"gate FAILED as it must" if not ok else "GATE PASSED, WHICH IS WRONG"}')
            passed += not ok
        finally:
            with open(fpath, 'w', encoding='utf-8') as fh:
                fh.write(foriginal)

    # And the unregistered-listing guard.
    ok = report(LISTINGS[:-1])
    print(f'CONTROL [a listing nobody registered]: '
          f'{"gate FAILED as it must" if not ok else "GATE PASSED, WHICH IS WRONG"}')
    passed += not ok

    total = len(cases) + len(frag_cases) + 1
    print(f'\n{passed}/{total} control tests failed the gate as they must')
    return passed == total


if __name__ == '__main__':
    if '--control' in sys.argv:
        sys.exit(0 if control() else 1)
    sys.exit(0 if report() else 1)
