import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { findCourse } from '@/data/courses';
import Crumbs from '@/components/Crumbs';
import { SCRIPT_2526 } from '@/data/dts224/script2526';

/**
 * The paper answered as a student would hand it in.
 *
 * Question, then answer, straight through. No teaching, no hooks, no notes on
 * where the marks are; all of that lives on the question pages. This is the
 * script itself, for reading through once you understand the material, or for
 * checking your own attempt against.
 */
export function generateStaticParams() {
  return [{ course: 'dts224' }];
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ course: string }>;
}): Promise<Metadata> {
  const { course } = await params;
  const found = findCourse(course);
  return { title: found ? `The 2025/26 answer script | ${found.code}` : 'Not found' };
}

export default async function Page({ params }: { params: Promise<{ course: string }> }) {
  const { course } = await params;
  const found = findCourse(course);
  if (!found || found.code !== 'DTS224') notFound();

  return (
    <main className="wrap" data-course={found.code}>
      <header className="masthead">
        <span className="code">{found.code}</span>
        <h1>The 2025/26 answer script</h1>
        <span className="sub">Every question answered, as it would be written</span>
        <Link className="backlink" href={`/${found.code.toLowerCase()}/learn`}>
          Back to lessons
        </Link>
      </header>
      <Crumbs
        trail={[
          { label: found.code, href: `/${found.code.toLowerCase()}` },
          { label: 'Crash course', href: `/${found.code.toLowerCase()}/learn` },
          { label: 'Answer script' },
        ]}
        aside={{ label: 'The drill', href: `/${found.code.toLowerCase()}` }}
      />

      <div className="card">
        <p className="help">
          The complete paper, question by question, answered as a student would write it
          on the script. No teaching and no commentary. If you want the reasoning
          instead, each question has its own page under the crash course.
        </p>
      </div>

      {SCRIPT_2526.map((q) => (
        <section key={q.n} className="scriptsec" id={`q${q.n.toLowerCase()}`}>
          <h2 className="scriptq">{q.title.toUpperCase()}</h2>
          <div className="scriptqbody" dangerouslySetInnerHTML={{ __html: q.question }} />
          <h3 className="scripta">Answer</h3>
          <div className="scriptabody" dangerouslySetInnerHTML={{ __html: q.answer }} />
        </section>
      ))}
    </main>
  );
}
