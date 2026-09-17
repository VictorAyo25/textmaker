# Topic Four: functions, modules, files, exceptions. Loaded by csc241_doing.py.
M(
    "m4",
    kick="Topic Four",
    title="Learn by Doing: Topic Four",
    lead="Topic Four sat as a paper: the objective questions on functions, modules, files and exceptions, then two full written questions, each answered as you would write it and then taught from nothing.",
    minutes=90,
    intro="<p><b>Functions that return and functions that do not, the modules you are allowed to import, reading and writing files, and catching what goes wrong.</b> This topic is where the longer programs on the paper come from.</p>"
    "<div class=\"keypoint\"><span class=\"kplab\">How to sit this</span>"
    "<p><b>Part A</b> is the objective questions on this topic, the manual's own first.</p>"
    "<p><b>Part B</b> is two questions of 17.5 marks with four or five parts each. Every program here is one you could be asked to write from a blank page, so write it from a blank page.</p></div>"
    "<p><b>The habit that pays:</b> define the function above where it is called, give it a return, and let the program that uses it read as three lines. An examiner can see a structure like that from across the room.</p>",
    lockin=dict(
        big='"A function without return hands back None. A file opened with w is emptied the moment it is opened, and try catches only what you name."',
        sub="A parameter is in the definition, an argument is in the call. import math then math.pi. Open with the with statement and the file closes itself, whatever happens.",
    ),
)

