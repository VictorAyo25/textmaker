"""Learn by doing, COS221: each topic's method, taught from nothing and compiled.

    python scripts/author/cos221_doing.py

Writes the base of data/cos221/doing/m1.json to m9.json: the introduction, the
lock-in and the frames that teach each topic from nothing. The past questions
themselves are added by scripts/build-cos-doing.mjs, which lifts them with their
model answers from the two solved papers, and scripts/build-doing.mjs then
assembles the papers.

Every listing here is COMPILED BY javac AND RUN ON A JVM, by the same helper the
makeup manual uses, and the output printed under it is what Java actually
printed. A listing that does not compile stops the build, so a frame cannot
teach a program that would not run.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WEBAPP = HERE.parent.parent
REPO = WEBAPP.parent
TOOLS = REPO / "courses" / "COS221 - Computer Programming I (Java)" / "makeup" / "tools"
sys.path.insert(0, str(TOOLS))
import hl_java  # noqa: E402

OUT = WEBAPP / "data" / "cos221" / "doing"


def ran(src, stdin=""):
    """A listing plus what the JVM actually printed when it ran."""
    src = src.strip("\n")
    out = hl_java.run(src, stdin)
    return hl_java.listing(src) + hl_java.output(out)


def frag(src, note):
    """A fragment that is not a whole program, shown and never compiled."""
    return hl_java.fragment(src.strip("\n"), note)


def F(teach, ask="", check="", code=None, stdin=""):
    """One frame. `code` is compiled and run, and its output goes under it."""
    html = teach + (ran(code, stdin) if code else "")
    return {"check": check, "teach": html, "ask": ask}


TOPICS = {}


def T(key, **kw):
    TOPICS[key] = kw


# ============================================================== Topic One
T(
    "m1",
    kick="Topic One",
    title="Learn by Doing: The Language, the Toolchain and Objects",
    lead="The topic sat as a paper: its objective questions, then the method taught from nothing, with every listing compiled and run.",
    minutes=45,
    intro="<p><b>Part A</b> is every objective question the bank holds on this topic, the manual's own first.</p>"
    "<p><b>Part B is empty, and honestly so.</b> Neither past paper sets a written question on the toolchain by itself. It is asked in the objective half, and the skeleton below is the first six lines of every program you will write tomorrow, so the method still earns its place.</p>",
    lockin={
        "big": "\"javac turns .java into .class bytecode. java runs the bytecode on the JVM. The JDK contains the JRE, and the JRE contains the JVM.\"",
        "sub": "public static void main(String[] args) is the entry point, and the file name must match the public class name exactly, capital letters included.",
    },
    methodFrames=[
        F(
            "<p>Every Java program starts from the same six lines, and the exam expects you to write them without thinking. Here is the whole skeleton, compiled and run.</p>",
            ask="Before the explanation: which word makes this class visible to the JVM, and which line is the entry point?",
            code="""
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello from the JVM");
    }
}
""",
        ),
        F(
            "<p><b>public</b> makes it visible, and <b>main</b> is the entry point. Word by word: <code>public</code> visible everywhere, <code>static</code> callable without creating an object, <code>void</code> returns nothing, <code>main</code> the name the JVM looks for, <code>String[] args</code> the command line arguments.</p>",
            check="public, and the main line.",
            ask="The file must be called Hello.java. What happens if you save it as hello.java?",
        ),
        F(
            "<p>javac refuses it: <b>the file name must match the public class name exactly</b>, capital letter included. That is one of the planted errors in a debug question, so look at the class name first.</p>",
            check="It will not compile: the public class name and the file name must match.",
            ask="Two commands build and run it. What does each one produce?",
        ),
        F(
            "<p><b>javac Hello.java</b> compiles the source into <b>Hello.class</b>, which holds bytecode, not machine code. <b>java Hello</b> then runs that bytecode on the <b>JVM</b>. Note the second command takes the CLASS name, with no .class on the end.</p>",
            check="javac makes a .class file of bytecode; java runs it on the JVM.",
            ask="So why is Java called platform independent, and what is the phrase the examiner wants?",
        ),
        F(
            "<p><b>Write once, run anywhere.</b> The bytecode is the same on every machine, and each platform has its own JVM to run it. That is the whole answer to \"why is Java portable\".</p>",
            check="Because the bytecode runs on any JVM, so write once, run anywhere.",
            ask="Last piece of vocabulary: JDK, JRE and JVM. Which contains which?",
        ),
        F(
            "<p><b>The JDK contains the JRE, and the JRE contains the JVM.</b> The JDK is for developers and holds javac and the tools; the JRE is what a user needs to run a program; the JVM is the engine inside it. Draw it as three boxes inside one another and the mark is unmissable.</p>"
            "<p>One more pair the objective half asks: a <b>class</b> is the blueprint and an <b>object</b> is one thing built from it. <code>new</code> is what builds it.</p>",
            check="JDK contains JRE contains JVM.",
        ),
    ],
)

# ============================================================== Topic Two
T(
    "m2",
    kick="Topic Two",
    title="Learn by Doing: Types, Operators, Input and Output",
    lead="The topic sat as a paper: its objective questions, then the past question that uses JOptionPane, and the method taught from nothing with every listing run.",
    minutes=60,
    intro="<p><b>Part A</b> is the objective questions on this topic. <b>Part B</b> is past questions only, from the two solved papers.</p>"
    "<p>Integer division and the JOptionPane pattern are the two things in this topic that cost whole questions rather than single marks.</p>",
    lockin={
        "big": "\"int divided by int is an int. 7 / 2 is 3, and no amount of storing it in a double fixes it after the fact.\"",
        "sub": "Cast one side first, or use a double literal. JOptionPane reads a String, so parse it with Integer.parseInt or Double.parseDouble.",
    },
    methodFrames=[
        F(
            "<p>The eight primitives are <b>byte, short, int, long, float, double, char, boolean</b>. Whole numbers are int, decimals are double, and everything else is a special case.</p>",
            ask="What do you think this prints, before you look?",
            code="""
