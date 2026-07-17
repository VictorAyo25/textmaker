"""Execute every output this manual claims, and fail the build on any mismatch.

This is the CSC241 analogue of PHY121's "recompute every number" gate. A printed
output that was never run is a confident guess, and the source manual this course
is authored from contains at least one such guess (its printed p61 claims 690.0
for 10000 * 0.069, where a real interpreter gives 690.0000000000001). We do not
inherit that.

    python verify_code.py

Every claim below is stated the way the page states it, so the claim and its proof
live together. If a page changes, this changes with it.
"""
import io, contextlib, sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

fails = []
n = 0
HERE = os.path.dirname(os.path.abspath(__file__))


def check(label, src, expect):
    """Run src as a script; compare captured stdout with expect."""
    global n
    n += 1
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
    """Evaluate expr; compare repr with expect, as the prompt would echo it."""
    global n
    n += 1
    try:
        got = repr(eval(expr))
    except Exception as e:
        got = f'{type(e).__name__}: {e}'
    if got != expect:
        fails.append((label, expect, got))


def raises(label, fn, expect):
    """Call fn; compare 'ErrorType: message' with expect."""
    global n
    n += 1
    try:
        fn()
        got = 'no error raised'
    except Exception as e:
        got = f'{type(e).__name__}: {e}'
    if got != expect:
        fails.append((label, expect, got))


def traceback_tail(label, src, expect_lines):
    """Run src as a real script in a subprocess; compare the tail of the printed
    traceback with expect_lines.

    Needed because str(exception) is NOT what Python prints. The printer adds the
    caret markers and the "Did you mean" suggestion, so a page showing a traceback
    can only be checked against a real run, never against str(e). This gate learned
    that the hard way: it reported a page as wrong when the page was right.
    """
    global n
    n += 1
    import subprocess, tempfile as _tf
    d = _tf.mkdtemp(prefix='csc241_tb_')
    p = os.path.join(d, 'snippet.py')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(src)
    try:
        r = subprocess.run([sys.executable, p], capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, timeout=20)
        got = [ln.rstrip() for ln in r.stderr.strip().split('\n')][-len(expect_lines):]
    except Exception as e:
        got = [f'{type(e).__name__}: {e}']
    finally:
        import shutil as _sh
        _sh.rmtree(d, ignore_errors=True)
    if got != [ln.rstrip() for ln in expect_lines]:
        fails.append((label, '\n'.join(expect_lines), '\n'.join(got)))


def page(name):
    with open(os.path.join(HERE, 'content', name), encoding='utf-8') as fh:
        return fh.read()


def present(label, needle, html):
    """The page must contain this exact string."""
    global n
    n += 1
    if needle not in html:
        fails.append((label, needle, 'absent from the page'))


# ======================= MODULE ONE =======================
check('m1 hello', 'print("Hello, World!")', 'Hello, World!')
check('m1 script', 'print("Hello, World!")\nprint("I am running from a file.")',
      'Hello, World!\nI am running from a file.')

# ======================= MODULE TWO, UNIT 1 =======================
check('m2u1 print commas', 'print("Ada", 25, "Lagos")', 'Ada 25 Lagos')
check('m2u1 sep dash', 'print("2026", "07", "17", sep="-")', '2026-07-17')
check('m2u1 sep empty', 'print("Ada", "Bob", sep="")', 'AdaBob')
check('m2u1 end empty', 'print("Hello", end="")\nprint("World")', 'HelloWorld')
check('m2u1 apostrophe', 'print("It\'s fine")', "It's fine")
check('m2u1 escaped quotes', r'print("She said, \"Python is cool!\"")',
      'She said, "Python is cool!"')
check('m2u1 newline escape', r'print("Name: Ada\nCity: Lagos")', 'Name: Ada\nCity: Lagos')
check('m2u1 fstring', 'name="Ada"\nage=25\nprint(f"{name} is {age}")', 'Ada is 25')
check('m2u1 no f prefix', 'name="Ada"\nage=25\nprint("{name} is {age}")', '{name} is {age}')
check('m2u1 the output is 0, not "# Even"', 'print(10 % 2)', '0')

# --- alignment: dot forms are derived from a real run, then required verbatim ---
DOT = chr(0xB7)


def dots(s):
    return re.sub(r' +', lambda m: DOT * len(m.group()), s)


_m2 = page('module2.html')
_rows = [f"{'Item':<10}{'Price':>10}",
         f"{'Apple':<10}{1.5:>10.2f}",
         f"{'Banana':<10}{12.75:>10.2f}"]

n += 1
if len({len(r) for r in _rows}) != 1 or len(_rows[0]) != 20:
    fails.append(('m2u1 aligned rows are all 20 wide', '20',
                  str(sorted({len(r) for r in _rows}))))

for r in _rows:
    present(f'm2u1 printed row {r.strip()!r}', r, _m2)
    present(f'm2u1 dot form {dots(r).strip()!r}', dots(r), _m2)

n += 1
_gap = len(_rows[0]) - len('Item') - len('Price')
if _gap != 11:
    fails.append(('m2u1 the "11 dots" claim', '11', str(_gap)))

present('m2u1 table cell :<10', 'Item' + DOT * 6, _m2)
present('m2u1 table cell :>10', DOT * 5 + 'Price', _m2)

n += 1
_fig = f"{'Fig':<10}{3.5:>10.2f}"
_figgap = len(_fig) - len('Fig') - len('3.50')
if _figgap != 13:
    fails.append(('m2u1 "now you try" answer: Fig gap is 13', '13', str(_figgap)))

# ======================= MODULE TWO, UNIT 2 =======================
check('m2u2 reassign', 'x=99\nprint(x)\nx="Take me to your leader."\nprint(x)',
      '99\nTake me to your leader.')
val('m2u2 type int', 'type(25)', "<class 'int'>")
val('m2u2 type float', 'type(3.14)', "<class 'float'>")
val('m2u2 type str', 'type("Ada")', "<class 'str'>")
val('m2u2 type bool', 'type(True)', "<class 'bool'>")
check('m2u2 string concat trap', 'a="5"\nb="3"\nprint(a+b)', '53')
val('m2u2 int("25")', 'int("25")', '25')
val('m2u2 float("3.5")', 'float("3.5")', '3.5')
val('m2u2 str(100)', 'str(100)', "'100'")
val('m2u2 int(3.9) truncates', 'int(3.9)', '3')
val('m2u2 int(-3.9) truncates', 'int(-3.9)', '-3')
val('m2u2 0.1+0.2', '0.1 + 0.2', '0.30000000000000004')
val('m2u2 interest is NOT clean', '10000 * 0.069', '690.0000000000001')
val('m2u2 interest IS clean', '10000 * 0.072', '720.0')
check('m2u2 interest formatted',
      'amount = 10000 * 0.069\nprint(f"Interest: {amount:.2f}")', 'Interest: 690.00')
raises('m2u2 int("xyz") message', lambda: int("xyz"),
       "ValueError: invalid literal for int() with base 10: 'xyz'")

