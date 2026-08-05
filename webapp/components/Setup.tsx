'use client';

import { useMemo, useState } from 'react';
import type {
  Course,
  Difficulty,
  Facet,
  FeedbackMode,
  GapMode,
  Paper,
  Question,
  SourceFilter,
  TestConfig,
} from '@/lib/types';
import { pastCount, pool, poolByTier } from '@/lib/bank';

const PRESETS: { name: string; mix: Record<Difficulty, number> }[] = [
  { name: 'Warm up', mix: { easy: 60, medium: 30, hard: 10 } },
  { name: 'Balanced', mix: { easy: 30, medium: 40, hard: 30 } },
  { name: 'Exam hard', mix: { easy: 10, medium: 30, hard: 60 } },
  { name: 'Brutal', mix: { easy: 0, medium: 20, hard: 80 } },
];

export interface StartArgs {
  config: TestConfig;
  timeLimitSec: number | null;
}

interface Props {
  course: Course;
  /** Preselected topics, set when a crash-course lesson hands off to the drill. */
  initialModules?: number[];
  onStart: (args: StartArgs) => void;
  onStartPaper: (
    paper: Paper,
    timeLimitSec: number | null,
    fb: FeedbackMode,
    perPage: number
  ) => void;
  onExport: (questions: Question[], title: string) => void;
}

