import Link from 'next/link';
import { COURSES } from '@/data/courses';
import { courseHasDoing, doingCards, lessonCards } from '@/data/lessons';
import BOOKS from '@/data/question-books.json';
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
  // Only the papers still ahead. Hidden courses stay registered and open at
  // their own URL; they simply do not crowd the front page this week.
  const visible = COURSES.filter((c) => !c.hidden);
  const cards: CourseCard[] = visible.map((c) => ({
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
  const cards2 = new Map(visible.map((c) => [c.code, lessonCards(c.code)]));
  const dash: DashCourse[] = visible.filter((c) => !c.taken).map((c) => {
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
        .map((l) => ({ slug: l.slug, title: l.title, minutes: l.minutes, revision: l.revision })),
      sessions: (c.plan ?? []).map((s) => ({
        date: s.date,
        window: s.window,
        goal: s.goal,
        lessons: s.lessons
          .map((slug) => byslug.get(slug))
          .filter((l): l is NonNullable<typeof l> => Boolean(l))
          .map((l) => ({ slug: l.slug, title: l.title, minutes: l.minutes, revision: l.revision })),
      })),
      hasCrash: byslug.size > 0,
    };
  });

  // Learn by doing, named at the top of the page rather than found inside a
  // course: it is the thing to open when there is a paper this week.
  const doing = visible
    .filter((c) => !c.taken && courseHasDoing(c.code))
    .map((c) => ({ code: c.code, papers: doingCards(c.code).length }));

  return (
    <main className="wrap">
      <header className="masthead">
        <span className="code">CU DRILL</span>
        <h1>Makeup week: four papers, from scratch</h1>
        <span className="sub">
          {/* The week's order lives in the Exam week card below and in each course's
              dated plan, so this line names no course: one hidden course used to
              leave its name here after it had been hidden everywhere else. */}
          Each course teaches you frame by frame, drills you on every objective question
          with every option explained, and gives you the past theory questions to answer in
          your book.
        </span>
      </header>

      {doing.length > 0 && (
        <section className="doingtop">
          <span className="dkick">Learn by doing</span>
          <h2>Sit each module as a paper, then see it worked and taught</h2>
          <p>
            The objective questions on that module, the examiner's own first. Then the
            written questions in the shape that paper sets them, each answered twice: the
            answer you would write in the hall, then the same question taught from
            nothing, one step at a time.
          </p>
          <div className="doinglinks">
            {doing.map((d) => (
              <Link key={d.code} className="dlink" href={`/${d.code.toLowerCase()}/doing`}>
                <b>{d.code}</b>
                <span>{d.papers} papers</span>
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Every question, solved, as a file you can read with no signal and no
          battery anxiety. Built from the same bank by scripts/make-question-book-pdf.mjs,
          so it cannot drift from what the app shows. */}
      <section className="card pdfcard">
        <h2>Question books, as PDFs</h2>
        <p className="help">
          Every question each course owns, the examiner's own tests included, with the
          answer marked, why each wrong option is wrong, and the reasoning under it. The
          same bank the drill uses, printed.
        </p>
        <div className="pdflinks">
          {visible
            .filter((c) => !c.taken && (BOOKS as Record<string, { file: string; pages: number; mb: number }>)[c.code])
            .map((c) => {
              const b = (BOOKS as Record<string, { file: string; pages: number; mb: number }>)[c.code];
              return (
                <a className="pdflink" key={c.code} href={b.file} download>
                  <b>{c.code}</b>
                  <span>
                    {b.pages} pages &middot; {b.mb} MB
                  </span>
                </a>
              );
            })}
          <a className="pdflink all" href={BOOKS.ALL.file} download>
            <b>All three in one</b>
            <span>
              {BOOKS.ALL.pages} pages &middot; {BOOKS.ALL.mb} MB
            </span>
          </a>
        </div>
      </section>

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

      <Timetable
        onDrill={visible.filter((c) => c.plan).map((c) => c.code)}
        omit={COURSES.filter((c) => c.hidden).map((c) => c.code)}
      />

      <CourseList courses={cards} />

      {/* The Quira side quest is filed away for the makeup week. It still
          opens at /quira; it is simply not on the front page. */}

      <p className="note">
        Sign in above to carry your results, your place in every crash course, and
        which papers you have sat, between devices. Without it everything still works,
        kept in this browser.
      </p>
    </main>
  );
}