# Module Two, Unit 1 prints this traceback verbatim, including the ~~~^~~ markers
# that sit under the failing operator. Check it against a real run.
traceback_tail('m2u1 ZeroDivisionError printed traceback',
               'print("a")\nprint("b")\nprint(10 / 0)\n',
               ['    print(10 / 0)',
                '          ~~~^~~',
                'ZeroDivisionError: division by zero'])
raises('m2u2 int("3.5") fails too', lambda: int("3.5"),
       "ValueError: invalid literal for int() with base 10: '3.5'")

# ======================= MODULE TWO, UNIT 3 =======================
for expr, exp in [('7 + 5', '12'), ('7 - 5', '2'), ('7 * 5', '35'), ('7 / 5', '1.4'),
                  ('7 // 5', '1'), ('7 % 5', '2'), ('7 ** 2', '49')]:
    val(f'm2u3 arithmetic table {expr}', expr, exp)
val('m2u3 10/2 is a float', '10 / 2', '5.0')
val('m2u3 5/2', '5 / 2', '2.5')
val('m2u3 17//3', '17 // 3', '5')
val('m2u3 17%3', '17 % 3', '2')
val('m2u3 10%2 even', '10 % 2', '0')
val('m2u3 7%2 odd', '7 % 2', '1')
val('m2u3 2**3**2 right assoc', '2 ** 3 ** 2', '512')
val('m2u3 9**0.5 root', '9 ** 0.5', '3.0')
val('m2u3 2+3*4 precedence', '2 + 3 * 4', '14')
val('m2u3 (2+3)*4 brackets', '(2 + 3) * 4', '20')
val('m2u3 chained bmi', '18.5 <= 22.4 <= 24.9', 'True')
val('m2u3 fizzbuzz condition', '15 % 3 == 0 and 15 % 5 == 0', 'True')
for expr, exp in [('5 == 5', 'True'), ('5 != 3', 'True'), ('7 > 5', 'True'),
                  ('4 < 10', 'True'), ('7 >= 7', 'True'), ('2 <= 4', 'True'),
                  ('True and False', 'False'), ('True or False', 'True'),
                  ('not True', 'False')]:
    val(f'm2u3 table {expr}', expr, exp)

TIME = '''total_seconds = {}
hours   = total_seconds // 3600
minutes = (total_seconds // 60) % 60
seconds = total_seconds % 60
print("Hours:", hours)
print("Minutes:", minutes)
print("Seconds:", seconds)'''
check('m2u3 time converter 11730', TIME.format(11730), 'Hours: 3\nMinutes: 15\nSeconds: 30')
check('m2u3 time converter 7325 ("now you try")', TIME.format(7325),
      'Hours: 2\nMinutes: 2\nSeconds: 5')
check('m2u3 dry run', 'a=7\nb=2\na+=b\nc=a//b\nd=a%b\nprint(a,b,c,d)', '9 2 4 1')

# ======================= MODULE TWO, UNIT 4: STRINGS =======================
val('m2u4 index 0', '"Python"[0]', "'P'")
val('m2u4 index -1', '"Python"[-1]', "'n'")
val('m2u4 slice 0:3', '"Python"[0:3]', "'Pyt'")
val('m2u4 len', 'len("Python")', '6')


def _str_assign():
    name = "Python"
    name[0] = "J"


raises('m2u4 strings are immutable', _str_assign,
       "TypeError: 'str' object does not support item assignment")
check('m2u4 upper() does not change the original',
      'name = "Python"\nprint(name.upper())\nprint(name)', 'PYTHON\nPython')
check('m2u4 catching the result',
      'name = "Python"\nname = name.upper()\nprint(name)', 'PYTHON')

# the methods table
val('m2u4 upper', '"ada".upper()', "'ADA'")
val('m2u4 lower', '"ADA".lower()', "'ada'")
val('m2u4 strip', '"  hi  ".strip()', "'hi'")
val('m2u4 replace', '"a-b".replace("-", " ")', "'a b'")
val('m2u4 split with sep', '"a,b".split(",")', "['a', 'b']")
val('m2u4 index sub', '"Ada".index("d")', '1')
val('m2u4 find absent', '"Ada".find("z")', '-1')
val('m2u4 count', '"banana".count("a")', '3')
val('m2u4 startswith', '"https://x".startswith("https")', 'True')
val('m2u4 join', '", ".join(["a", "b"])', "'a, b'")
raises('m2u4 index absent raises', lambda: "Ada".index("z"),
       'ValueError: substring not found')

# split forms
val('m2u4 split no arg', '"70 55 90".split()', "['70', '55', '90']")
val('m2u4 split at @', '"ada@mail.com".split("@")', "['ada', 'mail.com']")
val('m2u4 split with no separator present', '"nothing here".split("@")',
    "['nothing here']")

# the broken first-name snippet
raises('m2u4 index() with no argument', lambda: "Ada Lovelace".index(),
       'TypeError: index expected at least 1 argument, got 0')
# Python does NOT suggest a fix here: 'uppercase' is too far from 'upper' for its
# similarity threshold. It DOES suggest for the closer typo 'uppe'. The page claimed
# a suggestion until this gate caught it, so both behaviours are pinned below.
traceback_tail('m2u4 .uppercase() gets NO suggestion',
               'full_name = "Ada Lovelace"\n'
               'first_name = full_name[0:full_name.index(" ")]\n'
               'print("First name:", first_name.uppercase())\n',
               ["AttributeError: 'str' object has no attribute 'uppercase'"])
traceback_tail('m2u4 .uppe() DOES get a suggestion',
               'print("Ada".uppe())\n',
               ["AttributeError: 'str' object has no attribute 'uppe'. "
                "Did you mean: 'upper'?"])
val('m2u4 index of the space is 3', '"Ada Lovelace".index(" ")', '3')
check('m2u4 corrected first name',
      'full_name = "Ada Lovelace"\nfirst_name = full_name[0:full_name.index(" ")]\n'
      'print("First name:", first_name.upper())', 'First name: ADA')
val('m2u4 the neater answer', '"Ada Lovelace".split()[0]', "'Ada'")

# the strip/lower.replace/len question
check('m2u4 the three-line output question',
      'text = "  Hello, Python!  "\nprint(text.strip())\n'
      'print(text.lower().replace("python", "world"))\nprint(len(text))',
      'Hello, Python!\n  hello, world!  \n18')
val('m2u4 len("  Hello, Python!  ") is 18', 'len("  Hello, Python!  ")', '18')
val('m2u4 "Hello, Python!" is 14 chars', 'len("Hello, Python!")', '14')

