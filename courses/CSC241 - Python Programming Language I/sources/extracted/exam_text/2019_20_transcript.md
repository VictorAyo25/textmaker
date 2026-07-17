# CSC241 2019/2020 Exam Transcript

> **[sic]** This paper is filed under CSC241 (Python Programming Language I), but the printed header block reads **COURSE CODE: CSC213** and **COURSE TITLE: Structured Programming**. Transcribed as printed. The paper's content is entirely Python.

## Header

COVENANT UNIVERSITY
CANAANLAND, KM 10, IDIROKO ROAD
P.M.B 1023, OTA, OGUN STATE, NIGERIA

- **TITLE OF EXAMINATION:** B.SC. EXAMINATION
- **COLLEGE:** College of Science and Technology
- **DEPARTMENT:** Computer and Information Sciences
- **SESSION:** 2019/2020
- **COURSE CODE:** CSC213
- **COURSE TITLE:** Structured Programming
- **SEMESTER:** ALPHA
- **CREDIT UNIT:** 3
- **TIME:** 3 hours
- **INSTRUCTION:** Answer any **FOUR (4)** Questions

> **[handwritten]** A circled annotation appears to the right of the "TITLE OF EXAMINATION" line, reading `[illegible: 57]` or `[illegible: SS]`.

---

## Question 1

**a.** With the aid of examples, mention the **Five (5)** relational operators in Python  **[2.5Marks]**

**b.** Write an if-else statement that determines whether a variable called **MyValues** that accepts input from the user is outside the range of **11** to **57**. If the variable's value is outside this range it should display *"Invalid Points"*; Otherwise, it should display *"Valid Points."*  **[2 Marks]**

> **[handwritten]** Illegible marginal note to the right of the "MyValues" line, at the page edge: `[illegible]`.

**c.** What will the output of the following code display?  **[1 Mark]**

```python
values = ['A', 14, 601, '8B', 10]
print (values[1:3])
```

> **[sic]** The string literals in the printed paper use typographic/curly quotes (`'A'`, `'8B'`) rather than straight ASCII quotes, so the snippet as printed is not valid Python source.

**d.** Identify the Error(s) in the Following Code Segment  **[3 Marks]**

```python
def main():
    prod nums = ['V475', 'F987', 'Q143', 'R688']
    search = input('Enter a product number: ')
    if sarch in prod_nums:
    print(search, 'was found in the list'.)
    else:
    print(search, 'was not found in the list'.)
main()
```

> **[sic]** Errors are the point of this question and are transcribed verbatim: `prod nums` has a space instead of an underscore; `sarch` is a misspelling of `search`; the two `print` calls are not indented under the `if`/`else`; the dot is misplaced outside the string in `'was found in the list'.)` and `'was not found in the list'.)`.

> **[handwritten]** A hand-drawn closing curve/bracket is pencilled around the end of the line `print(search, 'was found in the list'.)`. The words `prod nums` and `sarch` are underlined by hand.

**e.** Design a program that uses a loop to build a list named **valid_numbers** that contains only the numbers between 0 and 100 from the numbers list below. The program should then determine and display the **maximum**, **total** and **average** of the values in the **valid_numbers** list.  **[9 Marks]**

```python
Numbers = [45, 13, 290, 105, -20, 2, 67, 17, -12, 51, 80]
```

> **[handwritten]** Extensive pencil working fills the lower half of page 1. Left column, largely illegible: `[illegible: clean = ... numbers ...]`, `[illegible: integers[]]`, `[illegible: for n in range (check +1)]`, `[illegible: max = 0]`. Right column: `for n in Numbers`, `if n in range (100)`, `[illegible: partial_num[] = n]`, `[illegible: s3 = ... len (valid_n)]`, `[illegible: for i in partial... n ...]`, `[illegible: numbers = n .]`, `[illegible: avg = ... len]`.

*Page 1 of 5*

---

## Question 2

**a.** What is a Boolean function in Python?  **[1 Mark]**

**b.** Write a statement that creates a dictionary containing the following key-value pairs:  **[2 Marks]**

```python
'CST'    :1
'CBSS'   :2
'CLDS'   :3
'COE'    :4
```

