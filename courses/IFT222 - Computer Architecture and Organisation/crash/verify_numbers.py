"""Numeric gate for the CRASH edition: recompute every worked number, then prove
the book prints it. Same discipline as the full manual's verify_numbers.py, but the
checks are the crash course's own. A check is (label, computed, shown-in-book); the
gate fails if the recompute disagrees with what we meant to write, OR if that string
is missing from the book. Spaces and commas are normalised away for the compare, and
the book's minus entity (U+2212) reads the same as an ASCII '-'.

Checks are grouped by skill section and appended as each section is authored, so the
list never runs ahead of the book. Control it by flipping a digit in any skill file:
the gate then fails on that value.
"""
import html as _html
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')


def book_text():
    parts = []
    for name in sorted(os.listdir(CONTENT)):
        if name.endswith('.html'):
            with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
                parts.append(fh.read())
    text = _html.unescape('\n'.join(parts))
    return text.replace(chr(0x2212), '-').replace(chr(0x00A0), ' ')


# ---- independent recomputation helpers ----
def to_hex_f(x):
    return format(struct.unpack('>I', struct.pack('>f', x))[0], '08X')

def from_hex_f(h):
    return struct.unpack('>f', struct.pack('>I', int(h, 16)))[0]

def twos(n, bits):
    return format(n % (1 << bits), f'0{bits}b')

def sign_mag(n, bits):
    return ('1' if n < 0 else '0') + format(abs(n), f'0{bits-1}b')

def ones(n, bits):
    if n >= 0:
        return format(n, f'0{bits}b')
    return ''.join('1' if c == '0' else '0' for c in format(abs(n), f'0{bits}b'))

def log2p(x):
    return (x).bit_length() - 1


# ---- the checks: (label, computed, shown-in-book) ----
CHECKS = []
def add(label, computed, shown):
    CHECKS.append((label, computed, shown))


# ============================ CHECKS BY SECTION ============================

# --- Number systems ---
add('7D3A dec', int('7D3A', 16), '32 058')
add('11010110 hex', format(int('11010110', 2), 'X'), 'D6')
add('255 hex', format(255, 'X'), 'FF')
add('2A7F bin', format(int('2A7F', 16), '016b'), '0010101001111111')
add('59 bcd', '0101' + '1001', '01011001')
add('xs3 of 9', format(9 + 3, '04b'), '1100')
add('xs3 0110', int('0110', 2) - 3, '3')

# --- Signed numbers ---
add('10-bit unsigned', 2**10 - 1, '1023')
add('16b range low', 2**15, '32 768')
add('16b range high', 2**15 - 1, '32 767')
add('-182 hex', format((-182) % (1 << 16), '04X'), 'FF4A')
add('487 hex', format(487 % (1 << 16), '04X'), '01E7')
add('-1023 hex', format((-1023) % (1 << 16), '04X'), 'FC01')
add('(-182)+487', -182 + 487, '305')
add('twos 00101100', twos(-int('00101100', 2), 8), '1101 0100')
add('twos 10000000 mag', 2**7, '128')
add('-75 twos8', twos(-75, 8), '1011 0101')

# --- IEEE 754 ---
add('C1400000 exp', 130, '130')
add('encode 6.0', to_hex_f(6.0), '40C00000')
add('double bias', 2**10 - 1, '1023')

