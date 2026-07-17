# CSC241 2014/2015 Exam Transcript

> **[sic]** The file is named `2014_15` for CSC241 (Python Programming Language I), but the printed header of this paper reads **COURSE CODE: CSC213**, **COURSE TITLE: Structured Programming**. The paper is transcribed as printed. Its content is overwhelmingly Python.

> **Note on pagination:** the images are 12 pages, but the printed page numbers run 7 through 18, so this paper is an extract from a larger compiled document. Pages 1-3 of the images (printed 7-9) are the question paper; pages 4-12 of the images (printed 10-18) are the MARKING SCHEME.

---

## Header

*(Covenant University crest appears at the top of the page.)*

```
COVENANT UNIVERSITY
CANAANLAND, KM 10, IDIROKO ROAD
P.M.B 1023, OTA, OGUN STATE, NIGERIA.
B.SC DEGREE EXAMINATION
```

| Field | As printed |
|---|---|
| COLLEGE | Science & Technology |
| SCHOOL | Natural & Applied Sciences |
| DEPARTMENT | Computer & Information Sciences |
| SESSION | 2014/2015 |
| SEMESTER | Alpha |
| COURSE CODE | CSC213 |
| CREDIT UNIT | 3 |
| COURSE TITLE | Structured Programming |
| INSTRUCTION | Instruction(s): Answer ANY FOUR Questions |
| TIME | 3 HOURS |

> **[sic]** The INSTRUCTION line is printed with a redundant duplicated label: the field label "INSTRUCTION:" is immediately followed by the word "Instruction(s):".

---

# QUESTION PAPER

## Question One

**a)** Briefly explain the main problem of computer programming addressed by Structured Programming

**3<sup>1</sup>/<sub>2</sub> Marks**

**b)** State the three main features of structured programming. Describe the fundamental ideas in each of them.

**9 Marks**

**c)** Compare and contrast between the Structured Programming and Object Oriented Programming.

**5Marks**

> **[sic]** Layout defect: the label "c)" is printed at the far right of the same line as the "9 Marks" allocation for part (b), and the text of part (c) begins on the following line. The subpart marker is orphaned from its question text.

## Question Two

**a.** Explain in details the concept of Modularity in structured programming.

**3½ Marks**

**b.** Give a detailed overview of python programming State four application domains with examples of Python programming language.

**8 Marks**.

> **[sic]** Missing sentence break in (b): "...overview of python programming State four application domains..." runs two sentences together with no full stop after "programming".

**c.** Briefly state with appropriate examples, the types of Control Structures in Python Programming.

**6 Marks**

## Question Three

**a)** Write a python program to calculate the factorial of a positive integer quantity. The program should call another function called factorial.

**7½ Marks**

**b)** What does the following function do?

```python
def find (strng, ch):
index = 0
while index < len (strng):
                if strng [index] == ch:
                        return index
                index += 1
return -1
```

**3Marks**

> **[sic]** The code in 3(b) is printed with broken indentation. `index = 0`, the `while` header and the final `return -1` are all flush with the `def` line (not indented into the function body), while the `if` block is indented very deeply. As printed this is not valid Python. The snippet is also set in italic proportional type rather than a monospaced font.

**c)** Define a string S of four characters: S = "spam". Write an assignment that changes the string to "slam", using only slicing and concatenation.

**4Marks**

> **[sic]** The mark allocation "4Marks" for part (c) is printed at the top of the next page (printed page 8), separated from the question text that ends the previous page.

**d)** Fill in the blank spaces;

```python
>>>  s =  "Peter, Paul, and Mary"
>>>  print s [0:5]
……..
>>> print s [7:11]
…….
>>> print s [17:21]
…….
```

**3Marks**

## Question Four

**a)** Write a python program that adds two values gotten from two different functions.

- The first function should calculate the sum of even numbers between 1 and100.
- The second function should calculate the sum of odd numbers between 1 and 100
- In the main function, calculate and print the sum of the results from the first two functions.

**7½Marks**

> **[sic]** "between 1 and100" is printed with a missing space between "and" and "100" in the first bullet.

**b)** Find the error in the following code segment and provide the correct code segment:

```python
def username_pin()
        database = [
        ['adesuwa', '1234'],
        ['innocent', '4242'],
         ['smith', '7524'],
         username = rawinput('User name: ')
        pin = rawinput('PIN code: ')
         if [usernme, pin] in database
         Print 'Access granted'
        else:
        print 'Access denied')
```

