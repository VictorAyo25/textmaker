"""The objective half of the COS221 paper, as questions.

WHY THIS FILE EXISTS. The student confirmed on 2026-08-09 that every paper this
semester except the physics one is a SINGLE paper carrying an objective section
AND a theory section. This manual shipped at 347 pages of theory practice and
carried no objective practice at all.

WHERE THE QUESTIONS COME FROM. This course has no computer-based test among its
sources, so there is nothing to transcribe. These are AUTHORED, and the section
says so plainly rather than implying they are the examiner's. They are grounded in
what this manual teaches, unit by unit, and in what the two past papers actually
ask about, and they copy the paper's habits deliberately: it asks for the output
of a fragment, it asks you to find the error, it asks for a definition with an
example, and it asks about the difference between two things that look alike.

HOW THE CODE CLAIMS ARE KEPT HONEST. Every question carrying a `code` block also
carries `runs: True`, and gen_objective.py COMPILES and RUNS that code on a real
JVM (Temurin 17, the same one check_code.py uses) and refuses to write the section
unless the option marked correct is exactly what came back. Where the answer is a
compiler error rather than output, `expect_error` names the phrase the compiler
must produce, and that is checked too. No output in this bank was typed from
memory.

Each entry:
  id, module, topic, prompt
  code          a complete program, shown to the reader as it is run
  cls           its class name, so javac can be pointed at the right file
  options       4 strings, in the order they are printed
  answer        index into options
  why           4 strings, one per option, same order
  runs          True when the answer is this program's real output
  expect_error  set instead of runs when the answer is that it does not compile
  explanation   the line that goes under the answer
"""

Q = []


def q(**kw):
    kw.setdefault('runs', False)
    kw.setdefault('expect_error', None)
    Q.append(kw)


# ===========================================================================
# FOUNDATIONS, MODULE ONE and MODULE TWO: what Java is, and getting it running
# ===========================================================================
q(id='j1-01', module=1, topic='compiled and interpreted',
  prompt='What does javac produce, and what runs it?',
  options=['Machine code for your processor, run directly by the operating system',
           'Bytecode in a .class file, run by the Java Virtual Machine',
           'A .java file, run by javac itself',
           'An executable .exe file, run by double clicking it'],
  answer=1,
  why=['Wrong. Compiling straight to machine code is the C model, and it is exactly '
       'what Java avoids, because machine code runs on one kind of processor only.',
       'Correct. javac turns your .java source into bytecode in a .class file, and '
       'the java command starts a JVM that executes that bytecode. The JVM is what '
       'makes the same .class file run on any machine that has one.',
       'Wrong. The .java file is what you WRITE and what javac consumes. It is the '
       'input, not the output.',
       'Wrong. Java deliberately does not produce a platform executable. That is the '
       'whole point of write once, run anywhere.'],
  explanation='Source to bytecode by javac, bytecode to behaviour by the JVM. Java '
              'is compiled AND interpreted, and saying only one of those loses half '
              'the mark.')

q(id='j1-02', module=1, topic='the main method',
  prompt='Which signature does the JVM look for to start a program?',
  options=['public static void main(String[] args)',
           'public void main(String[] args)',
           'static void Main(String[] args)',
           'public static int main(String args)'],
  answer=0,
  why=['Correct. public so the JVM can reach it, static so it runs with no object, '
       'void because it returns nothing, and a String array for the command line '
       'arguments.',
       'Wrong. Without static the JVM would need an object to call it on, and no '
       'object exists yet when the program starts.',
       'Wrong on two counts: Java is case sensitive so Main is a different name, and '
       'without public the JVM cannot reach it.',
       'Wrong on two counts: main returns void, and the parameter is an ARRAY of '
       'String, not a single String.'],
  explanation='public static void main(String[] args). Write it out by hand until '
              'it is automatic; a paper answer that gets it wrong has failed before '
              'the first statement.')

q(id='j1-03', module=1, topic='class and object',
  prompt='Which statement best distinguishes a class from an object?',
  options=['A class is a running instance and an object is its definition',
           'A class is a blueprint; an object is an instance of it, with its own '
           'values',
           'A class and an object are two words for the same thing',
           'A class can have only one object at a time'],
  answer=1,
  why=['Wrong, and it is exactly backwards. The definition is the class; the running '
       'instance is the object.',
       'Correct. The class says what every instance will have and be able to do; each '
       'object made with new has its own copy of the fields.',
       'Wrong. If they were the same, new would have nothing to do.',
       'Wrong. A class exists so that many objects can be created from it.'],
  explanation='Class is the blueprint, object is the building. new is what turns one '
              'into the other.')

q(id='j1-04', module=2, topic='the JDK, JRE and JVM',
  prompt='Which statement is TRUE?',
  options=['The JDK contains the JRE, which contains the JVM',
           'The JVM contains the JRE, which contains the JDK',
           'The JDK and the JRE are two names for the same thing',
           'The JRE is needed to compile, the JDK only to run'],
  answer=0,
  why=['Correct. The JDK is the developer kit and holds the compiler; inside it is '
       'the runtime environment, and inside that is the virtual machine that '
       'actually executes bytecode.',
       'Wrong, and it inverts the nesting. The smallest of the three is the JVM.',
       'Wrong. The JRE can only RUN programs. Only the JDK carries javac.',
       'Wrong, and it swaps them: you compile with the JDK and can run with the JRE '
       'alone.'],
  explanation='JDK contains JRE contains JVM. Compile needs the JDK, run needs only '
              'the JRE.')

q(id='j1-05', module=1, topic='programming paradigms',
  prompt='Java is described as an object-oriented language. Which TWO features below '
         'are the reason? Choose the single option naming BOTH correctly.',
  options=['Pointers and manual memory management',
           'Encapsulation and inheritance',
           'Preprocessor directives and macros',
           'Goto statements and labels'],
  answer=1,
  why=['Wrong. Java deliberately has neither: references replace pointers and the '
       'garbage collector replaces manual freeing.',
       'Correct. Bundling data with the methods that act on it, and letting one class '
       'extend another, are two of the four pillars, alongside abstraction and '
       'polymorphism.',
       'Wrong. Those are C and C++ features. Java has no preprocessor at all.',
       'Wrong. goto is a reserved word in Java that is not usable, kept reserved '
       'precisely so nobody writes one.'],
  explanation='Encapsulation, inheritance, polymorphism, abstraction. Those four are '
              'the answer to any what-makes-it-object-oriented question.')