public class Divide {
    public static void main(String[] args) {
        int a = 7, b = 2;
        System.out.println(a / b);
        double wrong = a / b;
        System.out.println(wrong);
        double right = (double) a / b;
        System.out.println(right);
    }
}
""",
        ),
        F(
            "<p><b>int divided by int is an int</b>, and the fraction is thrown away at the moment of division. Storing the answer in a double afterwards is too late, which is why the second line still prints 3.0.</p>"
            "<p>The fix is to cast BEFORE dividing, or to make one side a double literal: <code>(double) a / b</code>, or <code>a / 2.0</code>.</p>",
            check="3, then 3.0, then 3.5.",
            ask="Now the other arithmetic trap. What does the modulus operator give you, and what is it used for in every exam question about digits?",
        ),
        F(
            "<p><b>% gives the remainder</b>, and the pair <code>n % 10</code> and <code>n / 10</code> is how you take a number apart digit by digit: the first gives the last digit, the second removes it.</p>",
            check="The remainder. n % 10 is the last digit and n / 10 drops it.",
            ask="Armstrong numbers, perfect numbers, palindromes and digit counts are all built on that pair. What does this print?",
            code="""
public class Digits {
    public static void main(String[] args) {
        int n = 407, sum = 0;
        while (n > 0) {
            int digit = n % 10;
            sum += digit * digit * digit;
            n = n / 10;
        }
        System.out.println(sum);
    }
}
""",
        ),
        F(
            "<p>It prints 407, because 4 cubed plus 0 cubed plus 7 cubed is 407: that is an Armstrong number, and it is a past question in Topic Three.</p>"
            "<p>Now the increment trap. <code>i++</code> uses the value THEN adds one; <code>++i</code> adds one THEN uses it.</p>",
            check="407.",
            ask="So what does this print?",
            code="""
public class Increment {
    public static void main(String[] args) {
        int i = 5;
        System.out.println(i++);
        System.out.println(i);
        System.out.println(++i);
    }
}
""",
        ),
        F(
            "<p>5, then 6, then 7. Read it as: post increment hands over the old value, pre increment hands over the new one.</p>"
            "<p>One more operator trap: <b>+ joins when either side is a String</b>. <code>\"total: \" + 1 + 2</code> gives \"total: 12\", because it works left to right. Bracket the arithmetic.</p>",
            check="5, 6, 7.",
            ask="Now input. This paper's Section C says JOptionPane only. What does showInputDialog return?",
        ),
        F(
            "<p><b>A String, always</b>, exactly like Scanner's nextLine. So it must be parsed: <code>Integer.parseInt(text)</code> or <code>Double.parseDouble(text)</code>. Forgetting that is the single most common lost mark in Section C.</p>"
            "<p>The pattern to memorise, since it is not compiled here only because it opens a window:</p>"
            + frag(
                """
import javax.swing.JOptionPane;

