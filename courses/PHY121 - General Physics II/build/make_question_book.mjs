/**
 * The PHY121 question book, as a standalone HTML page ready for Chromium.
 *
 *   node make_question_book.mjs > question_book.html
 *
 * Same data as the platform page, same ordering, same labels. It reads the
 * bank directly rather than importing the app, so the manual can be built
 * without a running server.
 */
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA = join(HERE, '..', '..', '..', 'webapp', 'data', 'phy121');

/** Structured solutions, keyed by question id. Same files the platform reads. */
const WORKED = {};
for (const f of readdirSync(join(DATA, 'worked')))
  if (f.endsWith('.json'))
    Object.assign(WORKED, JSON.parse(readFileSync(join(DATA, 'worked', f), 'utf8')));

const qs = [];
for (const f of readdirSync(DATA)) {
  if (!f.endsWith('.json') || f === 'lessons.json' || f === 'plan.json') continue;
  let a;
  try {
    a = JSON.parse(readFileSync(join(DATA, f), 'utf8'));
  } catch {
    continue;
  }
  if (Array.isArray(a)) qs.push(...a.filter((x) => x && x.id && x.prompt));
}

const TOPICS = [
  [1, 'Charge, Coulomb and the Electric Field'],
  [2, 'Electric Potential and Energy'],
  [3, 'Electric Flux and Gauss'],
  [4, 'Capacitance, Dielectrics and Energy'],
  [5, 'Current, Resistance and Networks'],
  [6, 'EMF and Internal Resistance'],
  [7, 'Magnetic Force on Charges and Wires'],
  [8, 'Sources of a Magnetic Field'],
  [9, 'Electromagnetic Induction'],
  [10, 'Transformers'],
  [11, 'Maxwell and Electromagnetic Waves'],
];

const SPEED = {
  1: 'Convert to SI before anything else. mg to kg, µC to C, cm to m. Then ask: one charge or two? One gives a field, two gives a force.',
  2: 'Potential has a plain r, field has r squared. Four times further out makes the potential a quarter and the field a sixteenth.',
  3: 'For flux, the angle is measured from the NORMAL, not the surface. Face on means the angle is 0 and the cosine is 1, so the flux is just EA.',
  4: 'Capacitors are the opposite of resistors: parallel adds, series is the reciprocal. Energy has V squared in it.',
  5: 'Resistivity questions hide the area: a wire of radius r has A = πr², not r. Halving the radius quarters the area and quadruples the resistance.',
  6: 'Terminal voltage is always LESS than the emf, by exactly Ir. If your answer exceeds the emf you added where you should have subtracted.',
  7: 'The magnetic force never changes the speed, only the direction. Kinetic energy is unchanged and the path is a circle of radius mv/qB.',
  8: 'The loop centre formula has NO π in the denominator. The straight wire and the toroid both do. That difference alone identifies the formula.',
  9: 'Nothing changing means no emf, whatever the field strength. Faraday needs a RATE, so look for a time in the question.',
  10: 'Step the voltage up and the current steps down. Power in equals power out if it is ideal.',
  11: 'In a vacuum everything is c = 3 × 10⁸. E/B = c for a plane wave, and c = fλ ties frequency to wavelength.',
};

const esc = (s) =>
  String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/**
 * Carets to real superscripts, and "a over b" to a drawn fraction.
 *
 * Must behave exactly as components/Sci.tsx does, or the page and the printed
 * manual disagree about the same sentence. Two rules matter: "+" counts as part
 * of a term, so a denominator like (R1 + R2) survives; and BOTH sides must look
 * like algebra, because "over" is an ordinary English word and the matcher was
 * drawing prose as fractions.
 */
const MATH_WORDS = /^(sin|cos|tan|log|ln|exp|emf|sqrt)$/;
const isAlgebra = (side) => {
  // By this point carets are already <sup> tags, and "sup" would otherwise read
  // as an English word and veto its own fraction.
  const bare = side.replace(/<[^>]*>/g, '').replace(/&[a-z]+;/g, ' ');
  return (
    bare.trim().length > 0 &&
    !bare
      .split(/[^A-Za-z]+/)
      .some((w) => w.length >= 3 && w === w.toLowerCase() && !MATH_WORDS.test(w))
  );
};