# ===========================================================================
# MODULE THREE: types, operators, input and output
# ===========================================================================
q(id='j3-01', module=3, topic='integer division', runs=True, cls='Q301',
  prompt='What does this print?',
  code='public class Q301 {\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println(7 / 2);\n'
       '        System.out.println(7 % 2);\n'
       '        System.out.println(7.0 / 2);\n'
       '    }\n'
       '}',
  options=['3\n1\n3.5', '3.5\n1\n3.5', '3\n1\n3', '3.5\n3.5\n3.5'],
  answer=0,
  why=['Correct. Two ints divide as ints, so the fraction is thrown away and 7 / 2 '
       'is 3. The remainder is 1. Making either operand a double promotes the whole '
       'expression, so 7.0 / 2 is 3.5.',
       'Wrong on the first line. Integer division truncates in Java; it does not '
       'produce a decimal. That is the single most common Java arithmetic error.',
       'Wrong on the last line. 7.0 is a double, so the division is done in doubles.',
       'Wrong throughout. % is the remainder operator, not a division.'],
  explanation='int divided by int gives int, and the fraction is discarded, not '
              'rounded. One double operand promotes the whole expression.')

q(id='j3-02', module=3, topic='the sign of the remainder', runs=True, cls='Q302',
  prompt='What does this print?',
  code='public class Q302 {\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println(-7 / 2);\n'
       '        System.out.println(-7 % 2);\n'
       '    }\n'
       '}',
  options=['-4\n1', '-3\n-1', '-4\n-1', '-3\n1'],
  answer=1,
  why=['Wrong. Java truncates towards ZERO, so -7 / 2 is -3, not -4. Flooring to -4 '
       'is what Python does, and the difference is a real exam trap.',
       'Correct. Division truncates towards zero giving -3, and the remainder takes '
       'the sign of the LEFT operand, giving -1.',
       'Wrong on the division for the same reason: Java truncates towards zero.',
       'Wrong on the remainder. In Java the result of % has the sign of the dividend, '
       'so a negative dividend gives a negative remainder.'],
  explanation='Java truncates towards zero and % takes the sign of the left operand. '
              'Both differ from some other languages, so this is worth knowing '
              'exactly rather than by feel.')

q(id='j3-03', module=3, topic='char arithmetic', runs=True, cls='Q303',
  prompt='What does this print?',
  code='public class Q303 {\n'
       '    public static void main(String[] args) {\n'
       '        char c = \'A\';\n'
       '        System.out.println(c + 1);\n'
       '        System.out.println((char) (c + 1));\n'
       '    }\n'
       '}',
  options=['B\nB', '66\nB', 'A1\nB', '66\n66'],
  answer=1,
  why=['Wrong on the first line. A char in arithmetic is promoted to int, so the '
       'result is a number, not a letter.',
       'Correct. c + 1 promotes the char to its code, 65, and adds 1 to give 66. The '
       'cast on the second line turns 66 back into a char, which prints as B.',
       'Wrong. Plus between a char and an int is ARITHMETIC, not joining. Joining '
       'would need one side to be a String.',
       'Wrong on the second line: the cast to char is what makes it print as a '
       'letter.'],
  explanation='A char is a number with a costume on. Arithmetic strips the costume; '
              'a cast back to char puts it on again.')

q(id='j3-04', module=3, topic='string joining against addition', runs=True, cls='Q304',
  prompt='What does this print?',
  code='public class Q304 {\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println("Total: " + 1 + 2);\n'
       '        System.out.println("Total: " + (1 + 2));\n'
       '    }\n'
       '}',
  options=['Total: 12\nTotal: 3', 'Total: 3\nTotal: 3', 'Total: 12\nTotal: 12',
           'Total: 3\nTotal: 12'],
  answer=0,
  why=['Correct. Plus groups left to right. The first plus has a String on its left, '
       'so it JOINS, producing "Total: 1", and the next plus joins the 2 onto that. '
       'The brackets on the second line force the addition first.',
       'Wrong on the first line. Nothing adds 1 and 2 there: by the time the 2 is '
       'reached the left side is already a String.',
       'Wrong on the second line. The brackets change the answer, which is the whole '
       'point of the question.',
       'Wrong, and it has the two lines swapped.'],
  explanation='Plus is left-associative, and once a String is involved every later '
              'plus joins. Bracket the arithmetic and this whole class of bug goes '
              'away.')

q(id='j3-05', module=3, topic='integer overflow', runs=True, cls='Q305',
  prompt='What does this print?',
  code='public class Q305 {\n'
       '    public static void main(String[] args) {\n'
       '        int big = Integer.MAX_VALUE;\n'
       '        System.out.println(big);\n'
       '        System.out.println(big + 1);\n'
       '    }\n'
       '}',
  options=['2147483647\n2147483648', '2147483647\n-2147483648',
           '2147483647\nerror at run time', '2147483648\n-2147483648'],
  answer=1,
  why=['Wrong. An int cannot hold 2147483648. The type does not grow to fit.',
       'Correct. int is 32 bits, so its maximum is 2147483647, and adding 1 wraps '
       'round to the most negative value. Java does not report this: it just gives '
       'the wrong number quietly.',
       'Wrong. There is no exception for integer overflow in Java. That silence is '
       'exactly what makes it dangerous.',
       'Wrong on the first line. MAX_VALUE is 2147483647, one less than 2 to the '
       'power 31.'],
  explanation='int holds -2147483648 to 2147483647, and overflow wraps silently. '
              'Use long when a value might exceed it.')

q(id='j3-06', module=3, topic='floating point comparison', runs=True, cls='Q306',
  prompt='What does this print?',
  code='public class Q306 {\n'
       '    public static void main(String[] args) {\n'
       '        double a = 0.1 + 0.2;\n'
       '        System.out.println(a);\n'
       '        System.out.println(a == 0.3);\n'
       '    }\n'
       '}',
  options=['0.3\ntrue', '0.30000000000000004\nfalse', '0.3\nfalse',
           '0.30000000000000004\ntrue'],
  answer=1,
  why=['Wrong on both lines. Binary floating point cannot hold 0.1 or 0.2 exactly, so '
       'their sum is not exactly 0.3.',
       'Correct. The stored sum is very slightly above 0.3 and prints in full, so the '
       'equality test is false.',
       'Wrong on the first line: println shows the true stored value, tiny error and '
       'all.',
       'Wrong on the second line: if the value printed is not 0.3, it cannot equal '
       '0.3.'],
  explanation='Never compare two doubles with ==. Compare the size of their '
              'difference against a small tolerance instead.')

q(id='j3-07', module=3, topic='pre-increment and post-increment', runs=True, cls='Q307',
  prompt='What does this print?',
  code='public class Q307 {\n'
       '    public static void main(String[] args) {\n'
       '        int i = 5;\n'
       '        System.out.println(i++);\n'
       '        System.out.println(i);\n'
       '        System.out.println(++i);\n'
       '    }\n'
       '}',
  options=['5\n6\n7', '6\n6\n7', '5\n5\n6', '6\n7\n7'],
  answer=0,
  why=['Correct. i++ yields the OLD value 5 and then makes i 6. The second line shows '
       'that 6. ++i increments first, to 7, and yields 7.',
       'Wrong on the first line. The post-increment gives back the value BEFORE the '
       'increment.',
       'Wrong on the second line. The increment did happen, so i is 6 by then.',
       'Wrong on the first line, for the same reason as the second option.'],
  explanation='Post says use it then change it; pre says change it then use it. The '
              'variable ends up the same either way, and what the EXPRESSION gives '
              'back is what differs.')

