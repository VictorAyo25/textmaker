"""
Extra objective questions for CSC241, one set per crash-course lesson, with
every program RUN before it is written out.

    python scripts/author/csc241_lessons.py

Writes data/csc241/drill02.json. Run BY HAND; the web build never runs Python.

Why a generator and not hand-typed JSON: a "what does this print" question is
only as good as its key, and the key must be what Python actually prints, not
what the author expects. Every question that carries a program is executed in a
fresh temporary directory (so the file lessons really write files and the
database lessons really build a table), and the build STOPS if:

  - the correct option is not exactly the program's output;
  - any wrong option is also exactly the program's output;
  - a question that says the program raises an exception raises a different
    one, or none.

The correct option is written first in each spec, which keeps authoring
honest, and is then moved to a position fixed by a hash of the question id,
so the key is spread across A to D and a reader cannot learn a position.
Questions are plain text, as the drill renders them; a listing goes in `code`.
"""
import json
import os
import random
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "data" / "csc241" / "drill02.json"

# lesson number -> drill topic, as the crash course files them
TOPIC = {"1.1": 1, "1.2": 2, "1.3": 2, "1.4": 2, "1.5": 2,
         "2.1": 3, "2.2": 3, "2.3": 3, "2.4": 3,
         "3.1": 4, "3.2": 4, "3.3": 4, "3.4": 4, "3.5": 5, "3.6": 5}

QUESTIONS = []
_count = {}


def C(src):
    return textwrap.dedent(src).strip("\n")


def Q(lesson, topic, prompt, opts, why, exp, *, code=None, check=None, style="mcq",
      key=None, diff="medium", facets=None, run=None, before=None):
    """One mcq or multi. opts[0] is correct (multi: opts[:len(key)] are).

    check: "out" means opts[0] must be exactly what the program prints;
    "err:Name" means it must raise Name. before: with an error, what the
    program must have printed before it stopped."""
    _count[lesson] = _count.get(lesson, 0) + 1
    qid = f"csc-l{lesson.replace('.', '')}-{_count[lesson]:02d}"
    QUESTIONS.append(dict(id=qid, lesson=lesson, topic=topic, prompt=prompt, opts=opts,
                          why=why, exp=exp, code=code, check=check, style=style,
                          nkey=len(key) if key else 1, diff=diff, facets=facets, run=run,
                          before=before))


def TF(lesson, topic, prompt, answer, why_true, why_false, exp, *, code=None, check=None,
       diff="easy", facets=None):
    _count[lesson] = _count.get(lesson, 0) + 1
    qid = f"csc-l{lesson.replace('.', '')}-{_count[lesson]:02d}"
    QUESTIONS.append(dict(id=qid, lesson=lesson, topic=topic, prompt=prompt, style="tf",
                          answer=answer, why={"true": why_true, "false": why_false},
                          exp=exp, code=code, check=check, diff=diff, facets=facets))


# ============================================================ Lesson 1.1
L = "1.1"
Q(L, "running order", "What does this print?",
  ["4\n12", "4\n30", "12\n4", "4\n10"],
  ["Correct. y is worked out as 4 * 3 = 12 when that line runs; changing x later does not go back and change y.",
   "Wrong. y was calculated when x was 4. Reassigning x afterwards does not recalculate y.",
   "Wrong. Lines run top to bottom, so x is printed before y.",
   "Wrong. The second print shows y, not the new x."],
  "Python runs one line at a time, top to bottom, and each line uses the values that exist at that moment. y became 12 on line 2 and stays 12.",
  code=C("""
      x = 4
      y = x * 3
      print(x)
      x = 10
      print(y)
  """), check="out", diff="medium", facets=["numbers", "lists"])
Q(L, "print", "What does this print?",
  ["A B\nAB", "AB\nAB", "A B\nA B", "A,B\nAB"],
  ["Correct. A comma in print puts one space between the items; + joins two strings with nothing between.",
   "Wrong. The comma form adds a space between the two items.",
   "Wrong. + joins the strings end to end with no space.",
   "Wrong. The comma separates the arguments; it is not printed."],
  "print('A', 'B') prints its items separated by a single space. 'A' + 'B' is one string, AB, before print ever sees it.",
  code=C("""
      print("A", "B")
      print("A" + "B")
  """), check="out", diff="easy", facets=["numbers"])
Q(L, "indentation", "What does this print?",
  ["done", "hot\nstay inside\ndone", "stay inside\ndone", "hot\ndone"],
  ["Correct. t > 20 is False, so both indented lines are skipped; print('done') is back at the margin and always runs.",
   "Wrong. The indented lines only run when the condition is True, and 15 > 20 is False.",
   "Wrong. Both indented lines belong to the if, so they are skipped together.",
   "Wrong. Neither indented line runs; they belong to the same block."],
  "Indentation decides which lines belong to the if. The two indented prints are the block; the unindented print is outside it.",
  code=C("""
      t = 15
      if t > 20:
          print("hot")
          print("stay inside")
      print("done")
  """), check="out", diff="easy", facets=["lists"])
Q(L, "errors while running", "The variable name on line 3 is misspelt. What happens when this runs?",
  ["start is printed, then a NameError stops the program", "Nothing is printed; the NameError is found before anything runs",
   "start and end are both printed, with a warning", "start is printed, then end, and the misspelt line is skipped"],
  ["Correct. Python runs line by line: line 1 prints, line 3 raises NameError, and the program stops before line 4.",
   "Wrong. A misspelt NAME is only discovered when that line runs, so line 1 has already printed.",
   "Wrong. An unhandled error stops the program; line 4 never runs.",
   "Wrong. Python does not skip a failing line; it stops there."],
  "Python interprets as it goes, so everything before the faulty line runs normally. A name error is found only when the line using the name is reached.",
  code=C("""
      print("start")
      total = 5
      print(totl)
      print("end")
  """), check="err:NameError", before="start", diff="medium", facets=["wording"])
Q(L, "what Python is", "What does it mean that Python is INTERPRETED?",
  ["An interpreter reads and carries out the code line by line, rather than translating the whole program into machine code first",
   "The whole program must be compiled into machine code before any of it runs",
   "Python code can only be run on the computer it was written on",
   "Every variable must be declared with its type before use"],
  ["Correct. That is the course's definition of an interpreted language.",
   "Wrong. That describes a COMPILED language.",
   "Wrong. Being interpreted says nothing of that kind.",
   "Wrong. Python is dynamically typed; no declarations are needed."],
  "Interpreted means the interpreter executes the source line by line. That is why a runtime error on line 40 appears only after lines 1 to 39 have run.",
  diff="easy", facets=["wording"])
Q(L, "colons", "Which two of these lines must end with a colon?",
  ["if score >= 50", "def greet(name)", "total = total + 1", "print(\"done\")"],
  ["Correct. An if opens a block, so its line ends with a colon.",
   "Correct. A def opens a block, so its line ends with a colon.",
   "Wrong. An assignment does not open a block.",
   "Wrong. A print call does not open a block."],
  "Every line that opens a block, if, elif, else, for, while, def, try, except, ends with a colon, and the block under it is indented.",
  style="multi", key=[0, 1], diff="easy", facets=["lists"])
TF(L, "case sensitivity", "True or false: Python is case sensitive, so Print(\"hi\") works exactly like print(\"hi\").",
   "false",
   "Wrong. Because Python IS case sensitive, Print and print are different names, and Print is not defined.",
   "Correct. Print is a different name from print, so Print(\"hi\") raises a NameError.",
   "Case sensitive means name, Name and NAME are three different names. print exists; Print does not.",
   diff="easy", facets=["wording"])
Q(L, "input, process, output", "What are the three parts of almost every program on this paper, in order?",
  ["Input, processing, output", "Output, input, processing", "Processing, output, input", "Compile, link, run"],
  ["Correct. Read something in, work something out, print the answer.",
   "Wrong. The output comes last.",
   "Wrong. You cannot process before you have the input.",
   "Wrong. Python is interpreted; there is no separate compile and link step to write."],
  "Every long question is input, then processing, then output, however elaborate the story around it.",
  diff="easy", facets=["lists"])

# ============================================================ Lesson 1.2
L = "1.2"
Q(L, "types", "What does this print?",
  ["float str bool", "int str bool", "float float bool", "float str str"],
  ["Correct. 3.0 has a decimal point, \"3\" is in quotes, and a comparison gives a bool.",
   "Wrong. 3.0 is a float, not an int, because of its decimal point.",
   "Wrong. \"3\" is in quotes, so it is a str.",
   "Wrong. 3 > 2 is a comparison, which gives True, a bool."],
  "The decimal point makes a float; quotes make a str; a comparison makes a bool. type(x).__name__ gives the plain name.",
  code=C("""
      print(type(3.0).__name__, type("3").__name__, type(3 > 2).__name__)
  """), check="out", facets=["numbers", "names"])
Q(L, "input is text", "The user types 5 at the prompt, so a holds \"5\". What does this print?",
  ["55", "10", "7", "an error, because text cannot be multiplied"],
  ["Correct. a is the string \"5\", and * on a string repeats it: \"5\" twice is 55.",
   "Wrong. That would need int(a) * 2. a is text.",
   "Wrong. Nothing here adds 5 and 2.",
   "Wrong. A string times a whole number is allowed; it repeats the string."],
  "input() always returns a string. \"5\" * 2 repeats the text, which is the silent version of the conversion mistake: it runs and gives the wrong answer.",
  code=C("""
      a = "5"      # what input() handed back
      b = 2
      print(a * b)
  """), check="out", facets=["numbers"])
Q(L, "conversion", "What does this print?",
  ["12.5", "12", "\"12\"0.5", "an error"],
  ["Correct. int(\"12\") is 12 and float(\"0.5\") is 0.5; an int plus a float gives a float.",
   "Wrong. Adding 0.5 cannot give a whole number.",
   "Wrong. Both strings were converted to numbers, so + adds rather than joins.",
   "Wrong. Both conversions succeed."],
  "Convert first, then calculate. Mixing an int and a float gives a float.",
  code=C("""
      print(int("12") + float("0.5"))
  """), check="out", diff="easy", facets=["numbers"])
Q(L, "int truncates", "What does this print?",
  ["-3", "-4", "-3.7", "4"],
  ["Correct. int() chops off the decimal part, towards zero, so -3.7 becomes -3.",
   "Wrong. int() does not round down; it simply drops the fraction.",
   "Wrong. int() returns a whole number.",
   "Wrong. The sign is kept."],
  "int() truncates: it removes the fractional part and does not round. int(7.9) is 7 and int(-3.7) is -3.",
  code=C("""
      print(int(-3.7))
  """), check="out", diff="hard", facets=["numbers"])
Q(L, "dynamic typing", "What does this print?",
  ["int\nstr", "int\nint", "str\nstr", "an error, because x changed type"],
  ["Correct. The type belongs to the value. x first holds an int, then is rebound to a str.",
   "Wrong. After the reassignment x holds text.",
   "Wrong. At the first print x holds the whole number 7.",
   "Wrong. Python is dynamically typed, so a name may be rebound to any type."],
  "Dynamically typed means the type belongs to the value, not the name, so no declaration is needed and a name can be rebound to a different type.",
  code=C("""
      x = 7
      print(type(x).__name__)
      x = "seven"
      print(type(x).__name__)
  """), check="out", facets=["numbers", "wording"])
