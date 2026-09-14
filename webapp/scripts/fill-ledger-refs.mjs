/**
 * Fill in each authored question's provenance and unit from the ledger facts
 * it names, so neither can be mistyped.
 *
 *     node scripts/fill-ledger-refs.mjs ins224
 *
 * A question written from the ledger declares `facts`. Its `slides` must then
 * cite every one of those facts' pages (the gate refuses a fact tested without
 * its source), and its `module` is the unit those facts come from. Typing both
 * by hand across hundreds of questions is where errors come from; deriving them
 * cannot drift. A question that already carries slides keeps them, with any
 * missing fact page appended. Run BY HAND after authoring; idempotent.
 */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const code = process.argv[2];
if (!code) {
  console.error('usage: node scripts/fill-ledger-refs.mjs <course dir, e.g. ins224> [source dir]');
  process.exit(2);
}
const dir = join(dirname(fileURLToPath(import.meta.url)), '..', 'data', code);
// Drafts may be written elsewhere and brought in: read drill files from the
// source directory when one is given, and always write into data/<code>.
const src = process.argv[3] ?? dir;
const ledger = new Map();
for (const f of readdirSync(join(dir, 'ledger')).filter((f) => f.endsWith('.json')))
  for (const e of JSON.parse(readFileSync(join(dir, 'ledger', f), 'utf8'))) ledger.set(e.id, e);

let touched = 0;
const problems = [];
for (const f of readdirSync(src).filter((f) => /^drill\d+[a-z]?\.json$/.test(f))) {
  const qs = JSON.parse(readFileSync(join(src, f), 'utf8'));
  for (const q of qs) {
    const facts = (q.facts ?? []).map((id) => ledger.get(id) ?? (problems.push(`${f} ${q.id}: no fact ${id}`), null));
    if (facts.some((x) => !x)) continue;
    const refs = [...new Set(facts.map((x) => x.ref))];
    const slides = [...(q.slides ?? [])];
    for (const r of refs) if (!slides.includes(r)) slides.push(r);
    const units = [...new Set(facts.map((x) => x.topic))];
    if (units.length > 1 && q.module === undefined)
      problems.push(`${f} ${q.id}: facts span units ${units.join(', ')}; set module by hand`);
    const ordered = { id: q.id, module: q.module ?? units[0], slides, ...q };
    ordered.slides = slides;
    ordered.module = q.module ?? units[0];
    Object.assign(q, ordered);
    touched += 1;
  }
  // re-key so id, module and slides lead, as in every other bank file
  const out = qs.map(({ id, module, slides, ...rest }) => ({ id, module, slides, ...rest }));
  writeFileSync(join(dir, f), JSON.stringify(out, null, 1) + '\n');
}
if (problems.length) {
  for (const p of problems) console.error('  x ' + p);
  process.exit(1);
}
console.log(`  filled ${touched} questions in data/${code}`);
