# Topic Three: control flow, lists, tuples, sets, dictionaries. Loaded by csc241_doing.py.
M(
    "m3",
    kick="Topic Three",
    title="Learn by Doing: Topic Three",
    lead="Topic Three sat as a paper: the objective questions on control flow and the four containers, then two full written questions, each answered as you would write it and then taught from nothing.",
    minutes=90,
    intro="<p><b>The if ladder, for and while, the accumulator, and lists, tuples, sets and dictionaries.</b> The biggest topic on the paper, and the one every program question is built out of.</p>"
    "<div class=\"keypoint\"><span class=\"kplab\">How to sit this</span>"
    "<p><b>Part A</b> is the objective questions on this topic, the manual's own first.</p>"
    "<p><b>Part B</b> is two questions of 17.5 marks with five parts each: definitions, a listing to trace, and programs to write. Trace by hand, with a table of variables, and write the printed lines exactly.</p></div>"
    "<p><b>Every program question in this topic is one of three patterns:</b> the accumulator (a running total), the search (a best so far), and the counter (how many satisfy a test). Learn the three and you can write any of them.</p>",
    lockin=dict(
        big='"A for loop repeats a known number of times. A while loop repeats until a condition goes false, and something inside it must change that condition."',
        sub="An elif ladder stops at the first true test, so order it from the narrowest test outwards. A list can be changed, a tuple cannot, a set drops duplicates, a dictionary maps a key to a value.",
    ),
)

