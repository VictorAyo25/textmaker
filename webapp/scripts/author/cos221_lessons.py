"""
Extra objective questions for COS221, one set per crash-course lesson, with
every program COMPILED AND RUN by a real JDK before it is written out.

    python scripts/author/cos221_lessons.py

Writes data/cos221/drill02.json. Run BY HAND; the web build never runs Java.

The same discipline as csc241_lessons.py, for Java. A program is written as the
statements of main (plus any helper methods or classes), wrapped in a class and
run with `java Main.java`, the JDK's single-file launcher, which compiles and
runs in one step. The build STOPS if:

  - check "out": the correct option is not exactly what the program printed,
    or a wrong option is also exactly that;
  - check "err:Name": the program does not throw exactly Name at run time;
  - check "compile": the program compiles (so "it does not compile" would be
    a false key), or check "out" and the program does NOT compile;
  - check "equiv": for a question whose options are rewritings of one loop,
    the correct rewriting does not print what the original prints, or a wrong
    one does.

The correct option is written first and moved to a position fixed by a hash of
the question id. Questions are plain text; a listing goes in `code`.
"""
import json
import random
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "data" / "cos221" / "drill02.json"

# lesson number -> drill topic, as the importer files the Java lessons
TOPIC = {"1.1": 1, "1.2": 1, "1.3": 2, "1.4": 2, "1.5": 2, "1.6": 3,
         "2.1": 3, "2.2": 3, "2.3": 3, "2.4": 3, "2.5": 3, "2.6": 4, "2.7": 4,
         "2.8": 7, "2.9": 6, "3.1": 5, "3.2": 5, "3.3": 5, "3.4": 5,
         "3.5": 8, "3.6": 9, "3.7": 9}

QUESTIONS = []
_count = {}


def C(src):
    return textwrap.dedent(src).strip("\n")


def program(body, methods="", classes="", throws=False):
    """The source that is compiled: helpers inside class Q, extra classes after it."""
    ind = lambda s, n: textwrap.indent(C(s), " " * n) if s else ""
    head = "    public static void main(String[] args)" + (" throws Exception" if throws else "") + " {"
    return ("import java.io.*;\nimport java.util.*;\n\nclass Q {\n"
            + (ind(methods, 4) + "\n\n" if methods else "")
            + head + "\n" + ind(body, 8) + "\n    }\n}\n"
            + ("\n" + C(classes) + "\n" if classes else ""))


def shown(body, methods="", classes=""):
    """What the reader sees: the helpers, then the statements of main."""
    parts = []
    if classes:
        parts.append(C(classes))
    if methods:
        parts.append(C(methods))
    if parts:
        parts.append("// in main:\n" + C(body))
        return "\n\n".join(parts)
    return C(body)


def Q(lesson, topic, prompt, opts, why, exp, *, body=None, methods="", classes="", throws=False,
      check=None, style="mcq", key=None, diff="medium", facets=None, before=None,
      stdin=None, equiv=None):
    _count[lesson] = _count.get(lesson, 0) + 1
    qid = f"cos-l{lesson.replace('.', '')}-{_count[lesson]:02d}"
    QUESTIONS.append(dict(id=qid, lesson=lesson, topic=topic, prompt=prompt, opts=opts, why=why,
                          exp=exp, body=body, methods=methods, classes=classes, throws=throws,
                          check=check, style=style, nkey=len(key) if key else 1, diff=diff,
                          facets=facets, before=before, stdin=stdin, equiv=equiv))


def TF(lesson, topic, prompt, answer, why_true, why_false, exp, *, diff="easy", facets=None):
    _count[lesson] = _count.get(lesson, 0) + 1
    qid = f"cos-l{lesson.replace('.', '')}-{_count[lesson]:02d}"
    QUESTIONS.append(dict(id=qid, lesson=lesson, topic=topic, prompt=prompt, style="tf",
                          answer=answer, why={"true": why_true, "false": why_false}, exp=exp,
                          body=None, check=None, diff=diff, facets=facets))


NOCOMPILE = "It does not compile"

# ============================================================ Lesson 1.1
L = "1.1"
Q(L, "print and println", "What does this print?",
  ["AB\nC", "A\nB\nC", "ABC", "A B\nC"],
  ["Correct. print stays on the line, println ends it after B, and the last print starts the new line.",
   "Wrong. Only println moves to a new line; print does not.",
   "Wrong. println(\"B\") ends the line before C.",
   "Wrong. Nothing adds a space between A and B."],
  "println prints and then moves to a new line; print leaves the cursor where it is.",
  body='''
      System.out.print("A");
      System.out.println("B");
      System.out.print("C");
  ''', check="out", diff="easy", facets=["numbers"])
Q(L, "the main line", "A program compiles without error but refuses to start. Which main line explains it?",
  ["public static void Main(String[] args)", "public static void main(String[] args)",
   "public static void main(String args[])", "static public void main(String[] args)"],
  ["Correct. Main with a capital M is a different name, so there is no starting point, though it compiles.",
   "Wrong. That is the correct header.",
   "Wrong. String args[] is another legal way to declare the same array.",
   "Wrong. The order of public and static does not matter."],
  "Java is case sensitive. main is the name the JVM looks for; Main compiles and never runs.",
  diff="medium", facets=["names"])
Q(L, "semicolons", "What happens when this is compiled?",
  [NOCOMPILE + ": the println statement has no semicolon", "It prints Hi",
   NOCOMPILE + ": the class line needs a semicolon", "It prints Hi with a warning"],
  ["Correct. Every statement ends in a semicolon, and this one has none.",
   "Wrong. The missing semicolon stops compilation.",
   "Wrong. A line ending in an opening brace is a heading, not a statement, and takes no semicolon.",
   "Wrong. A missing semicolon is an error, not a warning."],
  "A missing semicolon is the single most common error in a handwritten script.",
  body='''
      System.out.println("Hi")
  ''', check="compile", diff="easy", facets=["wording"])
Q(L, "semicolons", "Which of these lines needs a semicolon at the end?",
  ["int total = 0", "public class Hello {", "}", "public static void main(String[] args) {"],
  ["Correct. An assignment is a statement, and every statement ends in a semicolon.",
   "Wrong. A line ending in an opening brace opens a block.",
   "Wrong. A closing brace ends a block.",
   "Wrong. The main line opens a block."],
  "Semicolons go on statements only: assignments, calls and returns.",
  diff="easy", facets=["wording"])
Q(L, "file names", "A file holds public class ReportCard. What must the file be called?",
  ["ReportCard.java", "reportcard.java", "ReportCard.class", "Main.java"],
  ["Correct. A public class lives in a file of exactly its own name.",
   "Wrong. The case must match: ReportCard.",
   "Wrong. .class is the compiled bytecode, not the source you write.",
   "Wrong. The file is named after the class."],
  "A public class must live in a file named after it, exactly, ending .java.",
  diff="easy", facets=["names"])
Q(L, "case sensitivity", "What happens when this is compiled?",
  [NOCOMPILE + ", because Java is case sensitive and the class is System", "It prints hi",
   "It prints hi and a warning", "It compiles, then fails when it runs"],
  ["Correct. system with a small s is not a name Java knows.",
   "Wrong. The lower case s stops compilation.",
   "Wrong. It is an error, not a warning.",
   "Wrong. The compiler catches it before anything runs."],
  "String, System and println: case is part of every name.",
  body='''
      system.out.println("hi");
  ''', check="compile", diff="easy", facets=["names"])
Q(L, "text against arithmetic", "What does this print?",
  ["5 + 3\n8", "8\n8", "5 + 3\n5 + 3", "8\n5 + 3"],
  ["Correct. In quotes it is text and is printed as written; without quotes it is worked out.",
   "Wrong. The quotes make the first line text.",
   "Wrong. Without quotes, 5 + 3 is calculated.",
   "Wrong. The lines are in the other order."],
  "Anything in double quotes is a String, printed exactly; an expression outside quotes is evaluated.",
  body='''
      System.out.println("5 + 3");
      System.out.println(5 + 3);
  ''', check="out", diff="easy", facets=["numbers"])
TF(L, "comments", "True or false: a comment written after // is ignored by the compiler.",
   "true",
   "Correct. // makes the rest of the line a note to the reader.",
   "Wrong. The compiler skips comments entirely.",
   "// comments to the end of the line; /* ... */ comments across several lines. The paper asks for comments in Sections B and C.",
   facets=["wording"])

# ============================================================ Lesson 1.2
L = "1.2"
Q(L, "the journey", "Which file does the JVM actually read and run?",
  ["Hello.class, the bytecode", "Hello.java, the source", "javac.exe", "Both files, one after the other"],
  ["Correct. javac turns the source into bytecode in a .class file, and the JVM runs that.",
   "Wrong. The JVM never sees your source file.",
   "Wrong. javac is the compiler that MAKES the .class file.",
   "Wrong. Only the bytecode is run."],
  "Source, compiler, bytecode, virtual machine: Hello.java, javac, Hello.class, the JVM.",
  diff="easy", facets=["names"])
Q(L, "platform independence", "What makes Java platform independent?",
  ["The same bytecode runs on any machine that has a JVM", "javac produces machine code for every processor",
   "Java has no compiler", "Every operating system uses the same JVM"],
  ["Correct. Write once, run anywhere: the bytecode never changes.",
   "Wrong. javac produces bytecode, not machine code.",
   "Wrong. javac is the compiler.",
   "Wrong. The JVM is the one part that differs from platform to platform."],
  "The bytecode is the same everywhere, and a platform specific JVM executes it.",
  diff="easy", facets=["wording"])
Q(L, "JDK, JRE, JVM", "How do the JDK, the JRE and the JVM fit together?",
  ["The JDK contains the JRE, which contains the JVM", "The JVM contains the JRE, which contains the JDK",
   "They are three unrelated programs", "The JRE contains the JDK and the JVM"],
  ["Correct. Each adds to the one inside it: JDK adds javac, JRE adds the class libraries, JVM executes.",
   "Wrong. This is upside down.",
   "Wrong. They nest.",
   "Wrong. The JDK is the largest."],
  "Draw three nested boxes: JDK around JRE around JVM.",
  diff="medium", facets=["names"])
Q(L, "JDK, JRE, JVM", "Which two statements are true?",
  ["The JRE is the JVM plus the standard class libraries", "The JDK adds development tools, principally javac",
   "The JVM compiles your source code", "The JVM reads your .java file"],
  ["Correct. That is the JRE.",
   "Correct. That is the JDK.",
   "Wrong. javac compiles; the JVM executes.",
   "Wrong. The JVM only ever sees the .class bytecode."],
  "javac compiles to bytecode, the JVM runs bytecode. Getting those two the wrong way round is the commonest lost mark here.",
  style="multi", key=[0, 1], diff="medium", facets=["names"])
TF(L, "the JVM", "True or false: the JVM is the one part of Java that differs from platform to platform.",
   "true",
   "Correct. There is a different JVM for Windows, Linux or a phone; your bytecode does not change.",
   "Wrong. The JVM is exactly the platform specific part.",
   "Platform independence works because only the JVM changes between machines.",
   facets=["wording"])
Q(L, "compiled, not interpreted", "A Java file has a syntax error on line 40. How much of the program runs?",
  ["None of it; the compiler rejects the file before anything runs", "Lines 1 to 39", "Everything except line 40",
   "Everything, with a warning at line 40"],
  ["Correct. Java is compiled, so the whole file is checked first.",
   "Wrong. That is how an interpreted language behaves with a runtime error.",
   "Wrong. A file that does not compile does not run at all.",
   "Wrong. A syntax error is not a warning."],
  "A syntax error means nothing runs, not even the correct lines above it.",
  diff="medium", facets=["wording"])
Q(L, "features", "Which feature means memory you stop using is reclaimed for you?",
  ["Automatic garbage collection", "Multithreading", "Platform independence", "Strong type checking"],
  ["Correct. Garbage collection frees memory nothing refers to any more.",
   "Wrong. Multithreading is running tasks at the same time.",
   "Wrong. That is about bytecode running anywhere.",
   "Wrong. That is what makes Java robust about types."],
  "Java is simple, secure, robust, multithreaded, and garbage collected.",
  diff="easy", facets=["names"])
TF(L, "javac", "True or false: javac executes the bytecode.",
   "false",
   "Wrong. javac compiles; the JVM executes.",
   "Correct. javac turns source into bytecode; the command java starts the JVM, which runs it.",
   "Compiler makes it, virtual machine runs it.",
   facets=["names"])

