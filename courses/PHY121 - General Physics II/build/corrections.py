"""
corrections.py — errata against the original manual.

The rebuild reproduces v1's wording verbatim, which is what keeps it trustworthy.
These are the places where v1 is WRONG and reproducing it faithfully would ship a
physics error. Each entry records what was wrong and why the replacement is right.

Applied to the generated HTML in freeze.py, so they survive `freeze.py --force`
and cannot be lost by re-deriving from the PDF.

Every entry MUST match exactly once. If v1's text ever changes so a pattern stops
matching, the build fails loudly rather than silently dropping the correction.
"""

THIN = ' '   # v1 sets its formulas with thin spaces

CORRECTIONS = {

 'module2': [
  # U = -p.E. As printed, aligned (theta=0) gives U = +pE, a MAXIMUM, which
  # contradicts this box's own note ("minimum when aligned") and the next box's
  # text. Decisive check: tau = -dU/dtheta on the printed form gives +pE sin theta,
  # an ANTI-restoring torque that would drive the dipole away from alignment. The
  # error survived because the box verifies its claim against the torque formula,
  # which is correct, and never against the energy formula.
  (f'<div class="eq">U = pE{THIN}cos{THIN}θ</div>',
   f'<div class="eq">U = −pE{THIN}cos{THIN}θ</div>',
   'dipole potential energy is U = -pE cos(theta); the minus sign was missing'),

  # Ceq = 20/9 uF exactly, so Q = (20/9)e-6 * 12 = 2.6667e-5 C = 26.7 uC to 3 s.f.
  # 26.6 comes from carrying the rounded 2.22 uF forward -- the exact mistake this
  # manual's own rounding-discipline trap warns against. The same box already
  # states "I recomputed each independently: Q = 2.6667e-5 C", i.e. 26.7.
  ('(b) Q ≈ 26.6 µC',
   '(b) Q ≈ 26.7 µC',
   'Q = 2.6667e-5 C rounds to 26.7 uC, not 26.6; 26.6 came from early rounding'),
 ],

 'module1': [
  # The Gauss's law cases run 1, 2, 3, then 5. "CASE 4" appears nowhere in the
  # manual, so this is a numbering slip, not a missing case.
  ('CASE 5: THE FIELD INSIDE A HOLLOW CONDUCTOR IS ZERO',
   'CASE 4: THE FIELD INSIDE A HOLLOW CONDUCTOR IS ZERO',
   'cases run 1,2,3,5; there is no CASE 4 anywhere in the manual'),
 ],

 'module3': [
  # Both loop arrows sweep clockwise, and every sign in the working is the
  # clockwise reading: "the battery is a rise" is only true travelling - to +,
  # i.e. UP the left side, which is clockwise. Loop 2 likewise goes UP the 8 ohm
  # against I2 (-I2(8), a rise). A student who traverses anticlockwise as
  # instructed gets every sign flipped.
  ('Assume an anticlockwise traverse.',
   'Assume a clockwise traverse.',
   'the figure and every sign in the working are clockwise'),

  # Same defect: the drawn "traverse" arrow is clockwise and step 1 travels WITH
  # the current (I(7) + I(3) - 12 = 0 is the clockwise reading). The slides' choice
  # is kept, since KVL is direction-independent and this box says so itself, but
  # the direction actually used here is now stated.
  ('choose a travel direction (the slides take anticlockwise)',
   'choose a travel direction (the arrow shows the one used here; the slides take '
   'anticlockwise, which gives the same answer)',
   'the drawn arrow and the working are clockwise, not anticlockwise'),

  # NOT corrected here, deliberately: "Req = 1/0.01352 = 73.96" (exact 73.94),
  # "1.923 + 1.538 = 3.461" (exact 3.46154 -> 3.462) and "34.61 + 15.38 = 49.99".
  # Each is the honest arithmetic of the rounded values it displays, and the manual
  # writes "= 49.99 ~ 50" rather than claiming it closes. Rewriting 3.461 to 3.462
  # would leave "1.923 + 1.538 = 3.462" on the page, which does not add up. A
  # visible sum must stay true to the numbers beside it.
 ],

 'module4': [
  # Delta-Phi is defined final - initial. The manual computes initial - final, gets
  # +0.06, and so lands on -120 V. The flux FELL, so Delta-Phi = -0.06 Wb and
  # eps = -N dPhi/dt = -(200)(-0.06)/0.10 = +120 V. The magnitude quoted in the
  # answer box (120 V) is right either way, but this is the only worked example
  # exercising the minus sign the manual devotes a MUST-MEMORISE box to, and as
  # printed it teaches "flux falls -> emf negative", which is backwards.
  ('ΔΦ = 0.08 − 0.02 = <b>0.06 Wb</b>',
   'ΔΦ = 0.02 − 0.08 = <b>−0.06 Wb</b>',
   'change in flux is final minus initial; the flux fell, so it is negative'),
  ('ε = −N · ΔΦ/Δt = −(200)(0.06) / 0.10',
   'ε = −N · ΔΦ/Δt = −(200)(−0.06) / 0.10',
   'follows the corrected sign of the flux change'),
  ('Numerator: (200)(0.06) = 12',
   'Numerator: −(200)(−0.06) = +12',
   'two minus signs make the numerator positive'),
  ('So ε = −120 V.',
   'So ε = +120 V.',
   'a falling flux drives a positive emf here; -120 V had the sign backwards'),
 ],

 'reference': [
  # Same defect as module2, on the formula sheet -- the page a student memorises.
  # The row's own note ("Minimum when aligned") is correct and contradicts the
  # formula it annotates.
  (f'<td>U = pE{THIN}cos{THIN}θ</td>',
   f'<td>U = −pE{THIN}cos{THIN}θ</td>',
   'dipole potential energy is U = -pE cos(theta); the minus sign was missing'),

  # R.1 calls itself the COMPLETE formula sheet, and the mock papers say to sit
  # them "with only a calculator and the formula sheet" -- but it stops at
  # internal resistance and carries nothing from Units 4.5 or 4.6. All four of
  # these are MUST-MEMORISE boxes in the teaching text, and both units are
  # examined (4.5 in CBT Test 2 Q1; 4.6 is Q7's torque on a current loop). A
  # student following the manual's own instruction sat those questions with no
  # sheet entry for them.
  ('<td>emf and internal resistance</td><td>E = I(R + r), V = E − Ir</td>'
   '<td>V is always less than E</td></tr></tbody>',
   '<td>emf and internal resistance</td><td>E = I(R + r), V = E − Ir</td>'
   '<td>V is always less than E</td></tr>'
   f'<tr><td>Self-induced emf</td><td>ε = −L{THIN}dI/dt</td>'
   '<td>Unit 4.5. The minus sign is Lenz again</td></tr>'
   f'<tr><td>Energy in an inductor</td><td>W = ½LI<sup>2</sup></td>'
   '<td>Unit 4.5. Mirrors ½CV² for a capacitor</td></tr>'
   f'<tr><td>Magnetic dipole moment</td><td>m = NIA</td>'
   '<td>Unit 4.6. N turns, current I, area A</td></tr>'
   f'<tr><td>Torque on a current loop</td><td>τ = mB{THIN}sin{THIN}θ = NIAB{THIN}sin{THIN}θ</td>'
   '<td>Unit 4.6. Zero when m is along B</td></tr></tbody>',
   'R.1 omitted every formula from Units 4.5 and 4.6, both examined, while '
   'calling itself complete and being the only aid allowed in the mocks'),
 ],
}


def apply(name, html):
    """Apply this section's errata. Raises if an entry does not match exactly once."""
    for old, new, why in CORRECTIONS.get(name, []):
        n = html.count(old)
        if n != 1:
            raise SystemExit(
                f'\ncorrections.py: expected exactly 1 match in {name}, found {n}.\n'
                f'  looking for: {old!r}\n'
                f'  reason     : {why}\n'
                f'The source text changed. Re-check the correction before building.\n')
        html = html.replace(old, new)
    return html


def count(name):
    return len(CORRECTIONS.get(name, []))
