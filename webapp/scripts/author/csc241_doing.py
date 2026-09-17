"""Learn by doing, CSC241: the theory questions for each module, run and verified.

    python scripts/author/csc241_doing.py

Writes data/csc241/doing/m1.json to m5.json, which scripts/build-doing.mjs turns
into the five papers. Part A of each paper, the objective questions, is chosen by
that script from the bank; this file is Part B, the questions you write out.

Every listing here is EXECUTED, by the same highlighter and runner the makeup
manual uses, and the output printed under it is what Python actually printed. A
model answer that claims an output it was never run to produce is the one kind of
mistake this course cannot afford, so a program that fails stops the build.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WEBAPP = HERE.parent.parent
REPO = WEBAPP.parent
TOOLS = REPO / "courses" / "CSC241 - Python Programming Language I" / "makeup" / "tools"
sys.path.insert(0, str(TOOLS))
import hl_py  # noqa: E402

OUT = WEBAPP / "data" / "csc241" / "doing"

MODULES = {}


def M(key, **kw):
    MODULES[key] = dict(questions=[], **kw)


def Q(key, **kw):
    MODULES[key]["questions"].append(kw)


def lab(name):
    return f'<div class="codelabel">{name}</div>'


def show(src, name=None):
    """A listing, highlighted, not run: for code whose output is a window."""
    return (lab(name) if name else "") + hl_py.listing(src.strip("\n"))


def ran(src, stdin="", name=None, expect=None):
    """A listing plus what Python actually printed when it was run."""
    src = src.strip("\n")
    out = hl_py.run(src, stdin)
    if expect is not None and out.rstrip() != expect.rstrip():
        raise SystemExit(f"listing {name or ''} printed {out!r}, not the expected {expect!r}")
    return (lab(name) if name else "") + hl_py.listing(src) + hl_py.output(out)


def out_of(src, stdin=""):
    """Just what a program printed, for questions that ask you to trace it."""
    return hl_py.run(src, stdin).rstrip("\n")


# =============================================================== Module One
M(
    "m1",
    kick="Topic One",
    title="Learn by Doing: Topic One",
    lead="Topic One sat as a paper: every objective question this topic has, then the written questions, each answered as you would write it and then taught from nothing.",
    minutes=55,
    intro="<p><b>What Python is, how a program runs, indentation, print and input.</b> The smallest topic on the paper, and the one that decides whether the rest of your answers even run.</p>"
    "<div class=\"keypoint\"><span class=\"kplab\">How to sit this</span>"
    "<p><b>Part A</b> is every objective question in the bank on this topic, each with every option explained as you answer.</p>"
    "<p><b>Part B</b> is the written questions. Write the code in your book by hand first, then open <b>Part 1</b>, the answer as you would write it in the hall. <b>Part 2</b> then teaches the same question from nothing.</p></div>"
    "<p><b>Marks do not come from running code in the exam,</b> they come from the code on the page, so practise writing it by hand, indentation and colons and all.</p>",
    lockin=dict(
        big='"A Python program runs top to bottom, line by line. A colon opens a block, and the indentation under it IS the block."',
        sub="print writes, input reads and always returns a string, and int() or float() is what makes it a number.",
    ),
)

Q(
    "m1",
    heading="What Python is, and a program that will not run",
    marks="10 marks",
    scenario=dict(
        printed=False,
        tag="written for practice, in the shape the examiner sets",
        text="<p>A student submits the program below. It is meant to ask for a name and an age, then print a greeting and the age next year. It does not run.</p>"
        + show(
            """
