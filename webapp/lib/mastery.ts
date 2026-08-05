import type { Course, Marked, Question } from './types';

/**
 * What the platform remembers about each question, across sessions.
 *
 * Every test used to be a fresh random draw, so a fact you keep missing came
 * round exactly as often as one you already knew cold. This fixes that: each
 * question carries a Leitner box, and a question you have just missed drops to
 * box 0 and comes back at once, while one you keep getting right climbs and
 * goes quiet for longer and longer.
 *
 * Kept in this browser only, like the lesson progress and for the same reason:
 * it needs no account, no database and no environment variable to work, so it
 * works for everyone on day one. Clearing site data clears it.
 */

export interface QuestionRecord {
  /** Leitner box: 0 is just missed, BOXES - 1 is resting. */
  box: number;
  hits: number;
  misses: number;
  /** Epoch ms of the last time this question was marked. */
  last: number;
}

export type Mastery = Record<string, QuestionRecord>;

const DAY = 24 * 60 * 60 * 1000;

/**
 * How long a question rests in each box before it is worth asking again.
 * Box 0 is due immediately, which is the point of box 0.
 */
export const INTERVALS = [0, 1 * DAY, 3 * DAY, 7 * DAY, 16 * DAY, 35 * DAY];
export const BOXES = INTERVALS.length;

const key = (code: string) => `drill-mastery-v1:${code}`;

export function loadMastery(code: string): Mastery {
  if (typeof window === 'undefined') return {};
  try {
    const raw = localStorage.getItem(key(code));
    const parsed: unknown = raw ? JSON.parse(raw) : {};
    // Storage is user-writable and survives across deploys, so anything that is
    // not the shape we expect is discarded rather than trusted.
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return {};
    const out: Mastery = {};
    for (const [id, v] of Object.entries(parsed as Record<string, unknown>)) {
      const r = v as Partial<QuestionRecord>;
      if (
        typeof r?.box === 'number' &&
        typeof r?.hits === 'number' &&
        typeof r?.misses === 'number' &&
        typeof r?.last === 'number'
      ) {
        out[id] = {
          box: Math.min(BOXES - 1, Math.max(0, Math.floor(r.box))),
          hits: Math.max(0, Math.floor(r.hits)),
          misses: Math.max(0, Math.floor(r.misses)),
          last: r.last,
        };
      }
    }
    return out;
  } catch {
    return {};
  }
}

export function saveMastery(code: string, m: Mastery): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(key(code), JSON.stringify(m));
  } catch {
    /* storage full or blocked: mastery is simply not remembered */
  }
}

/**
 * Fold a finished paper into what we already knew.
 *
 * Part marks count as a miss. Three of four blanks is not knowing the fact, and
 * a question that comes back is cheaper than a mark lost in the hall.
 */
export function record(previous: Mastery, marked: Marked[], now: number): Mastery {
  const next: Mastery = { ...previous };
  for (const m of marked) {
    const id = m.question.id;
    const was = next[id] ?? { box: 0, hits: 0, misses: 0, last: 0 };
    next[id] = m.correct
      ? {
          box: Math.min(BOXES - 1, was.box + 1),
          hits: was.hits + 1,
          misses: was.misses,
          last: now,
        }
      : { box: 0, hits: was.hits, misses: was.misses + 1, last: now };
  }
  return next;
}

export function isDue(r: QuestionRecord, now: number): boolean {
  return now - r.last >= INTERVALS[Math.min(r.box, BOXES - 1)];
}

/**
 * The questions worth drilling now: ones you have missed before, whose rest is
 * over. Sorted worst first, so a short session spends itself where it hurts.
 */
export function weakSpots(course: Course, m: Mastery, now: number): Question[] {
  return course.questions
    .filter((q) => {
      const r = m[q.id];
      return !!r && r.misses > 0 && isDue(r, now);
    })
    .sort((a, b) => {
      const ra = m[a.id];
      const rb = m[b.id];
      if (ra.box !== rb.box) return ra.box - rb.box;
      if (ra.misses !== rb.misses) return rb.misses - ra.misses;
      return ra.last - rb.last;
    });
}

export interface MasterySummary {
  /** Questions in this course that have been marked at least once. */
  seen: number;
  unseen: number;
  /** Missed before and due now. */
  weak: number;
  byMisses: { once: number; twice: number; more: number };
  /** Missed before, but resting: asked again later, not now. */
  resting: number;
  /** Right every time so far, and in the top box. */
  mastered: number;
}

export function summarise(course: Course, m: Mastery, now: number): MasterySummary {
  const s: MasterySummary = {
    seen: 0,
    unseen: 0,
    weak: 0,
    byMisses: { once: 0, twice: 0, more: 0 },
    resting: 0,
    mastered: 0,
  };
  for (const q of course.questions) {
    const r = m[q.id];
    if (!r) {
      s.unseen += 1;
      continue;
    }
    s.seen += 1;
    if (r.misses > 0) {
      if (isDue(r, now)) {
        s.weak += 1;
        if (r.misses === 1) s.byMisses.once += 1;
        else if (r.misses === 2) s.byMisses.twice += 1;
        else s.byMisses.more += 1;
      } else {
        s.resting += 1;
      }
    } else if (r.box >= BOXES - 1) {
      s.mastered += 1;
    }
  }
  return s;
}

// ---- the fact-level view, for courses that carry a ledger ----

export type FactState = 'solid' | 'shaky' | 'untested';

/**
 * How a single fact stands, judged through the questions that test it.
 *
 * A fact is shaky the moment any question testing it sits in box 0, because
 * box 0 means the last answer on it was wrong. Being right about a fact once
 * and wrong about it twice is not knowing it.
 */
export function factState(
  factId: string,
  byFact: Map<string, Question[]>,
  m: Mastery
): FactState {
  const qs = byFact.get(factId) ?? [];
  const seen = qs.filter((q) => m[q.id]);
  if (!seen.length) return 'untested';
  return seen.some((q) => m[q.id].box === 0) ? 'shaky' : 'solid';
}

/** Which questions test which fact, built once from the bank. */
export function indexByFact(course: Course): Map<string, Question[]> {
  const map = new Map<string, Question[]>();
  for (const q of course.questions) {
    for (const f of q.facts ?? []) {
      const list = map.get(f);
      if (list) list.push(q);
      else map.set(f, [q]);
    }
  }
  return map;
}
