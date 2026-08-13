import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { COURSES, findCourse } from '@/data/courses';
import { courseHasCrashCourse, lessonCards } from '@/data/lessons';
import LessonIndex from '@/components/LessonIndex';
import StudyPlan from '@/components/StudyPlan';
import Crumbs from '@/components/Crumbs';

// Only courses that actually have a crash course get a route. The others 404,
// which is what the platform already claims by hiding every link to it.
export function generateStaticParams() {
  return COURSES.filter((c) => courseHasCrashCourse(c.code)).map((c) => ({
    course: c.code.toLowerCase(),
  }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ course: string }>;
}): Promise<Metadata> {
  const { course } = await params;
  const found = findCourse(course);
  return { title: found ? `${found.code} Crash Course` : 'Course not found' };
}

export default async function Page({
  params,
}: {
  params: Promise<{ course: string }>;
}) {
  const { course } = await params;
  const found = findCourse(course);
  if (!found) notFound();
  const cards = lessonCards(found.code);
  if (!cards.length) notFound();

  return (
    <main className="wrap" data-course={found.code}>
      <header className="masthead">
        <span className="code">{found.code}</span>
        <h1>Crash course</h1>
        <span className="sub">
          Zero to a mark, taught in programmed steps. {found.title}.
        </span>
        <Link className="backlink" href={`/${found.code.toLowerCase()}`}>
          The drill
        </Link>
      </header>
      <Crumbs
        trail={[
          { label: found.code, href: `/${found.code.toLowerCase()}` },
          { label: 'Crash course' },
        ]}
        aside={{ label: 'The drill', href: `/${found.code.toLowerCase()}` }}
      />
      {/* The finished paper, answered end to end. Given its own card and a loud
          button because it is the single thing most worth reading last. */}
      {found.code === 'DTS224' && (
        <div className="card">
          <h2>The 2025/26 paper, answered</h2>
          <p className="help">
            All six questions, written out as you would put them on the answer script.
            No teaching and no commentary, just the answers, from Question One to
            Question Six.
          </p>
          <Link className="bigbtn" href={`/${found.code.toLowerCase()}/learn/answer-script`}>
            Open the answer script
          </Link>
        </div>
      )}

      {/* With hours left rather than days, navigating between lessons is friction.
          This offers the whole course as one continuous scroll instead. */}
      <div className="card">
        <h2>Short of time?</h2>
        <p className="help">
          Read <b>everything on one page</b>: every lesson, the solved past paper, every
          test question and every drill, in reading order, with nothing to click between
          them.
        </p>
        <div className="chips">
          <Link className="chip" href={`/${found.code.toLowerCase()}/learn/everything`}>
            Open everything on one page
          </Link>
          <Link className="chip" href={`/${found.code.toLowerCase()}/learn/question-book`}>
            The question book: every question by topic
          </Link>
          <Link className="chip" href={`/${found.code.toLowerCase()}/learn/solutions`}>
            Every question solved and explained
          </Link>
        </div>
        <p className="note">
          The first is the course in reading order. The second shows every answer
          already, with the reasoning written out, which is what you want when you are
          meeting something for the first time rather than testing yourself on it.
        </p>
      </div>
      {found.plan && (
        <StudyPlan
          code={found.code}
          plan={found.plan}
          exam={found.exam}
          cards={cards}
        />
      )}
      <LessonIndex code={found.code} cards={cards} />
    </main>
  );
}
