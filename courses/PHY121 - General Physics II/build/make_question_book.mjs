/**
 * The PHY121 question book, as a standalone HTML page ready for Chromium.
 *
 *   node make_question_book.mjs > question_book.html
 *
 * Same data as the platform page, same ordering, same labels. It reads the
 * bank directly rather than importing the app, so the manual can be built
 * without a running server.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA = join(HERE, '..', '..', '..', 'webapp', 'data', 'phy121');

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

/** Carets to real superscripts, and "a over b" to a drawn fraction. */
const sci = (raw) => {
  let s = esc(raw).replace(/\^(-?\d+)/g, (_, d) => `<sup>${d}</sup>`);
  if ((s.split(' over ').length) === 2) {
    const T = '[A-Za-z0-9εμθΦλσρτπΔ₀₁₂₃₄₅₆₇₈₉²³⁻<>\\/\\w()\\s-]';
    const re = new RegExp(
      `(${T}+?)\\s+over\\s+((?:${T}|\\.(?=\\d))+?)(?=[,;]|\\.(?!\\d)|\\s+(?:where|which|and|so|if|is|means|gives|equals|then)\\b|$)`
    );
    s = s.replace(re, (_, a, b) => `<span class="frac"><span>${a.trim()}</span><span>${b.trim()}</span></span>`);
  }
  return s;
};

const sourceOf = (q) => {
  const t = q.slides ?? [];
  const test = t.find((x) => /^Test [12] Q/.test(x));
  if (test) return `The real ${test.replace(/^Test (\d) Q(\d+)$/, 'test $1, question $2')}`;
  const sl = t.find((x) => /^M\d+ S\d+/.test(x));
  if (sl) {
    const m = /^M(\d+) S(\d+)/.exec(sl);
    return `Lecture slides, module ${m[1]}, slide ${m[2]}`;
  }
  const r = t.find((x) => /^Ref R\./.test(x));
  if (r) return `Reference sheet ${r.replace('Ref ', '')}`;
  return t.join(', ') || 'Authored for this course';
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

for (const [num, title] of TOPICS) {
  const mine = qs
    .filter((q) => q.module === num)
    .sort((a, b) => (RANK[a.difficulty] ?? 1) - (RANK[b.difficulty] ?? 1));
  if (!mine.length) continue;
  total += mine.length;
  contents += `<li><b>${num}. ${esc(title)}</b> <span class="mut">${mine.length} questions</span></li>`;

  body += `<section class="topic"><h2><span class="tnum">${num}</span>${esc(title)}</h2>`;
  if (SPEED[num]) body += `<p class="speed"><b>Speed tip.</b> ${esc(SPEED[num])}</p>`;

  mine.forEach((q, i) => {
    const ans = Array.isArray(q.answer) ? q.answer : [q.answer];
    body += `<article class="q"><div class="qh"><span class="qn">${num}.${i + 1}</span>`;
    body += `<span class="pill ${q.difficulty}">${q.difficulty}</span>`;
    body += `<span class="src">${esc(sourceOf(q))}</span></div>`;
    if (repeat.get(q.id))
      body += `<p class="rep"><b>Asked twice.</b> Also set as: ${esc(repeat.get(q.id))}.</p>`;
    body += `<p class="prompt">${sci(q.prompt)}</p>`;

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
      body += `<p class="ans">Answer: <b>${esc(ans.join(', '))}</b></p>`;
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
.topic { page-break-before: always; }
.speed { background: #fdf6e3; border-left: 3px solid #9a6a00; padding: 8px 11px; margin: 0 0 12px; }
.q { border: 1px solid #d8e2da; border-radius: 6px; padding: 9px 11px; margin: 0 0 9px; page-break-inside: avoid; }
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
