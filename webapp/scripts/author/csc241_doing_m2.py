# Topic Two: types, operators, strings, finding errors. Loaded by csc241_doing.py.
M(
    "m2",
    kick="Topic Two",
    title="Learn by Doing: Topic Two",
    lead="Topic Two sat as a paper: the objective questions on types, operators and strings, then two full written questions in the paper's own shape, each answered and then taught from nothing.",
    minutes=85,
    intro="<p><b>Types and conversion, every operator and what it returns, slicing and the string methods.</b> This topic and the next carry most of the paper.</p>"
    "<div class=\"keypoint\"><span class=\"kplab\">How to sit this</span>"
    "<p><b>Part A</b> is the objective questions on this topic, the manual's own first, every option explained as you answer.</p>"
    "<p><b>Part B</b> is two questions of 17.5 marks, which is what one question on this paper is worth, with five parts each: theory, a listing to trace, a listing to fix, and a program to write. Do every one by hand first.</p></div>"
    "<p><b>The most common lost mark in this topic:</b> claiming an output you did not work out line by line. Trace with a table of variables, and write the printed lines exactly.</p>",
    lockin=dict(
        big='"Slash divides and gives a float, double slash floors, percent leaves the remainder, double star is the power. A string cannot be changed, only rebuilt."',
        sub="input returns a string. int of the string 3.5 is a ValueError. and returns an operand, not True or False. A slice excludes its stop index.",
    ),
)