public class Fees {
    public static void main(String[] args) {
        String text = JOptionPane.showInputDialog("How many hours?");
        int hours = Integer.parseInt(text);
        double fee = hours * 150.0;
        JOptionPane.showMessageDialog(null, "Fee: " + fee);
        System.exit(0);
    }
}
""",
                "a GUI program: it opens a window rather than printing",
            ),
            check="A String.",
            ask="Two more lines in that skeleton earn marks. Which, and why?",
        ),
        F(
            "<p><b>import javax.swing.JOptionPane;</b> at the top, and <b>System.exit(0);</b> at the end, which closes the program after the last dialog. Both are on the mark scheme, and both are one line each.</p>"
            "<p>For printed output, <code>printf</code> formats: <code>%d</code> whole number, <code>%.2f</code> two decimals, <code>%s</code> string, <code>%n</code> newline.</p>",
            check="The import, and System.exit(0).",
        ),
    ],
)

# ============================================================ Topic Three
T(
    "m3",
    kick="Topic Three",
    title="Learn by Doing: Control Structures",
    lead="The topic sat as a paper: its objective questions, then every past question on decisions, loops and dry runs, each with its model answer, and the method taught from nothing.",
    minutes=90,
    intro="<p><b>Part A</b> is the objective questions on this topic, the largest group in the bank. <b>Part B</b> is past questions only, and this topic carries the most of them: every dry run, every debug snippet built on a loop, and the number theory programs.</p>"
    "<p>The dry run is the cheapest question on the paper and the one most often lost, because it is done in the head instead of in a table.</p>",
    lockin={
        "big": "\"A dry run is a table, one column per variable and one row per pass. Never do it in your head.\"",
        "sub": "A for loop when the count is known, a while when it is not, a do-while when the body must run at least once. break leaves the loop, continue skips to the next pass.",
    },
    methodFrames=[
        F(
            "<p>Three loops, and the exam asks you to tell them apart and to convert between them. A <b>for</b> loop when you know how many times, a <b>while</b> when you do not, a <b>do-while</b> when the body must run at least once.</p>",
            ask="What do you expect each of these three to print?",
            code="""
public class Loops {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) System.out.print(i + " ");
        System.out.println();

        int j = 5;
        while (j >= 1) { System.out.print(j + " "); j--; }
        System.out.println();

        int k = 10;
        do { System.out.print("ran once "); k++; } while (k < 5);
        System.out.println();
    }
}
""",
        ),
        F(
            "<p>The do-while is the one to notice: its condition was false from the start and the body still ran, because a do-while tests AFTER. That is a favourite objective question.</p>"
            "<p>Converting a for into a while is on the paper: take the three parts out of the for and put them where they belong.</p>"
            + frag(
                """
for (int i = 1; i <= 5; i++) { ... }

int i = 1;          // 1. the initialisation goes above the loop
while (i <= 5) {    // 2. the condition goes in the while
    ...
    i++;            // 3. the update goes at the END of the body
}
""",
                "the conversion, side by side",
            ),
            check="1 2 3 4 5, then 5 4 3 2 1, then ran once.",
            ask="If you put the update at the TOP of the while body instead of the bottom, what breaks?",
        ),
        F(
            "<p>The first pass uses the wrong value and the loop runs one fewer time. That is a planted error in a debug question, so check where the update sits every time.</p>"
            "<p>Now the dry run, which is four marks on the 24/25 paper, three times over. The method is a <b>table</b>: one column per variable, one row per pass.</p>",
            check="The first pass uses the wrong value and the count is off by one.",
            ask="Trace this one on paper before you run it: what is the final sum?",
            code="""
public class Trace {
    public static void main(String[] args) {
        int sum = 0;
        for (int i = 1; i <= 7; i++) {
            if (i % 2 == 0) continue;
            if (i > 5) break;
            sum += i;
            System.out.println("i=" + i + " sum=" + sum);
        }
        System.out.println("final " + sum);
    }
}
""",
        ),
        F(
            "<p>9. The even numbers are skipped by <b>continue</b>, and <b>break</b> leaves the loop at i = 7 before it can be added. The two keywords are asked as a pair: <b>continue skips the rest of this pass, break leaves the loop entirely</b>.</p>",
            check="9, from 1 + 3 + 5.",
            ask="Now decisions. In an if-else-if ladder, why does the order of the tests matter?",
        ),
        F(
            "<p>Because <b>the ladder stops at the first true test</b>. A grade ladder must run from the highest boundary down, or a score of 90 matches a test for 45 and above and is graded wrongly.</p>",
            check="It stops at the first test that is true, so a wide test placed early swallows everything.",
            ask="A switch does the same job for exact values. What happens if you leave out a break inside it?",
            code="""
public class Fall {
    public static void main(String[] args) {
        int level = 2;
        switch (level) {
            case 1: System.out.println("Bronze");
            case 2: System.out.println("Silver");
            case 3: System.out.println("Gold"); break;
            default: System.out.println("unranked");
        }
    }
}
""",
        ),
        F(
            "<p>It <b>falls through</b>: execution carries on into the next case until it meets a break. Level 2 printed Silver AND Gold, because only the third case ends in a break. Deliberate fall through is used to group cases; accidental fall through is a planted error.</p>"
            "<p>Note the rest of the rules: a switch works on int, char, String and enum, <code>default</code> catches everything else, and case labels must be constants.</p>",
            check="Silver and Gold, because the missing break falls through.",
        ),
    ],
)

# ============================================================= Topic Four
T(
    "m4",
    kick="Topic Four",
    title="Learn by Doing: Methods",
    lead="The topic sat as a paper: its objective questions, then every past question on methods and overloading, each with its model answer, and the method taught from nothing.",
    minutes=70,
    intro="<p><b>Part A</b> is the objective questions on this topic. <b>Part B</b> is past questions only. Both papers open on this topic: 25/26 asks you to define overloading and the role of the signature, and 24/25 asks for three definitions and then a program that overloads area.</p>",
    lockin={
        "big": "\"The signature is the name and the parameter list. The return type is not part of it, which is why two methods cannot differ by return type alone.\"",
        "sub": "Java passes by value: a method cannot change the caller's int. An array variable holds a reference, so its contents can be changed.",
    },
    methodFrames=[
        F(
            "<p>A method is a named block that does one job. The header carries four things in order: <b>modifiers, return type, name, parameter list</b>.</p>",
            ask="Which of those four make up the SIGNATURE, the part the compiler uses to tell two methods apart?",
            code="""