q(id='j3-08', module=3, topic='operator precedence', runs=True, cls='Q308',
  prompt='What does this print?',
  code='public class Q308 {\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println(2 + 3 * 4);\n'
       '        System.out.println((2 + 3) * 4);\n'
       '        System.out.println(10 - 2 - 3);\n'
       '    }\n'
       '}',
  options=['14\n20\n5', '20\n20\n5', '14\n20\n11', '14\n14\n5'],
  answer=0,
  why=['Correct. Multiply before add gives 14, brackets force 20, and subtraction '
       'groups left to right so 10 - 2 is 8 and 8 - 3 is 5.',
       'Wrong on the first line. Multiplication binds tighter than addition without '
       'any brackets.',
       'Wrong on the last line. Left to right gives 5; grouping the right pair first '
       'would give 11, and no operator in Java does that.',
       'Wrong on the second line: the brackets really do change it.'],
  explanation='Multiply and divide before add and subtract, then left to right. When '
              'in doubt, write the brackets yourself.')

q(id='j3-09', module=3, topic='short-circuit evaluation', runs=True, cls='Q309',
  prompt='What does this print?',
  code='public class Q309 {\n'
       '    static boolean shout(String s) {\n'
       '        System.out.println(s);\n'
       '        return true;\n'
       '    }\n'
       '    public static void main(String[] args) {\n'
       '        if (false && shout("left")) { }\n'
       '        if (true || shout("right")) { }\n'
       '        System.out.println("done");\n'
       '    }\n'
       '}',
  options=['left\nright\ndone', 'done', 'left\ndone', 'right\ndone'],
  answer=1,
  why=['Wrong. Neither call happens, which is the whole point of short circuiting.',
       'Correct. && stops as soon as its left side is false, and || stops as soon as '
       'its left side is true, so neither shout is ever called.',
       'Wrong. false && anything is already decided, so the right side is skipped.',
       'Wrong. true || anything is already decided, so the right side is skipped.'],
  explanation='&& and || evaluate the right side only when they must. That is what '
              'makes if (s != null && s.length() > 0) safe.')

q(id='j3-10', module=3, topic='Scanner input',
  prompt='A program reads an integer with a Scanner named in. Which line is correct?',
  options=['int n = in.nextInt();', 'int n = in.next();',
           'int n = in.nextLine();', 'int n = Scanner.nextInt();'],
  answer=0,
  why=['Correct. nextInt() reads the next token and returns it as an int, which is '
       'what the variable needs.',
       'Wrong. next() returns a String, and a String cannot be assigned to an int '
       'without conversion.',
       'Wrong for the same reason: nextLine() also returns a String. It would need '
       'Integer.parseInt around it.',
       'Wrong. nextInt is an instance method, called on your Scanner object, not on '
       'the class.'],
  explanation='nextInt for an int, nextDouble for a double, nextLine for a whole line '
              'of text. Mixing nextInt with nextLine leaves the newline behind, which '
              'is the classic Scanner bug.')

q(id='j3-11', module=3, topic='printf rounding', runs=True, cls='Q311',
  prompt='What does this print?',
  code='public class Q311 {\n'
       '    public static void main(String[] args) {\n'
       '        System.out.printf("%.2f%n", 3.14159);\n'
       '        System.out.printf("%5d|%n", 42);\n'
       '    }\n'
       '}',
  options=['3.14\n   42|', '3.142\n42   |', '3.14\n42   |', '3.1\n   42|'],
  answer=0,
  why=['Correct. %.2f gives two decimal places, and %5d pads the number to five '
       'characters on the LEFT, so the spaces come first.',
       'Wrong on both counts: .2f is two decimals, and %5d right-aligns.',
       'Wrong on the padding. A width without a minus sign right-aligns; %-5d would '
       'pad on the right.',
       'Wrong on the decimals: two were asked for, not one.'],
  explanation='%.2f fixes the decimals, %5d fixes the width and right-aligns, %-5d '
              'left-aligns, and %n is the newline that works everywhere.')

q(id='j3-12', module=3, topic='casting',
  prompt='Which assignment compiles WITHOUT a cast?',
  options=['int n = 3.5;', 'double d = 7;', 'int n = 7L;', 'char c = "A";'],
  answer=1,
  why=['Wrong. A double into an int loses information, so Java requires you to say '
       'so with an explicit cast.',
       'Correct. int to double is a WIDENING conversion: nothing can be lost, so Java '
       'does it silently.',
       'Wrong. long to int is narrowing, so it needs a cast.',
       'Wrong. Double quotes make a String, and a String is not a char. A char '
       'literal uses single quotes.'],
  explanation='Widening is automatic, narrowing needs a cast. Remember the direction: '
              'small into big is safe, big into small is your responsibility.')


# ===========================================================================
# MODULE FOUR: control structures
# ===========================================================================
q(id='j4-01', module=4, topic='switch fall-through', runs=True, cls='Q401',
  prompt='What does this print?',
  code='public class Q401 {\n'
       '    public static void main(String[] args) {\n'
       '        int day = 2;\n'
       '        switch (day) {\n'
       '            case 1: System.out.println("Mon");\n'
       '            case 2: System.out.println("Tue");\n'
       '            case 3: System.out.println("Wed");\n'
       '                    break;\n'
       '            default: System.out.println("Other");\n'
       '        }\n'
       '    }\n'
       '}',
  options=['Tue', 'Tue\nWed', 'Tue\nWed\nOther', 'Mon\nTue\nWed'],
  answer=1,
  why=['Wrong. Without a break at the end of case 2, execution falls straight into '
       'case 3.',
       'Correct. It enters at case 2, prints Tue, falls through into case 3 and '
       'prints Wed, and the break there stops it.',
       'Wrong. The break at the end of case 3 stops it before default.',
       'Wrong. It ENTERS at the matching case; the cases above it are skipped '
       'entirely.'],
  explanation='A switch enters at the matching label and runs on until a break. '
              'Missing breaks are the classic switch bug and a favourite exam '
              'question.')

