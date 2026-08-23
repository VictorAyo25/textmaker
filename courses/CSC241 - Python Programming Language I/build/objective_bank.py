"""The objective half of the CSC241 paper, as questions.

WHY THIS FILE EXISTS. The student confirmed on 2026-08-09 that every paper this
semester except the physics one is a SINGLE paper carrying an objective section
AND a theory section. Every edition of this manual before 2026-08-20 taught and
drilled the theory half only.

WHERE THE QUESTIONS COME FROM. Unlike IFT222, this course has no computer-based
test among its sources, so there is nothing to transcribe. These are AUTHORED,
and the book says so plainly rather than implying they are the examiner's. They
are grounded in two things: what this manual teaches, unit by unit, and what the
ten past papers in sources/exams actually ask about. The paper's own habits are
copied deliberately: it loves "what will be the output", it loves "identify and
correct the error", and it asks for properties by name (lists are ordered, sets
are unique, strings are immutable), so the bank does the same in objective form.

HOW THE CODE CLAIMS ARE KEPT HONEST. Every question carrying a `code` block also
carries `runs: True`, and gen_objective.py EXECUTES that code and refuses to
write the section unless the real interpreter produces exactly the option marked
correct. verify_code.py imports this file and runs the same claims as part of the
standing gate, so a claim cannot drift after the fact. No output in this bank was
typed from memory.

THE HOUSE RULE. Every option is explained, right and wrong alike, and an
explanation names an option by its words, never by its letter.
"""

# Each entry:
#   id, module, topic, prompt
#   code    optional listing shown with the question, exactly as the reader sees it
#   options 4 strings, in the order they are printed
#   answer  index into options
#   why     4 strings, one per option, in the same order
#   runs    True when the answer is this code's real stdout, checked by execution
#   note    optional line printed under the answer

Q = []


def q(**kw):
    kw.setdefault('runs', False)
    Q.append(kw)


# ===========================================================================
# MODULE ONE: what Python is, and getting it running
# ===========================================================================
q(id='m1-01', module=1, topic='What Python is',
  prompt='Python is best described as which kind of language?',
  options=['A compiled language, translated to machine code before it runs',
           'An interpreted, high-level, general-purpose language',
           'A markup language for describing documents',
           'An assembly language for a specific processor family'],
  answer=1,
  why=['Wrong. Compilation to machine code ahead of running is the C and Java '
       'model. Python translates and runs statement by statement through an '
       'interpreter, which is why an error can appear only when that line runs.',
       'Correct. Interpreted means a program runs it line by line; high-level '
       'means it hides the machine; general-purpose means it is not tied to one '
       'kind of task.',
       'Wrong. A markup language describes how content is structured, like HTML. '
       'Python computes, it does not mark up.',
       'Wrong. Assembly is tied to one processor and its instruction set. Python '
       'code runs unchanged wherever the interpreter runs.'],
  explanation='Interpreted, high-level, general-purpose. Those three words are '
              'the definition the paper wants back.')

q(id='m1-02', module=1, topic='Interpreted execution',
  prompt='A Python script contains a syntax error on its last line. What happens '
         'when you run it?',
  options=['The first lines run, then the error is reported when that line is reached',
           'Nothing runs: the whole file is checked before any of it executes',
           'The error is ignored and the script finishes normally',
           'The line is skipped and the rest of the script continues'],
  answer=1,
  why=['Wrong, and it is the trap. This is true of a NAME error or a type error, '
       'which are found only when the line runs, but a SYNTAX error is found while '
       'the file is being parsed, before anything executes.',
       'Correct. Python parses the whole file first. A syntax error anywhere stops '
       'it before the first line runs, which is why a stray colon can produce no '
       'output at all.',
       'Wrong. Python never ignores an error. Something is always reported.',
       'Wrong. Python does not skip statements it cannot parse. There is no '
       '"carry on regardless" mode.'],
  explanation='Syntax errors are found at parse time, before execution. Runtime '
              'errors are found when their line runs. Knowing which is which '
              'explains why some faulty scripts print nothing at all.')

q(id='m1-03', module=1, topic='Features of Python',
  prompt='Which of these is NOT a stated advantage of Python?',
  options=['It is easy to read, with a syntax close to English',
           'It is portable: the same code runs on different platforms',
           'It is the fastest executing language available',
           'It has a large standard library and a large community'],
  answer=2,
  why=['Wrong choice, because readability IS an advantage. The whitespace rules '
       'exist to force it.',
       'Wrong choice, because portability IS an advantage. The interpreter hides '
       'the platform.',
       'Correct, and this is the one to remember. Interpretation costs speed. '
       'Python is chosen for programmer time, not for execution time, and a paper '
       'listing slow execution as a disadvantage of Python is common.',
       'Wrong choice, because the standard library IS an advantage. It is the '
       '"batteries included" claim.'],
  explanation='Speed of execution is a DISadvantage of Python, not an advantage. '
              'Everything else on that list is real.')

q(id='m1-04', module=1, topic='The interactive prompt',
  prompt='At the interactive prompt you type 2 + 3 and press enter. Why does 5 '
         'appear even though you never wrote print?',
  options=['The prompt echoes the value of any expression you type',
           'Python adds a print automatically to every line of every program',
           'The plus operator prints its result',
           'It does not appear; the prompt shows nothing without print'],
  answer=0,
  why=['Correct. The interactive prompt evaluates what you type and displays the '
       'result. That is a feature of the prompt, not of the language.',
       'Wrong, and this is the trap. Inside a SCRIPT, 2 + 3 on its own line '
       'computes 5 and throws it away silently. Only the prompt echoes.',
       'Wrong. The plus operator produces a value and does nothing else with it.',
       'Wrong. The prompt does echo. Try it: this is the difference between the '
       'three kinds of code block this manual sets out.'],
  explanation='The prompt echoes; a script does not. This is why the manual marks '
              'its three kinds of block differently, and why copying prompt '
              'examples into a file makes the output vanish.')

q(id='m1-05', module=1, topic='Running a script',
  prompt='What is the correct way to run a saved file called grades.py from the '
         'command line?',
  options=['run grades.py', 'python grades.py', 'grades.py run', 'execute python grades.py'],
  answer=1,
  why=['Wrong. There is no run command. The interpreter is the program you '
       'launch, and the script is what you hand it.',
       'Correct. You launch the interpreter, python, and give it the file to run '
       'as its argument.',
       'Wrong. The order is wrong and run is not a Python word.',
       'Wrong. There is no execute command wrapping it.'],
  explanation='python <filename>. The interpreter is the program; your file is '
              'the input to it.')

q(id='m1-06', module=1, topic='Comments',
  prompt='Which line is a valid single-line comment in Python?',
  options=['// this is a comment', '/* this is a comment */',
           '# this is a comment', '-- this is a comment'],
  answer=2,
  why=['Wrong. Two slashes are the C, Java and JavaScript comment. In Python two '
       'slashes are the floor division operator, so this line is an error.',
       'Wrong. Slash-star is the C block comment. Python has no block comment '
       'syntax at all.',
       'Correct. The hash starts a comment that runs to the end of the line.',
       'Wrong. Two hyphens are the SQL comment, which matters here because this '
       'course also writes SQL through Python. The two languages do not share it.'],
  explanation='Hash to end of line. Python has no block comment: a run of hashes, '
              'or a string used as a docstring, is how several lines are done.')

q(id='m1-07', module=1, topic='Indentation',
  prompt='In Python, what does indentation do?',
  options=['Nothing: it is style only, as in C or Java',
           'It marks which statements belong to a block, and is part of the syntax',
           'It sets how far output is printed from the left edge',
           'It is required only inside functions'],
  answer=1,
  why=['Wrong, and it is the single biggest habit to break coming from another '
       'language. In Python the indentation IS the block structure, so getting it '
       'wrong changes the meaning of the program or stops it running.',
       'Correct. Where C uses braces, Python uses the indentation itself. An '
       'inconsistent indent raises IndentationError.',
       'Wrong. Output position is decided by what you print, not by how the '
       'source is laid out.',
       'Wrong. Every block needs it: if, else, for, while, def, class, try, with.'],
  explanation='Indentation is syntax, not decoration. It replaces the braces that '
              'other languages use to group statements.')