Q(
    "m4",
    heading="Functions, scope, and a module you are given",
    marks="17.5 marks",
    scenario=dict(
        printed=False,
        tag="written for practice, in the shape the examiner sets",
        text="<p>Part (c) gives you a listing to trace by hand.</p>"
        + show(
            """
count = 0

def add(item, basket=[]):
    basket.append(item)
    return basket

def tally():
    count = 1
    return count

print(add("bread"))
print(add("milk"))
print(tally(), count)
""",
            "trace.py",
        ),
    ),
    asked="<table><tr><th>Part</th><th>What to write</th><th>Marks</th></tr>"
    "<tr><td>(a)</td><td>What is a function? Distinguish a void function from a value returning one, and a parameter from an argument</td><td>3.5</td></tr>"
    "<tr><td>(b)</td><td>Explain default parameter values, and show how a function can return more than one value</td><td>3</td></tr>"
    "<tr><td>(c)</td><td>Write down exactly what the listing prints, and explain the last line of output</td><td>3</td></tr>"
    "<tr><td>(d)</td><td>Write a function that tests whether a number is prime, and a program that uses it to print every prime up to a number the user enters</td><td>4</td></tr>"
    "<tr><td>(e)</td><td>What is a module? State two ways to import one, and write a program that uses the math module to find the area and circumference of a circle</td><td>4</td></tr></table>",
    breakdown=dict(
        question="<p>The last line of the listing prints two numbers. Why is the second one still zero, and what would you have to write to change it?</p>",
        answer="<p class=\"row\"><b class=\"lab\">Why zero</b> The assignment inside tally creates a NEW local variable that happens to share the name. A function cannot change a global by assigning to it; the local one dies when the function returns.</p>"
        "<p class=\"row\"><b class=\"lab\">To change it</b> Declare <code>global count</code> inside the function, or better, return the value and assign it at the call: <code>count = tally()</code>.</p>"
        "<p class=\"row\"><b class=\"lab\">The other catch</b> The default list in add is created ONCE, when the function is defined, so the second call appends to the same list and shows both items.</p>"
        "<p class=\"row\"><b class=\"lab\">Marks</b> Part (d) is four marks for two things: the function, and the loop that uses it. Write the function first and call it from a loop; do not write one long program with no function in it.</p>",
    ),
    exam=dict(
        problem="<p>(a) Functions, void against value returning, parameter against argument. (b) Default parameters and returning several values. (c) Trace the listing and explain its last line. (d) A prime testing function and a program that uses it. (e) Modules, two import forms, and a circle program.</p>",
        answer="<p><b>(a) Functions.</b> A function is a named block of code that performs one task and can be called as often as needed. It is defined with <code>def</code>, a name, brackets holding its parameters, and a colon, and its body is the indented block under it.</p>"
        "<table><tr><th></th><th>Void function</th><th>Value returning function</th></tr>"
        "<tr><td>What it does</td><td>Performs an action, such as printing, and hands nothing back</td><td>Computes a value and hands it back with <code>return</code></td></tr>"
        "<tr><td>What the call is worth</td><td><b>None</b>, which is what Python returns when there is no return statement</td><td>The returned value, which can be assigned or printed</td></tr>"
        "<tr><td>Typical use</td><td><code>show_menu()</code></td><td><code>area = circle_area(7)</code></td></tr>"
        "</table><p><b>Parameter against argument:</b> a <b>parameter</b> is the name in the function's definition; an <b>argument</b> is the actual value passed in the call. In <code>def cube(num)</code> the parameter is num; in the call <code>cube(4)</code> the argument is 4.</p>"
        + ran(
            """
def show(name):
    print("Hello", name)

def cube(num):
    return num ** 3

result = show("Ada")
print("show returned:", result)
print("cube returned:", cube(4))
"""
        )
        + "<p><b>(b) Default parameters, and returning several values.</b> A parameter can be given a default in the definition, and the call may then leave it out. Defaults must come after the parameters that have none.</p>"
        "<p>A function returns several values by returning them separated by commas, which makes a <b>tuple</b>, and the call can unpack it into several names at once.</p>"
        + ran(
            """
def power(base, exponent=2):
    return base ** exponent

def stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

print(power(5), power(5, 3))

low, high, mean = stats([45, 62, 70])
print(low, high, round(mean, 2))
print(stats([45, 62, 70]))
"""
        )
        + "<p><b>(c) The trace.</b></p>"
        + ran(
            """
count = 0

def add(item, basket=[]):
    basket.append(item)
    return basket

def tally():
    count = 1
    return count

print(add("bread"))
print(add("milk"))
print(tally(), count)
"""
        )
        + "<p><b>The last line explained.</b> The function returned 1, so the first number is 1. The global <code>count</code> is still 0, because the assignment inside the function created a <b>new local variable</b> with the same name, which was destroyed when the function returned. A function can READ a global, but assigning to that name inside it makes a local instead, unless the name is declared <code>global</code> first. The cleaner fix is the one the exam rewards: return the value and assign it at the call site, <code>count = tally()</code>.</p>"
        "<p><b>And the second line of output.</b> The list printed both items, although each call passed only one. A <b>default value is created once</b>, when the def is executed, so every call that leaves the parameter out shares the same list. It is why a mutable default is a bug: write <code>basket=None</code> and build a fresh list inside the function.</p>"
        "<p><b>(d) The prime function and the program.</b></p>"
        + ran(
            """
def is_prime(number):
    if number < 2:
        return False
    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False
    return True

limit = int(input("Up to: "))

for candidate in range(2, limit + 1):
    if is_prime(candidate):
        print(candidate, end=" ")

print()
""",
            stdin="30",
            name="primes.py",
        )
        + "<p>Three things earn the marks: the function does one job and returns True or False; <code>return False</code> leaves the moment a divisor is found, so nothing is tested after the answer is known; and the loop only goes up to the square root, because a factor above it would already have been found below it. Testing every number up to n is still correct and still earns most of the marks.</p>"
        "<p><b>(e) Modules.</b> A module is a file of Python code, holding functions, constants and classes, that another program can bring in and use. The standard library ships with many: math, random, datetime, os, sqlite3.</p>"
        "<p>Two ways to import:</p><ol>"
        "<li><code>import math</code>, then use it as <code>math.pi</code>. The module name stays in front, so nothing clashes with your own names.</li>"
        "<li><code>from math import pi, sqrt</code>, then use <code>pi</code> directly. Shorter, but it can collide with a name of your own.</li>"
        "</ol><p>A third form, <code>import math as m</code>, renames it.</p>"
        + ran(
            """
import math
from math import sqrt

radius = float(input("Radius: "))

area = math.pi * radius ** 2
circumference = 2 * math.pi * radius

print(f"Area: {area:.2f}")
print(f"Circumference: {circumference:.2f}")
print(f"The radius from the area again: {sqrt(area / math.pi):.2f}")
""",
            stdin="7",
            name="circle.py",
        ),
    ),
    frames=[
        dict(
            check="",
            teach="<p>A function is a named block you can call as often as you like. <code>def</code>, a name, brackets, a colon, then an indented body.</p>"
            + ran('def greet(name):\n    print("Hello", name)\n\ngreet("Ada")\ngreet("Grace")'),
            ask="That function printed something. What value did the CALL itself produce?",
        ),
        dict(
            check="None: it has no return statement.",
            teach="<p>That is the difference between a <b>void</b> function, which acts, and a <b>value returning</b> one, which hands something back with <code>return</code>. Print inside the function and you can only see it; return it and you can use it.</p>"
            + ran('def cube(n):\n    return n ** 3\n\nprint(cube(4))\nprint(cube(4) + 1)'),
            ask="In def cube(n) and the call cube(4), which is the parameter and which is the argument?",
        ),
        dict(
            check="n is the parameter, in the definition. 4 is the argument, in the call.",
            teach="<p>Worth memorising in those words, because it is asked directly. Next: a parameter can carry a <b>default</b>, and then the call may leave it out.</p>"
            + ran('def power(base, exponent=2):\n    return base ** exponent\n\nprint(power(5), power(5, 3))'),
            ask="A function can also hand back several values at once. How, do you think?",
        ),
        dict(
            check="Return them separated by commas, which makes a tuple.",
            teach="<p>And the call can unpack it into several names in one line, which is how min, max and mean come back from one function.</p>"
            + ran(
                """
def stats(xs):
    return min(xs), max(xs), sum(xs) / len(xs)

low, high, mean = stats([45, 62, 70])
print(low, high, round(mean, 2))
"""
            ),
            ask="Now scope. A global count is 0, and a function assigns count = 1 inside itself. What is the global afterwards?",
        ),
        dict(
            check="Still 0.",
            teach="<p>Because assigning to a name inside a function creates a <b>local</b> variable, which dies when the function returns. It can read a global, but it cannot change one by assignment unless it says <code>global count</code> first.</p>"
            + ran(
                """
count = 0

def tally():
    count = 1
    return count

print(tally(), count)
"""
            ),
            ask="What is the better fix than declaring it global?",
        ),
        dict(
            check="Return the value and assign it where the function is called.",
            teach="<p>A function that takes its inputs as parameters and hands its answer back with return is one you can test and reuse. Now modules: a file of code you import.</p>"
            + ran('import math\nfrom math import sqrt\nprint(math.pi, sqrt(49))'),
            ask="Two import forms are shown. What does the first one buy you that the second does not?",
        ),
        dict(
            check="The module name stays in front, so nothing collides with your own names.",
            teach="<p><code>import math</code> then <code>math.pi</code> is the safe default; <code>from math import pi</code> is shorter and can clash. Either earns the mark, and the area of a circle is <code>math.pi * r ** 2</code>, with two stars and never a caret.</p>",
            ask="",
        ),
    ],
)

