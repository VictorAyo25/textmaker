"""Authored objective questions for the topics the class tests never reached.

WHY. Both class tests together cover the analyst, the life cycle, methodology,
fact-finding, use cases and data flow diagrams, and exactly one question beyond
that. They stop where the course had got to when they were set. But the paper
does not stop there: entity-relationship diagrams complete compulsory Question
Two, object orientation and UML ARE compulsory Question Three, and Module Six can
still be asked in the objective half.

So the captured tests are thin exactly where the written half is heaviest. These
questions fill that gap, in the FORM the lecturer named for the examination, which
is multi-select: which TWO of the options are correct.

THEY ARE OURS AND THEY SAY SO. Every one carries an AUTHORED chip rather than a
test number, so no reader can mistake them for the examiner's. They are grounded
in what this manual teaches, unit by unit, and in the distinctions the course text
draws.

Merged into the section by gen_objective.py, which checks them against the same
rules as the transcribed questions: four options, every option explained, exactly
two answers on a which-two, and no dashes.
"""

E = []


def q(qid, module, topic, prompt, options, answer, explanation, why, style=None):
    ids = 'abcd'
    E.append({
        'id': qid,
        'module': module,
        'slides': ['Authored'],
        'style': style or ('multi' if isinstance(answer, list) else 'mcq'),
        'difficulty': 'medium',
        'facets': ['names'],
        'topic': topic,
        'prompt': prompt,
        'options': [{'id': ids[i], 'text': t} for i, t in enumerate(options)],
        'answer': answer,
        'explanation': explanation,
        'why': {ids[i]: w for i, w in enumerate(why)},
    })


# ===========================================================================
# MODULE FOUR: the entity-relationship model  (drill topic 7)
# ===========================================================================
q('ins-x-01', 7, 'entities and attributes',
  'A university system stores, for each student, a matriculation number, a name '
  'and a date of birth. Which TWO statements are correct?',
  ['Student is an entity and matriculation number is one of its attributes',
   'Student, matriculation number, name and date of birth are four separate entities',
   'The matriculation number is a candidate identifier, because it is unique to one student',
   'Date of birth is the natural primary key, because everyone has one'],
  ['a', 'c'],
  'An entity is the THING the business keeps data about; its attributes are the '
  'pieces of data kept. An identifier is the attribute that picks out exactly one '
  'instance, which is why uniqueness, not universality, is the test.',
  ['Correct. Student is the thing; matriculation number, name and date of birth are '
   'facts about it.',
   'Wrong. Attributes are not entities. Making each attribute an entity gives a '
   'diagram with no structure and no relationships worth drawing.',
   'Correct. It is unique to one student, which is exactly what a candidate '
   'identifier means.',
   'Wrong. Everyone having one is not enough: many students share a date of birth, '
   'so it cannot identify a single instance.'])

q('ins-x-02', 7, 'the three cardinalities',
  'In a library, one member may borrow many books over time, and one book may be '
  'borrowed by many members over time. Which TWO statements are correct?',
  ['The relationship between Member and Book is many to many',
   'The relationship between Member and Book is one to many',
   'A many-to-many relationship should be resolved into an associative entity such '
   'as Loan',
   'A many-to-many relationship is drawn with a single bar at each end'],
  ['a', 'c'],
  'Many to many is read in BOTH directions, and it is the one cardinality that '
  'cannot be implemented directly. It is resolved by an associative entity, which '
  'is where the attributes of the relationship itself, such as the date borrowed, '
  'finally have somewhere to live.',
  ['Correct. Many in each direction is the definition of many to many.',
   'Wrong. One to many would mean a book could only ever be borrowed by one member, '
   'which the description contradicts.',
   'Correct. Loan holds the two foreign keys plus the borrow date and due date, '
   'which have no home on either original entity.',
   'Wrong. A single bar means exactly one. Many is the crow\'s foot.'])

q('ins-x-03', 7, 'crow\'s foot notation',
  'On a crow\'s foot diagram, a line from Department to Employee ends at Employee '
  'with a crow\'s foot and a circle. What does that end mean?',
  ['Exactly one employee', 'Zero or many employees', 'One or many employees',
   'Zero or one employee'],
  'b',
  'Read the end symbols as two marks: the INNER one nearest the entity gives the '
  'maximum, and the OUTER one gives the minimum. A crow\'s foot is many, a bar is '
  'one, and a circle is zero.',
  ['Wrong. Exactly one is two bars, not a foot and a circle.',
   'Correct. The foot gives many as the maximum and the circle gives zero as the '
   'minimum, so a department may have no employees at all.',
   'Wrong. One or many would be a crow\'s foot with a BAR, not a circle. The circle '
   'is what makes it optional.',
   'Wrong. Zero or one is a circle with a bar. There is no crow\'s foot in it.'])