q(id='m1-08', module=1, topic='Identifiers',
  prompt='Which of these is a VALID Python variable name?',
  options=['2nd_score', 'class', 'total score', '_total2'],
  answer=3,
  why=['Wrong. A name may not start with a digit. Letters and the underscore '
       'only, then digits are allowed after the first character.',
       'Wrong. class is a reserved keyword, so it cannot be used as a name. The '
       'same applies to if, for, def, and the rest.',
       'Wrong. A space separates two names, so Python reads this as two things '
       'and reports a syntax error. Use an underscore.',
       'Correct. It starts with an underscore, which is allowed, and the digit is '
       'not in first position.'],
  explanation='Start with a letter or underscore, then letters, digits or '
              'underscores, and never a keyword. Names are case sensitive, so '
              'Total and total are two different variables.')


# ===========================================================================
# MODULE TWO: syntax, variables, types, operators, strings
# ===========================================================================
q(id='m2-01', module=2, topic='Dynamic typing',
  prompt='What does it mean to say Python is dynamically typed?',
  options=['A variable must be declared with its type before use',
           'The type belongs to the value, and a name may be rebound to a value of '
           'another type',
           'Types are checked by the compiler before the program runs',
           'Every value in Python is a string until converted'],
  answer=1,
  why=['Wrong, and this is the static-typing model of C and Java. Python needs no '
       'declaration at all: assignment creates the name.',
       'Correct. x = 5 then x = "five" is legal, because the type travels with '
       'the value, not with the name.',
       'Wrong. There is no compiler pass checking types ahead of time. A type '
       'error surfaces when the offending line runs.',
       'Wrong. This describes what input() returns, not what Python does '
       'generally. 5 is an int the moment you write it.',],
  explanation='The value carries the type; the name is only a label. That is why '
              'type() reports on the value and why a name can change type '
              'mid-program.')

q(id='m2-02', module=2, topic='input() returns a string', runs=True,
  prompt='A program does age = input() and the user types 20. What is printed?',
  code='age = "20"        # this is exactly what input() hands back\n'
       'print(type(age).__name__)\nprint(age * 2)',
  options=['int\n40', 'str\n2020', 'str\n40', 'int\n2020'],
  answer=1,
  why=['Wrong on both lines. input() never returns an int, and star on a string '
       'repeats rather than multiplies.',
       'Correct. input() always returns a str, so type reports str, and "20" * 2 '
       'repeats the characters to give 2020.',
       'Wrong on the second line. 40 would need age to be a number; it is a '
       'string, so star repeats it.',
       'Wrong on the first line. The value came from input(), so it is a string '
       'however numeric it looks.'],
  explanation='input() always returns a string. That is why age + 5 raises '
              'TypeError and age * 2 gives 2020, and it is the single most common '
              'first-program bug in this course. Wrap it in int() or float().')

q(id='m2-03', module=2, topic='Integer division', runs=True,
  prompt='What is printed?',
  code='print(7 / 2)\nprint(7 // 2)\nprint(7 % 2)',
  options=['3.5\n3\n1', '3\n3\n1', '3.5\n3.5\n1', '3.5\n3\n3.5'],
  answer=0,
  why=['Correct. A single slash is true division and always gives a float, even '
       'when it divides exactly. Double slash floors the result to an integer. '
       'The percent sign gives the remainder.',
       'Wrong. A single slash never truncates in Python 3. 7 / 2 is 3.5, not 3. '
       'That was Python 2 behaviour, and the change is a favourite exam point.',
       'Wrong. Double slash is floor division, so it produces 3, not 3.5.',
       'Wrong. The percent sign is remainder, not division, so 7 % 2 is 1.'],
  explanation='Slash gives a float, double slash floors, percent is the '
              'remainder. Note 7 // 2 is 3 but -7 // 2 is -4, because flooring '
              'goes DOWN, not towards zero.')

q(id='m2-04', module=2, topic='Operator precedence', runs=True,
  prompt='What is printed?',
  code='print(2 + 3 * 4 ** 2)',
  options=['50', '80', '400', '100'],
  answer=0,
  why=['Correct. Exponent first: 4 ** 2 is 16. Then multiply: 3 * 16 is 48. Then '
       'add: 2 + 48 is 50.',
       'Wrong. That is (2 + 3) * 4 ** 2, which adds before multiplying. Addition '
       'is last, not first.',
       'Wrong. That is ((2 + 3) * 4) ** 2, which applies the exponent to '
       'everything.',
       'Wrong. That is (2 + 3 * 4) ** 2, exponent applied last.'],
  explanation='Exponent, then multiply and divide, then add and subtract. When in '
              'doubt in the exam, write the brackets in yourself: they cost '
              'nothing and remove the question.')

q(id='m2-05', module=2, topic='Exponent associativity', runs=True,
  prompt='What is printed?',
  code='print(2 ** 3 ** 2)',
  options=['64', '512', '18', '12'],
  answer=1,
  why=['Wrong. 64 is (2 ** 3) ** 2, grouping from the left. The exponent operator '
       'is the exception: it groups from the RIGHT.',
       'Correct. It reads as 2 ** (3 ** 2), which is 2 ** 9, which is 512.',
       'Wrong. 18 would be 2 * 3 * 3, which is not what any part of this '
       'expression does.',
       'Wrong. There is no reading of this expression that gives 12.'],
  explanation='Exponent is right-associative, and it is the only common operator '
              'that is. Everything else in this course groups left to right.')

q(id='m2-06', module=2, topic='Augmented assignment', runs=True,
  prompt='What is printed?',
  code='x = 10\nx += 5\nx -= 3\nx *= 2\nprint(x)',
  options=['24', '12', '30', '17'],
  answer=0,
  why=['Correct. 10 plus 5 is 15, minus 3 is 12, times 2 is 24. Each line uses '
       'the value the line before it left behind.',
       'Wrong. 12 is the value after the subtraction. The multiplication still '
       'has to happen.',
       'Wrong. 30 would be 15 times 2, which skips the subtraction.',
       'Wrong. 17 would be 10 plus 5 plus 2, which misreads two of the three '
       'operators.'],
  explanation='x += 5 is exactly x = x + 5. Work these line by line and write the '
              'running value in the margin; the exam asks this shape often.')

q(id='m2-07', module=2, topic='Comparison chaining', runs=True,
  prompt='What is printed?',
  code='x = 5\nprint(1 < x < 10)\nprint(x == 5 and x != 5)',
  options=['True\nFalse', 'True\nTrue', 'False\nFalse', 'TypeError'],
  answer=0,
  why=['Correct. Python allows a chained comparison, and 1 < 5 < 10 is True. The '
       'second line asks for something and its own opposite at once, which can '
       'never be True.',
       'Wrong. The second line cannot be True: x == 5 and x != 5 contradict each '
       'other by construction.',
       'Wrong. The first line is True, because chaining is legal in Python and '
       '5 does lie between 1 and 10.',
       'Wrong. Nothing here is a type error; all the operands are numbers.'],
  explanation='Chained comparison is real Python and reads exactly as it does in '
              'mathematics. Most languages do not have it, so it is worth a mark '
              'when the paper shows one.')

q(id='m2-08', module=2, topic='and, or, not', runs=True,
  prompt='What is printed?',
  code='print(True and False or True)\nprint(not True and False)',
  options=['True\nFalse', 'False\nFalse', 'True\nTrue', 'False\nTrue'],
  answer=0,
  why=['Correct. and binds tighter than or, so the first line is (True and False) '
       'or True, which is False or True, which is True. On the second, not binds '
       'tightest, so it is (not True) and False, which is False and False.',
       'Wrong. The first line is True, because the or rescues it: only one side '
       'of an or needs to be true.',
       'Wrong. The second line is False. not True is False, and False and '
       'anything is False.',
       'Wrong on both counts, and it has the precedence backwards.'],
  explanation='Precedence among the three: not, then and, then or. Read them in '
              'that order and these questions become mechanical.')

