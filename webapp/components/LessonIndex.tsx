'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import type { LessonCard } from '@/data/lessons';
import { lessonProgressKey, readProgress, type ProgressMap } from '@/lib/progress';

export default function LessonIndex({
  code,
  cards,
}: {
  code: string;
  cards: LessonCard[];
}) {
  const [progress, setProgress] = useState<ProgressMap>({});

  useEffect(() => {
    setProgress(readProgress(lessonProgressKey(code)));
  }, [code]);

  const doneCount = cards.filter((c) => progress[c.slug]?.done).length;
  const totalMinutes = cards.reduce((t, c) => t + c.minutes, 0);
  const parts = [...new Set(cards.map((c) => c.part))];

  return (
    <>
      <div className="card">
        <h2>The crash course</h2>
        <p className="help">
          The whole course taught from zero, in the order that gets you a mark fastest.
          Each skill is a programmed lesson: one small step at a time, and you answer
          before the page will tell you anything. Then it hands you the real questions on
          that skill.
        </p>
        <p className="note">
          {cards.length} lessons &middot; about {Math.round(totalMinutes / 60)} hours end
          to end &middot; {doneCount} marked done
        </p>
        {doneCount > 0 && (
          <div className="frametrack" style={{ marginTop: 10 }}>
            <i style={{ width: `${(doneCount / cards.length) * 100}%` }} />
          </div>
        )}
      </div>

      {parts.map((part) => (
        <div className="card" key={part}>
          <h2>{part}</h2>
          {cards
            .filter((c) => c.part === part)
            .map((c) => {
              const p = progress[c.slug];
              const started = (p?.frames ?? 1) > 1 || p?.done;
              return (
                <Link
                  key={c.slug}
                  className="modrow lessonrow"
                  href={`/${code.toLowerCase()}/learn/${c.slug}`}
                >
                  <span className={`box ${p?.done ? 'ticked' : ''}`}>
                    {p?.done ? '✓' : ''}
                  </span>
                  <span>
                    <span className="t">{c.title}</span>
                    <br />
                    <span
                      className="b"
                      dangerouslySetInnerHTML={{ __html: shorten(c.lead) }}
                    />
                    <br />
                    <span className="stat">
                      {c.minutes} min
                      {c.frames > 0 && ` · ${c.frames} frames`}
                      {c.worked > 0 && ` · ${c.worked} worked example${c.worked === 1 ? '' : 's'}`}
                      {c.recalls > 0 && ` · ${c.recalls} recall${c.recalls === 1 ? '' : 's'}`}
                      {started && !p?.done && ' · in progress'}
                    </span>
                  </span>
                  <span className="cnt">{p?.done ? 'Done' : started ? 'Resume' : 'Read'}</span>
                </Link>
              );
            })}
        </div>
      ))}

      <div className="card">
        <h2>When the lessons are done</h2>
        <p className="help">
          Sit the real papers. Both objective tests are in the drill, all 120 questions,
          each one reviewed option by option.
        </p>
        <Link className="btn" href={`/${code.toLowerCase()}`}>
          Go to the drill
        </Link>
      </div>
    </>
  );
}

/**
 * Index rows take the opening of a lead, not the whole paragraph. Sentences are
 * taken whole until there is enough to say something, so a row never ends up
 * with four words or with the entire lesson introduction.
 */
function shorten(lead: string): string {
  const flat = lead.replace(/\s+/g, ' ').trim();
  let out = '';
  for (const piece of flat.split(/(?<=\.)\s+/)) {
    out = out ? `${out} ${piece}` : piece;
    if (out.length >= 45) break;
  }
  return out;
}
