import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { COURSES, findCourse } from '@/data/courses';
import { lessonBySlug, lessonsFor } from '@/data/lessons';
import LessonView from '@/components/LessonView';
import type { Question } from '@/lib/types';
import { drillQuestions } from '@/lib/lessondrill';

export function generateStaticParams() {
  return COURSES.flatMap((c) =>
    lessonsFor(c.code).map((l) => ({ course: c.code.toLowerCase(), slug: l.slug }))
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ course: string; slug: string }>;
}): Promise<Metadata> {
  const { course, slug } = await params;
  const found = findCourse(course);
  const lesson = found && lessonBySlug(found.code, slug);
  return { title: lesson ? `${lesson.title} | ${found!.code}` : 'Lesson not found' };
}

export default async function Page({
  params,
}: {
  params: Promise<{ course: string; slug: string }>;
}) {
  const { course, slug } = await params;
  const found = findCourse(course);
  if (!found) notFound();
  const lessons = lessonsFor(found.code);
  const idx = lessons.findIndex((l) => l.slug === slug);
  if (idx === -1) notFound();
  const lesson = lessons[idx];

  // The lesson hands off to the drill, so it needs to name the topics it taught
  // and say how many real questions are waiting on each.
  const moduleTitles: Record<number, string> = {};
  const moduleCounts: Record<number, number> = {};
  for (const m of lesson.modules) {
    moduleTitles[m] = found.modules.find((x) => x.number === m)?.title ?? `Topic ${m}`;
    moduleCounts[m] = found.questions.filter((q) => q.module === m).length;
  }

  // Each drill block's questions are selected here, on the server, so the page
  // ships only the questions this lesson actually asks rather than the bank.
  const drills: Record<number, Question[]> = {};
  lesson.blocks.forEach((b, i) => {
    if (b.kind === 'drill') drills[i] = drillQuestions(found, lesson, b);
  });

  const brief = (i: number) =>
    lessons[i] ? { slug: lessons[i].slug, title: lessons[i].title } : null;

  return (
    <main className="wrap" data-course={found.code}>
      <header className="masthead">
        <span className="code">{found.code}</span>
        <h1>Crash course</h1>
        <span className="sub">{found.title}</span>
        <Link className="backlink" href={`/${found.code.toLowerCase()}/learn`}>
          All lessons
        </Link>
      </header>
      <LessonView
        code={found.code}
        lesson={lesson}
        moduleTitles={moduleTitles}
        moduleCounts={moduleCounts}
        prev={brief(idx - 1)}
        next={brief(idx + 1)}
        course={{ ...found, questions: [] }}
        drills={drills}
        position={idx + 1}
        total={lessons.length}
      />
    </main>
  );
}