> **[sic]** The key literals are printed with typographic/curly quotes.

**c.** Write a loop that calculates the **Total** of the following series of numbers:  **[3.5Marks]**

1/50 + 2/49 + 3/48 + ... + 50/1

*(printed as a boxed mathematical expression with stacked fractions)*

**d.** Spot the Error(s) in the following Code Segment  **[3 Marks]**

```python
def main():
        outfile = openfile('citiesInNigeria.txt', 'r')
        outfile.write(Abuja\n)
        outfile.write(Paris\n)
        outfile.write(Kaduna\n)
outfile.closefile()
main()
```

> **[sic]** Errors are the point of this question and are transcribed verbatim: `openfile(...)` is not a Python builtin (should be `open`); the file is opened in `'r'` (read) mode but written to; the arguments to `write` (`Abuja\n`, `Paris\n`, `Kaduna\n`) are unquoted; `closefile()` is not a method (should be `close`); `outfile.closefile()` sits outside the function body, where `outfile` is not defined.

**e.** Assume a file named **HarvestNumbers.txt** containing an unspecified series of integer values exists on the computer's disk. Write a program that reads the numbers from the file and calculates the average of all the numbers.  **[8 Marks]**

> **[handwritten]** Sideways along the right edge of page 2 (bleed from the facing page): `Write a` / `separate` / `"username"` / `"David" and` / `OYEDEPO`.

---

## Question 3

**a.** Differentiate between a **Condition-Controlled** and **Counter-Controlled** loop? Mention and Show examples of each loop type.  **[2.5Marks]**

**b.** Write an **if** statement that adds **500** to a variable **first_1**, and adds **400** to the variable **second_2** if the values entered as input into variable **inputVar** is greater than **100**, otherwise, it deducts **300**, from **first_1** and **150** from **second_2**.  **[2 Marks]**

> **[sic]** The sentence is scrambled: the clause order ("adds 400 to the variable second_2 if the values entered ... is greater than 100") reads as printed and the comma placement in "deducts **300**, from **first_1**" is as printed.

**c.** Identify the Error(s) in the following lines of Code  **[3 Marks]**

```python
def main():
    name_list = []
    again == 'y'
    while again = 'y':
        name = input('Enter a name: ')
        Append the name to the list=list().name
        name_list.append(name)
        print('Do you want to add another name?')
        again = input('y = yes, anything else = no: ')
        print()
    print('Here are the names you entered.')
    for name in name_list:
    print(name)
main()
```

> **[sic]** Errors are the point of this question and are transcribed verbatim: `again == 'y'` uses the equality operator where assignment is intended; `while again = 'y':` uses assignment where equality is intended; the line `Append the name to the list=list().name` is prose, not code; the final `print(name)` is not indented inside the `for` loop.

> **[handwritten]** The words `name_list` (line 2) and `name_list` (in the `for` line) are underlined by hand, and a hand-drawn arrow points at the final `print(name)`. Pencil working runs down the left margin: `[illegible: ... = ... input ...]`, `[illegible: if Var > 100 :]`, `[illegible: 1 = 500 + first-]`, `[illegible: 2 = 400 + input-]`, `[illegible: ... = ... otherwise -]`. Pencil working at the bottom right of the page: `[illegible: from (:0]]`, `[illegible: line [0]]`, `[illegible: = first . the ... . yes]`, `[illegible: ... the ... of how ...]`.

*Page 2 of 5*

---

**d.** Write a program that gets strings containing a person's first and last name as separate values, and then displays their "initials", "name in address book", "username", and "reversed form". For example, if the user enters a first name of "David" and a last name of "Oyedepo", the program should display **"D.O"**, **"David OYEDEPO"**, **"davidoyedepo"**, and **"OPEDEYO Divad"**.  **[10 Marks]**

> **[sic]** This subpart is unlabelled in the printed paper: no letter appears beside it. It falls between Question 3 (c) on page 2 and the Question 4 heading on page 3, so it is Question 3's fourth subpart. The 10 marks here bring Question 3 to 17.5, matching every other question, which confirms it belongs to Question 3.

