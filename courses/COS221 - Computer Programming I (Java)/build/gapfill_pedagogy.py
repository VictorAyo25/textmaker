"""Pedagogy retrofit for the COS221 manual, run 2026-08-20.

WHY. The house pedagogy was settled on 2026-08-08 and recorded as owed to the
study manuals: teaching must be KEY-POINT LED as well as worked, and a hard idea
opens on an ordinary-life anchor before any symbol. Key points fix recall, the
worked steps fix understanding, and a lesson with only one of the two is either a
formula sheet or a wall.

WHAT THIS ADDS. Eleven KEY POINT boxes, one closing each module and one closing
the Foundations, each said twice, once formally and once bluntly, because the
blunt version is what survives the examination hall. Plus four ordinary-life
anchors on the ideas this course keeps abstract: what a variable actually is, what
pass by value means, what a reference is, and what an exception is for.

A key point CONSOLIDATES, so it closes the part it summarises rather than
previewing it. Each is placed at the end of the file's last section, which in this
book is the end of that module.

Idempotent, and the marker is always a literal substring of what is written.

    cd build && python gapfill_pedagogy.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

EDITS = []


def kp(fname, marker, formal, blunt, after_kick=None):
    EDITS.append((fname, marker, after_kick,
                  '\n<div class="box keypoint"><div class="bar"><span>KEY POINT</span>'
                  '</div>\n<div class="body">\n'
                  f'<p class="formal">{formal}</p>\n'
                  f'<p class="blunt"><b>Blunt version:</b> {blunt}</p>\n'
                  '</div></div>\n'))


def anchor(fname, marker, after_kick, text):
    EDITS.append((fname, marker, after_kick,
                  '\n<div class="anchor"><span class="alab">Anchor</span>\n'
                  f'<p>{text}</p></div>\n', 'open'))


# ---- Foundations ---------------------------------------------------------
anchor('foundations.html', 'A pigeonhole with a label on it', 'F.8 · VARIABLES',
       'A pigeonhole with a label on it. That is a variable. The label is the name, '
       'the hole is a fixed size decided when you declare it, and whatever is in the '
       'hole is the value. Two things follow that catch people out. The size is fixed, '
       'so an int hole cannot hold a number too big for it and the number wraps round '
       'instead. And the label can be moved to a different hole, which is what an '
       'assignment does: it never changes the value that was in the old one.')

kp('foundations.html', 'the compiler is the pedant',
   'Java is compiled before it runs, so a whole class of mistake is caught before the '
   'program starts: a misspelled name, a missing semicolon, an int given to a String. '
   'Everything the compiler accepts may still be wrong, and those faults appear only '
   'when the line runs.',
   'the compiler is the pedant who checks your spelling. It cannot tell you the essay '
   'is wrong.')

# ---- Module One ----------------------------------------------------------
kp('module1.html', 'the biscuit cutter, the object is the biscuit',
   'A class is a definition and an object is an instance built from it. The class says '
   'what fields and methods every instance will have; each object made with new gets '
   'its own copy of the fields and shares the methods.',
   'the class is the biscuit cutter, the object is the biscuit. new is the press.')

# ---- Module Two ----------------------------------------------------------
kp('module2.html', 'javac makes it portable, java makes it run',
   'javac turns source into bytecode and the JVM executes that bytecode. The bytecode '
   'is the same file everywhere; only the JVM differs from machine to machine, which '
   'is what write once run anywhere actually means.',
   'javac makes it portable, java makes it run. The JVM is the part that changes '
   'between computers so your file does not have to.')

# ---- Module Three --------------------------------------------------------
kp('module3.html', 'int over int stays int',
   'The TYPES of the operands decide what an operator does, not the values. Two ints '
   'divide as ints and throw the fraction away; one double promotes the whole '
   'expression; and once a String is involved, plus stops adding and starts joining.',
   'int over int stays int, and plus next to a String glues rather than adds. Look at '
   'the types before you look at the numbers.')

# ---- Module Four ---------------------------------------------------------
kp('module4.html', 'a switch falls through and an else clings',
   'Two control structures behave in a way the layout does not show. A switch enters '
   'at its matching label and runs ON until a break, and an else attaches to the '
   'nearest unmatched if however the code is indented. Braces on every block and a '
   'break on every case remove both.',
   'a switch falls through and an else clings to the nearest if. Indentation is a '
   'comment, not an instruction.')

# ---- Module Five ---------------------------------------------------------
anchor('module5.html', 'a photocopy of a form', 'UNIT 5.4 · PARAMETER PASSING · READ THIS TWICE',
       'You hand somebody a photocopy of a form. They can scribble all over their copy '
       'and your original is untouched: that is passing an int. Now the form is a '
       'library card with a shelf number on it. You photocopy the CARD, so they still '
       'cannot change your card, but they can walk to that shelf and move the book. '
       'That is passing an object. In both cases what travels is a copy; what differs '
       'is whether the copy points at something shared.')

kp('module5.html', 'the copy cannot reach your variable',
   'Java passes arguments BY VALUE without exception. For a primitive the value copied '
   'is the number, so a method cannot change the caller\'s variable at all. For an '
   'object the value copied is the REFERENCE, so the method can change the object it '
   'points at, but assigning a new object to the parameter still cannot reach the '
   'caller.',
   'the copy cannot reach your variable, but it can reach your object.')

# ---- Module Six ----------------------------------------------------------
kp('module6.html', 'the variable decides what you may call',
   'The DECLARED type of a variable decides which methods you are allowed to call on '
   'it. The ACTUAL type of the object decides which version of an overridden method '
   'runs. Those are two different questions answered at two different times, compile '
   'time and run time, and polymorphism is the gap between them.',
   'the variable decides what you may call; the object decides what actually happens.')

# ---- Module Seven --------------------------------------------------------
kp('module7.html', 'equals reads the letters',
   'A String is an object, so == compares REFERENCES and equals compares CHARACTERS. '
   'Identical literals are pooled and share one object, which makes == look correct '
   'until a string arrives from input or from new, at which point it silently starts '
   'answering false.',
   'equals reads the letters, == compares the addresses. For text, always equals.')

# ---- Module Eight --------------------------------------------------------
kp('module8.html', 'the last index is always length minus one',
   'An array has a fixed length fixed at creation, indexes running from 0 to length '
   'minus 1, and elements pre-filled with the zero of their type. Every array error on '
   'this paper is one of those three facts not yet held: a length that cannot grow, a '
   'last index one less than the length, or a default assumed to be something else.',
   'the last index is always length minus one. Write a.length - 1 rather than counting '
   'in your head.')

# ---- Module Nine ---------------------------------------------------------
kp('module9.html', 'a base case and a step towards it',
   'A recursive method needs two things and fails without either: a base case that '
   'returns without recursing, and a recursive step whose argument moves towards that '
   'base case. Missing the first, or a step that does not converge, gives '
   'StackOverflowError rather than a wrong answer.',
   'a base case and a step towards it. Check for both before you trace a single '
   'call.')

# ---- Module Ten ----------------------------------------------------------
anchor('module10.html', 'A smoke alarm', 'UNIT 10.1 · EXCEPTIONS',
       'A smoke alarm does not stop a fire; it stops the fire being discovered too '
       'late. An exception is the same idea in a program: something has gone wrong '
       'where it was noticed, and the notice is passed up to whoever is in a position '
       'to do something about it. A method that reads a file cannot decide what to do '
       'about a missing file; the code that asked for it can.')

kp('module10.html', 'catch the specific one first',
   'Catch clauses are tried in order, so the most specific exception must come first '
   'and the general one last; the reverse is a compile error, not a subtle bug. '
   'finally runs on every path out of the try, including a return, which is why '
   'cleanup belongs there and nowhere else.',
   'catch the specific one first, and put the cleanup in finally.')


def apply_one(fname, marker, after_kick, payload, where='close'):
    path = os.path.join(CONTENT, fname)
    with open(path, encoding='utf-8') as fh:
        s = fh.read()
    if marker not in payload:
        return f'FAIL {fname}: marker "{marker[:30]}" is not in what would be written'
    if marker in s:
        return f'{fname}: already carries "{marker[:34]}", skipped'
    if where == 'open':
        m = re.search(r'<div class="kick">' + re.escape(after_kick) + r'</div>', s)
        if not m:
            return f'FAIL {fname}: no section kicked "{after_kick}"'
        at = s.find('<div class="box', m.end())
        if at < 0:
            return f'FAIL {fname}: no box after "{after_kick}"'
    else:
        at = s.rstrip().rindex('</section>')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s[:at] + payload + s[at:])
    return f'{fname}: {"opened" if where == "open" else "closed"} with '\
           f'"{marker[:34]}"'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    fails = []
    for e in EDITS:
        msg = apply_one(*e)
        print('  ' + msg)
        if msg.startswith('FAIL'):
            fails.append(msg)
    print(f'gapfill_pedagogy: {len(EDITS)} insertions attempted, {len(fails)} failed')
    if fails:
        sys.exit(1)


if __name__ == '__main__':
    main()
