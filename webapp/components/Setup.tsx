'use client';

import { useMemo, useState } from 'react';
import type { Course, Difficulty, Facet, GapMode, Paper, TestConfig } from '@/lib/types';
import { pool, poolByTier } from '@/lib/bank';

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
  onStartPaper: (paper: Paper, timeLimitSec: number | null) => void;
}

export default function Setup({
  course,
  initialModules = [],
  onStart,
  onStartPaper,
}: Props) {
  const [modules, setModules] = useState<number[]>(initialModules);
  const [facets, setFacets] = useState<Facet[]>([]);
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

  const config: TestConfig = { modules, facets, mix, count, gapMode, shuffleOptions };
  const available = useMemo(() => pool(course, config), [course, modules, facets]);
  const tiers = useMemo(() => poolByTier(available), [available]);

  const FACETS = course.facetGuide;
  const noun = course.moduleNoun;
  const nouns = `${noun.toLowerCase()}s`;
  // Typed short answers only exist where the bank has gap or cloze questions.
  // An MCQ-only course would otherwise be offered a setting that does nothing.
  const hasBlanks = useMemo(
    () => course.questions.some((q) => q.style === 'gap' || q.style === 'cloze'),
    [course]
  );

  const countPerModule = useMemo(() => {
    const m: Record<number, number> = {};
    for (const q of course.questions) m[q.module] = (m[q.module] ?? 0) + 1;
    return m;
  }, [course]);

  const toggleModule = (n: number) =>
    setModules((prev) => (prev.includes(n) ? prev.filter((x) => x !== n) : [...prev, n]));

  const toggleFacet = (f: Facet) =>
    setFacets((prev) => (prev.includes(f) ? prev.filter((x) => x !== f) : [...prev, f]));

  const canStart = available.length > 0 && count > 0;
  const effectiveCount = Math.min(count, available.length);

  return (
    <>
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

        {hasBlanks && (
          <>
            <p className="help" style={{ marginBottom: 6 }}>
              Short-answer blanks: type the answer from memory, or pick it from a
              dropdown like the real Moodle test. Long cloze continuations are always
              dropdowns.
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
            </div>
          </>
        )}

        <p className="help" style={{ margin: hasBlanks ? '16px 0 6px' : '0 0 6px' }}>
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
                onClick={() => onStartPaper(p, null)}
              >
                Sit it untimed
              </button>
              <button
                type="button"
                className="btn ghost"
                onClick={() => onStartPaper(p, mins * 60)}
              >
                Sit it in {mins} minutes
              </button>
            </div>
          </div>
        );
      })}
    </>
  );
}
