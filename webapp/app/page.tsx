import Link from 'next/link';
import { COURSES } from '@/data/courses';
import { lessonCards } from '@/data/lessons';

// The landing page. A plain server component: it lists every registered course
// and links into its drill. Registering a course in data/courses.ts is enough
// to make it appear here, so this file never needs editing again.
export default function Page() {
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

      <div className="card">
        <h2>Your courses</h2>
        <p className="help">
          {COURSES.length} course{COURSES.length === 1 ? '' : 's'} loaded. Tap one to set
          up a test.
        </p>
        {COURSES.map((c) => {
          const lessons = lessonCards(c.code).length;
          return (
            <Link
              key={c.code}
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
                  {c.modules.length === 1 ? '' : 's'} &middot; {c.papers.length} full
                  paper{c.papers.length === 1 ? '' : 's'} to sit
                  {lessons > 0 && ` · a ${lessons}-lesson crash course`}
                </span>
              </span>
              <span className="cnt">Start</span>
            </Link>
          );
        })}
      </div>

      <p className="note">
        Results are kept in this browser. Sign in inside a course to carry them between
        devices.
      </p>
    </main>
  );
}
