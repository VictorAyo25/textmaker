/**
 * Crash-course progress, kept in the browser.
 *
 * Deliberately local and not synced. Attempt scores are worth carrying between
 * devices because they are evidence; "I have read frame 14" is not, and syncing
 * it would mean a database write on every button press in a lesson. If storage
 * is blocked the lessons still work, they simply start from the top each time.
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
