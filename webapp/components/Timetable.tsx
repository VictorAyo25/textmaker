'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { EXAMS, countdown, longDate } from '@/data/timetable';

/**
 * The whole exam week on one card, in the order the papers are sat.
 *
 * Which row is next depends on today's date, which a statically built page
 * cannot know, so the highlighting is decided in the browser after mount. Before
 * that the rows still read correctly, they are simply all the same weight.
 */
export default function Timetable({ onDrill }: { onDrill: string[] }) {
  const [today, setToday] = useState<string | null>(null);

  useEffect(() => {
    const d = new Date();
    setToday(
      `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(
        d.getDate()
      ).padStart(2, '0')}`
    );
  }, []);

  const nextUp = today ? EXAMS.find((e) => e.at.slice(0, 10) >= today)?.code : null;
  const days = [...new Set(EXAMS.map((e) => e.at.slice(0, 10)))];

  return (
    <div className="card timetable">
      <h2>Exam week</h2>
      <p className="help">
        Seven papers in five days. The two on the drill carry a dated reading plan;
        the rest name the manual to revise from.
      </p>
      {days.map((day) => (
        <section className={`tday ${today && day < today ? 'past' : ''}`} key={day}>
          <h3>
            {longDate(day)}
            {today && (
              <span className="cdown">{countdown(today, day)}</span>
            )}
          </h3>
          {EXAMS.filter((e) => e.at.slice(0, 10) === day).map((e) => {
            const drillable = onDrill.includes(e.code);
            const row = (
              <>
                <span className="badge">{e.code}</span>
                <span>
                  <span className="t">{e.title}</span>
                  <br />
                  <span className="b">{e.window}</span>
                  <br />
                  <span className="stat">
                    {drillable
                      ? 'On the drill, with a dated reading plan'
                      : `Revise from ${e.studyWith}`}
                  </span>
                </span>
                <span className="cnt">{drillable ? 'Plan' : 'Manual'}</span>
              </>
            );
            return drillable ? (
              <Link
                className={`modrow examrow ${e.code === nextUp ? 'next' : ''}`}
                key={e.code}
                data-course={e.code}
                href={`/${e.code.toLowerCase()}/learn`}
              >
                {row}
              </Link>
            ) : (
              <div
                className={`modrow examrow flat ${e.code === nextUp ? 'next' : ''}`}
                key={e.code}
              >
                {row}
              </div>
            );
          })}
        </section>
      ))}
    </div>
  );
}