name = input("Enter your name: ")
age = input("Enter your age: ")
if age > 17
print("Hello " name)
print("Next year you will be", age + 1)
""",
            "student.py",
        ),
    ),
    asked="<table><tr><th>Part</th><th>What to write</th><th>Marks</th></tr>"
    "<tr><td>(a)</td><td>What is Python? State four features of the language</td><td>3</td></tr>"
    "<tr><td>(b)</td><td>Explain how a Python program is executed, and how that differs from a compiled language</td><td>2</td></tr>"
    "<tr><td>(c)</td><td>Identify the errors in the program above, saying what is wrong with each line</td><td>3</td></tr>"
    "<tr><td>(d)</td><td>Rewrite it so that it works</td><td>2</td></tr></table>",
    breakdown=dict(
        question="<p>There are four separate faults in five lines, and two of them are the same kind of fault. Find all four before you read on, and say which one Python reports first.</p>",
        answer="<p class=\"row\"><b class=\"lab\">Fault one</b> The if line has no colon, so the block never opens. Python reports this first, as a SyntaxError, and stops: nothing else runs.</p>"
        "<p class=\"row\"><b class=\"lab\">Fault two</b> The two print lines are not indented under the if, so even with a colon the block would be empty.</p>"
        "<p class=\"row\"><b class=\"lab\">Fault three</b> Two values sit side by side inside print with nothing between them, neither a comma nor a plus.</p>"
        "<p class=\"row\"><b class=\"lab\">Fault four</b> age came from input, so it is a STRING. Comparing it with 17 and adding 1 to it both fail, and the fix is int().</p>"
        "<p class=\"row\"><b class=\"lab\">Marks</b> Part (c) is three marks for four faults, so name them in a list, one line each, and do not explain at length.</p>",
    ),
    exam=dict(
        problem="<p>(a) What is Python, with four features. (b) How a Python program is executed, against a compiled language. (c) The errors in the student's program. (d) A corrected version.</p>",
        answer="<p><b>(a) What Python is.</b> Python is a high level, general purpose programming language that is <b>interpreted</b> rather than compiled, and it is designed to be readable.</p>"
        "<p>Four features:</p><ol>"
        "<li><b>Interpreted:</b> the source is executed line by line by the Python interpreter, with no separate compile step.</li>"
        "<li><b>Dynamically typed:</b> a variable takes the type of whatever is assigned to it, so no type is declared.</li>"
        "<li><b>Readable, indentation defined syntax:</b> blocks are marked by indentation rather than by braces, so the layout is the structure.</li>"
        "<li><b>Cross platform, with a large standard library:</b> the same program runs on Windows, Linux or macOS, and modules such as math, random and sqlite3 ship with it.</li>"
        "</ol><p>Others that earn the mark: free and open source, supports several paradigms, and can be extended with modules.</p>"
        "<p><b>(b) How it is executed.</b> Python runs a program <b>top to bottom, one statement at a time</b>. The interpreter reads a statement, executes it, then moves to the next, so a line that has not been reached has not run, and a name must be defined before the line that uses it.</p>"
        "<p>A compiled language such as C is translated, whole, into machine code by a compiler before it is run, and the program you run is the translated file. Two consequences the examiner looks for: a compiled language catches many errors before the program ever runs, while Python reports most of them only when the line is reached; and Python must be installed to run the source, while a compiled binary runs on its own.</p>"
        "<p>One exception worth a mark: a syntax error is found when the file is first parsed, before any line runs at all, which is exactly what happens in part (c).</p>"
        "<p><b>(c) The errors.</b></p><table><tr><th>Line</th><th>Error</th></tr>"
        "<tr><td>3</td><td><b>No colon</b> at the end of the if statement. A statement that opens a block must end in a colon, so this is a SyntaxError and the program does not start.</td></tr>"
        "<tr><td>4 and 5</td><td><b>No indentation.</b> The body of the if must be indented under it. As written, the if has an empty body and the prints are not part of it.</td></tr>"
        "<tr><td>4</td><td><b>Two values with nothing between them</b> inside print: <code>\"Hello \" name</code>. It needs a comma, or a plus to join the strings, or an f-string.</td></tr>"
        "<tr><td>2, then 3 and 5</td><td><b>age is a string,</b> because input always returns a string. So <code>age &gt; 17</code> compares a string with an integer, which raises a TypeError, and <code>age + 1</code> tries to add an integer to a string, which raises a TypeError too.</td></tr>"
        "</table><p><b>(d) The corrected program.</b></p>"
        + ran(
            """
name = input("Enter your name: ")
age = int(input("Enter your age: "))

if age > 17:
    print("Hello", name)
    print("Next year you will be", age + 1)
