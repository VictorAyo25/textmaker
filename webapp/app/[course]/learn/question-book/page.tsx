import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { findCourse } from '@/data/courses';
import Crumbs from '@/components/Crumbs';
import { Sci } from '@/components/Sci';
import { Worked, type WorkedSolution } from '@/components/Worked';
import { Figure } from '@/components/Figure';
import WORKED_TEST1 from '@/data/phy121/worked/test1.json';
import WORKED_TEST2 from '@/data/phy121/worked/test2.json';
import WORKED_DECKS from '@/data/phy121/worked/decks.json';
import WORKED_RECALL from '@/data/phy121/worked/recall.json';
import WORKED_TUTORIAL from '@/data/phy121/worked/tutorial.json';

/**
 * Structured solutions, keyed by question id: both real tests, then the deck
 * calculations, then the recall drills whose one-line answers said WHAT without
 * saying why, then the tutorial questions the examiner has not set yet.
 */
const WORKED: Record<string, WorkedSolution> = {
  ...(WORKED_TEST1 as Record<string, WorkedSolution>),
  ...(WORKED_TEST2 as Record<string, WorkedSolution>),
  ...(WORKED_DECKS as Record<string, WorkedSolution>),
  ...(WORKED_RECALL as Record<string, WorkedSolution>),
  ...(WORKED_TUTORIAL as Record<string, WorkedSolution>),
};
import { answerText, blankedPrompt, buildBook, SPEED } from '@/lib/questionbook';

/**
 * Every question this course owns, solved, arranged by topic and ordered easy
 * to hard.
 *
 * The crash course teaches and then tests. This is the other way round: the
 * questions ARE the spine, and the reasoning hangs off each one. It suits a
 * reader who learns by working through problems rather than by reading first,
 * and it suits the last hours before a paper, when what you want is to see
 * every question you could be asked and why each answer is the answer.
 *
 * Nothing here is authored separately; it is the same bank the drill uses.
 */
export function generateStaticParams() {
  return [{ course: 'phy121' }];
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ course: string }>;
}): Promise<Metadata> {
  const { course } = await params;
  const found = findCourse(course);
  return { title: found ? `Every question, solved | ${found.code}` : 'Not found' };
}

export default async function Page({ params }: { params: Promise<{ course: string }> }) {
  const { course } = await params;
  const found = findCourse(course);
  if (!found) notFound();
  const book = buildBook(found);
  const total = book.reduce((t, b) => t + b.entries.length, 0);

  return (
    <main className="wrap" data-course={found.code}>
      <header className="masthead">
        <span className="code">{found.code}</span>
        <h1>The question book</h1>
        <span className="sub">Every question, solved and explained</span>
        <Link className="backlink" href={`/${found.code.toLowerCase()}/learn`}>
          Back to lessons
        </Link>
      </header>
      <Crumbs
        trail={[
          { label: found.code, href: `/${found.code.toLowerCase()}` },
          { label: 'Crash course', href: `/${found.code.toLowerCase()}/learn` },
          { label: 'Question book' },
        ]}
        aside={{ label: 'The drill', href: `/${found.code.toLowerCase()}` }}
      />

      <div className="card">
        <h2>How this is arranged</h2>
        <p className="help">
          All <b>{total} questions</b> from the lecture slides, the reference sheets and both
          real tests. Grouped by topic, and within each topic ordered <b>easy first</b>, so
          the definitions come before the two-step calculations that assume them.
        </p>
        <p className="note">
          Every question carries the source it came from. Where the same question was set
          twice, it appears once and says where else it was asked. The answer is marked, and
          every other option has a line saying why it fails.
        </p>
        <ul className="bookmap">
          {book.map((t) => (
            <li key={t.number}>
              <a href={`#t${t.number}`}>
                {t.number}. {t.title}
              </a>{' '}
              <span className="note">
                {t.entries.length} questions &middot; {t.counts.easy} easy, {t.counts.medium}{' '}
                medium, {t.counts.hard} hard
              </span>
            </li>
          ))}
        </ul>
      </div>

      {book.map((t) => (
        <section key={t.number} className="everysec" id={`t${t.number}`}>
          <h2 className="everyhead">
            <span className="everynum">{t.number}</span>
            {t.title}
          </h2>
          {SPEED[t.number] && (
            <div className="speedtip">
              <b>Speed tip.</b> {SPEED[t.number]}
            </div>
          )}
          {t.entries.map(({ q, n, source, repeatOf }) => {
            const answers = Array.isArray(q.answer) ? q.answer : [q.answer];
            return (
              <article key={q.id} className="solq">
                <div className="solhead">
                  <span className="soln">
                    {t.number}.{n}
                  </span>
                  <span className={`diffpill ${q.difficulty}`}>{q.difficulty}</span>
                  <span className="solsrc">{source}</span>
                </div>
                {repeatOf && (
                  <p className="repeatnote">
                    <b>Asked twice.</b> This same question also appears as: {repeatOf}.
                  </p>
                )}
                <p className="solprompt">
                  <Sci text={blankedPrompt(q)} />
                </p>
                {/* A question that carried a diagram on the slide or the test
                    must carry it here too, or it cannot be answered. */}
                {q.figure && <Figure figure={q.figure} />}

                {/* The paper's own options first, unmarked, so the question can
                    be attempted. Only then the verdicts. */}
                {q.options && (
                  <ol className="rawopts">
                    {q.options.map((o) => (
                      <li key={o.id}>
                        <Sci text={o.text} />
                      </li>
                    ))}
                  </ol>
                )}

                {/* A gap question offers its words in the blank, so it is
                    attemptable too, and should not be the one style that
                    hands over its answer unasked. */}
                {!q.options &&
                  q.blanks?.map((b, bi) =>
                    b.choices?.length ? (
                      <div key={bi}>
                        {(q.blanks?.length ?? 0) > 1 && (
                          <p className="blanklab">Blank {bi + 1}</p>
                        )}
                        <ol className="rawopts">
                          {b.choices.map((c) => (
                            <li key={c}>
                              <Sci text={c} />
                            </li>
                          ))}
                        </ol>
                      </div>
                    ) : null
                  )}

                {/* Everything below this line gives the answer away, so it is
                    the same line on every question, options or not. */}
                <p className="attemptgap">
                  {q.options ? 'Answer, and why each option is right or wrong' : 'Answer'}
                </p>

                {q.options && (
                  <ul className="solopts">
                    {q.options.map((o) => {
                      const right = answers.includes(o.id);
                      return (
                        <li key={o.id} className={right ? 'solopt right' : 'solopt'}>
                          <span className="soltick">{right ? '✓' : '✗'}</span>
                          <span>
                            <Sci text={o.text} />
                            {q.why?.[o.id] && (
                              <em className="solwhy">
                                <Sci text={q.why[o.id]} />
                              </em>
                            )}
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
                    Answer: <b>{answerText(q)}</b>
                  </p>
                )}

                {WORKED[q.id] && <Worked s={WORKED[q.id]} />}

                {q.explanation && (
                  <p className="solexp">
                    <Sci text={q.explanation} />
                  </p>
                )}
              </article>
            );
          })}
        </section>
      ))}
    </main>
  );
}
