"""
shortcuts.py — the exam-speed "Shortcut" line added under every worked example
and every solved question in the manual.

Each worked/solution box (class "box work") gets one teal Shortcut callout at the
foot of its body: the fastest correct route to the same answer under exam time.
Kept out of the frozen content and injected at ASSEMBLE time, so it survives
`freeze.py --force` (which re-derives the teaching prose from the v1 PDF) and
lives in exactly one place.

Data shape: SHORTCUTS[section][exact_bar_label] = "inner html of the shortcut".
Every label must match exactly one box in its section, or the build fails loudly
(a label that stopped matching means the box text changed and the shortcut needs
re-checking). House style still applies: no em/en dashes.

The module5 and tutorial sections carry their shortcuts inline in their authored
HTML, so they are not listed here.
"""
import re

SHORTCUTS = {
  'foundations': {
    'WORKED EXAMPLE · CONVERT BEFORE YOU CALCULATE': 'Recognition tip: scan the units before reaching for any formula. Metres and coulombs are already SI, so there is nothing to convert here; the only quantities that ever need work are cm (×10<sup>−2</sup>), cm<sup>2</sup> (×10<sup>−4</sup>), and the milli, micro, nano prefixes.',
    'WORKED EXAMPLE · THREE REARRANGEMENTS YOU WILL NEED CONSTANTLY': 'Recognition tip: undo operations outermost first. In W = ½CV<sup>2</sup> the ½ is the outermost multiplier, so clear it (×2) before you touch the V<sup>2</sup>; trying to divide by V<sup>2</sup> while the ½ still clings on is the usual slip.',
    'WORKED EXAMPLE · THE KIRCHHOFF SYSTEM FROM MODULE 3': 'Because I<sub>1</sub> is already isolated, skip the expansion line: the I<sub>3</sub> coefficient collapses to 10 − 18 = −8 and the constant to 50 − 1.25 × 18 = 27.5, so I<sub>3</sub> = 27.5 / (−8) = −3.44 A in one step.',
    'WORKED EXAMPLE · BOTH ROUTES, SAME ANSWER': 'Pull out the common 50: the two resistors are 50 × 5 and 50 × 3, so product over sum is 50 × (5 × 3)/(5 + 3) = 50 × 15/8 = 93.75 Ω, with no large multiplication to do.',
  },
  'module1': {
    'WORKED EXAMPLE · FORCE BETWEEN TWO PROTONS 5 M APART': 'Group the powers of ten first: 10<sup>9</sup> × (10<sup>−19</sup>)<sup>2</sup> = 10<sup>−29</sup>, leaving only 8.99 × 2.56 / 25 ≈ 0.92, so the answer is 0.92 × 10<sup>−29</sup> = 9.2 × 10<sup>−30</sup> N without dragging the tiny numbers through every line.',
    'WORKED EXAMPLE · DIRECTION AND FORCE NEAR A 1 C CHARGE': 'With r = 1 m the r<sup>2</sup> disappears, so E = kQ = 8.99 × 10<sup>9</sup> N/C straight off; then F = qE just multiplies the fronts (1.4 × 8.99 ≈ 12.6) and adds exponents (−5 + 9 = 4) to give 1.26 × 10<sup>5</sup> N. The negative test charge flips the direction, so the force points in toward the source while the field points out: the classic field versus force trap.',
    'WORKED EXAMPLE · TWO POINT CHARGES, 1.0 CM APART': 'Use k ≈ 9 × 10<sup>9</sup> and combine powers: k × q<sub>A</sub>q<sub>B</sub> = 9 × 10<sup>9</sup> × 4 × 10<sup>−18</sup> = 3.6 × 10<sup>−8</sup>, then divide by r<sup>2</sup> = (10<sup>−2</sup>)<sup>2</sup> = 10<sup>−4</sup>, which merely adds 4 to the exponent: 3.6 × 10<sup>−4</sup> N. The one trap is r<sup>2</sup> = 10<sup>−4</sup>, not 10<sup>−3</sup>.',
    'WORKED EXAMPLE · POTENTIAL 2 M FROM A 5 × 10 −6 C CHARGE': 'Potential carries plain r, not r<sup>2</sup>: with k ≈ 9 × 10<sup>9</sup> the top is 9 × 10<sup>9</sup> × 5 × 10<sup>−6</sup> = 4.5 × 10<sup>4</sup>, halved to 2.25 × 10<sup>4</sup> V. The field at the same point is this divided by one more r, i.e. half again, 1.12 × 10<sup>4</sup> V/m: the 1/r versus 1/r<sup>2</sup> distinction in a single line.',
    'WORKED EXAMPLE · WORK DONE MOVING 3 C THROUGH 12 V': 'Recognition tip: this is pure W = qV, so it is one multiplication, 3 × 12 = 36 J. The potential difference already bundles in every field and distance, so never reach for those here.',
    'CASE 1 · FIELD OF A POINT CHARGE': "Recognition tip: the 4π in E = Q/(4πε<sub>0</sub>r<sup>2</sup>) is nothing but the 4πr<sup>2</sup> surface area of the sphere you drew. Once you see flux = E × 4πr<sup>2</sup> = Q/ε<sub>0</sub>, the field falls out in one rearrangement and Coulomb's law is recovered for free.",
    'WORKED EXAMPLE · FIELD AT THE SURFACE OF A GAUSSIAN SPHERE': 'With k ≈ 9 × 10<sup>9</sup> the top is 9 × 10<sup>9</sup> × 5 × 10<sup>−6</sup> = 4.5 × 10<sup>4</sup>, and dividing by 0.2<sup>2</sup> = 0.04 is the same as multiplying by 25, giving 1.12 × 10<sup>6</sup> N/C. Guard the 0.2<sup>2</sup> = 0.04, not 0.4.',
    'WORKED EXAMPLE · TOTAL FLUX THROUGH A SURFACE ENCLOSING 3 µC': 'Recognition tip: flux through a closed surface is only Q<sub>enclosed</sub>/ε<sub>0</sub>, so it is one division, 3/8.85 = 0.339 with exponent −6 − (−12) = 6, giving 0.339 × 10<sup>6</sup> = 3.39 × 10<sup>5</sup> N m<sup>2</sup>/C. The radius and shape are decoys; do not go looking for geometry.',
    'WORKED EXAMPLE · FIELD FROM A LONG CHARGED WIRE': 'Since k = 1/(4πε<sub>0</sub>), the line-charge prefactor 1/(2πε<sub>0</sub>) is just 2k, so E = 2kλ/r = 2 × 9 × 10<sup>9</sup> × 4 × 10<sup>−6</sup> / 0.05 ≈ 1.44 × 10<sup>6</sup> N/C, skipping the 2πε<sub>0</sub> arithmetic entirely.',
  },
  'module2': {
    "WORKED EXAMPLE · THE OHM'S LAW TEMPERATURE TEST": 'Recognition tip: the voltage is 2 V in both trials, so R simply tracks 1/I. The current jumps from 2 to 5 mA, so R must fall, and any material whose R changes with temperature is by definition not ohmic. You can call it before finishing either division.',
    'WORKED EXAMPLE 1 · CAPACITANCE OF AN ISOLATED CONDUCTING SPHERE': 'Recognition tip: substituting V = Q/(4πε<sub>0</sub>R) into C = Q/V cancels the Q on sight, since dividing Q by Q/(4πε<sub>0</sub>R) flips the fraction to 4πε<sub>0</sub>R. Capacitance always ends up charge-free, a pure function of geometry.',
    'WORKED EXAMPLE · CAPACITANCE OF A SHELL OF RADIUS 100 CM': "Since 4πε<sub>0</sub> = 1/k, the sphere's C = 4πε<sub>0</sub>R is simply R/k = 1.0 / (9 × 10<sup>9</sup>) ≈ 1.11 × 10<sup>−10</sup> F, with no 4π multiplication at all.",
    'WORKED EXAMPLE 2 · INSERTING A DIELECTRIC': 'A dielectric just multiplies C by ε<sub>r</sub>, so this is one product: 3 × 8.85 × 10<sup>−11</sup> = 2.66 × 10<sup>−10</sup> F. Because ε<sub>r</sub> > 1 the answer must grow, never shrink.',
    'WORKED EXAMPLE 3 · A PARALLEL AND SERIES COMBINATION': 'Collapse the parallel pair by adding (2 + 3 = 5 µF), then series is product over sum, (5 × 4)/(5 + 4) = 20/9 µF. For the energy reuse Q from part (b): W = ½QV = ½ × 2.667 × 10<sup>−5</sup> × 12 = 1.6 × 10<sup>−4</sup> J, and keep C<sub>eq</sub> as the exact 20/9 so Q lands on 2.667 × 10<sup>−5</sup>, not the rounded 2.66.',
  },
  'module3': {
    'WORKED EXAMPLE · COMPARING CURRENTS': 'Spot the trap first: a walking person carries no <i>net</i> charge, so (c) is zero on sight. For the other two just divide coulombs by seconds, and the one with less time underneath, (b) at 3 C in 1 s, wins.',
    'WORKED EXAMPLE · HOW MANY ELECTRONS?': 'Do it in one line, N = IΔt/e = (0.22 × 4.5)/(1.6 × 10⁻¹⁹). Divide the fronts, 0.99/1.6 = 0.62, and the 10⁻¹⁹ on the bottom flips up to 10¹⁹: 6.2 × 10¹⁸ electrons.',
    'WORKED EXAMPLE · CHARGE AND WORK IN A FLASHLIGHT': 'Chain it as W = εIΔt without isolating the charge: (1.5)(0.44)(64). And multiplying by 1.5 is just adding half, so 28 + 14 = 42 J.',
    'WORKED EXAMPLE · CURRENT THROUGH A RESISTOR': 'I = V/R = 24/150 cancels by 3 to 8/50, and 8/50 = 0.16 A.',
    'WORKED EXAMPLE · THREE RESISTORS IN SERIES': 'The same I flows through all three, so V₁ = 0.032 × 250 = 8 V and V₂ = 0.032 × 150 = 4.8 V, and V₃ is simply the leftover of the supply: 24 − 8 − 4.8 = 11.2 V. Then R₃ = V₃/I = 11.2/0.032 = 350 Ω.',
    'WORKED EXAMPLE · THREE RESISTORS IN PARALLEL': 'You never need R<sub>eq</sub> for the currents. Every branch sees the full 24 V, so I = 24/R directly: 0.096, 0.160 and 0.0686 A, and the total is just their sum, 0.325 A. That skips inverting the reciprocals.',
    'WORKED EXAMPLE · FOUR RESISTORS, EACH R': "Two equal resistors in parallel are always half of one, R/2. The line is then R + R/2 + R, and two whole R's plus a half read straight off as 2.5R.",
    'WORKED EXAMPLE · COMBINATION SPECIAL': 'For two resistors use product over sum. The series pair is 2R = 900 Ω, so R<sub>eq</sub> = (450 × 900)/(450 + 900) = 300 Ω, and I = 12/300 = 0.04 A.',
    'WORKED EXAMPLE · VOLTAGE ACROSS R 2': 'Voltage divider straight to the answer, the wanted resistor on top: V₂ = (R₂/R<sub>T</sub>) × V = (10/25) × 20. The kΩ cancel and 10/25 = 0.4, so 0.4 × 20 = 8 V, with no current computed.',
    'WORKED EXAMPLE · DIVIDER WITH 4 Ω AND 10 Ω': 'The 12 V splits in the resistor ratio 4:10. Find the smaller share, V₁ = (4/14) × 12 = 3.43 V, then V₂ is just the rest: 12 − 3.43 = 8.57 V.',
    'WORKED EXAMPLE · CURRENT DIVIDER, 2.2 KΩ AND 4.7 KΩ': 'The current divider puts the <i>other</i> resistor on top: I₁ = (4.7/6.9) × 8 = 5.45 mA. Then I₂ is simply the leftover, 8 − 5.45 = 2.55 mA, so no second ratio is needed.',
    'WORKED EXAMPLE · TWO MULTIPLE CHOICE QUESTIONS': 'Recognise it without full working: in parallel the larger resistor carries the smaller current, so the 200 Ω branch takes the smallest option, 6.7 mA. Both branches share one voltage, V = I₂R₂ = 6.7 mA × 200 = 1.33 V.',
    'WORKED EXAMPLE · A SINGLE LOOP, WORKED COMPLETELY': 'This loop is plain series, so skip the sign bookkeeping: I = ε/(7 + 3) = 12/10 = 1.2 A in one step. Then V<sub>AB</sub> = 1.2 × 7 = 8.4 V and V<sub>BC</sub> = 1.2 × 3 = 3.6 V, which must add back to 12.',
    'WORKED EXAMPLE · USING KCL AND KVL TOGETHER': 'Parallel branches split the 10 A inversely to resistance, so the 4 Ω takes twice the 8 Ω current: divide 10 in the ratio 1:2 to get I₁ = 3.33 A and I₂ = 6.67 A. The pair is (8 × 4)/12 = 8/3 Ω, so V<sub>AB</sub> = 10 × 8/3 = 26.67 V.',
    'WORKED EXAMPLE · THE COMPLETE KIRCHHOFF CIRCUIT': 'You can skip the three-equation system, because this network is just series-parallel. The 6 Ω and 4 Ω are in series (10 Ω), parallel with the 8 Ω gives (8 × 10)/18 = 4.44 Ω, in series with the first 10 Ω for 14.44 Ω, so I₁ = 50/14.44 = 3.46 A. That I₁ splits between the 8 Ω and the 10 Ω branch inversely: I₂ = I₁ × 10/18 = 1.92 A and I₃ = I₁ × 8/18 = 1.54 A.',
  },
  'module4': {
    "WORKED EXAMPLE · RADIUS OF AN ELECTRON'S PATH": 'Read r = mv/(qB) as momentum over (charge × field). Divide the fronts, 3.644/6.4 = 0.569, and subtract the exponents, −24 − (−20) = −4: 0.569 × 10⁻⁴ = 5.69 × 10⁻⁵ m.',
    'WORKED EXAMPLE · FORCE AT AN ANGLE OF 30 DEGREES': 'sin 30° = ½, so the answer is just half of qvB. Multiply the fronts, 2 × 4 × 0.2 = 1.6, add the exponents −6 + 3 = −3 for 1.6 × 10⁻³, then halve to 8.0 × 10⁻⁴ N.',
    'WORKED EXAMPLE · FIELD 5 CM FROM A WIRE CARRYING 12 A': 'The π always cancels in B = µ₀I/(2πr): B = (4π × 12)/(2π × 0.05) × 10⁻⁷ = (2 × 12/0.05) × 10⁻⁷ = 480 × 10⁻⁷ = 4.8 × 10⁻⁵ T.',
    "WORKED EXAMPLE · DERIVING THE STRAIGHT-WIRE FIELD FROM AMPERE'S LAW": 'Recognise the one move: on a circular loop B is constant, so the integral is just B times the circumference, B(2πr). Set that equal to µ₀I and divide, giving B = µ₀I/(2πr) with no calculus.',
    'WORKED EXAMPLE · A COIL OF 200 TURNS': "Dividing by 0.10 s is multiplying by 10, so ε = N × |ΔΦ| × 10 = 200 × 0.06 × 10 = 120 V. The flux fell, so the minus sign in Faraday's law lands on a negative ΔΦ and the emf comes out positive.",
    'WORKED EXAMPLE 1 · FIND THE EMF': 'With I = 1 A, E = I(R + r) is just the sum of the resistances read straight off as volts: 5 + 0.5 = 5.5 V.',
    'WORKED EXAMPLE 2 · FROM TERMINAL P.D. TO EMF': 'Emf is the terminal p.d. plus the internal drop: I = V/R = 1/5 = 0.2 A, so E = 1 + (0.2 × 2) = 1.4 V.',
    'WORKED EXAMPLE 3 · TWO MEASUREMENTS, TWO UNKNOWNS': 'Write both as E = V + Ir with currents 0.6 A and 0.3 A, then subtract to cancel E: 0.6r − 0.3r = 13.5 − 12, so 0.3r = 1.5, r = 5 Ω, and E = 12 + 0.6 × 5 = 15 V.',
    'WORKED EXAMPLE · A 2 H INDUCTOR CARRYING 5 A': '½LI² with L = 2: the ½ and the 2 cancel, so it is just I² = 5² = 25 J.',
    'WORKED EXAMPLE · FIND THE MAGNETIC DIPOLE MOMENT': 'Torque uses sine, and sin 30° = ½, so B sin θ = 0.6 × 0.5 = 0.3. Then m = τ/(B sin θ) = (4.8/0.3) × 10⁻³ = 16 × 10⁻³ = 1.6 × 10⁻² A m².',
  },
  'exercises': {
    'Q11 · FIELD INSIDE A UNIFORMLY CHARGED SOLID SPHERE': 'Inside a uniform sphere the enclosed charge and the area cancel to leave E = ρr/(3ε<sub>0</sub>), so skip the volume and flux algebra: (2 × 10<sup>−6</sup> × 0.05)/(3 × 8.85 × 10<sup>−12</sup>) ≈ 3.8 × 10<sup>3</sup> N/C. The field simply rises in proportion to r until the surface.',
    'Q12 · FIELD OUTSIDE A CHARGED CONDUCTING SPHERE': 'Once r &gt; R, treat the whole charge as a point at the centre and use kQ/r<sup>2</sup>. Work out kQ = 5.394 × 10<sup>4</sup> once, then dividing by 0.5<sup>2</sup> = 0.25 is just multiplying by 4, giving E = 2.16 × 10<sup>5</sup> N/C.',
    'Q1 · THE CAPACITOR NETWORK': 'Two in series is product over sum: 1 and 5 give 5/6 = 0.83 µF without touching reciprocals. That arm sits below the smaller 1 µF, so adding the parallel 8 barely lifts it: 0.83 + 8 = 8.83 µF in one line.',
    'Q2 · CAPACITANCE FROM STORED ENERGY': 'Go straight to C = 2W/V<sup>2</sup>: double 2.25 mJ to 4.5 × 10<sup>−3</sup> and divide by 30<sup>2</sup> = 900, giving 5 × 10<sup>−6</sup> F. Square the 30, never double it.',
    'Q3 · PARALLEL PLATE CAPACITOR WITH A DIELECTRIC': 'Sort the powers of ten first: dividing by d = 10<sup>−3</sup> just adds 3 to the exponent, so ε<sub>0</sub>A/d = (8.85 × 10<sup>−12</sup>)(4 × 10<sup>−2</sup>)/10<sup>−3</sup> = 3.54 × 10<sup>−10</sup>. Multiply by ε<sub>r</sub> = 7 to land on 2.48 × 10<sup>−9</sup> F.',
    'Q4 · CURRENT THROUGH A SERIES RESISTOR': 'Series shares one current, so naming R<sub>3</sub> changes nothing: add 7 + 6 + 3 = 16 Ω and divide, I = 48/16 = 3 A. No divider rule is needed.',
    'Q5 · CAPACITANCE OF A CHARGED SPHERE': 'Any two conductors at different potentials form a capacitor, so use the definition C = Q/V with no geometry: 4.5 × 10<sup>−9</sup>/180 = 2.5 × 10<sup>−11</sup> F = 25 pF.',
    'Q6 · VOLTAGE ACROSS R 2 WHEN R 2 = 2R 1': 'Series voltage splits in the ratio of the resistances, and R<sub>2</sub> is 2 of the 3 total parts, so V<sub>2</sub> = 2/3 of the source at a glance. The R cancels, which is why no numbers are given.',
    'Q7 · THE KIRCHHOFF TWO-LOOP PROBLEM': 'Sanity-check any two-loop answer in seconds: the branch currents must satisfy KCL at the node (1.923 + 1.538 = 3.461), and each quoted voltage should equal one current times its own resistor. If both checks pass, the solution is self-consistent.',
    'Q1 · PROTON ENTERING PERPENDICULAR TO THE FIELD': 'Perpendicular means sin θ = 1, so F = qvB in one line. For the period use T = 2πm/(qB): the speed cancels, so T is fixed by the particle and field alone (the cyclotron result), giving 1.31 × 10<sup>−7</sup> s without needing r.',
    'Q2 · ELECTRON AT 45 DEGREES: WHY THE PATH IS A HELIX': 'Recognise the split: sin θ curls the perpendicular part into the circle (r = mv sin θ/qB) while cos θ carries the parallel part forward (pitch = v cos θ × 2πm/qB). At exactly 45° the two speeds are equal, since sin 45° = cos 45°.',
    'Q3 · PROTON AT 60 DEGREES: FORCE, RADIUS AND PITCH': 'Read the half-angle values off by heart: sin 60° = 0.866, cos 60° = 0.5. Sin feeds the radius (v sin θ), cos feeds the pitch (v cos θ × T), and F = qvB sin θ, so all three parts reuse the same two numbers.',
    'Q4 · CLASS DRILL: FIND THE INTERNAL RESISTANCE': 'With I = 1 A the emf equation E = I(R + r) collapses to E = R + r, so r = 6 − 4 = 2 Ω by inspection, no algebra.',
    'Q2 · CAPACITOR NETWORK': 'Product over sum for the series pair: 1 and 5 give 5/6 = 0.83 µF, below the smaller plate, so adding the parallel 8 gives 8.8 µF (option d). Option b, 3.43, is the trap from treating the pair as parallel first.',
    'Q3 · OIL DROP HELD STATIONARY': 'Balance the forces at once: qE = mg gives E = mg/q, and the 10<sup>−6</sup> in 5 mg (as kg) cancels the µC, leaving (5 × 9.8)/9 ≈ 5.4 V/m upward. The milligram to kilogram step is the only trap.',
    'Q4 · POTENTIAL AT TWO DISTANCES': 'Potential goes as 1/r, not 1/r<sup>2</sup>. Work out kQ = 3.6 × 10<sup>4</sup> once to get 720 kV at 5 cm, then 20 cm is four times further, so quarter it: 180 kV with no fresh arithmetic.',
    'Q5 · ELECTRIC FLUX': 'Straight through means θ = 0 and cos 0 = 1, so flux is just E × A = 200 × 2 = 400 N m<sup>2</sup>/C.',
    'Q6 · PARALLEL PLATE WITH DIELECTRIC': 'Handle the powers of ten first: ε<sub>0</sub>A/d where dividing by 10<sup>−3</sup> adds 3 to the exponent, then multiply by ε<sub>r</sub> = 7 to get 2.478 × 10<sup>−9</sup> F. The 0.2478 × 10<sup>−9</sup> distractors are a single factor of ten out.',
    'Q7 · FORCE ON A CHARGE IN A FIELD': 'F = qE directly, both already in SI: 1.5 × 2500 = 3750, carry the 10<sup>−9</sup> to get 3.75 × 10<sup>−6</sup> N.',
    'Q8 · FIELD AT THE MIDPOINT BETWEEN OPPOSITE CHARGES': 'Opposite charges make both fields point the same way at the midpoint, so they add: find one, E = kQ/r<sup>2</sup> = 1.08 × 10<sup>7</sup>, then double to 2.16 × 10<sup>7</sup> N/C. Like charges would instead cancel to zero.',
    'Q9 · THE TWO VERSIONS OF THIS QUESTION THAT DO APPEAR IN THE SLIDES': 'Square, add, root: a minus component counts the same as a plus (squaring kills the sign) and a missing component is 0. Here √(3<sup>2</sup> + 4<sup>2</sup> + 2<sup>2</sup>) = √29 ≈ 5.4, and watch for Pythagorean triples that give whole numbers on sight.',
    'Q10 · CHARGE OF 6.2×10 1 8 ELECTRONS': 'Q = ne, so multiply the fronts and add the exponents: 6.2 × 1.6 = 9.92 and 10<sup>18</sup> × 10<sup>−19</sup> = 10<sup>−1</sup>, giving 0.99 C at a glance.',
    'Q11 · CAPACITANCE OF A SPHERE': 'Ignore the sphere wording and use the definition C = Q/V: 4.5 × 10<sup>−9</sup>/180 = 2.5 × 10<sup>−11</sup> F = 25 pF. No radius or geometry enters.',
    'Q12 · CURRENT THROUGH A SERIES RESISTOR': 'Series passes one current through every resistor, so R<sub>3</sub> is a red herring: I = 48/(7 + 6 + 3) = 48/16 = 3 A.',
    'Q13 · FIELD PRODUCED BY A SOURCE CHARGE': "A source charge's field depends only on itself and r, so the 8 × 10<sup>−8</sup> C is a distractor: use the 2 × 10<sup>−8</sup> C alone. With k = 9 × 10<sup>9</sup>, kQ = 180, divide by 0.4<sup>2</sup> = 0.16 to get 1125 N/C.",
    'Q14 · FIELD OUTSIDE A CONDUCTING SPHERE': 'Check r &gt; R, then treat the charge as a point at the centre: kQ = 5.394 × 10<sup>4</sup>, and dividing by 0.5<sup>2</sup> = 0.25 multiplies by 4, giving 2.16 × 10<sup>5</sup> N/C. Inside would be exactly zero.',
    'Q15 · CAPACITANCE FROM STORED ENERGY': 'C = 2W/V<sup>2</sup> straight away: 4.5 × 10<sup>−3</sup>/900 = 5 µF. Dropping the ½ gives 2.5 µF, the planted option (e), so keep the 2 in front of W.',
    'Q1 · ENERGY STORED IN AN INDUCTOR': 'W = ½LI<sup>2</sup> is the magnetic twin of ½CV<sup>2</sup>, so square the current: ½ × 2 × 5<sup>2</sup> = 25 J. Squaring L instead gives the 10 J trap.',
    'Q2 · SPEED OF A PROTON FROM THE MAGNETIC FORCE': 'Perpendicular, so F = qvB and v = F/(qB): with qB = 3.2 × 10<sup>−20</sup> the 3.2 fronts cancel and −14 − (−20) = 6, giving v = 1.0 × 10<sup>6</sup> m/s.',
    'Q3 · EMF FROM INTERNAL RESISTANCE': 'With I = 1 A, E = I(R + r) is just the sum R + r = 5 + 0.5 = 5.5 V.',
    'Q4 · EMF FROM TERMINAL P.D.': 'Use E = V + Ir with the terminal p.d. as V: I = V/R = 1/5 = 0.2 A, so E = 1 + 0.2 × 2 = 1.4 V. The external resistor hands you the current in one step.',
    "Q5 · AMPERE'S LAW IS MOST USEFUL FOR CONDUCTORS WITH HIGH ______ FILL IN THE BLANK": "Any blank about when Gauss's or Ampere's law becomes easy is answered by SYMMETRY: the integral only collapses when the field is constant along the chosen loop or surface.",
    'Q6 · TRANSFORMER EFFICIENCY': 'Efficiency is P<sub>out</sub>/P<sub>in</sub>: the lamps give 8 × 24 = 192 W out, the primary draws 240 × 1 = 240 W in, so 192/240 = 80%. The 12 V rating is a distractor.',
    'Q7 · MAGNETIC DIPOLE MOMENT OF A CURRENT LOOP': 'τ = mB sin θ, and sin 30° = ½, so the denominator is B × ½ = 0.3: m = 4.8 × 10<sup>−3</sup>/0.3 = 1.6 × 10<sup>−2</sup> A m<sup>2</sup>. Torque always takes sine.',
    "Q8 · RADIUS OF AN ELECTRON'S CIRCULAR PATH": 'Every option is 7.58 with a different power of ten, so only the exponent is tested: r = mv/(qB), and −24 − (−21) = −3, giving 7.58 × 10<sup>−4</sup> m.',
    'Q9 · CURRENT IN A SOLENOID': 'Convert total turns to turns per metre first: n = 800/0.4 = 2000. Then I = B/(µ<sub>0</sub>n) = 2.5 × 10<sup>−4</sup>/2.51 × 10<sup>−3</sup> ≈ 0.1 A. Skipping the N to n step is the whole trap.',
    'Q10 · TERMINAL VOLTAGE': 'Terminal voltage is emf minus the lost volts: V = E − Ir = 9 − 2 × 1 = 7 V, and it is always below the emf, so any answer above 9 V has the sign flipped.',
    'Q11 · A CHANGING MAGNETIC ______ INDUCES AN EMF': "The word is FLUX, not field: Faraday's ε = −N dΦ/dt responds to any change in Φ = BA cos θ, including area or angle, which is why a coil spinning in a steady field still induces an emf.",
    'Q12 · BIOT-SAVART DECREASES WITH THE SQUARE OF THE ______': 'Any inverse-square blank (Biot-Savart here, like Coulomb) is DISTANCE: the law carries 1/r<sup>2</sup>, so it falls with the square of the distance.',
    'Q13 · CURRENT FROM THE TERMINAL P.D.': 'The terminal p.d. is already the voltage across the external resistor, so I = V/R = 2/10 = 0.2 A. The 5 Ω internal resistance and the "after 2 seconds" are both red herrings.',
    'Q14 · CURRENT IN A LONG STRAIGHT WIRE': 'Write µ<sub>0</sub> = 4π × 10<sup>−7</sup> so the 2π in I = 2πrB/µ<sub>0</sub> cancels to a half: I = rB/(2 × 10<sup>−7</sup>) = (0.05 × 4 × 10<sup>−5</sup>)/(2 × 10<sup>−7</sup>) = 10 A.',
    'Q15 · STEP-UP TRANSFORMER': 'Voltage follows the turns ratio: N<sub>s</sub>/N<sub>p</sub> = 1000/100 = 10, so V<sub>s</sub> = 10 × 240 = 2400 V. N<sub>s</sub> &gt; N<sub>p</sub> means step up, so the answer must exceed 240 V.',
  },
  'mocks': {
    "Q16 · COULOMB'S LAW AND 2-D SUPERPOSITION": 'The two forces are already perpendicular: P sits directly above S and R directly beside it, so skip resolving into components and go straight to F<sub>net</sub> = √(F<sub>P</sub><sup>2</sup> + F<sub>R</sub><sup>2</sup>). Fix the directions by feel: unlike charges attract, so S is pulled up toward P; like charges repel, so S is pushed left away from R.',
    'Q17 · POTENTIAL, FIELD AND WORK': 'Find V = kQ/r once, then the field is just E = V/r with no need to re-substitute an r squared, and the work is W = qV in a single line. Keep the minus sign on the −2.0 µC charge so the work lands negative.',
    'Q18 · CAPACITOR NETWORK': 'Add the parallel pair (4 + 12 = 16 µF), then product over sum with C<sub>3</sub> gives C<sub>eq</sub> = 128/24 = 5.33 µF; from there Q = C<sub>eq</sub>V and W = ½QV each fall out in one line. For part (d) only C<sub>3</sub> changes, so reuse the 16 µF and redo product over sum with 4 × 8 = 32: C<sub>eq</sub> = 512/48 = 10.67 µF.',
    "Q19 · KIRCHHOFF'S LAWS": 'The resistors hand you the ratios: equation (2) gives I<sub>2</sub> = 1.5 I<sub>3</sub> and the junction gives I<sub>1</sub> = 2.5 I<sub>3</sub>, so equation (1) collapses to 27.5 I<sub>3</sub> = 40 in one substitution. The p.d. across the 10 Ω is then the source minus the 5 Ω drop: 40 − 5 I<sub>1</sub> = 21.8 V.',
    'Q20 · INDUCTION AND HELICAL MOTION': 'One velocity split unlocks all three parts: v sin30° is the perpendicular part that bends into the circle, v cos30° is the parallel part that just drifts along. Use r = mv<sub>perp</sub>/(qB) for the radius and pitch = v<sub>par</sub>T for the pitch, where the period T = 2πm/(qB) needs no speed at all.',
    'QUESTION 11 · ELECTROSTATICS': "Both charges sit 0.10 m from the midpoint, so factor the shared distance: V = k(q<sub>1</sub> + q<sub>2</sub>)/0.10, simply adding the signed charges since potential is a scalar. The force needs only the magnitudes in one Coulomb's-law line, and the opposite signs make it attractive.",
    'QUESTION 12 · CAPACITANCE': 'Compute C<sub>0</sub> = ε<sub>0</sub>A/d once, then the dielectric merely multiplies it by 5 with no re-derivation. With C known, take Q = CV first and get the energy from W = ½QV, which reuses that charge and skips squaring the voltage.',
    'QUESTION 13 · CIRCUIT ANALYSIS': 'Product over sum gives R<sub>p</sub> = 48/16 = 3 Ω, so R<sub>total</sub> = 6 + 3 = 9 Ω and I = 24/9 = 2.67 A. Skip the voltage step for the last part: the current divider puts the other branch on top, so I<sub>4</sub> = I × 12/(4 + 12) = 2.0 A.',
    'QUESTION 14 · MAGNETISM AND INDUCTION': 'At 90° sin\u2009θ = 1, so F = qvB drops the angle entirely and r = mv/(qB) follows at once (use the electron mass, not the proton). For the emf only the change counts: ΔΦ = 0.05 − 0.01 = 0.04 Wb, then ε = N ΔΦ/Δt = 30 V.',
  },
  'module5body': {
    'Worked example · Displacement current in a charging capacitor': 'Part (a) needs no arithmetic: the displacement current simply continues the wire current, so I<sub>d</sub> = 2.5 A. For (b), fold the area in directly, dE/dt = I / (ε₀πr²) = 2.5 / (8.85 × 10⁻¹² × 0.0314) ≈ 9.0 × 10¹² V/(m·s), since ε₀πr² ≈ 2.78 × 10⁻¹³.',
    'Worked example · Computing the speed of light': 'Split the tens from the fronts: μ₀ε₀ = (4π × 8.85) × 10⁻¹⁹ ≈ 111 × 10⁻¹⁹ = 1.11 × 10⁻¹⁷, whose square root is about 3.34 × 10⁻⁹, so c = 1/that ≈ 3.0 × 10⁸ m/s.',
    'Worked example · From E₀ to B₀': 'B₀ = E₀/c is one division by 3 × 10⁸: 0.080/3.0 = 0.0267, then shift by 10⁸ to get 2.67 × 10⁻¹⁰ T. B is smaller than E by the full factor of c, which is why light reads as an electric effect.',
    'Worked example · Intensity and field of a laser beam': 'I = P/A = 5.0 × 10⁻³ / 3.0 × 10⁻⁶ = 1.67 × 10³ W/m² by inspection. Then use that 1/(ε₀c) ≈ 377 (the impedance of free space), so E₀ = √(2 × 377 × I) = √(754 × 1667) ≈ 1120 V/m in a single root.',
  },
  'module5assess': {
    'Exercise 1 · Displacement current': 'Cancel the powers of ten before multiplying: 10⁻¹² × 10⁻² × 10¹² = 10⁻², leaving only 8.85 × 2.0 × 5.0 = 88.5, so I<sub>d</sub> = 88.5 × 10⁻² = 0.885 A.',
    'Exercise 2 · Wavelength from frequency': 'λ = c/f, and the tens do the work: 3.0/2.45 ≈ 1.22 with 10⁸/10⁹ = 10⁻¹, so λ ≈ 0.122 m, about 12 cm, no calculator needed.',
    'Exercise 3 · Amplitudes and energy': 'B₀ = E₀/c = 60/(3 × 10⁸) = 2.0 × 10⁻⁷ T in one step. Do (c) before (b): u = ε₀E₀² = 3.19 × 10⁻⁸ J/m³, then the intensity is just I = ½cu = ½(3 × 10⁸)(3.19 × 10⁻⁸) = 4.78 W/m², reusing u instead of re-multiplying ε₀c.',
    'Exercise 4 · From intensity back to the field': 'Since 1/(ε₀c) ≈ 377, the field from an intensity is E₀ = √(2 × 377 × I) = √(754 × 1000) ≈ 868 V/m, then B₀ = E₀/c ≈ 2.9 × 10⁻⁶ T in one more division.',
    'Exercise 5 · Field rate in a charging capacitor': 'Skip computing I<sub>d</sub> on its own: it is just the 3.0 A wire current, so dE/dt = I / (ε₀πr²) = 3.0 / (8.85 × 10⁻¹² × 7.85 × 10⁻³) ≈ 4.3 × 10¹³ V/(m·s). Halving the radius from the 10 cm example quarters the area, hence quadruples the rate.',
  },
}


