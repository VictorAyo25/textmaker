"""Pedagogy retrofit for the INS224 manual, run 2026-08-20.

WHY. The house pedagogy was settled on 2026-08-08 and recorded as owed to the
study manuals: teaching must be KEY-POINT LED as well as worked, and a hard idea
opens on an ordinary-life anchor before any symbol.

WHAT THIS ADDS. One KEY POINT closing each of the ten teaching units, each said
twice, once formally and once bluntly. Plus four ordinary-life anchors on the
ideas this course keeps abstract: what a system actually is, why requirements are
gathered before anything is built, what a data flow diagram is a picture OF, and
the lifetime test that separates aggregation from composition.

A key point CONSOLIDATES, so it goes at the END of its unit. This book marks its
units with a .kick heading and has no sub-headings, so each insertion is anchored
on the unit's own closing </section>, located by counting sections in the file.

Idempotent, and the marker is always a literal substring of what is written.

    cd build && python gapfill_pedagogy.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

EDITS = []


def kp(fname, unit_title, marker, formal, blunt):
    """Close the unit whose <h2 class="title"> is unit_title with a key point."""
    EDITS.append((fname, unit_title, marker,
                  '<div class="box keypoint"><div class="bar"><span>Key point</span>'
                  '</div>\n<div class="body">\n'
                  f'<p class="formal">{formal}</p>\n'
                  f'<p class="blunt"><b>Blunt version:</b> {blunt}</p>\n'
                  '</div></div>\n'))


def anchor(fname, unit_title, marker, text):
    """Open the unit with an ordinary-life image, before its first box."""
    EDITS.append((fname, unit_title, marker,
                  '<div class="anchor"><span class="alab">Anchor</span>\n'
                  f'<p>{text}</p></div>\n\n', 'open'))


# ---- Module One ----------------------------------------------------------
anchor('module1.html', 'Systems Analysis and the Systems Analyst',
       'A restaurant is a system',
       'A restaurant is a system. It has parts doing different jobs, the kitchen, the '
       'waiters, the till, and none of them is the restaurant on its own. It has a '
       'boundary: the supplier who delivers the fish is outside it. It takes input, '
       'orders and ingredients, turns them into output, meals and receipts, and it '
       'has feedback, because complaints change the next service. Every one of those '
       'words is used in its technical sense in this unit.')

kp('module1.html', 'Systems Analysis and the Systems Analyst',
   'a translator who can be held responsible',
   'The analyst is not primarily a programmer. The role is to understand a business '
   'problem well enough to specify a solution, and then to hold that specification '
   'steady between people who know the business and people who can build software. '
   'Both technical and non-technical skills are required, and the paper asks for '
   'both.',
   'the analyst is a translator who can be held responsible for the translation.')

kp('module1.html', 'The System Development Life Cycle',
   'name the phase and its deliverable together',
   'Every phase of the life cycle produces a named deliverable, and the deliverable '
   'is what makes the phase examinable. A phase named without its output is half an '
   'answer: planning yields a project plan and a feasibility report, analysis yields '
   'a requirements specification, design yields the design specification.',
   'name the phase and its deliverable together, always. One without the other is '
   'half a mark.')

kp('module1.html', 'Methodologies, Feasibility and Approaches',
   'predictive plans the whole road',
   'Methodologies divide on ONE question: how much is decided up front. Predictive '
   'approaches, waterfall above all, fix the requirements first and are right when '
   'those requirements are well understood and stable. Adaptive approaches, '
   'prototyping, rapid application development, agile, expect the requirements to '
   'move and are right when they will.',
   'predictive plans the whole road before setting off. Adaptive drives and looks '
   'ahead. Choose by how well you know the destination.')

# ---- Module Two ----------------------------------------------------------
anchor('module2.html', 'Fact-Finding and Requirements',
       'Ask a friend what they want for dinner',
       'Ask a friend what they want for dinner and they say "anything". Ask whether '
       'they want rice, and suddenly there are conditions: not rice again, not too '
       'late, nothing with fish. The requirement was always there; the open question '
       'simply failed to reach it. That is the whole difficulty of fact-finding, and '
       'it is why there are seven techniques rather than one.')

kp('module2.html', 'Fact-Finding and Requirements',
   'functional is what it does',
   'A functional requirement says what the system must DO; a non-functional '
   'requirement says how well, how fast, how safely or how reliably it must do it. '
   'The distinction earns marks on its own and is tested by a single question: could '
   'you write a test that passes or fails on this sentence, and would that test be '
   'about behaviour or about quality?',
   'functional is what it does. Non-functional is how well it does it.')

kp('module2.html', 'Use Case Modelling',
   'an actor is a role',
   'A use case describes a complete interaction that delivers something of value to '
   'an actor, and an actor is a ROLE rather than a person. One human may be two '
   'actors, and one actor may be another system entirely. Getting that wrong turns a '
   'use case diagram into an organisation chart.',
   'an actor is a role, not a person, and a use case is a whole job, not a button '
   'press.')

# ---- Module Three --------------------------------------------------------
anchor('module3.html', 'Data Flow Diagrams',
       'Follow one form through an office',
       'Follow one form through an office. Somebody outside hands it in, that is an '
       'external entity. Somebody checks and stamps it, that is a process. It sits in '
       'a filing cabinet until it is needed, that is a data store. And it travels '
       'between all of these in somebody\'s hand, which is a data flow. Four things, '
       'and every data flow diagram you will ever draw is made of exactly those four.')

kp('module3.html', 'Data Flow Diagrams',
   'a process must earn its outputs',
   'A data flow diagram shows how data MOVES and is transformed, never when things '
   'happen or in what order. It has no decisions, no loops and no timing. Two rules '
   'then follow that the examiner checks first: every process must have at least one '
   'input and at least one output, and a child diagram must balance with the parent '
   'process it explodes.',
   'a process must earn its outputs from its inputs. No inputs is a miracle, no '
   'outputs is a black hole, and not enough inputs is a grey hole.')

# ---- Module Four ---------------------------------------------------------
kp('module4.html', 'The Entity-Relationship Model',
   'read the far end',
   'The marks at the end of a relationship line describe the entity at the OTHER '
   'end, and each end carries two of them: the inner mark gives the maximum and the '
   'outer mark gives the minimum. A crow\'s foot is many, a bar is one, a circle is '
   'zero. Read every line out loud in both directions before you commit to it.',
   'read the far end, and say the sentence both ways round. Most lost ERD marks are '
   'a correct diagram read backwards.')

# ---- Module Five ---------------------------------------------------------
kp('module5.html', 'UML and Class Diagrams',
   'the class box is name, has, does',
   'A class box has three compartments in a fixed order: the name, then the '
   'attributes, then the operations. The lines between boxes carry the meaning, and '
   'their multiplicities sit at the end NEAR the class they describe, so a class '
   'diagram is read the same way an entity-relationship diagram is: across the line, '
   'in both directions.',
   'the class box is name, has, does. Never in another order.')

anchor('module5.html', 'Object-Oriented Design Concepts',
       'A car and its wheels',
       'A car and its wheels: take the wheels off and both the car and the wheels '
       'still exist, so that is a hollow diamond. A house and its rooms: demolish the '
       'house and the rooms are gone with it, so that is a filled diamond. The two '
       'symbols differ by whether the middle is coloured in, and they mean opposite '
       'things about what survives what.')

kp('module5.html', 'Object-Oriented Design Concepts',
   'the test is what survives',
   'Aggregation and composition are both whole to part, and they differ on LIFETIME '
   'alone. If the part can outlive the whole it is aggregation, drawn with a hollow '
   'diamond; if the part dies with the whole it is composition, drawn with a filled '
   'one. Ownership, importance and containment are not the test.',
   'the test is what survives, not what owns. Hollow means the part lives on.')

kp('module5.html', 'Activity and Sequence Diagrams',
   'activity answers what happens next',
   'The two behavioural diagrams answer different questions. An activity diagram '
   'shows the FLOW of a process: what happens next, where it branches, what runs in '
   'parallel, and who does it if there are swimlanes. A sequence diagram shows an '
   'INTERACTION over time: which participant sends which message to which other, in '
   'what order, with time running down the page.',
   'activity answers what happens next. Sequence answers who says what to whom, and '
   'when.')


def apply_one(fname, unit_title, marker, payload, where='close'):
    path = os.path.join(CONTENT, fname)
    with open(path, encoding='utf-8') as fh:
        s = fh.read()
    if marker not in payload:
        return f'FAIL {fname}: marker "{marker[:30]}" is not in what would be written'
    if marker in s:
        return f'{fname}: already carries "{marker[:34]}", skipped'
    m = re.search(r'<h2 class="title">\s*' + re.escape(unit_title) + r'\s*</h2>', s)
    if not m:
        return f'FAIL {fname}: no unit titled "{unit_title}"'
    if where == 'open':
        # first block-level box after the unit's lead paragraphs
        at = s.find('<div class="box', m.end())
        if at < 0:
            return f'FAIL {fname}: no box after "{unit_title}"'
    else:
        at = s.find('</section>', m.end())
        if at < 0:
            return f'FAIL {fname}: no </section> after "{unit_title}"'
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s[:at] + payload + s[at:])
    return f'{fname}: {"opened" if where == "open" else "closed"} '\
           f'"{unit_title[:34]}" with "{marker[:30]}"'


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
