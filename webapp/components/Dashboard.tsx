'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { countdown, longDate } from '@/data/timetable';
import { lessonHref } from '@/data/lessons';
import { lessonProgressKey, pullProgress, readProgress, type ProgressMap } from '@/lib/progress';

/**
 * One row per course: where you are, and what to do next.
 *
 * Everything here answers a question a reader actually asks at 6am with an
 * exam that afternoon. How long until it. How much of the reading is left. What
 * did I score last time. And the one that matters most: what do I open now.
 *
 * All of it is computed in the browser from progress and attempt history, so it
 * is per reader rather than per course, and it costs the page nothing until it
 * mounts.
 */
export interface DashCourse {
  code: string;
  title: string;
  examAt?: string;
  examWindow?: string;
  questions: number;
  lessons: number;
  minutes: number;
  /** Lesson slugs in reading order, from the dated plan where there is one. */
  order: DashLesson[];
  /** The dated plan's sittings, so the page can say what TODAY holds. */
  sessions: DashSession[];
  hasCrash: boolean;
}

export interface DashSession {
  date: string;
  window: string;
  goal: string;
  lessons: DashLesson[];
}

/** A lesson as the dashboard needs it. `revision` decides which section serves it. */
export interface DashLesson {
  slug: string;
  title: string;
  minutes: number;
  revision?: boolean;
}

/** Minutes after midnight of the first clock time in a window, for ordering.
 *  A window with no clock time, an optional "if you finish early" sitting,
 *  goes after every timed one. */
function startOf(window: string): number {
  const m = window.match(/(\d{1,2}):(\d{2})\s*(am|pm)/i);
  if (!m) return 24 * 60;
  const h = (Number(m[1]) % 12) + (m[3].toLowerCase() === 'pm' ? 12 : 0);
  return h * 60 + Number(m[2]);
}

/**
 * Today's sittings across every course, in clock order, with anything an
 * earlier day left unread listed first as catch-up. When nothing is planned for
 * today it shows the next day that has something, so the card is never empty
 * while there is work ahead.
 */
function Today({
  courses,
  today,
  done,
}: {
  courses: DashCourse[];
  today: string;
  done: (code: string, slug: string) => boolean;
}) {
  const all = courses.flatMap((c) => c.sessions.map((s) => ({ ...s, code: c.code })));
  const behind = all
    .filter((s) => s.date < today)
    .map((s) => ({ ...s, lessons: s.lessons.filter((l) => !done(s.code, l.slug)) }))
    .filter((s) => s.lessons.length);
  const ahead = [...new Set(all.filter((s) => s.date >= today).map((s) => s.date))].sort();
  const day = ahead[0];
  if (!day && !behind.length) return null;
  const sittings = all
    .filter((s) => s.date === day)
    .sort((a, b) => startOf(a.window) - startOf(b.window));

  return (
    <div className="today">
      <h3>{day === today ? 'Today' : 'Next'}, {day ? longDate(`${day}T00:00`) : ''}</h3>
      {behind.length > 0 && (
        <div className="sitting behind">
          <p className="swhen">
            <b>Catch up first:</b> {behind.reduce((t, s) => t + s.lessons.length, 0)} lesson
            {behind.reduce((t, s) => t + s.lessons.length, 0) === 1 ? '' : 's'} from an earlier day,
            not yet marked done
          </p>
          <ul className="slessons">
            {behind.flatMap((s) =>
              s.lessons.map((l) => (
                <li key={s.code + l.slug}>
                  <Link href={lessonHref(s.code, l)}>
                    <span className="badge">{s.code}</span> {l.title}
                  </Link>
                </li>
              ))
            )}
          </ul>
        </div>
      )}
      {sittings.map((s) => {
        const left = s.lessons.filter((l) => !done(s.code, l.slug));
        const read = s.lessons.length - left.length;
        return (
          <div className="sitting" key={s.code + s.window} data-course={s.code}>
            <p className="swhen">
              <span className="badge">{s.code}</span> {s.window}
            </p>
            <p className="sgoal">{s.goal}</p>
            <div className="frametrack">
              <i style={{ width: `${Math.round((read / s.lessons.length) * 100)}%` }} />
            </div>
            <ol className="slessons">
              {s.lessons.map((l) => (
                <li key={l.slug} className={done(s.code, l.slug) ? 'isdone' : ''}>
                  <Link href={lessonHref(s.code, l)}>
                    {done(s.code, l.slug) ? '✓ ' : ''}
                    {l.title}
                  </Link>
                  <span className="smin">{l.minutes} min</span>
                </li>
              ))}
            </ol>
            {left[0] ? (
              <Link className="btn" href={lessonHref(s.code, left[0])}>
                {read ? 'Carry on' : 'Start'}: {left[0].title}
              </Link>
            ) : (
              <p className="note">All {s.lessons.length} read. Well done.</p>
            )}
          </div>
        );
      })}
    </div>
  );
}

