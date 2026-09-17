/**
 * Build the "Learn by doing" section of a course.
 *
 *     node scripts/build-doing.mjs ins224
 *
 * One lesson per module of the course text. Each lesson is a paper in two
 * parts, which is how the paper itself is shaped:
 *
 *   Part A  fifty objective questions on that module, the examiner's own test
 *           questions first, then the authored bank chosen for COVERAGE: at
 *           each step the question that tests the most facts nothing in the set
 *           has tested yet. So fifty questions reach further than fifty picked
 *           by hand would.
 *   Part B  the theory questions, each with the practical scenario the lecturer
 *           confirmed every question carries, and each answered TWICE: the
 *           answer to write in the hall, then the same ground taught from
 *           scratch in frames for a reader who has never read the course.
 *
 * Part B is authored, in data/<course>/doing/<set>.json. Part A is chosen here,
 * because a hand-picked fifty cannot be checked and this can: rerun it and the
 * same fifty come back.
 *
 * Idempotent. It replaces the lessons it wrote last time and adds each one to
 * its sitting in the dated plan, so the reading plan still covers every lesson.
 */
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));

const COURSES = {
  ins224: {
    part: 'Learn by doing',
    // After the practicals, before the past papers: teach, practise the skill,
    // then sit the whole module, then meet the real papers.
    insertBefore: 'paper-2526',
    size: 50,
    sets: [
      { slug: 'doing-m1', dir: 'm1', units: [1, 2, 3], planDate: '2026-09-15' },
      { slug: 'doing-m2', dir: 'm2', units: [4, 5, 6, 7], planDate: '2026-09-16' },
      { slug: 'doing-m3', dir: 'm3', units: [8, 9, 10], planDate: '2026-09-18' },
    ],
  },
};

const STYLE_ORDER = ['match', 'multi', 'mcq', 'tf'];
const isTest = (q) => (q.slides ?? []).some((s) => /^Test [12] Q/.test(s));

/**
 * The examiner's own questions first, in the order the tests set them, then a
 * greedy coverage fill: the question testing the most UNTESTED facts wins, ties
 * broken by the style that carries the most facts per question, then by id so
 * the choice is stable.
 */
function choose(pool, size) {
  const picked = pool.filter(isTest).sort((a, b) => {
    const n = (q) => Number((q.slides.find((s) => /^Test [12] Q/.test(s)) ?? '').match(/Q(\d+)/)?.[1] ?? 0);
    const t = (q) => (q.slides.some((s) => s.startsWith('Test 1')) ? 1 : 2);
    return t(a) - t(b) || n(a) - n(b);
  });
  const covered = new Set(picked.flatMap((q) => q.facts ?? []));
  const rest = pool.filter((q) => !isTest(q));
  while (picked.length < size && rest.length) {
    let best = null;
    let bestScore = -Infinity;
    for (const q of rest) {
      const fresh = (q.facts ?? []).filter((f) => !covered.has(f)).length;
      const score = fresh * 100 - STYLE_ORDER.indexOf(q.style);
      if (score > bestScore) {
        bestScore = score;
        best = q;
      }
    }
    picked.push(best);
    for (const f of best.facts ?? []) covered.add(f);
    rest.splice(rest.indexOf(best), 1);
  }
  return { picked, covered };
}

/** The blocks one authored theory question turns into. */
function questionBlocks(q, n) {
  const word = ['One', 'Two', 'Three', 'Four', 'Five'][n - 1] ?? String(n);
  const blocks = [{ kind: 'heading', text: `Question ${word}: ${q.heading}` }];
  if (q.scenario.printed)
    blocks.push({
      kind: 'asprinted',
      label: 'The scenario, as the course text prints it',
      tag: q.scenario.tag,
      src: 'the course text, unedited',
      printed: `<div class="asprinted" data-src="${q.scenario.src}">${q.scenario.text}</div>`,
    });
  else
    blocks.push({
      kind: 'teach',
      label: 'The scenario',
      tag: q.scenario.tag,
      html: q.scenario.text,
    });
  blocks.push({ kind: 'teach', label: 'What you are asked', tag: q.marks, html: q.asked });
  blocks.push({
    kind: 'recall',
    label: 'Break it down first',
    tag: 'before you write a word',
    question: q.breakdown.question,
    answer: q.breakdown.answer,
  });
  blocks.push({
    kind: 'worked',
    mode: 'model',
    label: 'Part 1: the answer you write in the hall',
    tag: 'write yours first, then open this',
    problem: q.exam.problem,
    answer: q.exam.answer,
  });
  blocks.push({
    kind: 'frames',
    label: 'Part 2: the same question, taught from scratch',
    tag: 'for a reader who has never read the course',
    frames: q.frames,
  });
  return blocks;
}