q(id='m2-09', module=2, topic='Type conversion', runs=True,
  prompt='What is printed?',
  code='print(int("7") + int(3.9))\nprint(float("2.5") * 2)\nprint(str(4) + "2")',
  options=['10\n5.0\n42', '10.9\n5.0\n6', '11\n5.0\n42', '10\n5\n42'],
  answer=0,
  why=['Correct. int("7") is 7 and int(3.9) TRUNCATES to 3, so the sum is 10. '
       'float("2.5") * 2 is 5.0, a float because one operand is. str(4) + "2" '
       'joins two strings into "42".',
       'Wrong. int() applied to a float does not keep the fraction. It truncates '
       'towards zero.',
       'Wrong. int(3.9) is 3, not 4. int() truncates, it does not round; round() '
       'is the function that rounds.',
       'Wrong. Multiplying a float by an int gives a float, so it prints 5.0, '
       'with the point.'],
  explanation='int() truncates towards zero and round() rounds. Mixing an int '
              'with a float gives a float. Plus on two strings joins them.')

q(id='m2-10', module=2, topic='Strings are immutable',
  prompt='What is meant by saying that Python strings are immutable?',
  options=['A string cannot be printed twice',
           'Once created, a string object cannot be changed; operations return a '
           'new string',
           'A string cannot be assigned to a variable more than once',
           'A string cannot contain numbers'],
  answer=1,
  why=['Wrong. Printing does not change anything, and there is no limit on how '
       'often you may print.',
       'Correct. s.upper() hands back a NEW string and leaves s untouched, and '
       's[0] = "X" raises TypeError. To "change" a string you must rebind the '
       'name to a new one.',
       'Wrong. Rebinding a name is always allowed. That changes what the name '
       'points to, not the string it used to point at.',
       'Wrong. "abc123" is a perfectly ordinary string. The characters in it are '
       'irrelevant to mutability.'],
  explanation='Immutable means the object cannot be modified in place. This is a '
              'question the paper asks in words ("Strings are Immutable. Explain '
              'and with reasons."), so have the sentence ready and an example '
              'with it.')

q(id='m2-11', module=2, topic='String indexing', runs=True,
  prompt='What is printed?',
  code='s = "PYTHON"\nprint(s[0], s[-1], s[1:4], s[::-1])',
  options=['P N YTH NOHTYP', 'P N YTHO NOHTYP', 'Y N YTH NOHTYP', 'P O YTH NOHTYP'],
  answer=0,
  why=['Correct. Index 0 is the first character, minus 1 is the last, a slice '
       'stops BEFORE its end index so 1:4 gives characters 1, 2 and 3, and a step '
       'of minus 1 walks the string backwards.',
       'Wrong. The slice s[1:4] does not include index 4, so it is three '
       'characters, not four.',
       'Wrong. s[0] is P. Python indexes from 0, not from 1.',
       'Wrong. s[-1] is the last character, N, not the second to last.'],
  explanation='Index from 0, negative counts from the end, a slice excludes its '
              'stop, and [::-1] reverses. Those four facts answer most string '
              'questions on this paper.')

q(id='m2-12', module=2, topic='String methods', runs=True,
  prompt='What is printed?',
  code='s = "  Hello World  "\nprint(s.strip().upper())\nprint(s.strip().split())\n'
       'print("-".join(["a", "b", "c"]))',
  options=['HELLO WORLD\n[\'Hello\', \'World\']\na-b-c',
           'HELLO WORLD\n[\'Hello World\']\na-b-c',
           '  HELLO WORLD  \n[\'Hello\', \'World\']\na-b-c',
           'Hello World\n[\'Hello\', \'World\']\nabc'],
  answer=0,
  why=['Correct. strip() removes the leading and trailing spaces, upper() '
       'uppercases what is left, split() with no argument splits on whitespace '
       'into a list of words, and join() glues a list together with the string it '
       'is called on as the separator.',
       'Wrong. split() with no argument splits on EVERY run of whitespace, so two '
       'words come back as two items.',
       'Wrong. strip() really does remove the outer spaces. That is its only job.',
       'Wrong on two counts: upper() does uppercase, and join() really does put '
       'the hyphen between the items.'],
  explanation='strip, upper, lower, split, join, replace, find. Those seven cover '
              'nearly every string question this course has ever set.')

q(id='m2-13', module=2, topic='String repetition', runs=True,
  prompt='What is printed?',
  code='print("ab" * 3)\nprint("ab" + "3")',
  options=['ababab\nab3', 'ab3\nababab', 'abababab\nab3', 'TypeError\nab3'],
  answer=0,
  why=['Correct. A string times an integer repeats it. A string plus a string '
       'joins them. Both operators are overloaded for strings.',
       'Wrong, and it has the two operators swapped. Star repeats, plus joins.',
       'Wrong. Times 3 gives three copies, not four.',
       'Wrong. String times int is perfectly legal. It is string PLUS int that '
       'raises TypeError.'],
  explanation='Star repeats, plus joins, and "ab" + 3 is the error. The operator '
              'means different things for numbers and for strings, which is what '
              'operator overloading is.')

q(id='m2-14', module=2, topic='f-strings and format', runs=True,
  prompt='What is printed?',
  code='name = "Ada"\nscore = 87.456\nprint(f"{name} scored {score:.1f}")',
  options=['Ada scored 87.456', 'Ada scored 87.5', 'Ada scored 87.4',
           '{name} scored {score:.1f}'],
  answer=1,
  why=['Wrong. The .1f asks for one decimal place, so the full value is not '
       'printed.',
       'Correct. The f before the quote turns it into a formatted string, the '
       'braces are replaced by the values, and .1f rounds to one decimal place, '
       'giving 87.5.',
       'Wrong. Formatting ROUNDS, it does not truncate, and 87.456 rounds up to '
       '87.5.',
       'Wrong. That is what you get WITHOUT the f prefix, which is a real and '
       'common slip: the braces then print literally.'],
  explanation='f"..." substitutes; :.2f fixes the decimal places. Forgetting the '
              'f is the classic error and the output tells you at once.')

q(id='m2-15', module=2, topic='Escape sequences', runs=True,
  prompt='What is printed?',
  code='print("a\\tb")\nprint("c\\nd")\nprint("e\\\\f")',
  options=['a\tb\nc\nd\ne\\f', 'a\\tb\nc\\nd\ne\\\\f', 'ab\ncd\nef', 'a b\ncd\nef'],
  answer=0,
  why=['Correct. Backslash t is a tab, backslash n is a newline, and two '
       'backslashes print one literal backslash.',
       'Wrong. That is what a RAW string would print, written r"a\\tb". Without '
       'the r, the escapes are interpreted.',
       'Wrong. The escapes produce real whitespace: a tab and a line break, not '
       'nothing.',
       'Wrong. Backslash t is a tab character, which is wider than a single '
       'space, and the last line keeps its backslash.'],
  explanation='Backslash n newline, backslash t tab, double backslash for a real '
              'backslash. This matters for file paths, where a Windows path needs '
              'doubling or a raw string.')

q(id='m2-16', module=2, topic='Identity against equality', runs=True,
  prompt='What is printed?',
  code='a = [1, 2]\nb = [1, 2]\nprint(a == b)\nprint(a is b)',
  options=['True\nTrue', 'True\nFalse', 'False\nFalse', 'False\nTrue'],
  answer=1,
  why=['Wrong. is asks whether they are the SAME object, and two separately '
       'written lists are two objects however alike they look.',
       'Correct. == compares contents, so it is True. is compares identity, so it '
       'is False: a and b name two different list objects.',
       'Wrong. == on two lists compares them item by item, and these match.',
       'Wrong, and it has the two operators exactly backwards.'],
  explanation='== is equal in value, is is the very same object. Use is only for '
              'None, and use == for everything else.')