**6Marks**

*(Note: the errors in this snippet are the object of the question and are therefore intentional, not paper defects. They include the missing colon after `def username_pin()`, the unclosed `database = [` list, `rawinput` instead of `raw_input`, the missing colon after the `if`, the misspelling `usernme`, the capitalised `Print`, and the stray closing parenthesis on the last line.)*

**c)** Explain and give examples of the following;

i. Lists

ii. Strings

**4Marks**

## Question Five

**a)** Write a function named is_divisible_by_3 that takes a single integer as an argument and prints "This number is divisible by three." if the argument is evenly divisible by 3 and "This number is not divisible by three." otherwise.

Now write a similar function named is_divisible_by_5.

**7½ Marks**

**b)** Give examples of the following statements in python;

i. If statement

ii. The if statement with  alternative execution

iii. Chained conditional statements

iv. While statements

**6Marks**

**c)** What will be the output of the following programs?

**i.**

```python
.>>> a_list = ['a', 'b', 'c', 'd', 'e', 'f']
   >>> a_list[1:3] = [ ]
     >>> print a_list
```

> **[sic]** Part (c)(i) is printed as ". >>>" with a stray leading full stop before the prompt.

**ii.**

```python
>>> fruit = ["banana",  "apple",  "quince"]
   >>> fruit[0] = "pear"
     >>> fruit[-1] = "orange"
   >>> print fruit
```

**iii.**

```python
>>> range(10)
```

**iv.**

```python
>>> range(1,  10,  2)
```

**4Marks**

## Question Six

**a)** Write a python program that will accept the students score in a course and print the letter grade as follows:

- 70 and above: A
- 60-69  B
- 50-59  C
- 45-49  D
- Below 45      F

Note: make sure you take care of scores less than 0 and greater than 100

**5Marks**

**b)**

**i.** What two common syntaxes are required in a C-like language, but omitted in Python?

**2Marks**

**ii.** How are the statements in a nested block of code normally associated in Python?

**2Marks**

**c)** What does the following program do.

```python
infile = open('test2.txt', 'r')
outfile = open('test.txt', 'w')
while True:
  text = infile.read()
  if text == "":
       break
  outfile.write(text)
infile.close()
outfile.close()
```

**3½Marks**

**d)** Write a python program to calculate the sum of the first 10 terms of the series.

1/1  + ¼ + 1/9  + 1/16…………………..

**5 Marks**

---

# MARKING SCHEME

*(Beginning on printed page 10. Question restatements are printed in red bold; answers in black.)*

## Marking Scheme — Question One

### 1. (a) State and explain the main problem of computer programming addressed by structured programming?

- To minimize Program complexity. **(1.5Marks)**
- Most programs that do anything significant in the real world are rather long .i.e. word processor, OS, Compiler, Enterprise software- banking software. They have complicated interrelated parts and contain several thousand or even millions lines of codes which makes them very difficult to understand, maintain and reuse.        **(2Marks)**

> **[sic]** The marking scheme restates 1(a) as "State and explain the main problem..." with a question mark, whereas the question paper prints "Briefly explain the main problem of computer programming addressed by Structured Programming" with no question mark. The wording does not match the paper.

### 1. (b) State the three main features of structured programming? Describe the fundamental ideas in each of them.

Three main aspects:

- Top-down analysis for problem solving
- Modularization for program structure and organization,
- Structured code for the individual modules.        **(3Marks)**

Description:

- Top down analysis is a method of problem solving. The essential idea is to subdivide a large problem into several tasks or parts. Top down analysis, therefore, simplifies or reduces the complexity of the process of problem solving.
- Modular programming is a method of organizing these instructions. Large programs are broken down into separate, smaller sections called modules, subroutines, or subprograms. Each module has a specific job to do and is relatively easy to write.
- Structured codes: In SP, are organized within various control structures.  A control structure represents a unique pattern of execution for a specific set of instructions. It determines the precise order in which that set of instructions is executed.        **(6Marks)**

> **[sic]** The restated 1(b) ends "State the three main features of structured programming?" with a question mark, where the paper prints a full stop.

### 1.(c) Compare and contrast between the Structured Programming and Object Oriented Programming  **(5Marks)**

*(Printed as two bulleted lines carrying the question text, followed by a two-column table.)*