# the emails program
check('m2u4 emails program', '''emails = [
    "azu.ezenwoke@university.edu.ng",
    "odunayo.osofuye@university.edu",
    "emmanuel.franklin@university.edu",
    "ada.lovelace@university.edu",
    "bola.ahmed@university.edu",
]
for email in emails:
    username = email.split("@")[0]
    print(f"Email: {email} | Username: {username}")''',
      'Email: azu.ezenwoke@university.edu.ng | Username: azu.ezenwoke\n'
      'Email: odunayo.osofuye@university.edu | Username: odunayo.osofuye\n'
      'Email: emmanuel.franklin@university.edu | Username: emmanuel.franklin\n'
      'Email: ada.lovelace@university.edu | Username: ada.lovelace\n'
      'Email: bola.ahmed@university.edu | Username: bola.ahmed')

# the paragraph analyser, including the empty-piece claim
val('m2u4 splitting leaves an empty final piece', '"A. B.".split(".")',
    "['A', ' B', '']")
check('m2u4 paragraph analyser', '''paragraph = "Python is fun. I like code."
for sentence in paragraph.split("."):
    sentence = sentence.strip()
    if sentence == "":
        continue
    words = len(sentence.split())
    vowels = 0
    for ch in sentence.lower():
        if ch in "aeiou":
            vowels += 1
    print(f"Sentence: {sentence.upper()}")
    print(f"  Words: {words}, Vowels: {vowels}")''',
      'Sentence: PYTHON IS FUN\n  Words: 3, Vowels: 3\n'
      'Sentence: I LIKE CODE\n  Words: 3, Vowels: 5')
# "Python is fun" has 3 vowels: o, i, u. The y is NOT one, per the question's own
# definition (a, e, i, o, u). The page said 4 until this gate caught it.
val('m2u4 "python is fun" vowel count',
    'len([c for c in "python is fun" if c in "aeiou"])', '3')
val('m2u4 y is not in aeiou', '"y" in "aeiou"', 'False')

# isalpha(): the consonant box. The space is what makes the whole string false,
# which is the point the box is making.
val('m2u4 "Ada".isalpha()', '"Ada".isalpha()', 'True')
val('m2u4 "Ada Lovelace".isalpha() is False because of the space',
    '"Ada Lovelace".isalpha()', 'False')
val('m2u4 " ".isalpha()', '" ".isalpha()', 'False')
val('m2u4 "!".isalpha()', '"!".isalpha()', 'False')
# The consonant count is the vowel count's mirror and fails the same way: 8, not
# 7, because y is a consonant under the question's own definition of the vowels.
val('m2u4 "python is fun" consonant count',
    'len([c for c in "python is fun" if c.isalpha() and c not in "aeiou"])', '8')
val('m2u4 "python is fun" letter count',
    'len([c for c in "python is fun" if c.isalpha()])', '11')
val('m2u4 the 8 consonants are exactly these',
    '"".join(c for c in "python is fun" if c.isalpha() and c not in "aeiou")',
    "'pythnsfn'")

# ======================= MODULE THREE, UNIT 1 =======================
check('m3u1 vote', 'age=20\nif age >= 18:\n    print("You may vote.")', 'You may vote.')
check('m3u1 if/else odd',
      'n=7\nif n % 2 == 0:\n    print("even")\nelse:\n    print("odd")', 'odd')
check('m3u1 elif grade A',
      'score=72\nif score>=70:\n    print("A")\nelif score>=60:\n    print("B")\n'
      'elif score>=50:\n    print("C")\nelse:\n    print("F")', 'A')
check('m3u1 elif in the WRONG order prints C',
      'score=72\nif score>=50:\n    print("C")\nelif score>=70:\n    print("A")', 'C')
check('m3u1 nested',
      'n=15\nif n>0:\n    if n % 2 == 0:\n        print("positive and even")\n'
      '    else:\n        print("positive and odd")\nelse:\n    print("not positive")',
      'positive and odd')

FITNESS = '''n = {}
if n > 0:
    if n % 3 == 0 and n % 5 == 0:
        print("Active - FizzBuzz")
    elif n % 3 == 0:
        print("Active - Fizz")
    elif n % 5 == 0:
        print("Active - Buzz")
    else:
        print("Delulu - Not divisible by 3 or 5")
else:
    print("Please enter a positive number")'''
for v, exp in [(15, 'Active - FizzBuzz'), (9, 'Active - Fizz'), (10, 'Active - Buzz'),
               (7, 'Delulu - Not divisible by 3 or 5'),
               (0, 'Please enter a positive number'),   # "now you try"
               (30, 'Active - FizzBuzz')]:              # "now you try"
    check(f'm3u1 fitness n={v}', FITNESS.format(v), exp)

# ======================= MODULE THREE, UNIT 2 =======================
check('m3u2 while 1 to 3', 'i=1\nwhile i<=3:\n    print(i)\n    i+=1', '1\n2\n3')
check('m3u2 for range(5)', 'for i in range(5):\n    print(i)', '0\n1\n2\n3\n4')
check('m3u2 break at 3', 'for i in range(5):\n    if i==3:\n        break\n    print(i)',
      '0\n1\n2')
check('m3u2 continue at 3',
      'for i in range(5):\n    if i==3:\n        continue\n    print(i)', '0\n1\n2\n4')
check('m3u2 for/else WITH break omits "Loop finished"',
      'for i in range(5):\n    if i==3:\n        break\n    print(i)\nelse:\n'
      '    print("Loop finished")', '0\n1\n2')
check('m3u2 for/else WITHOUT break prints it',
      'for i in range(5):\n    print(i)\nelse:\n    print("Loop finished")',
      '0\n1\n2\n3\n4\nLoop finished')
check('m3u2 even-skip-6, fixed version',
      'i=1\nwhile i<=10:\n    if i % 2 == 0 and i != 6:\n        print(i)\n    i+=1',
      '2\n4\n8\n10')
for expr, exp in [('list(range(5))', '[0, 1, 2, 3, 4]'),
                  ('list(range(1,5))', '[1, 2, 3, 4]'),
                  ('list(range(1,10,2))', '[1, 3, 5, 7, 9]'),
                  ('list(range(5,0,-1))', '[5, 4, 3, 2, 1]')]:
    val(f'm3u2 range table {expr}', expr, exp)

# The hanging loop. The page claims: prints 2, then 4, then spins with i stuck at 6.
# Proven with a trip counter rather than by running it as printed, for obvious reasons.
n += 1
_out, _i, _steps = [], 1, 0
while _i <= 10:
    _steps += 1
    if _steps > 500:
        break
    if _i % 2 == 0:
        if _i == 6:
            continue
        _out.append(_i)
    _i += 1
if _out != [2, 4] or _i != 6 or _steps <= 500:
    fails.append(('m3u2 the hanging loop prints 2,4 then sticks at i=6',
                  'out=[2, 4], i=6, does not terminate',
                  f'out={_out}, i={_i}, steps={_steps}'))

check('m3u2 sentinel loop', '''inputs = iter(["Ada", "Bola", "done"])
names = []
while True:
    name = next(inputs)
    if name == "done":
        break
    names.append(name)
print("You entered:", names)''', "You entered: ['Ada', 'Bola']")