Q(
    "m3",
    heading="The if ladder, the two kinds of loop, and a program to write",
    marks="17.5 marks",
    scenario=dict(
        printed=False,
        tag="written for practice, in the shape the examiner sets",
        text="<p>Part (c) gives you a listing to trace by hand. The university grades a score of 70 and above as A, 60 to 69 as B, 50 to 59 as C, 45 to 49 as D, and anything below 45 as F.</p>"
        + show(
            """
total = 0
n = 1

while n <= 10:
    if n % 3 == 0:
        n = n + 1
        continue
    total = total + n
    n = n + 1

print(total, n)
""",
            "trace.py",
        ),
    ),
    asked="<table><tr><th>Part</th><th>What to write</th><th>Marks</th></tr>"
    "<tr><td>(a)</td><td>Explain the if, elif and else ladder, and state why the order of the tests matters</td><td>3</td></tr>"
    "<tr><td>(b)</td><td>What is a count controlled loop? How does it differ from a condition controlled loop? Give an example of each</td><td>3.5</td></tr>"
    "<tr><td>(c)</td><td>Write down exactly what the listing above prints, and explain what continue did</td><td>3</td></tr>"
    "<tr><td>(d)</td><td>Write a program that reads a score and prints the grade, rejecting a score outside 0 to 100</td><td>4</td></tr>"
    "<tr><td>(e)</td><td>Write a program that reads a number n and prints the sum of the even numbers from 1 to n, and how many there were</td><td>4</td></tr></table>",
    breakdown=dict(
        question="<p>In part (d), what goes wrong if you test for the lowest grade first? And in part (e), what are the three lines every accumulator program has?</p>",
        answer="<p class=\"row\"><b class=\"lab\">Order</b> An elif ladder stops at the FIRST true test. Test below 45 first and every score under 45 is caught, but a 90 falls through every test to the end. Start from one end and move steadily to the other, and never leave a gap.</p>"
        "<p class=\"row\"><b class=\"lab\">The accumulator</b> Three lines: set the total to zero BEFORE the loop, add to it INSIDE the loop, print it AFTER the loop. Put the initialisation inside the loop and it resets every pass.</p>"
        "<p class=\"row\"><b class=\"lab\">Validation</b> Part (d) says reject an impossible score, so one test comes before the ladder, not inside it.</p>"
        "<p class=\"row\"><b class=\"lab\">In (c)</b> continue jumps to the next pass of the loop, skipping the rest of the body. Since n is increased before it, the loop still ends.</p>",
    ),
    exam=dict(
        problem="<p>(a) The if, elif, else ladder and why order matters. (b) Count controlled against condition controlled loops. (c) Trace the listing and explain continue. (d) A grade program with validation. (e) A sum of even numbers program.</p>",
        answer="<p><b>(a) The if, elif and else ladder.</b> <code>if</code> tests a condition and runs its indented block when the condition is true. <code>elif</code> offers another test, tried only when every test above it was false. <code>else</code> has no test and runs when all of them were false. Each of those lines ends in a colon, and the block belonging to it is the indented lines under it.</p>"
        "<p><b>Why the order matters:</b> the ladder stops at the <b>first true test</b> and every branch below it is skipped. So the tests must be arranged so that the first one that can be true is the one you want. Written from the top down, a grade ladder must go from the highest boundary to the lowest, or a score of 90 would match a test for 45 and above and be graded D.</p>"
        + ran(
            """
score = 90

if score >= 45:
    print("wrong ladder says D")
elif score >= 70:
    print("A, never reached")

if score >= 70:
    print("right ladder says A")
elif score >= 45:
    print("D, not reached")
"""
        )
        + "<p><b>(b) The two kinds of loop.</b></p><table><tr><th></th><th>Count controlled</th><th>Condition controlled</th></tr>"
        "<tr><td>What it is</td><td>Repeats a KNOWN number of times, once for each item in a sequence</td><td>Repeats WHILE a condition stays true, however many times that turns out to be</td></tr>"
        "<tr><td>Written with</td><td><code>for</code>, usually over <code>range()</code> or a list</td><td><code>while</code></td></tr>"
        "<tr><td>The risk</td><td>Off by one: range stops one before its second number</td><td>An infinite loop, if nothing inside changes the condition</td></tr>"
        "</table>"
        + ran(
            """
for i in range(1, 6):
    print("count controlled", i)

n = 1
while n * n < 20:
    print("condition controlled", n, n * n)
    n = n + 1
"""
        )
        + "<p>The for loop runs exactly five times, decided before it starts. The while loop runs until the square reaches 20, which you would have to work out, and <b>the line that changes n is what makes it end</b>.</p>"
        "<p><b>(c) The trace.</b></p>"
        + ran(
            """
total = 0
n = 1

while n <= 10:
    if n % 3 == 0:
        n = n + 1
        continue
    total = total + n
    n = n + 1

print(total, n)
"""
        )
        + "<p>The loop adds every number from 1 to 10 except the multiples of three, which are 3, 6 and 9. The numbers added are 1, 2, 4, 5, 7, 8 and 10, giving 37, and the loop leaves n at 11, which is the value that failed the test.</p>"
        "<p><b>What continue did:</b> it abandoned the rest of that pass and jumped straight to the next test of the condition, so the line that adds to the total was skipped for 3, 6 and 9. Note the deliberate detail: n is increased BEFORE the continue. Had it not been, n would have stayed at 3 forever and the program would never end.</p>"
        "<p><b>(d) The grade program.</b></p>"
        + ran(
            """
score = int(input("Score: "))

if score < 0 or score > 100:
    print("Invalid score. It must be between 0 and 100.")
else:
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
    print(f"Score {score} is grade {grade}")
""",
            stdin="64",
            name="grade.py",
        )
        + "<p>Validation first, in its own test, then the ladder from the highest boundary down. Because each elif is only reached when the ones above failed, no upper bound is needed in the tests: by the time <code>score &gt;= 60</code> is reached, the score is already known to be under 70.</p>"
        "<p><b>(e) The sum of the even numbers.</b></p>"
        + ran(
            """
n = int(input("n: "))

total = 0
count = 0

for number in range(1, n + 1):
    if number % 2 == 0:
        total = total + number
        count = count + 1

print(f"The {count} even numbers up to {n} add up to {total}")
""",
            stdin="10",
            name="evens.py",
        )
        + "<p>This is the accumulator and the counter in one program: both are set to zero before the loop, both are updated inside it, and both are printed after it. Note <code>range(1, n + 1)</code>: range stops one before its second number, so the plus one is what makes n itself count.</p>",
    ),
    frames=[
        dict(
            check="",
            teach="<p>An <b>if</b> runs a block when a test is true. Add <b>elif</b> and you get a ladder of tests, and Python tries them from the top and stops at the first true one.</p>",
            ask="If the ladder stops at the first true test, what happens to a score of 90 in a ladder that tests 45 and above first?",
        ),
        dict(
            check="It is graded D, because that test is true and everything below it is skipped.",
            teach="<p>That is why <b>order is part of the answer</b>. Grades go from the highest boundary down. And because a lower branch is only reached when the ones above failed, you never need an upper bound in the test.</p>",
            ask="What does else do, and what happens if you leave it out?",
        ),
        dict(
            check="It runs when every test failed. Without it, nothing runs at all in that case.",
            teach="<p>Which is how a grade program silently prints nothing for a score nobody thought about. Now loops. A <b>for</b> loop repeats a known number of times, once per item.</p>"
            + ran("for i in range(1, 4):\n    print(i)"),
            ask="range(1, 4) printed 1, 2, 3. What is the rule, and what does range(1, n + 1) give you?",
        ),
        dict(
            check="range stops one before its second number, so range(1, n + 1) runs from 1 to n inclusive.",
            teach="<p>That plus one is the single most common off by one in the paper. Now the other loop: <b>while</b> repeats as long as a condition holds, and nobody knows in advance how many passes that is.</p>"
            + ran("n = 1\nwhile n * n < 20:\n    print(n, n * n)\n    n = n + 1"),
            ask="Delete the last line of that loop. What happens, and what is it called?",
        ),
        dict(
            check="It never ends: an infinite loop.",
            teach="<p>So the rule for every while loop you write: <b>something inside the body must move the condition towards false</b>. That is also why the listing in part (c) increases n before its continue.</p>",
            ask="What does continue do, and how is it different from break?",
        ),
        dict(
            check="continue skips the rest of this pass and goes to the next. break leaves the loop entirely.",
            teach="<p>Now the pattern behind part (e), the <b>accumulator</b>: a total set to zero BEFORE the loop, added to INSIDE it, printed AFTER it. A counter is the same pattern adding one instead of a value.</p>"
            + ran(
                """
total = 0
count = 0
for number in range(1, 11):
    if number % 2 == 0:
        total += number
        count += 1
print(count, total)
"""
            ),
            ask="Move total = 0 inside the loop. What does the program print then, and why?",
        ),
        dict(
            check="10, because the total is wiped at the start of every pass and only the last even number survives.",
            teach="<p>Initialise before, update inside, print after. Those three positions are the whole pattern, and every program question in this topic is that pattern with a different test in the middle.</p>",
            ask="",
        ),
    ],
)