q('ins-x-04', 7, 'Chen against crow\'s foot',
  'The course text draws entity-relationship diagrams in Chen notation while the '
  'examination asks for the crow\'s foot style. Which TWO statements are correct?',
  ['In Chen notation a relationship is drawn as a diamond on the line',
   'In Chen notation attributes are drawn as ovals attached to the entity',
   'Crow\'s foot notation writes cardinality as the numbers 1, M and N beside the line',
   'Crow\'s foot notation cannot express an optional relationship'],
  ['a', 'b'],
  'The two styles say the same thing differently. Chen spends space: a diamond for '
  'each relationship and an oval for each attribute. Crow\'s foot is compact: '
  'attributes go inside the entity box and the cardinality is carried by the marks '
  'on the line ends.',
  ['Correct. The diamond holds the relationship name, with the two entities either '
   'side of it.',
   'Correct. Each attribute gets its own oval joined to the entity rectangle, which '
   'is why a Chen diagram of a real system covers a wall.',
   'Wrong. Writing 1, M and N beside the line is the CHEN convention. Crow\'s foot '
   'uses the bar, the circle and the foot.',
   'Wrong. Optionality is exactly what the circle expresses, and expressing it is '
   'one of the reasons the style is preferred.'])

q('ins-x-05', 7, 'primary and foreign keys',
  'Which TWO statements about keys are correct?',
  ['A primary key uniquely identifies one instance of an entity',
   'A foreign key is an attribute that holds the primary key of a related entity',
   'A foreign key must be unique within its own table',
   'An entity may have several primary keys at once'],
  ['a', 'b'],
  'The primary key identifies; the foreign key refers. That pair is how a set of '
  'separate entities becomes a connected model, and it is what a relationship line '
  'actually becomes when the design is built.',
  ['Correct. Unique identification of a single instance is the whole job of a '
   'primary key.',
   'Correct. The foreign key is the copy of the other entity\'s identifier, and it '
   'is where the relationship physically lives.',
   'Wrong, and it is the common confusion. A foreign key repeats freely: many '
   'employees carry the same department number, which is what many to one MEANS.',
   'Wrong. There may be several CANDIDATE keys, but exactly one of them is chosen '
   'as the primary key.'])

q('ins-x-06', 7, 'reading a diagram',
  'A diagram shows Customer connected to Order with a bar and circle at the '
  'Customer end and a crow\'s foot and bar at the Order end. Which TWO readings are '
  'correct?',
  ['Each order belongs to exactly one customer',
   'Each customer has at least one order',
   'A customer may exist with no orders',
   'An order may exist with no customer'],
  ['b', 'c'],
  'Read each end for the entity at the OTHER end. This is the single most common '
  'reading error on the paper, and the cure is to say the sentence out loud in both '
  'directions before writing anything.',
  ['Wrong as a reading of the marks given. The Customer end carries a bar and a '
   'circle, which is zero or one, not exactly one.',
   'Correct. The Order end has a foot and a bar, which is one or many, so at least '
   'one order per customer.',
   'Correct as the other half of the same pair: the circle at the Customer end makes '
   'the customer optional to an order.',
   'Wrong. Optionality on the Customer end says a customer need not be attached, not '
   'that an order floats free of the relationship entirely.'])


# ===========================================================================
# MODULE FIVE: object orientation and UML  (drill topics 8, 9, 10)
# ===========================================================================
q('ins-x-07', 8, 'class against object',
  'Which TWO statements correctly distinguish a class from an object?',
  ['A class is a blueprint describing structure and behaviour',
   'An object is an instance of a class, with actual values for its attributes',
   'A class holds the values and an object holds the definitions',
   'There can be only one object of any given class'],
  ['a', 'b'],
  'The class is the definition and the object is one filled-in copy of it. The '
  'Contacts app is the standard image: one idea of what a contact is, and hundreds '
  'of saved contacts that are instances of it.',
  ['Correct. It defines what every instance will have and be able to do.',
   'Correct. Instantiating the class produces an object with real values in its '
   'attributes.',
   'Wrong, and it is exactly backwards. The definitions are in the class; the values '
   'are in the object.',
   'Wrong. A class exists precisely so that many objects can be made from it.'])