q(id='m2-17', module=2, topic='Multiple assignment', runs=True,
  prompt='What is printed?',
  code='a, b = 1, 2\na, b = b, a\nprint(a, b)',
  options=['1 2', '2 1', '2 2', '1 1'],
  answer=1,
  why=['Wrong. That is the value before the swap.',
       'Correct. The right-hand side is evaluated first, into the pair (2, 1), '
       'and only then unpacked into a and b. So the swap needs no temporary '
       'variable.',
       'Wrong. That is what happens in a language where a = b runs first and '
       'destroys the old a. Python does not: it builds the whole right side '
       'first.',
       'Wrong, for the same reason: nothing is overwritten before it is read.'],
  explanation='a, b = b, a swaps in one line because the right side is built '
              'completely before anything is assigned.')

q(id='m2-18', module=2, topic='Common errors',
  prompt='Which error does Python raise for int("abc")?',
  options=['TypeError', 'ValueError', 'SyntaxError', 'NameError'],
  answer=1,
  why=['Wrong. TypeError is for the wrong KIND of thing, such as "5" + 5. Here '
       'the kind is right, a string, and int() does accept strings.',
       'Correct. The type is acceptable but the VALUE is not: "abc" is a string '
       'that does not spell a number. That is exactly what ValueError means.',
       'Wrong. The line parses perfectly. A syntax error would mean Python could '
       'not read the line at all.',
       'Wrong. NameError means a name was used before it was assigned. Every name '
       'here exists.'],
  explanation='TypeError is the wrong type, ValueError is the right type carrying '
              'an impossible value. int("abc") is the standard example of the '
              'second.')


# ===========================================================================
# MODULE THREE: decisions, loops, lists, tuples, sets, dictionaries
# ===========================================================================
q(id='m3-01', module=3, topic='elif', runs=True,
  prompt='What is printed?',
  code='score = 75\nif score >= 70:\n    print("A")\nelif score >= 60:\n'
       '    print("B")\nelse:\n    print("C")',
  options=['A', 'B', 'A\nB', 'C'],
  answer=0,
  why=['Correct. The first condition that is true wins, its block runs, and the '
       'whole chain is then finished.',
       'Wrong. 75 is at or above 60, but the chain never reaches that test: it '
       'stopped at the first true one.',
       'Wrong. An if/elif chain runs AT MOST one block. Separate if statements '
       'would print both, which is exactly the trap the paper sets.',
       'Wrong. else runs only when every test above it failed.'],
  explanation='elif tests only if everything above it failed. Replacing elif with '
              'a second if changes the answer, and the paper has asked for '
              'exactly that comparison.')

q(id='m3-02', module=3, topic='range', runs=True,
  prompt='What is printed?',
  code='for i in range(1, 6, 2):\n    print(i, end=" ")',
  options=['1 2 3 4 5', '1 3 5', '1 3 5 7', '2 4'],
  answer=1,
  why=['Wrong. That ignores the third argument, the step of 2.',
       'Correct. range(start, stop, step) begins at 1, adds 2 each time, and '
       'stops BEFORE 6. So 1, 3, 5.',
       'Wrong. 7 is past the stop value, so it is never produced.',
       'Wrong. The start is 1, not 2. range starts where you tell it to.'],
  explanation='range(stop), range(start, stop), range(start, stop, step), and the '
              'stop is never included. That last part is the one people lose '
              'marks on.')

q(id='m3-03', module=3, topic='while with break', runs=True,
  prompt='What is printed?',
  code='n = 0\nwhile True:\n    n += 1\n    if n == 3:\n        break\nprint(n)',
  options=['0', '2', '3', 'the loop never ends'],
  answer=2,
  why=['Wrong. n is incremented before anything else in the body, so it can never '
       'still be 0 at the end.',
       'Wrong. break happens AFTER the increment that made n equal to 3, so 3 is '
       'the value that survives.',
       'Correct. n reaches 3, the if fires, break leaves the loop immediately, and '
       'print sees 3.',
       'Wrong. while True does loop forever unless something leaves it, and break '
       'is exactly that something.'],
  explanation='break leaves the loop at once; continue jumps to the next '
              'iteration. while True with a break inside is the standard way to '
              'write a menu loop.')

q(id='m3-04', module=3, topic='continue', runs=True,
  prompt='What is printed?',
  code='for i in range(5):\n    if i % 2 == 0:\n        continue\n    print(i, end=" ")',
  options=['0 2 4', '1 3', '0 1 2 3 4', '1 3 5'],
  answer=1,
  why=['Wrong, and it is backwards: continue SKIPS the even numbers, so they are '
       'the ones that never print.',
       'Correct. When i is even the continue skips the print, so only the odd '
       'values 1 and 3 appear. range(5) stops at 4.',
       'Wrong. The continue means not every value reaches the print.',
       'Wrong. range(5) produces 0 to 4, so 5 is never reached.'],
  explanation='continue abandons this pass and starts the next. Reading it as '
              '"skip the rest of the body" is the reliable way to trace it.')

q(id='m3-05', module=3, topic='else on a loop', runs=True,
  prompt='What is printed?',
  code='for i in range(3):\n    print(i, end=" ")\nelse:\n    print("done")',
  options=['0 1 2 done', '0 1 2', 'done', '0 1 2 3 done'],
  answer=0,
  why=['Correct. A loop else runs when the loop finished normally, that is '
       'without a break. Nothing breaks here, so it runs.',
       'Wrong. The else does run, because there is no break in this loop.',
       'Wrong. The loop body runs first, three times.',
       'Wrong. range(3) gives 0, 1 and 2. It never reaches 3.'],
  explanation='A loop else means "no break happened". It is Python-specific and a '
              'favourite for a "what is the output" question because it looks '
              'like an if else and is not.')

q(id='m3-06', module=3, topic='Lists are ordered and mutable', runs=True,
  prompt='What is printed?',
  code='xs = [3, 1, 2]\nxs.append(4)\nxs.sort()\nprint(xs)\nprint(xs[0], xs[-1])',
  options=['[1, 2, 3, 4]\n1 4', '[3, 1, 2, 4]\n3 4', '[4, 3, 2, 1]\n4 1',
           '[1, 2, 3]\n1 3'],
  answer=0,
  why=['Correct. append adds to the end, sort orders the list IN PLACE, and the '
       'first and last items are then 1 and 4.',
       'Wrong. sort() really does reorder the list. It changes it and returns '
       'None.',
       'Wrong. sort() ascends by default. Descending needs reverse=True.',
       'Wrong. The 4 that append added is still there. append modifies the list '
       'itself.'],
  explanation='Lists are ORDERED, so position has meaning, and MUTABLE, so they '
              'can be changed in place. The paper asks for both properties by '
              'name.')

q(id='m3-07', module=3, topic='sort returns None', runs=True,
  prompt='What is printed?',
  code='xs = [3, 1, 2]\nys = xs.sort()\nprint(ys)',
  options=['[1, 2, 3]', 'None', '[3, 1, 2]', 'TypeError'],
  answer=1,
  why=['Wrong, and this is the trap. sort() changes xs and hands back nothing, so '
       'the sorted list is in xs, not in ys.',
       'Correct. sort() returns None. If you want a new sorted list without '
       'touching the original, use sorted(xs).',
       'Wrong. xs itself IS sorted now; it is ys that is empty of meaning.',
       'Wrong. Nothing raises here. It runs and quietly gives you None, which is '
       'what makes the bug hard to see.'],
  explanation='Methods that change a list in place return None: sort, append, '
              'reverse, extend. The functions that return a NEW value are '
              'sorted() and reversed().')

