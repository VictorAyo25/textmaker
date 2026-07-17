"""Execute every output this manual claims, and fail the build on any mismatch.

This is the CSC241 analogue of PHY121's "recompute every number" gate. A printed
output that was never run is a confident guess, and the source manual this course
is authored from contains at least one such guess (its printed p61 claims 690.0
for 10000 * 0.069, where a real interpreter gives 690.0000000000001). We do not
inherit that. Run:  python verify_code.py
"""
import io, contextlib, sys
sys.stdout.reconfigure(encoding='utf-8')
fails = []; n = 0

def check(label, src, expect):
    """expect = exact stdout (including trailing newline handling via strip)."""
    global n; n += 1
    b = io.StringIO()
    try:
        with contextlib.redirect_stdout(b):
            exec(src, {})
        got = b.getvalue()
    except Exception as e:
        got = f'{type(e).__name__}: {e}'
    if got.strip('\n') != expect.strip('\n'):
        fails.append((label, expect, got))

def val(label, expr, expect):
    """expect = repr of the value, as the prompt would echo it."""
    global n; n += 1
    try:
        got = repr(eval(expr))
    except Exception as e:
        got = f'{type(e).__name__}: {e}'
    if got != expect:
        fails.append((label, expect, got))

# ---- Module 1 ----
check('m1 hello', 'print("Hello, World!")', 'Hello, World!')
check('m1 script', 'print("Hello, World!")\nprint("I am running from a file.")',
      'Hello, World!\nI am running from a file.')

# ---- Module 2 Unit 1 ----
check('m2u1 print commas', 'print("Ada", 25, "Lagos")', 'Ada 25 Lagos')
check('m2u1 sep dash', 'print("2026", "07", "17", sep="-")', '2026-07-17')
check('m2u1 sep empty', 'print("Ada", "Bob", sep="")', 'AdaBob')
check('m2u1 end empty', 'print("Hello", end="")\nprint("World")', 'HelloWorld')
check('m2u1 apostrophe', 'print("It\'s fine")', "It's fine")
check('m2u1 escaped quotes', r'print("She said, \"Python is cool!\"")', 'She said, "Python is cool!"')
check('m2u1 newline esc', r'print("Name: Ada\nCity: Lagos")', 'Name: Ada\nCity: Lagos')
check('m2u1 fstring', 'name="Ada"\nage=25\nprint(f"{name} is {age}")', 'Ada is 25')
check('m2u1 no-f', 'name="Ada"\nage=25\nprint("{name} is {age}")', '{name} is {age}')
check('m2u1 align Item/Price', "print(f\"{'Item':<10} {'Price':>10}\")", 'Item            Price')
check('m2u1 align Apple', "print(f\"{'Apple':<10}{1.5:>10.2f}\")", 'Apple           1.50')
# the manual claims 12 spaces between Item and Price
_s = f"{'Item':<10} {'Price':>10}"
n += 1
if (len(_s) - len('Item') - len('Price')) != 12:
    fails.append(('m2u1 the "12 spaces" claim', '12', str(len(_s)-9)))

# ---- Module 2 Unit 2 ----
val('m2u2 age', '25', '25')
check('m2u2 reassign', 'x=99\nprint(x)\nx="Take me to your leader."\nprint(x)',
      '99\nTake me to your leader.')
val('m2u2 type int',   'type(25)',    "<class 'int'>")
val('m2u2 type float', 'type(3.14)',  "<class 'float'>")
val('m2u2 type str',   'type("Ada")', "<class 'str'>")
val('m2u2 type bool',  'type(True)',  "<class 'bool'>")
check('m2u2 str concat trap', 'a="5"\nb="3"\nprint(a+b)', '53')
val('m2u2 int("25")',   'int("25")',   '25')
val('m2u2 float("3.5")','float("3.5")','3.5')
val('m2u2 str(100)',    'str(100)',    "'100'")
val('m2u2 int(3.9)',    'int(3.9)',    '3')
val('m2u2 int(-3.9)',   'int(-3.9)',   '-3')
val('m2u2 0.1+0.2',     '0.1 + 0.2',   '0.30000000000000004')
val('m2u2 interest ugly','10000 * 0.069', '690.0000000000001')
val('m2u2 interest clean','10000 * 0.072', '720.0')
check('m2u2 interest fmt', 'amount = 10000 * 0.069\nprint(f"Interest: {amount:.2f}")',
      'Interest: 690.00')
# the ValueError message the manual prints verbatim
n += 1
try:
    int("xyz"); got = 'no error'
