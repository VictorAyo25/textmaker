'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import type { LessonCard } from '@/data/lessons';
import { lessonProgressKey, pullProgress, readProgress, type ProgressMap } from '@/lib/progress';

/**
 * The Learn by doing section: one paper per module, each a whole sitting.
 *
 * Deliberately not the lesson index. A lesson row is a title and a length; a
 * paper is a thing you sit, so each row says what is inside it, and the page
 * says once, at the top, how the two parts work.
 */
export default function DoingIndex({ code, cards }: { code: string; cards: LessonCard[] }) {
  const [progress, setProgress] = useState<ProgressMap>({});

  useEffect(() => {
    setProgress(readProgress(lessonProgressKey(code)));
    void pullProgress(lessonProgressKey(code)).then(setProgress);
  }, [code]);

  const minutes = cards.reduce((t, c) => t + c.minutes, 0);
  const done = cards.filter((c) => progress[c.slug]?.done).length;

  return (
    <>
      <div className="card doinghead">
        <h2>Learn by doing</h2>
        <p className="help">
          One paper for each module, in the shape of the real one. <b>Part A</b> is the
          objective questions on that module, the examiner's own first, every option
          explained as you answer. <b>Part B</b> is the theory questions, each with its
          practical scenario, and each answered twice: the answer you would write in the
          hall, then the same question taught from nothing in steps.
        </p>
        <p className="note">
          {cards.length} papers &middot; about {Math.round(minutes / 60)} hours end to end
          &middot; {done} marked done
        </p>
      </div>

      {cards.map((c) => (
        <Link className="card doingrow" key={c.slug} href={`/${code.toLowerCase()}/doing/${c.slug}`}>
          <span className="dkick">{c.kick}</span>
          <h3>
            {progress[c.slug]?.done ? '✓ ' : ''}
            {c.title}
          </h3>
          <p className="dlead">{c.lead}</p>
          <p className="note">
            {c.minutes} min &middot; {c.worked} model answers &middot; {c.frames} teaching frames
          </p>
          <span className="btn">{progress[c.slug]?.done ? 'Sit it again' : 'Sit this paper'}</span>
        </Link>
      ))}
    </>
  );
}