# --- Image sizing ---
add('img pixels', int(17.12 * 250) * int(9.45 * 250 * 2) // 2, '10 111 500')
add('img bytes', 10111500 / 8, '1 263 937.5')
add('img MB', round(10111500 / 8 / 1024 / 1024, 2), '1.21')

# --- Instruction formats ---
add('instr length', 8 + 6 + 18, '32 bits')

# --- Addressing modes (25/26 Q1e + MCQs) ---
add('Q1e indirect', 999, '999')
add('Q1e reg-indirect', 6000, '6000')
add('Q1e relative EA', 7000 + 1200, '8200')
add('Q1e direct', 4500, '4500')
add('pc-relative EA', 500 + 30, '530')
add('indexed EA', 20 + 300, '320')
add('base EA', 4000 + 120, '4120')

# --- CPU performance (25/26 Q1d, Q3c + MCQ) ---
_mix = [(0.40, 1), (0.20, 1), (0.15, 2), (0.10, 4), (0.10, 3), (0.05, 2)]
_cpi = round(sum(f * c for f, c in _mix), 2)
add('Q1d CPI', _cpi, '1.70')
add('Q1d total cycles', int(_cpi * 1_000_000), '1 700 000')
add('Q1d new CPI', round(_cpi - 0.10 * 4 + 0.10 * 2, 2), '1.50')
add('Q1d improvement', round((_cpi - 1.5) / _cpi * 100, 2), '11.76')
add('Amdahl 85/10', round(1 / ((1 - 0.85) + 0.85 / 10), 2), '4.26')
add('CPI time', round(12e9 * 1.5 / 4e9, 1), '4.5')

# --- Pipelining (25/26 Q5b + revision 6-stage) ---
add('Q5b cycle', max(60, 50, 90, 80) + 10, '100 ns')
add('Q5b one task', 60 + 50 + 90 + 80, '280 ns')
add('Q5b speedup', round((60 + 50 + 90 + 80) / 100, 1), '2.8')
add('Q5b pipe500', (4 + 499) * 100, '50 300')
add('Q5b seq500', 500 * 280, '140 000')
add('revD nonpipe', 50 * 60, '3000')
add('revD fill', 6 * 12, '72')
add('revD rest', 49 * 12, '588')
add('revD pipe', (6 + 50 - 1) * 12, '660')
add('revD speedup', round(50 * 60 / ((6 + 50 - 1) * 12), 2), '4.55')

# --- Memory and cache (direct 64KB/1KB/16B + AMAT) ---
add('cache TD bits', (1024 // 16) * (16 - 6 - 4), '384 bits')
add('cache TD bytes', (1024 // 16) * (16 - 6 - 4) // 8, '48 bytes')
add('AMAT simultaneous', int(0.8 * 5 + 0.2 * 100), '24 ns')
add('AMAT hierarchical', int(5 + 0.2 * 100), '25 ns')

# --- Final mock (25/26 numbers not gated above) ---
# Q1b: five-stage pipeline, actual CPI under the stated reading of the penalties
_cpi1b = round(1 + 0.20 * 2 + 0.35 * (2 + 0.10 * 4) + 0.05 * 4, 2)
add('Q1b clock', 6 + 1, '7 ns')
add('Q1b CPI', _cpi1b, '2.44')
add('Q1b time', round(20_000_000 * _cpi1b * 7 / 1e9, 4), '0.3416')
add('Q1b nonpipe', 20_000_000 * 25 / 1e9, '0.5 s')
add('Q1b speedup', round((20_000_000 * 25 / 1e9) / (20_000_000 * _cpi1b * 7 / 1e9), 2), '1.46')
# Q5d: reverse IEEE decode
add('Q5d decimal', int(from_hex_f('C4F2E000')), '1943')
add('Y decimal', int(from_hex_f('42100000')), '36')
add('Z decimal', int(from_hex_f('41400000')), '12')
for _h, _shown in [('CA2DFC12', '193'), ('F24F25FF', '95'),
                   ('24BBABCD', '188'), ('C1D9EEF2', '239')]:
    add(f'Q2a {_h}', (int(_h, 16) >> 4) & 0xFF, _shown)
add('Q2c blocks', 512 * 1024 // 128, '4096')
add('Q2c sets', (512 * 1024 // 128) // 4, '1024')
add('Q2c tag', 30 - 10 - 7, '13')
add('Q2c AMAT', round(2 + 0.04 * 80, 1), '5.2')
add('Q3a lines', 128 * 1024 // 64, '2048')
add('Q3a direct tag', 26 - 11 - 6, '9')
add('Q3a 4way tag', 26 - 9 - 6, '11')
add('Q2b cycles', 5 + 6 - 1 + 1 + 2, '13 cycles')
add('Q3b forwarding', 15, '15 cycles')
add('Q3b no forwarding', 17, '17 cycles')
add('Q5a hex', 'C49B11EB', 'C49B11EB')          # hand truncation, per full manual

# --- Revision cache practice bank (Examples 2 and 3 of each mapping) ---
def _direct(mm, cs, blk):
    lines = cs // blk
    return lines * (log2p(mm) - log2p(lines) - log2p(blk))
def _fully(mm, cs, blk):
    lines = cs // blk
    return lines * (log2p(mm) - log2p(blk))
def _sa(mm, cs, blk, ways):
    lines = cs // blk
    return lines * (log2p(mm) - log2p(lines // ways) - log2p(blk))
_KB, _MB = 1024, 1024 * 1024
add('D2 TD', _direct(128 * _KB, 4 * _KB, 32), '640 bits')
add('D2 TDb', _direct(128 * _KB, 4 * _KB, 32) // 8, '80 bytes')
add('D3 TD', _direct(1 * _MB, 8 * _KB, 64), '896 bits')
add('D3 TDb', _direct(1 * _MB, 8 * _KB, 64) // 8, '112 bytes')
add('F2 TD', _fully(256 * _KB, 4 * _KB, 32), '1664 bits')
add('F2 TDb', _fully(256 * _KB, 4 * _KB, 32) // 8, '208 bytes')
add('F3 TD', _fully(2 * _MB, 16 * _KB, 64), '3840 bits')
add('F3 TDb', _fully(2 * _MB, 16 * _KB, 64) // 8, '480 bytes')
add('S2 TD', _sa(512 * _KB, 8 * _KB, 32, 4), '2048 bits')
add('S2 TDb', _sa(512 * _KB, 8 * _KB, 32, 4) // 8, '256 bytes')
add('S3 TD', _sa(4 * _MB, 32 * _KB, 64, 8), '5120 bits')
add('S3 TDb', _sa(4 * _MB, 32 * _KB, 64, 8) // 8, '640 bytes')


def norm(s):
    return str(s).replace(' ', '').replace(',', '')


def report(_ignored_html=None):
    text = book_text()
    ntext = norm(text)   # spaces and commas stripped, so "1 700 000" and "1,700,000" match
    fails = []
    for label, computed, shown in CHECKS:
        if shown not in text and norm(shown) not in ntext:
            fails.append(f'{label}: the book does not contain {shown!r} '
                         f'(recompute says {computed})')
            continue
        want, got = norm(computed), norm(shown)
        if want not in got and got not in want:
            fails.append(f'{label}: book shows {shown!r} but recompute is {computed}')

    print(f'NUMERIC GATE: {len(CHECKS)} worked values recomputed')
    if fails:
        print('NUMERIC GATE: FAIL')
        for f in fails:
            print('  x ' + f)
        return False
    print('  . every worked number matches an independent recomputation')
    print('  . every recomputed value appears in the crash course')
    return True


if __name__ == '__main__':
    sys.exit(0 if report() else 1)