# ============================================================ Lesson 1.3
L = "1.3"
Q(L, "casting chops", "What does this print?",
  ["7\n8", "8\n8", "7\n7", "7.89\n8"],
  ["Correct. A cast to int chops off the decimal part; Math.round rounds to the nearest.",
   "Wrong. The cast does not round.",
   "Wrong. Math.round(7.89) rounds up to 8.",
   "Wrong. (int) produces a whole number."],
  "(int) 7.89 is 7: a cast chops. For proper rounding use Math.round.",
  body='''
      System.out.println((int) 7.89);
      System.out.println(Math.round(7.89));
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "char against String", "What happens when this is compiled?",
  [NOCOMPILE + ": \"A\" is a String, which does not fit in a char", "It prints A",
   "It prints 65", "It compiles and prints nothing"],
  ["Correct. A char takes single quotes, 'A'.",
   "Wrong. The double quotes make it a String.",
   "Wrong. It never compiles, so nothing prints.",
   "Wrong. The type mismatch stops compilation."],
  "Double quotes for a String, single quotes for a char. A value that does not fit its box is the planted error to look for.",
  body='''
      char grade = "A";
      System.out.println(grade);
  ''', check="compile", diff="easy", facets=["names"])
Q(L, "float literals", "What happens when this is compiled?",
  [NOCOMPILE + ": 1.5 is a double; write 1.5f", "It prints 1.5", "It prints 1.0", "It prints 2"],
  ["Correct. A decimal literal is a double, and a double does not fit a float without the f suffix.",
   "Wrong. The literal does not fit the float box as written.",
   "Wrong. It does not compile.",
   "Wrong. It does not compile."],
  "Two suffixes to remember: a long literal ends in L, a float literal ends in f.",
  body='''
      float f = 1.5;
      System.out.println(f);
  ''', check="compile", diff="medium", facets=["names"])
Q(L, "widening", "What does this print?",
  ["7.0", "7", "7.00", "It does not compile"],
  ["Correct. An int widens to a double automatically, and a double prints with a decimal point.",
   "Wrong. d is a double, so it prints as 7.0.",
   "Wrong. println shows 7.0.",
   "Wrong. Widening is always allowed."],
  "Widening is free: byte to short to int to long to float to double. Narrowing needs a cast.",
  body='''
      double d = 7;
      System.out.println(d);
  ''', check="out", diff="easy", facets=["numbers"])
Q(L, "naming", "Which two of these are legal variable names?",
  ["_total", "price2", "2price", "class"],
  ["Correct. A name may start with an underscore.",
   "Correct. Digits are allowed after the first character.",
   "Wrong. A name may not start with a digit.",
   "Wrong. class is a Java keyword."],
  "Letters, digits, _ and $; not starting with a digit; no spaces; not a keyword.",
  style="multi", key=[0, 1], diff="easy", facets=["names"])
Q(L, "primitive sizes", "How many bytes does a char take in Java?",
  ["2", "1", "4", "It is not defined"],
  ["Correct. Java characters are Unicode, two bytes.",
   "Wrong. One byte is a byte.",
   "Wrong. Four bytes is an int or a float.",
   "Wrong. It is boolean whose size is not defined."],
  "byte 1, short 2, int 4, long 8, float 4, double 8, char 2, boolean undefined.",
  diff="medium", facets=["numbers"])
Q(L, "final", "What happens when this is compiled?",
  [NOCOMPILE + ": a final variable cannot be assigned again", "It prints 6", "It prints 5", "It prints 11"],
  ["Correct. final means the value can never change after it is set.",
   "Wrong. The reassignment is refused.",
   "Wrong. It never runs.",
   "Wrong. It never runs."],
  "final makes a constant, named in capitals: MAX, VAT.",
  body='''
      final int MAX = 5;
      MAX = 6;
      System.out.println(MAX);
  ''', check="compile", diff="easy", facets=["names"])
Q(L, "widening", "What does this print?",
  ["11", "11.0", "It does not compile", "101"],
  ["Correct. An int widens to a long automatically, and a long plus 1 is the whole number 11.",
   "Wrong. long is a whole-number type.",
   "Wrong. int to long is widening, which is always allowed.",
   "Wrong. + adds numbers; nothing here is text."],
  "Moving to a bigger box is silent and safe.",
  body='''
      int x = 10;
      long y = x;
      System.out.println(y + 1);
  ''', check="out", diff="easy", facets=["numbers"])
TF(L, "String is a class", "True or false: String is one of Java's eight primitive types.",
   "false",
   "Wrong. String is a class, which is why it has a capital letter.",
   "Correct. String is a class; a String variable holds a reference to an object.",
   "Every primitive is lower case; String, with its capital S, is a class.",
   diff="easy", facets=["names"])

# ============================================================ Lesson 1.4
L = "1.4"
Q(L, "integer division", "What does this print?",
  ["7 1", "7.25 1", "7 0.25", "8 1"],
  ["Correct. 29 / 4 between ints is 7, remainder 1.",
   "Wrong. Two ints divide as ints and the remainder is dropped.",
   "Wrong. % gives the remainder as a whole number, 1.",
   "Wrong. Integer division does not round up."],
  "Two ints divide as ints. The remainder is what % gives you.",
  body='''
      System.out.println(29 / 4 + " " + 29 % 4);
  ''', check="out", diff="easy", facets=["numbers"])
Q(L, "where the cast goes", "What does this print?",
  ["3\n3.5\n3.0", "3.5\n3.5\n3.5", "3\n3\n3", "3\n3.5\n3.5"],
  ["Correct. sum / n is integer division, 3; casting one side first gives 3.5; casting AFTER the division only converts the wrong 3 into 3.0.",
   "Wrong. The first line divides two ints.",
   "Wrong. The second line casts sum before dividing.",
   "Wrong. (double)(sum / n) divides first, in integers."],
  "Cast one operand, before the division: (double) sum / n. (double)(sum / n) converts an answer that is already wrong.",
  body='''
      int sum = 7, n = 2;
      System.out.println(sum / n);
      System.out.println((double) sum / n);
      System.out.println((double) (sum / n));
  ''', check="out", diff="hard", facets=["numbers"])
Q(L, "plus joins or adds", "What does this print?",
  ["x23\n5x", "x5\n5x", "x23\n23x", "x5\n23x"],
  ["Correct. + works left to right: \"x\" + 2 is already text, so 3 joins too; 2 + 3 are both numbers, so they add before meeting \"x\".",
   "Wrong. Once text is on the left, every later + joins.",
   "Wrong. 2 + 3 adds before the text is reached.",
   "Wrong. Both lines are the other way round."],
  "If either side of + is a String, + joins. Bracket arithmetic that sits next to text.",
  body='''
      System.out.println("x" + 2 + 3);
      System.out.println(2 + 3 + "x");
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "a++ against ++a", "What does this print?",
  ["5 8", "5 7", "4 8", "5 9"],
  ["Correct. a++ gives 3 then makes a 4; ++a makes a 5 and gives 5; so b is 3 + 5 = 8 and a is 5.",
   "Wrong. ++a increments to 5 before it is used.",
   "Wrong. Both increments happen, so a ends at 5.",
   "Wrong. a++ contributes its OLD value, 3."],
  "Post uses the old value then adds one; pre adds one then uses the new value.",
  body='''
      int a = 3;
      int b = a++ + ++a;
      System.out.println(a + " " + b);
  ''', check="out", diff="hard", facets=["numbers"])