""",
            stdin="Ada\n19",
            name="fixed.py",
        )
        + "<p>The conversion is done once, on the way in, which is the habit to keep: read with input, convert immediately with int or float, and the rest of the program can then do arithmetic without thinking about it.</p>",
    ),
    frames=[
        dict(
            check="",
            teach="<p>Python runs a file from the top, one statement at a time. Nothing is set up in advance: a name exists only after the line that assigns it has run.</p>",
            ask="So what happens if line 5 uses a variable first created on line 7?",
        ),
        dict(
            check="It fails, because the name does not exist yet when line 5 runs.",
            teach="<p>That is a <b>NameError</b>. It is the first consequence of top to bottom execution, and it is why the order of lines is part of the answer in every program question.</p>",
            ask="Next: what does input() hand back, whatever the user types?",
        ),
        dict(
            check="A string. Always.",
            teach="<p>Type <code>19</code> and you get the string <code>\"19\"</code>, not the number 19. So <code>int()</code> or <code>float()</code> has to convert it before any arithmetic or comparison.</p>"
            + ran(
                """
age = input("Age: ")
print(type(age))
age = int(age)
print(type(age), age + 1)
""",
                stdin="19",
            ),
            ask="Now look at the student's line 3: if age > 17. What does that raise, and why?",
        ),
        dict(
            check="A TypeError: it compares a string with an integer.",
            teach="<p>Except it never gets that far, because line 3 has a worse problem: <b>no colon</b>. A statement that opens a block, if, elif, else, for, while, def, try, ends in a colon, and a SyntaxError is found before any line runs.</p>",
            ask="What has to be true of the lines that belong to that if?",
        ),
        dict(
            check="They must be indented under it, all by the same amount.",
            teach="<p>In Python the <b>indentation IS the block</b>. Four spaces is the convention. Indent by a different amount within one block and you get an IndentationError, and mix tabs with spaces and you get one too.</p>",
            ask="Last fault. What is wrong with print(\"Hello \" name)?",
        ),
        dict(
            check="Two values sit next to each other with nothing joining them.",
            teach="<p>Three ways to fix it, and all earn the mark:</p>"
            + ran(
                """
name = "Ada"
print("Hello", name)
print("Hello " + name)
print(f"Hello {name}")
""",
            )
            + "<p>The comma prints a space between the items. The plus joins two strings and fails if one is a number. The f-string is the one to use when text and values mix.</p>",
            ask="",
        ),
    ],
)

Q(
    "m1",
    heading="Reading input, converting it, and printing a result",
    marks="10 marks",
    scenario=dict(
        printed=False,
        tag="written for practice, in the shape the examiner sets",
        text="<p>A campus printing shop charges 20 naira a page for black and white, and 50 naira a page for colour. A student brings a job with some of each.</p>",
    ),
    asked="<table><tr><th>Part</th><th>What to write</th><th>Marks</th></tr>"
    "<tr><td>(a)</td><td>State the difference between a keyword, an identifier and a literal, with one example of each</td><td>3</td></tr>"
    "<tr><td>(b)</td><td>Write a program that reads the number of black and white pages and the number of colour pages, then prints the cost of each and the total</td><td>5</td></tr>"
    "<tr><td>(c)</td><td>Show what your program prints for 10 black and white pages and 3 colour pages</td><td>2</td></tr></table>",
    breakdown=dict(
        question="<p>Which two lines of this program carry all five marks in part (b), and what does part (c) want that most students forget to supply?</p>",
        answer="<p class=\"row\"><b class=\"lab\">The two lines</b> The input lines, wrapped in int(). If the conversion is missing, the multiplication silently repeats a string instead of costing anything, and the program is wrong without crashing.</p>"
        "<p class=\"row\"><b class=\"lab\">Part (c)</b> The actual printed lines, exactly as they would appear, prompts included. Write the output as a block, not as a sentence describing it.</p>"
        "<p class=\"row\"><b class=\"lab\">Worth a mark cheaply</b> Formatting money to two decimal places with an f-string, and labelling each figure.</p>",
    ),
    exam=dict(
        problem="<p>(a) Keyword, identifier and literal, with examples. (b) A program that reads black and white and colour page counts and prints each cost and the total. (c) Its output for 10 and 3.</p>",
        answer="<p><b>(a) The three terms.</b></p><table><tr><th>Term</th><th>What it is</th><th>Example</th></tr>"
        "<tr><td>Keyword</td><td>A word reserved by the language itself, which cannot be used as a name</td><td><code>if</code>, <code>for</code>, <code>def</code>, <code>while</code>, <code>True</code></td></tr>"
        "<tr><td>Identifier</td><td>A name the programmer gives to a variable, function, class or module. It may contain letters, digits and underscores, may not begin with a digit, and is case sensitive</td><td><code>bw_pages</code>, <code>total_cost</code></td></tr>"
        "<tr><td>Literal</td><td>A fixed value written directly in the code</td><td><code>20</code>, <code>50.0</code>, <code>\"colour\"</code>, <code>True</code></td></tr>"
        "</table><p><b>(b) The program.</b></p>"
        + ran(
            """