q(id='m3-08', module=3, topic='List slicing', runs=True,
  prompt='What is printed?',
  code='numbers = [1, 2, 3, 4, 5]\nprint(numbers[-3:])\nprint(numbers[:2])\n'
       'print(numbers[-3:] * 2)',
  options=['[3, 4, 5]\n[1, 2]\n[3, 4, 5, 3, 4, 5]',
           '[2, 3, 4]\n[1, 2]\n[6, 8, 10]',
           '[3, 4, 5]\n[1, 2, 3]\n[6, 8, 10]',
           '[3, 4, 5]\n[1, 2]\n[6, 8, 10]'],
  answer=0,
  why=['Correct. Minus 3 to the end is the last three items. Up to 2 stops before '
       'index 2, so two items. A list times 2 REPEATS the list, it does not '
       'multiply the numbers in it.',
       'Wrong. numbers[-3:] counts three back from the end, giving 3, 4 and 5.',
       'Wrong. numbers[:2] excludes index 2, so it is two items, not three.',
       'Wrong on the last line. Star on a list repeats the list; to multiply each '
       'number you would need a loop or a comprehension.'],
  explanation='This exact shape, numbers[-3:] * 2, is on a past paper. A slice '
              'excludes its stop, and star repeats rather than scales.')

q(id='m3-09', module=3, topic='Nested indexing', runs=True,
  prompt='What is printed?',
  code='m = [[1, 2], [3, 4, 5], [6]]\nprint(m[1][2])\nprint(len(m))',
  options=['5\n3', '4\n3', '5\n6', '3\n3'],
  answer=0,
  why=['Correct. m[1] is the middle list, [3, 4, 5], and its index 2 is 5. len(m) '
       'counts the OUTER items, of which there are three.',
       'Wrong. Index 2 of [3, 4, 5] is 5. Index 1 would be 4.',
       'Wrong. len() of a nested list counts the sublists, not the numbers inside '
       'them.',
       'Wrong. m[1][2] reaches into the second list and takes its third item.'],
  explanation='Read a nested index left to right: first pick the sublist, then '
              'index into it. The paper prints a three-deep version of this, so '
              'do it one bracket at a time on paper.')

q(id='m3-10', module=3, topic='Tuples are immutable',
  prompt='Which statement about tuples is TRUE?',
  options=['A tuple can be changed after creation, like a list',
           'A tuple is ordered and immutable, and can be used as a dictionary key',
           'A tuple cannot contain more than two items',
           'A tuple is written with square brackets'],
  answer=1,
  why=['Wrong. That is a list. Assigning to t[0] on a tuple raises TypeError.',
       'Correct. Ordered like a list, immutable unlike one, and because it cannot '
       'change it can be hashed, so it may be a dictionary key where a list may '
       'not.',
       'Wrong. The name comes from the general mathematical term, not from two. A '
       'tuple can hold any number of items, including none.',
       'Wrong. Round brackets, or in fact just commas: 1, 2 is already a tuple. '
       'Square brackets make a list.'],
  explanation='List against tuple is a guaranteed question. Ordered both, mutable '
              'only the list, and only the tuple can be a dictionary key.')

q(id='m3-11', module=3, topic='Sets are unique and unordered', runs=True,
  prompt='What is printed?',
  code='s = {3, 1, 2, 3, 1}\nprint(len(s))\nprint(sorted(s))',
  options=['5\n[1, 1, 2, 3, 3]', '3\n[1, 2, 3]', '3\n[3, 1, 2]', '5\n[1, 2, 3]'],
  answer=1,
  why=['Wrong. A set discards duplicates the moment it is built, so it never held '
       'five items.',
       'Correct. The duplicates collapse, leaving three items, and sorted() puts '
       'them in order for printing, which is how you show a set reliably.',
       'Wrong. sorted() returns an ordered LIST, so it prints in ascending order '
       'whatever order the set happened to be in.',
       'Wrong. len() of that set is 3, not 5, because uniqueness is enforced.'],
  explanation='Sets are unique and unordered. That is why the manual compares set '
              'answers as sets, never by printed order: Python randomises string '
              'hashing per run.')

q(id='m3-12', module=3, topic='Set operations', runs=True,
  prompt='What is printed?',
  code='a = {1, 2, 3, 4}\nb = {3, 4, 5}\nprint(sorted(a & b))\nprint(sorted(a | b))\n'
       'print(sorted(a - b))',
  options=['[3, 4]\n[1, 2, 3, 4, 5]\n[1, 2]',
           '[1, 2]\n[1, 2, 3, 4, 5]\n[3, 4]',
           '[3, 4]\n[1, 2, 5]\n[1, 2]',
           '[3, 4]\n[1, 2, 3, 3, 4, 4, 5]\n[1, 2]'],
  answer=0,
  why=['Correct. The ampersand is intersection, what is in both. The bar is '
       'union, everything once. The minus is difference, what is in a and not in '
       'b.',
       'Wrong, and it has intersection and difference swapped.',
       'Wrong. Union is EVERYTHING from both, not only the items unique to one.',
       'Wrong. A union is still a set, so nothing appears twice in it.'],
  explanation='Ampersand intersection, bar union, minus difference, caret '
              'symmetric difference. The named methods are intersection(), '
              'union(), difference() and they mean the same thing.')

q(id='m3-13', module=3, topic='Dictionary basics', runs=True,
  prompt='What is printed?',
  code='d = {"a": 1, "b": 2}\nd["c"] = 3\nd["a"] = 9\nprint(d)\nprint(len(d))',
  options=["{'a': 9, 'b': 2, 'c': 3}\n3", "{'a': 1, 'b': 2, 'c': 3}\n3",
           "{'a': 9, 'b': 2, 'c': 3}\n4", "{'a': 1, 'a': 9, 'b': 2, 'c': 3}\n4"],
  answer=0,
  why=['Correct. Assigning to a key that does not exist ADDS it; assigning to one '
       'that does REPLACES its value. Three keys remain.',
       'Wrong. d["a"] = 9 really does overwrite the 1.',
       'Wrong. There are three keys, not four. Overwriting a key does not add '
       'one.',
       'Wrong. A dictionary cannot hold the same key twice. That is what makes it '
       'a mapping.'],
  explanation='Keys are unique; assigning to an existing key replaces its value. '
              'Since Python 3.7 a dictionary also keeps insertion order, which is '
              'why the printed order is predictable.')

q(id='m3-14', module=3, topic='KeyError', runs=True,
  prompt='What is printed?',
  code='months = {"Jan": 1, "Feb": 2}\ntry:\n    print(months[2])\nexcept KeyError as e:\n'
       '    print("KeyError", e)',
  options=['2', 'KeyError 2', 'Feb', 'None'],
  answer=1,
  why=['Wrong. Looking up 2 asks for a KEY equal to 2, and there is no such key. '
       'The values are 1 and 2, but you cannot look a dictionary up by its value.',
       'Correct. The subscript is a KEY lookup, the key 2 is absent, KeyError is '
       'raised and caught, and the missing key is what the exception carries.',
       'Wrong. Nothing here searches the values to find the key that maps to 2. '
       'That would need a loop or a reversed dictionary.',
       'Wrong. A missing key raises rather than returning None. It is get() that '
       'returns None instead of raising.'],
  explanation='months[2] asks for the KEY 2. Use months.get(2) to get None '
              'instead of a KeyError. This exact confusion is on a past paper.')

q(id='m3-15', module=3, topic='Dictionary iteration', runs=True,
  prompt='What is printed?',
  code='d = {"x": 1, "y": 2}\nfor k in d:\n    print(k, end=" ")\nprint()\n'
       'for k, v in d.items():\n    print(k, v, end=" ")',
  options=['x y \nx 1 y 2 ', '1 2 \nx 1 y 2 ', "('x', 1) ('y', 2) \nx 1 y 2 ",
           'x y \n1 2 '],
  answer=0,
  why=['Correct. Iterating a dictionary directly gives its KEYS. items() gives '
       'key and value pairs, which unpack into the two loop variables.',
       'Wrong. The plain loop gives keys, not values. For values you would write '
       'd.values().',
       'Wrong. The plain loop yields keys alone, not pairs. Pairs come from '
       'items().',
       'Wrong on the second line: items() gives both parts, and both are printed.'],
  explanation='for k in d gives keys. d.keys(), d.values(), d.items() give what '
              'they say. Forgetting items() and then trying to unpack a key is a '
              'common exam slip.')

