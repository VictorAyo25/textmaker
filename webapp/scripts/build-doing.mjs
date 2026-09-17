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
 *   Part B  the written questions, in whatever shape THIS paper sets them: INS224
 *           pairs every theory question with a practical, IFT222 and COS221 carry
 *           past questions only. Each is answered TWICE: the answer to write in
 *           the hall, then the same ground taught from scratch in frames, for a
 *           reader who has never read the course.
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
    partBHeading: 'Part B: the theory questions, each with its practical',
    part: 'Learn by doing',
    // After the practicals, before the past papers: teach, practise the skill,
    // then sit the whole module, then meet the real papers.
    insertBefore: 'paper-2526',
    size: 50,
    // What counts as a question the examiner actually set, which goes first.
    examTag: /^Test [12] Q/,
    examNoun: "the examiner's own test questions",
    sets: [
      { slug: 'doing-m1', dir: 'm1', units: [1, 2, 3], planAfter: 'practical-one' },
      { slug: 'doing-m2', dir: 'm2', units: [4, 5, 6, 7], planAfter: 'practical-two' },
      { slug: 'doing-m3', dir: 'm3', units: [8, 9, 10], planAfter: 'cram' },
    ],
  },
  ift222: {
    partBHeading: 'Part B: every past question the examiner has set on this topic',
    part: 'Learn by doing',
    insertBefore: 'final-paper',
    // Capped rather than exhaustive: this bank holds 1,245 questions over twelve
    // topics, and eighty chosen for coverage is a sitting. The rest stay in the
    // drill, which is where a reader goes for volume.
    size: 80,
    // This course files its bank by lecture deck and manual module, not by drill.
    bank: /^(deck|module)\d+[a-z]?\.json$/,
    examTag: /^Test [12] Q/,
    examNoun: "the examiner's own test questions",
    sets: [
      { slug: 'doing-m1', dir: 'm1', units: [1], planAfter: 'big-picture' },
      { slug: 'doing-m2', dir: 'm2', units: [2], planAfter: 'big-picture' },
      { slug: 'doing-m3', dir: 'm3', units: [3], planAfter: 'numbers' },
      { slug: 'doing-m4', dir: 'm4', units: [4], planAfter: 'signed' },
      { slug: 'doing-m5', dir: 'm5', units: [5], planAfter: 'ieee' },
      { slug: 'doing-m6', dir: 'm6', units: [6], planAfter: 'instructions' },
      { slug: 'doing-m7', dir: 'm7', units: [7], planAfter: 'addressing' },
      { slug: 'doing-m8', dir: 'm8', units: [8], planAfter: 'memory' },
      { slug: 'doing-m9', dir: 'm9', units: [9], planAfter: 'performance' },
      { slug: 'doing-m10', dir: 'm10', units: [10], planAfter: 'image' },
      { slug: 'doing-m11', dir: 'm11', units: [11], planAfter: 'memory' },
      { slug: 'doing-m12', dir: 'm12', units: [12], planAfter: 'pipelining' },
    ],
  },
  cos221: {
    partBHeading: 'Part B: the past questions on this topic, from both papers',
    part: 'Learn by doing',
    insertBefore: 'paper-2526',
    size: 50,
    examTag: /^Manual O\./,
    examNoun: "from the manual's objective sections",
    sets: [
      { slug: 'doing-m1', dir: 'm1', units: [1], planAfter: 'first-program' },
      { slug: 'doing-m2', dir: 'm2', units: [2], planAfter: 'types' },
      { slug: 'doing-m3', dir: 'm3', units: [3], planAfter: 'loops' },
      { slug: 'doing-m4', dir: 'm4', units: [4], planAfter: 'methods' },
      { slug: 'doing-m5', dir: 'm5', units: [5], planAfter: 'classes' },
      { slug: 'doing-m6', dir: 'm6', units: [6], planAfter: 'strings' },
      { slug: 'doing-m7', dir: 'm7', units: [7], planAfter: 'arrays' },
      { slug: 'doing-m8', dir: 'm8', units: [8], planAfter: 'recursion' },
      { slug: 'doing-m9', dir: 'm9', units: [9], planAfter: 'exceptions' },
    ],
  },
  csc241: {
    partBHeading: 'Part B: the written questions, in the shape this paper sets them',
    part: 'Learn by doing',
    insertBefore: 'paper-2526',
    size: 50,
    // This bank's objective half came from the manual's own objective sections,
    // which is the closest thing the course has to a set paper, so those lead.
    examTag: /^Manual O\./,
    examNoun: "from the manual's objective sections",
    sets: [
      { slug: 'doing-m1', dir: 'm1', units: [1], planAfter: 'sets-dicts' },
      { slug: 'doing-m2', dir: 'm2', units: [2], planAfter: 'sets-dicts' },
      { slug: 'doing-m3', dir: 'm3', units: [3], planAfter: 'sets-dicts' },
      { slug: 'doing-m4', dir: 'm4', units: [4], planAfter: 'databases' },
      { slug: 'doing-m5', dir: 'm5', units: [5], planAfter: 'databases' },
    ],
  },
};