BW_RATE = 20
COLOUR_RATE = 50

bw = int(input("Black and white pages: "))
colour = int(input("Colour pages: "))

bw_cost = bw * BW_RATE
colour_cost = colour * COLOUR_RATE
total = bw_cost + colour_cost

print(f"Black and white: {bw} pages at {BW_RATE} naira = {bw_cost:.2f}")
print(f"Colour: {colour} pages at {COLOUR_RATE} naira = {colour_cost:.2f}")
print(f"Total: {total:.2f}")
""",
            stdin="10\n3",
            name="printing.py",
        )
        + "<p><b>(c) The output</b> is the block above, produced by running it with 10 and 3. Note three things the examiner can see at a glance: the rates are named constants rather than numbers buried in the arithmetic, both inputs are converted with int on the way in, and the money is formatted to two decimal places with <code>:.2f</code>.</p>",
    ),
    frames=[
        dict(
            check="",
            teach="<p>Every program of this kind has the same three phases: <b>read the input, do the arithmetic, print the result</b>. Write them in that order and leave a blank line between them, and the examiner can follow it without effort.</p>",
            ask="What should the first two lines of this program do?",
        ),
        dict(
            check="Read the two page counts.",
            teach="<p>And convert them. <code>int(input(\"Colour pages: \"))</code> does both in one line: the prompt goes inside input, and int makes it a number.</p>",
            ask="Suppose you forget the int. The program still runs. What does colour * 50 give you then?",
        ),
        dict(
            check="The string repeated 50 times.",
            teach="<p>That is the quiet failure worth knowing: <code>\"3\" * 50</code> is legal Python and prints 3 fifty times. No crash, no cost, no marks.</p>"
            + ran(
                """
pages = "3"
print(pages * 5)
print(int(pages) * 5)
""",
            ),
            ask="Now the rates, 20 and 50. Where should they live?",
        ),
        dict(
            check="In named constants at the top.",
            teach="<p><code>BW_RATE = 20</code> in capitals is the convention for a value that does not change. It costs one line and it makes the arithmetic read as a sentence: <code>bw * BW_RATE</code>.</p>",
            ask="Last piece: how do you print a number to exactly two decimal places?",
        ),
        dict(
            check="With an f-string and a format specifier.",
            teach="<p><code>f\"Total: {total:.2f}\"</code>. The name goes in the braces, then a colon, then the format. <code>.2f</code> means fixed point, two decimals, which is what money needs.</p>"
            + ran(
                """
total = 350
print(f"Total: {total:.2f}")
print(f"Half: {total / 3:.2f}")
""",
            ),
            ask="",
        ),
    ],
)


# The rest of the content lives one file per topic, loaded into this namespace so
# each file can call M and Q and the verified listing helpers without an import
# cycle. Every listing in them runs when this line does.
for part in ("m2", "m3", "m4", "m5"):
    exec((HERE / f"csc241_doing_{part}.py").read_text(encoding="utf-8"), globals())


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for key, mod in MODULES.items():
        path = OUT / f"{key}.json"
        path.write_text(json.dumps(mod, indent=2, ensure_ascii=False) + chr(10), encoding="utf-8")
        frames = sum(len(q["frames"]) for q in mod["questions"])
        print(f"  {key}: {len(mod['questions'])} questions, {frames} frames -> {path.name}")
    print(f"  {len(MODULES)} topic papers written, every listing run")


if __name__ == "__main__":
    build()