> **[handwritten]** Small pencil marks beneath this paragraph near the Question 4 rule: `[illegible: true =]`, `[illegible]`, `[illegible: ... =]`.

> **[handwritten]** Sideways along the left edge of page 3 (bleed from the facing page): `[1 Mark]` / `ing key-value` / `[2 Marks]`.

---

## Question 4

**a.** With the aid of a sample code, describe and infinite loop?  **[1.5Marks]**

> **[sic]** "describe and infinite loop?" — "and" is printed where "an" is meant, and the sentence ends in a question mark.

**b.** What will the following code display?  **[1 Mark]**

```python
MyDict = {1: [1, 2, [3, 4], 5, 6]}
print (MyDict [0][2][1])
```

> **[handwritten]** Illegible pencil note above this box, to the right of "c. Given the following statement:": `[illegible: nothing, ... ...]`.

**c.** Given the following statement:

```python
levels = 'Beginner, Average, Advanced, Expert'
```

Write a statement that splits this string, creating the following list: ['Beginner', 'Average', 'Advanced', 'Expert']  **[1 Marks]**

> **[sic]** "[1 Marks]" is printed with a plural "Marks" for a single mark.

> **[handwritten]** Illegible pencil note to the right of the `levels` box: `[illegible: split]`.

**d.** Identify the Error(s) in the following lines of code  **[3 Marks]**

```python
def main():
        print('I have a message for you'.)
        message():
        print('Goodbye'!)

message():
        print('I am a Student of Greatness',)
        print('A Royalty in Hebron'.)
main()
```

> **[sic]** Errors are the point of this question and are transcribed verbatim: `message():` is used both to call and to define a function, with no `def` on the definition; the call `message():` carries a stray colon; the dot is misplaced outside the string in `'I have a message for you'.)` and `'A Royalty in Hebron'.)`; the `!` sits outside the string in `'Goodbye'!)`; a stray comma trails `'I am a Student of Greatness',)`.

> **[handwritten]** Hand-drawn correction marks sit in and around this box: a caret and slash on the `message():/` line, a curve after `print('Goodbye'!)`, a comma-like mark after `message():`, slashes after `print('I am a Student of Greatness',)`, and a mark after `print('A Royalty in Hebron'.)`. A large hand-drawn bracket and an `[illegible]` scribble occupy the left side of the box.

**e.** Write out the output of the correct version of the code in above  **[2 Marks]**

**f.** The date **June 10, 1960**, is special because when it is written in the following format, the month times the day equals the year: **6 / 10 / 60**. Design a program that asks the user to enter a month (in shortened form, e.g. Oct), a day in numeric form (e.g. 07), and a four-digit year (e.g. 1978). The program should then determine whether the month times the day equals the year. If so, it should display a message saying the date is **Special**. Otherwise, it should display a message saying the date is **Not Special**. *(Hint: use Dictionary and Strings)*.  **[9 Marks]**

---

## Question 5

**a.** What will the following program display?  **[1.5Marks]**

> **[handwritten]** Pencil working fills the bottom of page 3, relating to Question 4 (f): `[illegible: dict]`, `[illegible: dict ...]`, `[illegible: ... months [0:2]]`, `[illegible: if month * day == YEAR]`, `[illegible: for ... in ...]`, `[illegible: year . [s:]]`, and right column `[illegible: month =]`, `[illegible: months_no = months [month]]`, `[illegible: ... 1 =]`, `[illegible: year = 1978]`, `[illegible: ... ... in year :]`.

*Page 3 of 5*

---

```python
def main():
    x = 1
    y = 3.4
    print (x, y)
    change_us (x, y)
    print (x, y)
def change_us (a, b):
    a = 0
    b = 0
    print (a, b)
main()
```

> **[handwritten]** Pencil working sits either side of the box: on the left a fraction-like scribble `[illegible: 1/3.4]` with a slash; on the right `[illegible: 1 0]`, `[illegible: 1.8]`, `[illegible: set 1]`, `[illegible: 6]`, `[illegible: 4]`, `[illegible: 64]`, `[illegible: 90 c]`.