public class Area {
    static double area(double r) { return Math.PI * r * r; }
    static double area(double l, double w) { return l * w; }
    static double area(double b, double h, boolean triangle) { return 0.5 * b * h; }

    public static void main(String[] args) {
        System.out.printf("circle %.2f%n", area(7));
        System.out.printf("rectangle %.2f%n", area(4, 5));
        System.out.printf("triangle %.2f%n", area(6, 8, true));
    }
}
""",
        ),
        F(
            "<p><b>The name and the parameter list</b>, and nothing else. The return type is NOT part of the signature, which is the precise point 25/26 asks for: it is the signature that lets the compiler resolve an overloaded call at compile time.</p>"
            "<p>So <b>overloading</b> is several methods with the same name whose parameter lists differ in number, type or order.</p>",
            check="The name and the parameter list.",
            ask="Two methods differ only in return type, int and double. Will that compile?",
        ),
        F(
            "<p>No. The signatures are identical, so the compiler cannot choose, and it is a compile error. That single sentence answers half the overloading questions in the objective half.</p>"
            "<p>Now the distinction the paper asks for in words: a <b>parameter</b> is the name in the header, an <b>argument</b> is the value in the call.</p>",
            check="No: same signature, so it will not compile.",
            ask="A void method and a value returning one. What is the difference in what the CALL is worth?",
        ),
        F(
            "<p>A <b>void</b> method hands nothing back, so its call cannot be assigned or printed. A value returning method ends in <code>return</code>, and its call IS a value. In the exam, prefer a method that returns: Section B and C both say \"a method that returns\".</p>",
            check="A void call is not a value; a value returning call is.",
            ask="Now pass by value. What does this print, and why does the array behave differently from the int?",
            code="""
public class PassByValue {
    static void change(int n, int[] nums) {
        n = 99;
        nums[0] = 99;
    }

    public static void main(String[] args) {
        int n = 1;
        int[] nums = {1, 2, 3};
        change(n, nums);
        System.out.println(n + " " + nums[0]);
    }
}
""",
        ),
        F(
            "<p>1 and 99. <b>Java always passes by value</b>, but the value of an array variable is a REFERENCE to the array. The copy of that reference still points at the same array, so a change through it is visible to the caller; the copy of the int is just a copy.</p>",
            check="1 99.",
            ask="Last: static. Why can main call a method directly only if that method is static?",
        ),
        F(
            "<p>Because <b>main is static</b>, so it runs without an object, and it can only call other static methods directly. A non static method needs an object first: <code>new Thing().method()</code>. Marking a helper method <code>static</code> in an exam program is the simplest way to keep it callable from main.</p>",
            check="main is static, so it has no object to call an instance method on.",
        ),
    ],
)

# ============================================================= Topic Five
T(
    "m5",
    kick="Topic Five",
    title="Learn by Doing: Object-Oriented Programming",
    lead="The topic sat as a paper: its objective questions, then every past question on classes, inheritance and polymorphism, each with its model answer, and the method taught from nothing.",
    minutes=90,
    intro="<p><b>Part A</b> is the objective questions on this topic. <b>Part B</b> is past questions only, and this is where the biggest single question lives: the 25 mark bank account question on inheritance and polymorphism, plus Vehicle and TemperatureCheck from 24/25.</p>"
    "<p>Those questions are marked on structure, so learn the shape of a class and write it the same way every time.</p>",
    lockin={
        "big": "\"Private fields, a constructor that sets them, getters and setters, and a method that does the work. That is encapsulation, and it is worth marks before the logic is even read.\"",
        "sub": "Overriding replaces a superclass method, same signature, in a subclass. Overloading is same name, different parameters, in one class. super() calls the parent constructor and must come first.",
    },
    methodFrames=[
        F(
            "<p>A class is a blueprint; an object is one thing built from it with <code>new</code>. The exam's class questions always want the same four parts: private fields, a constructor, getters and setters, and a method that does the work.</p>",
            ask="Read this and say what the constructor is for, and why the fields are private.",
            code="""
public class Student {
    private String name;
    private double cgpa;

    public Student(String name, double cgpa) {
        this.name = name;
        this.cgpa = cgpa;
    }

    public String getName() { return name; }
    public void setCgpa(double cgpa) {
        if (cgpa >= 0 && cgpa <= 5) this.cgpa = cgpa;
    }

    public String classify() {
        if (cgpa >= 4.5) return "First Class";
        if (cgpa >= 3.5) return "Second Upper";
        return "Lower";
    }