function build(code) {
  const cfg = COURSES[code];
  if (!cfg) throw new Error(`no Learn by doing config for ${code}`);
  const dir = join(HERE, '..', 'data', code);
  const bank = [];
  for (const f of readdirSync(dir).filter((f) => /^(drill\d+[a-z]?|test\d+)\.json$/.test(f)))
    bank.push(...JSON.parse(readFileSync(join(dir, f), 'utf8')));

  const lessons = JSON.parse(readFileSync(join(dir, 'lessons.json'), 'utf8'));
  const made = [];
  for (const set of cfg.sets) {
    const authored = JSON.parse(readFileSync(join(dir, 'doing', `${set.dir}.json`), 'utf8'));
    const pool = bank.filter((q) => set.units.includes(q.module));
    const { picked, covered } = choose(pool, cfg.size);
    const tests = picked.filter(isTest).length;
    const blocks = [
      { kind: 'teach', label: 'How to sit this', tag: 'read this first', html: authored.intro },
      {
        kind: 'drill',
        label: `Part A: ${cfg.size} objective questions on this module`,
        tag: `${tests} of them the examiner's own test questions, then ${
          cfg.size - tests
        } more chosen to reach ${covered.size} facts`,
        pick: 'all',
        topics: [],
        ids: picked.map((q) => q.id),
      },
      { kind: 'heading', text: 'Part B: the theory questions, each with its practical' },
      ...authored.questions.flatMap((q, i) => questionBlocks(q, i + 1)),
      { kind: 'lockin', big: authored.lockin.big, sub: authored.lockin.sub },
    ];
    made.push({
      slug: set.slug,
      part: cfg.part,
      kick: authored.kick,
      title: authored.title,
      lead: authored.lead,
      minutes: authored.minutes,
      modules: [],
      // Deliberate revision: every question here was met in the lesson that
      // taught it, and is asked again as a paper. The gate's one-lesson-per
      // question rule is about the TEACHING sequence, so it skips these.
      revision: true,
      blocks,
    });
    console.log(
      `  ${set.slug.padEnd(9)} Part A ${picked.length} questions (${tests} real test), ${
        covered.size
      } facts; Part B ${authored.questions.length} theory questions, ${authored.questions.reduce(
        (t, q) => t + q.frames.length,
        0
      )} frames`
    );
  }

  const kept = lessons.filter((l) => !cfg.sets.some((s) => s.slug === l.slug));
  const at = kept.findIndex((l) => l.slug === cfg.insertBefore);
  kept.splice(at === -1 ? kept.length : at, 0, ...made);
  writeFileSync(join(dir, 'lessons.json'), JSON.stringify(kept, null, 2) + '\n');

  // The dated plan must cover every lesson, so each set joins the sitting that
  // studies its module.
  const planFile = join(dir, 'plan.json');
  if (existsSync(planFile)) {
    const plan = JSON.parse(readFileSync(planFile, 'utf8'));
    for (const set of cfg.sets) {
      const sitting = plan.find((s) => s.date === set.planDate);
      if (!sitting) throw new Error(`no sitting dated ${set.planDate} for ${set.slug}`);
      if (!sitting.lessons.includes(set.slug)) sitting.lessons.push(set.slug);
    }
    writeFileSync(planFile, JSON.stringify(plan, null, 2) + '\n');
  }
  console.log(`  wrote ${made.length} lessons into data/${code}/lessons.json`);
}

build(process.argv[2] ?? 'ins224');