q('ins-x-08', 8, 'the four object-oriented concepts',
  'Which TWO statements about encapsulation are correct?',
  ['It hides an object\'s internal data and exposes it only through its methods',
   'It means one class inherits the attributes of another',
   'It protects an object from being changed in ways its own methods do not allow',
   'It allows the same method name to behave differently in different classes'],
  ['a', 'c'],
  'Encapsulation is data hiding plus controlled access. The two halves go together: '
  'hiding the data is pointless without a defined way in, and a defined way in is '
  'what lets the object keep itself valid.',
  ['Correct. Attributes are private, methods are the public door.',
   'Wrong. That is inheritance, a different concept entirely.',
   'Correct. Because every change goes through a method, the object can refuse an '
   'invalid one.',
   'Wrong. That is polymorphism.'])

q('ins-x-09', 8, 'inheritance and polymorphism',
  'Which TWO statements are correct?',
  ['Inheritance lets a subclass reuse the attributes and methods of a superclass',
   'Polymorphism lets the same message produce different behaviour in different '
   'classes',
   'Inheritance is drawn as a filled diamond on the superclass end',
   'Polymorphism removes the need for classes to define their own methods'],
  ['a', 'b'],
  'Inheritance is about REUSE and is a relationship between classes. Polymorphism '
  'is about BEHAVIOUR and is what makes that reuse worth having: the caller sends '
  'one message and each subclass answers it in its own way.',
  ['Correct. The subclass gets everything the superclass has and adds or overrides '
   'what it needs.',
   'Correct. Draw() sent to Circle and to Square produces two different drawings '
   'from one call.',
   'Wrong. Inheritance, or generalisation, is a hollow TRIANGLE pointing at the '
   'superclass. A filled diamond is composition.',
   'Wrong. Polymorphism depends on each class defining its own version. Without '
   'those definitions there is nothing to vary.'])

q('ins-x-10', 9, 'the class box',
  'A UML class is drawn as a rectangle split into three compartments. What do they '
  'hold, from top to bottom?',
  ['Name, attributes, operations', 'Name, operations, attributes',
   'Attributes, name, operations', 'Name, attributes, relationships'],
  'a',
  'Name, then data, then behaviour. It is worth writing in that order every time, '
  'because an examiner scanning a page of class boxes reads the top line first and '
  'a box with no name is a box with no marks.',
  ['Correct. The class name on top, its attributes in the middle, its operations or '
   'methods at the bottom.',
   'Wrong. Data comes before behaviour: what the thing HAS, then what it DOES.',
   'Wrong. The name is always the top compartment.',
   'Wrong. Relationships are drawn as lines BETWEEN boxes, never inside one.'])

q('ins-x-11', 9, 'aggregation against composition',
  'A Department has Lecturers; if the department closes, the lecturers remain. A '
  'House has Rooms; if the house is demolished, the rooms cease to exist. Which TWO '
  'statements are correct?',
  ['Department to Lecturer is aggregation, drawn with a hollow diamond',
   'House to Room is composition, drawn with a filled diamond',
   'Department to Lecturer is composition, because a lecturer belongs to a department',
   'Both are drawn with a hollow triangle, because both are whole to part'],
  ['a', 'b'],
  'The test is LIFETIME, not ownership. If the part survives the whole it is '
  'aggregation and the diamond is hollow; if the part dies with the whole it is '
  'composition and the diamond is filled. The two symbols look almost identical and '
  'mean opposite things, which is exactly why the paper asks.',
  ['Correct. The lecturer outlives the department, so the whole-to-part link is the '
   'weaker one.',
   'Correct. A room cannot exist without its house, so the diamond is filled.',
   'Wrong. Belonging is not the test. A lecturer belongs to a department and still '
   'survives it.',
   'Wrong. A hollow triangle is generalisation, that is inheritance, which is a '
   'different relationship altogether.'])

q('ins-x-12', 9, 'include against extend',
  'In a use case diagram, which TWO statements are correct?',
  ['An include relationship means the included use case ALWAYS runs as part of the '
   'base use case',
   'An extend relationship means the extending use case runs only under a stated '
   'condition',
   'An include relationship means the included use case is optional',
   'The arrow of an include points from the included use case to the base use case'],
  ['a', 'b'],
  'Include is compulsory and factors out shared behaviour; extend is conditional '
  'and adds behaviour in special cases. Both arrows are dashed with an open head, '
  'and the direction is what separates them: include points AT what is included, '
  'extend points AT what is being extended.',
  ['Correct. Verify PIN is included by Withdraw Cash because it happens every time.',
   'Correct. Print Receipt extends Withdraw Cash because it happens only if the '
   'customer asks.',
   'Wrong. Optional is extend. Include is always.',
   'Wrong. The include arrow points FROM the base use case TO the included one.'])