const sci = (raw) => {
  let s = esc(raw).replace(/\^(-?\d+)/g, (_, d) => `<sup>${d}</sup>`);
  if (s.split(' over ').length === 2) {
    const T = '[A-Za-z0-9εμθΦλσρτπΔ₀₁₂₃₄₅₆₇₈₉²³⁻<>\\/\\w()+\\s-]';
    const re = new RegExp(
      `(${T}+?)\\s+over\\s+((?:${T}|\\.(?=\\d))+?)(?=[,;]|\\.(?!\\d)|\\s+(?:where|which|and|so|if|is|means|gives|equals|then)\\b|$)`
    );
    s = s.replace(re, (whole, a, b) =>
      isAlgebra(a) && isAlgebra(b)
        ? `<span class="frac"><span>${a.trim()}</span><span>${b.trim()}</span></span>`
        : whole
    );
  }
  return s;
};

const sourceOf = (q) => {
  const t = q.slides ?? [];
  // Mirrors lib/questionbook.ts. A test question that also carries a tutorial
  // tag says so: eighteen of the thirty were lifted straight off that deck.
  const tut = t.find((x) => /^Tut S\d+$/.test(x));
  const fromTut = tut ? `, set on tutorial slide ${tut.replace('Tut S', '')}` : '';
  const test = t.find((x) => /^Test [12] Q/.test(x));
  if (test)
    return `The real ${test.replace(/^Test (\d) Q(\d+)$/, 'test $1, question $2')}${fromTut}`;
  if (tut) return `The tutorial deck, slide ${tut.replace('Tut S', '')}, never yet set on a test`;
  const sl = t.find((x) => /^M\d+ S\d+/.test(x));
  if (sl) {
    const m = /^M(\d+) S(\d+)/.exec(sl);
    return `Lecture slides, module ${m[1]}, slide ${m[2]}`;
  }
  const r = t.find((x) => /^Ref R\./.test(x));
  if (r) return `Reference sheet ${r.replace('Ref ', '')}`;
  return t.join(', ') || 'Authored for this course';
};

/**
 * A gap question stores its holes as {{1}}, which the drill turns into an input
 * box. On paper there is no box, so the braces reached the reader raw. And its
 * answer is not in `answer` at all, it is the accepted word of each blank, so
 * the Answer line came out EMPTY on all 76 of them: 76 questions asked and
 * never answered. Mirrors lib/questionbook.ts.
 */
const blanked = (p) => String(p ?? '').replace(/\{\{\d+\}\}/g, ' ______ ');
const answerText = (q) => {
  if (q.blanks?.length)
    return q.blanks.map((b) => b.accept?.[0] ?? '').filter(Boolean).join(', ');
  const a = Array.isArray(q.answer) ? q.answer : [q.answer];
  return a.filter(Boolean).join(', ');
};

// Repeats, so they can be labelled rather than dropped.
const norm = (q) => q.prompt.toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 90);
const groups = new Map();
for (const q of qs) {
  const k = norm(q);
  if (!groups.has(k)) groups.set(k, []);
  groups.get(k).push(q);
}
const repeat = new Map();
for (const g of groups.values())
  if (g.length > 1)
    for (const q of g)
      repeat.set(q.id, g.filter((x) => x.id !== q.id).map(sourceOf).join(' and '));

const RANK = { easy: 0, medium: 1, hard: 2 };
const today = process.argv[2] ?? '';

let body = '';
let total = 0;
let contents = '';
let figuresDrawn = 0;
/**
 * The topic titles, written out beside the HTML for the renderer.
 *
 * Chromium's print-to-PDF keeps external URLs but silently drops same-document
 * anchors, so the Contents came out as printed text with nothing behind it.
 * render.py rebuilds the links afterwards, and it does that from THIS list
 * rather than by parsing the page back out of the PDF, so the two cannot
 * disagree about what the sections are called.
 */
const tocEntries = [];