| Structured Programming | Object Oriented Programming |
|---|---|
| Structured or procedural programming is a programming paradigm that attempts to divide the problem into smaller blocks or procedures which interact with other. | OOP is a programming paradigm that program is written as a collection of interacting objects. |
| In structured programs the blocks are pieces of code which are executed as the program is run | In object-oriented programs objects have lives of their own – they can be created, copied, destroyed or even lost! |
| Structured programming is a programming technique in which the programmer divides the source code into logical chunks of code. Using structured programming techniques, programs are typically organized around code. This approach can be thought of as "code acting on data." | Object-oriented programming is a programming technique in which programs work the other way around. They are organized around data, with the key principle being "data controlling access to code." In an object-oriented language, you define the data and the routines that are permitted to act on that data. Thus, a data type defines precisely what sort of operations can be applied to that data. |
| In Structured programming, the program is built around functions and /or modules which are nothing but reusable pieces of programs. Typically it follows a top-down design approach with block-oriented structures. | The object-oriented programming paradigm is built on the foundation laid by the structured programming concept. Object-oriented programming took the best ideas of structured programming and combined them with several new concepts. In object-oriented programming, the program is built around objects which combine data and functionality. |

*(A second, separate table then begins on printed page 11 and continues onto printed page 12:)*

| Structured Programming | Object Oriented Programming |
|---|---|
| In Structured programming, the program is built around functions and /or modules which are nothing but reusable pieces of programs. Typically it follows a top-down design approach with block-oriented structures. | The object-oriented programming paradigm is built on the foundation laid by the structured programming concept. Object-oriented programming took the best ideas of structured programming and combined them with several new concepts. In object-oriented programming, the program is built around objects which combine data and functionality. |
| In structured programming large programs are broken into smaller pieces called subprograms. Each subprogram can have it own data and logic.<br><br>The base composition of any type of structured programming includes three fundamental elements: sequencing, selection and repetition. | OOP provide a new way of organizing data and code that promises increased control over the complexity of the software development process. The major difference is that OOP treat data as critical elements (as it should be) in the program development and do not allow it to flow freely around the system.<br><br>In OOP the focus is not on the code but on what you want the code to do. Basic concepts of OOP: object, class, inheritance, methods, Encapsulation and polymorphism. |

> **[sic]** The row beginning "In Structured programming, the program is built around functions and /or modules..." is printed **twice**: once as the last row of the first table (printed page 11) and again as the first row of the second table (spanning printed pages 11-12). The content is duplicated verbatim.

> **[sic]** "procedures which interact with other." — the word "each" appears to be missing ("interact with each other").

> **[sic]** "Each subprogram can have it own data and logic." — "it" should be "its".

## Marking Scheme — Question Two

### 2. (a) Explain in details the concept of Modularity.  **(3.5Marks)**

- It is a method of organizing computer instructions. Large programs are broken down into separate, smaller sections called *"Modules, Subroutines, or Subprograms". Each module has a specific task/operation to execute which is relatively less complexity to achieve.*

> **[sic]** The restated 2(a) drops "in structured programming" from the paper's wording.

> **[sic]** "which is relatively less complexity to achieve" is ungrammatical as printed.

### 2. (b) Give a detailed overview of Python Programming. State four application use cases of python, stating two (2) examples in each case.  **(8Marks)**

- A versatile, interpreted, high-level, & dynamic programming language.
- Multi-paradigm: Simple procedural programming, OOP & Functional programming.
- Easy to Learn: Automatic mememory mgt, high-level built-in data structures & libraries.
- Highly Readable: Intuitive syntax, Interpreted language, dynamic typing, etc.
- Portable Language: Many Versions-CPython, Jython, IronPython, PyPy
- Extensibility: Reusable Codes-Module & Packages, Open Source, Modularity.

> **[sic]** "mememory" is a typo for "memory".

> **[sic]** The marking scheme restates 2(b) as "State four application use cases of python, stating two (2) examples in each case", whereas the question paper asks to "State four application domains with examples". The restatement adds a "two (2) examples" requirement that the paper does not state.

**Application Areas:**

- Application development, e.g  3D games, GUI-based applications, etc
- Web development, e.g Youtube, Reddit, Yelp, etc
- Scientific computing, e.g Bioinformatics, NLP, machine learning, etc.
- Scripting, e.g OpenOffice, Games, Emacs, Blender, etc.