check('m3u2 split and convert', '''line = "70 55 90"
parts = line.split()
scores = []
for p in parts:
    scores.append(int(p))
print(scores)''', '[70, 55, 90]')
val('m3u2 split gives strings', '"70 55 90".split()', "['70', '55', '90']")

# ======================= MODULE THREE, UNIT 3 =======================
val('m3u3 len', 'len([70,55,90,45])', '4')
val('m3u3 index 0', '[70,55,90,45][0]', '70')
val('m3u3 index 3', '[70,55,90,45][3]', '45')
val('m3u3 index -1', '[70,55,90,45][-1]', '45')
val('m3u3 index -2', '[70,55,90,45][-2]', '90')
val('m3u3 slice 1:3', '[1,2,3,4,5][1:3]', '[2, 3]')
val('m3u3 slice :2', '[1,2,3,4,5][:2]', '[1, 2]')
val('m3u3 slice 2:', '[1,2,3,4,5][2:]', '[3, 4, 5]')
val('m3u3 slice -3:', '[1,2,3,4,5][-3:]', '[3, 4, 5]')
val('m3u3 list concat', '[1,2]+[3,4]', '[1, 2, 3, 4]')
val('m3u3 list repeat', '[1,2]*2', '[1, 2, 1, 2]')
val('m3u3 tuple index', '(3,4)[0]', '3')
check('m3u3 mutate', 's=[70,55,90,45]\ns[1]=65\nprint(s)', '[70, 65, 90, 45]')
check('m3u3 sort() returns None', 's=[70,55,90]\ns=s.sort()\nprint(s)', 'None')
check('m3u3 sort in place', 's=[70,55,90]\ns.sort()\nprint(s)', '[55, 70, 90]')
check('m3u3 sort reverse=True', 's=[55,70,90]\ns.sort(reverse=True)\nprint(s)',
      '[90, 70, 55]')
check('m3u3 dry run sum of odds',
      'nums=[1,2,3,4,5]\ntotal=0\nfor n in nums:\n    if n%2==0:\n        continue\n'
      '    total+=n\nprint(total)', '9')
raises('m3u3 IndexError message', lambda: [70, 55, 90, 45][4],
       'IndexError: list index out of range')
raises('m3u3 remove ValueError message',
       lambda: ["apples", "bananas", "carrots"].remove("banana"),
       'ValueError: list.remove(x): x not in list')


def _tuple_assign():
    t = (3, 4)
    t[0] = 9


raises('m3u3 tuple TypeError message', _tuple_assign,
       "TypeError: 'tuple' object does not support item assignment")

# ======================= MODULE THREE, UNIT 4 =======================
# Sets are unordered, so compare as sets, never by printed order. Python randomises
# string hashing per process, so a set of strings prints in a DIFFERENT order each
# run. No page may claim a string-set's printed order as reproducible output; the
# only stable forms are len() and sorted(). The trap box shows real varying orders,
# and each is checked below to be a genuine permutation of the members.
val('m3u4 set dedup', 'set(["Alice","Bob","Alice","Eve","Bob"]) == {"Alice","Bob","Eve"}',
    'True')
val('m3u4 unique count', 'len(set(["Alice","Bob","Alice","Eve","Bob"]))', '3')
val('m3u4 sorted() is the stable form',
    'sorted(set(["Alice","Bob","Alice","Eve","Bob"]))', "['Alice', 'Bob', 'Eve']")

# the dictionary methods reference table
val('m3u4 keys() table row', 'list({"name": "John", "age": 25}.keys())',
    "['name', 'age']")
val('m3u4 values() table row', 'list({"name": "John", "age": 25}.values())',
    "['John', 25]")

# the three orders printed in the trap box must each be a real permutation
_m3 = page('module3.html')
_members = {'Alice', 'Bob', 'Eve'}
for _shown in ["{'Alice', 'Eve', 'Bob'}", "{'Bob', 'Alice', 'Eve'}",
               "{'Alice', 'Bob', 'Eve'}"]:
    present(f'm3u4 trap box shows {_shown}', _shown, _m3)
    n += 1
    if {x.strip().strip("'") for x in _shown.strip('{}').split(',')} != _members:
        fails.append((f'm3u4 {_shown} is a permutation of the members',
                      str(_members), _shown))
check('m3u4 broken dedup prints 5',
      'students=["Alice","Bob","Alice","Eve","Bob"]\nstudents=list(students)\n'
      'u=students\nprint("Total unique students:", len(u))', 'Total unique students: 5')
check('m3u4 fixed dedup prints 3',
      'students=["Alice","Bob","Alice","Eve","Bob"]\nu=set(students)\n'
      'print("Total unique students:", len(u))', 'Total unique students: 3')
val('m3u4 union', '{1,2,3,4} | {3,4,5,6} == {1,2,3,4,5,6}', 'True')
val('m3u4 intersection', '{1,2,3,4} & {3,4,5,6} == {3,4}', 'True')
val('m3u4 difference', '{1,2,3,4} - {3,4,5,6} == {1,2}', 'True')
val('m3u4 symmetric difference', '{1,2,3,4} ^ {3,4,5,6} == {1,2,5,6}', 'True')
val('m3u4 difference has a direction', '{3,4,5,6} - {1,2,3,4} == {5,6}', 'True')
val('m3u4 small intersection', '{1,2,3} & {3,4} == {3}', 'True')
val('m3u4 dict lookup', '{"name":"John","age":25}["name"]', "'John'")
check('m3u4 dict add and replace',
      'p={"name":"John","age":25}\np["city"]="Lagos"\np["age"]=26\nprint(p)',
      "{'name': 'John', 'age': 26, 'city': 'Lagos'}")
val('m3u4 keys', 'list({"name":"John","age":25}.keys())', "['name', 'age']")
val('m3u4 values', 'list({"name":"John","age":25}.values())', "['John', 25]")
check('m3u4 items loop',
      'p={"name":"John","age":25}\nfor k,v in p.items():\n    print(k,"is",v)',
      'name is John\nage is 25')
check('m3u4 nested list mutation',
      'person={"name":"John","age":25,"skills":["Python","Java"]}\n'
      'person["skills"].append("C++")\nprint(person["skills"])',
      "['Python', 'Java', 'C++']")
raises('m3u4 KeyError message', lambda: {"name": "John"}["height"], "KeyError: 'height'")

# ======================= MODULE FOUR, UNIT 1 =======================
check('m4u1 define and call', 'def greet():\n    print("Hello!")\n\ngreet()', 'Hello!')
check('m4u1 parameter/argument', 'def greet(name):\n    print("Hello,", name)\n\ngreet("Ada")',
      'Hello, Ada')
check('m4u1 two parameters', 'def add(a, b):\n    print(a + b)\n\nadd(2, 3)', '5')
check('m4u1 return is a value',
      'def square(x):\n    return x * x\n\nprint(square(4))\ny = square(4) + 1\nprint(y)',
      '16\n17')