const STYLE_ORDER = ['match', 'multi', 'mcq', 'tf'];

/**
 * What a question covers, for the greedy fill. A course with a fact ledger says
 * so itself; one without is spread across its provenance instead, so the fifty
 * still reach every lesson rather than piling into the first few.
 */
const keysOf = (q) => ((q.facts ?? []).length ? q.facts : (q.slides ?? []));

/**
 * The examiner's own questions first, in the order the tests set them, then a
 * greedy coverage fill: the question testing the most UNTESTED facts wins, ties
 * broken by the style that carries the most facts per question, then by id so
 * the choice is stable.
 */
function choose(pool, size, cfg) {
  const isExam = (q) => (q.slides ?? []).some((s) => cfg.examTag.test(s));
  const picked = pool.filter(isExam).sort((a, b) => {
    const at = (q) => (q.slides ?? []).find((s) => cfg.examTag.test(s)) ?? '';
    const num = (q) => (at(q).match(/(\d+)\D*$/) ?? [])[1] ?? 0;
    return at(a).localeCompare(at(b)) || Number(num(a)) - Number(num(b));
  });
  const covered = new Set(picked.flatMap(keysOf));
  const rest = pool.filter((q) => !isExam(q));
  while (picked.length < size && rest.length) {
    let best = null;
    let bestScore = -Infinity;
    for (const q of rest) {
      const fresh = keysOf(q).filter((f) => !covered.has(f)).length;
      const score = fresh * 100 - STYLE_ORDER.indexOf(q.style);
      if (score > bestScore) {
        bestScore = score;
        best = q;
      }
    }
    picked.push(best);
    for (const f of keysOf(best)) covered.add(f);
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
  if (q.frames?.length)
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
  const pattern = cfg.bank ?? /^(drill\d+[a-z]?|test\d+)\.json$/;
  for (const f of readdirSync(dir).filter((f) => pattern.test(f)))
    bank.push(...JSON.parse(readFileSync(join(dir, f), 'utf8')));

  const lessons = JSON.parse(readFileSync(join(dir, 'lessons.json'), 'utf8'));
  const made = [];
  for (const set of cfg.sets) {
    const authored = JSON.parse(readFileSync(join(dir, 'doing', `${set.dir}.json`), 'utf8'));
    const pool = bank.filter((q) => set.units.includes(q.module));
    const { picked, covered } = choose(pool, cfg.size, cfg);
    const tests = picked.filter((q) => (q.slides ?? []).some((s) => cfg.examTag.test(s))).length;
    const blocks = [
      { kind: 'teach', label: 'How to sit this', tag: 'read this first', html: authored.intro },
      {
        kind: 'drill',
        label: `Part A: ${picked.length} objective questions on this module`,
        tag: `${tests} of them ${cfg.examNoun}, then ${
          picked.length - tests
        } more chosen so the set reaches ${covered.size} separate points`,
        pick: 'all',
        topics: [],
        ids: picked.map((q) => q.id),
      },
      ...(authored.questions.length
        ? [
            {
              kind: 'heading',
              // Each paper says what its own Part B is: only INS224 pairs every
              // theory question with a practical, and saying so on a course that
              // does not is simply wrong.
              text: authored.partBHeading ?? cfg.partBHeading ?? 'Part B: the written questions',
            },
            ...authored.questions.flatMap((q, i) => questionBlocks(q, i + 1)),
          ]
        : []),
      // A course whose Part B is past questions teaches the method once, after
      // them, rather than repeating it under every question that uses it.
      ...(authored.methodFrames?.length
        ? [
            { kind: 'heading', text: 'Part 2: the method behind these, taught from nothing' },
            {
              kind: 'frames',
              label: 'Work it frame by frame',
              tag: 'for a reader who has never read the course',
              frames: authored.methodFrames,
            },
          ]
        : []),
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
      } facts; Part B ${authored.questions.length} theory questions, ${
        authored.questions.reduce((t, q) => t + (q.frames?.length ?? 0), 0) +
        (authored.methodFrames?.length ?? 0)
      } frames`
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
      const sitting = plan.find((s) => s.lessons.includes(set.planAfter));
      if (!sitting) throw new Error(`no sitting studies ${set.planAfter}, for ${set.slug}`);
      if (!sitting.lessons.includes(set.slug)) sitting.lessons.push(set.slug);
    }
    writeFileSync(planFile, JSON.stringify(plan, null, 2) + '\n');
  }
  console.log(`  wrote ${made.length} lessons into data/${code}/lessons.json`);
}

build(process.argv[2] ?? 'ins224');
