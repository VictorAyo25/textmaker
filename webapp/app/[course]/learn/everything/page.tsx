import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { COURSES, findCourse } from '@/data/courses';
import { lessonsFor } from '@/data/lessons';
import LessonView from '@/components/LessonView';
import type { Question } from '@/lib/types';
import { drillQuestions } from '@/lib/lessondrill';
import Crumbs from '@/components/Crumbs';

/**
 * Everything, on one page.
 *
 * The crash course is split into lessons because that is how it should be read
 * over days. With hours left it is the wrong shape: the reader does not want to
 * navigate, they want to start at the top and not stop. This route renders every
 * lesson in plan order into a single continuous page, teaching first, then the
 * solved paper, then the tests, then the drills, with nothing to click between.
 *
 * It reuses the same lesson blocks rather than copying them, so there is one
 * source of truth. Nothing here is authored: correct a lesson and this page is
 * corrected with it.
 */
export function generateStaticParams() {
  return COURSES.filter((c) => lessonsFor(c.code).length).map((c) => ({
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
  return { title: found ? `Everything on one page | ${found.code}` : 'Not found' };
}

export default async function Page({ params }: { params: Promise<{ course: string }> }) {
  const { course } = await params;
  const found = findCourse(course);
  if (!found) notFound();
  const lessons = lessonsFor(found.code);
  if (!lessons.length) notFound();

  const moduleTitles: Record<number, string> = {};
  const moduleCounts: Record<number, number> = {};
  for (const m of found.modules) {
    moduleTitles[m.number] = m.title;
    moduleCounts[m.number] = found.questions.filter((q) => q.module === m.number).length;
  }

  // Drill selections are resolved per lesson on the server, exactly as the
  // single-lesson route does, so the page ships only the questions asked.
  const drillsFor = lessons.map((lesson) => {
    const d: Record<number, Question[]> = {};
    lesson.blocks.forEach((b, i) => {
      if (b.kind === 'drill') d[i] = drillQuestions(found, lesson, b);
    });
    return d;
  });

  const minutes = lessons.reduce((t, l) => t + (l.minutes ?? 0), 0);
  const parts: string[] = [];
  for (const l of lessons) if (l.part && !parts.includes(l.part)) parts.push(l.part);

  return (
    <main className="wrap" data-course={found.code}>
      <header className="masthead">
        <span className="code">{found.code}</span>
        <h1>Everything, on one page</h1>
        <span className="sub">{found.title}</span>
        <Link className="backlink" href={`/${found.code.toLowerCase()}/learn`}>
          Back to lessons
        </Link>
      </header>
      <Crumbs
        trail={[
          { label: found.code, href: `/${found.code.toLowerCase()}` },
          { label: 'Crash course', href: `/${found.code.toLowerCase()}/learn` },
          { label: 'Everything' },
        ]}
        aside={{ label: 'The drill', href: `/${found.code.toLowerCase()}` }}
      />

      <div className="card">
        <h2>Start at the top and do not stop</h2>
        <p className="help">
          Every lesson, the solved past paper, every test question and every drill, in
          reading order, with nothing to click between them. {lessons.length} sections,
          about {Math.round(minutes / 60)} hours if you read all of it.
        </p>
        <p className="note">
          {parts.join(' · ')}
        </p>
        <p className="note">
          Attempt each worked example on paper before you reveal it. A model answer you
          have not tried teaches you nothing.
        </p>
      </div>

      {lessons.map((lesson, i) => (
        <section key={lesson.slug} className="everysec" id={lesson.slug}>
          <h2 className="everyhead">
            <span className="everynum">{i + 1}</span>
            {lesson.title}
          </h2>
          <LessonView
            code={found.code}
            lesson={lesson}
            moduleTitles={moduleTitles}
            moduleCounts={moduleCounts}
            prev={null}
            next={null}
            course={{ ...found, questions: [] }}
            drills={drillsFor[i]}
            position={i + 1}
            total={lessons.length}
          />
        </section>
      ))}
    </main>
  );
}