check('m4u1 print is not return',
      'def shout(x):\n    print(x * 2)\n\nresult = shout(5)\nprint(result)', '10\nNone')
check('m4u1 corrected square', 'def square(x):\n    return x * x\n\nprint(square(4))', '16')
check('m4u1 default parameter',
      'def greet(name="Guest"):\n    print("Hello,", name)\n\ngreet()\ngreet("Ada")',
      'Hello, Guest\nHello, Ada')

# the broken square: missing colon is a SyntaxError, so nothing runs
n += 1
try:
    compile('def square(x)\n    return x * x\nprint(Square(4))', '<m>', 'exec')
    _got = 'compiled, no error'
except SyntaxError:
    _got = 'SyntaxError'
if _got != 'SyntaxError':
    fails.append(('m4u1 def square(x) with no colon is a SyntaxError', 'SyntaxError', _got))


# The page prints this traceback verbatim, carets and suggestion included, so it
# must be checked against a real run rather than against str(e).
traceback_tail('m4u1 Square(4) printed traceback',
               'def square(x):\n    return x * x\nprint(Square(4))\n',
               ['    print(Square(4))',
                '          ^^^^^^',
                "NameError: name 'Square' is not defined. Did you mean: 'square'?"])

# default-before-required is a SyntaxError
n += 1
try:
    compile('def f(a=1, b): pass', '<m>', 'exec')
    _got = 'compiled, no error'
except SyntaxError:
    _got = 'SyntaxError'
if _got != 'SyntaxError':
    fails.append(('m4u1 def f(a=1, b) is a SyntaxError', 'SyntaxError', _got))

HEALTH = '''def is_healthy(bmi):
    if 18.5 <= bmi <= 24.9:
        return "Healthy"
    else:
        return "Unhealthy"

data = iter([("John", "22.4"), ("Ada", "17.9"), ("Bola", "24.9")])
for i in range(3):
    name, raw = next(data)
    bmi = float(raw)
    status = is_healthy(bmi)
    print(f"Patient: {name} | BMI: {bmi} | Status: {status}")'''
check('m4u1 health program', HEALTH,
      'Patient: John | BMI: 22.4 | Status: Healthy\n'
      'Patient: Ada | BMI: 17.9 | Status: Unhealthy\n'
      'Patient: Bola | BMI: 24.9 | Status: Healthy')
check('m4u1 is_healthy(24.95) "now you try"',
      'def is_healthy(bmi):\n    if 18.5 <= bmi <= 24.9:\n        return "Healthy"\n'
      '    else:\n        return "Unhealthy"\nprint(is_healthy(24.95))', 'Unhealthy')

# part (e): the same function, a sentinel loop around it
check('m4u1 health part (e)', '''def is_healthy(bmi):
    if 18.5 <= bmi <= 24.9:
        return "Healthy"
    else:
        return "Unhealthy"

data = iter([("John", "22.4"), ("Ada", "17.9"), ("done", None)])
healthy = 0
total = 0
while True:
    name, raw = next(data)
    if name == "done":
        break
    bmi = float(raw)
    status = is_healthy(bmi)
    total += 1
    if status == "Healthy":
        healthy += 1
print(f"Total: {total}, Healthy: {healthy}, Unhealthy: {total - healthy}")''',
      'Total: 2, Healthy: 1, Unhealthy: 1')

# ======================= MODULE FOUR, UNIT 2 =======================
val('m4u2 import math', '__import__("math").sqrt(16)', '4.0')
check('m4u2 from math import sqrt', 'from math import sqrt\nprint(sqrt(16))', '4.0')
val('m4u2 randint includes both ends',
    'all(1 <= __import__("random").randint(1, 6) <= 6 for _ in range(200))', 'True')

# ======================= MODULE FOUR, UNIT 3 =======================
# Real files, in a throwaway directory.
import tempfile

_tmp = tempfile.mkdtemp(prefix='csc241_gate_')
_cwd = os.getcwd()
os.chdir(_tmp)
try:
    check('m4u3 write with newlines',
          'f = open("names.txt", "w")\nf.write("Ada\\n")\nf.write("Bola\\n")\nf.close()\n'
          'print(open("names.txt").read(), end="")', 'Ada\nBola')
    val('m4u3 read() whole file', 'open("names.txt").read()', "'Ada\\nBola\\n'")
    val('m4u3 readline() first line', 'open("names.txt").readline()', "'Ada\\n'")
    val('m4u3 readlines() list', 'open("names.txt").readlines()', "['Ada\\n', 'Bola\\n']")
    check('m4u3 loop with strip',
          'with open("names.txt") as f:\n    for line in f:\n        print(line.strip())',
          'Ada\nBola')
    check('m4u3 write adds no newline',
          'f = open("j.txt", "w")\nf.write("Ada")\nf.write("Bola")\nf.close()\n'
          'print(open("j.txt").read())', 'AdaBola')
    check('m4u3 with + append prints only "Done writing."',
          'with open("example.txt", "a") as f:\n    f.write("New line added.\\n")\n\n'
          'print("Done writing.")', 'Done writing.')
    check('m4u3 "w" erases an existing file',
          'open("x.txt", "w").write("first")\n'
          'f = open("x.txt", "w")\nf.close()\n'
          'print(repr(open("x.txt").read()))', "''")
    check('m4u3 "a" keeps what is there',
          'open("y.txt", "w").write("first")\n'
          'f = open("y.txt", "a")\nf.write("second")\nf.close()\n'
          'print(open("y.txt").read())', 'firstsecond')
    raises('m4u3 "r" on a missing file', lambda: open("nope.txt"),
           "FileNotFoundError: [Errno 2] No such file or directory: 'nope.txt'")

    # file.close without brackets does nothing and reports nothing
    check('m4u3 file.close (no brackets) is silent',
          'f = open("z.txt", "w")\nf.write("hi")\nf.close\nprint("no error")', 'no error')

    # the students program
    check('m4u3 students program', '''data = iter([("John", "76"), ("Ada", "45"), ("Bola", "30"), ("done", None)])
with open("students.txt", "w") as f:
    while True:
        name, raw = next(data)
        if name == "done":
            break
        score = int(raw)
        f.write(f"{name}, {score}\\n")

passes = 0
fails_ = 0
with open("students.txt", "r") as f:
    for line in f:
        name, score = line.strip().split(", ")
        score = int(score)
        print(f"{name} scored {score}")
        if score >= 45:
            passes += 1
        else:
            fails_ += 1

print(f"Passes: {passes}, Fails: {fails_}")''',
          'John scored 76\nAda scored 45\nBola scored 30\nPasses: 2, Fails: 1')

    # ======================= MODULE FOUR, UNIT 4 =======================
    check('m4u4 try/except ValueError', '''inputs = iter(["xyz"])
try:
    age = int(next(inputs))
    print("Next year you are", age + 1)
except ValueError:
    print("That is not a whole number.")''', 'That is not a whole number.')

    check('m4u4 robust input loop', '''inputs = iter(["xyz", "3.5", "7"])
while True:
    try:
        n_ = int(next(inputs))
        break
    except ValueError:
        print("Not a whole number. Try again.")

print("You entered", n_)''', 'Not a whole number. Try again.\n'
                              'Not a whole number. Try again.\nYou entered 7')

    check('m4u4 try/except/else/finally, file absent', '''try:
    f = open("data.txt")
except FileNotFoundError:
    print("No such file.")
else:
    print("Opened it.")
    f.close()
finally:
    print("Finished trying.")''', 'No such file.\nFinished trying.')