    public static void main(String[] args) {
        Student s = new Student("Ada", 4.6);
        System.out.println(s.getName() + ": " + s.classify());
        s.setCgpa(9.9);
        System.out.println("after a bad set: " + s.classify());
    }
}
""",
        ),
        F(
            "<p>The constructor <b>sets the fields when the object is created</b>, and it has the class's name and no return type. The fields are private so nothing outside can set a CGPA of 9.9: the setter refused it, which is why the classification did not change.</p>"
            "<p>That is <b>encapsulation</b>: data hidden behind methods that can validate it. Say the word AND the reason in the exam.</p>",
            check="It sets the fields at creation; private fields force changes through a setter that can check them.",
            ask="What is this. for, in this.name = name?",
        ),
        F(
            "<p><code>this</code> is the object the method was called on, so <code>this.name</code> is the FIELD and <code>name</code> alone is the PARAMETER. Without it the parameter would simply assign to itself and the field would stay empty.</p>",
            check="It separates the field from the parameter of the same name.",
            ask="Now inheritance. What does extends give the subclass, and what does super do?",
            code="""
class Vehicle {
    protected int speed;
    public Vehicle(int speed) { this.speed = speed; }
    public void display() { System.out.println("Vehicle at " + speed); }
}

class Car extends Vehicle {
    private int doors;
    public Car(int speed, int doors) {
        super(speed);
        this.doors = doors;
    }
    @Override
    public void display() { System.out.println("Car at " + speed + " with " + doors + " doors"); }
}

public class Ride {
    public static void main(String[] args) {
        Vehicle[] fleet = { new Vehicle(80), new Car(120, 4) };
        for (Vehicle v : fleet) v.display();
    }
}
""",
        ),
        F(
            "<p><b>extends</b> gives the subclass every field and method of the superclass, and <b>super(speed)</b> calls the parent constructor, which must be the first line of the child's constructor.</p>"
            "<p>Now look at what the loop did: both objects are held in a <code>Vehicle</code> array, but each printed its OWN version of display.</p>",
            check="extends inherits everything; super() calls the parent constructor first.",
            ask="What is that called, and when does Java decide which display to run?",
        ),
        F(
            "<p><b>Polymorphism</b>, and the decision is made at RUN TIME, from the actual object rather than the declared type. That is dynamic method dispatch, and it is the sentence the 25 mark question is marked on.</p>"
            "<p>The method in the child is an <b>override</b>: same name, same parameters, same return type. <code>@Override</code> is optional but it makes the compiler check you.</p>",
            check="Polymorphism, decided at run time by the actual object.",
            ask="Overriding against overloading, three differences. Say them before you read on."
        ),
        F(
            "<p><b>Overloading:</b> same name, DIFFERENT parameter lists, in the SAME class, resolved at COMPILE time. <b>Overriding:</b> same name and same parameters, in a SUBCLASS, resolved at RUN time. Overloading is about convenience; overriding is about replacing behaviour.</p>"
            "<p>That is 25/26's three mark question, and it is three lines if you learn the pairs: where, what differs, when it is resolved.</p>",
            check="Different parameters against identical ones, same class against subclass, compile time against run time.",
        ),
    ],
)

# ============================================================== Topic Six
T(
    "m6",
    kick="Topic Six",
    title="Learn by Doing: Strings",
    lead="The topic sat as a paper: its objective questions, then the method taught from nothing, with every listing compiled and run.",
    minutes=45,
    intro="<p><b>Part A</b> is every objective question the bank holds on this topic.</p>"
    "<p><b>Part B is empty, and honestly so.</b> Neither past paper sets a written question on strings by itself. They appear inside other questions instead, so the trap below is still worth ten minutes: comparing strings with == is the fastest way to lose a program question that is otherwise right.</p>",
    lockin={
        "big": "\"== compares references. equals compares characters. For strings, always equals.\"",
        "sub": "A String cannot be changed, only rebuilt, so every method returns a new one. Use StringBuilder when you are building in a loop.",
    },
    methodFrames=[
        F(
            "<p>Start with the trap, because it costs whole questions.</p>",
            ask="Both pairs hold the same characters. Do you expect both comparisons to be true?",
            code="""
public class Compare {
    public static void main(String[] args) {
        String a = "java";
        String b = "java";
        String c = new String("java");

        System.out.println(a == b);
        System.out.println(a == c);
        System.out.println(a.equals(c));
    }
}
""",
        ),
        F(
            "<p>true, false, true. <b>== asks whether they are the same OBJECT</b>; equals asks whether they hold the same characters. The literals share one pooled object, so == happened to be true; the moment <code>new</code> is used it is false.</p>"
            "<p>So: <b>always compare strings with equals</b>, and with equalsIgnoreCase when case does not matter.</p>",
            check="No: true, false, true.",
            ask="Now immutability. What does this print, and why?",
            code="""
