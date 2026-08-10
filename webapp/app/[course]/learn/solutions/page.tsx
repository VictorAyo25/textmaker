import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { COURSES, findCourse } from '@/data/courses';
import { lessonsFor } from '@/data/lessons';
import LessonView from '@/components/LessonView';
import Crumbs from '@/components/Crumbs';
import LessonDrill from '@/components/LessonDrill';
import type { Course, Question } from '@/lib/types';

/**
 * Every question, solved and explained, in one place.
 *
 * The drill hides the answer until you commit, which is right when you are
 * practising and wrong when you are learning something for the first time with
 * hours to spare. This page is the other mode: the teaching from scratch, then
 * the real paper solved, then every question the examiner set, then every
 * authored question, each with its answer already marked and its reasoning
 * written out, including why each wrong option is wrong.
 *
 * Nothing here is authored separately. The lessons and the bank are the single
 * source; this is a second way of reading them.
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
  return { title: found ? `Every question solved | ${found.code}` : 'Not found' };
}

const isExam = (c: Course, q: Question) =>
  (c.examTags ?? []).some((t) => q.slides.some((s) => s.startsWith(t)));

/** One question, with the answer already shown and the reasoning written out. */
function Solved({ q, n, course }: { q: Question; n: number; course: Course }) {
  const answers = Array.isArray(q.answer) ? q.answer : [q.answer];
  const topic = course.modules.find((m) => m.number === q.module)?.title;

  return (
    <article className="solq">
      <div className="solhead">
        <span className="soln">{n}</span>
        <span className="solsrc">{q.slides.join(' · ')}</span>
        {topic && <span className="soltopic">{topic}</span>}
      </div>
      <p className="solprompt">{q.prompt}</p>

      {q.options && (
        <ul className="solopts">
          {q.options.map((o) => {
            const right = answers.includes(o.id);
            return (
              <li key={o.id} className={right ? 'solopt right' : 'solopt'}>
                <span className="soltick">{right ? '✓' : '✗'}</span>
                <span>
                  {o.text}
                  {q.why?.[o.id] && <em className="solwhy">{q.why[o.id]}</em>}
                </span>
              </li>
            );
          })}
        </ul>
      )}

      {q.pairs && (
        <table className="solpairs">
          <tbody>
            {q.pairs.map((p) => (
              <tr key={p.left}>
                <td>
                  <b>{p.left}</b>
                </td>
                <td>{p.right}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!q.options && !q.pairs && (
        <p className="solans">
          Answer: <b>{answers.join(', ')}</b>
        </p>
      )}

      {q.explanation && <p className="solexp">{q.explanation}</p>}
    </article>
  );
}

export default async function Page({ params }: { params: Promise<{ course: string }> }) {
  const { course } = await params;
  const found = findCourse(course);
  if (!found) notFound();
  const lessons = lessonsFor(found.code);
  if (!lessons.length) notFound();

  // Part 1: teaching from scratch. The from-zero lesson if the course has one,
  // otherwise whatever the course opens with.
  const teach = lessons.filter((l) => ['zero', 'how-to-pass'].includes(l.slug));
  // Part 2: the solved past paper, identified by slug.
  const papers = lessons.filter((l) => /^paper-/.test(l.slug));

  const exam = found.questions.filter((q) => isExam(found, q));
  const authored = found.questions.filter((q) => !isExam(found, q));

  const byTopic = new Map<number, Question[]>();
  for (const q of authored) {
    if (!byTopic.has(q.module)) byTopic.set(q.module, []);
    byTopic.get(q.module)!.push(q);
  }
  const topics = [...byTopic.keys()].sort((a, b) => a - b);

  const empty = { ...found, questions: [] };
  const titles: Record<number, string> = {};
  const counts: Record<number, number> = {};
  for (const m of found.modules) {
    titles[m.number] = m.title;
    counts[m.number] = found.questions.filter((q) => q.module === m.number).length;
  }

  return (
    <main className="wrap" data-course={found.code}>
      <header className="masthead">
        <span className="code">{found.code}</span>
        <h1>Every question, solved</h1>
        <span className="sub">{found.title}</span>
        <Link className="backlink" href={`/${found.code.toLowerCase()}/learn`}>
          Back to lessons
        </Link>
      </header>
      <Crumbs
        trail={[
          { label: found.code, href: `/${found.code.toLowerCase()}` },
          { label: 'Crash course', href: `/${found.code.toLowerCase()}/learn` },
          { label: 'Every question solved' },
        ]}
        aside={{ label: 'The drill', href: `/${found.code.toLowerCase()}` }}
      />

      <div className="card">
        <h2>What is on this page</h2>
        <p className="help">
          Parts 1 to 3 show their answers already, with the reasoning written out and every wrong
          option explained, which is what you want when meeting something the first time. Part 4 is the opposite: you answer first, then it explains. When you want
          to be tested instead, use the drill, which hides the answer until you commit.
        </p>
        <ol className="solmap">
          <li>
            <b>The teaching, from nothing.</b> What the course is about and what every
            term means, built from one worked example.
          </li>
          <li>
            <b>The {papers.length ? '2025/26 paper' : 'past paper'}, solved.</b> Question
            by question, written as you should write it in the hall.
          </li>
          <li>
            <b>Every question the examiner set,</b> {exam.length} of them, each answered
            and explained option by option.
          </li>
          <li>
            <b>Every authored question, answered by you first.</b> {authored.length} more
            covering every unit of the manual, grouped by unit. These do not show the
            answer until you have chosen, because being wrong once teaches more than
            reading a correct answer. Then the answer and every wrong option are
            explained.
          </li>
        </ol>
      </div>

      {teach.map((lesson, i) => (
        <section key={lesson.slug} className="everysec">
          <h2 className="everyhead">
            <span className="everynum">1.{i + 1}</span>
            {lesson.title}
          </h2>
          <LessonView
            code={found.code}
            lesson={lesson}
            moduleTitles={titles}
            moduleCounts={counts}
            prev={null}
            next={null}
            course={empty}
            drills={{}}
            position={i + 1}
            total={lessons.length}
          />
        </section>
      ))}

      {papers.map((lesson, i) => (
        <section key={lesson.slug} className="everysec">
          <h2 className="everyhead">
            <span className="everynum">2.{i + 1}</span>
            {lesson.title}
          </h2>
          <LessonView
            code={found.code}
            lesson={lesson}
            moduleTitles={titles}
            moduleCounts={counts}
            prev={null}
            next={null}
            course={empty}
            drills={{}}
            position={i + 1}
            total={lessons.length}
          />
        </section>
      ))}

      {exam.length > 0 && (
        <section className="everysec">
          <h2 className="everyhead">
            <span className="everynum">3</span>
            Every question the examiner set, solved
          </h2>
          <p className="note">
            {exam.length} questions. The tick marks the answer; the note beside each other
            option says why it fails.
          </p>
          {exam.map((q, i) => (
            <Solved key={q.id} q={q} n={i + 1} course={found} />
          ))}
        </section>
      )}

      {/* Part 4 is ANSWERED, not read. Showing the answer before the reader has
          committed teaches far less than making them choose and be wrong first,
          which is the whole reason the drill exists. So these are live. */}
      {topics.map((t, ti) => (
        <section key={t} className="everysec">
          <h2 className="everyhead">
            <span className="everynum">4.{ti + 1}</span>
            {titles[t] ?? `Topic ${t}`}
          </h2>
          <LessonDrill
            course={empty}
            questions={byTopic.get(t)!}
            label={`Answer these first: ${titles[t] ?? `Topic ${t}`}`}
            tag={`${byTopic.get(t)!.length} questions. Choose, then the answer and every wrong option are explained`}
          />
        </section>
      ))}
    </main>
  );
}
