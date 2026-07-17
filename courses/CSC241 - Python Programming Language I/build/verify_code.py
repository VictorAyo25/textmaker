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

# ======================= report =======================
print(f'CODE GATE: {n} claimed outputs checked against a real interpreter')
if fails:
    print('CODE GATE: FAIL')
    for label, exp, got in fails:
        print(f'\n  x [{label}]\n      manual claims: {exp!r}\n      actual       : {got!r}')
    sys.exit(1)
print('CODE GATE: pass, every claimed output was produced by a real run')
