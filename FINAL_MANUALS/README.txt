FINAL_MANUALS — signed-off study manuals only. One per course.
Work in progress belongs in that course's drafts/ folder, never here.

-------------------------------------------------------------------------------
PHY121 - General Physics II - Study Manual v4.pdf   148 pp   signed off 2026-07-17
-------------------------------------------------------------------------------
PHY121 General Physics II, complete manual, Modules 1 to 5.

Contents: Foundations F.1-F.11, Modules 1 to 5 (eighteen units), full solutions
S.1-S.7, mock papers M.1-M.5, reference R.1-R.4. Module 5 is Maxwell's Equations
and Electromagnetic Waves. 55 clickable Contents links, real selectable text
throughout including every table.

What changed from v3 (150 pp): PHYSICS ERRORS.

v3 reproduced the original manual's wording faithfully, and the original was
wrong in places. Reproducing an error faithfully still ships the error. A full
audit of the teaching text, the solutions, the mocks and the reference sections
found and fixed:

  - Dipole potential energy printed U = pE cos(theta), missing its minus sign.
    As printed, an aligned dipole sits at maximum energy, contradicting the
    box's own note. It is U = -pE cos(theta).
  - Faraday's law example computed the flux change as initial minus final and
    landed on -120 V. The flux fell, so the change is -0.06 Wb and the emf is
    +120 V. This was the only example exercising the minus sign the manual
    devotes a MUST-MEMORISE box to, and it taught the sign backwards.
  - Both Kirchhoff examples said "anticlockwise traverse" while their diagrams
    and every sign in their working were clockwise. A student following the word
    instead of the working gets every sign inverted.
  - Total charge given as 26.6 uC, from carrying a rounded 2.22 uF forward. The
    exact 20/9 uF gives 26.7 uC. This is the early-rounding mistake the manual's
    own trap box warns against.
  - The EM spectrum chart put radio at 10^4 Hz; c/lambda gives 10^5.
  - Smaller reasoning and reference defects: an equipotential described as
    "V = 0 along it" (V is constant, not zero), a path width quoting the radius
    as the diameter, a stationary charge explained by "sin 0 = 0" when the issue
    is that v = 0, a phantom "CASE 5", and four formulas missing from R.1.

The three loop-arrow diagrams were redrawn as vector art. Their arrowheads were
rotated ~80 degrees off the arc tangent, pointing across the loop instead of
along it, which hid the clockwise/anticlockwise contradiction above.

Every correction is recorded in build/corrections.py with its rationale, applied
at freeze time so it cannot be lost by re-deriving from the original.

Verified: no blank pages; footer numbering sequential; all 55 Contents links
resolve; every number recomputed independently; no em/en dashes; no institution
or methodology-author names. Structural gates (bold, sub/superscript, blanks,
lists, tables, figures) all above floor. Every correction was then independently
re-checked by an adversarial pass, which caught two that had fixed the answer
while leaving the working beneath it describing the old one.

v3 and v2 were withdrawn as defective. Both remain in git history if a copy is
ever needed (v2 at commit 2312940).

To rebuild or update:  see "courses/PHY121 - General Physics II/README.md"
                       (cd build && python assemble.py)