except ValueError as e:
    got = f'ValueError: {e}'
if got != "ValueError: invalid literal for int() with base 10: 'xyz'":
    fails.append(('m2u2 int("xyz") message', "invalid literal for int() with base 10: 'xyz'", got))

# ---- Module 2 Unit 3 ----
for expr, exp in [('7 + 5','12'), ('7 - 5','2'), ('7 * 5','35'), ('7 / 5','1.4'),
                  ('7 // 5','1'), ('7 % 5','2'), ('7 ** 2','49')]:
    val(f'm2u3 table {expr}', expr, exp)
val('m2u3 10/2', '10 / 2', '5.0')
val('m2u3 5/2',  '5 / 2',  '2.5')
val('m2u3 17//3','17 // 3','5')
val('m2u3 17%3', '17 % 3', '2')
val('m2u3 10%2', '10 % 2', '0')
val('m2u3 7%2',  '7 % 2',  '1')
val('m2u3 2**3**2', '2 ** 3 ** 2', '512')
val('m2u3 9**0.5',  '9 ** 0.5',    '3.0')
val('m2u3 2+3*4',   '2 + 3 * 4',   '14')
val('m2u3 (2+3)*4', '(2 + 3) * 4', '20')
val('m2u3 chain bmi', '18.5 <= 22.4 <= 24.9', 'True')
val('m2u3 fizzbuzz and', '15 % 3 == 0 and 15 % 5 == 0', 'True')
for expr, exp in [('5 == 5','True'), ('5 != 3','True'), ('7 > 5','True'),
                  ('4 < 10','True'), ('7 >= 7','True'), ('2 <= 4','True'),
                  ('True and False','False'), ('True or False','True'), ('not True','False')]:
    val(f'm2u3 {expr}', expr, exp)

TIME = '''total_seconds = {}
hours   = total_seconds // 3600
minutes = (total_seconds // 60) % 60
seconds = total_seconds % 60
print("Hours:", hours)
print("Minutes:", minutes)
print("Seconds:", seconds)'''
check('m2u3 time 11730', TIME.format(11730), 'Hours: 3\nMinutes: 15\nSeconds: 30')
check('m2u3 time 7325 (the "now you try")', TIME.format(7325), 'Hours: 2\nMinutes: 2\nSeconds: 5')

# ---- alignment claims (Module 2 Unit 1) ----
# Dot forms stand for real spaces: derive them from a real run, then require that
# exact string to be present in the page. A hand-miscounted dot fails here.
import os, re
DOT = chr(0xB7)

def dots(s):
    return re.sub(r' +', lambda m: DOT * len(m.group()), s)

_page = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content', 'module2.html')
_html = open(_page, encoding='utf-8').read()

_rows = [f"{'Item':<10}{'Price':>10}",
         f"{'Apple':<10}{1.5:>10.2f}",
         f"{'Banana':<10}{12.75:>10.2f}"]

# every row is the same width, which is the claim the box makes
n += 1
if len({len(r) for r in _rows}) != 1 or len(_rows[0]) != 20:
    fails.append(('aligned rows all 20 wide', '20', str(sorted({len(r) for r in _rows}))))

# the printed rows and their dot forms must both appear verbatim
for r in _rows:
    n += 1
    if r not in _html:
        fails.append(('printed row missing from page', r, 'absent'))
    n += 1
    if dots(r) not in _html:
        fails.append(('dot form missing from page', dots(r), 'absent'))

# the "11 dots" claim
n += 1
_gap = len(_rows[0]) - len('Item') - len('Price')
if _gap != 11:
    fails.append(('the "11 dots" claim', '11', str(_gap)))

# table cells :<10 and :>10
for label, want in [('table :<10 cell', 'Item' + DOT * 6),
                    ('table :>10 cell', DOT * 5 + 'Price')]:
    n += 1
    if want not in _html:
        fails.append((label, want, 'absent'))

# the "now you try" answer: Fig / 3.5 in the same format
n += 1
_fig = f"{'Fig':<10}{3.5:>10.2f}"
_figgap = len(_fig) - len('Fig') - len('3.50')
if _figgap != 13:
    fails.append(('"now you try" answer: Fig gap', '13', str(_figgap)))

print(f'CODE GATE: {n} claimed outputs checked against a real interpreter')
if fails:
    print('CODE GATE: FAIL')
    for label, exp, got in fails:
        print(f'\n  x [{label}]\n      manual claims: {exp!r}\n      actual       : {got!r}')
    sys.exit(1)
print('CODE GATE: pass, every claimed output was produced by a real run')