Q(
    "m3",
    heading="Lists, tuples, sets and dictionaries, and marks to analyse",
    marks="17.5 marks",
    scenario=dict(
        printed=False,
        tag="written for practice, in the shape the examiner sets",
        text="<p>Part (c) gives you a listing to trace. Parts (d) and (e) are programs to write.</p>"
        + show(
            """
scores = [45, 62, 70, 38]
copy = scores
copy.append(90)

names = ("ada", "grace")
words = "the cat sat on the mat".split()

print(scores)
print(len(names), len(set(words)))
""",
            "trace.py",
        ),
    ),
    asked="<table><tr><th>Part</th><th>What to write</th><th>Marks</th></tr>"
    "<tr><td>(a)</td><td>Compare a list, a tuple, a set and a dictionary: how each is written, whether it can be changed, and what it is for</td><td>4</td></tr>"
    "<tr><td>(b)</td><td>Explain five list operations, with an example of each</td><td>3</td></tr>"
    "<tr><td>(c)</td><td>Write down exactly what the listing prints, and explain the first line of output</td><td>3.5</td></tr>"
    "<tr><td>(d)</td><td>Write a program that reads five marks into a list and prints the average, the highest, and how many are above the average</td><td>4</td></tr>"
    "<tr><td>(e)</td><td>Write a program that counts how many times each word appears in a sentence, using a dictionary</td><td>3</td></tr></table>",
    breakdown=dict(
        question="<p>The first line of output in part (c) catches most people. What does copy = scores actually copy, and how would you make a real copy?</p>",
        answer="<p class=\"row\"><b class=\"lab\">What it copies</b> Nothing. It makes a second NAME for the same list, so appending through one name shows up through the other. That is aliasing.</p>"
        "<p class=\"row\"><b class=\"lab\">A real copy</b> <code>copy = scores[:]</code> or <code>copy = list(scores)</code>, either of which builds a new list.</p>"
        "<p class=\"row\"><b class=\"lab\">Why it only bites here</b> A list is MUTABLE. Aliasing a tuple or a string is harmless, because neither can be changed in place.</p>"
        "<p class=\"row\"><b class=\"lab\">The set in the last line</b> The sentence has six words but only five different ones, because the repeats collapse. That is what a set is for.</p>",
    ),
    exam=dict(
        problem="<p>(a) List, tuple, set and dictionary compared. (b) Five list operations. (c) Trace the listing and explain its first line. (d) A program for average, highest and count above average. (e) A word frequency program.</p>",
        answer="<p><b>(a) The four containers.</b></p><table><tr><th></th><th>Written</th><th>Changeable</th><th>What it is for</th></tr>"
        "<tr><td><b>List</b></td><td>Square brackets, comma separated</td><td>Yes, mutable</td><td>An ordered collection you will add to, remove from or sort. The default choice</td></tr>"
        "<tr><td><b>Tuple</b></td><td>Round brackets</td><td>No, immutable</td><td>A fixed group of related values, such as a coordinate or a record that must not change. It can be a dictionary key, which a list cannot</td></tr>"
        "<tr><td><b>Set</b></td><td>Curly braces of values, or <code>set()</code></td><td>Yes, but it holds no duplicates and no order</td><td>Membership and uniqueness: removing duplicates, or asking whether something is present</td></tr>"
        "<tr><td><b>Dictionary</b></td><td>Curly braces of key colon value</td><td>Yes</td><td>Looking a value up BY A KEY rather than by position, such as a name to a mark</td></tr>"
        "</table>"
        + ran(
            """
marks = [45, 62, 70]
point = (3, 4)
unique = {"a", "b", "a"}
ages = {"ada": 36, "grace": 45}

print(marks, point, sorted(unique), ages["grace"])
print(type(marks), type(point), type(unique), type(ages))
"""
        )
        + "<p><b>(b) Five list operations.</b></p><table><tr><th>Operation</th><th>What it does</th><th>Example</th></tr>"
        "<tr><td><code>append(x)</code></td><td>Adds one item to the end</td><td>a list of three becomes four</td></tr>"
        "<tr><td><code>insert(i, x)</code></td><td>Puts an item at position i and shifts the rest along</td><td>insert at 0 makes it the new first item</td></tr>"
        "<tr><td><code>remove(x)</code></td><td>Removes the FIRST item equal to x, and raises a ValueError if there is none</td><td>removes a value by what it is</td></tr>"
        "<tr><td><code>pop(i)</code></td><td>Removes the item at position i and RETURNS it. With no argument it takes the last one</td><td>removes a value by where it is</td></tr>"
        "<tr><td><code>sort()</code></td><td>Sorts the list IN PLACE and returns nothing. <code>sorted(list)</code> returns a new sorted list instead</td><td>ascending by default, descending with reverse set to true</td></tr>"
        "</table>"
        + ran(
            """
marks = [45, 62, 70]
marks.append(38)
marks.insert(0, 99)
marks.remove(62)
taken = marks.pop()
marks.sort()
print(marks, "popped", taken)
print(sorted(marks, reverse=True))
"""
        )
        + "<p>The pair worth naming: <code>remove</code> takes a VALUE, <code>pop</code> takes a POSITION and hands the item back. And <code>sort()</code> returns None, so <code>marks = marks.sort()</code> destroys the list, which is a favourite objective question.</p>"
        "<p><b>(c) The trace.</b></p>"
        + ran(
            """
scores = [45, 62, 70, 38]
copy = scores
copy.append(90)

names = ("ada", "grace")
words = "the cat sat on the mat".split()

print(scores)
print(len(names), len(set(words)))
"""
        )
        + "<p><b>The first line explained.</b> <code>copy = scores</code> did not copy the list. It gave the same list a second name, so appending through <code>copy</code> changed the one and only list, and printing <code>scores</code> shows the 90. This is <b>aliasing</b>, and it only matters for mutable containers. To take a real copy use <code>scores[:]</code> or <code>list(scores)</code>.</p>"
        "<p>The second line: the tuple holds two names, and the sentence has six words of which five are different, since the repeated word collapses in the set.</p>"
        "<p><b>(d) The marks program.</b></p>"
        + ran(
            """
marks = []

for i in range(1, 6):
    mark = float(input(f"Mark {i}: "))
    marks.append(mark)

average = sum(marks) / len(marks)
highest = max(marks)

above = 0
for mark in marks:
    if mark > average:
        above += 1

print(f"Average: {average:.2f}")
print(f"Highest: {highest}")
print(f"Above average: {above}")
""",
            stdin="45\n62\n70\n38\n55",
            name="marks.py",
        )
        + "<p>Read into a list with append inside a count controlled loop, then let the built ins do the work: <code>sum()</code>, <code>len()</code> and <code>max()</code>. The count above the average needs its own loop, because the average is not known until every mark is in.</p>"
        "<p><b>(e) The word count.</b></p>"
        + ran(
            """
sentence = input("Sentence: ")
words = sentence.lower().split()

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

for word, times in counts.items():
    print(f"{word}: {times}")
""",
            stdin="the cat sat on the mat",
            name="wordcount.py",
        )
        + "<p>The line that carries the marks is <code>counts.get(word, 0) + 1</code>: <code>get</code> returns the value for a key, or the default you give it when the key is absent, which is what saves you writing an if to test whether the word is already there. Indexing a missing key with square brackets would raise a <b>KeyError</b> instead. <code>items()</code> then walks the dictionary as key and value pairs.</p>",
    ),
    frames=[
        dict(
            check="",
            teach="<p>Four containers, and the exam asks you to tell them apart. A <b>list</b> is ordered and changeable, in square brackets. A <b>tuple</b> is ordered and fixed, in round ones.</p>"
            + ran("marks = [45, 62]\npoint = (3, 4)\nmarks.append(70)\nprint(marks, point)"),
            ask="Why would a language offer a container you are not allowed to change?",
        ),
        dict(
            check="Because some groups of values should not change: a coordinate, a date, a record.",
            teach="<p>And because being unchangeable makes a tuple usable as a <b>dictionary key</b>, which a list can never be. Next: a <b>set</b> holds no duplicates and no order, and a <b>dictionary</b> maps a key to a value.</p>"
            + ran('print(set("the cat sat on the mat".split()))\nprint({"ada": 36}["ada"])'),
            ask="A sentence of six words gave a set of five. What does that tell you a set is for?",
        ),
        dict(
            check="Uniqueness: removing duplicates, or asking whether something is present.",
            teach="<p>Now the trap in this topic. Watch what happens when one list is given a second name and then changed.</p>"
            + ran("scores = [45, 62]\ncopy = scores\ncopy.append(90)\nprint(scores)"),
            ask="The original changed. Why, and how would you make a copy that does not do this?",
        ),
        dict(
            check="Because both names point at the same list. A real copy is scores[:] or list(scores).",
            teach="<p>That is <b>aliasing</b>, and it only bites on mutable containers: you cannot do it to a tuple or a string, because neither can be changed in place.</p>",
            ask="Now the list methods. Which one takes a value, and which takes a position and hands the item back?",
        ),
        dict(
            check="remove takes a value, pop takes a position and returns the item.",
            teach="<p>Plus append to add at the end, insert to add at a position, and sort to sort in place. Sort's return value is the one to remember, because it is a favourite question.</p>"
            + ran("marks = [62, 45, 70]\nprint(marks.sort())\nprint(marks)\nprint(sorted([62, 45, 70], reverse=True))"),
            ask="So what does marks = marks.sort() leave you with?",
        ),
        dict(
            check="None. The list is gone.",
            teach="<p>sort changes the list and returns nothing; <code>sorted()</code> leaves the list alone and returns a new one. Last piece: counting with a dictionary.</p>"
            + ran(
                """
counts = {}
for word in "the cat the".split():
    counts[word] = counts.get(word, 0) + 1
print(counts)
"""
            ),
            ask="Why use get here rather than counts[word] + 1?",
        ),
        dict(
            check="Because the first time a word appears it is not in the dictionary yet, and indexing a missing key raises a KeyError.",
            teach="<p><code>get(key, default)</code> returns the default instead of failing, so the first occurrence starts from zero. That one line is the whole word frequency program, and it is worth memorising exactly.</p>",
            ask="",
        ),
    ],
)