q(id='j4-02', module=4, topic='the dangling else', runs=True, cls='Q402',
  prompt='What does this print?',
  code='public class Q402 {\n'
       '    public static void main(String[] args) {\n'
       '        int x = 5;\n'
       '        if (x > 10)\n'
       '            if (x > 20) System.out.println("big");\n'
       '        else System.out.println("small");\n'
       '        System.out.println("end");\n'
       '    }\n'
       '}',
  options=['small\nend', 'end', 'big\nend', 'small'],
  answer=1,
  why=['Wrong, and it is what the INDENTATION suggests, which is why the question is '
       'here. The else does not belong to the outer if.',
       'Correct. An else attaches to the nearest unmatched if, which is the INNER '
       'one. Since x is not greater than 10, neither if is entered and nothing but '
       'end prints.',
       'Wrong. x is 5, so the outer condition is already false.',
       'Wrong. The last println is outside every if and always runs.'],
  explanation='An else binds to the nearest if, whatever the indentation says. '
              'Braces on every if remove the ambiguity, and they cost nothing.')

q(id='j4-03', module=4, topic='for to while conversion', runs=True, cls='Q403',
  prompt='What does this print?',
  code='public class Q403 {\n'
       '    public static void main(String[] args) {\n'
       '        int sum = 0;\n'
       '        for (int i = 1; i <= 5; i++) sum += i;\n'
       '        System.out.println(sum);\n'
       '        int j = 1, prod = 1;\n'
       '        while (j <= 4) { prod *= j; j++; }\n'
       '        System.out.println(prod);\n'
       '    }\n'
       '}',
  options=['15\n24', '10\n24', '15\n10', '21\n24'],
  answer=0,
  why=['Correct. 1+2+3+4+5 is 15, and 1x2x3x4 is 24.',
       'Wrong. The loop includes 5, because the test is i <= 5, not i < 5.',
       'Wrong on the second: the while loop multiplies rather than adds.',
       'Wrong. 21 would be summing to 6, and the loop stops at 5.'],
  explanation='The three parts of a for header, initialise, test, update, are exactly '
              'the three pieces you place by hand when converting to a while. This '
              'conversion is worth 10 marks on the 2024/25 paper.')

q(id='j4-04', module=4, topic='do-while runs once', runs=True, cls='Q404',
  prompt='What does this print?',
  code='public class Q404 {\n'
       '    public static void main(String[] args) {\n'
       '        int n = 10;\n'
       '        while (n < 5) { System.out.println("while " + n); n++; }\n'
       '        do { System.out.println("do " + n); n++; } while (n < 5);\n'
       '    }\n'
       '}',
  options=['nothing is printed', 'do 10', 'while 10\ndo 10', 'do 10\ndo 11'],
  answer=1,
  why=['Wrong. The do-while body runs before its condition is ever looked at.',
       'Correct. The while loop tests first, finds 10 is not less than 5, and never '
       'runs. The do-while runs its body once, prints do 10, and only then tests.',
       'Wrong. The while loop prints nothing at all.',
       'Wrong. After the single pass n is 11, the condition fails, and the loop '
       'ends.'],
  explanation='while tests first and may run zero times; do-while runs at least once. '
              'That difference is the whole reason both exist.')

q(id='j4-05', module=4, topic='break and continue', runs=True, cls='Q405',
  prompt='What does this print?',
  code='public class Q405 {\n'
       '    public static void main(String[] args) {\n'
       '        for (int i = 1; i <= 5; i++) {\n'
       '            if (i == 2) continue;\n'
       '            if (i == 4) break;\n'
       '            System.out.print(i + " ");\n'
       '        }\n'
       '    }\n'
       '}',
  options=['1 3 ', '1 2 3 ', '1 3 5 ', '1 3 4 '],
  answer=0,
  why=['Correct. 1 prints, 2 is skipped by continue, 3 prints, and at 4 the break '
       'leaves the loop before 5 is reached.',
       'Wrong. The continue skips the print for 2.',
       'Wrong. The break at 4 stops the loop, so 5 never happens.',
       'Wrong. The break happens BEFORE the print, so 4 is never printed.'],
  explanation='continue abandons this pass, break abandons the loop. Read the order '
              'of the statements carefully: whether the break is before or after the '
              'print changes the answer.')

q(id='j4-06', module=4, topic='nested loops', runs=True, cls='Q406',
  prompt='What does this print?',
  code='public class Q406 {\n'
       '    public static void main(String[] args) {\n'
       '        for (int i = 1; i <= 3; i++) {\n'
       '            for (int j = 1; j <= i; j++) System.out.print("*");\n'
       '            System.out.println();\n'
       '        }\n'
       '    }\n'
       '}',
  options=['*\n**\n***', '***\n***\n***', '*\n*\n*', '***\n**\n*'],
  answer=0,
  why=['Correct. The inner loop runs i times, so one star, then two, then three.',
       'Wrong. The inner limit is i, not 3, so it grows with each outer pass.',
       'Wrong. That would need the inner loop to run exactly once each time.',
       'Wrong, and it is upside down: i grows, so the rows get longer.'],
  explanation='Triangle patterns are a standing favourite. Trace the inner limit for '
              'each value of the outer variable and write the row out; three rows of '
              'tracing settles any pattern question.')

q(id='j4-07', module=4, topic='off by one', runs=True, cls='Q407',
  prompt='How many times does the body run?',
  code='public class Q407 {\n'
       '    public static void main(String[] args) {\n'
       '        int count = 0;\n'
       '        for (int i = 0; i < 10; i += 2) count++;\n'
       '        System.out.println(count);\n'
       '    }\n'
       '}',
  options=['4', '5', '6', '10'],
  answer=1,
  why=['Wrong. Count them out: 0, 2, 4, 6, 8. That is five values, not four.',
       'Correct. i takes 0, 2, 4, 6 and 8, then 10 fails the test i < 10, so the body '
       'runs five times.',
       'Wrong. 10 is not less than 10, so it never enters with i at 10.',
       'Wrong. The step is 2, so it runs half as often as a step of 1 would.'],
  explanation='When a loop steps by more than one, write the values out rather than '
              'dividing in your head. The last value is the one people get wrong.')


# ===========================================================================
# MODULE FIVE: methods
# ===========================================================================
q(id='j5-01', module=5, topic='parameter passing', runs=True, cls='Q501',
  prompt='What does this print?',
  code='public class Q501 {\n'
       '    static void change(int n) { n = 99; }\n'
       '    public static void main(String[] args) {\n'
       '        int x = 5;\n'
       '        change(x);\n'
       '        System.out.println(x);\n'
       '    }\n'
       '}',
  options=['99', '5', '0', 'it does not compile'],
  answer=1,
  why=['Wrong. The method changed its own copy of the value, not the caller\'s '
       'variable.',
       'Correct. Java passes arguments BY VALUE. The parameter n is a separate '
       'variable holding a copy of 5, so assigning to it cannot reach x.',
       'Wrong. x was assigned 5 and nothing since has touched it.',
       'Wrong. The code is perfectly legal; it simply does not do what it looks like '
       'it does.'],
  explanation='Java is pass by value, always. For an object the VALUE passed is the '
              'reference, which is why an object\'s contents can be changed by a '
              'method while the caller\'s variable still points at the same object.')

