import type { Course, Question } from '@/lib/types';

/**
 * The question book: every question this course owns, arranged by topic and
 * ordered easy to hard, with its source labelled and repeats marked.
 *
 * Shared by the page and the PDF generator so the two can never disagree. The
 * ordering is deliberate: a reader working through a topic should meet the
 * definition questions before the two-step calculations, because the later ones
 * assume the earlier ones.
 */
export interface BookEntry {
  q: Question;
  n: number;
  /** Where the question came from, in words rather than tags. */
  source: string;
  /** Set when this question also appears elsewhere, naming the other place. */
  repeatOf?: string;
}

export interface BookTopic {
  number: number;
  title: string;
  blurb?: string;
  entries: BookEntry[];
  counts: { easy: number; medium: number; hard: number };
}

const RANK: Record<string, number> = { easy: 0, medium: 1, hard: 2 };

/** "Test 1 Q3" and "M1 S69" are tags; a reader wants to be told what they mean. */
export function sourceOf(q: Question): string {
  const tags = q.slides ?? [];
  const test = tags.find((t) => /^Test [12] Q/.test(t));
  if (test) return `The real ${test.replace(/^Test (\d) Q(\d+)$/, 'test $1, question $2')}`;
  const slide = tags.find((t) => /^M\d+ S\d+/.test(t));
  if (slide) {
    const m = /^M(\d+) S(\d+)/.exec(slide);
    return `Lecture slides, module ${m?.[1]}, slide ${m?.[2]}`;
  }
  const ref = tags.find((t) => /^Ref R\./.test(t));
  if (ref) return `Reference sheet ${ref.replace('Ref ', '')}`;
  return tags.join(', ') || 'Authored for this course';
}

const norm = (q: Question) =>
  (q.prompt ?? '').toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 90);

export function buildBook(course: Course): BookTopic[] {
  const all = course.questions;

  // Find repeats so they can be labelled rather than silently dropped. The
  // reader should see that the examiner asked the same thing twice.
  const groups = new Map<string, Question[]>();
  for (const q of all) {
    const k = norm(q);
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k)!.push(q);
  }
  const repeat = new Map<string, string>();
  for (const g of groups.values()) {
    if (g.length < 2) continue;
    for (const q of g) {
      const others = g.filter((x) => x.id !== q.id).map((x) => sourceOf(x));
      repeat.set(q.id, others.join(' and '));
    }
  }

  const topics: BookTopic[] = [];
  for (const m of course.modules) {
    const mine = all
      .filter((q) => q.module === m.number)
      .sort((a, b) => {
        const d = (RANK[a.difficulty] ?? 1) - (RANK[b.difficulty] ?? 1);
        if (d !== 0) return d;
        // Within a difficulty, the examiner's own questions come first.
        const ea = /^Test/.test(a.slides?.[0] ?? '') ? 0 : 1;
        const eb = /^Test/.test(b.slides?.[0] ?? '') ? 0 : 1;
        return ea - eb;
      });
    if (!mine.length) continue;
    topics.push({
      number: m.number,
      title: m.title,
      blurb: m.blurb,
      entries: mine.map((q, i) => ({
        q,
        n: i + 1,
        source: sourceOf(q),
        repeatOf: repeat.get(q.id),
      })),
      counts: {
        easy: mine.filter((q) => q.difficulty === 'easy').length,
        medium: mine.filter((q) => q.difficulty === 'medium').length,
        hard: mine.filter((q) => q.difficulty === 'hard').length,
      },
    });
  }
  return topics;
}

/** One speed tip per topic, because a tip per question would be noise. */
export const SPEED: Record<number, string> = {
  1: 'Convert to SI before anything else. mg to kg, µC to C, cm to m. Then ask: one charge or two? One gives a field, two gives a force.',
  2: 'Potential has a plain r, field has r squared. If the question says "four times further" the potential goes to a quarter and the field to a sixteenth.',
  3: 'For flux, θ is measured from the NORMAL, not the surface. Face on means θ = 0 and cos θ = 1, so Φ is just EA.',
  4: 'Capacitors are the opposite of resistors: parallel adds, series is the reciprocal. Energy has V squared in it.',
  5: 'Resistivity questions hide the area: a wire of radius r has A = πr², not r. Halving the radius quarters the area and quadruples the resistance.',
  6: 'Terminal voltage is always LESS than the emf, by exactly Ir. If your answer is bigger than the emf, you added where you should have subtracted.',
  7: 'The magnetic force never changes the speed, only the direction. So kinetic energy is unchanged and the path is a circle of radius mv/qB.',
  8: 'The loop centre formula has NO π in the denominator. The straight wire and the toroid both do. That single difference identifies the formula.',
  9: 'Nothing changing means no emf, whatever the field strength. Faraday needs a RATE, so look for a time in the question.',
  10: 'Step the voltage up and the current steps down. Power in equals power out if it is ideal, so V₁I₁ = V₂I₂.',
  11: 'In a vacuum everything is c = 3 × 10⁸. E/B = c for a plane wave, and c = fλ ties frequency to wavelength.',
};
