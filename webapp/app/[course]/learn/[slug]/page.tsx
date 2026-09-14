import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { COURSES, findCourse } from '@/data/courses';
import { lessonBySlug, lessonsFor } from '@/data/lessons';
import LessonView from '@/components/LessonView';
import type { Question } from '@/lib/types';
import { drillQuestions } from '@/lib/lessondrill';
import Crumbs from '@/components/Crumbs';

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
  // Back and Next follow the DATED plan where there is one, so finishing a
  // lesson leads to the next one you were told to read, not the next in the
  // file, which for Java would have jumped from loops to an optional lesson.
  const inFile = lessonsFor(found.code);
  const planned = (found.plan ?? []).flatMap((s) => s.lessons);
  const lessons = planned.length
    ? [
        ...planned.map((s) => inFile.find((l) => l.slug === s)!).filter(Boolean),
        ...inFile.filter((l) => !planned.includes(l.slug)),
      ]
    : inFile;
  const idx = lessons.findIndex((l) => l.slug === slug);
  if (idx === -1) notFound();
  const lesson = lessons[idx];
  const session = found.plan?.find((s) => s.lessons.includes(slug));
  const when = session ? { date: session.date, window: session.window } : null;

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
      <Crumbs
        trail={[
          { label: found.code, href: `/${found.code.toLowerCase()}` },
          { label: 'Crash course', href: `/${found.code.toLowerCase()}/learn` },
          { label: `${idx + 1}. ${lesson.title}` },
        ]}
        aside={{ label: 'The drill', href: `/${found.code.toLowerCase()}` }}
      />
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
        when={when}
      />
    </main>
  );
}