finally:
    os.chdir(_cwd)
    import shutil
    shutil.rmtree(_tmp, ignore_errors=True)

raises('m4u4 TypeError "a" + 1', lambda: "a" + 1,
       'TypeError: can only concatenate str (not "int") to str')

# ======================= MODULE FIVE, UNIT 1 =======================
# Real sqlite3, real database files, in a throwaway directory.
_tmp5 = tempfile.mkdtemp(prefix='csc241_db_')
_cwd5 = os.getcwd()
os.chdir(_tmp5)
try:
    check('m5u1 the five steps', '''import sqlite3
conn = sqlite3.connect("school.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()
conn.close()
print("ok")''', 'ok')

    # the broken version: conn.cursor without brackets
    def _no_brackets():
        import sqlite3
        conn = sqlite3.connect("b.db")
        cursor = conn.cursor          # the bug: no ()
        cursor.execute("CREATE TABLE t (id INTEGER PRIMARY KEY)")

    raises('m5u1 conn.cursor with no brackets', _no_brackets,
           "AttributeError: 'builtin_function_or_method' object has no attribute 'execute'")

    # creating a table twice
    def _twice():
        import sqlite3
        conn = sqlite3.connect("twice.db")
        c = conn.cursor()
        c.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT)")
        c.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT)")

    raises('m5u1 CREATE TABLE twice', _twice,
           'OperationalError: table students already exists')

    check('m5u1 IF NOT EXISTS is safe to repeat', '''import sqlite3
conn = sqlite3.connect("ine.db")
c = conn.cursor()
for _ in range(3):
    c.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()
conn.close()
print("ran three times, no error")''', 'ran three times, no error')

    # INSERT prints nothing at all
    check('m5u1 INSERT displays nothing', '''import sqlite3
conn = sqlite3.connect("school.db")
cursor = conn.cursor()
cursor.execute("INSERT INTO students (name) VALUES ('Ada')")
conn.commit()
conn.close()''', '')

    # no such table
    def _no_table():
        import sqlite3
        conn = sqlite3.connect("empty.db")
        c = conn.cursor()
        c.execute("INSERT INTO students (name) VALUES ('Ada')")

    raises('m5u1 INSERT with no table', _no_table,
           'OperationalError: no such table: students')

    # SELECT gives tuples, id fills itself
    check('m5u1 SELECT gives tuples', '''import sqlite3
conn = sqlite3.connect("sel.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO students (name) VALUES ('Ada')")
cursor.execute("INSERT INTO students (name) VALUES ('Bola')")
conn.commit()
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)
conn.close()''', "(1, 'Ada')\n(2, 'Bola')")

    # forgetting commit silently loses the insert
    check('m5u1 no commit means no data', '''import sqlite3
conn = sqlite3.connect("nc.db")
c = conn.cursor()
c.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()
c.execute("INSERT INTO t (name) VALUES ('Ada')")
conn.close()                      # no commit for the insert

conn = sqlite3.connect("nc.db")
c = conn.cursor()
c.execute("SELECT * FROM t")
print(c.fetchall())
conn.close()''', '[]')

    # the contacts program, part (d)
    check('m5u1 contacts program', '''import sqlite3
data = iter([("Ada", "08011112222"), ("Bola", "08033334444"), ("John", "08055556666")])
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS contacts
                  (id INTEGER PRIMARY KEY, name TEXT, phone TEXT)""")
for i in range(3):
    name, phone = next(data)
    cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
conn.commit()
conn.close()
print("Contacts saved.")''', 'Contacts saved.')

    # part (e): sentinel loop then display
    check('m5u1 contacts part (e)', '''import sqlite3
data = iter([("Ada", "08011112222"), ("Bola", "08033334444"), ("done", None)])
conn = sqlite3.connect("contacts2.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS contacts
                  (id INTEGER PRIMARY KEY, name TEXT, phone TEXT)""")
while True:
    name, phone = next(data)
    if name == "done":
        break
    cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
conn.commit()
cursor.execute("SELECT * FROM contacts")
for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]} | {row[2]}")
conn.close()''', '1 | Ada | 08011112222\n2 | Bola | 08033334444')

    # the "now you try": run again, ids continue
    check('m5u1 "now you try": ids continue across runs', '''import sqlite3
conn = sqlite3.connect("contacts2.db")
cursor = conn.cursor()
cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", ("John", "08055556666"))
conn.commit()
cursor.execute("SELECT id FROM contacts")
print([r[0] for r in cursor.fetchall()])
conn.close()''', '[1, 2, 3]')

    # the apostrophe that breaks string-joined SQL, and the placeholder that does not
    check('m5u1 placeholder survives an apostrophe', '''import sqlite3
conn = sqlite3.connect("ap.db")
c = conn.cursor()
c.execute("CREATE TABLE t (name TEXT)")
c.execute("INSERT INTO t (name) VALUES (?)", ("O'Brien",))
conn.commit()
c.execute("SELECT name FROM t")
print(c.fetchone()[0])
conn.close()''', "O'Brien")

    def _joined_sql_breaks():
        import sqlite3
        conn = sqlite3.connect("ap2.db")
        c = conn.cursor()
        c.execute("CREATE TABLE t (name TEXT)")
        name = "O'Brien"
        c.execute("INSERT INTO t (name) VALUES ('" + name + "')")

    raises('m5u1 joined SQL breaks on an apostrophe', _joined_sql_breaks,
           'OperationalError: near "Brien": syntax error')
finally:
    os.chdir(_cwd5)
    import shutil as _sh5
    _sh5.rmtree(_tmp5, ignore_errors=True)

# ======================= MODULE FIVE, UNIT 2 =======================
# The GUI cannot be clicked here, but its arithmetic and its error can be checked.
check('m5u2 converter maths 100 C',
      'celsius = float("100")\nfahrenheit = celsius * 9 / 5 + 32\n'
      'print(f"{fahrenheit:.1f} F")', '212.0 F')
check('m5u2 converter "now you try" 37 C',
      'celsius = float("37")\nfahrenheit = celsius * 9 / 5 + 32\n'
      'print(f"{fahrenheit:.1f} F")', '98.6 F')


def _get_without_convert():
    celsius = "100"          # what entry.get() hands back
    return celsius * 9 / 5 + 32


# The failure is at the DIVISION, not the multiply: "100" * 9 is a legal string
# repeat. The page quoted the multiply error until this gate caught it.
raises('m5u2 forgetting to convert entry.get()', _get_without_convert,
       "TypeError: unsupported operand type(s) for /: 'str' and 'int'")