q('ins-x-13', 10, 'activity diagram elements',
  'Which TWO statements about an activity diagram are correct?',
  ['A diamond represents a decision, with a guard condition on each outgoing branch',
   'A thick bar represents a fork into, or a join of, parallel flows',
   'A diamond represents an action carried out by the system',
   'A swimlane shows the order in which actions occur'],
  ['a', 'b'],
  'The diamond BRANCHES, the bar PARALLELISES, and the rounded rectangle acts. A '
  'swimlane answers a different question: not when, but WHO.',
  ['Correct. The guards must be mutually exclusive and cover every case, or the flow '
   'can stall or split.',
   'Correct. One bar in and several out is a fork; several in and one out is a join.',
   'Wrong. An action is a rounded rectangle. A diamond never does work.',
   'Wrong. A swimlane shows WHO or WHAT performs each action. Order is carried by '
   'the arrows.'])

q('ins-x-14', 10, 'sequence diagram elements',
  'Which TWO statements about a sequence diagram are correct?',
  ['Time runs down the page, so the vertical order of messages is their order in time',
   'A vertical dashed line under an object is its lifeline',
   'Time runs left to right across the page',
   'A sequence diagram shows the static structure of the classes involved'],
  ['a', 'b'],
  'A sequence diagram is a BEHAVIOURAL diagram: participants across the top, time '
  'down the side, messages as horizontal arrows between lifelines. Structure is what '
  'a class diagram is for.',
  ['Correct, and it is the one rule that makes the diagram readable. Read it top to '
   'bottom like a script.',
   'Correct. The lifeline is the object\'s existence over time, with an activation '
   'bar drawn on it while it is actually doing something.',
   'Wrong. The participants are arranged left to right; TIME is the vertical axis.',
   'Wrong. Static structure is the class diagram. A sequence diagram shows one '
   'scenario unfolding.'])

q('ins-x-15', 9, 'multiplicity on an association',
  'A class diagram shows Order 1 ..... 1..* OrderLine. What does it say?',
  ['One order has one or more order lines, and each order line belongs to exactly '
   'one order',
   'One order has exactly one order line',
   'One order may have no order lines',
   'Many orders share the same order line'],
  'a',
  'Multiplicity is written at the END NEAR the class it describes, so read across '
  'the line to find which number applies to which class. 1..* is one or more, 0..* '
  'is zero or more, and a bare 1 is exactly one.',
  ['Correct. 1..* at the OrderLine end is one or more lines; 1 at the Order end is '
   'exactly one order.',
   'Wrong. The star means many. Exactly one would be written 1.',
   'Wrong. Zero would need 0..*, and the lower bound here is 1.',
   'Wrong. The 1 at the Order end forbids that: a line belongs to one order only.'])


# ===========================================================================
# MODULE SIX: design, architecture and delivery  (objective section only)
# ===========================================================================
q('ins-x-16', 11, 'installation strategies',
  'Which TWO statements about system installation strategies are correct?',
  ['Direct cutover switches off the old system and starts the new one at once, which '
   'is cheapest and riskiest',
   'Parallel running operates both systems together for a period and compares their '
   'output',
   'Phased installation means installing the whole system at one site before the '
   'others',
   'Parallel running is the cheapest strategy because only one system is paid for'],
  ['a', 'b'],
  'The four strategies trade cost against risk. Direct is cheap and dangerous, '
  'parallel is expensive and safe, phased brings the system in a part at a time, and '
  'pilot brings it in at one place at a time.',
  ['Correct. There is no fallback, which is exactly why it is the cheapest and the '
   'most exposed.',
   'Correct. Running both and comparing is what makes it safe, and paying for both is '
   'what makes it costly.',
   'Wrong. Installing at one site first is the PILOT strategy. Phased brings the '
   'system in module by module.',
   'Wrong, and it is the reverse: parallel running is the most expensive, because '
   'both systems and both sets of staff effort are paid for at once.'])

