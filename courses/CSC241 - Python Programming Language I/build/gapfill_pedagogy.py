"""Pedagogy retrofit for the CSC241 manual, run 2026-08-20.

WHY. The house pedagogy was settled on 2026-08-08 and recorded as owed to the
study manuals: teaching must be KEY-POINT LED as well as worked, and a hard idea
opens on an ordinary-life anchor before any symbol. Key points fix recall, the
worked steps fix understanding, and a lesson with only one of the two is either a
formula sheet or a wall.

WHAT THIS ADDS. Twelve KEY POINT boxes closing the teaching across the five
modules, each said twice, once formally and once bluntly, because the blunt
version is what survives the examination hall. Plus four ordinary-life anchors
where the book opened straight onto the abstraction: a recipe for what a program
is, a labelled box for a variable, a hotel guest register for a dictionary, and a
filing cabinet for a database.

A key point CONSOLIDATES, so it is placed after the teaching it summarises, never
before it as a preview.

Idempotent: an insertion whose marker text is already present is skipped, and the
marker is always a literal substring of what is written.

    cd build && python gapfill_pedagogy.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

EDITS = []
H3 = '<h3 class="sub">%s</h3>'


def kp(fname, marker, anchor, formal, blunt, where='before'):
    EDITS.append((fname, marker, anchor, where,
                  '<div class="box keypoint"><div class="bar"><span>Key point</span>'
                  '</div>\n<div class="body">\n'
                  f'<p class="formal">{formal}</p>\n'
                  f'<p class="blunt"><b>Blunt version:</b> {blunt}</p>\n'
                  '</div></div>\n\n'))


def anchor_box(fname, marker, at, text, where='before'):
    EDITS.append((fname, marker, at, where,
                  '<div class="anchor"><span class="alab">Anchor</span>\n'
                  f'<p>{text}</p></div>\n\n'))


# -- Module One -------------------------------------------------------------
anchor_box('module1.html', 'A recipe written down', H3 % 'Why we need a language',
           'A recipe written down is a program. It lists ingredients, which are the '
           'data, and steps in an order that matters, which are the instructions. '
           'Anyone who follows it exactly gets the same cake, and that is the whole '
           'idea: the cook does no thinking, and every decision was made by whoever '
           'wrote the recipe. A computer is a cook that follows a recipe perfectly '
           'and understands nothing.')

kp('module1.html', 'it runs until it hits the mistake', H3 % 'Why Python',
   'A compiler translates the whole program before any of it runs, so it finds '
   'faults up front. An interpreter translates and runs one statement at a time, '
   'so a fault on line 40 is only found when line 40 runs, and lines 1 to 39 have '
   'already had their effect.',
   'a compiler reads the whole recipe first. An interpreter starts cooking, and it '
   'runs until it hits the mistake.')

kp('module1.html', 'the prompt talks back', H3 % 'The two ways to run Python',
   'The interactive prompt evaluates what you type and DISPLAYS the result, which '
   'is why 2 + 3 shows 5 there. A script does not: an expression on its own line '
   'is computed and thrown away, so a script must call print() to show anything.',
   'the prompt talks back, a script does not. If your file prints nothing, that is '
   'usually why.')

# -- Module Two -------------------------------------------------------------
anchor_box('module2.html', 'a label on a box in a storeroom', H3 % 'Variables',
           'A variable is a label on a box in a storeroom. Writing total = 5 puts a '
           'value in a box and hangs the label "total" on it. Hanging the same label '
           'on a different box later is allowed, and the old box is simply forgotten. '
           'What the label can never do is change the thing inside the box while '
           'still pointing at it: that is a different idea, and it is what mutability '
           'means.')

kp('module2.html', 'the value carries the type', H3 % 'Input',
   'Python is dynamically typed: the type belongs to the VALUE, not to the name. No '
   'declaration is needed, and rebinding a name to a value of another type is '
   'legal, which is why type() reports on what a name currently holds rather than '
   'on what it was first given.',
   'the value carries the type. The name is only a sticker.')

kp('module2.html', 'wrap it in int', H3 % 'Floats are not exact',
   'input() returns a string every time, whatever the user typed. Any arithmetic on '
   'it must convert first, with int() for a whole number or float() for a decimal, '
   'or the plus operator will join text instead of adding numbers.',
   'wrap it in int() or float() the moment you read it. Every program on this paper '
   'needs that line.')

kp('module2.html', 'one slash, one point', H3 % 'Comparison operators',
   'A single slash is true division and always produces a float, even when the '
   'division is exact: 6 / 2 is 3.0, not 3. Double slash floors to an integer, and '
   'flooring goes DOWN, so -7 // 2 is -4 rather than -3.',
   'one slash, one point. Two slashes, no point, and it rounds down even for '
   'negatives.')

kp('module2_unit4.html', 'a new string comes back', H3 % 'The methods',
   'Strings are immutable: no string method changes the string it was called on. '
   'Each one returns a NEW string, so s.upper() on its own line accomplishes '
   'nothing at all unless the result is assigned or used.',
   'a new string comes back and the old one is untouched. If you did not catch the '
   'result, nothing happened.')

# -- Module Three -----------------------------------------------------------
kp('module3.html', 'elif is a queue', H3 % 'while',
   'In an if / elif / else chain, the first test that is true runs its block and '
   'the whole chain is then finished. Replacing an elif with a second if changes '
   'that: independent ifs are all tested, so two blocks can run.',
   'elif is a queue, one gets served. Separate ifs are a crowd, they all get in.')

kp('module3.html', 'up to, never including', H3 % 'Tuples',
   'A slice and a range both EXCLUDE their stop. xs[1:4] gives the items at 1, 2 '
   'and 3, and range(1, 4) gives 1, 2 and 3. A negative index counts back from the '
   'end, and [::-1] walks the whole thing backwards.',
   'up to, never including. Every off-by-one on this paper is that sentence not '
   'yet learned.')

kp('module3.html', 'one object, two labels', H3 % 'Dictionaries',
   'Assignment binds a name; it never copies. After b = a there is ONE list with '
   'two names, so a change made through either name is visible through the other. '
   'To get a genuine copy, use list(a), a[:] or a.copy().',
   'one object, two labels. If you did not ask for a copy, you did not get one.')

anchor_box('module3.html', 'A hotel guest register', H3 % 'Dictionaries',
           'A hotel guest register is a dictionary. You look a guest up by room '
           'number, not by walking the corridor. The room number is the key, the '
           'guest is the value, one room holds one guest at a time, and asking for a '
           'room the hotel does not have is an error rather than an empty answer. '
           'That last part is exactly what a KeyError is.')

# -- Module Four ------------------------------------------------------------
kp('module4.html', 'show it or give it back', H3 % 'Default parameters',
   'print() DISPLAYS a value and returns None. return HANDS A VALUE BACK to '
   'whoever called the function and displays nothing. A function that only prints '
   'returns None, so assigning its result stores None.',
   'show it or give it back. Those are two different jobs and mixing them is the '
   'commonest function bug on this paper.')

kp('module4.html', 'what happens in the function', H3 % 'The three steps',
   'Assigning to a name inside a function creates a LOCAL name, which disappears '
   'when the function ends and leaves any global of the same name untouched. '
   'Changing a global from inside requires the global keyword.',
   'what happens in the function stays in the function, unless you say global.')

kp('module4.html', 'w wipes', H3 % 'Reading',
   'The file mode decides what happens to what is already there. "r" reads, "w" '
   'creates or TRUNCATES, so an existing file is emptied the moment it is opened, '
   'and "a" appends. with open(...) guarantees the file is closed on the way out, '
   'even if the block raises.',
   'w wipes. If you meant to add to the file, the mode is "a".')

# -- Module Five ------------------------------------------------------------
anchor_box('module5.html', 'a filing cabinet with an index', H3 % 'What a database is',
           'A text file of records is a shoebox of receipts: everything is in there, '
           'and finding one means going through them all. A database is a filing '
           'cabinet with an index, where you ask for what you want and the cabinet '
           'finds it. That difference, asking rather than searching, is what SQL is '
           'for, and it is why a database is worth the extra setup.')

kp('module5.html', 'no commit, no data', H3 % 'Reading rows back',
   'Changes made through a cursor live in a transaction and are not permanent until '
   'commit() is called. Closing the connection without committing rolls them back, '
   'and nothing is reported: the program appears to have worked.',
   'no commit, no data, and no error message to tell you.')

kp('module5.html', 'WHERE or everywhere', H3 % 'Filtering, changing and summarising',
   'UPDATE and DELETE apply to every row that matches the WHERE clause, and a '
   'statement with no WHERE clause matches every row in the table. The clause is '
   'optional to SQL and not optional to you.',
   'WHERE or everywhere. Write the WHERE before you write the SET.')


def apply_one(fname, marker, anchor, where, payload):
    path = os.path.join(CONTENT, fname)
    with open(path, encoding='utf-8') as fh:
        s = fh.read()
    if marker not in payload:
        return f'FAIL {fname}: marker "{marker[:30]}" is not in what would be written'
    if marker in s:
        return f'{fname}: already carries "{marker[:34]}", skipped'
    n = s.count(anchor)
    if n != 1:
        return f'FAIL {fname}: anchor found {n} times, expected 1 ({anchor[:48]})'
    i = s.index(anchor)
    at = i if where == 'before' else i + len(anchor)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s[:at] + payload + s[at:])
    return f'{fname}: inserted "{marker[:34]}"'


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
