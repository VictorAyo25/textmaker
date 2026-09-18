import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { COURSES, findCourse } from '@/data/courses';
import { lessonsFor } from '@/data/lessons';
import Crumbs from '@/components/Crumbs';
import BOOKS from '@/data/question-books.json';
import { theoryAsksFor, theoryAskTally } from '@/data/theory-asks';

/**
 * Every theory question this course owns, with its full solution, in one file.
 *
 * The question book is the objective half: thousands of options, each with a
 * line on why it is wrong. This is the other half, the questions you WRITE: the
 * examiner's own past papers, the mock papers, and the questions in the Learn by
 * doing papers, each one as printed, then broken down, then answered in full.
 *
 * Nothing here is authored separately. It is the same lessons the app teaches
 * from, with every answer already open, which is what makes it printable:
 * scripts/make-question-book-pdf.mjs renders this page to a PDF.
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
  return { title: found ? `${found.code} Theory Solutions` : 'Course not found' };
}

function Html({ html, className }: { html: string; className?: string }) {
  return <div className={className} dangerouslySetInnerHTML={{ __html: html }} />;
}

const BOOKMAP = BOOKS as Record<string, { file: string; pages: number; mb: number }>;

export default async function Page({
  params,
}: {
  params: Promise<{ course: string }>;
}) {
  const { course } = await params;
  const found = findCourse(course);
  if (!found) notFound();

  // A lesson belongs in the solutions book when it carries a question the
  // reader has to WRITE: a printed past question, or a model answer.
  //
  // The Learn by doing papers mostly RE-PRESENT the papers' own questions,
  // grouped by topic, so printing both would put the same question in the book
  // twice and double the file. Each printed question is therefore kept once, on
  // the first lesson that carries it, and the teaching lessons come first.
  const seen = new Set<string>();
  const key = (html: string) => html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 300);
  const lessons = lessonsFor(found.code)
    .filter((l) =>
      l.blocks.some((b) => b.kind === 'asprinted' || (b.kind === 'worked' && b.mode === 'model'))
    )
    .map((lesson) => {
      const blocks: typeof lesson.blocks = [];
      let dropping = false;
      for (const b of lesson.blocks) {
        if (b.kind === 'asprinted') {
          const k = key(b.printed);
          dropping = seen.has(k);
          seen.add(k);
          if (dropping) continue;
        } else if (dropping && ['recall', 'worked', 'frames', 'teach'].includes(b.kind)) {
          continue;
        } else if (b.kind === 'heading') {
          dropping = false;
        }
        blocks.push(b);
      }
      return { ...lesson, blocks };
    })
    .filter((l) => l.blocks.some((b) => b.kind === 'asprinted' || b.kind === 'worked'));
  if (!lessons.length) notFound();

  const questions = lessons.reduce(
    (t, l) => t + l.blocks.filter((b) => b.kind === 'asprinted').length,
    0
  );
  const answers = lessons.reduce(
    (t, l) => t + l.blocks.filter((b) => b.kind === 'worked').length,
    0
  );
  const pdf = BOOKMAP[`${found.code}-theory`];
  // The asks that need no calculator, gathered out of the papers and printed
  // FIRST, because they are the marks you can bank before you can compute.
  const asks = theoryAsksFor(found.code);
  const tally = asks ? theoryAskTally(asks) : null;

  return (
    <main className="wrap" data-course={found.code}>
      <header className="masthead">
        <span className="code">{found.code}</span>
        <h1>Theory solutions</h1>
        <span className="sub">Every question you have to write, answered in full</span>
        <Link className="backlink" href={`/${found.code.toLowerCase()}/learn`}>
          The crash course
        </Link>
      </header>
      <Crumbs
        trail={[
          { label: found.code, href: `/${found.code.toLowerCase()}` },
          { label: 'Crash course', href: `/${found.code.toLowerCase()}/learn` },
          { label: 'Theory solutions' },
        ]}
        aside={{ label: 'Question book', href: `/${found.code.toLowerCase()}/learn/question-book` }}
      />

      {pdf && (
        <p className="pdfline noprint">
          <a className="btn" href={pdf.file} download>
            Download this as a PDF
          </a>
          <span className="note">
            {pdf.pages} pages, {pdf.mb} MB, readable with no signal
          </span>
        </p>
      )}

      <div className="card">
        <h2>What is in here</h2>
        <p className="help">
          {questions} questions and {answers} worked answers, from {lessons.length} papers and
          practice sets: the examiner's own past papers, the mock papers, and every written
          question in the Learn by doing section. Each one is quoted as printed, broken down,
          then answered in full.
        </p>
        {tally && (
          <p className="help">
            It opens with <b>every theory ask the examiner has ever made</b>, {tally.asks} of them,
            pulled out of the papers and grouped by what they ask you to do. Then the papers
            themselves, in full.
          </p>
        )}
        <p className="note">
          The objective half lives in the <Link href={`/${found.code.toLowerCase()}/learn/question-book`}>question book</Link>.
        </p>
      </div>

      {asks && tally && (
        <section className="card askbook" id="theory-asks">
          <h2>Every theory ask, asked and answered</h2>
          <p className="help">{asks.lead}</p>
          <p className="askmarks">
            {tally.papers.map((p) => (
              <span className="askmark" key={p.paper}>
                <b>{p.paper}</b> {p.asks} {p.asks === 1 ? 'ask' : 'asks'}, {p.marks} marks
                {p.shared ? ' and a shared block' : ''}
              </span>
            ))}
          </p>
          {asks.groups.map((group) => (
            <div className="askgroup" key={group.kind}>
              <h3 className="lheading">{group.kind}</h3>
              <p className="note">{group.when}</p>
              {group.asks.map((ask) => (
                <div className="askitem" key={ask.id}>
                  <div className="lblock paper">
                    <div className="lbar">
                      <span>As printed</span>
                      <span className="ltag">{ask.topic}</span>
                    </div>
                    <div className="lbody">
                      {ask.context && <p className="src">{ask.context}</p>}
                      {ask.papers.map((source) => (
                        <div className="askquote" key={`${source.paper} ${source.part}`}>
                          <p className="askwhere">
                            {source.paper}, {source.part},{' '}
                            {source.marks === null
                              ? source.note
                              : `${source.marks} ${source.marks === 1 ? 'mark' : 'marks'}`}
                          </p>
                          <p className="asprinted">{source.quote}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="lblock worked model">
                    <div className="lbar">
                      <span>The answer you write in the hall</span>
                    </div>
                    <div className="lbody">
                      <Html html={ask.answer} />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ))}
        </section>
      )}

      {lessons.map((lesson) => (
        <section className="card theorysec" key={lesson.slug}>
          <h2 className="theoryhead">{lesson.title}</h2>
          {lesson.kick && <p className="note">{lesson.kick}</p>}
          {lesson.blocks.map((block, i) => {
            if (block.kind === 'heading')
              return (
                <h3 className="lheading" key={i}>
                  {block.text}
                </h3>
              );
            if (block.kind === 'asprinted')
              return (
                <div className="lblock paper" key={i}>
                  <div className="lbar">
                    <span>{block.label || 'As printed'}</span>
                    {block.tag && <span className="ltag">{block.tag}</span>}
                  </div>
                  <div className="lbody">
                    {block.src && <p className="src">{block.src}</p>}
                    <Html className="asprinted" html={block.printed} />
                  </div>
                </div>
              );
            if (block.kind === 'recall')
              return (
                <div className="lblock recall" key={i}>
                  <div className="lbar">
                    <span>{block.label || 'Break it down first'}</span>
                    {block.tag && <span className="ltag">{block.tag}</span>}
                  </div>
                  <div className="lbody">
                    <Html html={block.question} />
                    <p className="alabel">Answer</p>
                    <Html html={block.answer} />
                  </div>
                </div>
              );
            if (block.kind === 'worked')
              return (
                <div className="lblock worked model" key={i}>
                  <div className="lbar">
                    <span>{block.label || 'Model answer'}</span>
                    {block.tag && <span className="ltag">{block.tag}</span>}
                  </div>
                  <div className="lbody">
                    {block.problem && <Html html={block.problem} />}
                    {block.working && <Html html={block.working} />}
                    {block.answer && <Html className="answerbox" html={block.answer} />}
                  </div>
                </div>
              );
            return null;
          })}
        </section>
      ))}
    </main>
  );
}