public class Immutable {
    public static void main(String[] args) {
        String s = "java";
        s.toUpperCase();
        System.out.println(s);
        s = s.toUpperCase();
        System.out.println(s);
    }
}
""",
        ),
        F(
            "<p>java, then JAVA. A String <b>cannot be changed in place</b>, so every method returns a NEW string and leaves the original alone. Calling a method without assigning the result changes nothing.</p>",
            check="java then JAVA: the first call was thrown away.",
            ask="Which methods are worth memorising for the exam?",
        ),
        F(
            "<p>The eight that appear: <code>length()</code>, <code>charAt(i)</code>, <code>substring(a, b)</code>, <code>indexOf(x)</code>, <code>equals</code>, <code>toUpperCase</code>, <code>trim()</code>, <code>split(sep)</code>. Note <code>length()</code> is a METHOD on a String but <code>length</code> is a FIELD on an array, with no brackets, which is asked directly.</p>",
            ask="Last: why does building a long string inside a loop with + get slow?",
            code="""
public class Build {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= 5; i++) sb.append(i).append(",");
        sb.setLength(sb.length() - 1);
        System.out.println(sb.toString());
        System.out.println(sb.reverse());
    }
}
""",
        ),
        F(
            "<p>Because each + builds a whole new String and throws the old one away, so a loop of n appends copies the text n times. <b>StringBuilder</b> is mutable: append, insert, reverse and setLength all change the one object, and toString hands you the finished String.</p>",
            check="Every + creates a new String, so the work grows with the length.",
        ),
    ],
)

# ============================================================ Topic Seven
T(
    "m7",
    kick="Topic Seven",
    title="Learn by Doing: Arrays",
    lead="The topic sat as a paper: its objective questions, then every past question that walks an array, each with its model answer, and the four patterns taught from nothing.",
    minutes=90,
    intro="<p><b>Part A</b> is the objective questions on this topic. <b>Part B</b> is past questions only, and no topic carries more of them: the consecutive duplicates, the discount loop, the temperature streak, the parking batch and countNegatives are all one array walk with a different test inside.</p>"
    "<p>Learn the four patterns as METHODS THAT RETURN, because that is how both papers ask for them.</p>",
    lockin={
        "big": "\"Declare, create, fill, walk. length is a field with no brackets, and the last index is length minus 1.\"",
        "sub": "Four patterns: total, count matching, best so far, and the neighbour comparison a[i] against a[i-1]. Each one is a method that returns a value."
    },
    methodFrames=[
        F(
            "<p>An array is a fixed length row of values of one type. Three steps: declare, create with a size, then fill.</p>",
            ask="What is the highest index of an array created with new int[5], and what happens if you use 5?",
            code="""
public class Walk {
    public static void main(String[] args) {
        int[] nums = new int[5];
        for (int i = 0; i < nums.length; i++) nums[i] = (i + 1) * 10;

        int[] given = {4, -2, 7, -9, 3};
        System.out.println(nums.length + " " + nums[nums.length - 1]);

        try {
            System.out.println(given[5]);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("caught: " + e.getMessage());
        }
    }
}
""",
        ),
        F(
            "<p>The highest index is 4, and index 5 throws <b>ArrayIndexOutOfBoundsException</b>, which 24/25 asks you to define by name. The loop condition is therefore <code>i &lt; nums.length</code>, never <code>&lt;=</code>.</p>"
            "<p><b>length is a field</b> on an array, with no brackets, unlike a String's length().</p>",
            check="4, and index 5 throws ArrayIndexOutOfBoundsException.",
            ask="Now the patterns. Write, in your head, a method that returns the total of an array.",
        ),
        F(
            "<p>Here are the four the exam wants, each as a method that returns, which is exactly how the papers word it.</p>",
            check="A running total set to zero before the loop, added to inside it, returned after it.",
            ask="Read the four and predict the four printed values.",
            code="""
public class Patterns {
    static int total(int[] a) {
        int sum = 0;
        for (int x : a) sum += x;
        return sum;
    }

    static int countNegatives(int[] a) {
        int count = 0;
        for (int x : a) if (x < 0) count++;
        return count;
    }

    static int largest(int[] a) {
        int best = a[0];
        for (int x : a) if (x > best) best = x;
        return best;
    }

    static int consecutiveDuplicates(int[] a) {
        int pairs = 0;
        for (int i = 1; i < a.length; i++) if (a[i] == a[i - 1]) pairs++;
        return pairs;
    }

    public static void main(String[] args) {
        int[] sales = {12, 12, -5, 30, 30, 30, -1};
        System.out.println(total(sales));
        System.out.println(countNegatives(sales));
        System.out.println(largest(sales));
        System.out.println(consecutiveDuplicates(sales));
    }
}
""",
        ),
        F(
            "<p>108, 2, 30, 3. Notice what the fourth one does differently: it starts at <b>i = 1</b> and looks BACK at <code>a[i - 1]</code>. Every question about repeats, streaks or rises uses that one line.</p>"
            "<p>Notice too that the best so far pattern starts from <code>a[0]</code>, not from zero: start from zero and an array of negatives returns the wrong answer.</p>",
            check="108, 2, 30, 3.",
            ask="A streak question asks for the LONGEST run. What two variables does that need?",
        ),
        F(
            "<p>A <b>current</b> run and a <b>best</b> run: extend current when the test holds, reset it to zero or one when it breaks, and update best whenever current beats it. That is the cold storage temperature question in one sentence.</p>",
            check="One for the run you are in, one for the longest seen.",
            ask="Last: two dimensions. How do you walk a table of rows and columns?",
            code="""
