import { COURSES } from '@/data/courses';
import { lessonCards } from '@/data/lessons';
import Timetable from '@/components/Timetable';
import Providers from '@/components/Providers';
import AuthBar from '@/components/AuthBar';
import CourseList, { type CourseCard } from '@/components/CourseList';
import { authEnabled } from '@/lib/auth';

// The landing page. A server component that lists every registered course and
// hands the split to the client, because which exams are behind you is a
// property of the READER, not of the course. Registering a course in
// data/courses.ts is enough to make it appear here.

export default function Page() {
  // Only what the list draws crosses to the client. The banks themselves are
  // thousands of questions and have no business on this page.
  const cards: CourseCard[] = COURSES.map((c) => ({
    code: c.code,
    title: c.title,
    blurb: c.blurb,
    questions: c.questions.length,
    modules: c.modules.length,
    moduleNoun: c.moduleNoun,
    papers: c.papers.length,
    lessons: lessonCards(c.code).length,
    taken: Boolean(c.taken),
  }));

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

      {/* Sign-in used to live only inside a course, which was fine when one
          person used one laptop. Anyone arriving at the platform should be able
          to sign in before choosing a course, so their progress is carried from
          the first lesson they read rather than from whenever they happened to
          find the control. */}
      <Providers>
        <div className="authbar landingauth">
          <AuthBar authEnabled={authEnabled} />
        </div>
      </Providers>

      <Timetable onDrill={COURSES.filter((c) => c.plan).map((c) => c.code)} />

      <CourseList courses={cards} />

      <p className="note">
        Sign in above to carry your results, your place in every crash course, and
        which papers you have sat, between devices. Without it everything still works,
        kept in this browser.
      </p>
    </main>
  );
}