> **[handwritten]** Sideways along the top-right edge of page 4 (bleed from the facing page): `uestion` / `a. Write co` / `repeats 4` / `program.` / `b. What wi`.

**b.** Write a program that opens an output file with the filename **bibleinfo.txt**, writes the name of a bible book, a bible character, and a bible city to the file on separate lines, then closes the file.  **[2 Marks]**

**c.** Show the output of the following code  **[4 Marks]**

```python
for i in range(2,10):
    values =[pow(i,2)] * (i-1)
    print (values)
```

> **[handwritten]** Pencil working to the right of this box, a table of squares/products: `2 * 1 = 4`, `3 * 2 = 18`, `4 * 3 = 48`, `5 * 4 = 100`, `6 * 5 = 150`, and a second column `7 * 6 = 294`, `8 * 7 = 305`, `9 * 8 = 648`. Several figures are `[illegible]`.

**d.** Identify the Error(s) in the Code Below  **[3 Marks]**

```python
num_students = int(input('How many students do you have'?))
num_test_scores = int(input('How many test scores per student'?))
for students in range(num_student):
    total = 0.0
    print('Student number', student + 1)
    print('-----------------')
    for test_num in range(num_test_scores)
        print('Test number', test_num + 1, end='')
        score = float(input(': '))
        total += score
        average = total / num_test_scores;
        print('Average for student #', student + 1, 'is:', average)
print()
```

> **[sic]** Errors are the point of this question and are transcribed verbatim: the `?` sits outside the string in both `input(...)` calls; the loop variable is `students` but the body uses `student`; `range(num_student)` refers to `num_student` while the variable defined is `num_students`; the inner `for test_num in range(num_test_scores)` is missing its colon; a stray semicolon terminates the `average = total / num_test_scores;` line; `average` and its `print` are computed inside the inner loop rather than after it.

> **[handwritten]** The `'?))` at the end of the `num_test_scores` line is underlined, and the closing parens on both `input` lines are circled/traced by hand. A hand mark follows `num_test_scores;`.

**e.** When an object is falling because of gravity, the following formula can be used to determine the distance the object falls in a specific time period:

d = ½gt²

*(printed as a boxed mathematical expression)*

The variables in the formula are as follows: d is the distance in meters, **g is 9.8**, and **t** is the amount of time, in **seconds**, that the object has been falling. Write a function named **falling_distance** that accepts an object's falling time (in **minutes**) as an argument. The function should return the distance, in meters, that the object has fallen during that time interval. Write a program that calls the function in a loop that passes the values 1 through 10 as arguments and displays the return value.  **[7Marks]**

> **[handwritten]** Pencil working at the bottom of page 4: `g = 9.8`, `[illegible: ... = (time)]`, `[illegible: fall dist (time)]`; right column `def [illegible: falling_dist (t)]`, `d = 0.5 * g * t**2`, `[illegible: return d]`; below `for n in range(1, 11)`, `[illegible: time = n]`, `[illegible: time = time / 60]`.

*Page 4 of 5*

---

## Question 6

**a.** Write code that contains a loop that repeats 5 times nested within a loop that repeats 4 times, and state the total iterations that would occur in such a program.  **[1.5Marks]**

**b.** What will be the output when the following code is executed?  **[1 Mark]**

```python
months = {'Jan':1, 'Feb':2, 'Mar':3}
print (months[2])
```

**c.** Look at the following statement: **NewLaw = ['L', 'O', 'V', 'E']**, What values are stored in NewLaw [-1], NewLaw [-3], and NewLaw [-2]  **[3 Marks]**

**d.** Identify the Error(s) in the following Code  **[3 Marks]**

```python
def main():
        first_age = int(input('Enter your age: '))
        second_age = int(input("Enter your friend's age: "))
        total = sum(first_age, second_age);
        print('Together you are', total, 'years old'.)
sum(num1, num2):
        result = first_age + second_age
        return
main()
```

> **[sic]** Errors are the point of this question and are transcribed verbatim: `sum(num1, num2):` is a function definition with no `def`; the dot is misplaced outside the string in `'years old'.)`; a stray semicolon terminates the `total = ...;` line; `return` returns nothing rather than `result`; the function body uses `first_age`/`second_age` instead of its own parameters `num1`/`num2`; `sum` shadows the Python builtin of the same name.