q(id='j5-02', module=5, topic='passing an object', runs=True, cls='Q502',
  prompt='What does this print?',
  code='public class Q502 {\n'
       '    static void fill(int[] a) { a[0] = 99; }\n'
       '    static void replace(int[] a) { a = new int[]{7, 7}; }\n'
       '    public static void main(String[] args) {\n'
       '        int[] nums = {1, 2};\n'
       '        fill(nums);\n'
       '        replace(nums);\n'
       '        System.out.println(nums[0] + " " + nums[1]);\n'
       '    }\n'
       '}',
  options=['1 2', '99 2', '7 7', '99 7'],
  answer=1,
  why=['Wrong. fill really did change the array, because both names refer to the same '
       'array object.',
       'Correct. fill reaches through the reference and changes element 0. replace '
       'only rebinds its own copy of the reference, so the caller\'s array is '
       'untouched.',
       'Wrong. replace cannot change which array the caller\'s variable points at.',
       'Wrong for the same reason: nothing from replace escapes the method.'],
  explanation='Through the reference you can change the object; assigning to the '
              'parameter only changes where that copy points. This one pair of '
              'methods is the clearest statement of what pass by value means in Java.')

q(id='j5-03', module=5, topic='overloading', runs=True, cls='Q503',
  prompt='What does this print?',
  code='public class Q503 {\n'
       '    static String f(int n) { return "int"; }\n'
       '    static String f(double d) { return "double"; }\n'
       '    static String f(String s) { return "String"; }\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println(f(1));\n'
       '        System.out.println(f(1.0));\n'
       '        System.out.println(f("1"));\n'
       '    }\n'
       '}',
  options=['int\ndouble\nString', 'double\ndouble\nString', 'int\nint\nString',
           'it does not compile, because three methods share a name'],
  answer=0,
  why=['Correct. Overload resolution picks by the argument TYPES: 1 is an int, 1.0 is '
       'a double, "1" is a String.',
       'Wrong. 1 is an int literal and an exact int match exists, so no widening is '
       'needed.',
       'Wrong. 1.0 is a double literal, so the double version matches exactly.',
       'Wrong. Sharing a name with different parameter lists is exactly what '
       'overloading IS.'],
  explanation='Overloading is same name, different parameter list, resolved at compile '
              'time by the argument types. Return type alone cannot distinguish two '
              'overloads.')

q(id='j5-04', module=5, topic='static and instance',
  prompt='Why can a static method not use an instance field directly?',
  options=['Because static methods are private',
           'Because a static method may run with no object in existence, so there is '
           'no instance whose field it could mean',
           'Because instance fields are always final',
           'Because static methods run before the class is loaded'],
  answer=1,
  why=['Wrong. static and private are unrelated: a static method can be public.',
       'Correct. Static belongs to the class, so it can be called with no object at '
       'all. An instance field only exists inside an object, so the reference would '
       'be to nothing.',
       'Wrong. Instance fields are ordinarily variable; final is a separate choice.',
       'Wrong. The class is loaded before any of its methods run.'],
  explanation='Static belongs to the class, instance belongs to the object. This is '
              'exactly why main is static: the JVM calls it before any object of your '
              'class exists.')

q(id='j5-05', module=5, topic='return', runs=True, cls='Q505',
  prompt='What does this print?',
  code='public class Q505 {\n'
       '    static int addUp(int n) {\n'
       '        int total = 0;\n'
       '        for (int i = 1; i <= n; i++) {\n'
       '            total += i;\n'
       '            if (total > 6) return total;\n'
       '        }\n'
       '        return -1;\n'
       '    }\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println(addUp(5));\n'
       '    }\n'
       '}',
  options=['15', '10', '-1', '6'],
  answer=1,
  why=['Wrong. 15 is the full sum to 5, but the method leaves as soon as the running '
       'total passes 6.',
       'Correct. The totals are 1, 3, 6, 10. The first that is greater than 6 is 10, '
       'and return hands it back immediately.',
       'Wrong. The final return is only reached if the loop finishes without the '
       'condition ever being true.',
       'Wrong. 6 is not GREATER than 6, so the loop continues one more pass.'],
  explanation='return leaves the method at once, loop and all. Note the strictness of '
              'the comparison: greater than 6 excludes 6 itself.')


# ===========================================================================
# MODULE SIX: object-oriented programming
# ===========================================================================
q(id='j6-01', module=6, topic='constructors', runs=True, cls='Q601',
  prompt='What does this print?',
  code='public class Q601 {\n'
       '    static class Dog {\n'
       '        String name;\n'
       '        Dog() { this("unnamed"); }\n'
       '        Dog(String n) { name = n; }\n'
       '    }\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println(new Dog().name);\n'
       '        System.out.println(new Dog("Rex").name);\n'
       '    }\n'
       '}',
  options=['null\nRex', 'unnamed\nRex', 'unnamed\nunnamed', 'it does not compile'],
  answer=1,
  why=['Wrong. The no-argument constructor does not leave name unset: it calls the '
       'other constructor with a default.',
       'Correct. this("unnamed") chains to the other constructor, so the first object '
       'gets unnamed and the second gets Rex.',
       'Wrong. The second call passes Rex explicitly, and that is what is stored.',
       'Wrong. Constructor chaining with this(...) is legal, provided it is the first '
       'statement.'],
  explanation='A constructor has the class name, no return type, and runs on new. '
              'this(...) chains to another constructor and must be the first '
              'statement in the body.')

q(id='j6-02', module=6, topic='encapsulation',
  prompt='Which pair of choices implements encapsulation?',
  options=['Public fields and no methods',
           'Private fields with public getters and setters',
           'Static fields with a public constructor',
           'Final fields with no constructor'],
  answer=1,
  why=['Wrong, and it is the opposite: public fields let anything change the object '
       'into an invalid state with no check possible.',
       'Correct. The data is hidden and every route to it goes through a method, '
       'which is where validation can live.',
       'Wrong. static concerns whether the field belongs to the class or the object, '
       'and has nothing to do with hiding it.',
       'Wrong. final stops reassignment; it does not hide anything, and a class with '
       'no constructor still gets the default one.'],
  explanation='Private data, public methods. Hiding the data is only half of it: the '
              'point of the getter and setter is that they are a place to check.')

q(id='j6-03', module=6, topic='inheritance and overriding', runs=True, cls='Q603',
  prompt='What does this print?',
  code='public class Q603 {\n'
       '    static class Animal {\n'
       '        void speak() { System.out.println("some sound"); }\n'
       '    }\n'
       '    static class Dog extends Animal {\n'
       '        @Override void speak() { System.out.println("woof"); }\n'
       '    }\n'
       '    public static void main(String[] args) {\n'
       '        Animal a = new Dog();\n'
       '        a.speak();\n'
       '    }\n'
       '}',
  options=['some sound', 'woof', 'it does not compile',
           'both lines print, superclass first'],
  answer=1,
  why=['Wrong. The DECLARED type is Animal, but the method that runs is chosen by '
       'the object\'s ACTUAL type at run time.',
       'Correct. The object is a Dog, so Dog\'s override runs. This is polymorphism, '
       'and it is exactly what makes inheritance useful.',
       'Wrong. Assigning a subclass object to a superclass variable is always '
       'allowed: a Dog IS an Animal.',
       'Wrong. An override replaces the superclass version. Running both would need '
       'an explicit super.speak() call.'],
  explanation='The variable\'s type decides what you may CALL; the object\'s type '
              'decides what actually RUNS. That sentence answers most polymorphism '
              'questions on this paper.')