export default function Setup({
  course,
  initialModules = [],
  onStart,
  onStartPaper,
  onExport,
}: Props) {
  const [modules, setModules] = useState<number[]>(initialModules);
  const [facets, setFacets] = useState<Facet[]>([]);
  const [source, setSource] = useState<SourceFilter>('all');
  const [mix, setMix] = useState<Record<Difficulty, number>>({
    easy: 30,
    medium: 40,
    hard: 30,
  });
  const [count, setCount] = useState(20);
  const [gapMode, setGapMode] = useState<GapMode>('typed');
  const [timed, setTimed] = useState(false);
  const [minutes, setMinutes] = useState(20);
  const [shuffleOptions, setShuffleOptions] = useState(true);
  const [feedback, setFeedback] = useState<FeedbackMode>('end');
  const [perPage, setPerPage] = useState(1);

  const config: TestConfig = {
    modules,
    facets,
    source,
    mix,
    count,
    gapMode,
    shuffleOptions,
    feedback,
    perPage,
  };
  const available = useMemo(
    () => pool(course, config),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [course, modules, facets, source]
  );
  const tiers = useMemo(() => poolByTier(available), [available]);

  const FACETS = course.facetGuide;
  const noun = course.moduleNoun;
  const nouns = `${noun.toLowerCase()}s`;
  // Offered only where it would actually change the draw: a course with no past
  // questions has nothing to filter to, and one whose bank IS the past papers
  // has nothing to filter out.
  const past = useMemo(() => pastCount(course), [course]);
  const offerSource = past > 0 && past < course.questions.length;
  // Typed short answers only exist where the bank has gap or cloze questions.
  // An MCQ-only course would otherwise be offered a setting that does nothing.
  const hasBlanks = useMemo(
    () => course.questions.some((q) => q.style === 'gap' || q.style === 'cloze'),
    [course]
  );

  // Counted through the source filter, so the per-module figure never promises
  // questions the current draw cannot supply.
  const countPerModule = useMemo(() => {
    const m: Record<number, number> = {};
    for (const q of pool(course, { ...config, modules: [], facets: [] }))
      m[q.module] = (m[q.module] ?? 0) + 1;
    return m;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [course, source]);

  const toggleModule = (n: number) =>
    setModules((prev) => (prev.includes(n) ? prev.filter((x) => x !== n) : [...prev, n]));

  const toggleFacet = (f: Facet) =>
    setFacets((prev) => (prev.includes(f) ? prev.filter((x) => x !== f) : [...prev, f]));

  const canStart = available.length > 0 && count > 0;
  const effectiveCount = Math.min(count, available.length);

  // The printable sheet honours the topic, specifics and source choices above,
  // but not the difficulty mix or the question count: it is the whole of what
  // you selected, which is the point of taking it away.
  const selectionLabel = modules.length
    ? `${noun}${modules.length === 1 ? '' : 's'} ${[...modules].sort((a, b) => a - b).join(', ')}`
    : `All ${nouns}`;
  const exportTitle =
    selectionLabel +
    (facets.length ? ` · ${FACETS.filter((f) => facets.includes(f.id)).map((f) => f.label).join(', ')}` : '') +
    (source === 'exam' ? ' · past questions only' : '');

  return (
    <>
      {offerSource && (
        <div className="card">
          <h2>Where should the questions come from?</h2>
          <p className="help">
            The whole bank covers every corner of the course. The past questions are
            only the ones the examiner actually set, in their own words.
          </p>
          <div className="seg">
            <button
              type="button"
              aria-pressed={source === 'all'}
              onClick={() => setSource('all')}
            >
              The whole bank ({course.questions.length})
            </button>
            <button
              type="button"
              aria-pressed={source === 'exam'}
              onClick={() => setSource('exam')}
            >
              Past test questions only ({past})
            </button>
          </div>
        </div>
      )}

      <div className="card">
        <h2>1. What do you want to be tested on?</h2>
        <p className="help">
          Leave every box unticked to mix all {course.modules.length} {nouns}. Tick one
          to drill it alone, or tick several to mix just those.
        </p>
        {course.modules.map((m) => (
          <button
            type="button"
            key={m.number}
            className="modrow"
            aria-pressed={modules.includes(m.number)}
            onClick={() => toggleModule(m.number)}
          >
            <span className="box">{modules.includes(m.number) ? '✓' : ''}</span>
            <span>
              <span className="t">
                {noun} {m.number}: {m.title}
              </span>
              <br />
              <span className="b">{m.blurb}</span>
            </span>
            <span className="cnt">{countPerModule[m.number] ?? 0} Q</span>
          </button>
        ))}
        <div className="footer-actions">
          <button
            type="button"
            className="chip"
            onClick={() => setModules(course.modules.map((m) => m.number))}
          >
            Select all
          </button>
          <button type="button" className="chip" onClick={() => setModules([])}>
            Clear (mix everything)
          </button>
          <span className="note">
            {available.length} question{available.length === 1 ? '' : 's'} match your
            current selection
          </span>
        </div>
      </div>

      <div className="card">
        <h2>2. Only test me on specifics</h2>
        <p className="help">
          Optional. Tick any of these to restrict the paper to questions that hang on a
          hard, quotable detail. Leave them all off for the full range.
        </p>
        <div className="chips">
          {FACETS.map((f) => (
            <button
              type="button"
              key={f.id}
              className="chip"
              aria-pressed={facets.includes(f.id)}
              title={f.help}
              onClick={() => toggleFacet(f.id)}
            >
              {f.label}
            </button>
          ))}
        </div>
        {facets.length > 0 && (
          <p className="note" style={{ marginTop: 10 }}>
            {FACETS.filter((f) => facets.includes(f.id))
              .map((f) => f.help)
              .join(' · ')}
          </p>
        )}
      </div>

      <div className="card">
        <h2>3. How hard?</h2>
        <p className="help">
          Easy is one fact recalled straight. Medium makes you tell near-misses apart.
          Hard is scenarios, exact figures, orderings and multi-step working.
        </p>
        <div className="chips">
          {PRESETS.map((p) => (
            <button
              type="button"
              key={p.name}
              className="chip"
              aria-pressed={
                mix.easy === p.mix.easy &&
                mix.medium === p.mix.medium &&
                mix.hard === p.mix.hard
              }
              onClick={() => setMix(p.mix)}
            >
              {p.name}
              <span className="n">
                {p.mix.easy}/{p.mix.medium}/{p.mix.hard}
              </span>
            </button>
          ))}
        </div>
        <div className="mixgrid">
          {(['easy', 'medium', 'hard'] as Difficulty[]).map((t) => (
            <div key={t}>
              <label htmlFor={`mix-${t}`}>
                {t} % <span className="note">({tiers[t].length} available)</span>
              </label>
              <input
                id={`mix-${t}`}
                type="number"
                min={0}
                max={100}
                value={mix[t]}
                onChange={(e) =>
                  setMix({ ...mix, [t]: Math.max(0, Number(e.target.value) || 0) })
                }
              />
            </div>
          ))}
        </div>
        <p className="note" style={{ marginTop: 8 }}>
          The three are treated as a ratio, so they do not have to add to 100. If a tier
          runs dry the shortfall is taken from the nearest tier, and the result screen
          tells you what you actually sat.
        </p>
      </div>

      <div className="card">
        <h2>4. How many questions?</h2>
        <div className="chips">
          {[10, 20, 30, 50].map((n) => (
            <button
              type="button"
              key={n}
              className="chip"
              aria-pressed={count === n}
              onClick={() => setCount(n)}
            >
              {n}
            </button>
          ))}
          <button
            type="button"
            className="chip"
            aria-pressed={count === available.length && available.length > 0}
            onClick={() => setCount(available.length)}
          >
            Everything ({available.length})
          </button>
        </div>
        <div style={{ marginTop: 12, maxWidth: 220 }}>
          <label htmlFor="count" className="note">
            or type a number
          </label>
          <input
            id="count"
            type="number"
            min={1}
            max={Math.max(1, available.length)}
            value={count}
            onChange={(e) => setCount(Math.max(1, Number(e.target.value) || 1))}
          />
        </div>
        {count > available.length && (
          <div className="warn">
            Only {available.length} questions match your filters, so the paper will be{' '}
            {available.length} long rather than {count}.
          </div>
        )}
      </div>

      <div className="card">
        <h2>5. How should it run?</h2>

        <p className="help" style={{ marginBottom: 6 }}>
          When do you want to be told how you did?
        </p>
        <div className="seg">
          <button
            type="button"
            aria-pressed={feedback === 'end'}
            onClick={() => setFeedback('end')}
          >
            Mark it at the end
          </button>
          <button
            type="button"
            aria-pressed={feedback === 'instant'}
            onClick={() => setFeedback('instant')}
          >
            Tell me after every question
          </button>
        </div>
        <p className="note" style={{ marginTop: 6 }}>
          {feedback === 'end'
            ? 'Exam conditions: answer everything, then see the score and the full review.'
            : 'Learning mode: the moment you commit an answer the page says right or wrong, why the answer is the answer, what is wrong with each other option, and where in the course it came from. Once shown, that question locks.'}
        </p>

        {hasBlanks && (
          <>
            <p className="help" style={{ margin: '16px 0 6px' }}>
              Short-answer blanks: type the answer from memory, pick it from a dropdown
              like the real Moodle test, or mix the two. Long cloze continuations are
              always dropdowns.
            </p>
            <div className="seg">
              <button
                type="button"
                aria-pressed={gapMode === 'typed'}
                onClick={() => setGapMode('typed')}
              >
                Type it from memory
              </button>
              <button
                type="button"
                aria-pressed={gapMode === 'choice'}
                onClick={() => setGapMode('choice')}
              >
                Choose from a dropdown
              </button>
              <button
                type="button"
                aria-pressed={gapMode === 'mixed'}
                onClick={() => setGapMode('mixed')}
              >
                Mix the two
              </button>
            </div>
            {gapMode === 'mixed' && (
              <p className="note" style={{ marginTop: 6 }}>
                Each short-answer question is decided on its own when the paper starts,
                so you will not know which is coming until you reach it.
              </p>
            )}
          </>
        )}

        <p className="help" style={{ margin: '16px 0 6px' }}>
          How many questions on screen at a time? One at a time is the real test.
          Longer pages let you read ahead and answer in any order without pressing
          Next.
        </p>
        <div className="seg">
          {[
            { n: 1, label: 'One' },
            { n: 5, label: 'Five' },
            { n: 10, label: 'Ten' },
            { n: 0, label: 'All of them' },
          ].map((o) => (
            <button
              key={o.n}
              type="button"
              aria-pressed={perPage === o.n}
              onClick={() => setPerPage(o.n)}
            >
              {o.label}
            </button>
          ))}
        </div>

        <p className="help" style={{ margin: '16px 0 6px' }}>
          Clock.
        </p>
        <div className="seg">
          <button type="button" aria-pressed={!timed} onClick={() => setTimed(false)}>
            Untimed
          </button>
          <button type="button" aria-pressed={timed} onClick={() => setTimed(true)}>
            Timed
          </button>
        </div>
        {timed && (
          <div style={{ marginTop: 10, maxWidth: 220 }}>
            <label htmlFor="mins" className="note">
              minutes for the whole paper
            </label>
            <input
              id="mins"
              type="number"
              min={1}
              max={240}
              value={minutes}
              onChange={(e) => setMinutes(Math.max(1, Number(e.target.value) || 1))}
            />
            <p className="note" style={{ marginTop: 6 }}>
              The real test allowed roughly one minute per question. When the clock hits
              zero the paper submits itself with whatever you have.
            </p>
          </div>
        )}

        <p className="help" style={{ margin: '16px 0 6px' }}>
          Option order.
        </p>
        <div className="seg">
          <button
            type="button"
            aria-pressed={shuffleOptions}
            onClick={() => setShuffleOptions(true)}
          >
            Shuffle options
          </button>
          <button
            type="button"
            aria-pressed={!shuffleOptions}
            onClick={() => setShuffleOptions(false)}
          >
            Keep original order
          </button>
        </div>
      </div>

      <button
        type="button"
        className="btn wide"
        disabled={!canStart}
        onClick={() => onStart({ config, timeLimitSec: timed ? minutes * 60 : null })}
      >
        Start test ({effectiveCount} question{effectiveCount === 1 ? '' : 's'}
        {timed ? `, ${minutes} min` : ', untimed'})
      </button>

      <div className="card" style={{ marginTop: 22 }}>
        <h2>Take the questions with you</h2>
        <p className="help">
          Every question in the selection above, printed with its answer, its
          explanation, the verdict on each option and the reference it came from. The
          difficulty mix and the question count do not apply here: you get all{' '}
          {available.length} of them.
        </p>
        <button
          type="button"
          className="btn ghost"
          disabled={available.length === 0}
          onClick={() => onExport(available, exportTitle)}
        >
          Printable sheet of all {available.length} question
          {available.length === 1 ? '' : 's'}
        </button>
      </div>

      {course.papers.map((p) => {
        const mins = p.minutes ?? 20;
        return (
          <div className="card" key={p.id} style={{ marginTop: 22 }}>
            <h2>{p.title}</h2>
            <p className="help">{p.subtitle}</p>
            <p className="note" style={{ marginBottom: 12 }}>
              {p.note}
            </p>
            <div className="footer-actions">
              <button
                type="button"
                className="btn ghost"
                onClick={() => onStartPaper(p, null, 'end', perPage)}
              >
                Sit it untimed
              </button>
              <button
                type="button"
                className="btn ghost"
                onClick={() => onStartPaper(p, mins * 60, 'end', perPage)}
              >
                Sit it in {mins} minutes
              </button>
              <button
                type="button"
                className="btn ghost"
                onClick={() => onStartPaper(p, null, 'instant', perPage)}
              >
                Walk me through it
              </button>
            </div>
          </div>
        );
      })}
    </>
  );
}
