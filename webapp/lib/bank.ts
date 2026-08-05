import type { Course, Difficulty, Question, TestConfig } from './types';

const TIERS: Difficulty[] = ['easy', 'medium', 'hard'];

export function shuffle<T>(items: T[]): T[] {
  const a = [...items];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * Did the examiner actually set this one?
 *
 * A question counts as a past question when one of its provenance tags starts
 * with a prefix the course declares in `examTags`, such as "Test 2 Q". That is
 * the same tag the papers are rebuilt from, so the filter and the papers can
 * never disagree about what came from a real test.
 */
export function isPastQuestion(course: Course, q: Question): boolean {
  const tags = course.examTags ?? [];
  if (!tags.length) return false;
  return q.slides.some((s) => tags.some((t) => s.startsWith(t)));
}

/** How many of the bank the examiner set. Zero hides the filter. */
export function pastCount(course: Course): number {
  return course.questions.filter((q) => isPastQuestion(course, q)).length;
}

/** Everything the config allows, before the difficulty mix is applied. */
export function pool(course: Course, config: TestConfig): Question[] {
  return course.questions.filter((q) => {
    if (config.modules.length && !config.modules.includes(q.module)) return false;
    if (config.facets.length && !config.facets.some((f) => q.facets.includes(f)))
      return false;
    if (config.source === 'exam' && !isPastQuestion(course, q)) return false;
    return true;
  });
}

export function poolByTier(items: Question[]): Record<Difficulty, Question[]> {
  return {
    easy: items.filter((q) => q.difficulty === 'easy'),
    medium: items.filter((q) => q.difficulty === 'medium'),
    hard: items.filter((q) => q.difficulty === 'hard'),
  };
}

function normaliseMix(mix: Record<Difficulty, number>): Record<Difficulty, number> {
  const sum = TIERS.reduce((t, k) => t + Math.max(0, mix[k] || 0), 0);
  if (sum <= 0) return { easy: 34, medium: 33, hard: 33 };
  const out = {} as Record<Difficulty, number>;
  for (const k of TIERS) out[k] = (Math.max(0, mix[k] || 0) / sum) * 100;
  return out;
}

/**
 * Pick the paper.
 *
 * The requested mix is a target, not a promise: if a tier runs out (asking for
 * 40 hard Module 3 number questions when only 12 exist), the shortfall is taken
 * from the nearest tier rather than silently returning a short paper. What
 * actually got used comes back in `actual` so the UI can say so plainly.
 */
export interface Selection {
  questions: Question[];
  requested: number;
  actual: Record<Difficulty, number>;
  shortfall: number;
}

export function selectQuestions(course: Course, config: TestConfig): Selection {
  const available = pool(course, config);
  const tiers = poolByTier(available);
  const want = Math.min(config.count, available.length);
  const mix = normaliseMix(config.mix);

  // Largest-remainder apportionment, so the counts always add up to `want`.
  const exact = TIERS.map((t) => ({ tier: t, raw: (mix[t] / 100) * want }));
  const target = {} as Record<Difficulty, number>;
  let assigned = 0;
  for (const e of exact) {
    target[e.tier] = Math.floor(e.raw);
    assigned += target[e.tier];
  }
  const remainders = exact
    .map((e) => ({ tier: e.tier, rem: e.raw - Math.floor(e.raw) }))
    .sort((a, b) => b.rem - a.rem);
  let k = 0;
  while (assigned < want) {
    target[remainders[k % remainders.length].tier] += 1;
    assigned += 1;
    k += 1;
  }

  const picked: Question[] = [];
  const leftovers: Record<Difficulty, Question[]> = {
    easy: shuffle(tiers.easy),
    medium: shuffle(tiers.medium),
    hard: shuffle(tiers.hard),
  };
  const actual: Record<Difficulty, number> = { easy: 0, medium: 0, hard: 0 };

  for (const t of TIERS) {
    const take = leftovers[t].splice(0, target[t]);
    picked.push(...take);
    actual[t] += take.length;
  }

  // Top up from the nearest tier: a missing hard is best replaced by a medium.
  const neighbours: Record<Difficulty, Difficulty[]> = {
    easy: ['medium', 'hard'],
    medium: ['hard', 'easy'],
    hard: ['medium', 'easy'],
  };
  for (const t of TIERS) {
    let missing = target[t] - actual[t];
    for (const n of neighbours[t]) {
      if (missing <= 0) break;
      const take = leftovers[n].splice(0, missing);
      picked.push(...take);
      actual[n] += take.length;
      missing -= take.length;
    }
  }

  return {
    questions: shuffle(picked),
    requested: config.count,
    actual,
    shortfall: config.count - picked.length,
  };
}

/** Shuffle the options a question presents, without touching the answer keys. */
export function presentQuestion(q: Question, shuffleOptions: boolean): Question {
  if (!shuffleOptions) return q;
  const out: Question = { ...q };
  if (out.options) out.options = shuffle(out.options);
  if (out.blanks) out.blanks = out.blanks.map((b) => ({ ...b, choices: shuffle(b.choices) }));
  if (out.pairs) out.pairs = shuffle(out.pairs);
  return out;
}

/** Every right-hand label a match question offers, correct ones plus decoys. */
export function matchLabels(q: Question): string[] {
  const base = (q.pairs ?? []).map((p) => p.right);
  return shuffle([...new Set([...base, ...(q.extraLabels ?? [])])]);
}