def _box_end(html, start):
    """Index just past the </div> that closes the box beginning at `start`."""
    i, depth = start, 0
    while i < len(html):
        if html.startswith('<div', i):
            depth += 1; i += 4
        elif html.startswith('</div>', i):
            depth -= 1; i += 6
            if depth == 0:
                return i
        else:
            i += 1
    raise ValueError('unclosed box')


def _norm(s):
    """A label reduced to bare uppercase words, so keys are clean and robust to the
    <sub>/<sup> tags and stray spaces the reconstruction leaves in a box bar."""
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', s).strip().upper()


def inject(name, html):
    """Insert each shortcut at the foot of its work box, matching boxes by their
    normalized bar label. Fails loudly if a key matches no box or more than one, or
    if a box already carries a shortcut (double application)."""
    data = {_norm(k): (k, v) for k, v in (SHORTCUTS.get(name) or {}).items()}
    if not data:
        return html
    out, i, used = [], 0, {}
    while True:
        start = html.find('<div class="box work">', i)
        if start == -1:
            out.append(html[i:]); break
        end = _box_end(html, start)
        box = html[start:end]
        m = re.search(r'<div class="bar"><span>(.*?)</span>', box, re.S)
        key = _norm(m.group(1)) if m else None
        out.append(html[i:start])
        if key in data:
            used[key] = used.get(key, 0) + 1
            if 'class="shortcut"' in box:
                raise SystemExit(f'\nshortcuts.py: box {data[key][0]!r} in {name} '
                                 f'already has a shortcut.\n')
            bc = box.rfind('</div>', 0, len(box) - 6)      # the body's </div>
            piece = f'<p class="shortcut"><b>Shortcut.</b> {data[key][1]}</p>'
            box = box[:bc] + piece + box[bc:]
        out.append(box)
        i = end
    for key, (orig, _) in data.items():
        n = used.get(key, 0)
        if n != 1:
            raise SystemExit(
                f'\nshortcuts.py: label {orig!r} matched {n} boxes in {name} '
                f'(need exactly 1). The box bar changed; re-check the key.\n')
    return ''.join(out)


def count(name):
    return len(SHORTCUTS.get(name) or {})