for (const [num, title] of TOPICS) {
  const mine = qs
    .filter((q) => q.module === num)
    .sort((a, b) => (RANK[a.difficulty] ?? 1) - (RANK[b.difficulty] ?? 1));
  if (!mine.length) continue;
  total += mine.length;
  tocEntries.push({ num, title, questions: mine.length });
  // The anchor is kept for the HTML, which honours it; the PDF's links are
  // rebuilt from the sidecar by render.py because Chromium drops these.
  contents += `<li><a href="#t${num}"><b>${num}. ${esc(title)}</b> <span class="mut">${mine.length} questions</span></a></li>`;

  body += `<section class="topic" id="t${num}"><h2><span class="tnum">${num}</span>${esc(title)}</h2>`;
  if (SPEED[num]) body += `<p class="speed"><b>Speed tip.</b> ${esc(SPEED[num])}</p>`;

  mine.forEach((q, i) => {
    const ans = Array.isArray(q.answer) ? q.answer : [q.answer];
    // The number, the stem and the diagram are one unit. Split them and the
    // reader meets "the field represented by" at the foot of a page with the
    // picture overleaf, which is the same as having no picture at all.
    body += `<article class="q"><div class="qtop"><div class="qh"><span class="qn">${num}.${i + 1}</span>`;
    body += `<span class="pill ${q.difficulty}">${q.difficulty}</span>`;
    body += `<span class="src">${esc(sourceOf(q))}</span></div>`;
    if (repeat.get(q.id))
      body += `<p class="rep"><b>Asked twice.</b> Also set as: ${esc(repeat.get(q.id))}.</p>`;
    body += `<p class="prompt">${sci(blanked(q.prompt))}</p>`;

    // A question that depends on a diagram cannot be answered without it. The
    // SVG is authored in the bank and drawn inline, exactly as the platform
    // draws it, so the two outputs cannot show different pictures.
    if (q.figure?.svg) {
      body += '<figure class="qfig">';
      body += q.figure.svg;
      if (q.figure.caption) body += `<figcaption>${esc(q.figure.caption)}</figcaption>`;
      body += '</figure>';
      figuresDrawn++;
    }
    body += '</div>';

    // The paper's own options first, lettered and unmarked, so the question can
    // be attempted. A ticked green row above crossed red ones answers it before
    // the reader has finished the stem.
    if (q.options) {
      body += '<ol class="rawopts">';
      for (const o of q.options) body += `<li>${sci(o.text)}</li>`;
      body += '</ol>';
    } else if (q.blanks?.some((b) => b.choices?.length)) {
      // A gap question offers its words in the blank, so it is attemptable too.
      q.blanks.forEach((b, bi) => {
        if (!b.choices?.length) return;
        if (q.blanks.length > 1) body += `<p class="blanklab">Blank ${bi + 1}</p>`;
        body += '<ol class="rawopts">';
        for (const c of b.choices) body += `<li>${sci(c)}</li>`;
        body += '</ol>';
      });
    }

    // Everything past this line gives the answer away, so it is the same line on
    // every question, options or not.
    body += `<p class="attemptgap"><span>${
      q.options ? 'Answer, and why each option is right or wrong' : 'Answer'
    }</span></p>`;

    if (q.options) {
      body += '<ul class="opts">';
      for (const o of q.options) {
        const right = ans.includes(o.id);
        body += `<li class="${right ? 'opt right' : 'opt'}"><span class="tick">${right ? '&#10003;' : '&#10007;'}</span><span>${sci(o.text)}`;
        if (q.why?.[o.id]) body += `<em>${sci(q.why[o.id])}</em>`;
        body += '</span></li>';
      }
      body += '</ul>';
    } else if (q.pairs) {
      body += '<table class="pairs"><tbody>';
      for (const p of q.pairs)
        body += `<tr><td><b>${esc(p.left)}</b></td><td>${esc(p.right)}</td></tr>`;
      body += '</tbody></table>';
    } else {
      body += `<p class="ans">Answer: <b>${esc(answerText(q))}</b></p>`;
    }

    const w = WORKED[q.id];
    if (w) {
      body += '<div class="wsol">';
      if (w.background)
        body += `<div class="wp"><span class="wl">Background, so this is not just a formula</span><p>${sci(w.background)}</p></div>`;
      if (w.given?.length || w.find) {
        body += '<div class="wp wg">';
        if (w.given?.length)
          body += `<span class="wl">Given</span><ul>${w.given.map((g) => `<li>${sci(g)}</li>`).join('')}</ul>`;
        if (w.find) body += `<p><b>Find:</b> ${sci(w.find)}</p>`;
        body += '</div>';
      }
      if (w.formula) {
        body += `<div class="wp"><span class="wl">Formula</span><p class="weq">${sci(w.formula)}</p>`;
        if (w.why) body += `<p><b>Why this one.</b> ${sci(w.why)}</p>`;
        if (w.symbols?.length)
          body += `<span class="wl">What each symbol means</span><ul class="wsy">${w.symbols.map((x) => `<li>${sci(x)}</li>`).join('')}</ul>`;
        body += '</div>';
      }
      if (w.steps?.length)
        body += `<div class="wp ws"><span class="wl">The working, line by line</span><ol>${w.steps.map((x) => `<li>${sci(x)}</li>`).join('')}</ol></div>`;
      if (w.check)
        body += `<div class="wp wc"><span class="wl">Check it</span><p>${sci(w.check)}</p></div>`;
      body += '</div>';
    }

    if (q.explanation) body += `<p class="exp">${sci(q.explanation)}</p>`;
    body += '</article>';
  });

  body += '</section>';
}