Q(
    "m2",
    heading="The operators, conversion, and a listing to trace",
    marks="17.5 marks",
    scenario=dict(
        printed=False,
        tag="written for practice, in the shape the examiner sets",
        text="<p>The parts stand on their own. Part (c) gives you a listing to trace by hand.</p>"
        + show(
            """
a = 17
b = 5

print(a / b)
print(a // b)
print(a % b)
print(a ** 2)
print(a > b and a % 2 == 0)
print(a > b or a % 2 == 0)
""",
            "trace.py",
        ),
    ),
    asked="<table><tr><th>Part</th><th>What to write</th><th>Marks</th></tr>"
    "<tr><td>(a)</td><td>Explain the difference between the division, floor division, modulus and exponent operators, with an example of each</td><td>3.5</td></tr>"
    "<tr><td>(b)</td><td>What is type conversion? State what int of the string 3.5 does and why, and how to convert that string to a number correctly</td><td>3</td></tr>"
    "<tr><td>(c)</td><td>Write down exactly what the listing above prints, line by line</td><td>3.5</td></tr>"
    "<tr><td>(d)</td><td>Write a program that reads a number of seconds and prints it as hours, minutes and seconds</td><td>4.5</td></tr>"
    "<tr><td>(e)</td><td>Briefly describe how the and, or and not operators work in Python, with examples</td><td>3</td></tr></table>",
    breakdown=dict(
        question="<p>Two of these parts are the same skill in different clothes. Which two, and what single arithmetic fact answers both the second printed line and the whole of part (d)?</p>",
        answer="<p class=\"row\"><b class=\"lab\">The same skill</b> Part (c) and part (d). Both turn on what floor division and modulus actually give you.</p>"
        "<p class=\"row\"><b class=\"lab\">The fact</b> Floor division gives how many WHOLE times one number goes into another, and modulus gives what is LEFT OVER. Every conversion of a total into units uses the pair together.</p>"
        "<p class=\"row\"><b class=\"lab\">Watch in (c)</b> The first line prints 3.4, with a decimal point, because a single slash always returns a float, even when it divides exactly.</p>"
        "<p class=\"row\"><b class=\"lab\">Watch in (e)</b> and and or hand back one of their OPERANDS rather than True or False. Here both operands are already booleans, so booleans print, but the examiner may ask about zero or an empty string.</p>",
    ),
    exam=dict(
        problem="<p>(a) Division, floor division, modulus and exponent. (b) Type conversion, and int of the string 3.5. (c) Trace the listing. (d) A seconds to hours, minutes and seconds program. (e) How and, or and not work.</p>",
        answer="<p><b>(a) The four arithmetic operators.</b></p><table><tr><th>Operator</th><th>What it does</th><th>Example</th></tr>"
        "<tr><td><code>/</code> division</td><td>True division. <b>Always returns a float</b>, even when the division is exact</td><td><code>17 / 5</code> is 3.4, and <code>10 / 2</code> is 5.0</td></tr>"
        "<tr><td><code>//</code> floor division</td><td>Divides and throws the fraction away, giving how many whole times it goes in</td><td><code>17 // 5</code> is 3</td></tr>"
        "<tr><td><code>%</code> modulus</td><td>The remainder after that division</td><td><code>17 % 5</code> is 2</td></tr>"
        "<tr><td><code>**</code> exponent</td><td>Raises to a power. This is the power operator in Python, not the caret</td><td><code>17 ** 2</code> is 289</td></tr>"
        "</table>"
        + ran(
            """
print(17 / 5, 17 // 5, 17 % 5, 17 ** 2)
print(10 / 2, type(10 / 2))
"""
        )
        + "<p><b>(b) Type conversion.</b> Type conversion, or casting, is changing a value from one type to another with a built in function: <code>int()</code>, <code>float()</code>, <code>str()</code>, <code>bool()</code>. It matters most on input, because <b>input always returns a string</b>.</p>"
        "<p>Converting the string 3.5 with <code>int()</code> <b>raises a ValueError</b>. int will parse a string of digits, but it will not parse a decimal point: it neither rounds nor truncates a string. Convert to float first, then to int if a whole number is wanted:</p>"
        + ran(
            """
print(float("3.5"))
print(int(float("3.5")))
try:
    print(int("3.5"))
except ValueError as e:
    print("ValueError:", e)
"""
        )
        + "<p>Note that <code>int(3.5)</code>, on the NUMBER, is legal and gives 3: it truncates towards zero rather than rounding.</p>"
        "<p><b>(c) What the listing prints.</b></p>"
        + ran(
            """
a = 17
b = 5

print(a / b)
print(a // b)
print(a % b)
print(a ** 2)
print(a > b and a % 2 == 0)
print(a > b or a % 2 == 0)
"""
        )
        + "<p>Line by line: 3.4, because a single slash gives a float; 3, because floor division drops the fraction; 2, the remainder; 289, the power; then 17 is greater than 5, which is True, but 17 leaves a remainder of 1 when divided by 2, so the second test is False. <b>and</b> needs both, so False. <b>or</b> needs one, so True.</p>"
        "<p><b>(d) Seconds to hours, minutes and seconds.</b></p>"
        + ran(
            """
total = int(input("Seconds: "))

hours = total // 3600
minutes = (total % 3600) // 60
seconds = total % 60

print(f"{total} seconds is {hours} h {minutes} m {seconds} s")
""",
            stdin="7325",
            name="seconds.py",
        )
        + "<p>Learn the shape, not the numbers: <b>floor divide to take the whole units out, modulus to keep what is left</b>, then repeat on the remainder. The same three lines turn kobo into naira or pages into reams.</p>"
        "<p><b>(e) and, or and not.</b></p><table><tr><th>Operator</th><th>How it works</th></tr>"
        "<tr><td><code>and</code></td><td>True only if BOTH sides are true. It <b>short circuits</b>: if the left side is false, the right side is never evaluated. It returns the first falsy operand, or the last one when all are truthy</td></tr>"
        "<tr><td><code>or</code></td><td>True if EITHER side is true. It short circuits too: if the left side is true, the right is never evaluated. It returns the first truthy operand, or the last when all are falsy</td></tr>"
        "<tr><td><code>not</code></td><td>Reverses a truth value, so not True is False</td></tr>"
        "</table>"
        + ran(
            """
age = 20
print(age > 17 and age < 65)
print(age < 17 or age > 65)
print(not age > 17)
print(0 or "default")
print("given" and "second")
"""
        )
        + "<p>The last two lines are the detail that separates a full answer: zero or a default gives back the default itself, not True, because or hands back an operand. That is how a fallback value is written in one line.</p>",
    ),
    frames=[
        dict(
            check="",
            teach="<p>Start with the one that surprises people. In Python 3 a single slash is <b>true division</b>, and it always gives a float.</p>"
            + ran("print(10 / 2)\nprint(type(10 / 2))"),
            ask="So how do you divide and get a whole number, say the full hours inside 7325 seconds?",
        ),
        dict(
            check="Floor division, with a double slash.",
            teach="<p>7325 floor divided by 3600 is 2: two whole hours. Floor division answers HOW MANY WHOLE TIMES.</p>"
            + ran("print(7325 // 3600)\nprint(7325 % 3600)"),
            ask="The second line printed 125. What is that number, in words?",
        ),
        dict(
            check="What is left over after the two whole hours are taken out.",
            teach="<p>That is <b>modulus</b>. The pair works together: floor division takes the units out, modulus keeps the remainder, and you run the pair again on the remainder to get minutes and seconds.</p>",
            ask="Write the three lines that turn total seconds into hours, minutes and seconds.",
        ),
        dict(
            check="hours = total // 3600, then minutes = (total % 3600) // 60, then seconds = total % 60.",
            teach="<p>The brackets in the middle line matter: take the remainder first, then divide it by 60. Without them you divide the whole total again and report every minute in it.</p>"
            + ran(
                """
total = 7325
print((total % 3600) // 60, "correct minutes")
print(total // 60, "wrong: every minute in the total")
"""
            ),
            ask="Now conversion. What happens with int on the string 3.5, and what about int on the number 3.5?",
        ),
        dict(
            check="The string raises a ValueError. The number gives 3.",
            teach="<p>int parses a string of DIGITS only, so a decimal point in a string kills it: use <code>float()</code> first. On a number it truncates towards zero rather than rounding, so int of 3.9 is also 3.</p>",
            ask="Last part. Does zero or the word default give you True, or something else?",
        ),
        dict(
            check="The word default itself.",
            teach="<p>Because <b>or returns an operand, not a boolean</b>: the first truthy one. and is the mirror image, returning the first falsy one. Both short circuit, so the right hand side may never run. Say that in the exam and the three marks are yours.</p>",
            ask="",
        ),
    ],
)

