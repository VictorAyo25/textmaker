import { COURSES } from '@/data/courses';
import { lessonCards } from '@/data/lessons';
import Timetable from '@/components/Timetable';
import Providers from '@/components/Providers';
import AuthBar from '@/components/AuthBar';
import CourseList, { type CourseCard } from '@/components/CourseList';
import Dashboard, { type DashCourse } from '@/components/Dashboard';
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

  // The reading ORDER comes from the dated plan where a course has one, so the
  // dashboard's "next lesson" is the next one you were actually told to read,
  // not merely the next in the file.
  const cards2 = new Map(COURSES.map((c) => [c.code, lessonCards(c.code)]));
  const dash: DashCourse[] = COURSES.filter((c) => !c.taken).map((c) => {
    const byslug = new Map((cards2.get(c.code) ?? []).map((l) => [l.slug, l]));
    const planned = c.plan ? c.plan.flatMap((s) => s.lessons) : [...byslug.keys()];
    return {
      code: c.code,
      title: c.title,
      examAt: c.exam?.at,
      examWindow: c.exam?.window,
      questions: c.questions.length,
      lessons: byslug.size,
      minutes: [...byslug.values()].reduce((t, l) => t + l.minutes, 0),
      order: planned
        .map((slug) => byslug.get(slug))
        .filter((l): l is NonNullable<typeof l> => Boolean(l))
        .map((l) => ({ slug: l.slug, title: l.title, minutes: l.minutes })),
      hasCrash: byslug.size > 0,
    };
  });

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

      {/* Where you are, before what exists. The dashboard answers the question
          a reader actually has at six in the morning: what do I open now. */}
      <Dashboard courses={dash} />

      <Timetable onDrill={COURSES.filter((c) => c.plan).map((c) => c.code)} />

      <CourseList courses={cards} />

      {/* The side quest. Not a course, not on the timetable, and deliberately
          not in COURSES, so it gets its own way in rather than a course card
          beside the Omega papers. */}
      <a className="sidequest" href="/quira">
        <span className="sq-tag">Side quest</span>
        <strong>Towards Mental Exploits</strong>
        <span className="sq-sub">
          Practice for the Quira challenge, in their app&apos;s own look and against its own
          clock. 419 questions from all 79 pages, target 5 seconds each.
        </span>
        <span className="sq-go" aria-hidden>
          Open the trainer →
        </span>
      </a>

      <p className="note">
        Sign in above to carry your results, your place in every crash course, and
        which papers you have sat, between devices. Without it everything still works,
        kept in this browser.
      </p>
    </main>
  );
}
