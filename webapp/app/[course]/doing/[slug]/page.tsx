import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { COURSES, findCourse } from '@/data/courses';
import { lessonsFor } from '@/data/lessons';
import LessonView from '@/components/LessonView';
import type { Question } from '@/lib/types';
import { drillQuestions } from '@/lib/lessondrill';
import Crumbs from '@/components/Crumbs';

/** One Learn by doing paper. Same renderer as a lesson, its own section. */
export function generateStaticParams() {
  return COURSES.flatMap((c) =>
    lessonsFor(c.code)
      .filter((l) => l.revision)
      .map((l) => ({ course: c.code.toLowerCase(), slug: l.slug }))
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ course: string; slug: string }>;
}): Promise<Metadata> {
  const { course, slug } = await params;
  const found = findCourse(course);
  const lesson = found && lessonsFor(found.code).find((l) => l.slug === slug && l.revision);
  return { title: lesson ? `${lesson.title} | ${found!.code}` : 'Paper not found' };
}

export default async function Page({
  params,
}: {
  params: Promise<{ course: string; slug: string }>;
}) {
  const { course, slug } = await params;
  const found = findCourse(course);
  if (!found) notFound();
  const papers = lessonsFor(found.code).filter((l) => l.revision);
  const idx = papers.findIndex((l) => l.slug === slug);
  if (idx === -1) notFound();
  const lesson = papers[idx];
  const session = found.plan?.find((s) => s.lessons.includes(slug));
  const when = session ? { date: session.date, window: session.window } : null;

  const moduleTitles: Record<number, string> = {};
  const moduleCounts: Record<number, number> = {};
  for (const m of lesson.modules) {
    moduleTitles[m] = found.modules.find((x) => x.number === m)?.title ?? `Topic ${m}`;
    moduleCounts[m] = found.questions.filter((q) => q.module === m).length;
  }

  const drills: Record<number, Question[]> = {};
  lesson.blocks.forEach((b, i) => {
    if (b.kind === 'drill') drills[i] = drillQuestions(found, lesson, b);
  });

  const brief = (i: number) =>
    papers[i] ? { slug: papers[i].slug, title: papers[i].title } : null;

  return (
    <main className="wrap" data-course={found.code}>
      <header className="masthead">
        <span className="code">{found.code}</span>
        <h1>Learn by doing</h1>
        <span className="sub">{found.title}</span>
        <Link className="backlink" href={`/${found.code.toLowerCase()}/doing`}>
          All papers
        </Link>
      </header>
      <Crumbs
        trail={[
          { label: found.code, href: `/${found.code.toLowerCase()}` },
          { label: 'Learn by doing', href: `/${found.code.toLowerCase()}/doing` },
          { label: lesson.kick },
        ]}
        aside={{ label: 'Crash course', href: `/${found.code.toLowerCase()}/learn` }}
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
        total={papers.length}
        when={when}
        base="doing"
      />
    </main>
  );
}