Q(
    "m4",
    heading="Files, exceptions, and a program that must not crash",
    marks="17.5 marks",
    scenario=dict(
        printed=False,
        tag="written for practice, in the shape the examiner sets",
        text="<p>A department keeps a list of student names in a text file, one per line, and a small program that divides two numbers typed by a user.</p>",
    ),
    asked="<table><tr><th>Part</th><th>What to write</th><th>Marks</th></tr>"
    "<tr><td>(a)</td><td>State four file modes and what each does, including what happens when the file does not exist</td><td>3.5</td></tr>"
    "<tr><td>(b)</td><td>What does the with statement do, and why is it preferred to open and close?</td><td>2</td></tr>"
    "<tr><td>(c)</td><td>Write a program that asks for three student names, saves them to a file one per line, then reads the file back and prints each name numbered, with a count at the end</td><td>5</td></tr>"
    "<tr><td>(d)</td><td>Explain try, except, else and finally, and what each part is for</td><td>3</td></tr>"
    "<tr><td>(e)</td><td>Write a program that divides two numbers typed by the user and survives both a letter typed instead of a number and a division by zero</td><td>4</td></tr></table>",
    breakdown=dict(
        question="<p>In part (c), which mode would silently destroy the file if the program were run twice, and in part (e), which two exception names must appear?</p>",
        answer="<p class=\"row\"><b class=\"lab\">The destructive mode</b> <code>\"w\"</code>. Opening a file for writing EMPTIES it immediately, before a single line is written. To add to a file instead, open it with <code>\"a\"</code>.</p>"
        "<p class=\"row\"><b class=\"lab\">The two exceptions</b> <code>ValueError</code>, raised by int() when the text is not a number, and <code>ZeroDivisionError</code>, raised by the division itself.</p>"
        "<p class=\"row\"><b class=\"lab\">The mark that is usually lost</b> Naming the exception. <code>except:</code> on its own catches everything, including your own typing mistakes, and the examiner wants the name.</p>"
        "<p class=\"row\"><b class=\"lab\">Reading back</b> A line read from a file ends in a newline, so strip it before printing or counting.</p>",
    ),
    exam=dict(
        problem="<p>(a) Four file modes. (b) The with statement. (c) A program that writes three names to a file and reads them back numbered. (d) try, except, else and finally. (e) A division program that survives bad input and division by zero.</p>",
        answer="<p><b>(a) The file modes.</b></p><table><tr><th>Mode</th><th>What it does</th><th>If the file does not exist</th></tr>"
        "<tr><td><code>\"r\"</code> read</td><td>Opens for reading only, positioned at the start. The default</td><td><b>FileNotFoundError</b></td></tr>"
        "<tr><td><code>\"w\"</code> write</td><td>Opens for writing and <b>empties the file at once</b>, whatever was in it</td><td>Creates it</td></tr>"
        "<tr><td><code>\"a\"</code> append</td><td>Opens for writing at the END, keeping what is already there</td><td>Creates it</td></tr>"
        "<tr><td><code>\"r+\"</code> read and write</td><td>Opens for both, positioned at the start, without emptying it</td><td>FileNotFoundError</td></tr>"
        "</table><p>Adding <code>b</code>, as in <code>\"rb\"</code>, opens the file in binary rather than text.</p>"
        "<p><b>(b) The with statement.</b> <code>with open(\"names.txt\") as f:</code> opens the file and <b>closes it automatically</b> when the block ends, even if an error is raised inside the block. Without it you must call <code>f.close()</code> yourself, and any exception before that line leaves the file open, with data possibly still unwritten in the buffer. Fewer lines, and nothing to forget.</p>"
        "<p><b>(c) Writing and reading the names.</b></p>"
        + ran(
            """
names = []
for i in range(1, 4):
    names.append(input(f"Name {i}: ").strip())

with open("students.txt", "w") as f:
    for name in names:
        f.write(name + "\\n")

print("Saved. Reading it back:")

count = 0
with open("students.txt", "r") as f:
    for line in f:
        count += 1
        print(f"{count}. {line.strip()}")

print(f"{count} names in the file")
""",
            stdin="Ada\nGrace\nChinwe",
            name="students.py",
        )
        + "<p>Four things the examiner is looking for: the file is opened with <code>with</code>; <code>\"w\"</code> to create it and <code>\"r\"</code> to read it; <code>write</code> does NOT add a line ending, so the newline is written explicitly; and each line read back is stripped, because it arrives with that newline still attached.</p>"
        "<p><b>(d) try, except, else and finally.</b></p><table><tr><th>Part</th><th>What it is for</th></tr>"
        "<tr><td><code>try</code></td><td>Holds the code that might raise an exception. Keep it as short as possible, so you know what failed</td></tr>"
        "<tr><td><code>except</code></td><td>Runs only if the named exception was raised, and stops the program from crashing. There may be several, one per exception name</td></tr>"
        "<tr><td><code>else</code></td><td>Runs only if NO exception was raised. It is where the work that depends on the try succeeding belongs</td></tr>"
        "<tr><td><code>finally</code></td><td>Runs either way, exception or not. It is for cleaning up, such as closing a file or a database connection</td></tr>"
        "</table><p>An exception is an error raised while the program runs: ValueError, ZeroDivisionError, FileNotFoundError, TypeError, IndexError, KeyError. Catching one by name is the whole point; a bare <code>except:</code> hides every fault, including your own.</p>"
        "<p><b>(e) The division program.</b></p>"
        + ran(
            """
try:
    a = float(input("First number: "))
    b = float(input("Second number: "))
    result = a / b
except ValueError:
    print("That was not a number.")
except ZeroDivisionError:
    print("You cannot divide by zero.")
else:
    print(f"{a} divided by {b} is {result:.2f}")
finally:
    print("Done.")
""",
            stdin="10\n4",
            name="divide.py",
        )
        + "<p>Run again with a letter, and again with a zero, and the same program survives both:</p>"
        + ran(
            """
for attempt in [("ten", "4"), ("10", "0")]:
    try:
        a = float(attempt[0])
        b = float(attempt[1])
        result = a / b
    except ValueError:
        print("That was not a number.")
    except ZeroDivisionError:
        print("You cannot divide by zero.")
    else:
        print(f"{a} divided by {b} is {result:.2f}")
    finally:
        print("Done.")
""",
            name="both_faults.py",
        ),
    ),
    frames=[
        dict(
            check="",
            teach="<p>A file is opened with <code>open(name, mode)</code>, and the mode is the whole question. <code>\"r\"</code> reads, <code>\"w\"</code> writes, <code>\"a\"</code> appends.</p>",
            ask="You open an existing file with w and then your program crashes before writing anything. What is in the file now?",
        ),
        dict(
            check="Nothing. It was emptied the moment it was opened.",
            teach="<p>That is the fact worth a mark on its own: <b>w truncates immediately</b>. Use <code>\"a\"</code> to add to a file and keep what is there. Reading a file that does not exist with <code>\"r\"</code> raises a FileNotFoundError.</p>",
            ask="Now, what is wrong with open, then work, then close, written out by hand?",
        ),
        dict(
            check="If the work raises an error, close never runs and the file stays open.",
            teach="<p>Which is why <code>with open(...) as f:</code> exists: the file is closed when the block ends, error or no error. Use it every time.</p>"
            + ran(
                """
with open("demo.txt", "w") as f:
    f.write("first\\n")
    f.write("second\\n")

with open("demo.txt") as f:
    print(repr(f.read()))
"""
            ),
            ask="Notice the backslash n in the writes. Why is it needed, when print does not need one?",
        ),
        dict(
            check="Because write does not add a line ending. print does.",
            teach="<p>And the mirror of that fact: a line READ from a file still carries its newline, so strip it before printing or comparing.</p>"
            + ran(
                """
with open("demo.txt", "w") as f:
    f.write("Ada\\nGrace\\n")

with open("demo.txt") as f:
    for line in f:
        print(repr(line), "stripped:", repr(line.strip()))
"""
            ),
            ask="Now exceptions. int(\"ten\") raises one. What is it called?",
        ),
        dict(
            check="A ValueError.",
            teach="<p>And dividing by zero raises a <b>ZeroDivisionError</b>. Catching them by name is what keeps a program alive without hiding real faults.</p>"
            + ran(
                """
try:
    print(int("ten"))
except ValueError:
    print("caught a ValueError")

try:
    print(1 / 0)
except ZeroDivisionError:
    print("caught a ZeroDivisionError")
"""
            ),
            ask="What is the difference between putting the success message in else and putting it at the end of try?",
        ),
        dict(
            check="Code in else runs only when nothing failed, and it is not itself guarded by the try.",
            teach="<p>So a mistake in the success line does not get swallowed by your except. And <b>finally</b> runs either way, which is where closing and cleaning up belongs. try, except, else, finally: that order, and one line each in the exam.</p>",
            ask="",
        ),
    ],
)