Q(
    "m2",
    heading="Strings: what they are, slicing them, and a listing to fix",
    marks="17.5 marks",
    scenario=dict(
        printed=False,
        tag="written for practice, in the shape the examiner sets",
        text="<p>Part (b) uses <code>title = \"PYTHON PROGRAMMING\"</code>. Part (e) gives you a listing with three faults in it.</p>"
        + show(
            """
name = "ada lovelace"
name[0] = "A"
print(name.upper)
print("Length:" len(name))
""",
            "broken.py",
        ),
    ),
    asked="<table><tr><th>Part</th><th>What to write</th><th>Marks</th></tr>"
    "<tr><td>(a)</td><td>What is a string in Python? Explain what immutable means, and show what happens if you try to change one character</td><td>3.5</td></tr>"
    "<tr><td>(b)</td><td>For the title above, write down the value of these five slices: the first six characters, everything from position seven, the last eleven characters, every second character, and the whole thing backwards</td><td>4</td></tr>"
    "<tr><td>(c)</td><td>List and briefly explain four common string methods, with an example of each</td><td>4</td></tr>"
    "<tr><td>(d)</td><td>Write a program that reads a word and prints it reversed, with the number of vowels in it</td><td>4</td></tr>"
    "<tr><td>(e)</td><td>Identify the errors in the listing above</td><td>2</td></tr></table>",
    breakdown=dict(
        question="<p>Part (b) asks for five slices. What two rules answer all five, and what does a negative index mean?</p>",
        answer="<p class=\"row\"><b class=\"lab\">Rule one</b> A slice is start, stop, step. The <b>start is included and the stop is excluded</b>, so positions 0 to 6 give six characters, 0 to 5.</p>"
        "<p class=\"row\"><b class=\"lab\">Rule two</b> Leave a side out and it runs to the end of the string on that side: nothing before the colon means from the beginning, nothing after it means to the end.</p>"
        "<p class=\"row\"><b class=\"lab\">Negative index</b> Counts from the right, starting at minus one for the last character. A step of minus one walks the whole string backwards, which is how a string is reversed.</p>"
        "<p class=\"row\"><b class=\"lab\">Part (e)</b> Three faults, not two: assigning to a character, calling a method without its brackets, and two values inside print with nothing between them.</p>",
    ),
    exam=dict(
        problem="<p>(a) What a string is, and immutability. (b) Five slices of PYTHON PROGRAMMING. (c) Four string methods with examples. (d) A program printing a word reversed with its vowel count. (e) The errors in the listing.</p>",
        answer="<p><b>(a) What a string is.</b> A string is an <b>ordered, immutable sequence of characters</b>, written in single or double quotes. Being a sequence, it can be indexed, sliced and looped over, and <code>len()</code> gives its length.</p>"
        "<p><b>Immutable</b> means that once a string exists it cannot be changed in place. Anything that looks like a change actually builds and returns a NEW string and leaves the original alone. So assigning to one character is an error:</p>"
        + ran(
            """
name = "ada lovelace"
try:
    name[0] = "A"
except TypeError as e:
    print("TypeError:", e)

upper = name.upper()
print(upper)
print(name)
"""
        )
        + "<p>The last two lines prove it: upper returned a new string, and name is exactly as it was. To keep a change you must assign it back, as <code>name = name.upper()</code>.</p>"
        "<p><b>(b) The five slices.</b></p>"
        + ran(
            """
title = "PYTHON PROGRAMMING"
print(repr(title[0:6]))
print(repr(title[7:]))
print(repr(title[-11:]))
print(repr(title[::2]))
print(repr(title[::-1]))
"""
        )
        + "<p>In words: the first six characters, because the stop is excluded; everything from position seven to the end; the last eleven characters, counted from the right; every second character; and the whole string backwards.</p>"
        "<p><b>(c) Four string methods.</b></p><table><tr><th>Method</th><th>What it does</th><th>Example</th></tr>"
        "<tr><td><code>upper()</code></td><td>Returns a copy with every letter in upper case, and <code>lower()</code> is its mirror</td><td>ada becomes ADA</td></tr>"
        "<tr><td><code>strip()</code></td><td>Returns a copy with leading and trailing whitespace removed, which is what you do to anything a user typed</td><td>two spaces around ada become nothing</td></tr>"
        "<tr><td><code>replace(old, new)</code></td><td>Returns a copy with every occurrence of one substring replaced by another</td><td>2025 with 5 replaced by 6 becomes 2026</td></tr>"
        "<tr><td><code>split(sep)</code></td><td>Breaks the string into a LIST of pieces at each separator, or at whitespace if none is given. <code>join</code> does the reverse</td><td>a,b,c split on the comma becomes a list of three strings</td></tr>"
        "</table><p>Others that earn the mark: <code>find()</code>, <code>count()</code>, <code>startswith()</code>, <code>title()</code>, <code>isdigit()</code>. Every one of them <b>returns a new value and leaves the original alone</b>, which is immutability again.</p>"
        + ran(
            """
print("ada".upper(), "  ada  ".strip(), "2025".replace("5", "6"), "a,b,c".split(","))
"""
        )
        + "<p><b>(d) The program.</b></p>"
        + ran(
            """
word = input("Enter a word: ").strip()

reversed_word = word[::-1]

vowels = 0
for letter in word.lower():
    if letter in "aeiou":
        vowels += 1

print(f"Reversed: {reversed_word}")
print(f"Vowels: {vowels}")
""",
            stdin="Programming",
            name="word.py",
        )
        + "<p>Three habits on show: strip what the user typed, reverse with a slice rather than a loop, and lower the word before testing so a capital A still counts. <code>letter in \"aeiou\"</code> is the short way to ask whether a character is one of a set.</p>"
        "<p><b>(e) The errors in the listing.</b></p><table><tr><th>Line</th><th>Error</th></tr>"
        "<tr><td>2</td><td>It assigns to one character of a string. Strings are immutable, so this raises a TypeError. Build a new string instead, joining the new first letter to the rest with a slice</td></tr>"
        "<tr><td>3</td><td>The method has no brackets, so it prints the method object rather than calling it. It must be <code>name.upper()</code></td></tr>"
        "<tr><td>4</td><td>Two values inside print with nothing between them. It needs a comma</td></tr>"
        "</table>"
        + ran(
            """
name = "ada lovelace"
name = "A" + name[1:]
print(name.upper())
print("Length:", len(name))
""",
            name="fixed.py",
        ),
    ),
    frames=[
        dict(
            check="",
            teach="<p>A string is a <b>sequence</b>: its characters are in order and each has a position, counted from zero. So the first character sits at 0 and the sixth at 5.</p>"
            + ran('title = "PYTHON PROGRAMMING"\nprint(title[0], title[5], len(title))'),
            ask="What do you think position minus one gives, and why would a language bother with that?",
        ),
        dict(
            check="The last character. It saves you working out the length first.",
            teach="<p>Negative positions count from the right, starting at minus one. Now slicing, written start colon stop, where <b>start is included and stop is excluded</b>.</p>"
            + ran('title = "PYTHON PROGRAMMING"\nprint(repr(title[0:6]))\nprint(repr(title[7:]))'),
            ask="Six characters came out of 0 to 6, not seven. Why is the rule built that way?",
        ),
        dict(
            check="So the length of a slice is simply stop minus start.",
            teach="<p>And so that a slice up to six and a slice from six split a string with nothing lost and nothing repeated. A third number is the <b>step</b>, and a step of minus one walks backwards.</p>"
            + ran('title = "PYTHON"\nprint(repr(title[::2]))\nprint(repr(title[::-1]))'),
            ask="So what is the shortest way to reverse any string?",
        ),
        dict(
            check="Slice it with an empty start, an empty stop and a step of minus one.",
            teach="<p>Now the property that shapes the whole topic. Try to change a single character and Python refuses: a string is <b>immutable</b>.</p>"
            + ran(
                """
name = "ada"
try:
    name[0] = "A"
except TypeError as e:
    print("TypeError:", e)
"""
            ),
            ask="So what must upper() do, if it cannot change the string it was called on?",
        ),
        dict(
            check="Return a brand new string.",
            teach="<p>Every string method does. Which means calling upper on its own changes nothing: you have to <b>assign it back</b>. This is the most common lost mark in the topic.</p>"
            + ran(
                """
name = "ada"
name.upper()
print(name)
name = name.upper()
print(name)
"""
            ),
            ask="One more trap from that listing: what prints if you leave the brackets off a method call?",
        ),
        dict(
            check="The method object itself, not what it would have returned.",
            teach="<p>Brackets are what CALL a method. No brackets, no call, and no error either, which is exactly why it survives to the exam paper as a fault to spot.</p>",
            ask="",
        ),
    ],
)