q('ins-x-17', 11, 'build against buy',
  'An organisation is choosing between developing a system in house and buying a '
  'commercial package. Which TWO statements are correct?',
  ['Building in house gives a closer fit to the organisation\'s own processes',
   'Buying a package usually delivers faster and at a lower initial cost',
   'Buying a package guarantees a closer fit to the business processes',
   'Building in house removes the need for a feasibility study'],
  ['a', 'b'],
  'The trade is FIT against TIME and COST. Building fits exactly and takes longer; '
  'buying arrives sooner and asks the organisation to bend towards the software.',
  ['Correct. It is built to the requirements you gathered, so it matches them.',
   'Correct. The development has already been paid for by everyone else who bought '
   'it.',
   'Wrong, and it is the main argument against buying: the package embodies someone '
   'else\'s idea of the process.',
   'Wrong. Feasibility is assessed whichever route is chosen, and the choice itself '
   'is part of what feasibility examines.'])

q('ins-x-18', 11, 'client-server architecture',
  'In a three-tier architecture, what are the three tiers?',
  ['Presentation, application logic, and data',
   'Input, processing, and output',
   'Hardware, software, and people',
   'Analysis, design, and implementation'],
  'a',
  'The tiers separate what the user sees, what the system decides, and where the '
  'data lives. The point of the split is that any one tier can be changed or scaled '
  'without rewriting the others.',
  ['Correct. Presentation at the front, business logic in the middle, the database '
   'behind.',
   'Wrong. Input, process, output is the general model of any program, not an '
   'architecture.',
   'Wrong. Those are components of an information SYSTEM, not tiers of an '
   'architecture.',
   'Wrong. Those are phases of the life cycle.'])

q('ins-x-19', 11, 'types of maintenance',
  'Which TWO statements about system maintenance are correct?',
  ['Corrective maintenance fixes faults found after the system went live',
   'Adaptive maintenance changes the system to suit a new environment or a new '
   'regulation',
   'Perfective maintenance means removing features that are no longer used',
   'Preventive maintenance is the same thing as corrective maintenance'],
  ['a', 'b'],
  'Four kinds, and the examiner wants them separated: corrective fixes what is '
  'broken, adaptive responds to a changed environment, perfective improves what '
  'already works, and preventive reduces future failure.',
  ['Correct. It is the reactive one: something is wrong, and it is repaired.',
   'Correct. A new tax rate or a new operating system forces adaptive change though '
   'nothing is broken.',
   'Wrong. Perfective maintenance IMPROVES performance or maintainability, or adds '
   'requested enhancements.',
   'Wrong. Preventive works on code that has not failed yet; corrective works on '
   'code that has.'])

q('ins-x-20', 11, 'project management',
  'Which TWO statements about scheduling a project are correct?',
  ['A Gantt chart shows tasks as bars against a calendar, making durations and '
   'overlaps visible',
   'The critical path is the longest chain of dependent tasks, and it sets the '
   'shortest possible project duration',
   'The critical path is the chain of tasks that can slip without affecting the end '
   'date',
   'A Gantt chart shows the dependencies between tasks better than any other tool'],
  ['a', 'b'],
  'A Gantt chart shows WHEN; a network diagram shows WHAT DEPENDS ON WHAT. The '
  'critical path comes out of the second and is the sequence with no slack, so a day '
  'lost anywhere on it is a day lost on the project.',
  ['Correct. It is the calendar view, and it is what a client is usually shown.',
   'Correct. It is longest and therefore binding: nothing can finish sooner than the '
   'critical path allows.',
   'Wrong, and it is exactly backwards. Tasks that can slip have FLOAT, and they are '
   'by definition not on the critical path.',
   'Wrong. Dependencies are what a PERT or network diagram shows. A Gantt chart shows '
   'them poorly, which is why both tools exist.'])

q('ins-x-21', 11, 'interface design',
  'Which TWO principles of user interface design are correct?',
  ['Be consistent, so the same action produces the same result everywhere in the '
   'system',
   'Give feedback, so the user always knows what the system is doing and what '
   'happened',
   'Maximise the amount of information on every screen so fewer screens are needed',
   'Require the user to memorise codes, since experts work faster with codes'],
  ['a', 'b'],
  'Consistency and feedback are the two that appear on every list. Both reduce the '
  'load on the user\'s memory, which is the underlying goal of the whole subject.',
  ['Correct. Consistency means the interface can be learned once rather than '
   'relearned per screen.',
   'Correct. A user with no feedback cannot tell a slow system from a broken one.',
   'Wrong. Crowding a screen raises the error rate. The principle is the opposite: '
   'reduce what the eye must sort through.',
   'Wrong. Recognition over recall is the principle. The system should show the '
   'options, not demand that the user remembers them.'])
