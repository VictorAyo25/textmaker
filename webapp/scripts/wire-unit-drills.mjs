/**
 * Put every authored question inside the lesson that teaches its unit.
 *
 *     node scripts/wire-unit-drills.mjs ins224
 *
 * A lesson already ends on the examiner's own test questions for its unit
 * (a drill block with pick: 'exam'). The questions authored from the ledger,
 * one or more for every fact in the course text, would otherwise live only in
 * the separate drill, where a reader following the dated plan never meets
 * them. This adds, to each lesson that teaches exactly one unit, a second drill
 * block naming that unit's authored questions by id, placed before the lesson's
 * closing lock-in. The ids are listed rather than the topic, so no test
 * question is asked twice (the gate refuses that). Idempotent: it replaces the
 * block it added last time.
 */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const code = process.argv[2];
if (!code) {
  console.error('usage: node scripts/wire-unit-drills.mjs <course dir>');
  process.exit(2);
}
const dir = join(dirname(fileURLToPath(import.meta.url)), '..', 'data', code);
const LABEL = 'Drill every fact in this unit';

const authored = [];
for (const f of readdirSync(dir).filter((f) => /^drill\d+[a-z]?\.json$/.test(f)))
  authored.push(...JSON.parse(readFileSync(join(dir, f), 'utf8')));

const file = join(dir, 'lessons.json');
const lessons = JSON.parse(readFileSync(file, 'utf8'));
let wired = 0;
for (const l of lessons) {
  l.blocks = l.blocks.filter((b) => !(b.kind === 'drill' && b.label === LABEL));
  if ((l.modules ?? []).length !== 1) continue;
  const unit = l.modules[0];
  // A unit taught by a lesson and ALSO by a practical keeps its drill on the
  // teaching lesson, the first one in the file.
  if (lessons.find((x) => (x.modules ?? []).length === 1 && x.modules[0] === unit) !== l) continue;
  const ids = authored.filter((q) => q.module === unit).map((q) => q.id);
  if (!ids.length) continue;
  const block = {
    kind: 'drill',
    label: LABEL,
    tag: `${ids.length} questions from the course text, every option explained`,
    pick: 'all',
    topics: [],
    ids,
  };
  const lock = l.blocks.findIndex((b) => b.kind === 'lockin');
  l.blocks.splice(lock === -1 ? l.blocks.length : lock, 0, block);
  wired += 1;
  console.log(`  ${l.slug.padEnd(18)} unit ${unit}: ${ids.length} questions`);
}
writeFileSync(file, JSON.stringify(lessons, null, 2) + '\n');
console.log(`  wired ${wired} lessons in data/${code}/lessons.json`);
