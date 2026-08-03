/**
 * Bank gate. Runs before every build, so a broken or thin bank cannot deploy.
 *
 *     npm run validate
 *
 * Four jobs, applied per course from the COURSES table below.
 *
 * 1. SCHEMA. Every question is well formed and answerable: unique id, a key that
 *    actually points at an option, dropdown choices that contain the right
 *    answer, no blank without an accepted answer. A question whose key names a
 *    missing option is unanswerable and would silently mark the student wrong
 *    forever, which is the worst failure this thing can have.
 *
 * 2. COVERAGE. The forcing function the manuals themselves use. For TMC221 that
 *    is slide coverage: every content-bearing slide of all five decks must be
 *    cited by at least one question, because a slide nothing asks about is a
 *    slide the student is never tested on. For IFT222 it is question coverage:
 *    all 120 objective questions from both tests must be present, exactly once
 *    each, with no gap and no duplicate.
 *
 * 3. THE KEY. IFT222 questions are cross-checked, letter by letter, against the
 *    answer key transcribed from the original test screenshots and held here
 *    independently of the JSON. Two transcriptions that disagree fail the build
 *    rather than shipping a wrong answer.
 *
 * 4. THE VERDICTS. Where a course explains its options, EVERY option must carry
 *    a verdict: why the key is the key, and what is wrong with each of the
 *    others. Half-explained questions do not ship.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA = join(HERE, '..', 'data');

const STYLES = ['mcq', 'multi', 'tf', 'match', 'cloze', 'gap'];
const DIFFS = ['easy', 'medium', 'hard'];
const FACETS = ['numbers', 'names', 'lists', 'wording'];
const FORMATS = ['word', 'words', 'number', 'percent', 'time', 'name', 'phrase'];

function range(a, b) {
  const out = [];
  for (let i = a; i <= b; i++) out.push(i);
  return out;
}

/**
 * The IFT222 answer key, transcribed from the test screenshots alongside the
 * bank and kept here as an independent second copy. Index 0 is question 1.
 */
const IFT_KEY = {
  'Test 1': (
    'cbbcbcabca' +
    'bbccacdcdb' +
    'dcdadbdbad' +
    'dcdabddadd' +
    'dcadacdaad' +
    'bdcaddaddb'
  ).split(''),
  'Test 2': (
    'bbabacdcdb' +
    'bbbbadabab' +
    'caabbadbbd' +
    'ddbabbbdaa' +
    'cdbbbddcab' +
    'dbdbadbcdb'
  ).split(''),
};

const COURSES = [
  {
    code: 'TMC221',
    dir: 'tmc221',
    // Content slides per deck: title and closing "Thank You" slides carry
    // nothing testable and are excluded. Matches qa_coverage.py in the build.
    slideRef: /^L[1-5] S\d{1,2}$/,
    slideRefHelp: 'like "L2 S9"',
    requireLecture: true,
    minPerModule: 100,
    requireEveryStyle: true,
    coverage: {
      kind: 'slides',
      required: Object.entries({
        L1: range(2, 20),
        L2: range(2, 19),
        L3: range(2, 15),
        L4: range(2, 19),
        L5: range(2, 19),
      }).flatMap(([deck, slides]) => slides.map((n) => `${deck} S${n}`)),
      noun: 'content slides of the five decks',
    },
  },
  {
    code: 'IFT222',
    dir: 'ift222',
    slideRef: /^Test [12] Q\d{1,2}$/,
    slideRefHelp: 'like "Test 1 Q16"',
    requireLecture: false,
    minPerModule: 5,
    // The objective tests are pure MCQ, so demanding all six styles here would
    // be demanding the drill differ from the exam.
    requireEveryStyle: false,
    requireWhy: true,
    coverage: {
      kind: 'exactly-once',
      required: [
        ...range(1, 60).map((n) => `Test 1 Q${n}`),
        ...range(1, 60).map((n) => `Test 2 Q${n}`),
      ],
      noun: 'objective questions across the two tests',
    },
    key: IFT_KEY,
    // The crash course, converted by scripts/import-crash.mjs. Every drill topic
    // must be taught by some lesson: a topic with questions and no lesson is a
    // hole a reader falls into.
    lessons: 'lessons.json',
  },
];