Q(L, "short circuit", "What does this print?",
  ["safe", "big", "an ArithmeticException", "It does not compile"],
  ["Correct. n != 0 is false, so && stops and the division is never attempted.",
   "Wrong. The condition is false.",
   "Wrong. The guard on the left prevents the division by zero.",
   "Wrong. It compiles."],
  "&& stops at the first false, so put the guard on the left: n != 0 && total / n > 1.",
  body='''
      int n = 0;
      if (n != 0 && 10 / n > 1) {
          System.out.println("big");
      } else {
          System.out.println("safe");
      }
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "precedence", "What does this print?",
  ["6", "14", "8", "-2"],
  ["Correct. * and / first: 2 * 3 = 6 and 4 / 2 = 2; then 10 - 6 + 2 = 6.",
   "Wrong. That works left to right ignoring precedence.",
   "Wrong. Check the subtraction: 10 - 6 is 4, plus 2 is 6.",
   "Wrong. The division gives 2, which is added."],
  "Precedence: brackets, unary and casts, * / %, then + -, left to right.",
  body='''
      System.out.println(10 - 2 * 3 + 4 / 2);
  ''', check="out", diff="medium", facets=["numbers", "lists"])
Q(L, "compound assignment", "What does this print?",
  ["1", "16", "3", "0"],
  ["Correct. 5 + 3 = 8, times 2 is 16, and 16 % 5 leaves 1.",
   "Wrong. The last line takes the remainder.",
   "Wrong. Work each line in turn: 8, 16, 1.",
   "Wrong. 16 is not a multiple of 5."],
  "x += 3 means x = x + 3; the same for *= and %=.",
  body='''
      int x = 5;
      x += 3;
      x *= 2;
      x %= 5;
      System.out.println(x);
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "= against ==", "What happens when this is compiled?",
  [NOCOMPILE + ": if needs a boolean, and x = 5 is an assignment", "It prints five",
   "It prints nothing", "It prints five, then x is 5"],
  ["Correct. = assigns; == compares. Java refuses an int where if needs a boolean.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "Writing if (x = 5) will not compile in Java, a small mercy.",
  body='''
      int x = 5;
      if (x = 5) {
          System.out.println("five");
      }
  ''', check="compile", diff="easy", facets=["wording"])
Q(L, "plus joins or adds", "What does this print?",
  ["3345", "15", "339", "12345"],
  ["Correct. 1 + 2 adds to 3; then \"3\" makes it text, so 4 and 5 are joined on: 3, 3, 4, 5.",
   "Wrong. Once text appears, the rest joins.",
   "Wrong. 4 and 5 are joined, not added, after the text.",
   "Wrong. The first two numbers add before the text."],
  "Left to right: numbers add until a String appears, then everything joins.",
  body='''
      System.out.println(1 + 2 + "3" + 4 + 5);
  ''', check="out", diff="hard", facets=["numbers"])

# ============================================================ Lesson 1.5
L = "1.5"
Q(L, "printf", "What does this print?",
  ["2.5|   42|ab  |", "2.46|42|ab|", "2.5|42   |  ab|", "2.4|   42|ab  |"],
  ["Correct. %.1f rounds to one place, %5d pads 42 to five columns on the left, %-4s pads ab to four on the right.",
   "Wrong. The widths and the precision change the output.",
   "Wrong. Numbers pad on the left; the minus makes text pad on the right.",
   "Wrong. %.1f rounds 2.46 to 2.5."],
  "% starts a placeholder, the number sets width and decimals, the letter sets the type; %n ends the line.",
  body='''
      System.out.printf("%.1f|%5d|%-4s|%n", 2.46, 42, "ab");
  ''', check="out", diff="hard", facets=["numbers", "names"])
Q(L, "JOptionPane", "Which import does a JOptionPane program need?",
  ["import javax.swing.JOptionPane;", "import java.swing.JOptionPane;",
   "import java.util.JOptionPane;", "import javax.util.Scanner;"],
  ["Correct. javax, with the x, then swing.",
   "Wrong. It is javax, not java.",
   "Wrong. java.util is Scanner's package.",
   "Wrong. Scanner is java.util.Scanner."],
  "java.util.Scanner, javax.swing.JOptionPane: one letter, whole import.",
  diff="easy", facets=["names"])
Q(L, "JOptionPane", "The user types 42 into a JOptionPane.showInputDialog. What does the call return?",
  ["The String \"42\"", "The int 42", "The double 42.0", "Nothing; it only shows a window"],
  ["Correct. A dialog only ever hands back text.",
   "Wrong. You must convert it with Integer.parseInt.",
   "Wrong. It is text until you parse it.",
   "Wrong. showInputDialog returns what was typed."],
  "A dialog always gives you text, so parse it: Integer.parseInt(t) or Double.parseDouble(t).",
  diff="easy", facets=["names"])
Q(L, "parsing", "What does this print?",
  ["43\n421", "43\n43", "421\n421", "It does not compile"],
  ["Correct. n is the number 42, so n + 1 is 43; t is still the text \"42\", so t + 1 joins to 421.",
   "Wrong. t was never converted.",
   "Wrong. n is a number after parseInt.",
   "Wrong. Both lines are legal."],
  "Integer.parseInt turns text into a whole number; the original String is unchanged.",
  body='''
      String t = "42";
      int n = Integer.parseInt(t);
      System.out.println(n + 1);
      System.out.println(t + 1);
  ''', check="out", diff="medium", facets=["numbers", "names"])
Q(L, "parsing", "What happens when this runs?",
  ["It throws NumberFormatException, because 4.5 is not a whole number", "It prints 4",
   "It prints 5", "It prints 4.5"],
  ["Correct. parseInt accepts only whole-number text.",
   "Wrong. parseInt does not chop; it refuses.",
   "Wrong. parseInt does not round.",
   "Wrong. That needs Double.parseDouble."],
  "Integer.parseInt(\"4.5\") fails; Double.parseDouble(\"4.5\") gives 4.5.",
  body='''
      int n = Integer.parseInt("4.5");
      System.out.println(n);
  ''', check="err:NumberFormatException", diff="medium", facets=["names"])
Q(L, "nextInt then nextLine", "The user types 5, presses Enter, then types Ada. What does this print?",
  ["[]", "[Ada]", "[5]", "[5 Ada]"],
  ["Correct. nextInt reads 5 but leaves the newline behind, so nextLine returns the empty rest of that line.",
   "Wrong. nextLine never reaches Ada; it stops at the leftover newline.",
   "Wrong. nextInt already consumed the 5.",
   "Wrong. nextLine reads only the rest of the current line."],
  "Reading a number and then a line: nextInt leaves the newline, so add an extra nextLine() to swallow it.",
  body='''
      Scanner in = new Scanner(System.in);
      int n = in.nextInt();
      String name = in.nextLine();
      System.out.println("[" + name + "]");
  ''', stdin="5\nAda\n", check="out", diff="hard", facets=["names"])
Q(L, "JOptionPane", "Which line should end a JOptionPane program, so it stops when main ends?",
  ["System.exit(0);", "return 0;", "JOptionPane.close();", "System.out.println();"],
  ["Correct. A window program does not stop on its own; System.exit(0) ends it.",
   "Wrong. main is void, so it returns no value.",
   "Wrong. There is no such call.",
   "Wrong. That only prints a blank line."],
  "Finish a dialog program with System.exit(0).",
  diff="easy", facets=["names"])
Q(L, "printf", "What does this print?",
  ["3 items at 2.50", "3 items at 2.5", "3.00 items at 2.50", "%d items at %.2f"],
  ["Correct. %d takes the whole number 3 and %.2f shows 2.5 to two decimal places.",
   "Wrong. %.2f always shows two decimal places.",
   "Wrong. %d is a whole number.",
   "Wrong. The placeholders are replaced by the values."],
  "%d for whole numbers, %.2f for money, %s for text, %n for the new line.",
  body='''
      System.out.printf("%d items at %.2f%n", 3, 2.5);
  ''', check="out", diff="easy", facets=["numbers", "names"])

# ============================================================ Lesson 1.6
L = "1.6"
Q(L, "tracing a loop", "What does this print?",
  ["15", "20", "10", "26"],
  ["Correct. i takes 2, 5 and 8; at 11 the test fails. 2 + 5 + 8 = 15.",
   "Wrong. The loop does not reach 11.",
   "Wrong. 8 is still <= 8, so it is added.",
   "Wrong. 11 fails the test and is never added."],
  "Write the table: every pass, and the pass that fails the test.",
  body='''
      int total = 0;
      for (int i = 2; i <= 8; i += 3) {
          total += i;
      }
      System.out.println(total);
  ''', check="out", diff="medium", facets=["numbers", "lists"])
Q(L, "digit walk", "What does this print?",
  ["12", "4071", "4", "11"],
  ["Correct. The loop pulls off 1, 7, 0 and 4 with % 10 and removes each with / 10: 1 + 7 + 0 + 4 = 12.",
   "Wrong. The loop sums the digits; it does not rebuild the number.",
   "Wrong. That is how many digits there are.",
   "Wrong. Add every digit: 4 + 0 + 7 + 1."],
  "n % 10 is the last digit and n /= 10 removes it: together they walk a number right to left.",
  body='''
      int n = 4071;
      int s = 0;
      while (n > 0) {
          s += n % 10;
          n /= 10;
      }
      System.out.println(s);
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "counting digits", "What does this print?",
  ["5", "4", "90210", "6"],
  ["Correct. Five divisions by 10 bring 90210 to 0: 9021, 902, 90, 9, 0.",
   "Wrong. The zeros inside the number still count.",
   "Wrong. d counts; n is used up.",
   "Wrong. The loop stops as soon as n reaches 0."],
  "A counting loop destroys what it counts, which is why a program copies n into temp first.",
  body='''
      int n = 90210, d = 0;
      while (n > 0) {
          d++;
          n /= 10;
      }
      System.out.println(d);
  ''', check="out", diff="easy", facets=["numbers"])
Q(L, "the ternary operator", "What does this print?",
  ["9", "7", "true", "16"],
  ["Correct. a > b is false, so the ternary gives the value after the colon, b.",
   "Wrong. The first value is chosen only when the test is true.",
   "Wrong. The ternary gives one of the two values, not the test.",
   "Wrong. Nothing adds a and b."],
  "test ? valueIfTrue : valueIfFalse is an if-else squeezed into an expression.",
  body='''
      int a = 7, b = 9;
      int m = (a > b) ? a : b;
      System.out.println(m);
  ''', check="out", diff="easy", facets=["numbers"])
Q(L, "Armstrong check", "What does this print?",
  ["190 false", "154 true", "190 true", "10 false"],
  ["Correct. The cubes of 1, 5 and 4 are 1, 125 and 64, which sum to 190, not 154.",
   "Wrong. The sum of the cubes is 190.",
   "Wrong. 190 is not equal to 154.",
   "Wrong. The digits are cubed before they are added."],
  "Trace it digit by digit: pull off the last digit, cube it, add it, remove it.",
  body='''
      int n = 154, temp = n, sum = 0;
      while (temp > 0) {
          int d = temp % 10;
          sum += d * d * d;
          temp /= 10;
      }
      System.out.println(sum + " " + (sum == n));
  ''', check="out", diff="hard", facets=["numbers"])
Q(L, "the failing pass", "What does this print?",
  ["4", "3", "5", "It does not compile"],
  ["Correct. i passes 0, 1, 2, 3; then i becomes 4, the test 4 < 4 fails, and the loop ends with i at 4.",
   "Wrong. The last step makes i 4 before the failing test.",
   "Wrong. The loop stops as soon as i reaches 4.",
   "Wrong. i is declared before the loop, so it exists afterwards."],
  "Always write the pass that fails the test: it is where off-by-one answers come from.",
  body='''
      int i;
      for (i = 0; i < 4; i++) {
      }
      System.out.println(i);
  ''', check="out", diff="medium", facets=["numbers", "lists"])
Q(L, "tracing a loop", "What does this print?",
  ["81", "27", "50", "243"],
  ["Correct. x goes 1, 3, 9, 27, 81; at 81 the test x < 50 fails.",
   "Wrong. 27 is still below 50, so it is tripled again.",
   "Wrong. x only ever holds powers of 3.",
   "Wrong. The loop stops at 81."],
  "The test happens before each pass; the last value is the first one that fails it.",
  body='''
      int x = 1;
      while (x < 50) {
          x *= 3;
      }
      System.out.println(x);
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "the dry-run method", "Why does the dry-run table include the pass where the loop test FAILS?",
  ["It shows why the loop stopped, which is where off-by-one answers are caught", "It prints an extra line",
   "The examiner does not want it", "The body runs once more on that pass"],
  ["Correct. The failing test decides the answer between < and <=.",
   "Wrong. Nothing is printed on that pass.",
   "Wrong. Writing it is the habit that catches the error.",
   "Wrong. The body does not run when the test fails."],
  "A table, one row per pass, including the pass that fails the test.",
  diff="easy", facets=["lists"])

# ============================================================ Lesson 2.1
L = "2.1"
Q(L, "the ladder", "What does this print?",
  ["Grade: D", "Grade: C", "Grade: F", "Grade: B"],
  ["Correct. 45 fails 70, 60 and 50, then matches 45, and the ladder stops.",
   "Wrong. 45 is not >= 50.",
   "Wrong. 45 >= 45 is true, so the else is never reached.",
   "Wrong. 45 is far below 60."],
  "A ladder runs exactly one block: the first whose condition is true.",
  body='''
      int score = 45;
      char grade;
      if (score >= 70) {
          grade = 'A';
      } else if (score >= 60) {
          grade = 'B';
      } else if (score >= 50) {
          grade = 'C';
      } else if (score >= 45) {
          grade = 'D';
      } else {
          grade = 'F';
      }
      System.out.println("Grade: " + grade);
  ''', check="out", diff="easy", facets=["lists"])
Q(L, "separate ifs", "Four separate ifs instead of a ladder. What does this print?",
  ["D", "A", "F", "ABCD"],
  ["Correct. All four tests are made; 95 passes each, so each assignment overwrites the last and D is left.",
   "Wrong. A was set first, then overwritten three times.",
   "Wrong. At least one test matched.",
   "Wrong. g holds one char, replaced each time."],
  "Separate ifs are all tested and the last match wins. The paper asks for a ladder, and says so.",
  body='''
      int score = 95;
      char g = 'F';
      if (score >= 70) g = 'A';
      if (score >= 60) g = 'B';
      if (score >= 50) g = 'C';
      if (score >= 45) g = 'D';
      System.out.println(g);
  ''', check="out", diff="medium", facets=["lists"])
Q(L, "a stray semicolon", "What does this print?",
  ["big\nend", "end", "It does not compile", "big"],
  ["Correct. if (x > 5); is a complete, empty if; the braces after it are an ordinary block that always runs.",
   "Wrong. The block is not controlled by the if.",
   "Wrong. It compiles, which is what makes it dangerous.",
   "Wrong. end prints after the block."],
  "A semicolon straight after the condition ends the if. The block that follows runs every time.",
  body='''
      int x = 3;
      if (x > 5); {
          System.out.println("big");
      }
      System.out.println("end");
  ''', check="out", diff="hard", facets=["wording"])
Q(L, "nested if-else", "What does this print?",
  ["Discount 5%", "Discount 10%", "Discount 15%", "Discount 25%"],
  ["Correct. Silver is not Gold, so the outer else runs; days is not 3, so the inner else gives 5.",
   "Wrong. 10 needs 3 days.",
   "Wrong. 15 is the Gold path.",
   "Wrong. 25 is Gold with 3 days."],
  "The outer test picks a pair, the inner test picks one of that pair. Compare Strings with equals.",
  body='''
      String tier = "Silver";
      int days = 2;
      int discount;
      if (tier.equals("Gold")) {
          if (days == 3) {
              discount = 25;
          } else {
              discount = 15;
          }
      } else {
          if (days == 3) {
              discount = 10;
          } else {
              discount = 5;
          }
      }
      System.out.println("Discount " + discount + "%");
  ''', check="out", diff="medium", facets=["lists"])
Q(L, "validation", "Which Java condition accepts a score from 0 to 100 inclusive?",
  ["score >= 0 && score <= 100", "0 <= score <= 100", "score >= 0 || score <= 100", "score > 0 && score < 100"],
  ["Correct. Both comparisons, joined with &&.",
   "Wrong. Java cannot chain comparisons; that does not compile.",
   "Wrong. || is true for every number.",
   "Wrong. That excludes 0 and 100."],
  "Java has no 0 <= score <= 100: write both comparisons and join them.",
  diff="easy", facets=["wording"])
Q(L, "chained comparisons", "What happens when this is compiled?",
  [NOCOMPILE + ": Java cannot chain comparisons like this", "It prints ok", "It prints nothing", "It prints true"],
  ["Correct. 0 <= score gives a boolean, and a boolean cannot be compared with <= 100.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "Write score >= 0 && score <= 100.",
  body='''
      int score = 50;
      if (0 <= score <= 100) {
          System.out.println("ok");
      }
  ''', check="compile", diff="medium", facets=["wording"])
Q(L, "control structures", "Which control structure do if and switch belong to?",
  ["Selection", "Sequence", "Iteration", "Recursion"],
  ["Correct. Selection chooses between alternatives so that only one runs.",
   "Wrong. Sequence is statements one after another.",
   "Wrong. Iteration is for, while and do-while.",
   "Wrong. Not one of the three control structures."],
  "Sequence, selection, iteration.",
  diff="easy", facets=["names"])
TF(L, "braces", "True or false: without braces, an else attaches to the nearest unmatched if.",
   "true",
   "Correct. That is why an else can silently attach to the wrong if.",
   "Wrong. It attaches to the nearest unmatched if, whatever the indentation says.",
   "Braces on every if and every else, always.",
   diff="medium", facets=["wording"])

# ============================================================ Lesson 2.2
L = "2.2"
Q(L, "fall-through", "What does this print?",
  ["two\nthree", "two", "two\nthree\nfour", "one\ntwo\nthree"],
  ["Correct. It matches case 2, prints, falls into case 3, prints, and meets the break.",
   "Wrong. With no break after case 2 it falls into case 3.",
   "Wrong. The break after case 3 stops it.",
   "Wrong. It jumps straight to case 2."],
  "A missing break falls through into the next case until a break or the closing brace.",
  body='''
      int day = 2;
      switch (day) {
          case 1:
              System.out.println("one");
          case 2:
              System.out.println("two");
          case 3:
              System.out.println("three");
              break;
          case 4:
              System.out.println("four");
      }
  ''', check="out", diff="medium", facets=["lists"])
Q(L, "grouped cases", "What does this print?",
  ["Harmattan", "Rainy", "Other", "It does not compile"],
  ["Correct. Cases 12 and 1 fall into case 2, which sets Harmattan and breaks.",
   "Wrong. Month 1 is in the first group.",
   "Wrong. Month 1 matches a case.",
   "Wrong. Empty cases sharing an answer are legal."],
  "Deliberate fall-through is how several values share one answer.",
  body='''
      int month = 1;
      String season;
      switch (month) {
          case 12: case 1: case 2:
              season = "Harmattan";
              break;
          case 6: case 7: case 8:
              season = "Rainy";
              break;
          default:
              season = "Other";
      }
      System.out.println(season);
  ''', check="out", diff="easy", facets=["lists"])
Q(L, "default", "What does this print?",
  ["Price 0.0", "Price 45.0", "Nothing", "It does not compile"],
  ["Correct. 9 matches no case, so default sets the price to 0.0.",
   "Wrong. Case 3 needs day to be 3.",
   "Wrong. The println after the switch always runs.",
   "Wrong. It compiles."],
  "default catches everything else. Always write one.",
  body='''
      int day = 9;
      double price;
      switch (day) {
          case 1: price = 75.0; break;
          case 2: price = 60.0; break;
          case 3: price = 45.0; break;
          default: price = 0.0;
      }
      System.out.println("Price " + price);
  ''', check="out", diff="easy", facets=["lists"])
Q(L, "what a switch takes", "What happens when this is compiled?",
  [NOCOMPILE + ": a switch cannot take a double", "It prints cheap", "It prints nothing", "It prints dear"],
  ["Correct. Switch on byte, short, int, char, String or an enum; never double or boolean.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "You cannot switch on a price, only on something exactly comparable.",
  body='''
      double price = 2.5;
      switch (price) {
          case 2.5: System.out.println("cheap"); break;
          default: System.out.println("dear");
      }
  ''', check="compile", diff="medium", facets=["names"])
Q(L, "switch on a String", "What does this print?",
  ["Good", "Excellent\nGood", "Fail", "It does not compile"],
  ["Correct. A switch can take a String and matches \"B\" exactly.",
   "Wrong. It jumps straight to the matching case.",
   "Wrong. \"B\" has its own case.",
   "Wrong. Switching on a String is allowed."],
  "A switch compares one value against exact constants, and a String is allowed.",
  body='''
      String c = "B";
      switch (c) {
          case "A": System.out.println("Excellent"); break;
          case "B": System.out.println("Good"); break;
          default: System.out.println("Fail");
      }
  ''', check="out", diff="easy", facets=["names"])
Q(L, "no match, no default", "What does this print?",
  ["none", "one", "two", "Nothing at all"],
  ["Correct. Nothing matches and there is no default, so label keeps its starting value.",
   "Wrong. code is 7.",
   "Wrong. code is 7.",
   "Wrong. The println after the switch still runs."],
  "Without a default, an unmatched value does nothing at all.",
  body='''
      int code = 7;
      String label = "none";
      switch (code) {
          case 1: label = "one"; break;
          case 2: label = "two"; break;
      }
      System.out.println(label);
  ''', check="out", diff="easy", facets=["lists"])
Q(L, "case labels", "What happens when this is compiled?",
  [NOCOMPILE + ": a case label must be a constant, and n is a variable", "It prints match",
   "It prints nothing", "It prints 2"],
  ["Correct. The compiler builds the jump table before the program runs, so labels must be constants.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "Every case label must be a literal or a final constant.",
  body='''
      int x = 2;
      int n = 2;
      switch (x) {
          case n: System.out.println("match"); break;
      }
  ''', check="compile", diff="hard", facets=["wording"])
Q(L, "rejecting a value", "What happens when this runs?",
  ["It throws IllegalArgumentException from the default", "It prints 75", "It prints nothing", "It does not compile"],
  ["Correct. 5 matches no case, so default throws the exception.",
   "Wrong. 75 is only for day 1.",
   "Wrong. The throw stops the program with an exception.",
   "Wrong. It compiles."],
  "The paper's ticket question rejects an invalid day with throw in the default.",
  body='''
      int day = 5;
      switch (day) {
          case 1: System.out.println(75); break;
          default: throw new IllegalArgumentException("Day must be 1, 2 or 3");
      }
  ''', check="err:IllegalArgumentException", diff="medium", facets=["names"])
Q(L, "switch or ladder", "Grading a score into bands, 70 and above, 60 and above, and so on. Which structure?",
  ["An if-else ladder, because each band is a range", "A switch, because there are several grades",
   "A switch with a case for every possible score", "A do-while loop"],
  ["Correct. A case must be an exact value; bands are ranges.",
   "Wrong. A switch cannot test a range.",
   "Wrong. Possible, but absurd, and not what the paper expects.",
   "Wrong. Nothing here repeats."],
  "Switch for exact values, ladder for ranges.",
  diff="easy", facets=["wording"])

# ============================================================ Lesson 2.3
L = "2.3"
Q(L, "do-while", "What does this print?",
  ["10", "Nothing", "10\n11\n12\n13\n14", "It loops for ever"],
  ["Correct. A do-while runs its body once before testing, and 11 < 5 is then false.",
   "Wrong. The body runs before the test.",
   "Wrong. After the first pass the test fails.",
   "Wrong. The test fails after one pass."],
  "A do-while always runs at least once: its test comes after the body.",
  body='''
      int n = 10;
      do {
          System.out.println(n);
          n++;
      } while (n < 5);
  ''', check="out", diff="medium", facets=["lists"])
Q(L, "while", "What does this print?",
  ["after", "10\nafter", "Nothing", "It loops for ever"],
  ["Correct. 10 < 5 is false at the start, so the while body never runs.",
   "Wrong. A while tests first.",
   "Wrong. The line after the loop still runs.",
   "Wrong. The body never runs, so it cannot loop."],
  "A while may run zero times; a do-while always runs once.",
  body='''
      int n = 10;
      while (n < 5) {
          System.out.println(n);
          n++;
      }
      System.out.println("after");
  ''', check="out", diff="easy", facets=["lists"])
Q(L, "nested loops", "What does this print?",
  ["1 2 3\n2 4 6", "1 2 3 2 4 6", "1 2\n2 4\n3 6", "1\n2\n3\n2\n4\n6"],
  ["Correct. Each outer pass prints a row of three, and println ends the row.",
   "Wrong. The println in the outer loop breaks the rows.",
   "Wrong. The inner loop runs three times, so each row has three values.",
   "Wrong. The inner loop uses print, so a row stays on one line."],
  "Which loop is each statement inside? That decides a row against a grid.",
  body='''
      for (int i = 1; i <= 2; i++) {
          for (int j = 1; j <= 3; j++) {
              System.out.print(i * j + " ");
          }
          System.out.println();
      }
  ''', check="out", diff="medium", facets=["numbers", "lists"])
Q(L, "counting down", "What does this print?",
  ["10 7 4 1", "10 7 4 1 -2", "10 7 4", "9 6 3"],
  ["Correct. Start 10, subtract 3 while i > 0: 10, 7, 4, 1.",
   "Wrong. -2 fails i > 0.",
   "Wrong. 1 > 0, so 1 is printed.",
   "Wrong. It starts at 10."],
  "start; test; step: the test is made before every pass.",
  body='''
      for (int i = 10; i > 0; i -= 3) {
          System.out.print(i + " ");
      }
  ''', check="out", diff="easy", facets=["numbers"])
Q(L, "a stray semicolon", "What does this print?",
  ["1", "5", "0", "It does not compile"],
  ["Correct. for (...); is a complete empty loop; the block after it is ordinary code that runs once.",
   "Wrong. The block is not the loop's body.",
   "Wrong. The block runs once.",
   "Wrong. It compiles, which is what makes it dangerous."],
  "A semicolon after the for line is a complete empty loop.",
  body='''
      int count = 0;
      for (int i = 0; i < 5; i++);
      {
          count++;
      }
      System.out.println(count);
  ''', check="out", diff="hard", facets=["numbers"])
Q(L, "loop scope", "What happens when this is compiled?",
  [NOCOMPILE + ": i exists only inside the for loop", "It prints 3", "It prints 2", "It prints 0"],
  ["Correct. A variable declared in the for header does not exist after the loop.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "Declare the counter before the loop if you need it afterwards.",
  body='''
      for (int i = 0; i < 3; i++) {
      }
      System.out.println(i);
  ''', check="compile", diff="medium", facets=["wording"])
Q(L, "the accumulator", "The total is declared INSIDE the loop. What does this print?",
  ["9", "18", "0", "It does not compile"],
  ["Correct. The last line uses last, which holds the final item. total resets every pass and cannot be seen outside anyway.",
   "Wrong. Nothing adds all the items outside the loop.",
   "Wrong. last holds 9.",
   "Wrong. The program prints last, which is declared outside."],
  "Declaring the total inside the loop resets it every pass; declare it before, add inside, print after.",
  body='''
      int[] a = {4, 5, 9};
      int last = 0;
      for (int i = 0; i < a.length; i++) {
          int total = 0;
          total += a[i];
          last = total;
      }
      System.out.println(last);
  ''', check="out", diff="hard", facets=["numbers", "lists"])
Q(L, "choosing a loop", "Which loop is guaranteed to run its body at least once?",
  ["do-while", "while", "for", "None of them"],
  ["Correct. Its test comes after the body.",
   "Wrong. A while tests first and may never run.",
   "Wrong. A for tests first too.",
   "Wrong. The do-while always runs once."],
  "for counts, while waits, do-while waits but always goes once. A do-while ends with a semicolon.",
  diff="easy", facets=["names"])
Q(L, "counting passes", "What does this print?",
  ["10", "9", "12", "11"],
  ["Correct. With <=, a loop from 3 to 12 runs last minus first plus one times: 12 - 3 + 1 = 10.",
   "Wrong. <= includes 12.",
   "Wrong. It starts at 3, not 1.",
   "Wrong. Count them: 3 to 12 is ten numbers."],
  "Count the passes before you trace: last minus first plus one, for a <= test.",
  body='''
      int count = 0;
      for (int i = 3; i <= 12; i++) {
          count++;
      }
      System.out.println(count);
  ''', check="out", diff="easy", facets=["numbers"])

# ============================================================ Lesson 2.4
REF_FOR = '''
      int sum = 0;
      for (int k = 1; k <= 4; k++) {
          sum += k;
      }
      System.out.println(sum);
'''
L = "2.4"
Q(L, "for to while", "Which while loop does exactly what this for loop does?",
  ["int k = 1; while (k <= 4) { sum += k; k++; }",
   "int k = 1; while (k <= 4) { k++; sum += k; }",
   "int k = 1; while (k < 4) { sum += k; k++; }",
   "int k = 1; while (k <= 4) { sum += k; }"],
  ["Correct. Start above, test unchanged, step at the bottom: the sum is 10, the same as the for.",
   "Wrong. Stepping BEFORE adding adds 2, 3, 4 and 5, giving 14.",
   "Wrong. The test changed from <= to <, so 4 is never added.",
   "Wrong. The step is missing, so k stays 1 and the loop never ends."],
  "Start goes above, test stays put, step goes to the bottom. Then check the output is identical.",
  body=REF_FOR, check="equiv",
  equiv=['''int sum = 0; int k = 1; while (k <= 4) { sum += k; k++; } System.out.println(sum);''',
         '''int sum = 0; int k = 1; while (k <= 4) { k++; sum += k; } System.out.println(sum);''',
         '''int sum = 0; int k = 1; while (k < 4) { sum += k; k++; } System.out.println(sum);''',
         '''int sum = 0; int k = 1; while (k <= 4) { sum += k; } System.out.println(sum);'''],
  diff="hard", facets=["lists"])
Q(L, "the double step", "Half converted: the step is in the header AND the body. What does this print?",
  ["25", "55", "30", "It loops for ever"],
  ["Correct. i goes up by 2 each pass, 1, 3, 5, 7, 9, so only the odd numbers are added: 25.",
   "Wrong. That is the sum of 1 to 10, which would need one step per pass.",
   "Wrong. The even numbers are skipped, not the odd.",
   "Wrong. i still passes 10, so it stops."],
  "Leaving the step in the body as well as the header double-steps the counter.",
  body='''
      int total = 0;
      for (int i = 1; i <= 10; i++) {
          total += i;
          i++;
      }
      System.out.println(total);
  ''', check="out", diff="hard", facets=["numbers"])
Q(L, "continue in a converted loop", "This for loop is converted to a while with i++ as the last line of the body. What goes wrong?",
  ["When i is 3, continue skips the i++, so i stays 3 and the while loop never ends",
   "Nothing; the while prints the same result", "The while version skips 4 as well", "The while version does not compile"],
  ["Correct. In a for, continue still runs the step; in the while, the step at the bottom is jumped over.",
   "Wrong. continue changes the meaning once the step is in the body.",
   "Wrong. It does not reach 4 at all.",
   "Wrong. It compiles; it just never stops."],
  "Convert a loop containing continue with care, and say so in your answer.",
  body='''
      int sum = 0;
      for (int i = 1; i <= 5; i++) {
          if (i == 3) continue;
          sum += i;
      }
      System.out.println(sum);
  ''', check=None, diff="hard", facets=["wording"])
Q(L, "the three homes", "Where does the STEP of a for header go in the while version?",
  ["On the last line inside the loop body", "Above the loop", "Inside the while brackets", "After the loop"],
  ["Correct. Start above, test in the brackets, step at the bottom of the body.",
   "Wrong. That is where the start goes.",
   "Wrong. That is where the test goes.",
   "Wrong. After the loop it would run only once."],
  "Start goes above. Test stays put. Step goes to the bottom of the body.",
  diff="easy", facets=["lists"])
Q(L, "while to for", "What does this print?",
  ["128", "64", "100", "256"],
  ["Correct. n doubles 1, 2, 4, ..., 64, 128; at 128 the test n < 100 fails.",
   "Wrong. 64 is still below 100, so it doubles again.",
   "Wrong. n only ever holds powers of 2.",
   "Wrong. The loop stops at 128."],
  "As a for loop: for (int n = 1; n < 100; n *= 2) { }, and the printed value is the same.",
  body='''
      int n = 1;
      while (n < 100) {
          n *= 2;
      }
      System.out.println(n);
  ''', check="out", diff="medium", facets=["numbers"])
TF(L, "scope after conversion", "True or false: a counter declared in a for header can still be used after the loop.",
   "false",
   "Wrong. It exists only inside the loop.",
   "Correct. In the while version the counter outlives the loop; in the for version it does not.",
   "That is the one real difference between the two forms.",
   diff="medium", facets=["wording"])

# ============================================================ Lesson 2.5
L = "2.5"
Q(L, "break in a nested loop", "What does this print?",
  ["11 12 21 22 31 32", "11 12", "11 12 13 21 22 23 31 32 33", "11 21 31"],
  ["Correct. break leaves only the inner loop, at j = 3, so each outer pass prints two values.",
   "Wrong. The outer loop carries on after the inner break.",
   "Wrong. j = 3 is never printed.",
   "Wrong. The break is at 3, not 2."],
  "break and continue act on the innermost loop only.",
  body='''
      for (int i = 1; i <= 3; i++) {
          for (int j = 1; j <= 3; j++) {
              if (j == 3) break;
              System.out.print(i + "" + j + " ");
          }
      }
  ''', check="out", diff="medium", facets=["numbers", "lists"])
Q(L, "skip, process, count, stop", "What does this print?",
  ["32 2", "62 3", "12 1", "78 6"],
  ["Correct. 5 and 3 are skipped; 12 and 20 are added and counted; at a count of 2 the loop breaks before 30.",
   "Wrong. The break at a count of 2 stops before 30.",
   "Wrong. 20 is added before the break.",
   "Wrong. Items under 10 are skipped, and the loop breaks early."],
  "Skip first, then process, then count, then decide whether to stop: the Section A pattern.",
  body='''
      int[] a = {5, 12, 3, 20, 8, 30};
      int count = 0, total = 0;
      for (int i = 0; i < a.length; i++) {
          if (a[i] < 10) continue;
          total += a[i];
          count++;
          if (count == 2) break;
      }
      System.out.println(total + " " + count);
  ''', check="out", diff="hard", facets=["numbers", "lists"])
Q(L, "count above the skip", "The count is placed ABOVE the continue. What does this print?",
  ["4", "2", "0", "1"],
  ["Correct. count++ runs for every item before the skip happens, so it counts all four.",
   "Wrong. That would need count++ after the continue.",
   "Wrong. count++ runs every pass.",
   "Wrong. It runs on all four passes."],
  "Anything above the continue runs for every item, including the ones you meant to skip.",
  body='''
      int[] a = {5, 12, 3, 20};
      int count = 0;
      for (int i = 0; i < a.length; i++) {
          count++;
          if (a[i] < 10) continue;
      }
      System.out.println(count);
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "printing money", "What does this print?",
  ["3.3000000000000003\n3.3", "3.3\n3.3", "3.3\n3.30", "3.3000000000000003\n3.30"],
  ["Correct. A double cannot hold 1.1 exactly, so the raw value shows a tail; printf with %.1f shows one decimal place.",
   "Wrong. println shows the exact double, tail included.",
   "Wrong. The first line shows the tail.",
   "Wrong. %.1f shows ONE decimal place."],
  "Compute money in double, print it with printf and a stated number of decimal places.",
  body='''
      double t = 1.1 * 3;
      System.out.println(t);
      System.out.printf("%.1f%n", t);
  ''', check="out", diff="hard", facets=["numbers"])
Q(L, "leaving both loops", "What does this print?",
  ["23", "32", "16", "-1"],
  ["Correct. The first pair with i * j == 6 is i = 2, j = 3; the flag then stops the outer loop too.",
   "Wrong. i = 2, j = 3 is found before i = 3, j = 2.",
   "Wrong. found is set as i * 10 + j.",
   "Wrong. A pair is found."],
  "To leave two loops, set a boolean flag and test it in the outer condition.",
  body='''
      boolean stop = false;
      int found = -1;
      for (int i = 1; i <= 5 && !stop; i++) {
          for (int j = 1; j <= 5; j++) {
              if (i * j == 6) {
                  found = i * 10 + j;
                  stop = true;
                  break;
              }
          }
      }
      System.out.println(found);
  ''', check="out", diff="hard", facets=["numbers"])
Q(L, "continue", "In a FOR loop, what does continue do?",
  ["Skips the rest of this pass, runs the step, and goes on to the test", "Leaves the loop entirely",
   "Restarts the loop from its start value", "Skips the step as well"],
  ["Correct. In a for loop the step still happens.",
   "Wrong. That is break.",
   "Wrong. The counter keeps its value and moves on.",
   "Wrong. In a for loop the step is not skipped; in a while loop a step at the bottom would be."],
  "continue skips one, break stops them all.",
  diff="medium", facets=["wording"])

# ============================================================ Lesson 2.6
L = "2.6"
Q(L, "passing an array", "What does this print?",
  ["42 2", "1 2", "42 1", "It does not compile"],
  ["Correct. The method gets a copy of the REFERENCE, which points at the same array, so the change is visible.",
   "Wrong. A change made through the copied reference reaches the same array.",
   "Wrong. The array still has two elements.",
   "Wrong. It compiles."],
  "Java is always pass by value; for an object the value copied is the reference.",
  methods='''
      static void fill(int[] a) {
          a[0] = 42;
      }
  ''', body='''
      int[] v = {1, 2};
      fill(v);
      System.out.println(v[0] + " " + v.length);
  ''', check="out", diff="hard", facets=["numbers"])
Q(L, "value returning", "What does this print?",
  ["25", "7", "14", "12"],
  ["Correct. sq(3) returns 9 and sq(4) returns 16; 9 + 16 is 25.",
   "Wrong. sq squares; it does not return its argument.",
   "Wrong. Squaring, not doubling.",
   "Wrong. 9 + 16 is 25."],
  "A call to a value returning method is a value, so two can be added.",
  methods='''
      static int sq(int n) {
          return n * n;
      }
  ''', body='''
      System.out.println(sq(3) + sq(4));
  ''', check="out", diff="easy", facets=["numbers"])
Q(L, "void is not a value", "What happens when this is compiled?",
  [NOCOMPILE + ": show is void, so there is no value to store", "It prints the number is 5, then 0",
   "It prints the number is 5", "It prints 5"],
  ["Correct. A void call is a statement, not a value.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "A void method performs an action and returns nothing; a value returning method hands a result back with return.",
  methods='''
      static void show(int n) {
          System.out.println("the number is " + n);
      }
  ''', body='''
      int y = show(5);
  ''', check="compile", diff="medium", facets=["wording"])
Q(L, "every path returns", "What happens when this is compiled?",
  [NOCOMPILE + ": there is a path (n == 0) with no return", "It prints 1", "It prints 0", "It prints -1"],
  ["Correct. A value returning method must return on every route out.",
   "Wrong. It never compiles.",
   "Wrong. Java does not invent a return value.",
   "Wrong. It never compiles."],
  "Every route out of a value returning method must return, including the one nobody tested.",
  methods='''
      static int sign(int n) {
          if (n > 0) {
              return 1;
          } else if (n < 0) {
              return -1;
          }
      }
  ''', body='''
      System.out.println(sign(5));
  ''', check="compile", diff="hard", facets=["wording"])
Q(L, "static", "twice is not static. What happens when this is compiled?",
  [NOCOMPILE + ": main is static and there is no object to call twice on", "It prints 8", "It prints 4", "It prints 0"],
  ["Correct. A method called from main without an object must be static.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "Forgetting static on a helper is one of the commonest first-exam compile errors.",
  methods='''
      int twice(int n) {
          return 2 * n;
      }
  ''', body='''
      System.out.println(twice(4));
  ''', check="compile", diff="medium", facets=["names"])
Q(L, "parameter and argument", "A method is declared area(double w, double h) and called as area(width, 3.0). Which are the arguments?",
  ["width and 3.0", "w and h", "area and double", "w and 3.0"],
  ["Correct. Arguments are the values supplied at the call.",
   "Wrong. w and h are the parameters, the names in the header.",
   "Wrong. Those are the name and a type.",
   "Wrong. w is a parameter."],
  "The parameter is the name in the header; the argument is the value passed at the call.",
  diff="easy", facets=["wording"])
Q(L, "calls in order", "What does this print?",
  ["f1 f2 3", "f2 f1 3", "f1 3", "f1 f2 2"],
  ["Correct. The inner call f(1) runs first, printing f1 and returning 2; then f(2) prints f2 and returns 3.",
   "Wrong. The inner call happens first.",
   "Wrong. f is called twice.",
   "Wrong. f(2) returns 3."],
  "Arguments are worked out before the method they are passed to runs.",
  methods='''
      static int f(int n) {
          System.out.print("f" + n + " ");
          return n + 1;
      }
  ''', body='''
      int r = f(f(1));
      System.out.println(r);
  ''', check="out", diff="hard", facets=["numbers"])

# ============================================================ Lesson 2.7
L = "2.7"
Q(L, "choosing an overload", "What does this print?",
  ["int double int", "int double char", "int double String", "It does not compile"],
  ["Correct. 7 matches int, 7.5 matches double, and 'A' has no char version, so it widens to int.",
   "Wrong. There is no kind(char), so 'A' widens to int.",
   "Wrong. 'A' is a char, not a String.",
   "Wrong. Each call matches a method."],
  "The compiler chooses by the signature: the number, types and order of the arguments.",
  methods='''
      static String kind(int x) { return "int"; }
      static String kind(double x) { return "double"; }
      static String kind(String x) { return "String"; }
  ''', body='''
      System.out.println(kind(7) + " " + kind(7.5) + " " + kind('A'));
  ''', check="out", diff="hard", facets=["names"])
Q(L, "the return type is not the signature", "What happens when this is compiled?",
  [NOCOMPILE + ": the two methods have the same signature", "It prints 2", "It prints 2.0", "It prints 2 and 2.0"],
  ["Correct. The signature is the name plus the parameter list; the return type is not part of it.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "Two methods differing only in return type cannot coexist: the compiler could never tell them apart.",
  methods='''
      static int f(int a) { return a; }
      static double f(int a) { return a; }
  ''', body='''
      System.out.println(f(2));
  ''', check="compile", diff="hard", facets=["wording"])
Q(L, "the signature", "What exactly is a method signature?",
  ["The method name together with the number, types and order of its parameters",
   "The return type and the method name", "The method's first line, including public static",
   "The values passed at the call"],
  ["Correct. And it does NOT include the return type.",
   "Wrong. The return type is not part of the signature.",
   "Wrong. Modifiers are not part of it.",
   "Wrong. Those are arguments."],
  "Signature is name plus parameter list. Never the return type.",
  diff="medium", facets=["wording"])
Q(L, "static fields", "What does this print?",
  ["2 3", "1 3", "3 3", "2 1"],
  ["Correct. made is one shared counter, 3 after three objects; b was the second, so its id is 2.",
   "Wrong. b was made second.",
   "Wrong. Each object has its own id.",
   "Wrong. made is shared, so it counts all three."],
  "static is one shared copy; an instance field is one copy per object.",
  classes='''
      class Box {
          static int made = 0;
          int id;
          Box() {
              made++;
              id = made;
          }
      }
  ''', body='''
      Box a = new Box();
      Box b = new Box();
      Box c = new Box();
      System.out.println(b.id + " " + Box.made);
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "static context", "count is an instance field. What happens when this is compiled?",
  [NOCOMPILE + ": a static method cannot use an instance field directly", "It prints 1", "It prints 0", "It prints nothing"],
  ["Correct. main is static and may run when no object exists, so there is no count to mean.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "\"non-static variable cannot be referenced from a static context\" is the commonest first-exam compile error.",
  methods='''
      int count = 0;
  ''', body='''
      count++;
      System.out.println(count);
  ''', check="compile", diff="medium", facets=["names"])
Q(L, "legal overloads", "Do void f(int a, double b) and void f(double a, int b) overload legally in one class?",
  ["Yes, because the order of the parameter types differs", "No, because they have the same types",
   "No, because both return void", "Only if one is static"],
  ["Correct. Same types in a different order makes a different signature.",
   "Wrong. Order is part of the signature.",
   "Wrong. The return type plays no part.",
   "Wrong. static has nothing to do with it."],
  "Number, types and order: change any of the three and the signature differs.",
  diff="medium", facets=["wording"])
TF(L, "compile time", "True or false: an overloaded call is resolved at run time, from the actual object.",
   "false",
   "Wrong. Overloading is resolved at compile time; it is OVERRIDING that is decided at run time.",
   "Correct. The compiler picks the overload from the signature, before anything runs.",
   "Overloading is static, or compile time, polymorphism.",
   diff="medium", facets=["wording"])

# ============================================================ Lesson 2.8
L = "2.8"
Q(L, "the last index", "What does this print?",
  ["16 4", "15 4", "16 3", "an ArrayIndexOutOfBoundsException"],
  ["Correct. The last index is length - 1, which is 3, holding 16; length is 4.",
   "Wrong. Index 3 holds 16.",
   "Wrong. length counts the elements, 4.",
   "Wrong. a.length - 1 is a valid index."],
  "The last index is always length - 1.",
  body='''
      int[] a = {4, 8, 15, 16};
      System.out.println(a[a.length - 1] + " " + a.length);
  ''', check="out", diff="easy", facets=["numbers"])
Q(L, "one step too far", "What happens when this runs?",
  ["It throws ArrayIndexOutOfBoundsException", "It prints 16", "It prints 0", "It does not compile"],
  ["Correct. Valid indexes run 0 to 3; index 4 is past the end.",
   "Wrong. 16 is at index 3.",
   "Wrong. Java does not give a default for a missing index.",
   "Wrong. It compiles; the fault shows only when it runs."],
  "i <= a.length is one step too far, every time.",
  body='''
      int[] a = {4, 8, 15, 16};
      System.out.println(a[a.length]);
  ''', check="err:ArrayIndexOutOfBoundsException", diff="medium", facets=["numbers"])
Q(L, "count matching", "What does this print?",
  ["1", "3", "2", "0"],
  ["Correct. Only 12 is strictly above 9; the two 9s are not.",
   "Wrong. > does not include 9.",
   "Wrong. Only one value is above 9.",
   "Wrong. 12 is above 9."],
  "Count matching: n = 0, if the test passes n++, return n.",
  methods='''
      static int countAbove(int[] a, int mark) {
          int n = 0;
          for (int i = 0; i < a.length; i++) {
              if (a[i] > mark) {
                  n++;
              }
          }
          return n;
      }
  ''', body='''
      System.out.println(countAbove(new int[]{3, 9, 12, 9}, 9));
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "find first", "What does this print?",
  ["0 -1", "2 -1", "0 0", "1 -1"],
  ["Correct. 7 is found first at index 0 and the method returns at once; 5 is absent, so -1.",
   "Wrong. The method returns the FIRST match.",
   "Wrong. -1 means not found.",
   "Wrong. Index 0 holds 7."],
  "Return from inside the loop on the first match; return -1 after the loop.",
  methods='''
      static int firstIndexOf(int[] a, int wanted) {
          for (int i = 0; i < a.length; i++) {
              if (a[i] == wanted) {
                  return i;
              }
          }
          return -1;
      }
  ''', body='''
      int[] a = {7, 3, 7, 1};
      System.out.println(firstIndexOf(a, 7) + " " + firstIndexOf(a, 5));
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "consecutive duplicates", "What does this print?",
  ["3", "2", "5", "4"],
  ["Correct. Indexes 1 and 2 equal the 1 before them, and index 4 equals the 2 before it.",
   "Wrong. A run of three 1s gives two matches, not one.",
   "Wrong. Each match compares a position with the one before it.",
   "Wrong. The 3 at the end has no equal neighbour."],
  "The neighbour walk starts at 1 and compares a[i] with a[i - 1]; a run of three gives two matches.",
  methods='''
      static int countConsecutive(int[] a) {
          int n = 0;
          for (int i = 1; i < a.length; i++) {
              if (a[i] == a[i - 1]) {
                  n++;
              }
          }
          return n;
      }
  ''', body='''
      System.out.println(countConsecutive(new int[]{1, 1, 1, 2, 2, 3}));
  ''', check="out", diff="hard", facets=["numbers"])
Q(L, "two dimensions", "What does this print?",
  ["3 5", "2 5", "3 4", "2 3"],
  ["Correct. Row 1 is {3, 4, 5}: its length is 3 and its index 2 is 5.",
   "Wrong. m[1].length is the width of row 1, which is 3.",
   "Wrong. m[1][2] is the third item of row 1.",
   "Wrong. m.length would be 2; m[1].length is 3."],
  "The first index picks the row, the second picks within it; each row has its own length.",
  body='''
      int[][] m = {{1, 2}, {3, 4, 5}};
      System.out.println(m[1].length + " " + m[1][2]);
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "an int array of decimals", "What happens when this is compiled?",
  [NOCOMPILE + ": 1.5 and 2.0 are doubles, which do not fit an int array", "It prints 1", "It prints 1.5", "It prints 2"],
  ["Correct. This is the planted error from the last paper: fix it with double[] or whole values.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "An int[] filled with decimals does not compile, and it is on the 2025/2026 paper.",
  body='''
      int[] a = {1.5, 2.0};
      System.out.println(a[0]);
  ''', check="compile", diff="easy", facets=["names"])
Q(L, "length against length()", "What happens when this is compiled?",
  [NOCOMPILE + ": an array's length is a field, written without brackets", "It prints 3", "It prints 2", "It prints 0"],
  ["Correct. Arrays have a length field; Strings have a length() method.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "a.length for an array, s.length() for a String. The examiner plants the swap.",
  body='''
      int[] a = {1, 2, 3};
      System.out.println(a.length());
  ''', check="compile", diff="medium", facets=["names"])
Q(L, "an average", "What does this print?",
  ["3.25", "3", "3.0", "13"],
  ["Correct. The total is 13, and casting it to double before dividing by 4 gives 3.25.",
   "Wrong. The cast makes this a double division.",
   "Wrong. The cast happens before the division, so the remainder survives.",
   "Wrong. That is the total, not the average."],
  "An average of an int array needs a cast on one side of the division.",
  body='''
      int[] a = {2, 3, 4, 4};
      int s = 0;
      for (int i = 0; i < a.length; i++) {
          s += a[i];
      }
      System.out.println((double) s / a.length);
  ''', check="out", diff="medium", facets=["numbers"])

# ============================================================ Lesson 2.9
L = "2.9"
Q(L, "substring, charAt, indexOf", "What does this print?",
  ["AMI I 5", "AMIN I 5", "AMI N 5", "AMI I 6"],
  ["Correct. substring(2, 5) takes indexes 2 to 4; charAt(4) is I; NATION starts at index 5.",
   "Wrong. substring stops BEFORE its end index.",
   "Wrong. Index 4 is I; N is at 5.",
   "Wrong. Count from 0: N of NATION is at index 5."],
  "substring(a, b) runs from a up to but not including b; indexes start at 0.",
  body='''
      String s = "EXAMINATION";
      System.out.println(s.substring(2, 5) + " " + s.charAt(4) + " " + s.indexOf("NATION"));
  ''', check="out", diff="hard", facets=["numbers", "names"])
Q(L, "equals", "What does this print?",
  ["false true", "true true", "false false", "true false"],
  ["Correct. equals compares characters exactly, so case matters; equalsIgnoreCase does not care about case.",
   "Wrong. Gold and gold differ in case.",
   "Wrong. equalsIgnoreCase ignores case.",
   "Wrong. They are the other way round."],
  "Always compare text with equals; use equalsIgnoreCase for anything the user typed.",
  body='''
      String a = "Gold";
      String b = "gold";
      System.out.println(a.equals(b) + " " + a.equalsIgnoreCase(b));
  ''', check="out", diff="easy", facets=["names"])
Q(L, "immutability", "What does this print?",
  ["java JAVA", "JAVA JAVA", "java! JAVA", "JAVA! JAVA"],
  ["Correct. Every String method returns a new String; s is never changed, and the concat result was thrown away.",
   "Wrong. toUpperCase made a copy for t; s is unchanged.",
   "Wrong. The concat result was never assigned.",
   "Wrong. s is still java."],
  "A String is immutable: if you did not assign the result, nothing happened.",
  body='''
      String s = "java";
      String t = s.toUpperCase();
      s.concat("!");
      System.out.println(s + " " + t);
  ''', check="out", diff="medium", facets=["names"])
Q(L, "trim and length", "What does this print?",
  ["[hi]6", "[hi]2", "[  hi  ]6", "[hi]4"],
  ["Correct. trim() returns a copy without the spaces; s itself still has all six characters.",
   "Wrong. s.length() measures the untrimmed s.",
   "Wrong. trim() removes the spaces in the copy that is printed.",
   "Wrong. Two spaces on each side plus two letters is six."],
  "trim() returns a trimmed copy; the original keeps its spaces.",
  body='''
      String s = "  hi  ";
      System.out.println("[" + s.trim() + "]" + s.length());
  ''', check="out", diff="medium", facets=["numbers", "names"])
Q(L, "StringBuilder", "What does this print?",
  ["1-2-3-", "1-2-3", "123", "-1-2-3"],
  ["Correct. Each pass appends the number and a dash, including after the last.",
   "Wrong. A dash is appended after 3 too.",
   "Wrong. Dashes are appended.",
   "Wrong. The number comes before its dash."],
  "StringBuilder changes in place: append adds, toString hands back the finished String.",
  body='''
      StringBuilder sb = new StringBuilder();
      for (int i = 1; i <= 3; i++) {
          sb.append(i).append("-");
      }
      System.out.println(sb.toString());
  ''', check="out", diff="easy", facets=["names"])
Q(L, "length() on a String", "What happens when this is compiled?",
  [NOCOMPILE + ": a String's length is a method, length()", "It prints 5", "It prints 4", "It prints 0"],
  ["Correct. Strings have a length() method; arrays have a length field.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "s.length() for a String, a.length for an array.",
  body='''
      String s = "hello";
      System.out.println(s.length);
  ''', check="compile", diff="medium", facets=["names"])
Q(L, "indexOf", "What does this print?",
  ["-1 1", "0 1", "-1 3", "-1 2"],
  ["Correct. x is absent, so -1; the first an starts at index 1.",
   "Wrong. indexOf gives -1 when the text is absent.",
   "Wrong. indexOf finds the FIRST occurrence.",
   "Wrong. b is index 0, a is index 1."],
  "indexOf(x) is where x starts, or -1 if it is not there.",
  body='''
      System.out.println("banana".indexOf("x") + " " + "banana".indexOf("an"));
  ''', check="out", diff="medium", facets=["numbers", "names"])
Q(L, "replace", "What does this print?",
  ["bonono", "bonana", "banana", "bnn"],
  ["Correct. replace swaps EVERY a for an o and returns the new String.",
   "Wrong. Every occurrence is replaced, not just the first.",
   "Wrong. The replaced copy is what is printed.",
   "Wrong. The a's become o's; they are not removed."],
  "replace(a, b) returns a copy with every a swapped for b.",
  body='''
      System.out.println("banana".replace("a", "o"));
  ''', check="out", diff="easy", facets=["names"])
Q(L, "reading the constraint", "The paper says to build a list \"using plain String concatenation only, no StringBuilder\". What do you use?",
  ["Plain concatenation with +, because the paper said so", "StringBuilder, because it is more efficient",
   "A char array", "Whichever you prefer"],
  ["Correct. Where the paper bans a tool, using it costs the marks whatever the output.",
   "Wrong. It is better in general, but the paper forbade it here.",
   "Wrong. Not what the paper asked for.",
   "Wrong. The constraint decides."],
  "Read the constraint before you choose the tool.",
  diff="easy", facets=["wording"])

# ============================================================ Lesson 3.1
L = "3.1"
Q(L, "default values", "What does this print?",
  ["null 0.0 false", "0 0 false", "null 0 null", "\"\" 0.0 false"],
  ["Correct. An unset object reference is null, a double is 0.0, a boolean is false.",
   "Wrong. A String field starts as null, not 0.",
   "Wrong. price is a double, 0.0, and sold is a boolean, false.",
   "Wrong. An unset String is null, not empty text."],
  "Defaults for fields never set: numbers 0, boolean false, every object reference null.",
  classes='''
      class Item {
          String name;
          double price;
          boolean sold;
      }
  ''', body='''
      Item i = new Item();
      System.out.println(i.name + " " + i.price + " " + i.sold);
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "forgetting this", "What does this print?",
  ["null", "Rex", "name", "It does not compile"],
  ["Correct. name = name assigns the parameter to itself; the field is never set and stays null.",
   "Wrong. Without this, the field is never assigned.",
   "Wrong. name is a variable, not the text \"name\".",
   "Wrong. It compiles, which is why it is dangerous."],
  "this.name = name, on every line of every constructor.",
  classes='''
      class Pet {
          String name;
          Pet(String name) {
              name = name;
          }
      }
  ''', body='''
      Pet p = new Pet("Rex");
      System.out.println(p.name);
  ''', check="out", diff="hard", facets=["names"])
Q(L, "the default constructor", "What happens when this is compiled?",
  [NOCOMPILE + ": writing your own constructor removes the free no-argument one", "It prints null",
   "It prints 0", "It prints nothing"],
  ["Correct. Once you write any constructor, new Student() no longer exists unless you write it too.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "Constructors can be overloaded; write both if you need both.",
  classes='''
      class Student {
          String name;
          Student(String name) {
              this.name = name;
          }
      }
  ''', body='''
      Student s = new Student();
      System.out.println(s.name);
  ''', check="compile", diff="hard", facets=["names"])
Q(L, "one copy per object", "What does this print?",
  ["2 1", "3 3", "1 1", "3 0"],
  ["Correct. Each object has its own n: a was incremented twice and b once.",
   "Wrong. n is an instance field, one per object.",
   "Wrong. a.inc() ran twice.",
   "Wrong. b.inc() ran once."],
  "An attribute is one copy per object; that is the difference between a class and its objects.",
  classes='''
      class Counter {
          int n;
          void inc() {
              n++;
          }
      }
  ''', body='''
      Counter a = new Counter();
      Counter b = new Counter();
      a.inc();
      a.inc();
      b.inc();
      System.out.println(a.n + " " + b.n);
  ''', check="out", diff="easy", facets=["numbers"])
Q(L, "null", "What happens when this runs?",
  ["It throws NullPointerException, because name was never set", "It prints 0", "It prints null", "It does not compile"],
  ["Correct. The field is null, and calling a method on null has no object to ask.",
   "Wrong. There is no String whose length could be 0.",
   "Wrong. The length() call fails before anything prints.",
   "Wrong. It compiles; the fault shows only when it runs."],
  "That is the argument for setting every field in the constructor.",
  classes='''
      class Item {
          String name;
      }
  ''', body='''
      Item i = new Item();
      System.out.println(i.name.length());
  ''', check="err:NullPointerException", diff="medium", facets=["names"])
Q(L, "constructors", "What two things make a constructor different from every other method?",
  ["It has the same name as the class, and no return type at all", "It is static and returns void",
   "It is private and takes no parameters", "It is called with a dot on an object"],
  ["Correct. Those two together are how Java recognises it.",
   "Wrong. A constructor has no return type, not even void.",
   "Wrong. Constructors are usually public and often take parameters.",
   "Wrong. It is run by new."],
  "A constructor shares the class name and has no return type; new runs it.",
  diff="easy", facets=["wording"])
Q(L, "a constructor with void", "What does this print?",
  ["unknown", "Rex", "null", "It does not compile"],
  ["Correct. void Pet(String n) is an ordinary method, not a constructor, so new Pet() uses the default and the field keeps unknown.",
   "Wrong. Nothing ever calls the void method.",
   "Wrong. name was given the starting value unknown.",
   "Wrong. A method may share the class name; it compiles."],
  "Giving a constructor a return type turns it into an ordinary method.",
  classes='''
      class Pet {
          String name = "unknown";
          void Pet(String n) {
              name = n;
          }
      }
  ''', body='''
      Pet p = new Pet();
      System.out.println(p.name);
  ''', check="out", diff="hard", facets=["names"])
Q(L, "class and object", "Which statement correctly defines an OBJECT?",
  ["An instance of a class, created with new, with its own copy of the attributes",
   "A blueprint that defines attributes and methods", "A method with no return type", "A variable declared final"],
  ["Correct. That is an object.",
   "Wrong. That is a class.",
   "Wrong. That describes a constructor.",
   "Wrong. That is a constant."],
  "Class is the blueprint, object is the building, new is the builder.",
  diff="easy", facets=["wording"])

# ============================================================ Lesson 3.2
L = "3.2"
Q(L, "a validating setter", "What does this print?",
  ["80", "150", "0", "It does not compile"],
  ["Correct. 80 is accepted; 150 is refused by the check, so the score stays 80.",
   "Wrong. The setter refuses anything above 100.",
   "Wrong. The first call set it to 80.",
   "Wrong. It compiles."],
  "Encapsulation is what makes validation possible: the setter checks before it changes anything.",
  classes='''
      class Student {
          private int score;
          public void setScore(int s) {
              if (s >= 0 && s <= 100) {
                  score = s;
              }
          }
          public int getScore() {
              return score;
          }
      }
  ''', body='''
      Student st = new Student();
      st.setScore(80);
      st.setScore(150);
      System.out.println(st.getScore());
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "private fields", "What happens when this is compiled?",
  [NOCOMPILE + ": score is private to Student", "It prints 50", "It prints 0", "It throws an exception"],
  ["Correct. A private field is reachable only from inside its own class. Go through a setter.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It is refused at compile time."],
  "Private data, public doors.",
  classes='''
      class Student {
          private int score;
      }
  ''', body='''
      Student st = new Student();
      st.score = 50;
      System.out.println(st.score);
  ''', check="compile", diff="easy", facets=["names"])
Q(L, "access modifiers", "Which list runs from MOST open to MOST closed?",
  ["public, protected, default, private", "private, default, protected, public",
   "public, default, protected, private", "protected, public, private, default"],
  ["Correct. Anywhere; subclasses and package; package only; the class itself only.",
   "Wrong. That is most closed first.",
   "Wrong. protected is more open than default.",
   "Wrong. public is the most open."],
  "Fields private, methods public: private data, public behaviour.",
  diff="medium", facets=["lists"])
Q(L, "protected", "From where can a protected member be reached?",
  ["The class itself, its subclasses, and the same package", "Anywhere at all",
   "The class itself only", "Other packages only"],
  ["Correct. Mine, my children's, and my package's.",
   "Wrong. That is public.",
   "Wrong. That is private.",
   "Wrong. Not what protected means."],
  "protected earns its place when a subclass needs a parent's field.",
  diff="medium", facets=["names"])
Q(L, "what encapsulation buys", "Which two are benefits of encapsulation?",
  ["Control: only the class's own methods change its data", "Validation: a setter can refuse an invalid value",
   "The program always runs faster", "A class can extend two parents"],
  ["Correct. Control is one benefit.",
   "Correct. Validation is one benefit.",
   "Wrong. Speed is not a benefit claimed.",
   "Wrong. Java has no multiple inheritance of classes."],
  "Control, validation and safe change: the internal representation can change without breaking callers.",
  style="multi", key=[0, 1], diff="easy", facets=["lists"])
Q(L, "encapsulation against abstraction", "What is the difference between encapsulation and abstraction?",
  ["Encapsulation hides the data; abstraction hides the implementation", "They are the same idea",
   "Encapsulation hides the implementation; abstraction hides the data", "Abstraction is about constructors"],
  ["Correct. Two different pillars, two different answers.",
   "Wrong. They are separate pillars.",
   "Wrong. This reverses them.",
   "Wrong. Not what abstraction means."],
  "Encapsulation: data behind methods. Abstraction: what a thing does, not how.",
  diff="medium", facets=["wording"])
TF(L, "decoration", "True or false: writing getters and setters while leaving the fields public is still encapsulation.",
   "false",
   "Wrong. The private is the point; with public fields anyone can bypass the methods.",
   "Correct. Without private fields it is decoration, not encapsulation.",
   "Private data, public doors. A setter with no check buys nothing either.",
   diff="medium", facets=["wording"])

# ============================================================ Lesson 3.3
L = "3.3"
Q(L, "super", "What does this print?",
  ["Account 100.0\nSavings 0.1\n10.0", "Savings 0.1\nAccount 100.0\n10.0", "Account 100.0\n10.0", "10.0"],
  ["Correct. super(b) runs the parent constructor first, then the rest of the child's; balance times rate is 10.0.",
   "Wrong. The parent's constructor runs first, through super.",
   "Wrong. The child's constructor prints its line too.",
   "Wrong. Both constructors print."],
  "super(...) calls the parent's constructor and must be the first statement in the child's.",
  classes='''
      class Account {
          double balance;
          Account(double b) {
              balance = b;
              System.out.println("Account " + b);
          }
      }
      class Savings extends Account {
          double rate;
          Savings(double b, double r) {
              super(b);
              rate = r;
              System.out.println("Savings " + r);
          }
      }
  ''', body='''
      Savings s = new Savings(100, 0.1);
      System.out.println(s.balance * s.rate);
  ''', check="out", diff="medium", facets=["lists"])
Q(L, "forgetting super", "What happens when this is compiled?",
  [NOCOMPILE + ": Savings must call super(...) because Account has no no-argument constructor",
   "It prints new", "It prints new and 0.0", "It throws an exception"],
  ["Correct. Java inserts a call to super(), which does not exist here.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It is a compile error."],
  "\"constructor Account in class Account cannot be applied to given types\" means one thing: you forgot super.",
  classes='''
      class Account {
          double balance;
          Account(double b) {
              balance = b;
          }
      }
      class Savings extends Account {
          Savings() {
              System.out.println("new");
          }
      }
  ''', body='''
      Savings s = new Savings();
  ''', check="compile", diff="hard", facets=["wording"])
Q(L, "super goes first", "What happens when this is compiled?",
  [NOCOMPILE + ": super(...) must be the first statement", "It prints x", "It prints nothing", "It prints x and 5.0"],
  ["Correct. The parent's part must exist before the child adds to it.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "extends takes it, super builds it, and super goes first.",
  classes='''
      class Account {
          double balance;
          Account(double b) {
              balance = b;
          }
      }
      class Savings extends Account {
          Savings(double b) {
              System.out.println("x");
              super(b);
          }
      }
  ''', body='''
      Savings s = new Savings(5);
  ''', check="compile", diff="medium", facets=["wording"])
Q(L, "private is not inherited", "What happens when this is compiled?",
  [NOCOMPILE + ": balance is private, so Savings cannot see it", "It prints 1.0", "It prints 0.0", "It throws an exception"],
  ["Correct. Use protected, or go through a getter.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It is a compile error."],
  "private is invisible even to a child; protected means mine and my children's.",
  classes='''
      class Account {
          private double balance;
      }
      class Savings extends Account {
          void add() {
              balance += 1;
          }
      }
  ''', body='''
      new Savings().add();
  ''', check="compile", diff="medium", facets=["names"])
Q(L, "one parent", "How many classes can one Java class extend?",
  ["Exactly one", "Two", "As many as it likes", "None; Java has no inheritance"],
  ["Correct. Java has no multiple inheritance of classes; a class may implement many interfaces instead.",
   "Wrong. One only.",
   "Wrong. That is true of interfaces, not classes.",
   "Wrong. extends is inheritance."],
  "One parent only; use interfaces for more.",
  diff="easy", facets=["numbers"])
Q(L, "is a against has a", "Should Car extend Engine?",
  ["No: a car HAS an engine, so Engine should be a field of Car", "Yes: a car is an engine",
   "Yes: extends is the only way to reuse code", "No: Java cannot model cars"],
  ["Correct. Inheritance is an is a; a field is a has a.",
   "Wrong. A car is not an engine.",
   "Wrong. A field reuses the engine's code too.",
   "Wrong. Not the reason."],
  "If you cannot say \"a child IS A parent\" with a straight face, you want a field.",
  diff="medium", facets=["wording"])
Q(L, "inherited methods", "What does this print?",
  ["breathing\nswimming", "swimming", "breathing", "It does not compile"],
  ["Correct. Fish inherits breathe() from Animal and adds swim().",
   "Wrong. breathe() is inherited, so it runs too.",
   "Wrong. swim() is Fish's own method.",
   "Wrong. It compiles."],
  "The child gets the parent's public and protected members for free, and adds what is new.",
  classes='''
      class Animal {
          void breathe() {
              System.out.println("breathing");
          }
      }
      class Fish extends Animal {
          void swim() {
              System.out.println("swimming");
          }
      }
  ''', body='''
      Fish f = new Fish();
      f.breathe();
      f.swim();
  ''', check="out", diff="easy", facets=["names"])
Q(L, "what is inherited", "Which two are NOT inherited by a subclass?",
  ["Constructors", "Private members", "Public methods", "Protected fields"],
  ["Correct. A constructor belongs to its own class; it is called with super.",
   "Correct. Private members exist in the child object but the child's code cannot see them.",
   "Wrong. Public methods are inherited.",
   "Wrong. Protected fields are inherited."],
  "Inherited: public and protected. Not inherited: constructors and anything private.",
  style="multi", key=[0, 1], diff="medium", facets=["lists"])

# ============================================================ Lesson 3.4
L = "3.4"
Q(L, "overloading by accident", "The child's describe takes a parameter. What does this print?",
  ["account", "savings null", "savings", "It does not compile"],
  ["Correct. describe(String) has different parameters, so it OVERLOADS; nothing overrides describe(), and the parent's version runs.",
   "Wrong. The call passes no argument, so describe(String) is not used.",
   "Wrong. Nothing overrides the no-argument describe().",
   "Wrong. It compiles."],
  "Changing the parameters while meaning to override overloads instead. @Override would have caught it.",
  classes='''
      class Account {
          void describe() {
              System.out.println("account");
          }
      }
      class Savings extends Account {
          void describe(String s) {
              System.out.println("savings " + s);
          }
      }
  ''', body='''
      Account a = new Savings();
      a.describe();
  ''', check="out", diff="hard", facets=["names"])
Q(L, "@Override", "What happens when this is compiled?",
  [NOCOMPILE + ": shwo does not override anything, and @Override makes that an error", "It prints nothing",
   "It compiles, and shwo is a new method", "It throws an exception"],
  ["Correct. @Override asks the compiler to check, so the typo is caught.",
   "Wrong. It never compiles.",
   "Wrong. Without @Override that would happen silently; with it, it is an error.",
   "Wrong. It is a compile error."],
  "Always write @Override: a misspelt name becomes an error instead of a silent new method.",
  classes='''
      class A {
          void show() { }
      }
      class B extends A {
          @Override
          void shwo() { }
      }
  ''', body='''
      new B().show();
  ''', check="compile", diff="medium", facets=["names"])
Q(L, "three differences", "Which three facts distinguish overloading from overriding?",
  ["Same class against subclass; parameters differ against identical; compile time against run time",
   "Public against private; static against final; int against double",
   "Loop against recursion; array against String; input against output",
   "There is no difference"],
  ["Correct. Class, parameters, timing.",
   "Wrong. Not the differences the paper wants.",
   "Wrong. Unrelated.",
   "Wrong. They differ in three independent ways."],
  "Class, parameters, timing: three words, three marks.",
  diff="medium", facets=["lists"])
Q(L, "dynamic binding", "An Account variable holds a Savings object, and Savings overrides describe(). Whose describe() runs?",
  ["Savings's, decided at run time from the actual object", "Account's, decided at compile time from the declared type",
   "Both, one after the other", "Neither; it does not compile"],
  ["Correct. The actual object decides, at run time.",
   "Wrong. That is how overloading is decided, not overriding.",
   "Wrong. One version runs.",
   "Wrong. A parent-typed variable may hold a child."],
  "Polymorphism: one call, many forms, chosen at run time by the object.",
  diff="medium", facets=["wording"])
Q(L, "weaker access", "What happens when this is compiled?",
  [NOCOMPILE + ": an override may not be more restrictive than the method it replaces", "It prints nothing",
   "It compiles, and B.show is private", "It throws an exception"],
  ["Correct. A public method cannot be overridden as private.",
   "Wrong. It never compiles.",
   "Wrong. Narrowing the access is refused.",
   "Wrong. It is a compile error."],
  "The fourth difference: an overridden method may not be made less accessible.",
  classes='''
      class A {
          public void show() { }
      }
      class B extends A {
          private void show() { }
      }
  ''', body='''
      new A().show();
  ''', check="compile", diff="hard", facets=["names"])
TF(L, "timing", "True or false: overriding is decided at compile time from the declared type.",
   "false",
   "Wrong. That is overloading; overriding is decided at run time.",
   "Correct. Overriding is run time polymorphism, decided by the actual object.",
   "Overloading at compile time, overriding at run time.",
   diff="medium", facets=["wording"])
Q(L, "a polymorphic loop", "What does this print?",
  ["600.0", "300.0", "350.0", "600"],
  ["Correct. Each object's own pay() runs: 100 + 250 + 250 = 600.0.",
   "Wrong. The Manager objects run Manager's pay().",
   "Wrong. There are two Managers.",
   "Wrong. total is a double, so it prints 600.0."],
  "The loop never has to know the kinds: each object answers with its own version.",
  classes='''
      class Emp {
          double pay() {
              return 100;
          }
      }
      class Manager extends Emp {
          double pay() {
              return 250;
          }
      }
  ''', body='''
      Emp[] staff = {new Emp(), new Manager(), new Manager()};
      double total = 0;
      for (int i = 0; i < staff.length; i++) {
          total += staff[i].pay();
      }
      System.out.println(total);
  ''', check="out", diff="medium", facets=["numbers"])

# ============================================================ Lesson 3.5
L = "3.5"
Q(L, "a power by recursion", "What does this print?",
  ["32", "10", "16", "64"],
  ["Correct. pow(2, 5) is 2 x 2 x 2 x 2 x 2 x 1 = 32.",
   "Wrong. That multiplies 2 by 5.",
   "Wrong. That is 2 to the power 4.",
   "Wrong. That is 2 to the power 6."],
  "Base case e == 0 returns 1; each call multiplies by b and shrinks e.",
  methods='''
      static int pow(int b, int e) {
          if (e == 0) {
              return 1;
          }
          return b * pow(b, e - 1);
      }
  ''', body='''
      System.out.println(pow(2, 5));
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "printing on the way down", "What does this print?",
  ["3 2 1", "1 2 3", "3", "3 2 1 0"],
  ["Correct. Each call prints before it recurses, so the numbers come out on the way down.",
   "Wrong. That is the order when the print comes after the call.",
   "Wrong. down calls itself until n is below 1.",
   "Wrong. At 0 the base case returns without printing."],
  "Where the print sits relative to the recursive call decides the order.",
  methods='''
      static void down(int n) {
          if (n < 1) {
              return;
          }
          System.out.print(n + " ");
          down(n - 1);
      }
  ''', body='''
      down(3);
  ''', check="out", diff="medium", facets=["numbers", "lists"])
Q(L, "printing on the way up", "What does this print?",
  ["1 2 3", "3 2 1", "3", "0 1 2 3"],
  ["Correct. Each call recurses FIRST and prints afterwards, so the prints happen on the way back up.",
   "Wrong. That would need the print before the call.",
   "Wrong. Every level prints once.",
   "Wrong. At 0 nothing is printed."],
  "Nothing is done on the way down that comes after the call; it all happens on the way back up.",
  methods='''
      static void up(int n) {
          if (n < 1) {
              return;
          }
          up(n - 1);
          System.out.print(n + " ");
      }
  ''', body='''
      up(3);
  ''', check="out", diff="hard", facets=["numbers", "lists"])
Q(L, "no base case", "What happens when this runs?",
  ["It fails with StackOverflowError", "It prints 0", "It loops quietly for ever", "It does not compile"],
  ["Correct. With no base case every call makes another, until the call stack is full.",
   "Wrong. Nothing ever returns.",
   "Wrong. Each call uses a stack frame, so it runs out of memory quickly.",
   "Wrong. It compiles."],
  "A recursion with no base case is the recursive infinite loop: StackOverflowError.",
  methods='''
      static int bad(int n) {
          return bad(n - 1);
      }
  ''', body='''
      System.out.println(bad(3));
  ''', check="err:StackOverflowError", diff="medium", facets=["names"])
Q(L, "digit sum by recursion", "What does this print?",
  ["18", "9045", "4", "27"],
  ["Correct. 5 + 4 + 0 + 9 = 18: each call peels the last digit off with % 10.",
   "Wrong. The method adds the digits.",
   "Wrong. That counts the digits.",
   "Wrong. Add each digit once."],
  "The base case is a single digit; the recursive case adds the last digit to the sum of the rest.",
  methods='''
      static int ds(int n) {
          if (n < 10) {
              return n;
          }
          return n % 10 + ds(n / 10);
      }
  ''', body='''
      System.out.println(ds(9045));
  ''', check="out", diff="medium", facets=["numbers"])
Q(L, "reversing a String", "What does this print?",
  ["EDOC", "CODE", "ODEC", "DEOC"],
  ["Correct. Each call puts the first character on the END of the reversed rest.",
   "Wrong. The method reverses the text.",
   "Wrong. Trace it: reverse(\"ODE\") + 'C', and so on down.",
   "Wrong. Trace one level at a time."],
  "reverse(s.substring(1)) + s.charAt(0): first character last.",
  methods='''
      static String reverse(String s) {
          if (s.length() <= 1) {
              return s;
          }
          return reverse(s.substring(1)) + s.charAt(0);
      }
  ''', body='''
      System.out.println(reverse("CODE"));
  ''', check="out", diff="medium", facets=["names"])
Q(L, "the two parts", "What is the BASE CASE of a recursive method?",
  ["The condition under which it returns without calling itself", "The first call made from main",
   "The call that passes a smaller input", "The largest value it can handle"],
  ["Correct. Every recursive method needs one, or it never stops.",
   "Wrong. That is just the first call.",
   "Wrong. That is the recursive case.",
   "Wrong. Not a definition in the course."],
  "Base case stops it, recursive case shrinks it.",
  diff="easy", facets=["wording"])
Q(L, "recursion against iteration", "Which uses more memory, and why?",
  ["Recursion, because every call in progress holds a stack frame until the base case returns",
   "Iteration, because a loop keeps every value", "They use exactly the same", "Recursion uses no memory at all"],
  ["Correct. A loop uses one set of variables however many times it goes round.",
   "Wrong. A loop reuses the same variables.",
   "Wrong. Each recursive call adds a frame.",
   "Wrong. Each call occupies memory."],
  "Recursion is clearer for self-similar problems and heavier in memory; iteration is the default.",
  diff="medium", facets=["wording"])

# ============================================================ Lesson 3.6
L = "3.6"
Q(L, "which catch runs", "What does this print?",
  ["index\ndone", "stored\ndone", "math\ndone", "index"],
  ["Correct. a[2] is past the end, so the ArrayIndexOutOfBounds catch runs, then finally.",
   "Wrong. The failing line stops the try before stored is printed.",
   "Wrong. Nothing divides by zero.",
   "Wrong. finally always runs."],
  "The matching catch runs; finally runs every time.",
  body='''
      try {
          int[] a = new int[2];
          a[2] = 5;
          System.out.println("stored");
      } catch (ArithmeticException e) {
          System.out.println("math");
      } catch (ArrayIndexOutOfBoundsException e) {
          System.out.println("index");
      } finally {
          System.out.println("done");
      }
  ''', check="out", diff="medium", facets=["names"])
Q(L, "getMessage", "What does this print?",
  ["For input string: \"12a\"", "12a", "NumberFormatException", "12"],
  ["Correct. e.getMessage() gives the detail the exception carries.",
   "Wrong. The message says more than the text.",
   "Wrong. getMessage gives the detail, not the class name.",
   "Wrong. parseInt refuses the whole text."],
  "The variable e holds the exception object, and e.getMessage() gives the detail.",
  body='''
      try {
          int n = Integer.parseInt("12a");
      } catch (NumberFormatException e) {
          System.out.println(e.getMessage());
      }
  ''', check="out", diff="hard", facets=["names"])
Q(L, "catching the wrong exception", "What happens when this runs?",
  ["A NullPointerException stops the program; the ArithmeticException catch does not match it",
   "It prints math", "It prints 0", "It does not compile"],
  ["Correct. A catch only catches its own type.",
   "Wrong. Nothing divides by zero.",
   "Wrong. s is null, so length() fails.",
   "Wrong. It compiles."],
  "Name the exception you expect; others pass straight through.",
  body='''
      try {
          String s = null;
          System.out.println(s.length());
      } catch (ArithmeticException e) {
          System.out.println("math");
      }
  ''', check="err:NullPointerException", diff="medium", facets=["names"])
Q(L, "a checked exception never thrown", "What happens when this is compiled?",
  [NOCOMPILE + ": the try block cannot throw IOException", "It prints 1", "It prints nothing", "It prints io"],
  ["Correct. Java refuses a catch for a checked exception the try block can never throw.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles.",
   "Wrong. It never compiles."],
  "Catching a checked exception you never cause is a compile error.",
  body='''
      try {
          int x = 1;
          System.out.println(x);
      } catch (IOException e) {
          System.out.println("io");
      }
  ''', check="compile", diff="hard", facets=["names"])
Q(L, "checked exceptions", "main does NOT declare throws. What happens when this is compiled?",
  [NOCOMPILE + ": FileNotFoundException is checked and must be caught or declared", "It prints opened",
   "It throws FileNotFoundException when it runs", "It prints nothing"],
  ["Correct. The compiler insists on checked exceptions: catch it or write throws.",
   "Wrong. It never compiles.",
   "Wrong. It is stopped before it can run.",
   "Wrong. It never compiles."],
  "Checked: the compiler makes you deal with it. File work is the everyday example.",
  body='''
      FileReader r = new FileReader("missing.txt");
      System.out.println("opened");
  ''', check="compile", diff="medium", facets=["names"])
Q(L, "checked or unchecked", "Which of these is a CHECKED exception?",
  ["IOException", "NullPointerException", "ArithmeticException", "NumberFormatException"],
  ["Correct. It comes from outside the program, so the compiler makes you handle it.",
   "Wrong. Unchecked: a fault in the program's own logic.",
   "Wrong. Unchecked: dividing by zero is your fault.",
   "Wrong. Unchecked: bad text given to parseInt."],
  "Checked extends Exception but not RuntimeException; unchecked extends RuntimeException.",
  diff="medium", facets=["names"])
Q(L, "throw and throws", "Which goes in a method HEADER to say the method may raise an exception it does not handle?",
  ["throws", "throw", "catch", "finally"],
  ["Correct. throws, with the s, declares it.",
   "Wrong. throw raises one now, inside the body.",
   "Wrong. catch handles one.",
   "Wrong. finally is the cleanup block."],
  "throw raises one, throws warns about one.",
  diff="easy", facets=["names"])
Q(L, "throwing and catching", "What does this print?",
  ["20\nError: Day must be 1, 2 or 3", "20\n40", "Error: Day must be 1, 2 or 3", "20"],
  ["Correct. check(2) returns 20; check(4) throws, and the catch prints its message.",
   "Wrong. 4 is rejected before any multiplication.",
   "Wrong. The first call succeeds and prints 20.",
   "Wrong. The second call's exception is caught and printed."],
  "throw new IllegalArgumentException(...) in the method; catch it where it is called.",
  methods='''
      static int check(int day) {
          if (day < 1 || day > 3) {
              throw new IllegalArgumentException("Day must be 1, 2 or 3");
          }
          return day * 10;
      }
  ''', body='''
      try {
          System.out.println(check(2));
          System.out.println(check(4));
      } catch (IllegalArgumentException e) {
          System.out.println("Error: " + e.getMessage());
      }
  ''', check="out", diff="hard", facets=["names"])

# ============================================================ Lesson 3.7
L = "3.7"
Q(L, "PrintWriter wipes", "main declares throws IOException. What does this print?",
  ["second", "first\nsecond", "first", "Nothing"],
  ["Correct. new PrintWriter on a filename starts an empty file every time, so the first line is gone.",
   "Wrong. That needs the append form with FileWriter and true.",
   "Wrong. The second writer replaced it.",
   "Wrong. The second line was written and the writer closed."],
  "PrintWriter on a name wipes it.",
  body='''
      PrintWriter out = new PrintWriter("log.txt");
      out.println("first");
      out.close();
      PrintWriter again = new PrintWriter("log.txt");
      again.println("second");
      again.close();
      Scanner in = new Scanner(new File("log.txt"));
      while (in.hasNextLine()) {
          System.out.println(in.nextLine());
      }
      in.close();
  ''', throws=True, check="out", diff="medium", facets=["names"])
Q(L, "appending", "main declares throws IOException. What does this print?",
  ["first\nsecond", "second", "first", "second\nfirst"],
  ["Correct. FileWriter with true opens for append, so the new line goes after the old one.",
   "Wrong. The true keeps what was there.",
   "Wrong. The appended line is there too.",
   "Wrong. Appended lines go at the end."],
  "new PrintWriter(new FileWriter(name, true)): the true is the whole difference.",
  body='''
      PrintWriter out = new PrintWriter("log.txt");
      out.println("first");
      out.close();
      PrintWriter more = new PrintWriter(new FileWriter("log.txt", true));
      more.println("second");
      more.close();
      Scanner in = new Scanner(new File("log.txt"));
      while (in.hasNextLine()) {
          System.out.println(in.nextLine());
      }
      in.close();
  ''', throws=True, check="out", diff="easy", facets=["names"])
Q(L, "forgetting close", "The writer is never closed. main declares throws IOException. What does this print?",
  ["false", "true", "hello", "It does not compile"],
  ["Correct. The text is still in the writer's buffer, so the file on disk is empty and has no line.",
   "Wrong. Nothing reached the file without close().",
   "Wrong. The program prints whether a line exists, and none does.",
   "Wrong. It compiles."],
  "Close it, or nothing was written.",
  body='''
      PrintWriter out = new PrintWriter("f.txt");
      out.println("hello");
      Scanner in = new Scanner(new File("f.txt"));
      System.out.println(in.hasNextLine());
  ''', throws=True, check="out", diff="hard", facets=["names"])
Q(L, "reading every line", "main declares throws IOException. What does this print?",
  ["3", "2", "4", "0"],
  ["Correct. hasNextLine keeps the loop going for each of the three lines written.",
   "Wrong. All three lines are read.",
   "Wrong. Only three lines were written.",
   "Wrong. The writer was closed, so the lines reached the file."],
  "while (in.hasNextLine()) reads a file of any length.",
  body='''
      PrintWriter out = new PrintWriter("r.txt");
      out.println("a");
      out.println("b");
      out.println("c");
      out.close();
      Scanner in = new Scanner(new File("r.txt"));
      int n = 0;
      while (in.hasNextLine()) {
          in.nextLine();
          n++;
      }
      in.close();
      System.out.println(n);
  ''', throws=True, check="out", diff="easy", facets=["numbers", "names"])
Q(L, "the first records", "main declares throws IOException. What does this print?",
  ["Rec 1\nRec 2", "Rec 1\nRec 2\nRec 3", "Rec 1", "Rec 3"],
  ["Correct. The count reaches 3 on the third line, and break leaves before printing it.",
   "Wrong. The break comes before the third print.",
   "Wrong. Two lines print before the break.",
   "Wrong. The first lines print; the third is where it stops."],
  "Display only the first few: count as you read and break.",
  body='''
      PrintWriter out = new PrintWriter("r.txt");
      for (int i = 1; i <= 5; i++) {
          out.println("Rec " + i);
      }
      out.close();
      Scanner in = new Scanner(new File("r.txt"));
      int n = 0;
      while (in.hasNextLine()) {
          String line = in.nextLine();
          n++;
          if (n > 2) break;
          System.out.println(line);
      }
      in.close();
  ''', throws=True, check="out", diff="medium", facets=["numbers"])
Q(L, "append or overwrite", "Which line opens records.txt to ADD records without destroying the existing ones?",
  ["new PrintWriter(new FileWriter(\"records.txt\", true))", "new PrintWriter(\"records.txt\")",
   "new Scanner(new File(\"records.txt\"))", "new FileWriter(\"records.txt\", false)"],
  ["Correct. FileWriter with true appends.",
   "Wrong. That wipes the file.",
   "Wrong. A Scanner reads; it does not write.",
   "Wrong. false means overwrite."],
  "The file question always asks you to add to the file you made earlier. That one true is the mark.",
  diff="easy", facets=["names"])
Q(L, "throws IOException", "Why do the file listings write throws IOException on main?",
  ["File operations raise checked exceptions, which must be caught or declared",
   "To make the program run faster", "Because every Java program needs it", "To close the file automatically"],
  ["Correct. Declaring them is the short, legal way to satisfy the compiler.",
   "Wrong. It has nothing to do with speed.",
   "Wrong. Only methods that can raise checked exceptions need it.",
   "Wrong. You must still close the file."],
  "Catch them, or declare throws IOException.",
  diff="easy", facets=["wording"])
Q(L, "imports", "Which import is needed for new File(\"records.txt\"), separately from Scanner?",
  ["import java.io.File;", "import java.util.File;", "import javax.swing.File;", "No import is needed"],
  ["Correct. File lives in java.io, Scanner in java.util.",
   "Wrong. java.util is Scanner's package, not File's.",
   "Wrong. javax.swing is for JOptionPane.",
   "Wrong. File must be imported."],
  "java.io.PrintWriter, java.io.FileWriter, java.io.File, java.io.IOException, java.util.Scanner.",
  diff="medium", facets=["names"])


# ============================================================ build
def run(src, stdin=None, timeout=25):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "Main.java"
        p.write_text(src, encoding="utf-8")
        try:
            r = subprocess.run(["java", "-Xss512k", str(p)], cwd=d, input=stdin, capture_output=True,
                               text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None, "timeout"
    err = None
    if r.returncode != 0:
        if "compilation failed" in r.stderr or ": error:" in r.stderr:
            err = "compile"
        else:
            m = re.search(r'Exception in thread "main" ([\w.$]+)', r.stderr)
            err = m.group(1).split(".")[-1] if m else "unknown:" + r.stderr[:80]
    out = "\n".join(l.rstrip() for l in r.stdout.rstrip("\n").splitlines())
    return out, err


def build():
    problems = []
    out = []
    ran = 0
    for q in QUESTIONS:
        where = f"{q['id']} ({q['prompt'][:40]})"
        chk = q.get("check")
        if q.get("body") and chk:
            src = program(q["body"], q.get("methods", ""), q.get("classes", ""), q.get("throws", False))
            got, err = run(src, q.get("stdin"))
            ran += 1
            if chk == "compile":
                if err != "compile":
                    problems.append(f"{where}: expected a compile error, but it {'ran: ' + repr(got) if err is None else err}")
            elif chk.startswith("err:"):
                if err != chk[4:]:
                    problems.append(f"{where}: expected {chk[4:]}, got {err} (stdout {got!r})")
                if q.get("before") is not None and got != q["before"]:
                    problems.append(f"{where}: printed {got!r} before stopping")
            elif chk == "out":
                if err:
                    problems.append(f"{where}: expected output, got {err}")
                elif q["opts"][0] != got:
                    problems.append(f"{where}: key {q['opts'][0]!r} but Java printed {got!r}")
                for o in q["opts"][1:]:
                    if o == got:
                        problems.append(f"{where}: wrong option {o!r} is ALSO the real output")
            elif chk == "equiv":
                if err:
                    problems.append(f"{where}: the reference program failed: {err}")
                for k, alt in enumerate(q["equiv"]):
                    if alt is None:
                        continue
                    g2, e2 = run(program(alt), timeout=8)
                    ran += 1
                    same = (e2 is None and g2 == got)
                    if k == 0 and not same:
                        problems.append(f"{where}: the correct rewriting printed {g2!r} ({e2}), not {got!r}")
                    if k > 0 and same:
                        problems.append(f"{where}: wrong rewriting {k} ALSO prints {got!r}")
        base = dict(id=q["id"], module=TOPIC[q["lesson"]], slides=[f"Lesson {q['lesson']}"],
                    style=q["style"], difficulty=q["diff"],
                    facets=q["facets"] or (["numbers"] if q.get("body") else ["wording"]),
                    topic=q["topic"], prompt=q["prompt"])
        if q.get("body"):
            base["code"] = shown(q["body"], q.get("methods", ""), q.get("classes", ""))
        if q["style"] == "tf":
            base.update(answer=q["answer"], explanation=q["exp"], why=q["why"])
        else:
            n = len(q["opts"])
            if len(q["why"]) != n:
                problems.append(f"{where}: {n} options but {len(q['why'])} verdicts")
                continue
            order = list(range(n))
            random.Random(q["id"]).shuffle(order)
            ids = "abcdef"
            opts = [dict(id=ids[i], text=q["opts"][j]) for i, j in enumerate(order)]
            why = {ids[i]: q["why"][j] for i, j in enumerate(order)}
            correct = [ids[i] for i, j in enumerate(order) if j < q["nkey"]]
            base.update(options=opts, answer=correct if q["style"] == "multi" else correct[0],
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
    print(f"  wrote {len(out)} questions to {OUT.relative_to(HERE.parent.parent)}; {ran} Java programs compiled and run")
    print("  " + ", ".join(f"{k}: {v}" for k, v in sorted(by.items())))


if __name__ == "__main__":
    build()
