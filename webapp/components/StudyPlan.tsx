'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import type { ExamSlot, StudySession } from '@/lib/types';
import type { LessonCard } from '@/data/lessons';
import { countdown, longDate } from '@/data/timetable';
import { lessonProgressKey, readProgress, type ProgressMap } from '@/lib/progress';

/**
 * The crash course as a dated timetable rather than a pile of lessons.
 *
 * Which sitting is "now" is decided in the browser, because a statically built
 * page has no idea what day the reader opened it on. Until that resolves, every
 * sitting renders plainly, so the page is never wrong, only briefly undecided.
 */
export default function StudyPlan({
  code,
  plan,
  exam,
  cards,
}: {
  code: string;
  plan: StudySession[];
  exam?: ExamSlot;
  cards: LessonCard[];
}) {
  const [today, setToday] = useState<string | null>(null);
  const [progress, setProgress] = useState<ProgressMap>({});

  useEffect(() => {
    const d = new Date();
    const iso = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(
      d.getDate()
    ).padStart(2, '0')}`;
    setToday(iso);
    setProgress(readProgress(lessonProgressKey(code)));
  }, [code]);

  const byslug = new Map(cards.map((c) => [c.slug, c]));
  const minutesOf = (s: StudySession) =>
    s.lessons.reduce((t, slug) => t + (byslug.get(slug)?.minutes ?? 0), 0);

  return (
    <div className="card plan">
      <h2>Your reading plan</h2>
      {exam && (
        <p className="examline">
          <b>{exam.code}</b> is sat on <b>{longDate(exam.at)}</b>, {exam.window}
          {today && <span className="cdown">{countdown(today, exam.at)}</span>}
        </p>
      )}
      <p className="help">
        Every lesson is placed in a sitting that fits the gaps this week actually
        leaves. Read them in this order and you will not have to decide anything at
        eleven at night.
      </p>

      {plan.map((s, i) => {
        const done = s.lessons.every((slug) => progress[slug]?.done);
        const state =
          today === null ? '' : s.date < today ? 'past' : s.date === today ? 'now' : 'ahead';
        return (
          <section className={`sitting ${state} ${done ? 'alldone' : ''}`} key={`${s.date}-${i}`}>
            <header>
              <span className="when">{longDate(s.date)}</span>
              <span className="win">{s.window}</span>
              <span className="mins">{minutesOf(s)} min of reading</span>
              {state === 'now' && <span className="tag">today</span>}
              {done && <span className="tag ok">done</span>}
            </header>
            <p className="goal">{s.goal}</p>
            <ol className="sitlist">
              {s.lessons.map((slug) => {
                const c = byslug.get(slug);
                if (!c) return null;
                return (
                  <li key={slug}>
                    <Link href={`/${code.toLowerCase()}/learn/${slug}`}>
                      <span className={`box ${progress[slug]?.done ? 'ticked' : ''}`}>
                        {progress[slug]?.done ? '✓' : ''}
                      </span>
                      <span className="t">{c.title}</span>
                      <span className="stat">{c.minutes} min</span>
                    </Link>
                  </li>
                );
              })}
            </ol>
            {s.drill && (
              <p className="drillline">
                <b>Then drill:</b> {s.drill}
              </p>
            )}
          </section>
        );
      })}
    </div>
  );
}