val('m5u2 "100" * 9 really does succeed', 'len("100" * 9)', '27')

# tkinter must actually be importable, since the manual promises it ships with Python
n += 1
try:
    import tkinter  # noqa: F401
    _got = 'importable'
except Exception as e:
    _got = f'{type(e).__name__}: {e}'
if _got != 'importable':
    fails.append(('m5u2 tkinter ships with Python', 'importable', _got))

# ======================= MOCK ONE =======================
# Every answer in the mock, executed. A mock with a wrong answer is worse than no
# mock: it teaches the wrong thing to somebody who has no way to check.

# ---- Q1 ----
# (b) the hang: prints 1, 3, then sticks at n = 5
n += 1
_o, _n, _s = [], 1, 0
while _n <= 9:
    _s += 1
    if _s > 500:
        break
    if _n % 2 != 0:
        if _n == 5:
            continue
        _o.append(_n)
    _n += 1
if _o != [1, 3] or _n != 5 or _s <= 500:
    fails.append(('mock1 Q1(b) hangs: prints 1,3 then sticks at n=5',
                  'out=[1, 3], n=5, does not terminate', f'out={_o}, n={_n}, steps={_s}'))
check('mock1 Q1(b) fixed', 'n=1\nwhile n<=9:\n    if n % 2 != 0 and n != 5:\n'
      '        print(n)\n    n+=1', '1\n3\n7\n9')
check('mock1 Q1(c) for/else with break',
      'for i in range(1,6):\n    if i % 4 == 0:\n        break\n    print(i)\n'
      'else:\n    print("All done")', '1\n2\n3')

TICKET = '''age = {}
if age > 0:
    if age < 13:
        print("Child - N500")
    elif age < 18:
        print("Teen - N800")
    elif age >= 60:
        print("Senior - N600")
    else:
        print("Adult - N1200")
else:
    print("Please enter a valid age")'''
for v, exp in [(8, 'Child - N500'), (15, 'Teen - N800'), (70, 'Senior - N600'),
               (30, 'Adult - N1200'), (0, 'Please enter a valid age')]:
    check(f'mock1 Q1(d) age={v}', TICKET.format(v), exp)

check('mock1 Q1(e)', '''line = "8 15 70 30"
count = 0
for part in line.split():
    age = int(part)
    if age > 0:
        if age < 13:
            print(age, "Child - N500")
        elif age < 18:
            print(age, "Teen - N800")
        elif age >= 60:
            print(age, "Senior - N600")
        else:
            print(age, "Adult - N1200")
        count += 1
    else:
        print(age, "Please enter a valid age")
print("Tickets priced:", count)''',
      '8 Child - N500\n15 Teen - N800\n70 Senior - N600\n30 Adult - N1200\n'
      'Tickets priced: 4')

# ---- Q2 ----
check('mock1 Q2(b) broken prints 5',
      'courses = ["CSC241","MAT121","CSC241","PHY121","MAT121"]\ncourses = list(courses)\n'
      'distinct = courses\nprint("Distinct courses:", len(distinct))',
      'Distinct courses: 5')
check('mock1 Q2(b) fixed prints 3',
      'courses = ["CSC241","MAT121","CSC241","PHY121","MAT121"]\ndistinct = set(courses)\n'
      'print("Distinct courses:", len(distinct))', 'Distinct courses: 3')
check('mock1 Q2(b) the loop alternative',
      'courses = ["CSC241","MAT121","CSC241","PHY121","MAT121"]\ndistinct = []\n'
      'for c in courses:\n    if c not in distinct:\n        distinct.append(c)\n'
      'print(len(distinct))', '3')
check('mock1 Q2(c)', '''student = {"name": "Bola", "level": 200, "courses": ["CSC241", "MAT121"]}
student["courses"].append("PHY121")
student["level"] = 300
print(student["courses"])
print(len(student))''', "['CSC241', 'MAT121', 'PHY121']\n3")
check('mock1 Q2(d)', '''data = iter([25, 4, 60, 12])
quantities = []
for i in range(4):
    quantities.append(next(data))
quantities.sort()
print("Sorted:", quantities)
print("Highest:", max(quantities))
print("Lowest:", min(quantities))''',
      'Sorted: [4, 12, 25, 60]\nHighest: 60\nLowest: 4')
check('mock1 Q2(e)', '''line = "25 4 60 12 8"
quantities = []
for part in line.split():
    quantities.append(int(part))
quantities.sort(reverse=True)
reorder = 0
for q in quantities:
    if q < 10:
        reorder += 1
average = sum(quantities) / len(quantities)
print("Sorted:", quantities)
print("Highest:", max(quantities))
print("Lowest:", min(quantities))
print(f"Average: {average:.2f}")
print("Need reordering:", reorder)''',
      'Sorted: [60, 25, 12, 8, 4]\nHighest: 60\nLowest: 4\nAverage: 21.80\n'
      'Need reordering: 2')

# ---- Q3 ----
check('mock1 Q3(b) fixed cube', 'def cube(n):\n    return n ** 3\n\nprint(cube(3))', '27')
n += 1
try:
    compile('def cube(n)\n    return n ** 3\nprint(Cube(3))', '<m>', 'exec')
    _g = 'compiled'
except SyntaxError:
    _g = 'SyntaxError'
if _g != 'SyntaxError':
    fails.append(('mock1 Q3(b) missing colon is a SyntaxError', 'SyntaxError', _g))
traceback_tail('mock1 Q3(b) Cube NameError',
               'def cube(n):\n    return n ** 3\nprint(Cube(3))\n',
               ["NameError: name 'Cube' is not defined. Did you mean: 'cube'?"])
check('mock1 Q3(c) defaults', 'def total(price, tax=0.1):\n    return price + price * tax\n\n'
      'print(total(100))\nprint(total(100, 0.2))', '110.0\n120.0')

GRADE = '''def grade(score):
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "F"
'''
check('mock1 Q3(d)', GRADE + '''data = iter([("Ada", 72), ("Bola", 45), ("John", 65)])
for i in range(3):
    name, score = next(data)
    print(f"Student: {name} | Score: {score} | Grade: {grade(score)}")''',
      'Student: Ada | Score: 72 | Grade: A\nStudent: Bola | Score: 45 | Grade: F\n'
      'Student: John | Score: 65 | Grade: B')
check('mock1 Q3(e)', GRADE + '''data = iter([("Ada", 72), ("Bola", 45), ("John", 65), ("done", 0)])
total = 0
passed = 0
while True:
    name, score = next(data)
    if name == "done":
        break
    print(f"Student: {name} | Score: {score} | Grade: {grade(score)}")
    total += 1
    if score >= 50:
        passed += 1
print(f"Students: {total}, Passed: {passed}, Failed: {total - passed}")''',
      'Student: Ada | Score: 72 | Grade: A\nStudent: Bola | Score: 45 | Grade: F\n'
      'Student: John | Score: 65 | Grade: B\nStudents: 3, Passed: 2, Failed: 1')