public class Grid {
    public static void main(String[] args) {
        int[][] marks = { {70, 65}, {40, 55}, {90, 80} };
        for (int r = 0; r < marks.length; r++) {
            int sum = 0;
            for (int c = 0; c < marks[r].length; c++) sum += marks[r][c];
            System.out.println("row " + r + " total " + sum);
        }
    }
}
""",
        ),
        F(
            "<p>A loop inside a loop: the outer over <code>marks.length</code>, the rows, the inner over <code>marks[r].length</code>, that row's columns. Writing the inner bound as marks.length is a planted error, and it only shows when the table is not square.</p>",
            check="Nested loops, the inner one bounded by that row's own length.",
        ),
    ],
)

# ============================================================ Topic Eight
T(
    "m8",
    kick="Topic Eight",
    title="Learn by Doing: Recursion",
    lead="The topic sat as a paper: its objective questions, then the past question that traces a recursive method, with its model answer, and the method taught from nothing.",
    minutes=50,
    intro="<p><b>Part A</b> is the objective questions on this topic. <b>Part B</b> is past questions only: 24/25 asks what compute(13) returns and to show the steps, which is a trace, not a definition.</p>"
    "<p>A recursion question is answered with a two column table: the call, and what it is waiting for.</p>",
    lockin={
        "big": "\"Every recursive method needs a base case that returns without calling itself, and a recursive case that moves towards it.\"",
        "sub": "Trace it as a table of calls going down and answers coming back up. No base case, or one you never reach, is a StackOverflowError."
    },
    methodFrames=[
        F(
            "<p>A recursive method calls itself on a smaller version of the problem. Two parts, always: the <b>base case</b>, which returns without calling itself, and the <b>recursive case</b>, which moves towards the base case.</p>",
            ask="Find both parts in this, then predict the two printed values.",
            code="""
public class Recurse {
    static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }

    static int digitSum(int n) {
        if (n < 10) return n;
        return n % 10 + digitSum(n / 10);
    }

    public static void main(String[] args) {
        System.out.println(factorial(5));
        System.out.println(digitSum(13));
    }
}
""",
        ),
        F(
            "<p>120 and 4. In factorial the base case is <code>n &lt;= 1</code>; in digitSum it is <code>n &lt; 10</code>, one digit left. Both recursive cases shrink the argument, which is what guarantees the base case is reached.</p>",
            check="120 and 4.",
            ask="What happens if the base case is missing, or never reached?",
        ),
        F(
            "<p>The calls pile up until the call stack is full and the program dies with a <b>StackOverflowError</b>. Naming that error is a mark, and \"no base case\" is a planted error in a debug question.</p>",
            check="It recurses forever and throws StackOverflowError.",
            ask="Now the trace, which is how the paper asks it. Write out digitSum(13) as calls going down and answers coming back."
        ),
        F(
            "<p>Two columns, and both directions matter:</p>"
            "<table><tr><th>Going down</th><th>Coming back</th></tr>"
            "<tr><td>digitSum(13) needs 3 + digitSum(1)</td><td>3 + 1 = <b>4</b></td></tr>"
            "<tr><td>digitSum(1), and 1 is under 10</td><td>returns 1</td></tr></table>"
            "<p>Write the table, then the answer. The marks in \"show the steps\" are the steps, not the number.</p>",
            check="digitSum(13) = 3 + digitSum(1) = 3 + 1 = 4.",
            ask="Last: recursion against iteration. One advantage each.",
        ),
        F(
            "<p><b>Recursion</b> is shorter and closer to the definition for problems that are naturally recursive, factorials, Fibonacci, tree walks. <b>Iteration</b> uses no call stack, so it is faster and cannot overflow. Any recursive method can be written as a loop, and the exam sometimes asks for both.</p>",
            check="Recursion is clearer for recursive definitions; iteration is faster and safer on memory.",
        ),
    ],
)

# ============================================================= Topic Nine
T(
    "m9",
    kick="Topic Nine",
    title="Learn by Doing: Exceptions and File Input and Output",
    lead="The topic sat as a paper: its objective questions, then every past question on exceptions and files, each with its model answer, and the method taught from nothing.",
    minutes=80,
    intro="<p><b>Part A</b> is the objective questions on this topic. <b>Part B</b> is past questions only, and a whole question of the 24/25 paper is files, end to end: define the classes, debug a snippet, state what the file contains, then write a program that creates it, writes records and reads them back.</p>",
    lockin={
        "big": "\"Checked exceptions must be caught or declared with throws, and the compiler enforces it. Unchecked ones are your bugs, and it does not.\"",
        "sub": "FileWriter with true appends, without it overwrites. try-with-resources closes the file for you, whatever happens."
    },
    methodFrames=[
        F(
            "<p>An exception is an error raised while the program runs. Java splits them in two, and the difference is who is responsible.</p>",
            ask="Which kind does the compiler force you to handle, and what is the other kind usually caused by?",
            code="""