**e.** Write a GUI program that converts Celsius temperatures to Fahrenheit temperatures. The user should be able to enter a Celsius temperature, click a button, then see the equivalent Fahrenheit temperature. Use the following formula to make the conversion: **F** is the Fahrenheit temperature, and **C** is the Celsius temperature.  **[9 Marks]**

F = (9/5)C + 32

*(printed as a boxed mathematical expression)*

> **[sic]** The Question 6 heading is cut off at the left edge of the scan and reads "estion 6"; it is "Question 6".

*Page 5 of 5*

---

## Transcription notes

**Total pages:** 5 (2019_20_p1.png through 2019_20_p5.png). All five read visually and re-verified against the transcript.

**Paper structure:**
- 6 questions; candidates answer **any Four (4)**.
- Every question is worth **17.5 marks** (4 x 17.5 = 70 total).
- Time: 3 hours. Credit unit: 3. Session 2019/2020, Alpha semester.
- Questions follow a strong repeating subpart template:
  1. a short definition/theory subpart (1 to 2.5 marks);
  2. one or two short "write a statement / write a loop" subparts (1 to 2 marks);
  3. a "what will the following code display?" trace subpart (1 to 4 marks);
  4. an **"Identify/Spot the Error(s) in the following code"** subpart worth **[3 Marks]** — present in every one of the six questions;
  5. a large program-design subpart worth 7 to 10 marks closing the question.
- Question 4 is the only one to break the template's length, running to six subparts (a-f) because it adds "write out the output of the corrected code" [2 Marks] after the error-spotting subpart.

**Defects found ([sic] notes):**
1. **Header/course mismatch (most significant):** the paper is filed as CSC241 Python Programming Language I but its header prints **COURSE CODE: CSC213** and **COURSE TITLE: Structured Programming**. Content is Python throughout.
2. **Unlabelled subpart:** the "first and last name / initials / username / reversed form" question at the top of page 3 carries no subpart letter. It is Question 3 (d) by position, confirmed arithmetically (its 10 marks bring Q3 to 17.5, matching every other question).
3. **Q3 (b) scrambled prose:** the clause order makes the if-condition read as attached to the wrong action.
4. **Q4 (a):** "describe **and** infinite loop?" — "and" for "an", plus a question mark on an imperative.
5. **Q4 (c):** mark allocation printed as "**[1 Marks]**" (plural for one mark).
6. **Curly quotes in code:** Q1 (c) and Q2 (b) print string literals with typographic quotes, so the snippets are not valid Python as printed.
7. **Intentional bugs:** the six "Identify the Error(s)" subparts (Q1 d, Q2 d, Q3 c, Q4 d, Q5 d, Q6 d) are full of deliberate defects — misplaced dots outside string literals, missing `def`, `=` vs `==` confusion, wrong indentation, misspelled identifiers, stray semicolons. All transcribed verbatim with the indentation exactly as printed, since the indentation is frequently the point of the question.

**Handwriting:** Heavy pencil annotation throughout, all transcribed separately under `> **[handwritten]**` markers and never merged into printed text. It falls into three kinds: (1) a student's rough working for the program-design subparts (Q1 e, Q3 b, Q4 f, Q5 c, Q5 e) — mostly legible in structure but individually illegible words; (2) correction/underline marks on the error-spotting code boxes (Q1 d, Q3 c, Q4 d, Q5 d), where the marker or student has ringed the bugs; (3) sideways text bleeding in from facing pages during scanning (right edge of p2, left edge of p3, top-right of p4) — this is not annotation but neighbouring-page print, and is labelled as bleed.

**Illegible items:** The great majority of the handwritten pencil working is only partially legible and is marked inline with `[illegible: best-guess]`. Nothing in the **printed** text is illegible except the Question 6 heading, which is cropped at the left scan edge to "estion 6" (unambiguously "Question 6"). One circled handwritten annotation beside the header's "TITLE OF EXAMINATION" line is illegible (`57` or `SS`).
