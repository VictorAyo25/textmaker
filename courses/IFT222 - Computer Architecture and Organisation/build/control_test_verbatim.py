"""Control test for qa_verbatim.py. Green today is not proof (methodology 0.9).

    cd build && python control_test_verbatim.py

A gate that has never failed has never been shown to work. This feeds the verbatim
gate known-bad inputs and requires it to reject each one, then feeds it the real
book and requires it to accept that. It works on COPIES in a scratch directory, so
it never edits the manual.

The two defects it injects are exactly the two the gate exists to catch:

  A. PARAPHRASE. One word of one quoted question is changed. This is the original
     defect in miniature: the book still looks right, still cites the right paper,
     and is now lying about what the examiner wrote.
  B. A DROPPED PART. One whole quote is deleted from the book. The paper is still
     presented as solved in full, so a part of it has silently vanished.

If either injection still passes, the gate is decorative and the manual is not
actually protected.
"""
import io
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qa_verbatim  # noqa: E402

REAL_CONTENT = os.path.join(HERE, 'content')
REAL_TX = qa_verbatim.TRANSCRIPTS


def run_against(content_dir):
    """Run the gate quietly against a content dir. Returns True if it passed."""
    qa_verbatim.CONTENT = content_dir
    out = sys.stdout
    sys.stdout = io.StringIO()      # not devnull: a report may name a non-ASCII
    try:                            # glyph, and a cp1252 file handle would die
        ok = qa_verbatim.report()
    finally:
        sys.stdout = out
    return ok


def first_quote_file(content_dir):
    """The first file holding a declared quote, and that quote's inner text."""
    for fname in sorted(os.listdir(content_dir)):
        if not fname.endswith('.html'):
            continue
        path = os.path.join(content_dir, fname)
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        m = qa_verbatim.ASPRINTED_RE.search(text)
        if m:
            return path, text, m
    return None, None, None