q(id='j6-04', module=6, topic='super', runs=True, cls='Q604',
  prompt='What does this print?',
  code='public class Q604 {\n'
       '    static class A {\n'
       '        A() { System.out.println("A"); }\n'
       '    }\n'
       '    static class B extends A {\n'
       '        B() { System.out.println("B"); }\n'
       '    }\n'
       '    public static void main(String[] args) { new B(); }\n'
       '}',
  options=['B', 'A\nB', 'B\nA', 'nothing prints'],
  answer=1,
  why=['Wrong. The superclass constructor always runs first, whether or not you '
       'wrote super().',
       'Correct. Java inserts an implicit super() at the top of B\'s constructor, so '
       'A\'s constructor completes before B\'s body starts.',
       'Wrong, and it is the wrong way round: the base is built before the part '
       'built on top of it.',
       'Wrong. new B() runs both constructors.'],
  explanation='Constructors run from the top of the hierarchy down. A subclass object '
              'cannot exist until the superclass part of it has been built.')

q(id='j6-05', module=6, topic='abstract classes and interfaces',
  prompt='Which statement is TRUE of an abstract class?',
  options=['It can be instantiated directly with new',
           'It may contain both abstract methods and fully implemented methods',
           'All of its methods must be abstract',
           'A class may extend several abstract classes at once'],
  answer=1,
  why=['Wrong. An abstract class is incomplete by definition, so new on it is a '
       'compile error. Its subclasses are what get instantiated.',
       'Correct. That is the difference from an interface in the classic form: an '
       'abstract class can carry shared state and shared behaviour alongside the '
       'methods it leaves to subclasses.',
       'Wrong. It may have none at all and still be marked abstract.',
       'Wrong. Java allows single inheritance of classes. Several INTERFACES may be '
       'implemented, which is how the restriction is worked around.'],
  explanation='Abstract class for shared state and partial implementation; interface '
              'for a contract that many unrelated classes can sign. One superclass, '
              'many interfaces.')

q(id='j6-06', module=6, topic='toString', runs=True, cls='Q606',
  prompt='What does this print?',
  code='public class Q606 {\n'
       '    static class Point {\n'
       '        int x = 1, y = 2;\n'
       '        @Override public String toString() { return "(" + x + ", " + y + ")"; }\n'
       '    }\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println(new Point());\n'
       '    }\n'
       '}',
  options=['(1, 2)', 'Point@1b6d3586', 'Point', 'it does not compile'],
  answer=0,
  why=['Correct. println on an object calls its toString(), and this class overrides '
       'it.',
       'Wrong for THIS class. That class-name-and-hash form is what the INHERITED '
       'toString gives, and it is what you see when you forget to override it.',
       'Wrong. Nothing prints just the class name.',
       'Wrong. Overriding toString is ordinary and expected.'],
  explanation='println on an object calls toString(). Override it and your objects '
              'become printable; forget to, and you get the class name and a hash.')


# ===========================================================================
# MODULE SEVEN: strings
# ===========================================================================
q(id='j7-01', module=7, topic='== against equals', runs=True, cls='Q701',
  prompt='What does this print?',
  code='public class Q701 {\n'
       '    public static void main(String[] args) {\n'
       '        String a = "hello";\n'
       '        String b = "hello";\n'
       '        String c = new String("hello");\n'
       '        System.out.println(a == b);\n'
       '        System.out.println(a == c);\n'
       '        System.out.println(a.equals(c));\n'
       '    }\n'
       '}',
  options=['true\ntrue\ntrue', 'true\nfalse\ntrue', 'false\nfalse\ntrue',
           'true\nfalse\nfalse'],
  answer=1,
  why=['Wrong on the second line. new String() deliberately builds a separate object, '
       'so the two references differ.',
       'Correct. Two identical literals share one pooled object, so a == b is true. '
       'new String makes a distinct object, so a == c is false. equals compares the '
       'CHARACTERS, so it is true.',
       'Wrong on the first line: string literals are interned, so both names point at '
       'the same pooled object.',
       'Wrong on the last line. equals compares contents, and the contents are the '
       'same.'],
  explanation='== asks whether they are the same OBJECT; equals asks whether they '
              'read the same. For strings, always use equals. This is the most asked '
              'string question there is.')

q(id='j7-02', module=7, topic='strings are immutable', runs=True, cls='Q702',
  prompt='What does this print?',
  code='public class Q702 {\n'
       '    public static void main(String[] args) {\n'
       '        String s = "java";\n'
       '        s.toUpperCase();\n'
       '        System.out.println(s);\n'
       '        System.out.println(s.toUpperCase());\n'
       '    }\n'
       '}',
  options=['JAVA\nJAVA', 'java\nJAVA', 'java\njava', 'JAVA\njava'],
  answer=1,
  why=['Wrong on the first line. The result of the first call was thrown away, '
       'because nothing was assigned.',
       'Correct. Strings are immutable, so toUpperCase returns a NEW string and '
       'leaves s alone. The first call changes nothing; the second prints its result '
       'directly.',
       'Wrong on the second line: the value returned by the call is what is printed, '
       'and it is uppercase.',
       'Wrong, and it has the two lines the wrong way round.'],
  explanation='A String method never changes the string. If you do not catch what it '
              'returns, nothing happened. A statement that is only a method call on a '
              'String is almost always a bug.')

q(id='j7-03', module=7, topic='substring and indexes', runs=True, cls='Q703',
  prompt='What does this print?',
  code='public class Q703 {\n'
       '    public static void main(String[] args) {\n'
       '        String s = "PROGRAM";\n'
       '        System.out.println(s.length());\n'
       '        System.out.println(s.charAt(0));\n'
       '        System.out.println(s.substring(1, 4));\n'
       '        System.out.println(s.indexOf("G"));\n'
       '    }\n'
       '}',
  options=['7\nP\nROG\n3', '7\nP\nROGR\n3', '7\nR\nROG\n4', '6\nP\nROG\n3'],
  answer=0,
  why=['Correct. Seven characters; index 0 is P; substring(1, 4) takes indexes 1, 2 '
       'and 3, stopping BEFORE 4; and the first G is at index 3.',
       'Wrong. substring stops before its second index, so it takes three characters, '
       'not four.',
       'Wrong. charAt(0) is the first character, P. Java indexes from zero.',
       'Wrong. PROGRAM has seven letters.'],
  explanation='length() has brackets on a String and none on an array, index from '
              'zero, and substring excludes its end index. Those three answer most '
              'string questions.')

