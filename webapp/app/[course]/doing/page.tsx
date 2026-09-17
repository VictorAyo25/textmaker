import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { COURSES, findCourse } from '@/data/courses';
import { courseHasDoing, doingCards } from '@/data/lessons';
import { doingCopy } from '@/data/doing';
import DoingIndex from '@/components/DoingIndex';
import Crumbs from '@/components/Crumbs';

/**
 * Learn by doing: its own section, not a part of the crash course.
 *
 * The crash course teaches. This sits each module as a paper: the objective
 * questions on that module, then the written questions in whatever shape that
 * course's paper sets them, every one answered twice, as you would write it in
 * the hall and then taught from nothing. What Part B holds differs by course,
 * so the words come from data/doing.ts rather than from this page.
 */
export function generateStaticParams() {
  return COURSES.filter((c) => courseHasDoing(c.code)).map((c) => ({
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
  return { title: found ? `${found.code} Learn by Doing` : 'Course not found' };
}

export default async function Page({
  params,
}: {
  params: Promise<{ course: string }>;
}) {
  const { course } = await params;
  const found = findCourse(course);
  if (!found) notFound();
  const cards = doingCards(found.code);
  if (!cards.length) notFound();

  return (
    <main className="wrap" data-course={found.code}>
      <header className="masthead">
        <span className="code">{found.code}</span>
        <h1>Learn by doing</h1>
        <span className="sub">
          Every module sat as a paper, with every answer worked and then taught. {found.title}.
        </span>
        <Link className="backlink" href={`/${found.code.toLowerCase()}`}>
          The drill
        </Link>
      </header>
      <Crumbs
        trail={[
          { label: found.code, href: `/${found.code.toLowerCase()}` },
          { label: 'Learn by doing' },
        ]}
        aside={{ label: 'Crash course', href: `/${found.code.toLowerCase()}/learn` }}
      />
      <DoingIndex code={found.code} cards={cards} copy={doingCopy(found.code)} />
    </main>
  );
}