q(id='m3-16', module=3, topic='Mutable default trap', runs=True,
  prompt='What is printed?',
  code='a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)',
  options=['[1, 2, 3]', '[1, 2, 3, 4]', '[4]', '[[1, 2, 3], 4]'],
  answer=1,
  why=['Wrong. b = a does not copy anything. It gives the same list a second '
       'name, so a change through one name is visible through the other.',
       'Correct. There is only ONE list here with two names, so appending through '
       'b shows up in a.',
       'Wrong. append adds to the existing contents; it does not replace them.',
       'Wrong. append adds an item to the list, it does not nest the old list '
       'inside a new one.'],
  explanation='Assignment binds a name, it does not copy. To copy, use a[:] or '
              'list(a) or a.copy(). This is the most expensive misunderstanding '
              'in the whole course.')

q(id='m3-17', module=3, topic='in operator', runs=True,
  prompt='What is printed?',
  code='print("a" in "cat")\nprint(2 in [1, 2, 3])\nprint("x" in {"x": 1})',
  options=['True\nTrue\nTrue', 'True\nTrue\nFalse', 'False\nTrue\nTrue',
           'True\nFalse\nTrue'],
  answer=0,
  why=['Correct. On a string, in tests for a substring. On a list, for an item. '
       'On a dictionary, for a KEY.',
       'Wrong on the third line. in on a dictionary searches the keys, and "x" is '
       'a key here.',
       'Wrong on the first line. "a" is one of the characters of "cat", so it is '
       'found.',
       'Wrong on the second line. 2 is an item of that list.'],
  explanation='in means substring on a string, membership on a list or set, and '
              'KEY membership on a dictionary. That last one is the trap.')

q(id='m3-18', module=3, topic='del', runs=True,
  prompt='What is printed?',
  code='xs = [10, 20, 30, 40]\ndel xs[1]\nprint(xs)\nd = {"a": 1, "b": 2}\n'
       'del d["a"]\nprint(d)',
  options=["[10, 30, 40]\n{'b': 2}", "[20, 30, 40]\n{'b': 2}",
           "[10, 20, 30]\n{'a': 1}", "[10, 30, 40]\n{'a': 1}"],
  answer=0,
  why=['Correct. del removes by POSITION on a list, so index 1 (the 20) goes, and '
       'by KEY on a dictionary.',
       'Wrong. Index 1 is the second item. Index 0 is the 10.',
       'Wrong. del xs[1] takes out the second item, not the last, and del d["a"] '
       'takes out the "a" entry.',
       'Wrong on the dictionary: del d["a"] removes the key it names.'],
  explanation='del removes by index on a list and by key on a dictionary. '
              'remove() removes by VALUE on a list, and pop() removes and gives '
              'the item back.')


# ===========================================================================
# MODULE FOUR: functions, modules, files, exceptions
# ===========================================================================
q(id='m4-01', module=4, topic='Defining a function', runs=True,
  prompt='What is printed?',
  code='def add(a, b=10):\n    return a + b\n\nprint(add(5))\nprint(add(5, 1))\n'
       'print(add(b=2, a=3))',
  options=['15\n6\n5', '15\n6\n6', '5\n6\n5', 'TypeError\n6\n5'],
  answer=0,
  why=['Correct. The default fills in for b when only one argument is given. '
       'Positional arguments fill left to right. Keyword arguments may be given '
       'in any order because they name their parameter.',
       'Wrong on the last line: 3 + 2 is 5, not 6.',
       'Wrong on the first line. b defaults to 10, so add(5) is 15.',
       'Wrong. add(5) is legal precisely BECAUSE b has a default.'],
  explanation='A parameter with a default may be omitted. Keyword arguments name '
              'their target, so order stops mattering. Defaults must come after '
              'non-defaults in the definition.')

q(id='m4-02', module=4, topic='return against print', runs=True,
  prompt='What is printed?',
  code='def f(x):\n    print(x * 2)\n\ndef g(x):\n    return x * 2\n\n'
       'a = f(3)\nb = g(3)\nprint(a, b)',
  options=['6\nNone 6', '6\n6 6', '6 6\nNone 6', 'None 6'],
  answer=0,
  why=['Correct. f prints 6 and returns nothing, so a is None. g returns 6 '
       'silently, so b is 6. The last line then prints None 6.',
       'Wrong. a is None. A function with no return statement gives back None.',
       'Wrong. f prints once, when it is called; the value it gives back is still '
       'None.',
       'Wrong. The 6 printed inside f appears first, on its own line.'],
  explanation='print SHOWS a value, return HANDS IT BACK. A function that only '
              'prints returns None, and using that None later is a standard '
              'exam bug.')

q(id='m4-03', module=4, topic='Scope', runs=True,
  prompt='What is printed?',
  code='x = 1\n\ndef f():\n    x = 2\n    print(x)\n\nf()\nprint(x)',
  options=['2\n1', '2\n2', '1\n1', '1\n2'],
  answer=0,
  why=['Correct. The assignment inside f creates a LOCAL x. The global x is '
       'untouched, so it is still 1 afterwards.',
       'Wrong. Assigning inside a function does not change the global unless the '
       'function declares global x.',
       'Wrong. Inside f, the local x shadows the global one, so 2 prints first.',
       'Wrong, and it has the two the wrong way round.'],
  explanation='Assigning to a name inside a function makes it local. To change a '
              'global you must say global x, and this pair of prints is exactly '
              'how the paper tests it.')

q(id='m4-04', module=4, topic='Why modularise',
  prompt='Which of these is NOT a benefit of breaking a program into functions?',
  options=['The same code can be reused instead of repeated',
           'The program runs measurably faster because it is shorter',
           'Each piece can be tested on its own',
           'The program is easier to read and to maintain'],
  answer=1,
  why=['Wrong choice, because reuse IS a benefit, and usually the first one '
       'listed.',
       'Correct. Calling a function costs a little time rather than saving it. '
       'The benefits of modularising are all about the PROGRAMMER: reuse, '
       'testing, readability, maintainability, teamwork. Speed is not among '
       'them.',
       'Wrong choice, because testing a piece in isolation IS a benefit.',
       'Wrong choice, because readability and maintenance ARE benefits, and the '
       'paper lists them.'],
  explanation='Every benefit of modularising is a benefit to the person reading '
              'or changing the code. Speed is not one, and a question offering it '
              'is offering the distractor.')

q(id='m4-05', module=4, topic='Importing', runs=True,
  prompt='What is printed?',
  code='import math\nfrom math import sqrt\nprint(math.sqrt(16), sqrt(16))',
  options=['4.0 4.0', '4 4', '4.0 4', 'NameError'],
  answer=0,
  why=['Correct. Both forms reach the same function. sqrt always returns a float, '
       'so both print 4.0.',
       'Wrong. math.sqrt returns a float even for a perfect square, so the point '
       'and zero are printed.',
       'Wrong. Both calls are the same function and give the same value.',
       'Wrong. Both imports are valid, and each makes its name available in its '
       'own way.'],
  explanation='import math needs the math. prefix; from math import sqrt puts the '
              'name in directly. Both are examinable and the difference is which '
              'name you must then write.')

q(id='m4-06', module=4, topic='File modes',
  prompt='A file is opened with open("data.txt", "w") when data.txt already '
         'exists and contains text. What happens?',
  options=['The new text is added after the existing text',
           'The existing contents are erased',
           'Python raises FileExistsError',
           'The file is opened read-only'],
  answer=1,
  why=['Wrong, and this is the mode people mean when they choose "w" by mistake. '
       'Appending is "a".',
       'Correct. "w" truncates the file to nothing the moment it is opened, '
       'before you write a single character. Data is lost even if the program '
       'then crashes.',
       'Wrong. "w" is perfectly happy for the file to exist. It just empties it. '
       'The mode that refuses to overwrite is "x".',
       'Wrong. "w" is write-only. Reading is "r", which is also the default.'],
  explanation='"r" read, "w" write and TRUNCATE, "a" append, "x" create only if '
              'absent. Choosing "w" where you meant "a" destroys the file, and '
              'the paper asks about this.')

