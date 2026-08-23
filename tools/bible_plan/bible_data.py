"""Book data for the reading plan.

Each entry: (name, chapters, verses, [chapters after which a SECTION ends]).

The break list is the whole point of the plan. A day may only end at one of these
chapters, so a reading never stops in the middle of a narrative, a discourse or an
argument. They are the standard structural divisions: the flood narrative, the
Sermon on the Mount, Paul's argument in Romans 9 to 11, the Servant Songs, and so
on. Where a book is short enough to read whole, its only break is its last chapter.

Verse counts are the traditional totals and are used only for BALANCE: a Psalms
chapter averages 16 verses and a Kings chapter over 30, so counting chapters alone
would make some days twice the reading of others.
"""

OT = [
    ("Genesis",         50, 1533, [2,5,9,11,14,17,20,23,24,26,28,31,33,36,37,38,41,45,47,50]),
    ("Exodus",          40, 1213, [2,4,7,10,13,15,18,20,24,31,34,40]),
    ("Leviticus",       27,  859, [7,10,15,17,20,22,25,27]),
    ("Numbers",         36, 1288, [4,6,10,12,14,19,21,25,30,36]),
    ("Deuteronomy",     34,  959, [4,11,16,20,26,28,30,34]),
    ("Joshua",          24,  658, [5,8,12,19,21,24]),
    ("Judges",          21,  618, [2,5,8,9,12,16,18,21]),
    ("Ruth",             4,   85, [4]),
    ("1 Samuel",        31,  810, [3,7,12,15,17,20,24,27,31]),
    ("2 Samuel",        24,  695, [4,7,10,12,14,18,20,24]),
    ("1 Kings",         22,  816, [2,4,8,11,14,16,19,22]),
    ("2 Kings",         25,  719, [2,8,11,14,17,20,23,25]),
    ("1 Chronicles",    29,  942, [9,12,17,21,27,29]),
    ("2 Chronicles",    36,  822, [9,12,16,20,24,28,32,36]),
    ("Ezra",            10,  280, [6,10]),
    ("Nehemiah",        13,  406, [7,10,13]),
    ("Esther",          10,  167, [2,5,10]),
    ("Job",             42, 1070, [2,14,21,31,37,41,42]),
    # Every psalm is complete in itself, so any boundary is legitimate; the five
    # books of the Psalter and the named collections are preferred where they fall.
    ("Psalms",         150, 2461, list(range(1,151))),
    ("Ecclesiastes",    12,  222, [2,6,8,11,12]),
    ("Song of Songs",    8,  117, [4,8]),
    ("Isaiah",          66, 1292, [5,6,12,17,20,23,27,33,35,39,44,48,53,55,59,62,66]),
    ("Jeremiah",        52, 1364, [1,6,10,15,20,25,29,33,38,45,51,52]),
    ("Lamentations",     5,  154, [1,2,3,4,5]),
    ("Ezekiel",         48, 1273, [3,7,11,15,19,24,28,32,36,39,43,48]),
    ("Daniel",          12,  357, [3,6,7,9,12]),
    ("Hosea",           14,  197, [3,7,11,14]),
    ("Joel",             3,   73, [3]),
    ("Amos",             9,  146, [2,6,9]),
    ("Obadiah",          1,   21, [1]),
    ("Jonah",            4,   48, [4]),
    ("Micah",            7,  105, [2,5,7]),
    ("Nahum",            3,   47, [3]),
    ("Habakkuk",         3,   56, [3]),
    ("Zephaniah",        3,   53, [3]),
    ("Haggai",           2,   38, [2]),
    ("Zechariah",       14,  211, [6,8,14]),
    ("Malachi",          4,   55, [4]),
]

NT = [
    ("Matthew",         28, 1071, [2,4,7,9,10,12,13,17,18,20,23,25,28]),
    ("Mark",            16,  678, [1,3,4,6,8,10,13,16]),
    ("Luke",            24, 1151, [2,4,6,8,9,11,13,16,18,21,24]),
    ("John",            21,  879, [1,4,6,8,10,12,17,19,21]),
    ("Acts",            28, 1007, [2,5,8,12,15,18,21,26,28]),
    ("Romans",          16,  433, [3,5,8,11,16]),
    ("1 Corinthians",   16,  437, [4,7,11,14,16]),
    ("2 Corinthians",   13,  257, [7,9,13]),
    ("Galatians",        6,  149, [2,4,6]),
    ("Ephesians",        6,  155, [3,6]),
    ("Philippians",      4,  104, [2,4]),
    ("Colossians",       4,   95, [2,4]),
    ("1 Thessalonians",  5,   89, [3,5]),
    ("2 Thessalonians",  3,   47, [3]),
    ("1 Timothy",        6,  113, [3,6]),
    ("2 Timothy",        4,   83, [4]),
    ("Titus",            3,   46, [3]),
    ("Philemon",         1,   25, [1]),
    ("Hebrews",         13,  303, [4,7,10,13]),
    ("James",            5,  108, [2,5]),
    ("1 Peter",          5,  105, [2,5]),
    ("2 Peter",          3,   61, [3]),
    ("1 John",           5,  105, [2,5]),
    ("2 John",           1,   13, [1]),
    ("3 John",           1,   14, [1]),
    ("Jude",             1,   25, [1]),
    ("Revelation",      22,  404, [3,5,8,11,14,16,19,22]),
]