def main():
    results = []
    scratch = tempfile.mkdtemp(prefix='verbatim_control_')
    try:
        work = os.path.join(scratch, 'content')
        shutil.copytree(REAL_CONTENT, work)

        # ---- 0. baseline: the real book must pass, or the test proves nothing ----
        base = run_against(work)
        results.append(('baseline, the manual as it stands', base, True))
        if not base:
            print('CONTROL TEST: cannot run. The manual does not currently pass the '
                  'verbatim gate, so a failure below would prove nothing.')
            for name, got, want in results:
                print(f'  {name}: got {got}, wanted {want}')
            return 1

        path, text, m = first_quote_file(work)
        if not path:
            print('CONTROL TEST: cannot run, no declared quote found to corrupt.')
            return 1

        # ---- A. paraphrase: change ONE word inside a quoted question ----
        inner = m.group(2)
        words = [w for w in re.findall(r'\b[A-Za-z]{4,}\b', inner)]
        if not words:
            print('CONTROL TEST: cannot run, quote has no word long enough to swap.')
            return 1
        target = words[0]
        broken = text[:m.start(2)] + inner.replace(target, target.upper() + 'X', 1) \
            + text[m.end(2):]
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(broken)
        got = run_against(work)
        results.append((f'A. one word reworded ("{target}" changed) in '
                        f'{os.path.basename(path)}', got, False))
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)

        # ---- B. a dropped part: delete one whole quote from the book ----
        dropped = text[:m.start()] + text[m.end():]
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(dropped)
        got = run_against(work)
        results.append((f'B. one whole quoted question deleted from '
                        f'{os.path.basename(path)}', got, False))
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)

        # ---- C. restored: the gate must go green again, not stay stuck red ----
        got = run_against(work)
        results.append(('C. file restored', got, True))

        # ---- E. straightened wrapping: same words, the paper's layout destroyed ----
        # Joins two lines of a quoted listing into one. Every word survives, so
        # checks 1, 2 and 3 all still pass: they compare text with whitespace
        # collapsed. Only the line-structure check can see it. This is the COS221
        # lesson in miniature, where a quoted listing was re-wrapped to taste.
        listing = None
        for fn in sorted(os.listdir(work)):
            if not fn.endswith('.html'):
                continue
            p = os.path.join(work, fn)
            with open(p, encoding='utf-8') as fh:
                t = fh.read()
            for mm in qa_verbatim.ASPRINTED_RE.finditer(t):
                lines = mm.group(2).split('\n')
                # find a quote with two adjacent short lines, i.e. a listing
                for k in range(len(lines) - 1):
                    a, b = lines[k].strip(), lines[k + 1].strip()
                    if 0 < len(a) < 60 and 0 < len(b) < 60:
                        listing = (p, t, mm, k)
                        break
                if listing:
                    break
            if listing:
                break
        if not listing:
            results.append(('E. no listing found to straighten', False, True))
        else:
            p, t, mm, k = listing
            lines = mm.group(2).split('\n')
            joined = '\n'.join(lines[:k] + [lines[k] + ' ' + lines[k + 1].strip()]
                               + lines[k + 2:])
            bad = t[:mm.start(2)] + joined + t[mm.end(2):]
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(bad)
            got = run_against(work)
            results.append((f'E. two quoted lines joined into one in '
                            f'{os.path.basename(p)} (every word still present)',
                            got, False))
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(t)

        # ---- F. a misquote in OUR prose, at a site with no quote box to check ----
        # The COS221 defect: a flag note that puts words in quotation marks and
        # attributes them to the paper, while the AS PRINTED box beside it is
        # perfect. Every other mechanism works from the box, so all of them pass.
        # Here one letter is capitalised inside a flag quotation, which is exactly
        # the size of the eight real ones found in this book.
        flag = None
        for fn in sorted(os.listdir(work)):
            if not fn.endswith('.html'):
                continue
            p = os.path.join(work, fn)
            with open(p, encoding='utf-8') as fh:
                t = fh.read()
            for mm in qa_verbatim.FLAG_RE.finditer(t):
                for run in mm.group(1).split('"')[1::2]:
                    s = run.strip()
                    if len(s.split()) >= 3 and s[:1].islower() and '<' not in s:
                        flag = (p, t, run)
                        break
                if flag:
                    break
            if flag:
                break
        if not flag:
            results.append(('F. no flag quotation found to corrupt', False, True))
        else:
            p, t, run = flag
            bad = t.replace('"' + run + '"',
                            '"' + run.strip()[0].upper() + run.strip()[1:] + '"', 1)
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(bad)
            got = run_against(work)
            results.append((f'F. one letter capitalised inside a flag quotation in '
                            f'{os.path.basename(p)}, with its As-printed box left '
                            f'perfect', got, False))
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(t)

        # ---- G. a flattened glyph in the TRANSCRIPT, which is the authority ----
        # The only defect where the book can be a perfect copy and still be wrong,
        # because every other check measures the book against this file. The 23/24
        # paper prints its code-converter variables with true subscript digits and
        # the first pass of the transcript typed them flat, so the gate would have
        # blessed a flattened quote forever. Caught by comparing the transcript
        # against the meaningful glyphs present in the source PDF's text layer.
        tx_work = os.path.join(scratch, 'transcripts')
        shutil.copytree(REAL_TX, tx_work)
        qa_verbatim.TRANSCRIPTS = tx_work
        target = os.path.join(tx_work, '2023-2024.txt')
        if not os.path.exists(target):
            results.append(('G. no transcript found to flatten', False, True))
        else:
            with open(target, encoding='utf-8') as fh:
                orig_tx = fh.read()
            flat = orig_tx
            for sub, plain in (('₀', '0'), ('₁', '1'), ('₂', '2'), ('₃', '3')):
                flat = flat.replace(sub, plain)
            with open(target, 'w', encoding='utf-8') as fh:
                fh.write(flat)
            got = run_against(work)
            results.append(('G. subscripts flattened in the 23/24 TRANSCRIPT, the '
                            'file every other check trusts as the authority',
                            got, False))
            with open(target, 'w', encoding='utf-8') as fh:
                fh.write(orig_tx)
        qa_verbatim.TRANSCRIPTS = REAL_TX

        # ---- D. exercise the REVERSE direction on its own ----
        # B above is caught by the discovery check (a teaching site lost its
        # quote), which would mask a broken coverage check. Most questions are
        # quoted twice, once where they are taught and once in the solved paper,
        # so deleting one copy proves nothing about coverage. This finds a
        # question quoted exactly ONCE in the whole book, from a paper declared
        # solved in full, and deletes that single copy. Nothing else can catch
        # it: only the reverse check knows the paper is now incomplete.
        qa_verbatim.CONTENT = work
        quotes, _ = qa_verbatim.book_quotes()
        counts = {}
        for f, p, q, _t in quotes:
            counts.setdefault((p, q), []).append(f)
        unique = [(p, q, fs[0]) for (p, q), fs in sorted(counts.items())
                  if len(fs) == 1 and p in qa_verbatim.SOLVED_IN_FULL]
        if not unique:
            results.append(('D. reverse direction: no singly-quoted question '
                            'exists to test with', False, True))
        else:
            paper, qid, fname = unique[0]
            path = os.path.join(work, fname)
            with open(path, encoding='utf-8') as fh:
                orig = fh.read()
            cut = re.sub(
                r'<div class="asprinted"[^>]*\bdata-src="%s:%s"[^>]*>.*?</div>'
                % (re.escape(paper), re.escape(qid)), '', orig, count=1, flags=re.S)
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(cut)
            got = run_against(work)
            results.append((f'D. the only copy of {paper}:{qid} deleted from '
                            f'{fname}, so that paper is no longer solved in full',
                            got, False))
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(orig)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        qa_verbatim.CONTENT = REAL_CONTENT

    print('CONTROL TEST for the verbatim gate')
    bad = 0
    for name, got, want in results:
        verdict = 'passed' if got else 'FAILED'
        expect = 'must pass' if want else 'must be caught'
        ok = (got == want)
        bad += (not ok)
        print(f'  {"." if ok else "x"} {name}\n      gate {verdict}, {expect}')
    if bad:
        print(f'CONTROL TEST: FAIL, {bad} of {len(results)} behaved wrongly. The '
              f'verbatim gate does not actually catch what it claims to.')
        return 1
    print('CONTROL TEST: pass. Each mechanism was made to fire on its own: forward '
          '(a reworded quote), discovery (a teaching site left with no quote), '
          'reverse (a paper no longer solved in full), layout (a quoted listing '
          'straightened, every word still present), attribution (a misquote in our '
          'own prose beside a perfect quote box), and authority (a glyph flattened '
          'in the transcript itself, which every other check trusts).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
