/**
 * Bank gate. Runs before every build, so a broken or thin bank cannot deploy.
 *
 *     npm run validate
 *
 * Two jobs.
 *
 * 1. SCHEMA. Every question is well formed and answerable: unique id, a key that
 *    actually points at an option, dropdown choices that contain the right
 *    answer, no blank without an accepted answer. A question whose key names a
 *    missing option is unanswerable and would silently mark the student wrong
 *    forever, which is the worst failure this thing can have.
 *
 * 2. COVERAGE. This is the same forcing function the manual itself uses. Victor's
 *    standing instruction is that no single list, date, fact, acronym or author
 *    escapes, so every content-bearing slide of all five decks must be cited by
 *    at least one question's `slides`. A slide nothing asks about is a slide the
 *    student is never tested on.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA = join(HERE, '..', 'data', 'tmc221');

// Content slides per deck: title and closing "Thank You" slides carry nothing
// testable and are excluded. Matches qa_coverage.py in the manual build.
const REQUIRED = {
  L1: range(2, 20),
  L2: range(2, 19),
  L3: range(2, 15),
  L4: range(2, 19),
  L5: range(2, 19),
};

const MIN_PER_MODULE = 100;

const STYLES = ['mcq', 'multi', 'tf', 'match', 'cloze', 'gap'];
const DIFFS = ['easy', 'medium', 'hard'];
const FACETS = ['numbers', 'names', 'lists', 'wording'];
const FORMATS = ['word', 'words', 'number', 'percent', 'time', 'name', 'phrase'];

function range(a, b) {
  const out = [];
  for (let i = a; i <= b; i++) out.push(i);
  return out;
}

const problems = [];
const seenIds = new Set();

function check(cond, msg) {
  if (!cond) problems.push(msg);
}

function validate(q, where) {
  const at = `${where} [${q.id ?? '(no id)'}]`;
  check(typeof q.id === 'string' && q.id.length > 0, `${at}: missing id`);
  check(!seenIds.has(q.id), `${at}: duplicate id`);
  seenIds.add(q.id);
  check(Number.isInteger(q.module), `${at}: module must be a number`);
  check(Number.isInteger(q.lecture), `${at}: lecture must be a number`);
  check(
    Array.isArray(q.slides) && q.slides.length > 0,
    `${at}: needs at least one slide reference`
  );
  (q.slides ?? []).forEach((s) =>
    check(/^L[1-5] S\d{1,2}$/.test(s), `${at}: malformed slide ref ${JSON.stringify(s)}`)
  );
  check(STYLES.includes(q.style), `${at}: unknown style ${q.style}`);
  check(DIFFS.includes(q.difficulty), `${at}: unknown difficulty ${q.difficulty}`);
  check(Array.isArray(q.facets), `${at}: facets must be an array`);
  (q.facets ?? []).forEach((f) =>
    check(FACETS.includes(f), `${at}: unknown facet ${f}`)
  );
  check(typeof q.topic === 'string' && q.topic.length > 0, `${at}: missing topic`);
  check(typeof q.prompt === 'string' && q.prompt.length > 0, `${at}: missing prompt`);
  check(
    typeof q.explanation === 'string' && q.explanation.length > 10,
    `${at}: explanation missing or too thin to teach from`
  );

  if (q.style === 'mcq' || q.style === 'multi') {
    const ids = (q.options ?? []).map((o) => o.id);
    check(ids.length >= 3, `${at}: needs at least 3 options`);
    check(new Set(ids).size === ids.length, `${at}: duplicate option ids`);
    (q.options ?? []).forEach((o) =>
      check(
        typeof o.text === 'string' && o.text.trim().length > 0,
        `${at}: option ${o.id} has no text`
      )
    );
    if (q.style === 'mcq') {
      check(
        typeof q.answer === 'string' && ids.includes(q.answer),
        `${at}: answer ${JSON.stringify(q.answer)} is not one of the options`
      );
    } else {
      check(
        Array.isArray(q.answer) && q.answer.length >= 2,
        `${at}: a multiple-response needs at least 2 correct options`
      );
      (Array.isArray(q.answer) ? q.answer : []).forEach((a) =>
        check(ids.includes(a), `${at}: answer ${a} is not one of the options`)
      );
      check(
        (q.answer ?? []).length < ids.length,
        `${at}: every option is correct, so there is nothing to discriminate`
      );
    }
  }

  if (q.style === 'tf') {
    check(
      q.answer === 'true' || q.answer === 'false',
      `${at}: true/false answer must be the string "true" or "false"`
    );
  }

  if (q.style === 'match') {
    check(
      Array.isArray(q.pairs) && q.pairs.length >= 2,
      `${at}: a matching question needs at least 2 pairs`
    );
    const lefts = (q.pairs ?? []).map((p) => p.left);
    check(new Set(lefts).size === lefts.length, `${at}: duplicate left-hand items`);
    (q.pairs ?? []).forEach((p) =>
      check(
        typeof p.right === 'string' && p.right.trim().length > 0,
        `${at}: pair "${p.left}" has no right-hand label`
      )
    );
  }

  if (q.style === 'cloze' || q.style === 'gap') {
    const marks = [...q.prompt.matchAll(/\{\{(\d+)\}\}/g)].map((m) => Number(m[1]));
    check(marks.length > 0, `${at}: prompt has no {{n}} blank markers`);
    check(
      Array.isArray(q.blanks) && q.blanks.length === marks.length,
      `${at}: ${marks.length} markers in the prompt but ${
        (q.blanks ?? []).length
      } blanks defined`
    );
    marks.forEach((n, idx) =>
      check(n === idx + 1, `${at}: blank markers must run 1,2,3... in order`)
    );
    (q.blanks ?? []).forEach((b, i) => {
      check(
        Array.isArray(b.accept) && b.accept.length > 0,
        `${at}: blank ${i + 1} has no accepted answer`
      );
      check(
        Array.isArray(b.choices) && b.choices.length >= 3,
        `${at}: blank ${i + 1} needs at least 3 dropdown choices`
      );
      check(
        (b.choices ?? []).includes(b.accept?.[0]),
        `${at}: blank ${i + 1} dropdown does not contain its own answer "${b.accept?.[0]}"`
      );
      check(
        new Set(b.choices ?? []).size === (b.choices ?? []).length,
        `${at}: blank ${i + 1} has duplicate choices`
      );
      if (b.format !== undefined)
        check(FORMATS.includes(b.format), `${at}: blank ${i + 1} unknown format ${b.format}`);
      if (q.style === 'gap')
        check(
          b.format !== 'phrase',
          `${at}: blank ${i + 1} is a typed short answer, so it cannot be format "phrase"`
        );
    });
  }
}

// ---- load ----
const moduleFiles = readdirSync(DATA)
  .filter((f) => /^module\d+\.json$/.test(f))
  .sort();

const all = [];
const perModule = {};
for (const f of moduleFiles) {
  const items = JSON.parse(readFileSync(join(DATA, f), 'utf8'));
  check(Array.isArray(items), `${f}: expected a JSON array`);
  for (const q of items) validate(q, f);
  all.push(...items);
  const n = Number(f.match(/\d+/)[0]);
  perModule[n] = items.length;
  for (const q of items) {
    check(
      q.module === n,
      `${f} [${q.id}]: module field says ${q.module} but the file is module ${n}`
    );
  }
}

const papers = readdirSync(DATA).filter((f) => f.endsWith('-test.json'));
for (const f of papers) {
  const paper = JSON.parse(readFileSync(join(DATA, f), 'utf8'));
  check(typeof paper.id === 'string', `${f}: paper needs an id`);
  check(Array.isArray(paper.questions), `${f}: paper needs a questions array`);
  for (const q of paper.questions ?? []) validate(q, f);
  all.push(...(paper.questions ?? []));
}

// ---- coverage ----
const cited = new Set();
for (const q of all) for (const s of q.slides ?? []) cited.add(s);

const missing = [];
let requiredCount = 0;
for (const [deck, slides] of Object.entries(REQUIRED)) {
  for (const n of slides) {
    requiredCount += 1;
    if (!cited.has(`${deck} S${n}`)) missing.push(`${deck} S${n}`);
  }
}

// ---- report ----
console.log('BANK GATE');
console.log(`  questions loaded: ${all.length}`);
for (const [n, c] of Object.entries(perModule)) {
  const flag = c >= MIN_PER_MODULE ? '.' : 'x';
  console.log(`  ${flag} module ${n}: ${c} questions (minimum ${MIN_PER_MODULE})`);
  if (c < MIN_PER_MODULE)
    problems.push(`module ${n} has ${c} questions, under the ${MIN_PER_MODULE} minimum`);
}

const styleCounts = {};
const diffCounts = {};
const facetCounts = {};
for (const q of all) {
  styleCounts[q.style] = (styleCounts[q.style] ?? 0) + 1;
  diffCounts[q.difficulty] = (diffCounts[q.difficulty] ?? 0) + 1;
  for (const f of q.facets ?? []) facetCounts[f] = (facetCounts[f] ?? 0) + 1;
}
console.log(
  '  styles:',
  STYLES.map((s) => `${s} ${styleCounts[s] ?? 0}`).join(', ')
);
console.log(
  '  difficulty:',
  DIFFS.map((d) => `${d} ${diffCounts[d] ?? 0}`).join(', ')
);
console.log(
  '  facets:',
  FACETS.map((f) => `${f} ${facetCounts[f] ?? 0}`).join(', ')
);

// Every style the real test uses must be present, or the drill is not the exam.
for (const s of STYLES)
  check(
    (styleCounts[s] ?? 0) > 0,
    `no question anywhere uses style "${s}", which the real test does use`
  );
for (const f of FACETS)
  check((facetCounts[f] ?? 0) > 0, `no question carries the "${f}" facet`);

if (missing.length) {
  console.log(
    `  x slide coverage: ${missing.length} of ${requiredCount} content slides are never tested`
  );
  console.log('      ' + missing.join(', '));
  problems.push(`${missing.length} content slides are not covered by any question`);
} else {
  console.log(
    `  . slide coverage: all ${requiredCount} content slides of the five decks are tested`
  );
}

if (problems.length) {
  console.error(`\nBANK GATE FAILED: ${problems.length} problem(s)`);
  for (const p of problems.slice(0, 60)) console.error('  x ' + p);
  if (problems.length > 60) console.error(`  ... and ${problems.length - 60} more`);
  process.exit(1);
}
console.log('BANK GATE: pass');