const problems = [];

function check(cond, msg) {
  if (!cond) problems.push(msg);
}

function validate(q, where, cfg, seenIds) {
  const at = `${cfg.code} ${where} [${q.id ?? '(no id)'}]`;
  check(typeof q.id === 'string' && q.id.length > 0, `${at}: missing id`);
  check(!seenIds.has(q.id), `${at}: duplicate id`);
  seenIds.add(q.id);
  check(Number.isInteger(q.module), `${at}: module must be a number`);
  if (cfg.requireLecture)
    check(Number.isInteger(q.lecture), `${at}: lecture must be a number`);
  check(
    Array.isArray(q.slides) && q.slides.length > 0,
    `${at}: needs at least one provenance reference`
  );
  (q.slides ?? []).forEach((s) =>
    check(
      cfg.slideRef.test(s),
      `${at}: malformed provenance ref ${JSON.stringify(s)}, expected ${cfg.slideRefHelp}`
    )
  );
  check(STYLES.includes(q.style), `${at}: unknown style ${q.style}`);
  check(DIFFS.includes(q.difficulty), `${at}: unknown difficulty ${q.difficulty}`);
  check(Array.isArray(q.facets) && q.facets.length > 0, `${at}: needs at least one facet`);
  (q.facets ?? []).forEach((f) => check(FACETS.includes(f), `${at}: unknown facet ${f}`));
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

    // Every option explained, or none. A partly filled block is worse than an
    // absent one, because the reader assumes the silent options were fine.
    if (cfg.requireWhy || q.why) {
      check(
        q.why && typeof q.why === 'object',
        `${at}: no per-option verdicts, so a reader is never told why the other options fail`
      );
      for (const id of ids)
        check(
          typeof q.why?.[id] === 'string' && q.why[id].trim().length > 15,
          `${at}: option ${id} has no verdict explaining why it is right or wrong`
        );
      for (const id of Object.keys(q.why ?? {}))
        check(ids.includes(id), `${at}: verdict for option ${id}, which does not exist`);
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

/**
 * The crash course.
 *
 * Lessons are converted from the manual, so the words are already gated there.
 * What has to be checked HERE is the conversion and the wiring: that no lesson
 * lost its teaching, that no programmed frame asks a question the reader is
 * never given the answer to, and that every drill topic is actually taught by
 * some lesson.
 */
function checkLessons(cfg, dir, bankModules) {
  const path = join(dir, cfg.lessons);
  const lessons = JSON.parse(readFileSync(path, 'utf8'));
  const slugs = new Set();
  const taught = new Set();
  let frames = 0;
  let recalls = 0;
  let worked = 0;

  check(Array.isArray(lessons) && lessons.length > 0, `${cfg.code}: ${cfg.lessons} is empty`);

  for (const l of lessons) {
    const at = `${cfg.code} lesson [${l.slug ?? '(no slug)'}]`;
    check(/^[a-z0-9-]+$/.test(l.slug ?? ''), `${at}: slug must be url-safe lower case`);
    check(!slugs.has(l.slug), `${at}: duplicate slug`);
    slugs.add(l.slug);
    check(Boolean(l.title), `${at}: no title`);
    check(Boolean(l.part), `${at}: no part, so the index cannot group it`);
    check((l.lead ?? '').length > 20, `${at}: lead missing or too thin`);
    check(Number.isFinite(l.minutes) && l.minutes > 0, `${at}: needs a sitting time`);
    check((l.blocks ?? []).length > 0, `${at}: no blocks, the conversion dropped it`);

    for (const m of l.modules ?? []) {
      check(bankModules.has(m), `${at}: teaches topic ${m}, which has no questions`);
      taught.add(m);
    }

    for (const [i, b] of (l.blocks ?? []).entries()) {
      const where = `${at} block ${i} (${b.kind})`;
      if (b.kind === 'frames') {
        check((b.frames ?? []).length >= 2, `${where}: fewer than 2 frames`);
        frames += (b.frames ?? []).length;
        (b.frames ?? []).forEach((f, j) => {
          check(Boolean((f.teach ?? '').trim()), `${where}: frame ${j + 1} has no teaching text`);
          // A question with nothing after it is a reader left hanging: the check
          // that answers frame j lives at the head of frame j + 1.
          if (f.ask && j === b.frames.length - 1)
            check(false, `${where}: the last frame asks a question nothing answers`);
        });
      } else if (b.kind === 'worked') {
        worked += 1;
        check(
          Boolean(b.working || b.answer),
          `${where}: nothing to reveal, so the worked example teaches nothing`
        );
        check(['model', 'example'].includes(b.mode), `${where}: unknown mode ${b.mode}`);
      } else if (b.kind === 'recall') {
        recalls += 1;
        check(Boolean(b.question), `${where}: no question`);
        check(Boolean(b.answer), `${where}: no answer, so it cannot be self-marked`);
      } else if (['rules', 'trap', 'teach', 'prose'].includes(b.kind)) {
        check(Boolean((b.html ?? '').trim()), `${where}: empty body`);
      } else if (b.kind === 'asprinted') {
        check(Boolean((b.printed ?? '').trim()), `${where}: no printed question text`);
      }

      // House style, with the exam's own words exempt: an AS PRINTED block is
      // evidence and is quoted exactly, dashes and all.
      if (b.kind !== 'asprinted')
        for (const v of Object.values(b))
          if (typeof v === 'string' && /[—–]/.test(v))
            problems.push(`${where}: em or en dash in "${v.slice(0, 60)}..."`);
    }
  }

  const untaught = [...bankModules].filter((m) => !taught.has(m)).sort((a, b) => a - b);
  console.log(
    `    ${untaught.length ? 'x' : '.'} crash course: ${lessons.length} lessons, ${frames} frames, ${worked} worked, ${recalls} recalls, ${
      untaught.length ? `topics never taught: ${untaught.join(', ')}` : 'every topic taught'
    }`
  );
  check(
    untaught.length === 0,
    `${cfg.code}: topics ${untaught.join(', ')} have questions but no lesson teaches them`
  );
}

/** House style, carried over from the manuals: no em dashes, no en dashes. */
function houseStyle(q, cfg) {
  const texts = [
    q.prompt,
    q.explanation,
    ...(q.options ?? []).map((o) => o.text),
    ...Object.values(q.why ?? {}),
  ];
  for (const t of texts)
    if (/[—–]/.test(String(t)))
      problems.push(`${cfg.code} [${q.id}]: em or en dash in "${String(t).slice(0, 60)}..."`);
}

console.log('BANK GATE');
let grandTotal = 0;

for (const cfg of COURSES) {
  const dir = join(DATA, cfg.dir);
  const seenIds = new Set();
  const all = [];
  const perModule = {};

  const moduleFiles = readdirSync(dir)
    .filter((f) => /^module\d+\.json$/.test(f))
    .sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));

  for (const f of moduleFiles) {
    const items = JSON.parse(readFileSync(join(dir, f), 'utf8'));
    check(Array.isArray(items), `${cfg.code} ${f}: expected a JSON array`);
    for (const q of items) {
      validate(q, f, cfg, seenIds);
      houseStyle(q, cfg);
    }
    all.push(...items);
    const n = Number(f.match(/\d+/)[0]);
    perModule[n] = items.length;
    for (const q of items)
      check(
        q.module === n,
        `${cfg.code} ${f} [${q.id}]: module field says ${q.module} but the file is module ${n}`
      );
  }

  for (const f of readdirSync(dir).filter((f) => f.endsWith('-test.json'))) {
    const paper = JSON.parse(readFileSync(join(dir, f), 'utf8'));
    check(typeof paper.id === 'string', `${cfg.code} ${f}: paper needs an id`);
    check(Array.isArray(paper.questions), `${cfg.code} ${f}: paper needs a questions array`);
    for (const q of paper.questions ?? []) {
      validate(q, f, cfg, seenIds);
      houseStyle(q, cfg);
    }
    all.push(...(paper.questions ?? []));
  }

  grandTotal += all.length;
  console.log(`\n  ${cfg.code}: ${all.length} questions in ${moduleFiles.length} files`);

  for (const [n, c] of Object.entries(perModule)) {
    const flag = c >= cfg.minPerModule ? '.' : 'x';
    console.log(`    ${flag} group ${n}: ${c} questions (minimum ${cfg.minPerModule})`);
    if (c < cfg.minPerModule)
      problems.push(
        `${cfg.code} group ${n} has ${c} questions, under the ${cfg.minPerModule} minimum`
      );
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
    '    styles:',
    STYLES.filter((s) => styleCounts[s])
      .map((s) => `${s} ${styleCounts[s]}`)
      .join(', ')
  );
  console.log('    difficulty:', DIFFS.map((d) => `${d} ${diffCounts[d] ?? 0}`).join(', '));
  console.log('    facets:', FACETS.map((f) => `${f} ${facetCounts[f] ?? 0}`).join(', '));

  if (cfg.requireEveryStyle)
    for (const s of STYLES)
      check(
        (styleCounts[s] ?? 0) > 0,
        `${cfg.code}: no question anywhere uses style "${s}", which the real test does use`
      );
  for (const d of DIFFS)
    check(
      (diffCounts[d] ?? 0) > 0,
      `${cfg.code}: no "${d}" question, so the difficulty mix cannot be honoured`
    );
  for (const f of FACETS)
    check((facetCounts[f] ?? 0) > 0, `${cfg.code}: no question carries the "${f}" facet`);

  // ---- coverage ----
  const cites = new Map();
  for (const q of all)
    for (const s of q.slides ?? []) cites.set(s, (cites.get(s) ?? 0) + 1);

  const missing = cfg.coverage.required.filter((r) => !cites.has(r));
  if (missing.length) {
    console.log(
      `    x coverage: ${missing.length} of ${cfg.coverage.required.length} ${cfg.coverage.noun} are never tested`
    );
    console.log('        ' + missing.join(', '));
    problems.push(
      `${cfg.code}: ${missing.length} ${cfg.coverage.noun} are not covered by any question`
    );
  } else {
    console.log(
      `    . coverage: all ${cfg.coverage.required.length} ${cfg.coverage.noun} are tested`
    );
  }

  if (cfg.coverage.kind === 'exactly-once') {
    const dupes = cfg.coverage.required.filter((r) => (cites.get(r) ?? 0) > 1);
    check(
      dupes.length === 0,
      `${cfg.code}: ${dupes.join(', ')} appear more than once, so a paper would repeat a question`
    );
    const strays = [...cites.keys()].filter((k) => !cfg.coverage.required.includes(k));
    check(
      strays.length === 0,
      `${cfg.code}: provenance refs outside the two tests: ${strays.join(', ')}`
    );
    if (!dupes.length && !strays.length)
      console.log('    . coverage: each one cited exactly once, no duplicates, no strays');
  }

  // ---- the key ----
  if (cfg.key) {
    let checked = 0;
    let wrong = 0;
    for (const q of all) {
      for (const ref of q.slides ?? []) {
        const m = ref.match(/^(Test [12]) Q(\d+)$/);
        if (!m) continue;
        const expected = cfg.key[m[1]]?.[Number(m[2]) - 1];
        if (!expected) continue;
        checked += 1;
        if (q.answer !== expected) {
          wrong += 1;
          problems.push(
            `${cfg.code} [${q.id}] ${ref}: bank says "${q.answer}" but the transcribed key says "${expected}"`
          );
        }
      }
    }
    console.log(
      `    ${wrong ? 'x' : '.'} answer key: ${checked} answers cross-checked against the original transcription${
        wrong ? `, ${wrong} disagree` : ', all agree'
      }`
    );
  }

  if (cfg.lessons) checkLessons(cfg, dir, new Set(Object.keys(perModule).map(Number)));

  if (cfg.requireWhy) {
    const explained = all.filter(
      (q) => q.why && (q.options ?? []).every((o) => q.why[o.id])
    ).length;
    console.log(
      `    ${explained === all.length ? '.' : 'x'} verdicts: ${explained} of ${all.length} questions explain every option`
    );
  }
}

console.log(`\n  total across all courses: ${grandTotal} questions`);

if (problems.length) {
  console.error(`\nBANK GATE FAILED: ${problems.length} problem(s)`);
  for (const p of problems.slice(0, 60)) console.error('  x ' + p);
  if (problems.length > 60) console.error(`  ... and ${problems.length - 60} more`);
  process.exit(1);
}
console.log('\nBANK GATE: pass');