Q(L, "comparing text", "What does this print?",
  ["True", "False", "an error, because strings cannot be compared", "10"],
  ["Correct. Text compares character by character, and \"9\" comes after \"1\".",
   "Wrong. That would be true of the NUMBERS 9 and 10, but these are strings.",
   "Wrong. Strings can be compared; they compare in dictionary order.",
   "Wrong. A comparison gives a bool."],
  "This is the silent trap: comparing unconverted input compares text, so \"9\" > \"10\" is True.",
  code=C("""
      print("9" > "10")
  """), check="out", diff="hard", facets=["numbers"])
Q(L, "choosing a conversion", "A program reads a person's height in metres, such as 1.75. Which line is correct?",
  ["height = float(input(\"Height: \"))", "height = int(input(\"Height: \"))",
   "height = input(\"Height: \")", "height = str(input(\"Height: \"))"],
  ["Correct. A height has a fractional part, so it needs float.",
   "Wrong. int would make 1.75 into 1, silently wrong.",
   "Wrong. input alone gives a string, which cannot be used in arithmetic.",
   "Wrong. input already returns a string; str changes nothing."],
  "int for counts, float for measurements, str to turn a number back into text.",
  diff="easy", facets=["names"])
TF(L, "input is text", "True or false: input() returns an int when the user types only digits.",
   "false",
   "Wrong. input() always returns a string, whatever the user types.",
   "Correct. It always returns a str; you must convert it with int() or float().",
   "The keyboard has no number key that Python believes: input() returns text, always.",
   facets=["names"])
Q(L, "conversion", "What does this print?",
  ["60 str", "60 int", "12 str", "6 str"],
  ["Correct. n is 3 * 2 = 6; str(6) + \"0\" is the text \"60\", a str.",
   "Wrong. Joining with + on strings gives a str, not an int.",
   "Wrong. n is 6, not 12.",
   "Wrong. The \"0\" is joined on the end."],
  "str() turns a number into text so it can be joined; the result is text, even when it looks like a number.",
  code=C("""
      n = int("3") * 2
      s = str(n) + "0"
      print(s, type(s).__name__)
  """), check="out", facets=["numbers"])

# ============================================================ Lesson 1.3
L = "1.3"
Q(L, "floor division and remainder", "What does this print?",
  ["5 3", "5.75 3", "6 3", "5 0.75"],
  ["Correct. 23 divided by 4 is 5 remainder 3: // gives 5 and % gives 3.",
   "Wrong. // throws the fraction away, so it is 5, not 5.75.",
   "Wrong. // does not round up.",
   "Wrong. % gives the remainder as a whole number, 3."],
  "// is floor division, the whole part; % is modulus, the remainder.",
  code=C("""
      print(23 // 4, 23 % 4)
  """), check="out", diff="easy", facets=["numbers"])
Q(L, "true division", "What does this print?",
  ["3.0", "3", "3.00", "an error"],
  ["Correct. / always returns a float, even when the division is exact.",
   "Wrong. That would be 9 // 3.",
   "Wrong. Python prints the float as 3.0.",
   "Wrong. 9 / 3 is perfectly valid."],
  "One slash, one point: / always gives a float.",
  code=C("""
      print(9 / 3)
  """), check="out", diff="easy", facets=["numbers"])
Q(L, "precedence", "What does this print?",
  ["4.0", "9.0", "1.0", "4"],
  ["Correct. / and * first, left to right: 4 / 2 = 2.0, then 2.0 * 3 = 6.0, then 10 - 6.0 = 4.0.",
   "Wrong. That does the subtraction first, which is the wrong order.",
   "Wrong. That multiplies 2 * 3 before dividing, but / and * go left to right.",
   "Wrong. / made a float, so the answer is 4.0."],
  "Precedence: ** first, then * / // %, left to right, then + and -.",
  code=C("""
      print(10 - 4 / 2 * 3)
  """), check="out", diff="hard", facets=["numbers", "lists"])
Q(L, "precedence", "What does this print?",
  ["11", "18", "14", "50"],
  ["Correct. Power first, 2 ** 2 = 4; then 4 * 2 = 8; then 3 + 8 = 11.",
   "Wrong. That adds 3 + 2 first.",
   "Wrong. That squares 2 * 2 in the wrong order.",
   "Wrong. That treats the whole thing as (3 + 2) ** 2 * 2."],
  "** is done first of all, then *, then +.",
  code=C("""
      print(3 + 2 ** 2 * 2)
  """), check="out", facets=["numbers", "lists"])