public class Kinds {
    public static void main(String[] args) {
        int[] a = {1, 2, 3};
        try {
            System.out.println(a[5]);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("unchecked: " + e.getMessage());
        }

        try {
            System.out.println(Integer.parseInt("ten"));
        } catch (NumberFormatException e) {
            System.out.println("unchecked: " + e.getMessage());
        } finally {
            System.out.println("finally always runs");
        }
    }
}
""",
        ),
        F(
            "<p><b>Checked</b> exceptions are the ones the compiler forces you to catch or declare, IOException and FileNotFoundException among them, and they are about the world outside the program. <b>Unchecked</b> ones extend RuntimeException, are your own bugs, and the compiler says nothing: the two above are unchecked.</p>"
            "<p>Three differences for the 25/26 question: checked are checked at compile time, unchecked at run time; checked must be handled or declared, unchecked need not be; checked signal outside failures, unchecked signal programming faults.</p>",
            check="Checked ones. Unchecked ones come from bugs in the code.",
            ask="In that listing, when did finally run, and when would it not?",
        ),
        F(
            "<p>It ran after the catch, and it runs whether or not an exception was thrown, which is why it is where files and connections are closed. It is skipped only if the JVM itself exits.</p>"
            "<p><b>throw</b> raises an exception now; <b>throws</b> in a header declares that this method may raise one and will not handle it. One letter apart, and the exam asks for both.</p>",
            check="Always, exception or not.",
            ask="Now files. Which class writes, which reads, and what does the second argument true do?",
            code="""
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Records {
    public static void main(String[] args) {
        try (FileWriter out = new FileWriter("students.txt")) {
            out.write("20/1234,Ada,4.6\\n");
            out.write("20/1235,Grace,3.9\\n");
        } catch (IOException e) {
            System.out.println("could not write: " + e.getMessage());
        }

        try (FileWriter more = new FileWriter("students.txt", true)) {
            more.write("20/1236,Chinwe,4.1\\n");
        } catch (IOException e) {
            System.out.println("could not append: " + e.getMessage());
        }

        try (BufferedReader in = new BufferedReader(new FileReader("students.txt"))) {
            String line;
            int n = 0;
            while ((line = in.readLine()) != null) {
                n++;
                String[] parts = line.split(",");
                System.out.println(n + ". " + parts[1] + " has " + parts[2]);
            }
            System.out.println(n + " records");
        } catch (IOException e) {
            System.out.println("could not read: " + e.getMessage());
        }
    }
}
""",
        ),
        F(
            "<p><b>FileWriter</b> writes, <b>BufferedReader</b> wrapped around a <b>FileReader</b> reads a line at a time, and the second argument <b>true</b> means APPEND. Without it the file is emptied the moment it is opened, which is the difference between adding a record and destroying every record.</p>"
            "<p>Note the loop: <code>while ((line = in.readLine()) != null)</code> is the shape to memorise, because readLine returns null at the end of the file.</p>",
            check="FileWriter writes, BufferedReader with FileReader reads, and true appends.",
            ask="Every open above sits inside try (...) rather than before it. What is that called, and what does it save you?",
        ),
        F(
            "<p><b>try-with-resources</b>, which 24/25 asks you to define. Anything opened in those brackets is <b>closed automatically</b> when the block ends, whether it ended normally or by an exception, so no finally block and no forgotten close.</p>"
            "<p><b>PrintWriter</b> is the other writer to know: it wraps a file and gives you println and printf, so it writes formatted lines the way System.out does.</p>",
            check="try-with-resources: it closes the file for you.",
            ask="Last, the one that costs marks in a debug question: what must a method that opens a file either do or declare?",
        ),
        F(
            "<p>Either catch <b>IOException</b>, or declare <code>throws IOException</code> in its header. IOException is checked, so leaving it out is a compile error and is a favourite planted fault. Check the imports too: <code>java.io.*</code> or the four classes by name.</p>",
            check="Catch IOException or declare throws IOException.",
        ),
    ],
)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    listings = 0
    for key, topic in TOPICS.items():
        path = OUT / f"{key}.json"
        path.write_text(json.dumps(topic, indent=2, ensure_ascii=False) + chr(10), encoding="utf-8")
        listings += sum(f["teach"].count('<pre class="src"') for f in topic["methodFrames"])
        print(f"  {key}: {len(topic['methodFrames'])} method frames -> {path.name}")
    print(f"  {len(TOPICS)} topics written, {listings} listings compiled and run")


if __name__ == "__main__":
    build()
