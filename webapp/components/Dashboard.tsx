'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { countdown, longDate } from '@/data/timetable';
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
  order: { slug: string; title: string; minutes: number }[];
  hasCrash: boolean;
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

  return (
    <div className="card dash">
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
                <Link className="btn" href={`/${c.code.toLowerCase()}/learn/${next.slug}`}>
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