### 2. (c) Briefly state with appropriate examples the types of Control Structures in Python Programming.  **(6Marks)**

- Conditionals: if Stmts, elseIf/elif Stmts, *No Switch Stmt in Python.
- Loop: while Stmts.
- Continue and Break Statements.

**Examples:**

**if & elseif Stmts.**

```python
  if conditionExpr1: statement1

   elif conditionExpr2: statement2

     elif conditionExpr2: statement2

             … …

       else: statement4
```

> **[sic]** The `elif conditionExpr2: statement2` line is printed twice with the identical condition and identical statement, and the two copies are printed at different indentation levels. The indentation of the whole block is inconsistent (each line sits at a different depth), which would not be valid Python.

**Examples:**

**while Stmt.**

```python
     while conditionExpr: statement
```

**Examples:**

**continue & break Stmts.**

```python
  Expr while conditionExpr: statement

     if conditionExpr1: continue statement1

       if conditionExpr2: break
```

> **[sic]** "Expr while conditionExpr: statement" is not valid Python; the leading "Expr" is stray. The indentation across the three lines is also inconsistent.

> **[sic]** The heading "if & elseif Stmts." uses "elseif", which is not a Python keyword (the body of the example correctly uses `elif`).

## Marking Scheme — Question Three

**3. .a)** *(printed on a dark code-editor background, syntax-coloured:)*

```python
# Python program to display the Fibonacci
# sequence up to n-th term using
# recursive functions

def recur_fibo(n):
   """Recursive function to
   print Fibonacci sequence"""
   if n <= 1:
       return n
   else:
       return(recur_fibo(n-1) + recur_fibo(n-2))


# take input from the user
nterms = int(input("How many terms? "))

# check if the number of terms is valid
if nterms <= 0:
   print("Plese enter a positive integer")
else:
   print("Fibonacci sequence:")
   for i in range(nterms):
       print(recur_fibo(i))
```

> **[sic]** **Major mismatch.** Question 3(a) on the paper asks for a program to calculate the **factorial** of a positive integer calling a function named `factorial`. The marking scheme answers a completely different question: it gives a **Fibonacci** sequence program using `recur_fibo`. The model answer does not answer the question asked.

> **[sic]** "Plese enter a positive integer" is a typo for "Please".

> **[sic]** The subpart is labelled "3. .a)" with a stray extra full stop before the "a".

> **[sic]** The first two comment lines of this snippet are printed at the bottom of printed page 13 and the remainder at the top of printed page 14; the code block is split across a page break.

**b)** find is the opposite of the [ ] operator. Instead of taking an index and extracting the corresponding character, it takes a character and finds the index where that character appears. If the character is not found, the function returns -1.

**c)**

```python
>>> S = "spam"
>>> S = S[0] + 'l' + S[2:]
>>> S
'slam'
```

```python
>>> S = S[0] + 'l' + S[2] + S[3]
>>> S
'slam'
```

*(The two blocks are printed as two bulleted items.)*

**d)**

```python
>>>  s =  "Peter, Paul, and Mary"
>>>   print s [0:5]
Peter
>>> print s [7:11]
Paul
>>> print s [17:21]
Mary
```

*(Verified correct: with `s = "Peter, Paul, and Mary"`, `s[0:5]` = "Peter", `s[7:11]` = "Paul", `s[17:21]` = "Mary". No defect in this answer.)*

## Marking Scheme — Question Four

**4. a)** *(printed as a syntax-coloured editor screenshot with a green change-bar down the left margin:)*

```python
def sumEven( ):
    sum_Even=0
    i=0;
    while  i<100:
        sum_Even=sum_Even +i
        i=i+2
    return sum_Even

def sumOdd( ):
    sum_Odd=0
    i=1;
    while  i<100:
        sum_Odd=sum_Odd +i
        i=i+2
    return sum_Odd

totalSum = sumOdd() + sumEven();
print (totalSum)
```

> **[sic]** `sumEven` starts at `i=0`, so it sums 0, 2, 4, ... 98. The paper asks for the sum of even numbers **between 1 and 100**, so 100 itself is excluded and 0 is wrongly included. Likewise `sumOdd` sums 1, 3, ... 99. The `while i<100` bound does not match the stated range.

> **[sic]** The label "4. a)" is printed at the bottom of printed page 14 and the code it introduces appears at the top of printed page 15.

