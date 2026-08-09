/**
 * Crash-course progress: local first, then carried between devices.
 *
 * The browser copy is the working copy, so a lesson never waits on the network
 * and works with no connection at all. When there is a signed-in account, the
 * map is also pushed to /api/progress on a debounce and MERGED with whatever
 * the server holds on load, so reading four lessons on a laptop and picking up
 * on a phone shows four lessons read.
 *
 * The merge is deliberately generous rather than clever: the furthest frame
 * reached wins, done stays done, and a self-mark of "right" is not overwritten
 * by an older "wrong". Two devices can never destroy each other's progress,
 * which matters far more here than resolving which edit was truly last.
 */
export interface LessonProgress {
  /** How many programmed frames have been reached. */
  frames?: number;
  /** Self-marks on the "Your turn" recalls, keyed by block index. */
  marks?: Record<string, 'right' | 'wrong'>;
  done?: boolean;
}

export type ProgressMap = Record<string, LessonProgress>;

export const lessonProgressKey = (code: string) => `drill-lessons-v1:${code}`;

export function readProgress(key: string): ProgressMap {
  if (typeof window === 'undefined') return {};
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as ProgressMap) : {};
  } catch {
    return {};
  }
}

export function writeProgress(key: string, map: ProgressMap): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(key, JSON.stringify(map));
  } catch {
    /* private mode or a full quota: progress is a convenience, never a blocker */
  }
}

/**
 * Combine two progress maps without either one losing anything.
 *
 * Furthest frame wins, done stays done, and "right" beats "wrong" on a recall,
 * because a self-mark you earned on one device should not be taken away by an
 * older attempt on another.
 */
export function mergeProgress(a: ProgressMap, b: ProgressMap): ProgressMap {
  const out: ProgressMap = { ...a };
  for (const [slug, theirs] of Object.entries(b)) {
    const mine = out[slug];
    if (!mine) {
      out[slug] = theirs;
      continue;
    }
    const marks = { ...(mine.marks ?? {}) };
    for (const [k, v] of Object.entries(theirs.marks ?? {})) {
      if (marks[k] !== 'right') marks[k] = v;
    }
    out[slug] = {
      frames: Math.max(mine.frames ?? 1, theirs.frames ?? 1),
      done: Boolean(mine.done || theirs.done),
      marks,
    };
  }
  return out;
}

/** The course this key belongs to, for the sync endpoint. */
const courseOf = (key: string) => key.split(':')[1] ?? '';

/**
 * Pull the account's copy and fold it into the browser's.
 *
 * Returns the merged map, or the local one unchanged when there is no account,
 * no Supabase, or no network. Never throws: a sync failure must not stop
 * someone reading a lesson.
 */
export async function pullProgress(key: string): Promise<ProgressMap> {
  const local = readProgress(key);
  if (typeof window === 'undefined') return local;
  try {
    const r = await fetch(`/api/progress?course=${encodeURIComponent(courseOf(key))}`);
    if (!r.ok) return local;
    const body = (await r.json()) as { synced?: boolean; progress?: ProgressMap | null };
    if (!body.synced || !body.progress) return local;
    const merged = mergeProgress(local, body.progress);
    writeProgress(key, merged);
    return merged;
  } catch {
    return local;
  }
}

/** Debounced push, so a lesson costs one write after you stop, not one a click. */
const pending: Record<string, ReturnType<typeof setTimeout>> = {};

export function pushProgress(key: string, map: ProgressMap, delay = 2500): void {
  if (typeof window === 'undefined') return;
  clearTimeout(pending[key]);
  pending[key] = setTimeout(() => {
    void fetch('/api/progress', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ course: courseOf(key), progress: map }),
    }).catch(() => {
      /* offline, or signed out: the browser copy is still correct */
    });
  }, delay);
}