q(id='m4-07', module=4, topic='with',
  prompt='Why is with open(...) as f preferred to f = open(...)?',
  options=['It is faster to type',
           'It closes the file automatically, even if an error is raised inside '
           'the block',
           'It is the only way to read a file line by line',
           'It opens the file in a special faster mode'],
  answer=1,
  why=['Wrong. Brevity is not the reason, and it is barely shorter anyway.',
       'Correct. The with block guarantees f.close() runs on the way out, whether '
       'the block finished normally or raised. Without it, an exception can leave '
       'the file open and its buffer unwritten.',
       'Wrong. A plain open() can be iterated line by line just as well. The '
       'difference is only about closing.',
       'Wrong. The mode is whatever you pass to open. with changes nothing about '
       'how the file is opened.'],
  explanation='with guarantees the close. It is the same guarantee finally gives, '
              'written more briefly, and saying that in the exam earns the mark.')

q(id='m4-08', module=4, topic='Reading a file',
  prompt='A text file holds three lines. Which call gives a LIST of those three '
         'lines?',
  options=['f.read()', 'f.readline()', 'f.readlines()', 'f.line()'],
  answer=2,
  why=['Wrong. read() gives the WHOLE file as one string, newlines and all.',
       'Wrong. readline() gives ONE line, the next one, as a string.',
       'Correct. readlines() gives a list with one string per line, each still '
       'carrying its trailing newline unless you strip it.',
       'Wrong. There is no such method.'],
  explanation='read whole, readline one, readlines list. Note the newline stays '
              'on each item, so print() of one adds a blank line unless you '
              'strip.')

q(id='m4-09', module=4, topic='try and except', runs=True,
  prompt='What is printed?',
  code='try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print("caught")\n'
       'finally:\n    print("always")',
  options=['caught\nalways', 'always', 'caught', 'the program crashes'],
  answer=0,
  why=['Correct. The division raises, the matching except handles it, and finally '
       'runs afterwards as it always does.',
       'Wrong. The except block ran too, and its print came first.',
       'Wrong. finally runs whether or not anything was raised. That is its whole '
       'point.',
       'Wrong. The exception was caught, so nothing propagates and nothing '
       'crashes.'],
  explanation='try, except by exception type, else if nothing was raised, finally '
              'always. finally is where you put the cleanup that must happen '
              'either way.')

q(id='m4-10', module=4, topic='Exception types', runs=True,
  prompt='Which exception does this raise?',
  code='xs = [1, 2, 3]\nprint(xs[5])',
  options=['KeyError', 'IndexError', 'ValueError', 'TypeError'],
  answer=1,
  why=['Wrong. KeyError is for a missing DICTIONARY key. A list is indexed by '
       'position, not by key.',
       'Correct. The index is outside the range of the list, which is exactly '
       'what IndexError means.',
       'Wrong. ValueError is for a value of the right type that cannot be used, '
       'such as int("abc").',
       'Wrong. TypeError would be xs["a"], where the index is the wrong KIND of '
       'thing entirely.'],
  explanation='IndexError for a sequence, KeyError for a mapping. Naming the '
              'right exception is worth marks on its own in this paper.')

q(id='m4-11', module=4, topic='Bare except',
  prompt='Why is except: on its own considered bad practice?',
  options=['It is slower than naming the exception',
           'It catches everything, including errors you did not anticipate, and '
           'hides real bugs',
           'It is not valid Python',
           'It can only be used once per program'],
  answer=1,
  why=['Wrong. Speed is not the issue and the difference is immeasurable.',
       'Correct. A bare except swallows every exception, including a typo raising '
       'NameError, so the program keeps going in a broken state and the real '
       'fault is invisible.',
       'Wrong. It is valid, which is exactly why it is dangerous.',
       'Wrong. There is no such limit.'],
  explanation='Catch the exception you expect and no more. A bare except turns a '
              'loud failure into a silent wrong answer.')

q(id='m4-12', module=4, topic='raise', runs=True,
  prompt='What is printed?',
  code='def check(age):\n    if age < 0:\n        raise ValueError("negative age")\n'
       '    return age\n\ntry:\n    check(-1)\nexcept ValueError as e:\n    print(e)',
  options=['negative age', 'ValueError', '-1', 'nothing is printed'],
  answer=0,
  why=['Correct. raise creates the exception with that message, the except '
       'catches it and binds it to e, and printing an exception prints its '
       'message.',
       'Wrong. Printing the exception object shows its MESSAGE, not the name of '
       'its class. For the class name you would print type(e).__name__.',
       'Wrong. The argument is never returned, because the raise happens first.',
       'Wrong. The except block does run and does print.'],
  explanation='raise makes your own error, and validating input this way is what '
              'the paper means by defensive programming.')

q(id='m4-13', module=4, topic='Docstrings',
  prompt='What is a docstring?',
  options=['A comment starting with a hash inside a function',
           'A string literal as the first statement of a function, module or '
           'class, describing what it does',
           'A special variable holding the function name',
           'A file that documents the whole program'],
  answer=1,
  why=['Wrong. A hash comment is stripped and cannot be read back at run time. A '
       'docstring survives into the object.',
       'Correct. It sits directly under the def line, usually in triple quotes, '
       'and becomes the object\'s __doc__, which is what help() shows you.',
       'Wrong. That is __name__, a different attribute entirely.',
       'Wrong. A docstring lives inside the code, not beside it.'],
  explanation='First statement, a string, becomes __doc__. It is the '
              '"self-documenting" part of the modularisation answer.')

q(id='m4-14', module=4, topic='Recursion', runs=True,
  prompt='What is printed?',
  code='def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n - 1)\n\n'
       'print(fact(5))',
  options=['15', '120', '5', 'RecursionError'],
  answer=1,
  why=['Wrong. 15 is 1+2+3+4+5, the SUM. This function multiplies.',
       'Correct. 5 * 4 * 3 * 2 * 1 is 120. The base case at n <= 1 stops the '
       'recursion.',
       'Wrong. The function does not simply return its argument; it multiplies '
       'down to the base case.',
       'Wrong. There IS a base case, so the recursion terminates. Without one, '
       'RecursionError would be right.'],
  explanation='Every recursion needs a base case and a step that moves towards '
              'it. Missing the base case gives RecursionError, and the paper has '
              'asked for exactly that fault to be identified.')


# ===========================================================================
# MODULE FIVE: databases and GUI
# ===========================================================================
q(id='m5-01', module=5, topic='sqlite3 workflow',
  prompt='What is the correct order for working with a database in Python?',
  options=['connect, cursor, execute, commit, close',
           'cursor, connect, commit, execute, close',
           'connect, execute, cursor, close, commit',
           'open, read, write, close'],
  answer=0,
  why=['Correct. Connect to the database, get a cursor from the connection, '
       'execute SQL through the cursor, commit so the change is saved, then close '
       'the connection.',
       'Wrong. A cursor is obtained FROM a connection, so the connection must '
       'exist first.',
       'Wrong. You cannot execute before you have a cursor, and committing after '
       'closing is too late.',
       'Wrong. That is the file-handling pattern, not the database one.'],
  explanation='connect, cursor, execute, commit, close. Forget the commit and the '
              'rows vanish when the program ends, which is the classic lost mark.')

q(id='m5-02', module=5, topic='Why commit',
  prompt='A program inserts three rows and then closes the connection without '
         'calling commit. What is in the table?',
  options=['All three rows', 'The first row only', 'No rows', 'An error is raised'],
  answer=2,
  why=['Wrong. Uncommitted work is not saved. It lived only in the transaction.',
       'Wrong. There is nothing special about the first row; all three are in the '
       'same uncommitted transaction.',
       'Correct. Without a commit the transaction is rolled back when the '
       'connection closes, so the table is unchanged.',
       'Wrong. Nothing raises. The program appears to work, which is what makes '
       'this bug expensive.'],
  explanation='Commit is what makes a change permanent. No commit, no data, and '
              'no error message to tell you.')