> **[sic]** Trailing semicolons on `i=0;`, `i=1;` and `totalSum = ...;` are C-style and redundant in Python.

**b)** *(the corrected version of the Question 4(b) code:)*

```python
def username_pin():
   database = [
   ['adesuwa', '1234'],
   ['innocent', '4242'],
   ['smith', '7524'],
   ]
   username = raw_input('User name: ')
   pin = raw_input('PIN code: ')
   if [username, pin] in database:
      print 'Access granted'
   else:
      print 'Access denied'
```

**c)** Lists: The Python list object is the most general sequence provided by the language. Lists are positionally ordered collections of arbitrarily typed objects, and they have no fixed size. They are also mutable—unlike strings, lists can be modified in-place by assignment to offsets as well as a variety of list method calls.

Strings: strings are *immutable* in Python—they cannot be changed in-place after they are created. For example, you can't change a string by assigning to one of its positions, but you can always build a new one and assign it to the same name. Strings are qualitatively different from the other four because they are made up of smaller pieces — **characters.**

> **[sic]** "different from the other four" refers to a list of five core types that does not appear anywhere in this paper; the phrase is lifted from an external source and is dangling in this context.

## Marking Scheme — Question Five

**5. a)**

```python
def is divisible_by_3(n):
        if (n%3==0):
          print("This number is not divisible by 3")
        else:
          print("This number is not divisible by 3")

def is_divisible_by_5(m):
        if (m%5==0):
          print("This number is divisible by 5")
        else:
          print("This number is not divisible by 5")
```

> **[sic]** **Two defects in the `is_divisible_by_3` model answer.** (1) The function name is printed as `def is divisible_by_3(n):` with a **space** instead of an underscore between "is" and "divisible" — a syntax error, and it does not match the name `is_divisible_by_3` required by the question. (2) **Both** the `if` and the `else` branch print "This number is not divisible by 3" — the true branch should print that the number **is** divisible. The `is_divisible_by_5` function directly below is correct in both respects, confirming the 3-version is wrong.

> **[sic]** The model answers print "...divisible by 3" / "...divisible by 5", but the question specifies the exact strings "This number is divisible by three." and "This number is not divisible by three." (spelled-out numeral, trailing full stop).

**b)**

**i.**

```
if  BOOLEAN EXPRESSION:
        STATEMENTS
```

```python
e.g. if x > 0:
        print ("x is positive")
```

**ii.**

A second form of the if statement is alternative execution, in which there are two possibilities and the condition determines which one gets executed. The syntax looks like this:

```python
if x % 2 == 0:
print ("x is even")
else:
print ("x is odd")
```

> **[sic]** This snippet is printed with **no indentation at all** — the `print` calls sit flush with the `if` and `else`. As printed it is not valid Python. (Each line is printed as a separate paragraph of body text.)

**iii**

Sometimes there are more than two possibilities and we need more than two branches. One way to express a computation like that is a **chained conditional:**

```python
if x < y:
print x, "is less than", y
elif x > y:
print x, "is greater than", y
else:
print x, "and", y, "are equal"
```

> **[sic]** Again printed with no indentation under `if`/`elif`/`else`; not valid Python as printed.

> **[sic]** The final line ends with a reversed/low closing quotation mark: `"are equal“` — the closing double quote is printed as an opening-style mark.

> **[sic]** The marker is printed as "**iii**" with no trailing full stop, while its siblings are printed "**i.**", "**ii.**", "**iv.**" with full stops.

**iv.**

While Statement

```python
def sequence(n):
while n != 1:
        print n,
        if n % 2 == 0:          # n is even
            n = n / 2
            else:               # n is odd
            n = n * 3 + 1
```

> **[sic]** The indentation of this snippet is broken: `while n != 1:` is flush with `def sequence(n):`, and the `else:` is printed **indented to the same depth as `n = n / 2`**, i.e. inside the `if` body rather than aligned with the `if`. As printed this is not valid Python.

> **[sic]** The marker "iv." appears at the very bottom of printed page 16 and its content ("While Statement") at the top of printed page 17.

**c)**

i. ['a', 'd', 'e', 'f']

ii. ['pear', 'apple', 'orange']

iii. [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

iv. [1, 3, 5, 7, 9]

## Marking Scheme — Question Six

**6. a)** *(printed as two overlapping screenshots of the Python 2.7 IDLE editor and shell. The right-hand shell window overlaps and obscures part of the left-hand editor window and its title bar. Both title bars are cut off; the visible fragment of the editor title bar reads "try -" followed by text hidden behind the shell window: `[illegible: partially obscured window title]`.)*