q(id='j7-04', module=7, topic='StringBuilder',
  prompt='Why is StringBuilder preferred to String for building text in a loop?',
  options=['It is shorter to type',
           'String is immutable, so each join creates a new object, while '
           'StringBuilder changes one buffer in place',
           'StringBuilder can hold more characters than String',
           'String cannot be used inside a loop'],
  answer=1,
  why=['Wrong. It is longer to type, which is why the reason has to be a real one.',
       'Correct. Joining strings in a loop makes a fresh object every pass and throws '
       'the previous one away. StringBuilder appends to a single mutable buffer.',
       'Wrong. Neither has a practical limit you will meet on this course.',
       'Wrong. It can be used, it is just wasteful.'],
  explanation='Immutable means every join allocates. In a loop of n joins that is n '
              'objects created and discarded, which is why StringBuilder exists.')


# ===========================================================================
# MODULE EIGHT: arrays
# ===========================================================================
q(id='j8-01', module=8, topic='array basics', runs=True, cls='Q801',
  prompt='What does this print?',
  code='public class Q801 {\n'
       '    public static void main(String[] args) {\n'
       '        int[] a = new int[3];\n'
       '        a[0] = 5;\n'
       '        System.out.println(a.length);\n'
       '        System.out.println(a[1]);\n'
       '        System.out.println(a[0]);\n'
       '    }\n'
       '}',
  options=['3\n0\n5', '3\nnull\n5', '2\n0\n5', '3\n0\n0'],
  answer=0,
  why=['Correct. length is a FIELD on an array, with no brackets. An int array is '
       'filled with 0 when created, and a[0] was then set to 5.',
       'Wrong. null is the default for an OBJECT array. A numeric array defaults to '
       'zero.',
       'Wrong. new int[3] gives three elements, indexed 0, 1 and 2.',
       'Wrong. a[0] was assigned 5 on the second line.'],
  explanation='a.length with no brackets for an array, s.length() with brackets for a '
              'String. Arrays are created filled with the zero of their type: 0, 0.0, '
              'false or null.')

q(id='j8-02', module=8, topic='ArrayIndexOutOfBounds', runs=True, cls='Q802',
  prompt='What does this print?',
  code='public class Q802 {\n'
       '    public static void main(String[] args) {\n'
       '        int[] a = {1, 2, 3};\n'
       '        try {\n'
       '            System.out.println(a[3]);\n'
       '        } catch (ArrayIndexOutOfBoundsException e) {\n'
       '            System.out.println("caught " + e.getMessage());\n'
       '        }\n'
       '    }\n'
       '}',
  options=['3', 'caught Index 3 out of bounds for length 3', 'caught null', '0'],
  answer=1,
  why=['Wrong. Index 3 is the FOURTH element, and there are only three.',
       'Correct. Valid indexes are 0, 1 and 2, so a[3] throws, and the catch prints '
       'the exception\'s own message.',
       'Wrong. The exception carries a message describing the index and the length.',
       'Wrong. Reading past the end does not return a default; it throws.'],
  explanation='An array of length n has indexes 0 to n minus 1. The last valid index '
              'is always length minus one, and this off-by-one is the most common '
              'runtime error in the whole course.')

q(id='j8-03', module=8, topic='two-dimensional arrays', runs=True, cls='Q803',
  prompt='What does this print?',
  code='public class Q803 {\n'
       '    public static void main(String[] args) {\n'
       '        int[][] m = {{1, 2, 3}, {4, 5, 6}};\n'
       '        System.out.println(m.length);\n'
       '        System.out.println(m[0].length);\n'
       '        System.out.println(m[1][2]);\n'
       '    }\n'
       '}',
  options=['2\n3\n6', '3\n2\n6', '2\n3\n5', '6\n3\n6'],
  answer=0,
  why=['Correct. m.length is the number of ROWS, two. m[0].length is the length of '
       'the first row, three. m[1][2] is row 1, column 2, which is 6.',
       'Wrong, and it swaps rows and columns. The outer length is always the number '
       'of rows.',
       'Wrong. m[1][2] is the third element of the second row, which is 6, not 5.',
       'Wrong. m.length counts rows, not the total number of elements.'],
  explanation='Outer index is the row, inner index is the column, and both count from '
              'zero. m.length is rows; m[i].length is the width of row i.')

q(id='j8-04', module=8, topic='finding a maximum', runs=True, cls='Q804',
  prompt='What does this print?',
  code='public class Q804 {\n'
       '    public static void main(String[] args) {\n'
       '        int[] a = {-5, -2, -9};\n'
       '        int max = 0;\n'
       '        for (int x : a) if (x > max) max = x;\n'
       '        System.out.println(max);\n'
       '    }\n'
       '}',
  options=['-2', '0', '-9', '-5'],
  answer=1,
  why=['Wrong, and it is the answer the program was MEANT to give. It does not, '
       'because of the way max was initialised.',
       'Correct, and it is the bug. Starting max at 0 means no negative value can ever '
       'beat it, so 0 survives even though it is not in the array.',
       'Wrong. -9 is the smallest, not the largest.',
       'Wrong. -2 is larger than -5, so -5 could not win even with a correct start.'],
  explanation='Start max at the FIRST ELEMENT, never at zero. This exact fault is a '
              'standing exam favourite, and the fix is one line: int max = a[0], then '
              'loop from index 1.')


# ===========================================================================
# MODULE NINE: recursion
# ===========================================================================
q(id='j9-01', module=9, topic='factorial', runs=True, cls='Q901',
  prompt='What does this print?',
  code='public class Q901 {\n'
       '    static int fact(int n) {\n'
       '        if (n <= 1) return 1;\n'
       '        return n * fact(n - 1);\n'
       '    }\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println(fact(5));\n'
       '    }\n'
       '}',
  options=['15', '120', '5', 'StackOverflowError'],
  answer=1,
  why=['Wrong. 15 is the SUM 1+2+3+4+5. This method multiplies.',
       'Correct. 5 x 4 x 3 x 2 x 1 is 120, and the base case at n <= 1 stops the '
       'recursion.',
       'Wrong. The method does not simply return its argument.',
       'Wrong. There IS a base case and each call moves towards it, so the recursion '
       'terminates.'],
  explanation='Every recursion needs a base case and a step that moves towards it. '
              'Remove either and you get StackOverflowError, which is what the paper '
              'asks you to identify.')