q(id='m5-03', module=5, topic='SQL SELECT',
  prompt='Which SQL statement retrieves only the students whose score is above 50?',
  options=['SELECT * FROM students WHERE score > 50',
           'SELECT * FROM students IF score > 50',
           'GET * FROM students WHERE score > 50',
           'SELECT students WHERE score > 50'],
  answer=0,
  why=['Correct. SELECT names the columns, FROM names the table, WHERE filters '
       'the rows.',
       'Wrong. SQL filters with WHERE. IF is not part of a SELECT statement.',
       'Wrong. There is no GET in SQL. Retrieval is SELECT.',
       'Wrong. The table must be named after FROM, and the columns before it.'],
  explanation='SELECT columns FROM table WHERE condition. That one line is most '
              'of what this course asks of SQL.')

q(id='m5-04', module=5, topic='Placeholders',
  prompt='Why is cur.execute("INSERT INTO t VALUES (?, ?)", (a, b)) preferred to '
         'building the SQL string with the values in it?',
  options=['It runs faster on small tables',
           'It keeps the values separate from the SQL, so a value cannot be read '
           'as SQL',
           'It is the only form sqlite3 accepts',
           'It commits automatically'],
  answer=1,
  why=['Wrong. Speed is not the reason, though prepared statements can help on '
       'repeated inserts.',
       'Correct. The placeholder keeps data as data. Pasting a value into the '
       'text of a statement lets a value containing a quote change the statement, '
       'which is SQL injection.',
       'Wrong. String building is accepted. It is accepted and unsafe, which is '
       'the point.',
       'Wrong. You still have to commit yourself.'],
  explanation='The question mark placeholder separates data from code. It is the '
              'standard answer to "how do you prevent SQL injection".')

q(id='m5-05', module=5, topic='executemany',
  prompt='What does cur.executemany() do that execute() does not?',
  options=['It runs several DIFFERENT statements in one call',
           'It runs the same statement once for each item in a sequence of '
           'parameter tuples',
           'It commits after every row',
           'It returns all the rows of a table'],
  answer=1,
  why=['Wrong. The statement is the same every time. Only the parameters change.',
       'Correct. You give it one statement and a list of parameter tuples, and it '
       'runs the statement once per tuple, which is how a batch insert is done.',
       'Wrong. It does not commit at all. You still call commit yourself.',
       'Wrong. Retrieving rows is fetchall(), after a SELECT.'],
  explanation='One statement, many parameter sets. It is the tidy way to insert a '
              'list of records and this manual teaches it because the paper '
              'reached for it.')

q(id='m5-06', module=5, topic='fetchone and fetchall',
  prompt='After executing a SELECT that matches five rows, what does fetchone() '
         'return?',
  options=['All five rows as a list', 'The first row, as a tuple',
           'The number 5', 'None'],
  answer=1,
  why=['Wrong. That is fetchall(). fetchone gets one.',
       'Correct. fetchone() hands back the next row as a tuple, and returns None '
       'once the rows run out.',
       'Wrong. Counting rows is done in SQL, with COUNT(*).',
       'Wrong. None comes back only when there are no rows left, and here there '
       'are five.'],
  explanation='fetchone next row or None, fetchall the rest as a list of tuples. '
              'A row is a tuple, so index it by position.')

q(id='m5-07', module=5, topic='SQL aggregate functions',
  prompt='Which SQL function returns the number of rows matching a query?',
  options=['SUM()', 'COUNT()', 'TOTAL()', 'LEN()'],
  answer=1,
  why=['Wrong. SUM() adds up the values in a column. It answers how much, not how '
       'many.',
       'Correct. COUNT(*) counts rows; COUNT(column) counts the rows where that '
       'column is not null.',
       'Wrong. There is no standard TOTAL() in this course.',
       'Wrong. LEN() is not SQL. Python has len(); SQL has COUNT().'],
  explanation='COUNT how many, SUM the total, AVG the mean, MAX and MIN the '
              'extremes. The paper has asked for all five.')

q(id='m5-08', module=5, topic='UPDATE and DELETE',
  prompt='What does UPDATE students SET score = 0 do, with no WHERE clause?',
  options=['Nothing: a WHERE clause is required',
           'It sets score to 0 for EVERY row in the table',
           'It sets score to 0 for the first row only',
           'It deletes the score column'],
  answer=1,
  why=['Wrong. WHERE is optional, and that is precisely the danger.',
       'Correct. With no WHERE, the statement applies to the whole table. The '
       'same is true of DELETE FROM students, which empties it.',
       'Wrong. SQL is set-based: it acts on every row that matches, and with no '
       'WHERE every row matches.',
       'Wrong. Removing a column is ALTER TABLE. UPDATE changes values.'],
  explanation='No WHERE means every row. Write the WHERE first and the SET '
              'second if that helps you never forget it.')

q(id='m5-09', module=5, topic='tkinter basics',
  prompt='In tkinter, what does the mainloop() call do?',
  options=['It draws the window once and returns',
           'It starts the event loop, which waits for and dispatches user actions',
           'It creates the main window object',
           'It closes the application'],
  answer=1,
  why=['Wrong. Drawing once and returning would make the window appear and vanish '
       'immediately, which is exactly what happens if you forget mainloop.',
       'Correct. mainloop() keeps the program running, watching for clicks and '
       'keystrokes and calling the handlers bound to them, until the window is '
       'closed.',
       'Wrong. Creating the window is Tk(). mainloop is what makes it live.',
       'Wrong. It is what keeps the application OPEN.'],
  explanation='Tk() makes the window, widgets are created and placed, mainloop() '
              'runs the event loop. Without the last one nothing stays on '
              'screen.')

q(id='m5-10', module=5, topic='tkinter widgets',
  prompt='Which tkinter widget is used to collect a single line of typed text?',
  options=['Label', 'Entry', 'Button', 'Canvas'],
  answer=1,
  why=['Wrong. A Label DISPLAYS text. The user cannot type into it.',
       'Correct. Entry is the one-line text box, and its get() method reads what '
       'was typed.',
       'Wrong. A Button is clicked; it does not accept typing.',
       'Wrong. A Canvas is a drawing surface for shapes and images.'],
  explanation='Label shows, Entry takes one line, Text takes many, Button acts. '
              'Read what was typed with entry.get().')

q(id='m5-11', module=5, topic='Event handling',
  prompt='In Button(root, text="Go", command=run), when is run called?',
  options=['Immediately, as the button is created',
           'When the button is clicked',
           'When mainloop() starts', 'Never, unless bind() is also used'],
  answer=1,
  why=['Wrong, and this is the trap. It WOULD be immediate if you wrote '
       'command=run(), with brackets: that calls the function and hands its '
       'return value to command.',
       'Correct. command is given the function ITSELF, without brackets, and '
       'tkinter calls it later, each time the button is pressed.',
       'Wrong. mainloop starts the waiting; it does not fire the handlers by '
       'itself.',
       'Wrong. command= is a complete way to attach a handler to a button. bind() '
       'is for other events.'],
  explanation='Pass the function, not a call to it. command=run attaches it; '
              'command=run() runs it once immediately and attaches its result.')

q(id='m5-12', module=5, topic='Geometry managers',
  prompt='Which of these is NOT a tkinter geometry manager?',
  options=['pack', 'grid', 'place', 'align'],
  answer=3,
  why=['Wrong choice, because pack IS one: it stacks widgets in the space '
       'available.',
       'Wrong choice, because grid IS one: it places widgets by row and column.',
       'Wrong choice, because place IS one: it positions by exact coordinates.',
       'Correct. There is no align manager. The three are pack, grid and place, '
       'and you should not mix pack and grid in the same container.'],
  explanation='pack, grid, place. Three of them, and mixing pack with grid in one '
              'container makes the window hang while they argue.')