Editor window (File Edit Format Run Options Windows He[lp]):

```python
grade = input('Enter the grade :')
if grade >= 70:
  print 'A'
elif grade  >=60 and grade <=69:
  print 'B'
elif grade  >=50 and grade <=59:
  print 'C'
elif grade  >=45 and grade <=49:
  print 'D'
else:
  print 'F'
```

Shell window (File Edit Shell Debug Options [W]…):

```
Python 2.7.3 (default, Apr
32
Type "copyright", "credits"
>>> ======================
>>>
Enter the grade :7
F
>>>
```

> **[sic]** The shell transcript is truncated at the right edge by the screenshot crop: the version banner line reads "Python 2.7.3 (default, Apr" and the next line is a bare "32", which are the wrapped/cut remains of a longer banner. `[illegible: remainder of banner cropped out of the screenshot]`

> **[sic]** The model answer for 6(a) does **not** satisfy the question's own Note: "make sure you take care of scores less than 0 and greater than 100". The code has no validation for out-of-range scores. A grade of 150 would print 'A' and a grade of -5 would print 'F'.

> **[sic]** The demonstration run enters a grade of 7 and prints F, which exercises only the fall-through branch and does not demonstrate the range checking the question asks for.

**d) i.**  C-like languages require semicolons at the end of each statement, and braces around a nested block of code.

**ii.**       The statements in a nested block are all indented the same number of tabs or spaces.

> **[sic]** **Mislabelled subpart.** These two answers correspond to Question 6 **(b) i** and **(b) ii** on the question paper ("What two common syntaxes are required in a C-like language, but omitted in Python?" and "How are the statements in a nested block of code normally associated in Python?"). The marking scheme labels them **d)** instead of **b)**. There is no (b) in the Question 6 marking scheme.

**c)**

The following function copies a file, reading and writing up to fifty characters at a time. The first argument is the name of the original file; the second is the name of the new file:

This functions continues looping, reading characters from infile and writing the same charaters to outfile until the end of infile is reached, at which point text is empty and the break statement is executed.

> **[sic]** "The following function copies a file, reading and writing up to **fifty characters at a time**. The first argument is the name of the original file; the second is the name of the new file" does not describe the program in Question 6(c) at all. That program is not a function, takes no arguments, has hard-coded filenames ('test2.txt' and 'test.txt'), and uses `infile.read()` with **no size argument** — so it reads the whole file at once, not fifty characters at a time. The sentence is boilerplate copied from an external source describing a different `copy_file(old_file, new_file)` function.

> **[sic]** "This functions continues looping" — "functions" should be "function".

> **[sic]** "the same charaters" is a typo for "characters".

> **[sic]** The answer text for 6(c) is split across a page break: the introductory sentence ends printed page 17 and the explanation begins printed page 18.

> **[sic]** The marker "c)" appears **twice** in the Question 6 marking scheme: once as the mislabelled "d)"/"c)" pair on printed page 17 (where "c)" is printed immediately below "ii.") and the ordering runs a) … d) i/ii … c) … d). The subpart sequence is out of order.

**d)** *(printed as a syntax-coloured editor screenshot with a green change-bar:)*

```python
sum=0;
i=1
while  i<11:
     i=i+1
     sum=sum+(1/(i*i));
print(sum)
```

> **[sic]** **The model answer for 6(d) is wrong on at least three counts.** (1) `i=i+1` is executed **before** the term is added, so the first term added is 1/(2*2), not 1/(1*1) — the series starts at the wrong term and the loop computes terms for i=2..11 rather than i=1..10. (2) In Python 2 (which the 6(a) screenshot confirms is the environment, Python 2.7.3), `1/(i*i)` is **integer division** and evaluates to 0 for every i>1, so the program prints 0. (3) `sum` shadows the Python built-in `sum`. The trailing semicolons are also C-style and redundant.

---

## Transcription notes

**Total pages:** 12 image pages (`2014_15_p1.png` through `2014_15_p12.png`), all read and verified line by line against the transcript.

**Printed pagination:** the pages carry printed page numbers **7 to 18**, not 1 to 12. This paper is an extract from a larger compiled document (most likely a bound volume of several past papers). No page is missing from the extract itself — the printed numbers run consecutively 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18.

