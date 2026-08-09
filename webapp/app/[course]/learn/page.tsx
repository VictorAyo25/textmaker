import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { COURSES, findCourse } from '@/data/courses';
import { courseHasCrashCourse, lessonCards } from '@/data/lessons';
import LessonIndex from '@/components/LessonIndex';
import StudyPlan from '@/components/StudyPlan';

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
