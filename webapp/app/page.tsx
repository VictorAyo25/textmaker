import Link from 'next/link';
import type { Course } from '@/lib/types';
import { COURSES } from '@/data/courses';
import { lessonCards } from '@/data/lessons';
import Timetable from '@/components/Timetable';

// The landing page. A plain server component: it lists every registered course
// and links into its drill. Registering a course in data/courses.ts is enough
// to make it appear here, so this file never needs editing again.
//
// Courses marked `taken` have had their exam sat. They drop below the fold into
// their own group rather than disappearing, because the drill is still the
// fastest revision there is and nobody should lose their history.

function CourseRow({ c }: { c: Course }) {
  const lessons = lessonCards(c.code).length;
  return (
    <Link
      className="modrow courserow"
      href={`/${c.code.toLowerCase()}`}
      data-course={c.code}
    >
      <span className="badge">{c.code}</span>
      <span>
        <span className="t">{c.title}</span>
        <br />
        <span className="b">{c.blurb}</span>
        <br />
        <span className="stat">
          {c.questions.length} questions &middot; {c.modules.length}{' '}
          {c.moduleNoun.toLowerCase()}
          {c.modules.length === 1 ? '' : 's'} &middot; {c.papers.length} full paper
          {c.papers.length === 1 ? '' : 's'} to sit
          {lessons > 0 && ` · a ${lessons}-lesson crash course`}
        </span>
      </span>
      <span className="cnt">{c.taken ? 'Revise' : 'Start'}</span>
    </Link>
  );
}

export default function Page() {
  const live = COURSES.filter((c) => !c.taken);
  const taken = COURSES.filter((c) => c.taken);

  return (
    <main className="wrap">
      <header className="masthead">
        <span className="code">CU DRILL</span>
        <h1>Active recall, built from the study manuals</h1>
        <span className="sub">
          Pick a course. Every question is marked instantly and reviewed in full, with
          the reason the right answer is right and the reason each other option is not.
        </span>
      </header>

      <Timetable onDrill={COURSES.filter((c) => c.plan).map((c) => c.code)} />

      <div className="card">
        <h2>Your courses</h2>
        <p className="help">
          {live.length} exam{live.length === 1 ? '' : 's'} still ahead. Tap one to set up
          a test.
        </p>
        {live.map((c) => (
          <CourseRow key={c.code} c={c} />
        ))}
      </div>

      {taken.length > 0 && (
        <div className="card taken takenhead">
          <h2>Exams already taken</h2>
          <p className="help">
            Sat and done. Kept here for revision, and so your attempts are not lost.
          </p>
          {taken.map((c) => (
            <CourseRow key={c.code} c={c} />
          ))}
        </div>
      )}

      <p className="note">
        Results are kept in this browser. Sign in inside a course to carry them between
        devices.
      </p>
    </main>
  );
}