**Document structure:**

| Image pages | Printed pages | Content |
|---|---|---|
| 1-3 | 7-9 | Question paper (Questions 1-6) |
| 4-12 | 10-18 | MARKING SCHEME (model answers for Questions 1-6) |

**Paper structure:**

- **6 questions**, of which candidates **answer ANY FOUR**.
- **Time:** 3 hours. **Credit unit:** 3. **Semester:** Alpha.
- Each question totals **17½ marks** (4 × 17½ = 70 marks). Verified per question:
  - Q1: 3½ + 9 + 5 = 17½
  - Q2: 3½ + 8 + 6 = 17½
  - Q3: 7½ + 3 + 4 + 3 = 17½
  - Q4: 7½ + 6 + 4 = 17½
  - Q5: 7½ + 6 + 4 = 17½
  - Q6: 5 + 2 + 2 + 3½ + 5 = 17½
- **No repeating subpart template.** The subpart count varies (Q1, Q2 have three parts; Q4, Q5 have three; Q3 and Q6 have four). However there is a loose recurring **shape**: most questions pair a "write a program" part worth 5-7½ marks with one or more "explain / what is the output / find the error" parts. Q1 and Q2 are wholly theoretical (no code to write); Q3-Q6 are all code-centric.
- **Mark-notation is inconsistent throughout.** The paper mixes `3½ Marks`, `3<sup>1</sup>/<sub>2</sub> Marks`, `5Marks` (no space), `8 Marks.` (trailing full stop), `7½Marks`, `9 Marks`. The marking scheme uses a third style, `(1.5Marks)` / `(3.5Marks)` with decimals and parentheses. No allocation is printed in the `[3.5mks]` bracket form.

**Topics per question:**

| Q | Topics |
|---|---|
| 1 | Structured programming: the problem it addresses; its three main features (top-down analysis, modularization, structured code); SP vs OOP comparison |
| 2 | Modularity; overview of Python and its application domains; types of control structures in Python |
| 3 | Factorial program with function call; reading/tracing a `find` function on strings; string slicing and concatenation ("spam" → "slam"); slice output prediction |
| 4 | Multi-function program (sum of evens + sum of odds); debugging a broken code segment (`username_pin`); Lists vs Strings |
| 5 | Writing `is_divisible_by_3` / `is_divisible_by_5`; if / alternative execution / chained conditional / while examples; list slicing, list mutation and `range()` output |
| 6 | Grade-classification program with range validation; Python vs C-like syntax (semicolons, braces, indentation); tracing a file-copy program; summing a series (1/1 + 1/4 + 1/9 + 1/16 …) |

**Handwriting:** **None.** No handwritten annotation appears anywhere in the 12 pages. All content is printed/typeset (including the screenshot images, which are printed reproductions).

**Illegible items:** Two, both minor and both confined to the screenshots on printed page 17 (image page 11):

1. `[illegible: partially obscured window title]` — the IDLE editor window's title bar in the Question 6(a) screenshot is overlapped by the shell window in front of it. Only the fragment "try -" is visible.
2. `[illegible: remainder of banner cropped out of the screenshot]` — the Python shell version banner is cut off at the right edge of the screenshot crop ("Python 2.7.3 (default, Apr" / "32" / "Type "copyright", "credits"").

No other character on any page was in doubt.

**Defects found — summary of all `[sic]` notes:**

*Identity / header:*
1. Filed under CSC241 but the header reads **CSC213, Structured Programming**.
2. INSTRUCTION line duplicates its own label ("INSTRUCTION: Instruction(s): …").

*Question paper:*
3. Q1: the "c)" marker is orphaned onto the end of part (b)'s mark line.
4. Q2(b): two sentences run together with no full stop ("…python programming State four…").
5. Q3(b): code printed with broken indentation — `index = 0`, the `while` header and `return -1` are all flush with `def`; not valid Python as printed.
6. Q3(c): its "4Marks" allocation is stranded at the top of the next page.
7. Q4(a): "between 1 and100" missing a space.
8. Q5(c)(i): stray leading full stop before the `>>>` prompt.
9. Mark-notation is inconsistent across the whole paper (see above).

*Marking scheme — restatement mismatches:*
10. 1(a) restated with different wording and a spurious question mark.
11. 1(b) restated with a spurious question mark.
12. 2(a) restatement drops "in structured programming".
13. 2(b) restatement adds a "two (2) examples in each case" requirement absent from the paper.