Q(L, "logical operators", "What does this print?",
  ["False True False", "True True False", "False False True", "True False True"],
  ["Correct. x < 3 is False so the and is False; x > 1 is True so the or is True; x == 3 is True so not gives False.",
   "Wrong. 3 < 3 is False, so the and is False.",
   "Wrong. The or needs only one True side, and x > 1 is True.",
   "Wrong. Check each part: and needs both, or needs one, not flips."],
  "and is True only when both sides are True; or when at least one is; not flips it.",
  code=C("""
      x = 3
      print(x > 1 and x < 3, x > 1 or x > 5, not x == 3)
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "augmented assignment", "What does this print?",
  ["5.0", "5", "10.0", "4.0"],
  ["Correct. 4 * 3 = 12, minus 2 = 10, then /= 2 gives 5.0, a float because of the single slash.",
   "Wrong. /= uses true division, which always gives a float.",
   "Wrong. The last step halves 10.",
   "Wrong. Work each line in order: 12, 10, 5.0."],
  "total += 5 means total = total + 5, and likewise for the others. /= divides with /, so the result is a float.",
  code=C("""
      total = 4
      total *= 3
      total -= 2
      total /= 2
      print(total)
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "short circuiting", "What does this print?",
  ["False\nTrue", "checked\nFalse\nchecked\nTrue", "False\nchecked\nTrue", "checked\nFalse\nTrue"],
  ["Correct. and stops at a False left side and or stops at a True left side, so check() is never called.",
   "Wrong. Neither call runs, because both expressions short circuit.",
   "Wrong. True or ... already knows it is True, so the right side is skipped.",
   "Wrong. False and ... already knows it is False, so check() is never called."],
  "and and or short circuit: if the left side settles the answer, the right side is never evaluated.",
  code=C("""
      def check():
          print("checked")
          return True

      print(False and check())
      print(True or check())
  """), check="out", diff="hard", facets=["numbers", "wording"])
Q(L, "remainder", "What does this print?",
  ["8 3", "3 8", "3.8 8", "0 38"],
  ["Correct. 38 % 10 is the last digit, 8, and 38 // 10 is 3.",
   "Wrong. The first value is the remainder, 8.",
   "Wrong. // gives a whole number.",
   "Wrong. 38 % 10 is 8, not 0."],
  "n % 10 gives the last digit and n // 10 drops it: a pair that turns up in digit questions.",
  code=C("""
      n = 38
      print(n % 10, n // 10)
  """), check="out", diff="easy", facets=["numbers"])
TF(L, "= against ==", "True or false: = compares two values and == assigns a value.",
   "false",
   "Wrong. It is the other way round.",
   "Correct. = assigns; == compares and gives True or False.",
   "= puts a value into a name; == asks whether two values are equal. Using = inside an if is a syntax error.",
   facets=["wording"])

# ============================================================ Lesson 1.4
L = "1.4"
Q(L, "indexing and slicing", "What does this print?",
  ["P T MPU", "M T MPU", "P E MPUT", "P T OMP"],
  ["Correct. Index 3 is P, -3 counts back to T, and [2:5] takes indexes 2, 3 and 4: M, P, U.",
   "Wrong. Index 3 is the fourth character, P.",
   "Wrong. -3 is T, and a slice stops BEFORE its stop index.",
   "Wrong. [2:5] starts at index 2, M."],
  "Indexes start at 0, negatives count from the end, and a slice includes its start and excludes its stop.",
  code=C("""
      s = "COMPUTER"
      print(s[3], s[-3], s[2:5])
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "count and find", "What does this print?",
  ["3 2 -1", "3 2 None", "2 2 -1", "3 3 -1"],
  ["Correct. banana has three a's; the first n is at index 2; find gives -1 when the text is absent.",
   "Wrong. find returns -1, not None, when nothing is found.",
   "Wrong. Count them: b-a-n-a-n-a has three a's.",
   "Wrong. find gives the FIRST n, at index 2."],
  "count(x) counts occurrences; find(x) gives the index of the first match, or -1.",
  code=C("""
      s = "banana"
      print(s.count("a"), s.find("n"), s.find("z"))
  """), check="out", facets=["numbers", "names"])
Q(L, "immutability", "What does this print?",
  ["hello", "HELLO", "Hello", "None"],
  ["Correct. upper() returns a new string, which was thrown away; s itself never changes.",
   "Wrong. The upper-case copy was never assigned to anything.",
   "Wrong. Nothing here capitalises one letter.",
   "Wrong. s still holds its original string."],
  "Strings are immutable. A string method hands back a NEW string; to keep it you must assign it, s = s.upper().",
  code=C("""
      s = "hello"
      s.upper()
      print(s)
  """), check="out", diff="medium", facets=["names", "wording"])
Q(L, "strip and len", "What does this print?",
  ["8 4", "4 4", "8 8", "6 4"],
  ["Correct. The string has two spaces, four letters and two spaces: 8 characters; strip() removes the spaces, leaving 4.",
   "Wrong. len counts the spaces too.",
   "Wrong. strip() removes the spaces at both ends.",
   "Wrong. Count the spaces on both sides: two and two."],
  "len counts every character, spaces included. strip() returns a copy without the whitespace at the ends.",
  code=C("""
      w = "  data  "
      print(len(w), len(w.strip()))
  """), check="out", facets=["numbers", "names"])
Q(L, "split and join", "What does this print?",
  ["3\nred-green-blue", "1\nred-green-blue", "3\nred green blue", "14\nred-green-blue"],
  ["Correct. split() cuts on spaces into a list of three words, and \"-\".join glues them back with dashes.",
   "Wrong. split() gives a list of three separate words.",
   "Wrong. join puts the separator it is called on, the dash, between the words.",
   "Wrong. len(words) counts the list's items, not the characters."],
  "split() returns a list; sep.join(list) returns a string, with sep between the items.",
  code=C("""
      words = "red green blue".split()
      print(len(words))
      print("-".join(words))
  """), check="out", facets=["numbers", "names"])
Q(L, "reversing and slicing", "What does this print?",
  ["nohtyP Pyth", "Python Pyth", "nohtyP thon", "nohtyP Pytho"],
  ["Correct. [::-1] reverses the string, and [:-2] stops two characters before the end.",
   "Wrong. [::-1] reverses it.",
   "Wrong. [:-2] keeps the START and drops the last two.",
   "Wrong. [:-2] drops two characters, not one."],
  "A negative step reverses; a negative stop counts from the end and, as always, is excluded.",
  code=C("""
      s = "Python"
      print(s[::-1], s[:-2])
  """), check="out", diff="hard", facets=["numbers"])
Q(L, "replace", "What does this print?",
  ["cat bat", "bat bat", "cat cat", "bat cat"],
  ["Correct. replace returns a new string, bat, in t; s is untouched.",
   "Wrong. s never changes; strings are immutable.",
   "Wrong. t holds the replaced copy.",
   "Wrong. The order printed is s then t."],
  "Every string method returns a new value and leaves the original alone.",
  code=C("""
      s = "cat"
      t = s.replace("c", "b")
      print(s, t)
  """), check="out", diff="easy", facets=["names"])
Q(L, "index against find", "What happens when this runs?",
  ["It raises ValueError, because index() raises when the text is absent", "It prints -1",
   "It prints None", "It prints 0"],
  ["Correct. index() does the same job as find() but raises ValueError on a miss.",
   "Wrong. That is what find() would return.",
   "Wrong. Neither method returns None.",
   "Wrong. \"d\" is not in \"abc\" at all."],
  "Use find() when a miss is expected: it returns -1. index() raises ValueError instead.",
  code=C("""
      print("abc".index("d"))
  """), check="err:ValueError", diff="medium", facets=["names"])
Q(L, "indexing past the end", "What happens when this runs?",
  ["It raises IndexError, because the last index of a five-letter string is 4", "It prints o",
   "It prints an empty string", "It prints H"],
  ["Correct. Indexes run 0 to 4, so index 5 is out of range.",
   "Wrong. o is at index 4.",
   "Wrong. A SLICE past the end gives an empty string; a single INDEX past the end raises.",
   "Wrong. H is at index 0."],
  "A slice that starts past the end quietly gives \"\", but a single index past the end is an IndexError.",
  code=C("""
      print("Hello"[5])
  """), check="err:IndexError", diff="hard", facets=["numbers"])
TF(L, "negative zero", "True or false: s[-0] gives the last character of s.",
   "false",
   "Wrong. -0 is just 0, so it gives the FIRST character.",
   "Correct. -0 equals 0, the first character; the last is s[-1].",
   "The paper's broken program used my_string[-0] for the last character. It is the first; the last is -1.",
   diff="medium", facets=["numbers"])

# ============================================================ Lesson 1.5
L = "1.5"
Q(L, "syntax sweep", "Which fault stops this program from running at all?",
  ["The for line has no colon at the end", "range(3) should be range(1, 3)",
   "total += n should be total = n", "print(total) should be indented"],
  ["Correct. A missing colon is a SyntaxError, found before anything runs.",
   "Wrong. range(3) is valid; it gives 0, 1, 2.",
   "Wrong. += is the correct way to accumulate.",
   "Wrong. The print belongs after the loop, so it is correctly unindented."],
  "Sweep one is syntax: quotes, colons, commas, brackets. Every block-opening line needs its colon.",
  code=C("""
      total = 0
      for n in range(3)
          total += n
      print(total)
  """), check="err:SyntaxError", diff="easy", facets=["wording"])
Q(L, "name sweep", "What happens when this runs?",
  ["NameError, because Student_name is not the same name as student_name", "It prints Hi Ada",
   "SyntaxError, because of the capital letter", "It prints Hi Student_name"],
  ["Correct. Python is case sensitive, so Student_name was never defined.",
   "Wrong. The two names differ in case, so Python treats them as different names.",
   "Wrong. A capital letter in a name is legal; the name simply does not exist.",
   "Wrong. Without quotes it is a name, not text."],
  "Sweep two is names: check every name letter for letter and capital for capital against where it was defined.",
  code=C("""
      student_name = "Ada"
      print("Hi", Student_name)
  """), check="err:NameError", diff="easy", facets=["wording"])
Q(L, "key sweep", "What happens when this runs?",
  ["It raises KeyError: 'Name', and the program stops", "It prints Ada", "It prints None", "It prints Name"],
  ["Correct. Keys are case sensitive; 'Name' is not a key, so the lookup raises KeyError.",
   "Wrong. The key stored is 'name', lower case.",
   "Wrong. d[key] raises; only d.get(key) returns None.",
   "Wrong. The lookup fails; nothing is printed."],
  "A dictionary key is a string, so it is case sensitive, and a missing key stops the program with KeyError.",
  code=C("""
      person = {"name": "Ada"}
      print(person["Name"])
  """), check="err:KeyError", diff="medium", facets=["names"])
Q(L, "missing comma", "Which fault is in this line, and what kind of error is it?",
  ["A missing comma between the two items: a SyntaxError", "A missing colon: a SyntaxError",
   "total is undefined: a NameError", "Text cannot be printed with a number: a TypeError"],
  ["Correct. The two things being printed need a comma between them.",
   "Wrong. A print call does not open a block, so it needs no colon.",
   "Wrong. total is defined on the first line; the problem is the missing comma.",
   "Wrong. print can show text and numbers together, separated by a comma."],
  "Missing commas and colons are the syntax faults the examiner plants most often.",
  code=C("""
      total = 5
      print("Total:" total)
  """), check="err:SyntaxError", diff="medium", facets=["wording"])
Q(L, "= in a condition", "What is wrong with this program?",
  ["= should be == in the if, and that is a syntax error", "The if needs brackets around the condition",
   "print must not be indented", "x must be declared as an int first"],
  ["Correct. = assigns; a condition needs == to compare.",
   "Wrong. Brackets are optional in Python.",
   "Wrong. The indented print is the if's block, as it should be.",
   "Wrong. Python needs no declarations."],
  "Using = where == was meant is a planted fault; inside an if it will not even run.",
  code=C("""
      x = 5
      if x = 5:
          print("five")
  """), check="err:SyntaxError", diff="easy", facets=["wording"])
Q(L, "mismatched quotes", "What happens when this runs?",
  ["A SyntaxError, because the string opens with a double quote and closes with a single quote",
   "It prints Hello", "It prints Hello'", "A NameError, because msg is undefined"],
  ["Correct. The string never closes, so Python cannot read the line.",
   "Wrong. The line cannot be parsed, so nothing runs.",
   "Wrong. The single quote does not close a double-quoted string.",
   "Wrong. The fault is found before any name is used."],
  "Line 1 of the paper's broken program had exactly this: \"Serve Jesus Now'.",
  code=C("""
      msg = "Hello'
      print(msg)
  """), check="err:SyntaxError", diff="easy", facets=["wording"])
Q(L, "meaning sweep", "The programmer wanted the LAST character. What does this print?",
  ["P", "n", "an error", "o"],
  ["Correct. -0 is 0, so s[-0] is the first character, P.",
   "Wrong. That is what s[-1] would give.",
   "Wrong. It runs; it just gives the wrong character.",
   "Wrong. o is at index 4."],
  "Sweep three is meaning: the program runs and quietly gives the wrong answer. The last character is s[-1].",
  code=C("""
      s = "Python"
      last = s[-0]
      print(last)
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "type sweep", "The user typed 20, so age holds \"20\". What happens next?",
  ["TypeError, because text and a number cannot be added", "It prints 21", "It prints 201", "It prints 20 1"],
  ["Correct. \"20\" + 1 mixes a str and an int, which + refuses.",
   "Wrong. age was never converted with int().",
   "Wrong. That would need str(1); + will not join text to a number.",
   "Wrong. + does not insert a space; it fails here."],
  "The fix is age = int(input(\"Age: \")). Unconverted input is the commonest planted type error.",
  code=C("""
      age = "20"      # what input() handed back
      print(age + 1)
  """), check="err:TypeError", diff="medium", facets=["names"])
Q(L, "the three sweeps", "In what order does the checklist sweep a broken listing?",
  ["Syntax, then names, then meaning", "Meaning, then names, then syntax",
   "Names, then syntax, then meaning", "All at once, in a single careful read"],
  ["Correct. First what stops it running, then names checked against their definitions, then indexes, types and logic.",
   "Wrong. Syntax comes first, because nothing runs until it is fixed.",
   "Wrong. Syntax comes before names.",
   "Wrong. One pass looking for everything finds one or two errors, not all of them."],
  "Three sweeps, and count your findings against the marks before you stop.",
  diff="easy", facets=["lists"])

# ============================================================ Lesson 2.1
L = "2.1"
Q(L, "grading chain", "What does this print?",
  ["Grade: C", "Grade: D", "Grade: B", "Grade: F"],
  ["Correct. 50 fails >= 70 and >= 60, then matches >= 50, and the chain stops.",
   "Wrong. The chain stops at the first True test, which is >= 50.",
   "Wrong. 50 is not >= 60.",
   "Wrong. else is reached only if every test fails."],
  "In an if / elif chain exactly one block runs: the first whose condition is True.",
  code=C("""
      score = 50
      if score >= 70:
          grade = "A"
      elif score >= 60:
          grade = "B"
      elif score >= 50:
          grade = "C"
      elif score >= 45:
          grade = "D"
      else:
          grade = "F"
      print("Grade:", grade)
  """), check="out", diff="easy", facets=["lists"])
Q(L, "chain order", "The chain below is in the wrong order. What does it print?",
  ["Grade: D", "Grade: A", "Grade: C", "Grade: A then Grade: D"],
  ["Correct. 80 >= 40 is True at the first test, so the chain stops there and gives D.",
   "Wrong. The A test is never reached; the first True test wins.",
   "Wrong. The chain stopped at the first test.",
   "Wrong. An elif chain runs at most one block."],
  "Order a chain from the most demanding test to the least, or a high score is caught by a low band.",
  code=C("""
      score = 80
      if score >= 40:
          grade = "D"
      elif score >= 50:
          grade = "C"
      elif score >= 70:
          grade = "A"
      print("Grade:", grade)
  """), check="out", diff="medium", facets=["lists"])
Q(L, "if against elif", "What does this print?",
  ["big\nmedium", "big", "medium", "big\nmedium\nsmall"],
  ["Correct. These are two SEPARATE if statements, so both conditions are tested and both are True.",
   "Wrong. That would be true with elif; separate ifs are each tested.",
   "Wrong. x > 10 is also True, so big prints first.",
   "Wrong. The else belongs to the second if, which was True."],
  "Separate ifs are all tested, so more than one can run. An elif chain runs at most one.",
  code=C("""
      x = 15
      if x > 10:
          print("big")
      if x > 5:
          print("medium")
      else:
          print("small")
  """), check="out", diff="medium", facets=["lists"])
Q(L, "if against elif", "The same test written with elif. What does this print?",
  ["big", "big\nmedium", "medium", "small"],
  ["Correct. The first True branch runs and the rest of the chain is skipped.",
   "Wrong. elif is part of one chain, so only one branch runs.",
   "Wrong. x > 10 is tested first and is True.",
   "Wrong. else runs only when every test fails."],
  "elif is a queue, if is a crowd: in a chain, only the first True branch runs.",
  code=C("""
      x = 15
      if x > 10:
          print("big")
      elif x > 5:
          print("medium")
      else:
          print("small")
  """), check="out", diff="easy", facets=["lists"])
Q(L, "nested decisions", "What does this print?",
  ["Too young", "Full", "Guest", "Full\nToo young"],
  ["Correct. age >= 18 is False, so the outer else runs and the inner if is never reached.",
   "Wrong. The inner if is only reached when age is at least 18.",
   "Wrong. The inner else belongs to the inner if, which is never reached.",
   "Wrong. Exactly one outer branch runs."],
  "An else belongs to the if at the same indentation. The inner decision only happens inside the outer True branch.",
  code=C("""
      age = 16
      member = True
      if age >= 18:
          if member:
              print("Full")
          else:
              print("Guest")
      else:
          print("Too young")
  """), check="out", diff="medium", facets=["lists"])
Q(L, "validating a range", "What does this print?",
  ["invalid", "ok", "ok\ninvalid", "an error, because comparisons cannot be chained"],
  ["Correct. 0 <= 105 <= 100 is False because 105 is above 100.",
   "Wrong. 105 is outside the range.",
   "Wrong. if and else never both run.",
   "Wrong. Python allows 0 <= score <= 100."],
  "A chained comparison is the neatest way to test a range: good when at least 0 AND at most 100.",
  code=C("""
      score = 105
      if 0 <= score <= 100:
          print("ok")
      else:
          print("invalid")
  """), check="out", diff="easy", facets=["numbers"])
Q(L, "catching a bad value", "Which condition correctly catches a score that is NOT between 0 and 100?",
  ["score < 0 or score > 100", "score < 0 and score > 100", "score > 0 or score < 100", "0 <= score <= 100"],
  ["Correct. A score is bad if it is below 0 OR above 100.",
   "Wrong. No number is below 0 and above 100 at once, so this is never True.",
   "Wrong. This is True for almost every number, good or bad.",
   "Wrong. That tests for a GOOD score."],
  "To catch a bad value use or; to confirm a good value use and.",
  diff="medium", facets=["wording"])
Q(L, "control structures", "for and while loops belong to which of the three control structures?",
  ["Iteration", "Selection", "Sequence", "Decomposition"],
  ["Correct. Iteration repeats a block while a condition holds or for each item.",
   "Wrong. Selection is if, elif and else.",
   "Wrong. Sequence is statements one after another.",
   "Wrong. That is not one of the three control structures."],
  "Sequence, selection, iteration: one after another, choose one, do it again.",
  diff="easy", facets=["names"])
TF(L, "else", "True or false: an else can carry its own condition, as in else score < 50:",
   "false",
   "Wrong. else takes no condition; that needs an elif.",
   "Correct. else catches everything left and takes no condition. A condition makes it an elif.",
   "Writing a condition after else is a planted syntax error.",
   diff="easy", facets=["wording"])

# ============================================================ Lesson 2.2
L = "2.2"
Q(L, "range with a step", "What does this print?",
  ["2 5 8", "2 5 8 11", "2 3 4 5 6 7 8 9", "3 6 9"],
  ["Correct. Start at 2, step 3, stop before 10: 2, 5, 8.",
   "Wrong. 11 is beyond the stop of 10.",
   "Wrong. The third number is the step, 3.",
   "Wrong. The sequence starts at 2."],
  "range(start, stop, step) starts at start and stops BEFORE stop. end=\" \" keeps the output on one line.",
  code=C("""
      for i in range(2, 10, 3):
          print(i, end=" ")
  """), check="out", diff="easy", facets=["numbers"])
Q(L, "counting down", "What does this print?",
  ["[5, 3, 1]", "[5, 3, 1, -1]", "[5, 4, 3, 2, 1]", "[]"],
  ["Correct. A negative step counts down, stopping before 0.",
   "Wrong. The stop, 0, is excluded, and -1 is past it.",
   "Wrong. The step is -2, not -1.",
   "Wrong. A negative step makes a descending range work."],
  "A negative step counts down, and the stop is still excluded.",
  code=C("""
      print(list(range(5, 0, -2)))
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "accumulator", "What does this print?",
  ["12", "1", "4", "0"],
  ["Correct. total starts at 0 before the loop and adds 4, 7 and 1.",
   "Wrong. That is what happens if total is reset inside the loop.",
   "Wrong. The loop adds all three numbers.",
   "Wrong. The additions happen inside the loop."],
  "Zero it before, add inside, print after: the accumulator pattern.",
  code=C("""
      total = 0
      for n in [4, 7, 1]:
          total += n
      print(total)
  """), check="out", diff="easy", facets=["numbers", "lists"])
Q(L, "accumulator trap", "total is reset INSIDE the loop. What does this print?",
  ["1", "12", "0", "an error"],
  ["Correct. Each pass sets total back to 0 and adds one number, so only the last, 1, survives.",
   "Wrong. The reset throws away the earlier additions.",
   "Wrong. The last pass adds 1 after resetting.",
   "Wrong. It runs; it just gives the wrong answer."],
  "Initialising the total inside the loop resets it every pass, so the answer is always the last number.",
  code=C("""
      for n in [4, 7, 1]:
          total = 0
          total += n
      print(total)
  """), check="out", diff="medium", facets=["numbers", "lists"])
Q(L, "while loop", "What does this print?",
  ["3\n2\n1\ngo", "3\n2\n1\n0\ngo", "go", "2\n1\n0\ngo"],
  ["Correct. n prints then drops by 1 each pass; when n reaches 0 the test fails and the loop ends.",
   "Wrong. When n is 0 the condition n > 0 is False, so 0 is not printed.",
   "Wrong. n > 0 is True at the start, so the body runs.",
   "Wrong. The print comes before the decrease."],
  "A while loop repeats while its condition is True; something in the body must eventually make it False.",
  code=C("""
      n = 3
      while n > 0:
          print(n)
          n -= 1
      print("go")
  """), check="out", diff="easy", facets=["numbers", "lists"])
Q(L, "break and continue", "What does this print?",
  ["1\n3", "1\n3\n5\n7", "1\n2\n3\n4", "1\n3\n5"],
  ["Correct. Even numbers are skipped by continue, and at 5 break ends the loop before printing.",
   "Wrong. break stops the loop at 5.",
   "Wrong. continue skips the even numbers.",
   "Wrong. break runs before 5 can be printed."],
  "break leaves the loop at once; continue skips the rest of this pass.",
  code=C("""
      for n in range(1, 8):
          if n == 5:
              break
          if n % 2 == 0:
              continue
          print(n)
  """), check="out", diff="hard", facets=["numbers", "lists"])
Q(L, "nested loops", "What does this print?",
  ["12", "7", "3", "4"],
  ["Correct. The inner loop runs 4 times for each of the 3 outer passes: 3 x 4 = 12.",
   "Wrong. The counts multiply; they do not add.",
   "Wrong. That counts only the outer passes.",
   "Wrong. That counts only one pass of the inner loop."],
  "The inner loop runs completely for every pass of the outer one, so multiply the counts.",
  code=C("""
      count = 0
      for i in range(3):
          for j in range(4):
              count += 1
      print(count)
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "sentinel loop", "The user types 5, then 8, then 0, then 3. The list stands in for input(). What does this print?",
  ["13 2", "16 3", "13 3", "16 4"],
  ["Correct. 5 and 8 are added; the 0 stops the loop before it is added or counted, and the 3 is never read.",
   "Wrong. The loop stops at 0, so 3 is never added.",
   "Wrong. The 0 is not counted, because the body never runs for it.",
   "Wrong. Neither the 0 nor the 3 is counted."],
  "A sentinel loop reads once before the loop and again at the bottom. The sentinel itself is never added or counted.",
  code=C("""
      typed = [5, 8, 0, 3]     # stands in for four input() calls
      i = 0
      total = 0
      count = 0
      number = typed[i]
      while number != 0:
          total += number
          count += 1
          i += 1
          number = typed[i]
      print(total, count)
  """), check="out", diff="hard", facets=["numbers", "lists"])
Q(L, "infinite loop", "What is wrong with this loop?",
  ["n never changes, so n < 5 stays True and it loops forever", "range() is missing",
   "The print should come after the loop", "while cannot compare numbers"],
  ["Correct. Nothing in the body updates n, so the condition never becomes False.",
   "Wrong. A while loop does not use range.",
   "Wrong. Moving the print does not fix the missing update.",
   "Wrong. while works with any condition."],
  "Forgetting to update the variable in the condition is how an infinite loop is written by accident.",
  code=C("""
      n = 1
      while n < 5:
          print(n)
  """), check=None, diff="easy", facets=["wording"])
Q(L, "count controlled loop", "What is a count controlled loop?",
  ["A loop that repeats a fixed, known number of times, decided before the loop begins",
   "A loop that runs until the user types a sentinel", "A loop that counts how many errors occurred",
   "A loop that never ends"],
  ["Correct. That is the definition, written in Python with for and usually range().",
   "Wrong. That is a sentinel, or condition, controlled loop.",
   "Wrong. Not the definition.",
   "Wrong. That is an infinite loop."],
  "for when you know how many times; while when you are waiting for something to happen.",
  diff="easy", facets=["wording"])

# ============================================================ Lesson 2.3
L = "2.3"
Q(L, "changing a list", "What does this print?",
  ["[5, 9, 3, 8, 1]", "[9, 5, 3, 8, 1]", "[5, 3, 8, 1, 9]", "[5, 9, 3, 8]"],
  ["Correct. append puts 1 at the end, then insert(1, 9) puts 9 at index 1.",
   "Wrong. insert(1, ...) places the item at index 1, the second position.",
   "Wrong. insert places 9 at index 1, not at the end.",
   "Wrong. append added 1 at the end."],
  "append(x) adds at the end; insert(i, x) adds at position i.",
  code=C("""
      xs = [5, 3, 8]
      xs.append(1)
      xs.insert(1, 9)
      print(xs)
  """), check="out", diff="medium", facets=["numbers", "names"])
Q(L, "remove", "What does this print?",
  ["[2, 4, 1]", "[2, 1]", "[4, 2, 4]", "[4, 2, 1]"],
  ["Correct. remove deletes the FIRST item equal to 4 and leaves the second.",
   "Wrong. remove deletes only one matching item.",
   "Wrong. remove takes a value, not an index.",
   "Wrong. The first 4 is the one removed."],
  "remove(x) deletes the first item equal to x, and raises ValueError if there is none.",
  code=C("""
      xs = [4, 2, 4, 1]
      xs.remove(4)
      print(xs)
  """), check="out", diff="medium", facets=["numbers", "names"])
Q(L, "append against +=", "What does this print?",
  ["3 4", "4 4", "3 3", "4 3"],
  ["Correct. append adds [3, 4] as ONE item, giving 3; += adds 3 and 4 as separate items, giving 4.",
   "Wrong. append adds the whole list as a single item.",
   "Wrong. += extends the list item by item.",
   "Wrong. The two results are the other way round."],
  "append adds one item; += and extend add the items of the other list one by one.",
  code=C("""
      a = [1, 2]
      a.append([3, 4])
      b = [1, 2]
      b += [3, 4]
      print(len(a), len(b))
  """), check="out", diff="hard", facets=["numbers", "names"])
Q(L, "sorted against sort", "What does this print?",
  ["[3, 1, 2] [1, 2, 3]", "[1, 2, 3] [1, 2, 3]", "[3, 1, 2] None", "[1, 2, 3] None"],
  ["Correct. sorted() returns a NEW sorted list and leaves xs alone.",
   "Wrong. sorted() does not change xs.",
   "Wrong. sorted() returns a list; it is .sort() that returns None.",
   "Wrong. xs is unchanged and ys holds the sorted copy."],
  "sorted(xs) gives a new list; xs.sort() sorts in place and returns None.",
  code=C("""
      xs = [3, 1, 2]
      ys = sorted(xs)
      print(xs, ys)
  """), check="out", diff="medium", facets=["numbers", "names"])
Q(L, "nested lists", "What does this print?",
  ["2 2", "2 3", "[2, 3] 2", "1 2"],
  ["Correct. n[0] is [1, [2, 3]]; [1] of that is [2, 3]; [0] of that is 2. n[0] has two items.",
   "Wrong. len counts items: n[0] holds a number and a list, two items.",
   "Wrong. The last [0] reaches inside [2, 3].",
   "Wrong. Peel one bracket at a time: n[0], then [1], then [0]."],
  "Peel a nested index one bracket at a time and write down what you have after each; len counts items, not the numbers inside them.",
  code=C("""
      n = [[1, [2, 3]], [4, 5]]
      print(n[0][1][0], len(n[0]))
  """), check="out", diff="hard", facets=["numbers"])
Q(L, "one-item tuple", "What does this print?",
  ["tuple int", "tuple tuple", "int int", "int tuple"],
  ["Correct. (5,) is a tuple because of the comma; (5) is just the number 5 in brackets.",
   "Wrong. Without a comma the brackets are only grouping.",
   "Wrong. The comma makes t a tuple.",
   "Wrong. They are the other way round."],
  "A tuple of one item needs a comma: (5,) is a tuple, (5) is 5.",
  code=C("""
      t = (5,)
      u = (5)
      print(type(t).__name__, type(u).__name__)
  """), check="out", diff="hard", facets=["names"])
Q(L, "pop", "What does this print?",
  ["30 [10, 20]", "30 [10, 20, 30]", "10 [20, 30]", "None [10, 20]"],
  ["Correct. pop() with no argument removes and returns the last item.",
   "Wrong. pop removes the item as well as returning it.",
   "Wrong. With no index, pop takes the LAST item.",
   "Wrong. Unlike append and sort, pop returns the item it removed."],
  "pop(i) removes and returns; with no index it takes the last item.",
  code=C("""
      xs = [10, 20, 30]
      print(xs.pop(), xs)
  """), check="out", diff="medium", facets=["numbers", "names"])
Q(L, "repeating a list", "What does this print?",
  ["[0, 0, 0, 1]", "[0, 1, 0, 1, 0, 1]", "[3, 1]", "[0, 0, 0, [1]]"],
  ["Correct. [0] * 3 repeats to [0, 0, 0], and + joins [1] on the end.",
   "Wrong. Only [0] is repeated, before [1] is joined.",
   "Wrong. * repeats the list; it does not multiply the item.",
   "Wrong. + joins the items of [1], not the list itself."],
  "* on a list repeats it; + joins two lists into one.",
  code=C("""
      print([0] * 3 + [1])
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "tuples are fixed", "What happens when this runs?",
  ["It raises TypeError, because a tuple cannot be changed", "It prints (1, 9, 3)",
   "It prints (1, 2, 3)", "It raises IndexError"],
  ["Correct. A tuple is immutable, so item assignment is refused.",
   "Wrong. The assignment is refused.",
   "Wrong. The error stops the program before the print.",
   "Wrong. Index 1 exists; the problem is changing it."],
  "Round brackets are fixed: assigning to a tuple item raises TypeError, as with a string.",
  code=C("""
      t = (1, 2, 3)
      t[1] = 9
      print(t)
  """), check="err:TypeError", diff="medium", facets=["names"])
Q(L, "copying a list", "What does this print?",
  ["[1, 2] [1, 2, 3]", "[1, 2, 3] [1, 2, 3]", "[1, 2] [1, 2]", "[1, 2, 3] [1, 2]"],
  ["Correct. list(a) makes a NEW list, so appending to b leaves a alone.",
   "Wrong. That is what b = a would do; list(a) is a copy.",
   "Wrong. b did get the 3.",
   "Wrong. a is the one left unchanged."],
  "Assignment does not copy: b = a gives one list two names. list(a) or a[:] makes a real copy.",
  code=C("""
      a = [1, 2]
      b = list(a)
      b.append(3)
      print(a, b)
  """), check="out", diff="hard", facets=["numbers", "names"])

# ============================================================ Lesson 2.4
L = "2.4"
Q(L, "sets", "What does this print?",
  ["4", "5", "3", "an error, because a string cannot become a set"],
  ["Correct. The set of \"hello\" keeps h, e, l and o, with the repeated l stored once.",
   "Wrong. Duplicates vanish, so the two l's count once.",
   "Wrong. Count the distinct letters: h, e, l, o.",
   "Wrong. set() accepts any sequence, including a string."],
  "A set holds at most one copy of any value, so len() counts distinct items.",
  code=C("""
      print(len(set("hello")))
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "set operations", "What does this print?",
  ["[1] [4] [1, 2, 3, 4]", "[4] [1] [1, 2, 3, 4]", "[1] [4] [2, 3]", "[1, 4] [1, 4] [1, 2, 3, 4]"],
  ["Correct. a - b is in a but not b; b - a is in b but not a; | is everything in either.",
   "Wrong. The order of a difference matters.",
   "Wrong. | is the union; [2, 3] would be the intersection, &.",
   "Wrong. A difference is one-sided."],
  "a - b in a not b, a & b in both, a | b in either. Read the phrase left to right and write the sets in that order.",
  code=C("""
      a = {1, 2, 3}
      b = {2, 3, 4}
      print(sorted(a - b), sorted(b - a), sorted(a | b))
  """), check="out", diff="medium", facets=["numbers", "lists"])
Q(L, "get", "What does this print?",
  ["None 1", "KeyError", "0 1", "b 1"],
  ["Correct. get() returns None for a missing key instead of raising, and the value for a present one.",
   "Wrong. d[\"b\"] would raise; get() does not.",
   "Wrong. get() returns None, not 0, unless told otherwise.",
   "Wrong. get() returns the value, not the key."],
  "d.get(key) is the safe lookup: the value, or None. d[key] raises KeyError.",
  code=C("""
      d = {"a": 1}
      print(d.get("b"), d.get("a"))
  """), check="out", diff="easy", facets=["names"])
Q(L, "changing a dictionary", "What does this print?",
  ["3 6", "2 6", "3 5", "4 6"],
  ["Correct. Assigning to an existing key replaces its value; assigning to a new key adds a pair.",
   "Wrong. z is a new key, so there are three pairs.",
   "Wrong. d[\"x\"] = 6 replaced the 5.",
   "Wrong. x was replaced, not duplicated; keys are unique."],
  "d[key] = value adds a new pair or changes an existing one. Keys are unique.",
  code=C("""
      d = {"x": 5, "y": 7}
      d["x"] = 6
      d["z"] = 1
      print(len(d), d["x"])
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "empty braces", "What does this print?",
  ["dict set", "set set", "set dict", "dict dict"],
  ["Correct. {} on its own is an empty DICTIONARY; an empty set must be written set().",
   "Wrong. {} is a dictionary.",
   "Wrong. They are the other way round.",
   "Wrong. set() makes a set."],
  "{} alone is an empty dictionary, not an empty set.",
  code=C("""
      print(type({}).__name__, type(set()).__name__)
  """), check="out", diff="hard", facets=["names"])
Q(L, "walking a dictionary", "What does this print?",
  ["Ben\nCy", "Ada\nBen\nCy", "Ben", "Cy\nBen"],
  ["Correct. items() walks each pair in insertion order, and only marks of 60 and above print.",
   "Wrong. Ada's 58 fails the test.",
   "Wrong. 60 >= 60 is True, so Cy prints too.",
   "Wrong. A dictionary keeps insertion order, Ben before Cy."],
  "Walk the pairs, test the value, print the ones that pass: the shape of every 'display those which' requirement.",
  code=C("""
      marks = {"Ada": 58, "Ben": 71, "Cy": 60}
      for name, m in marks.items():
          if m >= 60:
              print(name)
  """), check="out", diff="medium", facets=["lists"])
Q(L, "keys must be hashable", "What happens when this runs?",
  ["It raises TypeError, because a list cannot be a dictionary key", "It prints {[1, 2]: 'a'}",
   "It prints a", "It raises KeyError"],
  ["Correct. A key must be hashable, which means immutable; a list is mutable.",
   "Wrong. The dictionary cannot be built.",
   "Wrong. The error happens when the dictionary is made.",
   "Wrong. Nothing is looked up; the key itself is rejected."],
  "Strings, numbers and tuples can be keys; lists and sets cannot, because they can change.",
  code=C("""
      d = {[1, 2]: "a"}
      print(d)
  """), check="err:TypeError", diff="hard", facets=["wording"])
Q(L, "membership in a dictionary", "What does this print?",
  ["False True", "True True", "True False", "False False"],
  ["Correct. in on a dictionary checks the KEYS. 1 is a value, not a key; \"x\" is a key.",
   "Wrong. 1 is a value, and in does not look at values.",
   "Wrong. They are the other way round.",
   "Wrong. \"x\" is a key, so that test is True."],
  "in means a substring on a string, an item on a list or set, and a KEY on a dictionary.",
  code=C("""
      d = {"x": 1}
      print(1 in d, "x" in d)
  """), check="out", diff="hard", facets=["names"])
Q(L, "choosing a container", "Each student's matric number is paired with that student's name. Which container suits this?",
  ["A dictionary, because each name is paired with its number and can be looked up by it",
   "A set, because the numbers are unique", "A tuple, because the data is fixed", "A list, because it is ordered"],
  ["Correct. Paired data is key to value, which is exactly a dictionary.",
   "Wrong. A set holds single values, not pairs.",
   "Wrong. A tuple is one fixed record, not a lookup of many pairs.",
   "Wrong. A list would make you search for each pair."],
  "List grows, tuple is fixed, set is unique, dictionary pairs. Give the reason: the reason carries the mark.",
  diff="easy", facets=["wording"])

# ============================================================ Lesson 3.1
L = "3.1"
Q(L, "value returning functions", "What does this print?",
  ["14", "12", "7", "None"],
  ["Correct. area(3, 4) returns 12 and area(1, 2) returns 2; 12 + 2 is 14.",
   "Wrong. The second call adds 2 more.",
   "Wrong. The function multiplies, it does not add.",
   "Wrong. The function returns its result, so the calls can be added."],
  "Because a value returning function hands back its result, a call can be used anywhere a value can.",
  code=C("""
      def area(l, w):
          return l * w

      print(area(3, 4) + area(1, 2))
  """), check="out", diff="easy", facets=["numbers"])
Q(L, "void functions", "What does this print?",
  ["Hi Ada\nNone", "Hi Ada\nHi Ada", "None", "Hi Ada"],
  ["Correct. greet prints, then returns nothing, so result holds None.",
   "Wrong. The call runs once; result is what it returned, which is None.",
   "Wrong. The call prints Hi Ada first.",
   "Wrong. The second print shows result, which is None."],
  "A void function performs an action and returns None. Assigning its call stores None.",
  code=C("""
      def greet(name):
          print("Hi", name)

      result = greet("Ada")
      print(result)
  """), check="out", diff="medium", facets=["numbers", "wording"])
Q(L, "default and named arguments", "What does this print?",
  ["9 8 9", "9 8 1", "6 8 9", "9 6 9"],
  ["Correct. power(3) uses the default exponent 2; power(2, 3) is 8; named arguments give 9 ** 1.",
   "Wrong. exp=1, base=9 is 9 to the power 1, which is 9.",
   "Wrong. ** is power, so 3 ** 2 is 9.",
   "Wrong. 2 ** 3 is 8."],
  "A parameter with a default can be left out; arguments passed by name can come in any order.",
  code=C("""
      def power(base, exp=2):
          return base ** exp

      print(power(3), power(2, 3), power(exp=1, base=9))
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "returning two values", "What does this print?",
  ["7", "2 9", "(2, 9)", "11"],
  ["Correct. stats returns 2 and 9, which unpack into lo and hi; 9 - 2 is 7.",
   "Wrong. The print shows hi - lo, one number.",
   "Wrong. The two values were unpacked into separate names.",
   "Wrong. The program subtracts, it does not add."],
  "return a, b hands back two values, unpacked with two names on the left.",
  code=C("""
      def stats(xs):
          return min(xs), max(xs)

      lo, hi = stats([4, 9, 2])
      print(hi - lo)
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "scope", "What does this print?",
  ["5", "0", "None", "an error"],
  ["Correct. The count inside reset() is local to it, so the outer count is untouched.",
   "Wrong. Assigning inside a function makes a new local name.",
   "Wrong. The outer count still holds 5.",
   "Wrong. It runs without error."],
  "A name assigned inside a function is local and disappears when the function ends: what happens in the function stays in the function.",
  code=C("""
      count = 5

      def reset():
          count = 0

      reset()
      print(count)
  """), check="out", diff="hard", facets=["numbers", "wording"])
Q(L, "return ends the function", "What does this print?",
  ["1", "after\n1", "1\nafter", "None"],
  ["Correct. return hands back 1 and leaves the function at once, so the print after it never runs.",
   "Wrong. The line after return is never reached.",
   "Wrong. Nothing after return runs.",
   "Wrong. The function returns 1."],
  "return hands a value back AND leaves the function.",
  code=C("""
      def f():
          return 1
          print("after")

      print(f())
  """), check="out", diff="medium", facets=["numbers"])
Q(L, "defining is not calling", "What does this print?",
  ["bye", "hello\nbye", "hello", "nothing at all"],
  ["Correct. hello is defined but never called, so its body never runs.",
   "Wrong. A definition on its own produces no output.",
   "Wrong. print(\"bye\") runs; the function body does not.",
   "Wrong. The last line does print."],
  "Nothing inside a function happens until it is called.",
  code=C("""
      def hello():
          print("hello")

      print("bye")
  """), check="out", diff="easy", facets=["numbers"])
Q(L, "parameter and argument", "In def cube(num): and the call cube(4), which is the ARGUMENT?",
  ["4, the value supplied at the call", "num, the name in the definition", "cube, the function's name", "return, the keyword"],
  ["Correct. The argument is the value passed in when you call.",
   "Wrong. num is the PARAMETER.",
   "Wrong. That is the function's name.",
   "Wrong. return hands a value back."],
  "The parameter is the name in the definition; the argument is the value supplied at the call.",
  diff="easy", facets=["wording"])
Q(L, "benefits of functions", "Which two of these are benefits of modularising a program with functions?",
  ["Reusability: write once, call from many places", "Easier maintenance: a change made in one place takes effect everywhere",
   "The program always runs faster", "Every variable becomes global"],
  ["Correct. Reusability is one of the five benefits.",
   "Correct. Easier maintenance is one of the five benefits.",
   "Wrong. The course says modularising does NOT make the program run faster.",
   "Wrong. Names made inside a function are local."],
  "Five benefits: reusability, readability, easier debugging and testing, easier maintenance, teamwork and simpler design.",
  style="multi", key=[0, 1], diff="medium", facets=["lists"])
TF(L, "void functions", "True or false: a function with no return statement gives back None.",
   "true",
   "Correct. No return, or a bare return, means the function returns None.",
   "Wrong. It does return something: the special value None.",
   "Show or give: print shows, return hands back, and no return means None.",
   facets=["wording"])

# ============================================================ Lesson 3.2
L = "3.2"
Q(L, "ceil and floor", "What does this print?",
  ["3 2", "2 3", "2 2", "3 3"],
  ["Correct. ceil always rounds UP to the next whole number and floor always rounds DOWN.",
   "Wrong. They are the other way round.",
   "Wrong. ceil(2.1) goes up to 3.",
   "Wrong. floor(2.9) goes down to 2."],
  "math.ceil rounds up, math.floor rounds down, round goes to the nearest.",
  code=C("""
      import math
      print(math.ceil(2.1), math.floor(2.9))
  """), check="out", diff="easy", facets=["names", "numbers"])
Q(L, "from import", "What does this print?",
  ["7.0", "7", "49", "an error, because sqrt needs the math. prefix"],
  ["Correct. from math import sqrt brings sqrt in directly, and sqrt always returns a float.",
   "Wrong. sqrt returns a float, 7.0.",
   "Wrong. sqrt is the square root, not the square.",
   "Wrong. The from form brings the name in, so no prefix is needed."],
  "from math import sqrt gives you sqrt alone; import math gives you math.sqrt.",
  code=C("""
      from math import sqrt
      print(sqrt(49))
  """), check="out", diff="easy", facets=["names", "numbers"])
Q(L, "math.pi", "What does this print?",
  ["3.142", "3.14", "3.1416", "3"],
  ["Correct. round(math.pi, 3) keeps three decimal places.",
   "Wrong. That is two decimal places.",
   "Wrong. That is four decimal places.",
   "Wrong. round with 3 keeps three decimal places."],
  "When the paper says use the math module, use math.pi, rounded as asked.",
  code=C("""
      import math
      print(round(math.pi, 3))
  """), check="out", diff="easy", facets=["names", "numbers"])
Q(L, "mixing the two imports", "What happens when this runs?",
  ["It raises NameError, because the name math was never imported", "It prints 3.141592653589793",
   "It prints 3.14", "It raises ImportError"],
  ["Correct. from math import pi brings in pi alone; math itself is not a name in the program.",
   "Wrong. math.pi needs import math.",
   "Wrong. The line fails before printing anything.",
   "Wrong. The import itself succeeded."],
  "The two forms are not interchangeable: after from math import pi, write pi, not math.pi.",
  code=C("""
      from math import pi
      print(math.pi)
  """), check="err:NameError", diff="medium", facets=["names"])
Q(L, "import as", "What does this print?",
  ["3.0", "9", "3", "an error, because math was renamed"],
  ["Correct. import math as m renames the module, so m.sqrt(9) is 3.0.",
   "Wrong. sqrt is the square root.",
   "Wrong. sqrt returns a float.",
   "Wrong. Renaming is allowed; you then use the new name."],
  "import math as m gives the module a shorter name; everything is then reached through m.",
  code=C("""
      import math as m
      print(m.sqrt(9))
  """), check="out", diff="medium", facets=["names", "numbers"])
Q(L, "what a module is", "What is a module, in the course's words?",
  ["A file of Python definitions and statements that other programs can import and reuse",
   "A single function inside a program", "A folder of databases", "A window in a graphical interface"],
  ["Correct. That is the definition.",
   "Wrong. A module is a whole file, which may hold many functions.",
   "Wrong. A directory of MODULES is a package.",
   "Wrong. That is a tkinter window."],
  "A module is a file of Python code that can be imported; a package is a directory of modules.",
  diff="easy", facets=["wording"])
Q(L, "random", "What can random.randint(1, 6) return?",
  ["A whole number from 1 to 6, with both 1 and 6 possible", "A whole number from 1 to 5",
   "A decimal between 1 and 6", "Always 1"],
  ["Correct. randint(a, b) includes both ends.",
   "Wrong. Unlike range, randint includes its upper limit.",
   "Wrong. randint gives whole numbers.",
   "Wrong. It is random."],
  "random.randint(a, b) gives a whole number from a to b inclusive; random.choice(seq) picks one item.",
  diff="medium", facets=["names"])
TF(L, "import math", "True or false: after import math you can write sqrt(16) without the math. prefix.",
   "false",
   "Wrong. import math gives you the module, so you must write math.sqrt(16).",
   "Correct. The prefix is needed; only from math import sqrt lets you write sqrt alone.",
   "import math gives math dot something; from math import sqrt gives sqrt alone.",
   diff="easy", facets=["names"])

# ============================================================ Lesson 3.3
L = "3.3"
Q(L, "write mode truncates", "What does this print?",
  ["two", "one\ntwo", "one", "an error, because the file already exists"],
  ["Correct. Opening with \"w\" a second time empties the file, so only the second line is left.",
   "Wrong. That is what append mode, \"a\", would give.",
   "Wrong. The second \"w\" replaced the first line.",
   "Wrong. \"w\" happily opens an existing file, and empties it."],
  "w wipes, a adds, r reads.",
  code=C(r"""
      with open("t.txt", "w") as f:
          f.write("one\n")
      with open("t.txt", "w") as f:
          f.write("two\n")
      print(open("t.txt").read().strip())
  """), check="out", diff="medium", facets=["names"])
Q(L, "append mode", "What does this print?",
  ["one\ntwo", "two", "one", "two\none"],
  ["Correct. \"a\" opens at the end of the file, so the new line goes after the old one.",
   "Wrong. Append keeps the existing content.",
   "Wrong. The appended line is there too.",
   "Wrong. Appended data goes at the end."],
  "Append adds new data at the end and leaves everything already there.",
  code=C(r"""
      with open("t.txt", "w") as f:
          f.write("one\n")
      with open("t.txt", "a") as f:
          f.write("two\n")
      print(open("t.txt").read().strip())
  """), check="out", diff="easy", facets=["names"])
Q(L, "write adds no newline", "What does this print?",
  ["ab", "a\nb", "a b", "b"],
  ["Correct. write() puts exactly what it is given; with no \\n the two pieces join.",
   "Wrong. write() does not add a newline for you.",
   "Wrong. No space was written.",
   "Wrong. Both writes happen inside the same open file."],
  "Always write the newline yourself: without \\n every record runs into the next.",
  code=C(r"""
      with open("t.txt", "w") as f:
          f.write("a")
          f.write("b")
      print(open("t.txt").read())
  """), check="out", diff="medium", facets=["names"])
Q(L, "readlines", "What does this print?",
  ["3", "1", "6", "5"],
  ["Correct. readlines() returns a list with one string per line: x, y and z.",
   "Wrong. That is how many strings read() returns.",
   "Wrong. len counts lines here, not characters.",
   "Wrong. There are three lines."],
  "read() gives one string, readline() one line, readlines() a list of every line.",
  code=C(r"""
      with open("t.txt", "w") as f:
          f.write("x\ny\nz\n")
      print(len(open("t.txt").readlines()))
  """), check="out", diff="easy", facets=["names", "numbers"])
Q(L, "readline", "What does this print?",
  [r"'x\n'", "'x'", "x", r"['x\n']"],
  [r"Correct. readline() gives the next line as a string, still carrying its newline, which repr shows as \n.",
   "Wrong. The newline is kept.",
   "Wrong. repr shows the quotes and the newline marker.",
   "Wrong. readline() gives a string, not a list."],
  "readline() returns one line including its newline; readlines() returns a list of such strings.",
  code=C(r"""
      with open("t.txt", "w") as f:
          f.write("x\ny\n")
      with open("t.txt") as f:
          print(repr(f.readline()))
  """), check="out", diff="hard", facets=["names"])
Q(L, "reading a missing file", "No file called gone.txt exists. What happens when this runs?",
  ["It raises FileNotFoundError", "It creates an empty gone.txt", "It prints an empty line", "It raises KeyError"],
  ["Correct. Read mode needs the file to exist.",
   "Wrong. Only \"w\" and \"a\" create a missing file.",
   "Wrong. The open fails before any read.",
   "Wrong. KeyError is for dictionaries."],
  "\"r\" raises FileNotFoundError if the file is missing; \"w\" and \"a\" create it.",
  code=C("""
      f = open("gone.txt", "r")
      print(f.read())
  """), check="err:FileNotFoundError", diff="medium", facets=["names"])
Q(L, "the first records", "The file holds seven records. What does this print?",
  ["Student 1\nStudent 2", "Student 1\nStudent 2\nStudent 3", "Student 7", "Student 1"],
  ["Correct. lines[:2] takes the first two lines, and strip() removes each newline.",
   "Wrong. A slice stops before its stop index, 2.",
   "Wrong. [:2] takes from the start.",
   "Wrong. Two lines are taken."],
  "Given a list of lines, lines[:5] is the first five: a one-line answer to the paper's requirement.",
  code=C(r"""
      with open("r.txt", "w") as f:
          for i in range(1, 8):
              f.write(f"Student {i}\n")
      with open("r.txt") as f:
          lines = f.readlines()
      for line in lines[:2]:
          print(line.strip())
  """), check="out", diff="medium", facets=["numbers", "names"])
Q(L, "file modes", "Which mode opens a file for BOTH reading and writing, at the start, without truncating it?",
  ["\"r+\"", "\"w\"", "\"a\"", "\"r\""],
  ["Correct. r+ reads and writes, keeps the content, and raises if the file is missing.",
   "Wrong. w erases the file.",
   "Wrong. a writes at the end.",
   "Wrong. r reads only."],
  "The four modes the paper asks for: r read, w write and truncate, a append, r+ read and write.",
  diff="medium", facets=["names"])
Q(L, "write returns a count", "What does this print?",
  ["6", "5", "None", "hello"],
  ["Correct. write() returns the number of characters written: five letters and the newline.",
   "Wrong. The newline counts as a character.",
   "Wrong. write() returns a count.",
   "Wrong. It returns a number, not the text."],
  "f.write(s) writes the text and returns how many characters it wrote.",
  code=C(r"""
      with open("t.txt", "w") as f:
          n = f.write("hello\n")
      print(n)
  """), check="out", diff="hard", facets=["numbers", "names"])

# ============================================================ Lesson 3.4
L = "3.4"
Q(L, "where the error jumps", "What does this print?",
  ["a\nd\ne", "a\nc\nd\ne", "a\nd", "d\ne"],
  ["Correct. a prints, int(\"b\") raises ValueError, the rest of the try is skipped, except prints d, and the program carries on to e.",
   "Wrong. c is skipped: the error jumps straight to except.",
   "Wrong. After a handled exception the program continues.",
   "Wrong. a printed before the error."],
  "When a line in try raises, the rest of the try is skipped and the matching except runs; then the program continues.",
  code=C("""
      try:
          print("a")
          x = int("b")
          print("c")
      except ValueError:
          print("d")
      print("e")
  """), check="out", diff="medium", facets=["lists"])
Q(L, "else and finally", "What does this print?",
  ["ok 5\nend", "zero\nend", "ok 5", "end"],
  ["Correct. Nothing is raised, so else runs; finally runs every time.",
   "Wrong. 10 // 2 does not divide by zero.",
   "Wrong. finally always runs.",
   "Wrong. else runs because the try succeeded."],
  "else runs when nothing was raised; finally runs either way.",
  code=C("""
      try:
          n = 10 // 2
      except ZeroDivisionError:
          print("zero")
      else:
          print("ok", n)
      finally:
          print("end")
  """), check="out", diff="medium", facets=["lists"])
Q(L, "else and finally", "Now the division is by zero. What does this print?",
  ["zero\nend", "ok\nend", "zero", "end"],
  ["Correct. The except runs, else is skipped because the try failed, and finally still runs.",
   "Wrong. else runs only when nothing was raised.",
   "Wrong. finally always runs.",
   "Wrong. The except block prints first."],
  "Finally means finally: it runs whether the try worked or not.",
  code=C("""
      try:
          n = 10 // 0
      except ZeroDivisionError:
          print("zero")
      else:
          print("ok")
      finally:
          print("end")
  """), check="out", diff="medium", facets=["lists"])
Q(L, "catching the wrong exception", "What happens when this runs?",
  ["A KeyError stops the program, because except ValueError does not catch it", "It prints bad value",
   "It prints None", "It prints nothing and carries on"],
  ["Correct. except only catches the exception it names; this one is a KeyError.",
   "Wrong. The lookup raises KeyError, not ValueError.",
   "Wrong. d[\"b\"] raises; it does not give None.",
   "Wrong. An exception that is not caught stops the program."],
  "Name the exception you expect. An exception you did not name passes straight through.",
  code=C("""
      try:
          d = {"a": 1}
          print(d["b"])
      except ValueError:
          print("bad value")
  """), check="err:KeyError", diff="hard", facets=["names"])
Q(L, "raise", "What does this print?",
  ["Error: insufficient funds", "-30", "insufficient funds", "an unhandled ValueError"],
  ["Correct. raise signals the error, and the except catches it and prints its message.",
   "Wrong. The raise stops the function before it subtracts.",
   "Wrong. The print adds \"Error:\" in front.",
   "Wrong. The ValueError is caught."],
  "raise signals an error yourself; except ValueError as e gives you its message in e.",
  code=C("""
      def withdraw(balance, amount):
          if amount > balance:
              raise ValueError("insufficient funds")
          return balance - amount

      try:
          print(withdraw(50, 80))
      except ValueError as e:
          print("Error:", e)
  """), check="out", diff="hard", facets=["lists"])
Q(L, "which exception", "Which exception does this raise?",
  ["TypeError", "ValueError", "NameError", "SyntaxError"],
  ["Correct. + cannot join a string and a number: the wrong KIND of thing.",
   "Wrong. ValueError is the right kind with an impossible value, like int(\"abc\").",
   "Wrong. Nothing here is undefined.",
   "Wrong. The line is legal Python; it fails only when run."],
  "TypeError is the wrong kind; ValueError is the right kind with an impossible value.",
  code=C("""
      print("5" + 5)
  """), check="err:TypeError", diff="easy", facets=["names"])
Q(L, "syntax errors are not exceptions", "Can try and except catch a missing colon in the same file?",
  ["No: a syntax error stops the program from running at all, so no try block ever runs",
   "Yes, with except SyntaxError", "Yes, with a bare except", "Only inside a function"],
  ["Correct. Python cannot parse the file, so nothing runs, the try included.",
   "Wrong. The try block never gets the chance to run.",
   "Wrong. Nothing runs at all.",
   "Wrong. A syntax error anywhere stops the whole file."],
  "Syntax errors stop it starting. Exceptions stop it finishing, and only those can be caught.",
  diff="medium", facets=["wording"])
Q(L, "runtime exceptions", "Which two of these are exceptions raised while a program RUNS, rather than syntax errors?",
  ["ZeroDivisionError, from 10 / 0", "KeyError, from d[\"missing\"]",
   "A missing colon after an if", "A string that opens with \" and closes with '"],
  ["Correct. 10 / 0 is legal code that fails only when it runs.",
   "Correct. A missing key is found only when the lookup runs.",
   "Wrong. That is a syntax error, found before anything runs.",
   "Wrong. That is a syntax error too."],
  "An exception is an error detected during execution; a syntax error is bad grammar found first.",
  style="multi", key=[0, 1], diff="medium", facets=["names"])

# ============================================================ Lesson 3.5
DB = r"""
import sqlite3
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE t (name TEXT, score REAL)")
cur.executemany("INSERT INTO t VALUES (?, ?)", [("Ada", 70), ("Ben", 55), ("Cy", 82)])
conn.commit()
"""
L = "3.5"
Q(L, "SELECT with WHERE", "The table t holds Ada 70, Ben 55 and Cy 82. What does this print?",
  ["[('Cy',), ('Ada',)]", "[('Ada',), ('Cy',)]", "['Cy', 'Ada']", "[('Cy',), ('Ada',), ('Ben',)]"],
  ["Correct. Only scores above 60 match, ordered highest first, and each row comes back as a one-item tuple.",
   "Wrong. ORDER BY score DESC puts 82 before 70.",
   "Wrong. fetchall() returns a list of TUPLES.",
   "Wrong. Ben's 55 fails the WHERE."],
  "fetchall() gives every matching row as a list of tuples, even when each row has one column.",
  code=C(DB + r"""
cur.execute("SELECT name FROM t WHERE score > ? ORDER BY score DESC", (60,))
print(cur.fetchall())
"""), check="out", diff="hard", facets=["names", "numbers"])
Q(L, "aggregate functions", "The same table. What does this print?",
  ["(3, 82.0, 69.0)", "[(3, 82.0, 69.0)]", "3 82.0 69.0", "(3, 82, 69)"],
  ["Correct. The three functions come back as ONE row, a tuple, and the REAL column gives floats.",
   "Wrong. fetchone() gives one row, not a list.",
   "Wrong. The row is printed as a tuple.",
   "Wrong. score is REAL, so MAX and AVG are floats."],
  "COUNT(*), MAX() and AVG() in one query return a single row, collected with fetchone().",
  code=C(DB + r"""
cur.execute("SELECT COUNT(*), MAX(score), AVG(score) FROM t")
print(cur.fetchone())
"""), check="out", diff="hard", facets=["names", "numbers"])
Q(L, "UPDATE with no WHERE", "The same table. What does this print?",
  ["[(50.0,), (50.0,), (50.0,)]", "[(50.0,), (55.0,), (82.0,)]", "[(70.0,), (55.0,), (82.0,)]", "[(50.0,)]"],
  ["Correct. With no WHERE, UPDATE changes every row in the table.",
   "Wrong. Nothing limits the UPDATE to the first row.",
   "Wrong. The UPDATE ran and changed the scores.",
   "Wrong. All three rows are still there, all changed."],
  "WHERE or everywhere: UPDATE and DELETE without WHERE apply to every row.",
  code=C(DB + r"""
cur.execute("UPDATE t SET score = 50")
cur.execute("SELECT score FROM t")
print(cur.fetchall())
"""), check="out", diff="medium", facets=["names"])
Q(L, "DELETE with WHERE", "The same table. What does this print?",
  ["2", "3", "1", "0"],
  ["Correct. Only Ben's row has a score below 60, so one row goes and two remain.",
   "Wrong. The DELETE removed Ben.",
   "Wrong. Ada and Cy both stay.",
   "Wrong. WHERE limits the DELETE to matching rows."],
  "DELETE FROM t WHERE ... removes only the matching rows.",
  code=C(DB + r"""
cur.execute("DELETE FROM t WHERE score < ?", (60,))
cur.execute("SELECT COUNT(*) FROM t")
print(cur.fetchone()[0])
"""), check="out", diff="medium", facets=["names", "numbers"])
Q(L, "fetchone when nothing matches", "The same table. What does this print?",
  ["None", "()", "[]", "an error"],
  ["Correct. fetchone() returns None when there is no row to give.",
   "Wrong. It returns None, not an empty tuple.",
   "Wrong. That is what fetchall() returns for no rows.",
   "Wrong. An empty result is not an error."],
  "fetchone() gives the next row as a tuple, or None when the rows run out.",
  code=C(DB + r"""
cur.execute("SELECT name FROM t WHERE score > 100")
print(cur.fetchone())
"""), check="out", diff="medium", facets=["names"])
Q(L, "the one-item tuple", "What happens when this runs?",
  ["An error, because (\"Ada\") is only a string; the placeholder needs the tuple (\"Ada\",)",
   "It prints Ada's row", "It prints None", "It prints every row"],
  ["Correct. Without the comma the brackets are just grouping, so SQLite receives three characters instead of one value.",
   "Wrong. The parameters are wrong, so the query never runs.",
   "Wrong. The error happens before any fetch.",
   "Wrong. The query fails."],
  "(\"SS2\") is a string; (\"SS2\",) is a tuple, and the placeholder needs the tuple.",
  code=C(DB + r"""
cur.execute("SELECT * FROM t WHERE name = ?", ("Ada"))
print(cur.fetchone())
"""), check="err:ProgrammingError", diff="hard", facets=["names"])
Q(L, "SQL types", "Which SQL column type suits a score that can have a decimal part?",
  ["REAL", "INTEGER", "TEXT", "BLOB"],
  ["Correct. REAL is SQL's floating point type.",
   "Wrong. INTEGER holds whole numbers only.",
   "Wrong. TEXT holds strings.",
   "Wrong. BLOB holds raw binary data."],
  "The four SQL types: INTEGER, TEXT, REAL, BLOB.",
  diff="easy", facets=["names"])
Q(L, "IF NOT EXISTS", "Why write CREATE TABLE IF NOT EXISTS rather than plain CREATE TABLE?",
  ["So running the program a second time does not fail because the table is already there",
   "So the table is emptied each time", "So commit() is not needed", "So the columns get types automatically"],
  ["Correct. Without it, the second run fails, and the paper asks for tables created 'if they do not already exist'.",
   "Wrong. It does not empty anything.",
   "Wrong. commit() is still needed to keep inserted rows.",
   "Wrong. You still write the column types."],
  "IF NOT EXISTS makes the create safe to run again.",
  diff="easy", facets=["wording"])

# ============================================================ Lesson 3.6
L = "3.6"
Q(L, "geometry managers", "You are laying out a form of labels beside entry boxes. Which geometry manager suits it?",
  ["grid(), because a form is rows and columns", "pack(), because it stacks widgets", "place(), because it uses exact pixels", "mainloop()"],
  ["Correct. grid places widgets by row and column numbers, which is what a form is.",
   "Wrong. pack stacks widgets in the order added; it does not line up columns.",
   "Wrong. place works, but fixing every pixel is fragile.",
   "Wrong. mainloop starts the event loop; it does not arrange anything."],
  "pack stacks, grid uses rows and columns, place uses exact x and y.",
  diff="easy", facets=["names"])
Q(L, "geometry managers", "Which geometry manager positions a widget at exact x and y coordinates?",
  ["place()", "pack()", "grid()", "config()"],
  ["Correct. place uses exact pixel coordinates.",
   "Wrong. pack stacks widgets.",
   "Wrong. grid uses rows and columns.",
   "Wrong. config changes a widget's settings."],
  "The three geometry managers: pack, grid and place.",
  diff="easy", facets=["names"])
Q(L, "widgets", "Which widget gives the user a MULTI-line area to type in?",
  ["Text", "Entry", "Label", "Button"],
  ["Correct. Text is a multi line typing area.",
   "Wrong. Entry takes a single line.",
   "Wrong. A Label displays text the user cannot edit.",
   "Wrong. A Button is clicked, not typed in."],
  "Entry for one line, Text for several, Label to show, Button to click.",
  diff="easy", facets=["names"])
Q(L, "widgets", "What is a Frame used for?",
  ["Grouping other widgets together as a container", "Showing a picture only", "Starting the event loop", "Reading typed text"],
  ["Correct. A Frame is a container that groups other widgets.",
   "Wrong. Not its purpose in the course.",
   "Wrong. That is mainloop().",
   "Wrong. That is entry.get()."],
  "Frame groups; Label shows; Entry and Text take typing; Button clicks.",
  diff="easy", facets=["names"])
Q(L, "the two rules", "What does the course warn happens if you mix pack() and grid() in the same container?",
  ["The program can freeze", "The widgets are drawn twice", "Nothing; they combine neatly", "The window closes immediately"],
  ["Correct. The rule is never to mix pack and grid in one container.",
   "Wrong. Not what the course says.",
   "Wrong. That is exactly what the rule forbids.",
   "Wrong. That is what happens without mainloop()."],
  "Two rules: no mainloop, no window; and never mix pack with grid inside the same container.",
  diff="medium", facets=["wording"])
Q(L, "geometry managers", "Which two of these are tkinter geometry managers?",
  ["pack()", "grid()", "mainloop()", "Entry()"],
  ["Correct. pack is a geometry manager.",
   "Correct. grid is a geometry manager.",
   "Wrong. mainloop starts the event loop.",
   "Wrong. Entry is a widget."],
  "pack, grid and place arrange widgets; mainloop keeps the window alive.",
  style="multi", key=[0, 1], diff="easy", facets=["names"])
Q(L, "reading an entry", "How does a program read what the user typed into an Entry called entry?",
  ["entry.get()", "entry.read()", "input(entry)", "entry.mainloop()"],
  ["Correct. get() returns the typed text.",
   "Wrong. read() is for files.",
   "Wrong. input() reads the text console, not a widget.",
   "Wrong. mainloop belongs to the window."],
  "entry.get() reads what the user typed.",
  diff="easy", facets=["names"])
TF(L, "mainloop", "True or false: without window.mainloop(), the window appears and vanishes at once.",
   "true",
   "Correct. The program reaches its end and exits, taking the window with it.",
   "Wrong. mainloop is what keeps the window alive and waiting for the user.",
   "No loop, no window: mainloop starts the event loop that waits for clicks and typing.",
   facets=["names"])


# ============================================================ build
def run(code):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "q.py"
        p.write_text(code, encoding="utf-8")
        r = subprocess.run([sys.executable, str(p)], cwd=d, capture_output=True, text=True, timeout=20)
    err = None
    if r.returncode != 0:
        last = [l for l in r.stderr.strip().splitlines() if l.strip()][-1]
        err = last.split(":")[0].split(".")[-1].strip()
    out = "\n".join(l.rstrip() for l in r.stdout.rstrip("\n").splitlines())
    return out, err


def build():
    problems = []
    out = []
    for q in QUESTIONS:
        where = f"{q['id']} ({q['prompt'][:40]})"
        if q.get("code") and q.get("check"):
            got, err = run(q.get("run") or q["code"])
            kinds = q["check"].split("+")
            want_err = next((k.split(":")[1] for k in kinds if k.startswith("err:")), None)
            if want_err != err:
                problems.append(f"{where}: expected error {want_err}, got {err} (stdout {got!r})")
            if q.get("before") is not None and got != q["before"]:
                problems.append(f"{where}: printed {got!r} before stopping, not {q['before']!r}")
            if "out" in kinds and q["style"] != "tf":
                key = q["opts"][0]
                if key != got:
                    problems.append(f"{where}: key {key!r} but Python printed {got!r}")
                for o in q["opts"][1:]:
                    if o == got:
                        problems.append(f"{where}: wrong option {o!r} is ALSO the real output")
        qid = q["id"]
        base = dict(id=qid, module=TOPIC[q["lesson"]], slides=[f"Lesson {q['lesson']}"],
                    style=q["style"], difficulty=q["diff"],
                    facets=q["facets"] or (["numbers"] if q.get("code") else ["wording"]),
                    topic=q["topic"], prompt=q["prompt"])
        if q.get("code"):
            base["code"] = q["code"]
        if q["style"] == "tf":
            base.update(answer=q["answer"], explanation=q["exp"], why=q["why"])
        else:
            n = len(q["opts"])
            if len(q["why"]) != n:
                problems.append(f"{where}: {n} options but {len(q['why'])} verdicts")
                continue
            order = list(range(n))
            random.Random(qid).shuffle(order)
            ids = "abcdef"
            opts = [dict(id=ids[i], text=q["opts"][j]) for i, j in enumerate(order)]
            why = {ids[i]: q["why"][j] for i, j in enumerate(order)}
            correct = [ids[i] for i, j in enumerate(order) if j < q["nkey"]]
            base.update(options=opts,
                        answer=correct if q["style"] == "multi" else correct[0],
                        explanation=q["exp"], why=why)
        out.append(base)
    if problems:
        print("AUTHORING STOPPED:")
        for p in problems:
            print("  x", p)
        sys.exit(1)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    by = {}
    for q in out:
        by[q["slides"][0]] = by.get(q["slides"][0], 0) + 1
    ran = sum(1 for q in QUESTIONS if q.get("check"))
    print(f"  wrote {len(out)} questions to {OUT.relative_to(HERE.parent.parent)}; {ran} programs run and checked")
    print("  " + ", ".join(f"{k}: {v}" for k, v in sorted(by.items())))


if __name__ == "__main__":
    build()