interface Attempt {
  title: string;
  percent: number;
  total: number;
  created_at: string;
}

const historyKey = (code: string) =>
  code === 'TMC221' ? 'tmc-drill-history-v1' : `drill-history-v1:${code}`;

function readHistory(code: string): Attempt[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(historyKey(code));
    return raw ? (JSON.parse(raw) as Attempt[]) : [];
  } catch {
    return [];
  }
}

export default function Dashboard({ courses }: { courses: DashCourse[] }) {
  const [today, setToday] = useState<string | null>(null);
  const [progress, setProgress] = useState<Record<string, ProgressMap>>({});
  const [history, setHistory] = useState<Record<string, Attempt[]>>({});

  useEffect(() => {
    const d = new Date();
    setToday(
      `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(
        d.getDate()
      ).padStart(2, '0')}`
    );
    const p: Record<string, ProgressMap> = {};
    const h: Record<string, Attempt[]> = {};
    for (const c of courses) {
      p[c.code] = readProgress(lessonProgressKey(c.code));
      h[c.code] = readHistory(c.code);
    }
    setProgress(p);
    setHistory(h);
    // Then fold in whatever the account holds, so a phone shows the laptop's work.
    for (const c of courses) {
      void pullProgress(lessonProgressKey(c.code)).then((m) =>
        setProgress((prev) => ({ ...prev, [c.code]: m }))
      );
    }
  }, [courses]);

  if (!courses.length) return null;

  const isDone = (code: string, slug: string) => Boolean(progress[code]?.[slug]?.done);

  return (
    <div className="card dash">
      {today && <Today courses={courses} today={today} done={isDone} />}
      <h2>Where you are</h2>
      <p className="help">
        Progress is yours and follows you between devices once you are signed in.
        The next lesson is the first one in the plan you have not marked done.
      </p>

      {courses.map((c) => {
        const done = new Set(
          Object.entries(progress[c.code] ?? {})
            .filter(([, v]) => v.done)
            .map(([slug]) => slug)
        );
        const readCount = c.order.filter((l) => done.has(l.slug)).length;
        const pct = c.order.length ? Math.round((readCount / c.order.length) * 100) : 0;
        const left = c.order.filter((l) => !done.has(l.slug));
        const minutesLeft = left.reduce((t, l) => t + l.minutes, 0);
        const next = left[0];
        const best = (history[c.code] ?? []).reduce(
          (m, a) => (a.percent > m ? a.percent : m),
          -1
        );
        const runs = (history[c.code] ?? []).length;

        return (
          <section className="dashrow" key={c.code} data-course={c.code}>
            <header>
              <span className="badge">{c.code}</span>
              <span className="dtitle">{c.title}</span>
              {c.examAt && today && (
                <span className="cdown">{countdown(today, c.examAt)}</span>
              )}
            </header>

            {c.examAt && (
              <p className="dwhen">
                {longDate(c.examAt)}
                {c.examWindow ? `, ${c.examWindow}` : ''}
              </p>
            )}

            {c.hasCrash && (
              <>
                <div className="frametrack">
                  <i style={{ width: `${pct}%` }} />
                </div>
                <p className="dstat">
                  <b>
                    {readCount} of {c.order.length}
                  </b>{' '}
                  lessons read
                  {minutesLeft > 0 && (
                    <>
                      {' '}
                      &middot; <b>{minutesLeft} min</b> of reading left
                    </>
                  )}
                  {' '}&middot; {c.questions} questions in the bank
                  {runs > 0 && (
                    <>
                      {' '}
                      &middot; {runs} run{runs === 1 ? '' : 's'} sat, best{' '}
                      <b>{best}%</b>
                    </>
                  )}
                </p>
              </>
            )}

            <div className="dactions">
              {next ? (
                <Link className="btn" href={lessonHref(c.code, next)}>
                  Next: {next.title}
                </Link>
              ) : c.hasCrash ? (
                <Link className="btn" href={`/${c.code.toLowerCase()}`}>
                  All read. Drill it
                </Link>
              ) : (
                <Link className="btn" href={`/${c.code.toLowerCase()}`}>
                  Open the drill
                </Link>
              )}
              {c.hasCrash && (
                <Link className="chip" href={`/${c.code.toLowerCase()}/learn`}>
                  The plan
                </Link>
              )}
              <Link className="chip" href={`/${c.code.toLowerCase()}`}>
                Drill
              </Link>
            </div>
          </section>
        );
      })}
    </div>
  );
}