# ---- Q4 ----
raises('mock1 Q4(b) index() no argument', lambda: "Grace Hopper".index(),
       'TypeError: index expected at least 1 argument, got 0')
val('mock1 Q4(b) index of space is 5', '"Grace Hopper".index(" ")', '5')
val('mock1 Q4(b) slicing from the space keeps it',
    '"Grace Hopper"[ "Grace Hopper".index(" "): ]', "' Hopper'")
check('mock1 Q4(b) fixed with +1',
      'full_name = "Grace Hopper"\nsurname = full_name[full_name.index(" ") + 1:]\n'
      'print("Surname:", surname.lower())', 'Surname: hopper')
check('mock1 Q4(b) the split alternative',
      'full_name = "Grace Hopper"\nsurname = full_name.split()[1]\n'
      'print("Surname:", surname.lower())', 'Surname: hopper')
check('mock1 Q4(c)', 'tag = "   CSC241 Python   "\nprint(tag.strip())\n'
      'print(tag.upper().replace("PYTHON", "CODE"))\nprint(len(tag.strip()))',
      'CSC241 Python\n   CSC241 CODE   \n13')
val('mock1 Q4(c) len(tag) is 19 not 13', 'len("   CSC241 Python   ")', '19')
check('mock1 Q4(d)', '''regs = ["24/CSC/001", "23/CSC/117", "24/MAT/042", "22/PHY/008", "24/CSC/236"]
for reg in regs:
    year = reg.split("/")[0]
    print(f"Reg: {reg} | Year: {year}")''',
      'Reg: 24/CSC/001 | Year: 24\nReg: 23/CSC/117 | Year: 23\n'
      'Reg: 24/MAT/042 | Year: 24\nReg: 22/PHY/008 | Year: 22\n'
      'Reg: 24/CSC/236 | Year: 24')
val('mock1 Q4(d) split on slash', '"24/CSC/001".split("/")', "['24', 'CSC', '001']")
check('mock1 Q4(e) consonants', '''paragraph = "Python is fun. I like code."
for sentence in paragraph.split("."):
    sentence = sentence.strip()
    if sentence == "":
        continue
    words = len(sentence.split())
    consonants = 0
    for ch in sentence.lower():
        if ch.isalpha() and ch not in "aeiou":
            consonants += 1
    print(f"Sentence: {sentence.lower()}")
    print(f"  Words: {words}, Consonants: {consonants}")''',
      'Sentence: python is fun\n  Words: 3, Consonants: 8\n'
      'Sentence: i like code\n  Words: 3, Consonants: 4')
# the isalpha() claim: without it the spaces are counted and 8 becomes 10
val('mock1 Q4(e) without isalpha the answer is 10',
    'len([c for c in "python is fun" if c not in "aeiou"])', '10')
val('mock1 Q4(e) the 8 consonants',
    'str([c for c in "python is fun" if c.isalpha() and c not in "aeiou"])',
    '"[\'p\', \'y\', \'t\', \'h\', \'n\', \'s\', \'f\', \'n\']"')

# ---- Q5 and Q6: real files and real databases ----
_tmpM = tempfile.mkdtemp(prefix='csc241_mock_')
_cwdM = os.getcwd()
os.chdir(_tmpM)
try:
    check('mock1 Q5(c) only "Log updated." is displayed',
          'with open("log.txt", "a") as f:\n    f.write("Entry recorded.\\n")\n\n'
          'print("Log updated.")', 'Log updated.')
    check('mock1 Q5(d)', '''data = iter(["Things Fall Apart", "Purple Hibiscus"])
count = 2
with open("borrowed.txt", "w") as f:
    for i in range(count):
        title = next(data)
        f.write(title + "\\n")
print("Log saved successfully.")
print(open("borrowed.txt").read(), end="")''',
          'Log saved successfully.\nThings Fall Apart\nPurple Hibiscus')
    check('mock1 Q5(e)', '''data = iter([("Things Fall Apart", 3), ("Purple Hibiscus", 0),
              ("Half of a Yellow Sun", 2), ("done", 0)])
with open("fines.txt", "w") as f:
    while True:
        title, days = next(data)
        if title == "done":
            break
        f.write(f"{title}, {days}\\n")

total_fine = 0
with open("fines.txt", "r") as f:
    for line in f:
        title, days = line.strip().split(", ")
        days = int(days)
        fine = days * 50
        total_fine += fine
        print(f"{title}: {days} days, N{fine}")
print("Total fine: N" + str(total_fine))''',
          'Things Fall Apart: 3 days, N150\nPurple Hibiscus: 0 days, N0\n'
          'Half of a Yellow Sun: 2 days, N100\nTotal fine: N250')

    check('mock1 Q6(d)', '''import sqlite3
data = iter([("Ada", "24/CSC/001"), ("Bola", "24/CSC/117"), ("John", "24/MAT/042")])
conn = sqlite3.connect("registry.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS students
                  (id INTEGER PRIMARY KEY, name TEXT, matric TEXT)""")
for i in range(3):
    name, matric = next(data)
    cursor.execute("INSERT INTO students (name, matric) VALUES (?, ?)", (name, matric))
conn.commit()
conn.close()
print("Students saved.")''', 'Students saved.')

    check('mock1 Q6(e)', '''import sqlite3
data = iter([("Ada", "24/CSC/001"), ("Bola", "24/CSC/117"), ("done", None)])
conn = sqlite3.connect("registry2.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS students
                  (id INTEGER PRIMARY KEY, name TEXT, matric TEXT)""")
while True:
    name, matric = next(data)
    if name == "done":
        break
    cursor.execute("INSERT INTO students (name, matric) VALUES (?, ?)", (name, matric))
conn.commit()
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(f"{row[0]} | {row[1]} | {row[2]}")
conn.close()''', '1 | Ada | 24/CSC/001\n2 | Bola | 24/CSC/117')

    # Q6(b): the fixed-but-no-IF-NOT-EXISTS version fails on a second run
    def _books_twice():
        import sqlite3
        for _ in range(2):
            conn = sqlite3.connect("library.db")
            c = conn.cursor()
            c.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT)")
            conn.commit()
            conn.close()

    raises('mock1 Q6(b) without IF NOT EXISTS the 2nd run fails', _books_twice,
           'OperationalError: table books already exists')
finally:
    os.chdir(_cwdM)
    import shutil as _shM
    _shM.rmtree(_tmpM, ignore_errors=True)

# ======================= report =======================
print(f'CODE GATE: {n} claimed outputs checked against a real interpreter')
if fails:
    print('CODE GATE: FAIL')
    for label, exp, got in fails:
        print(f'\n  x [{label}]\n      manual claims: {exp!r}\n      actual       : {got!r}')
    sys.exit(1)
print('CODE GATE: pass, every claimed output was produced by a real run')