process.stdout.write(`<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>PHY121 Question Book</title>
<style>
@page { size: A4; margin: 16mm 14mm 18mm; }
* { box-sizing: border-box; }
body { font-family: "DejaVu Sans", Arial, sans-serif; font-size: 9.4pt; line-height: 1.5; color: #16261c; margin: 0; }
h1 { font-size: 22pt; margin: 0 0 4px; }
h2 { font-size: 13pt; margin: 0 0 10px; padding-top: 10px; border-top: 2.5px solid #15803d; display: flex; gap: 9px; align-items: baseline; }
.tnum { background: #15803d; color: #fff; font-size: 8pt; padding: 2px 8px; border-radius: 99px; }
.cover { text-align: left; padding: 30mm 0 12mm; border-bottom: 3px solid #15803d; margin-bottom: 10mm; }
.cover .code { background: #15803d; color: #fff; font-weight: 700; letter-spacing: .09em; font-size: 9pt; padding: 4px 10px; border-radius: 5px; }
.cover p { max-width: 130mm; }
.mut { color: #5b6b60; }
.contents { page-break-after: always; }
.contents li { margin-bottom: 4px; list-style: none; }
.contents ul { padding: 0; }
/* The entries are links, but a printed page should not turn blue and
   underlined to say so. They inherit the surrounding type and stay clickable. */
.contents a { color: inherit; text-decoration: none; }
.topic { page-break-before: always; }
.speed { background: #fdf6e3; border-left: 3px solid #9a6a00; padding: 8px 11px; margin: 0 0 12px; }
/* A question keeps itself together, but only while it FITS. Once a question
   carries a full worked solution it can be taller than the space under a
   section heading, and "avoid" then pushed the whole thing to the next page,
   leaving three sections opening on a page holding nothing but their title and
   a speed tip. The parts that must not split are the option list and the
   solution box; the article as a whole may break between them. */
.q { border: 1px solid #d8e2da; border-radius: 6px; padding: 9px 11px; margin: 0 0 9px; }
.qtop { page-break-inside: avoid; page-break-after: avoid; }
.qh, .prompt { page-break-after: avoid; }
.opts, .pairs, .rawopts { page-break-inside: avoid; }
/* The options as the paper prints them: lettered, unmarked, uncoloured, so the
   question can be attempted before the verdicts below give it away. */
.rawopts { margin: 0 0 2px; padding-left: 20px; list-style: lower-alpha; }
.rawopts li { padding: 1.5px 0; }
.rawopts li::marker { color: #5b6b60; font-weight: 700; }
/* A question's diagram. currentColor in the SVG picks up the ink colour, so it
   prints as line art rather than as a grey block. */
.qfig { margin: 6px 0 8px; padding: 7px; border: 1px solid #d8e2da; border-radius: 5px; background: #fff; text-align: center; page-break-inside: avoid; }
.qfig svg { max-width: 78mm; height: auto; color: #1e2430; }
.qfig figcaption { font-size: 7pt; color: #5b6b60; margin-top: 4px; }
.blanklab { font-size: 6.6pt; letter-spacing: .08em; text-transform: uppercase; color: #5b6b60; margin: 5px 0 1px; }
/* The line that separates attempting from checking. */
.attemptgap { display: flex; align-items: center; gap: 8px; margin: 11px 0 7px; page-break-after: avoid; }
.attemptgap span { font-size: 6.6pt; letter-spacing: .1em; text-transform: uppercase; color: #5b6b60; white-space: nowrap; }
.attemptgap::before, .attemptgap::after { content: ''; flex: 1; height: 1px; background: #d8e2da; }
.qh { display: flex; gap: 8px; align-items: baseline; margin-bottom: 5px; flex-wrap: wrap; }
.qn { background: #16261c; color: #fff; font-size: 7.6pt; font-weight: 700; padding: 1px 7px; border-radius: 99px; }
.pill { font-size: 7pt; text-transform: uppercase; letter-spacing: .05em; padding: 1px 7px; border-radius: 99px; border: 1px solid #d8e2da; color: #5b6b60; }
.pill.easy { background: #eaf6ee; color: #0f5f2d; }
.pill.hard { background: #fdeceb; color: #b91c1c; }
.src { font-size: 7.8pt; color: #5b6b60; margin-left: auto; }
.rep { font-size: 8pt; color: #5b6b60; margin: 0 0 5px; }
.prompt { font-weight: 700; margin: 0 0 7px; }
.opts { list-style: none; margin: 0 0 7px; padding: 0; }
.opt { display: flex; gap: 7px; padding: 4px 7px; border-radius: 4px; margin-bottom: 3px; background: #fdeceb; }
.opt.right { background: #eaf6ee; }
.tick { font-weight: 700; color: #b91c1c; }
.opt.right .tick { color: #0f5f2d; }
.opt em { display: block; font-style: normal; font-size: 8.4pt; color: #5b6b60; margin-top: 2px; }
.exp { margin: 0; font-size: 8.9pt; border-left: 2.5px solid #15803d; padding-left: 9px; white-space: pre-line; }
.ans { margin: 0 0 7px; }
.pairs { width: 100%; border-collapse: collapse; margin-bottom: 7px; }
.pairs td { border-top: 1px solid #d8e2da; padding: 3px 6px; vertical-align: top; }
.frac { display: inline-flex; flex-direction: column; vertical-align: -0.55em; text-align: center; margin: 0 .22em; }
.frac span:first-child { padding: 0 .3em 1px; }
.frac span:last-child { padding: 1px .3em 0; border-top: 1.2px solid currentColor; }
sup { font-size: 0.72em; }
.wsol { border: 1.2px solid #15803d; border-radius: 6px; overflow: hidden; margin: 8px 0 0; page-break-inside: avoid; }
.wp { padding: 7px 10px; border-top: 1px solid #d8e2da; }
.wp:first-child { border-top: none; }
.wl { display: block; font-size: 6.8pt; letter-spacing: .09em; text-transform: uppercase; color: #0f5f2d; font-weight: 700; margin-bottom: 4px; }
.wp p { margin: 0 0 4px; }
.wg { background: #eaf6ee; }
.wg ul, .wsy { margin: 0 0 4px; padding-left: 15px; }
.wg li { font-family: "DejaVu Sans Mono", monospace; font-size: 8.4pt; }
.weq { font-family: "DejaVu Sans Mono", monospace; font-size: 10pt; font-weight: 700; text-align: center; padding: 5px 0; background: #fff; border-radius: 4px; }
.ws ol { margin: 0; padding-left: 18px; }
.ws li { font-family: "DejaVu Sans Mono", monospace; font-size: 8.6pt; padding: 1.5px 0; }
.wc { background: #fdf6e3; }
.wc .wl { color: #9a6a00; }
</style></head><body>
<div class="cover">
<span class="code">PHY121</span>
<h1>The Question Book</h1>
<p class="mut">General Physics II &middot; every question, solved and explained${today ? ` &middot; ${esc(today)}` : ''}</p>
<p>All <b>${total} questions</b> from the lecture slides, the reference sheets and both real tests. Grouped by topic, and within each topic ordered <b>easy first</b>, so the definitions come before the calculations that assume them.</p>
<p>Every question carries the source it came from. Where the same question was set twice it appears once and says where else it was asked. The answer is ticked, and every other option carries a line saying why it fails.</p>
</div>
<div class="contents"><h2><span class="tnum">C</span>Contents</h2><ul>${contents}</ul></div>
${body}
</body></html>`);

writeFileSync(join(HERE, 'question_book.toc.json'), `${JSON.stringify(tocEntries, null, 2)}\n`, 'utf8');

/*
 * Two counts that must agree, checked here rather than trusted.
 *
 * The printed book carried NO diagrams for months while the platform carried
 * them all, because this generator simply never looked at q.figure. Nothing
 * complained: the page count was plausible, the questions were all present, and
 * the only symptom was a question reading "the magnitude of the field
 * represented by" with nothing after it. A count that has to match turns that
 * into a build failure instead of a reader's problem.
 */
const expectedFigures = qs.filter((q) => q.figure?.svg).length;
if (figuresDrawn !== expectedFigures)
  throw new Error(
    `figures: ${expectedFigures} questions carry one but ${figuresDrawn} were drawn`
  );
if (total !== qs.length)
  throw new Error(`questions: ${qs.length} in the bank but ${total} reached the book`);
process.stderr.write(`  ${total} questions, ${expectedFigures} figures, ${tocEntries.length} topics\n`);
