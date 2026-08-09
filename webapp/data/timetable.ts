import type { ExamSlot } from '@/lib/types';

/**
 * The Omega semester timetable, every paper, in the order they are sat.
 *
 * Two of these courses are on the drill and carry a dated crash-course plan.
 * The rest are revised from their manual, and the slot still says when, so
 * nothing on the week is left undated. Times are local and inclusive of the
 * whole window the paper occupies.
 */
export const EXAMS: ExamSlot[] = [
  {
    code: 'DTS224',
    title: 'Data Management I',
    at: '2026-08-10T15:00',
    window: '03:00 PM to 06:00 PM',
    studyWith: 'the DTS224 manual, 84 pages',
  },
  {
    code: 'CSC242',
    title: 'Discrete Structures',
    at: '2026-08-11T10:00',
    window: '10:00 AM to 01:00 PM',
    studyWith: 'the CSC242 manual, 466 pages, Python and C++ edition',
  },
  {
    code: 'INS224',
    title: 'Systems Analysis and Design',
    at: '2026-08-11T15:00',
    window: '03:00 PM to 06:00 PM',
    studyWith: 'the INS224 manual, 101 pages',
  },
  {
    code: 'IFT222',
    title: 'Computer Architecture and Organization',
    at: '2026-08-12T10:00',
    window: '10:00 AM to 01:00 PM',
  },
  {
    code: 'CSC241',
    title: 'Python Programming Language',
    at: '2026-08-12T15:00',
    window: '03:00 PM to 06:00 PM',
    studyWith: 'the CSC241 manual, 200 pages, verbatim edition',
  },
  {
    code: 'COS221',
    title: 'Computer Programming I, Java',
    at: '2026-08-13T15:00',
    window: '03:00 PM to 06:00 PM',
    studyWith: 'the COS221 manual, 333 pages',
  },
  {
    code: 'PHY121',
    title: 'General Physics II',
    at: '2026-08-14T10:00',
    window: '10:00 AM to 01:00 PM',
  },
];

const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

/** "Wednesday 12 August" from '2026-08-12' or '2026-08-12T10:00'. */
export function longDate(iso: string): string {
  const [y, m, d] = iso.slice(0, 10).split('-').map(Number);
  const dt = new Date(Date.UTC(y, m - 1, d));
  return `${DAYS[dt.getUTCDay()]} ${d} ${MONTHS[m - 1]}`;
}

/** "Wed 12 Aug" for tight rows. */
export function shortDate(iso: string): string {
  const [y, m, d] = iso.slice(0, 10).split('-').map(Number);
  const dt = new Date(Date.UTC(y, m - 1, d));
  return `${DAYS[dt.getUTCDay()].slice(0, 3)} ${d} ${MONTHS[m - 1].slice(0, 3)}`;
}

/**
 * Whole days from `from` to `to`, both given as ISO dates. Counted on the dates
 * alone, so an exam tomorrow morning reads as 1 whether it is now dawn or dusk.
 */
export function daysBetween(from: string, to: string): number {
  const ms = Date.parse(`${to.slice(0, 10)}T00:00:00Z`) - Date.parse(`${from.slice(0, 10)}T00:00:00Z`);
  return Math.round(ms / 86400000);
}

/** "today", "tomorrow", "in 3 days", "sat". */
export function countdown(fromISO: string, examISO: string): string {
  const n = daysBetween(fromISO, examISO);
  if (n < 0) return 'sat';
  if (n === 0) return 'today';
  if (n === 1) return 'tomorrow';
  return `in ${n} days`;
}
