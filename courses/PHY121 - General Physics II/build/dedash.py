# Context-aware removal of ALL em/en dashes from manual content.
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))

# Ordered explicit replacements (old -> new). Each must be found at least once.
REPL = [
    # --- systematic: spelling + en dashes ---
    ("Ampère–Maxwell", "Ampere-Maxwell"),
    ("Ampère's law", "Ampere's law"),
    ("Ampère", "Ampere"),
    ("Modules 1–4", "Modules 1 to 4"),
    # --- paired appositives -> parentheses ---
    ("Faraday's law, and — with E in place of B — inside Maxwell's new term",
     "Faraday's law, and (with E in place of B) inside Maxwell's new term"),
    ("the missing half — the piece Maxwell added — and then watches",
     "the missing half (the piece Maxwell added) and then watches"),
    ("this changing-field effect a name — the displacement current — and added it",
     "this changing-field effect a name (the displacement current) and added it"),
    ("carries a term Maxwell added — the last — and that one term",
     "carries a term Maxwell added (the last one) and that one term"),
    ("In free space — no charges, no currents — Maxwell's equations",
     "In free space (no charges, no currents) Maxwell's equations"),
    ("you measured with capacitors and coils — nothing about light — combine",
     "you measured with capacitors and coils (nothing about light) combine"),
    ("The average power per unit area — the <b>intensity</b> — of a sinusoidal wave",
     "The average power per unit area (the <b>intensity</b>) of a sinusoidal wave"),
    ("<b>That is a wave</b> — an electromagnetic wave — and it needs no medium",
     "<b>That is a wave</b>, an electromagnetic wave, and it needs no medium"),
    # --- independent clauses -> period ---
    ("Keep this in your pocket — it answers half",
     "Keep this in your pocket. It answers half"),
    ("The ε₀ is the price of admission — it converts",
     "The ε₀ is the price of admission. It converts"),
    ("travel through empty space — that is a wave",
     "travel through empty space. That is a wave"),
    ("sustains itself and travels through empty space — that is a wave",
     "sustains itself and travels through empty space. That is a wave"),
    ("how tiny B is compared with E — that factor of c",
     "how tiny B is compared with E. That factor of c"),
    ("smaller than E₀ — the factor of c again",
     "smaller than E₀. The factor of c again"),
    ("a few microtesla — sunlight is a surprisingly strong field",
     "a few microtesla. Sunlight is a surprisingly strong field"),
    # --- lists / summaries -> colon ---
    ("for every problem you solved — straight wires, solenoids, toroids, any steady",
     "for every problem you solved: straight wires, solenoids, toroids, any steady"),
    ("between the plates — no electrons, no ions, nothing",
     "between the plates: no electrons, no ions, nothing"),
    ("share the same sine — same k, same ω, same phase",
     "share the same sine: same k, same ω, same phase"),
    ("3. Gauss (source) laws — Gauss for E and Gauss for B",
     "3. Gauss (source) laws: Gauss for E and Gauss for B"),
    # --- 'since' fix ---
    ("a larger dE/dt is needed for the same current — the flux is spread over less area",
     "a larger dE/dt is needed for the same current, since the flux is spread over less area"),
    # --- monospace answerbox ---
    ("c = 2.998 × 10⁸ m/s  —  exactly the measured speed of light",
     "c = 2.998 × 10⁸ m/s, the measured speed of light exactly"),
    # --- remaining single appositives/relatives -> comma ---
    ("the exact quantity inside Faraday's law, and (with E in place of B) inside",
     "the exact quantity inside Faraday's law, and (with E in place of B) inside"),  # noop guard
    ("A steady field induces nothing — the same lesson as Faraday's law",
     "A steady field induces nothing, the same lesson as Faraday's law"),
    ("like water from a tap — a source",
     "like water from a tap, a source"),
    ("magnetic field lines are never born anywhere</b> — there are no magnetic charges",
     "magnetic field lines are never born anywhere</b>, there are no magnetic charges"),
    ("Gauss's law for electricity — charges make electric fields",
     "Gauss's law for electricity, which says charges make electric fields"),
    ("Gauss's law for magnetism — there are no magnetic charges",
     "Gauss's law for magnetism, which says there are no magnetic charges"),
    ("Faraday's law — a changing magnetic field makes an electric",
     "Faraday's law, a changing magnetic field makes an electric"),
    ("Ampere's law — currents make magnetic fields",
     "Ampere's law, currents make magnetic fields"),
    ("there is no <i>moving charge</i> — but there <b>is</b> a changing electric",
     "there is no <i>moving charge</i>, but there <b>is</b> a changing electric"),
    ("Ampere's law so that both surfaces give the same answer",
     "Ampere's law so that both surfaces give the same answer"),  # noop guard
    ("(rearrange first, substitute second — Foundations F.2)",
     "(rearrange first, substitute second, see Foundations F.2)"),
    ("nine trillion volts per metre every second — an enormous rate, and exactly what is needed",
     "nine trillion volts per metre every second, an enormous rate, and exactly what is needed"),
    ("must equal the conduction current in the wire — otherwise the magnetic field would jump",
     "must equal the conduction current in the wire, otherwise the magnetic field would jump"),
    ("more energy per photon — which is why gamma rays are dangerous",
     "more energy per photon, which is why gamma rays are dangerous"),
    ("S points where the energy goes — the same way the wave moves",
     "S points where the energy goes, the same way the wave moves"),
    ("A three-metre wave — which is why FM aerials",
     "A three-metre wave, which is why FM aerials"),
    ("radio to gamma rays — all the same wave, all at c",
     "radio to gamma rays, all the same wave, all at c"),
    ("A ~12 cm wave — comparable to the spacing",
     "A ~12 cm wave, comparable to the spacing"),
    ("B₀ = 6.469 × 10⁻⁶ T — all confirmed",
     "B₀ = 6.469 × 10⁻⁶ T, all confirmed"),
]

for fn in ['module5_body.html', 'module5_assess.html']:
    p = os.path.join(HERE, fn)
    t = io.open(p, encoding='utf-8').read()
    for old, new in REPL:
        if old == new:
            continue
        if old in t:
            t = t.replace(old, new)
    io.open(p, 'w', encoding='utf-8').write(t)

# verify zero dashes remain
for fn in ['module5_body.html', 'module5_assess.html']:
    t = io.open(os.path.join(HERE, fn), encoding='utf-8').read()
    em = t.count('—'); en = t.count('–')
    print(f'{fn}: em={em} en={en}')
    if em or en:
        # show remaining
        for i, ch in enumerate(t):
            if ch in '—–':
                print('   REMAINS:', t[max(0,i-40):i+40].replace(chr(10),' '))
