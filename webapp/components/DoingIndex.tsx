'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import type { LessonCard } from '@/data/lessons';
import type { DoingCopy } from '@/data/doing';
import { lessonProgressKey, pullProgress, readProgress, type ProgressMap } from '@/lib/progress';

/**
 * The Learn by doing section: one paper per module, each a whole sitting.
 *
 * Deliberately not the lesson index. A lesson row is a title and a length; a
 * paper is a thing you sit, so each row says what is inside it, and the page
 * says once, at the top, how the two parts work.
 */
export default function DoingIndex({
  code,
  cards,
  copy,
}: {
  code: string;
  cards: LessonCard[];
  copy: DoingCopy;
}) {
  const [progress, setProgress] = useState<ProgressMap>({});

  useEffect(() => {
    setProgress(readProgress(lessonProgressKey(code)));
    void pullProgress(lessonProgressKey(code)).then(setProgress);
  }, [code]);

  const minutes = cards.reduce((t, c) => t + c.minutes, 0);
  const done = cards.filter((c) => progress[c.slug]?.done).length;
  // A course may hold more than one kind of paper: INS224 has the module
  // papers and, separately, the past questions filed by module. They are kept
  // in the lesson's own `part`, so grouping needs no new field.
  const groups = [...new Set(cards.map((c) => c.part))];

  return (
    <>
      <div className="card doinghead">
        <h2>Learn by doing</h2>
        <p className="help">
          One paper for each module, in the shape of the real one. <b>Part A</b> is{' '}
          {copy.partA}. <b>Part B</b> is {copy.partB}.
        </p>
        <p className="note">
          {cards.length} papers &middot; about {Math.round(minutes / 60)} hours end to end
          &middot; {done} marked done
        </p>
      </div>

      {groups.map((group) => (
        <div key={group}>
          {groups.length > 1 && (
            <h3 className="doinggroup">
              {group.replace(/^Learn by doing:?\s*/i, '') || 'Sit each module'}
            </h3>
          )}
          {cards
            .filter((c) => c.part === group)
            .map((c) => (
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
        </div>
      ))}
    </>
  );
}
