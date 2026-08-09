'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import {
  archivedSet,
  pullSettings,
  pushSettings,
  readSettings,
  toggleArchived,
  type Settings,
} from '@/lib/settings';

export interface CourseCard {
  code: string;
  title: string;
  blurb: string;
  questions: number;
  modules: number;
  moduleNoun: string;
  papers: number;
  lessons: number;
  taken: boolean;
}

/**
 * The course list, split into what is still ahead of THIS reader and what they
 * have already sat.
 *
 * Which is which used to be the author's judgement, baked into the course
 * table. Two people using the platform have sat different papers, so each
 * reader now files their own, and the author's flags are only the starting
 * position. Filing a course away does not close it: the drill stays open,
 * because revision does not stop at the exam hall.
 */
export default function CourseList({ courses }: { courses: CourseCard[] }) {
  const authorTaken = courses.filter((c) => c.taken).map((c) => c.code);
  const [settings, setSettings] = useState<Settings>({});
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setSettings(readSettings());
    setReady(true);
    void pullSettings().then(setSettings);
  }, []);

  // Before the browser has answered, fall back to the author's flags, so the
  // first paint is never wrong, only not yet personal.
  const archived = ready ? archivedSet(settings, authorTaken) : new Set(authorTaken);

  const flip = (code: string) => {
    const next = toggleArchived(settings, authorTaken, code);
    setSettings(next);
    // Written straight away so the split survives a refresh even offline.
    pushSettings(next);
    localStorage.setItem('drill-settings-v1', JSON.stringify(next));
  };

  const live = courses.filter((c) => !archived.has(c.code));
  const done = courses.filter((c) => archived.has(c.code));

  return (
    <>
      <div className="card">
        <h2>Your courses</h2>
        <p className="help">
          {live.length} exam{live.length === 1 ? '' : 's'} still ahead. Tap one to set
          up a test, or mark it sat once the paper is behind you.
        </p>
        {live.map((c) => (
          <Row key={c.code} c={c} archived={false} onFlip={() => flip(c.code)} />
        ))}
        {live.length === 0 && (
          <p className="note">
            Every paper is behind you. Everything below stays open for revision.
          </p>
        )}
      </div>

      {done.length > 0 && (
        <div className="card taken takenhead">
          <h2>Exams already taken</h2>
          <p className="help">
            Sat and done. Kept here for revision, and so your attempts are not lost.
            Put one back if you filed it by mistake.
          </p>
          {done.map((c) => (
            <Row key={c.code} c={c} archived onFlip={() => flip(c.code)} />
          ))}
        </div>
      )}
    </>
  );
}

/**
 * The row is a link, and the archive control is a button beside it rather than
 * inside it: a button nested in a link is unreachable by keyboard and ambiguous
 * to a screen reader.
 */
function Row({
  c,
  archived,
  onFlip,
}: {
  c: CourseCard;
  archived: boolean;
  onFlip: () => void;
}) {
  return (
    <div className="courseline">
      <Link className="modrow courserow" href={`/${c.code.toLowerCase()}`} data-course={c.code}>
        <span className="badge">{c.code}</span>
        <span>
          <span className="t">{c.title}</span>
          <br />
          <span className="b">{c.blurb}</span>
          <br />
          <span className="stat">
            {c.questions} questions &middot; {c.modules} {c.moduleNoun.toLowerCase()}
            {c.modules === 1 ? '' : 's'} &middot; {c.papers} full paper
            {c.papers === 1 ? '' : 's'} to sit
            {c.lessons > 0 && ` · a ${c.lessons}-lesson crash course`}
          </span>
        </span>
        <span className="cnt">{archived ? 'Revise' : 'Start'}</span>
      </Link>
      <button
        type="button"
        className="chip archivebtn"
        onClick={onFlip}
        aria-label={
          archived ? `Move ${c.code} back to your courses` : `Mark ${c.code} as sat`
        }
      >
        {archived ? 'Not sat yet' : 'I have sat this'}
      </button>
    </div>
  );
}