*Marking scheme — wrong or non-answering model answers (the serious ones):*
14. **Q3(a): the model answer answers the wrong question entirely** — the paper asks for **factorial**, the scheme supplies a **Fibonacci** (`recur_fibo`) program.
15. **Q5(a): `def is divisible_by_3(n):`** — space instead of underscore (syntax error, wrong name), **and both the `if` and `else` branches print the identical "This number is not divisible by 3"**, so the function can never report a successful division. The `_by_5` twin directly beneath it is correct, which confirms the error.
16. **Q6(d): the series model answer is wrong three ways** — increments `i` before adding (so it computes terms 2..11 instead of 1..10), uses Python-2 integer division `1/(i*i)` which is 0 for all i>1 (the program prints 0), and shadows the built-in `sum`.
17. **Q6(c): the explanatory text describes a completely different program** — boilerplate about a `copy_file(old, new)` function reading "fifty characters at a time" with two filename arguments, whereas the actual Q6(c) program is not a function, takes no arguments, hard-codes its filenames, and calls `infile.read()` with no size argument.
18. Q6(a): the model answer ignores the question's own Note requiring validation of scores <0 and >100; the demo run (grade 7 → F) does not exercise it.
19. Q4(a): `while i<100` starting from `i=0`/`i=1` does not match "between 1 and 100" (includes 0, excludes 100).
20. Q5(a): model answers use "divisible by 3"/"by 5" where the question specifies the exact strings "This number is divisible by three." etc.

*Marking scheme — structural / labelling:*
21. **Q6: subparts are mislabelled and out of order** — the answers to (b)(i) and (b)(ii) are labelled **d)**; there is no (b) at all; the sequence runs a) … d) i/ii … c) … d), with **"c)" and "d)" each appearing twice**.
22. Q1(c): an entire table row ("In Structured programming, the program is built around functions and /or modules…") is **duplicated verbatim** across the end of the first table and the start of the second.
23. Q3(a) labelled "3. .a)" with a stray extra full stop.
24. Q5(b)(iii) marker printed "iii" without the full stop its siblings carry.

*Marking scheme — invalid Python as printed:*
25. 2(c) if/elif example: `elif conditionExpr2: statement2` printed **twice** with identical condition and statement, at two different indent levels; whole block inconsistently indented.
26. 2(c) continue/break example: `Expr while conditionExpr: statement` — stray leading "Expr"; inconsistent indentation.
27. 2(c) heading uses "elseif", not a Python keyword (body correctly uses `elif`).
28. 5(b)(ii) and 5(b)(iii) snippets printed with **zero indentation** under `if`/`elif`/`else`.
29. 5(b)(iv) snippet: `while` flush with `def`; `else:` indented **inside** the `if` body rather than aligned with the `if`.

*Marking scheme — typos:*
30. "Plese" for "Please" (Q3(a) code).
31. "mememory" for "memory" (Q2(b)).
32. "This functions continues" for "This function continues" (Q6(c)).
33. "charaters" for "characters" (Q6(c)).
34. "interact with other" — missing "each" (Q1(c) table).
35. "Each subprogram can have it own data and logic" — "it" for "its" (Q1(c) table).
36. `"are equal“` — reversed closing quotation mark (Q5(b)(iii)).
37. Q4(c): "different from the other four" — dangling reference to a five-type list that appears nowhere in this paper; lifted from an external source.

*Formatting:*
38. Q3(b)'s code and several marking-scheme snippets are set in **italic proportional type**, not monospace, making indentation ambiguous to read.
39. Several code blocks and answers are split across page breaks (Q3(a) code across printed 13/14; "4. a)" label on 14 with its code on 15; Q5(b)(iv) marker on 16 with content on 17; Q6(c) text across 17/18).

**Overall assessment:** the question paper itself is broadly sound apart from layout slips and the Q3(b) indentation. The **marking scheme is substantially defective** — one model answer solves the wrong problem entirely (Q3(a) factorial → Fibonacci), one is internally contradictory (Q5(a) both branches print the same negative result), one produces the wrong output (Q6(d) prints 0 under Python 2), one explains a program that is not the program asked about (Q6(c)), and Q6's subparts are mislabelled with duplicate markers. Several snippets would not run as printed.