q(id='j9-02', module=9, topic='fibonacci', runs=True, cls='Q902',
  prompt='What does this print?',
  code='public class Q902 {\n'
       '    static int fib(int n) {\n'
       '        if (n <= 1) return n;\n'
       '        return fib(n - 1) + fib(n - 2);\n'
       '    }\n'
       '    public static void main(String[] args) {\n'
       '        for (int i = 0; i < 7; i++) System.out.print(fib(i) + " ");\n'
       '    }\n'
       '}',
  options=['0 1 1 2 3 5 8 ', '1 1 2 3 5 8 13 ', '0 1 2 3 4 5 6 ', '1 2 3 5 8 13 21 '],
  answer=0,
  why=['Correct. The base case returns n itself for 0 and 1, so the sequence starts '
       '0, 1, and each later term is the sum of the two before it.',
       'Wrong. This version starts at 0, because fib(0) returns 0.',
       'Wrong. That is just the counting numbers, not a sum of the two previous '
       'terms.',
       'Wrong. Seven terms from index 0 ends at 8, not 21.'],
  explanation='Two base cases here, folded into one line: fib(0) is 0 and fib(1) is 1. '
              'Trace the first four calls on paper and the pattern becomes obvious.')

q(id='j9-03', module=9, topic='recursion against iteration',
  prompt='Which statement about recursion compared with iteration is TRUE?',
  options=['Recursion is always faster because it uses fewer instructions',
           'Recursion uses stack space for every pending call, so a deep recursion can '
           'exhaust it',
           'Any recursive method is impossible to write as a loop',
           'Recursion never needs a stopping condition'],
  answer=1,
  why=['Wrong. Recursion is usually SLOWER: every call costs a stack frame and the '
       'work of calling.',
       'Correct. Each call in progress keeps its frame until it returns, so depth '
       'costs memory, and running out of it is StackOverflowError.',
       'Wrong. Anything recursive can be written iteratively, sometimes with an '
       'explicit stack of your own.',
       'Wrong. Without a base case it never stops, and the program dies.'],
  explanation='Recursion buys clarity on naturally recursive problems and pays for it '
              'in stack space and call overhead. Both sides of that trade earn marks.')


# ===========================================================================
# MODULE TEN: exceptions and file input/output
# ===========================================================================
q(id='j10-01', module=10, topic='finally always runs', runs=True, cls='Q1001',
  prompt='What does this print?',
  code='public class Q1001 {\n'
       '    static int f() {\n'
       '        try {\n'
       '            return 1;\n'
       '        } finally {\n'
       '            System.out.println("finally");\n'
       '        }\n'
       '    }\n'
       '    public static void main(String[] args) {\n'
       '        System.out.println(f());\n'
       '    }\n'
       '}',
  options=['1', 'finally\n1', '1\nfinally', 'finally'],
  answer=1,
  why=['Wrong. The finally block runs even when the try block returns.',
       'Correct. The return value is computed, then finally runs on the way out, and '
       'only then does the caller receive the 1 and print it.',
       'Wrong on the order. finally runs BEFORE the method actually returns to its '
       'caller, so its output appears first.',
       'Wrong. The method does return 1, and main prints it.'],
  explanation='finally runs on every path out of a try, including a return. That is '
              'why it is where cleanup belongs.')

q(id='j10-02', module=10, topic='catch order', expect_error='has already been caught',
  cls='Q1002',
  prompt='What happens when this is compiled?',
  code='public class Q1002 {\n'
       '    public static void main(String[] args) {\n'
       '        try {\n'
       '            int x = 1 / 0;\n'
       '        } catch (Exception e) {\n'
       '            System.out.println("general");\n'
       '        } catch (ArithmeticException e) {\n'
       '            System.out.println("arithmetic");\n'
       '        }\n'
       '    }\n'
       '}',
  options=['It prints general', 'It prints arithmetic',
           'It does not compile: the second catch can never be reached',
           'It prints both lines'],
  answer=2,
  why=['Wrong. It never runs at all, because it does not compile.',
       'Wrong for the same reason, and the general catch would win in any case.',
       'Correct. Exception is the superclass of ArithmeticException, so the first '
       'catch already covers everything the second could. Java rejects unreachable '
       'catch clauses at compile time.',
       'Wrong. At most one catch clause ever runs for a given exception.'],
  explanation='Catch the most specific exception FIRST and the general one last. '
              'Reversing them is a compile error, not a subtle bug, which is the '
              'helpful part.')

q(id='j10-03', module=10, topic='checked and unchecked',
  prompt='Which statement is TRUE?',
  options=['A checked exception must be caught or declared with throws',
           'An unchecked exception must always be caught',
           'All exceptions in Java are checked',
           'A checked exception cannot be caught'],
  answer=0,
  why=['Correct. The compiler insists: handle it, or declare that your method may '
       'throw it. IOException is the one this course meets most.',
       'Wrong. Unchecked exceptions, the RuntimeException family, need neither. '
       'NullPointerException is the standard example.',
       'Wrong. Everything descending from RuntimeException and Error is unchecked.',
       'Wrong. It can be caught; it simply may not be ignored.'],
  explanation='Checked means the compiler makes you deal with it. Unchecked means it '
              'is your job to avoid it, and the commonest ones, null pointer and '
              'array index, are bugs rather than conditions.')

q(id='j10-04', module=10, topic='reading a file',
  prompt='Which class does this course use to read a text file line by line, and what '
         'must surround it?',
  options=['Scanner or BufferedReader, inside a try block that handles IOException',
           'System.out, inside a for loop',
           'FileWriter, inside a switch',
           'String, with no exception handling needed'],
  answer=0,
  why=['Correct. Either class can read lines, and file work throws a CHECKED '
       'exception, so it must be caught or declared.',
       'Wrong. System.out is the output stream, not a way in.',
       'Wrong. FileWriter writes. Reading needs a reader.',
       'Wrong. String is a type, not a file, and the exception handling is not '
       'optional for file access.'],
  explanation='Reading needs a reader and reading can fail, so it needs a catch. Both '
              'halves of that sentence earn marks.')

q(id='j10-05', module=10, topic='NullPointerException', runs=True, cls='Q1005',
  prompt='What does this print?',
  code='public class Q1005 {\n'
       '    public static void main(String[] args) {\n'
       '        String s = null;\n'
       '        try {\n'
       '            System.out.println(s.length());\n'
       '        } catch (NullPointerException e) {\n'
       '            System.out.println("null pointer");\n'
       '        }\n'
       '    }\n'
       '}',
  options=['0', 'null pointer', 'null', 'it does not compile'],
  answer=1,
  why=['Wrong. There is no object to measure, so nothing returns 0.',
       'Correct. s refers to no object, so calling a method on it throws '
       'NullPointerException, which the catch handles.',
       'Wrong. Printing s alone would show null; calling a METHOD on it throws.',
       'Wrong. It compiles perfectly. The fault only appears when it runs, which is '
       'what unchecked means.'],
  explanation='null means the reference points at no object. Reading it is fine; '
              'calling a method on it is not. Check for null before you dereference.')
