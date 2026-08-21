'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { QUIRA_TOPICS, type QuiraQuestion } from '@/data/quira';

/*
 * The challenge trainer.
 *
 * Two things are being judged tomorrow: speed and accuracy. So this does two
 * things the real app does not.
 *
 * 1. It keeps a clock on every single question, not just on the paper, shows it
 *    live while you answer, and tells you afterwards which questions cost you
 *    time. The practice run was ten questions in 02:54, which is 17.4 seconds
 *    each, but that is what was DONE rather than what wins. The target here is
 *    5 seconds, which is recognition speed: you either know the stem on sight
 *    or you are reading, and reading is what loses. The live chip exists
 *    because at five seconds there is no time to pace yourself by feel.
 * 2. It remembers what you got wrong and weights those questions to the front
 *    of the next paper, so repeat practice is not repeat of the easy ones.
 *
 * Everything else is deliberately identical to the app: four unlettered
 * options, one selection, Previous and Next, and the score screen at the end.
 */

type Screen = 'home' | 'run' | 'done' | 'results' | 'study';
type Mode = 'exam' | 'coach';

interface Props {
  questions: QuiraQuestion[];
}

interface Shown {
  q: QuiraQuestion;
  /** Option ids in the order they are drawn, so nothing sits in a fixed slot. */
  order: string[];
}

interface Store {
  seen: Record<string, { right: number; wrong: number }>;
  papers: { at: number; score: number; total: number; ms: number }[];
}

const KEY = 'quira-mental-exploits-v1';
const EMPTY: Store = { seen: {}, papers: [] };

/** The goal: five seconds a question. Recognition, not reading. */
const TARGET = 5000;
/** What the practice run actually managed, kept only as a reference point. */
const BENCH = 17400;

function load(): Store {
  if (typeof window === 'undefined') return EMPTY;
  try {
    const raw = window.localStorage.getItem(KEY);
    if (!raw) return EMPTY;
    const parsed = JSON.parse(raw) as Store;
    return { seen: parsed.seen ?? {}, papers: parsed.papers ?? [] };
  } catch {
    return EMPTY;
  }
}

function save(s: Store) {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(s));
  } catch {
    /* private mode, or a full quota. Losing history is not worth an error. */
  }
}

/** mm:ss, the way the app prints "02:54". */
function clock(ms: number) {
  const t = Math.max(0, Math.round(ms / 1000));
  return `${String(Math.floor(t / 60)).padStart(2, '0')}:${String(t % 60).padStart(2, '0')}`;
}

function shuffle<T>(items: T[]): T[] {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

/** A+ at 100, matching the grade the app printed on a ten out of ten. */
function grade(pct: number) {
  if (pct >= 100) return 'A+';
  if (pct >= 90) return 'A';
  if (pct >= 80) return 'B';
  if (pct >= 70) return 'C';
  if (pct >= 60) return 'D';
  return 'F';
}

export default function Quira({ questions }: Props) {
  const [screen, setScreen] = useState<Screen>('home');
  const [store, setStore] = useState<Store>(EMPTY);
  const [ready, setReady] = useState(false);

  // paper setup
  const [count, setCount] = useState(10);
  const [mode, setMode] = useState<Mode>('exam');
  const [topics, setTopics] = useState<number[]>([]);

  // the running paper
  const [paper, setPaper] = useState<Shown[]>([]);
  const [at, setAt] = useState(0);
  const [picked, setPicked] = useState<Record<string, string>>({});
  const [spent, setSpent] = useState<Record<string, number>>({});
  const [sheet, setSheet] = useState(false);
  const started = useRef(0);
  const landed = useRef(0);
  const [total, setTotal] = useState(0);
  /** Milliseconds on the question currently open, ticked for the live chip. */
  const [onNow, setOnNow] = useState(0);

  useEffect(() => {
    setStore(load());
    setReady(true);
  }, []);

  // The live per-question clock. Five seconds is too short to feel, so it has
  // to be shown. It resets whenever the question changes, and stops mattering
  // outside the runner.
  useEffect(() => {
    if (screen !== 'run') return;
    setOnNow(0);
    const id = window.setInterval(() => setOnNow(Date.now() - landed.current), 100);
    return () => window.clearInterval(id);
  }, [screen, at]);

  const pool = useMemo(
    () => (topics.length ? questions.filter((q) => topics.includes(q.module)) : questions),
    [questions, topics]
  );

  /**
   * Draw the paper.
   *
   * Anything previously answered wrong comes first, then anything never seen,
   * then the rest. Inside each band the order is random, so sitting the same
   * length twice does not give the same paper.
   */
  const draw = useCallback(
    (n: number) => {
      const wrong: QuiraQuestion[] = [];
      const fresh: QuiraQuestion[] = [];
      const rest: QuiraQuestion[] = [];
      for (const q of pool) {
        const s = store.seen[q.id];
        if (s && s.wrong > 0 && s.wrong >= s.right) wrong.push(q);
        else if (!s) fresh.push(q);
        else rest.push(q);
      }
      const picked = [...shuffle(wrong), ...shuffle(fresh), ...shuffle(rest)].slice(0, n);
      return shuffle(picked).map((q) => ({ q, order: shuffle(q.options.map((o) => o.id)) }));
    },
    [pool, store.seen]
  );

  function begin(n: number) {
    const p = draw(n);
    if (!p.length) return;
    setPaper(p);
    setAt(0);
    setPicked({});
    setSpent({});
    setTotal(0);
    started.current = Date.now();
    landed.current = Date.now();
    setScreen('run');
  }

  /** Bank the time spent on the question being left, then move. */
  const stamp = useCallback((id: string) => {
    const now = Date.now();
    const ms = now - landed.current;
    landed.current = now;
    setSpent((prev) => ({ ...prev, [id]: (prev[id] ?? 0) + ms }));
  }, []);

  function go(next: number) {
    if (next < 0 || next >= paper.length) return;
    stamp(paper[at].q.id);
    setAt(next);
    setSheet(false);
  }

  function choose(id: string) {
    if (mode === 'coach' && picked[paper[at].q.id]) return; // locked once answered
    setPicked((p) => ({ ...p, [paper[at].q.id]: id }));
  }

  function submit() {
    stamp(paper[at].q.id);
    setTotal(Date.now() - started.current);
    const next: Store = { seen: { ...store.seen }, papers: [...store.papers] };
    let score = 0;
    for (const { q } of paper) {
      const ok = picked[q.id] === q.answer;
      if (ok) score++;
      const s = next.seen[q.id] ?? { right: 0, wrong: 0 };
      next.seen[q.id] = { right: s.right + (ok ? 1 : 0), wrong: s.wrong + (ok ? 0 : 1) };
    }
    next.papers = [
      ...next.papers,
      { at: Date.now(), score, total: paper.length, ms: Date.now() - started.current },
    ].slice(-40);
    setStore(next);
    save(next);
    setScreen('done');
  }

  const score = useMemo(
    () => paper.reduce((n, { q }) => n + (picked[q.id] === q.answer ? 1 : 0), 0),
    [paper, picked]
  );

  const answered = paper.filter(({ q }) => picked[q.id]).length;
  const pct = paper.length ? Math.round((score / paper.length) * 100) : 0;
  const perQ = paper.length ? total / paper.length : 0;

  if (!ready) return <div className="qx" />;

  // ---------------------------------------------------------------- home ----

  if (screen === 'home' || screen === 'study') {
    const done = store.papers.length;
    const asked = store.papers.reduce((n, p) => n + p.total, 0);
    const best = done ? Math.max(...store.papers.map((p) => (p.score / p.total) * 100)) : 0;
    const avg = done
      ? store.papers.reduce((n, p) => n + (p.score / p.total) * 100, 0) / done
      : 0;
    const shaky = Object.entries(store.seen).filter(([, s]) => s.wrong > 0).length;

    if (screen === 'study') {
      const list = pool.slice(0, 400);
      return (
        <div className="qx">
          <header className="qx-top">
            <div className="qx-top-row">
              <button className="qx-back chip" onClick={() => setScreen('home')} aria-label="Back">
                ‹
              </button>
              <h1 className="qx-title">Study</h1>
              <span className="qx-dot" />
            </div>
            <div style={{ height: 14 }} />
          </header>
          <div className="qx-body tint">
            <p className="qx-hint">
              Every question in the selected passages, with the key and the reason. Read this
              the way you would read the book, then come back and sit a paper against the clock.
            </p>
            {list.map((q, i) => (
              <div className="qx-study" key={q.id}>
                <p className="q">
                  {i + 1}. {q.prompt}
                </p>
                <p className="a">{q.options.find((o) => o.id === q.answer)?.text}</p>
                <p className="e">{q.explanation}</p>
                <p className="qx-src">{q.slides.join(' · ')}</p>
              </div>
            ))}
          </div>
        </div>
      );
    }

    return (
      <div className="qx">
        <header className="qx-top">
          <div className="qx-top-row">
            <span />
            <h1 className="qx-title">Towards Mental Exploits</h1>
            <span className="qx-dot" />
          </div>
          <div style={{ height: 14 }} />
        </header>

        <div className="qx-body tint">
          <div className="qx-hero">
            <h2>Win the challenge</h2>
            <p>
              {questions.length} questions built from all 79 pages, asked the way their generator
              asks them. The target is <strong>5 seconds a question</strong>: recognition, not
              reading. The practice run managed 17.4s, and that is the pace to beat rather than
              the pace to match.
            </p>
          </div>

          <div className="qx-stats">
            <div className="qx-stat">
              <b>{done}</b>
              <span>Papers sat</span>
            </div>
            <div className="qx-stat">
              <b>{asked}</b>
              <span>Questions answered</span>
            </div>
            <div className="qx-stat">
              <b>{done ? `${Math.round(avg)}%` : '—'}</b>
              <span>Average score</span>
            </div>
            <div className="qx-stat">
              <b>{done ? `${Math.round(best)}%` : '—'}</b>
              <span>Best score</span>
            </div>
          </div>

          {shaky > 0 && (
            <div className="qx-warn">
              {shaky} question{shaky === 1 ? '' : 's'} you have missed at least once will be dealt
              first on your next paper until you have them cold.
            </div>
          )}

          <h3 className="qx-section">How many questions</h3>
          <div className="qx-lens">
            {[10, 20, 30, 50].map((n) => (
              <button
                key={n}
                className="qx-chip"
                aria-pressed={count === n}
                onClick={() => setCount(n)}
              >
                {n}
              </button>
            ))}
          </div>
          <p className="qx-hint">
            The two papers in the screenshots were 10 and 30 questions, so drill both. Fifty is
            for stamina.
          </p>

          <h3 className="qx-section">Mode</h3>
          <div className="qx-lens">
            <button className="qx-chip" aria-pressed={mode === 'exam'} onClick={() => setMode('exam')}>
              Exam
            </button>
            <button
              className="qx-chip"
              aria-pressed={mode === 'coach'}
              onClick={() => setMode('coach')}
            >
              Coach
            </button>
          </div>
          <p className="qx-hint">
            Exam behaves like the real thing: answer everything, then mark. Coach marks each
            question the moment you commit and tells you why the other three are wrong, which is
            how you learn the traps.
          </p>

          <h3 className="qx-section">Passages</h3>
          <p className="qx-hint">
            Leave all off to draw from the whole book, which is what the challenge will do.
          </p>
          {QUIRA_TOPICS.map((t) => {
            const on = topics.includes(t.number);
            const n = questions.filter((q) => q.module === t.number).length;
            return (
              <button
                key={t.number}
                className="qx-topic"
                aria-pressed={on}
                onClick={() =>
                  setTopics((prev) =>
                    prev.includes(t.number)
                      ? prev.filter((x) => x !== t.number)
                      : [...prev, t.number]
                  )
                }
              >
                <span>
                  <b>{t.title}</b>
                  <span>{t.pages}</span>
                </span>
                <em>{n}</em>
              </button>
            );
          })}
        </div>

        <div className="qx-foot" style={{ gridTemplateColumns: '1fr 1fr', gap: 12 }}>
          <button className="qx-btn dark" onClick={() => setScreen('study')}>
            Study
          </button>
          <button className="qx-btn" onClick={() => begin(count)} disabled={!pool.length}>
            Start {Math.min(count, pool.length)}
          </button>
        </div>
      </div>
    );
  }

  // ----------------------------------------------------------- the paper ----

  if (screen === 'run') {
    const cur = paper[at];
    const chosen = picked[cur.q.id];
    const locked = mode === 'coach' && Boolean(chosen);
    const last = at === paper.length - 1;

    return (
      <div className="qx">
        <header className="qx-top">
          <div className="qx-top-row">
            <button
              className="qx-back"
              onClick={() => (at === 0 ? setScreen('home') : go(at - 1))}
              aria-label="Back"
            >
              ‹
            </button>
            <h1 className="qx-title">
              {String(at + 1).padStart(2, '0')} of {String(paper.length).padStart(2, '0')}
            </h1>
            <span />
          </div>
          <div className="qx-bar">
            <i style={{ width: `${((at + 1) / paper.length) * 100}%` }} />
          </div>
        </header>

        <div className="qx-body">
          <div className="qx-qrow">
            <p className="qx-qlabel">Question {String(at + 1).padStart(2, '0')}</p>
            <span
              className={`qx-tick ${onNow > BENCH ? 'over' : onNow > TARGET ? 'warn' : 'ok'}`}
              aria-label="Seconds on this question"
            >
              {(onNow / 1000).toFixed(1)}s
            </span>
          </div>
          <h2 className="qx-stem">{cur.q.prompt}</h2>

          <div className="qx-opts">
            {cur.order.map((oid) => {
              const opt = cur.q.options.find((o) => o.id === oid);
              if (!opt) return null;
              const isKey = oid === cur.q.answer;
              const mine = chosen === oid;
              let cls = 'qx-opt';
              if (locked && isKey) cls += ' right';
              else if (locked && mine && !isKey) cls += ' wrong';
              return (
                <button
                  key={oid}
                  className={cls}
                  aria-pressed={mine}
                  disabled={locked}
                  onClick={() => choose(oid)}
                >
                  {opt.text}
                </button>
              );
            })}
          </div>

          {locked && (
            <div className="qx-why">
              <p>
                <strong>{chosen === cur.q.answer ? 'Correct. ' : 'Not this one. '}</strong>
                {cur.q.explanation}
              </p>
              {cur.q.why && (
                <ul>
                  {cur.order.map((oid) => {
                    const text = cur.q.why?.[oid];
                    if (!text) return null;
                    return (
                      <li key={oid} className={oid === cur.q.answer ? 'key' : undefined}>
                        {text}
                      </li>
                    );
                  })}
                </ul>
              )}
              <p className="qx-src">{cur.q.slides.join(' · ')}</p>
            </div>
          )}
        </div>

        <div className="qx-foot">
          <button className="qx-prev" onClick={() => go(at - 1)} disabled={at === 0}>
            Previous
          </button>
          <button className="qx-grid" onClick={() => setSheet(true)} aria-label="Jump to question">
            <i />
            <i />
            <i />
            <i />
          </button>
          <button className="qx-next" onClick={() => (last ? submit() : go(at + 1))}>
            {last ? 'Submit' : 'Next'}
          </button>
        </div>

        {sheet && (
          <div className="qx-sheet-back" onClick={() => setSheet(false)}>
            <div className="qx-sheet" onClick={(e) => e.stopPropagation()}>
              <h3 className="headfont">
                {answered} of {paper.length} answered
              </h3>
              <div className="qx-jump">
                {paper.map(({ q }, i) => (
                  <button
                    key={q.id}
                    className={`${picked[q.id] ? 'done' : ''} ${i === at ? 'here' : ''}`.trim()}
                    onClick={() => go(i)}
                  >
                    {i + 1}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // ------------------------------------------------------------- results ----

  if (screen === 'done') {
    // Three bands rather than pass/fail, because 5s is deliberately hard and a
    // flat "too slow" on every early paper teaches nothing. `slow` counts the
    // questions that actually blew the target, which is the number to work on.
    const band = perQ <= TARGET ? 'good' : perQ <= BENCH ? 'near' : 'slow';
    const overTarget = paper.filter(({ q }) => (spent[q.id] ?? 0) > TARGET).length;
    return (
      <div className="qx">
        <header className="qx-top">
          <div className="qx-top-row">
            <span />
            <span />
            <span className="qx-dot" />
          </div>
          <div style={{ height: 8 }} />
        </header>

        <div className="qx-body qx-done tint">
          <svg className="qx-trophy" viewBox="0 0 120 120" role="img" aria-label="Trophy">
            <path d="M30 22h60v26a30 30 0 0 1-60 0z" fill="#1f7ae0" />
            <path
              d="M30 28H18a4 4 0 0 0-4 4v6a20 20 0 0 0 18 20M90 28h12a4 4 0 0 1 4 4v6a20 20 0 0 1-18 20"
              stroke="#1652f0"
              strokeWidth="6"
              fill="none"
            />
            <rect x="52" y="76" width="16" height="14" fill="#1652f0" />
            <rect x="40" y="90" width="40" height="14" rx="2" fill="#4b9df0" />
            <rect x="34" y="102" width="52" height="7" rx="3" fill="#0f2942" />
            <path
              d="M60 32l6.2 12.5 13.8 2-10 9.7 2.4 13.7L60 63.4 47.6 69.9 50 56.2l-10-9.7 13.8-2z"
              fill="#fff"
            />
          </svg>

          <h2>Quiz Complete!</h2>
          <p className="sub">Here&apos;s how you performed on this session.</p>

          <div className="qx-tiles">
            <div className="qx-tile grade">
              <div className="cap">Grade {grade(pct)}</div>
              <div className="val">{pct}%</div>
            </div>
            <div className="qx-tile score">
              <div className="cap">Score</div>
              <div className="val">
                {score}/{paper.length}
              </div>
            </div>
            <div className="qx-tile time">
              <div className="cap">Time spent</div>
              <div className="val">{clock(total)}</div>
            </div>
          </div>

          <div className={`qx-pace ${band}`}>
            <strong>Pace: {(perQ / 1000).toFixed(1)}s a question.</strong>{' '}
            {band === 'good' && (
              <>
                That is the 5s target. This is recognition speed, not reading speed, and it is
                the pace that wins a contest judged on time. Hold it.
              </>
            )}
            {band === 'near' && (
              <>
                The target is 5s. You are inside the 17.4s the practice run managed, but that is
                the pace to beat, not the pace to match.{' '}
                {overTarget > 0 && (
                  <>
                    {overTarget} of {paper.length} went over 5s, and they are marked below.
                  </>
                )}
              </>
            )}
            {band === 'slow' && (
              <>
                The target is 5s and the practice run managed 17.4s, so this paper is slower than
                both. Speed here comes from recognising the stem on sight, never from reading
                faster, so the fix is more reps rather than more hurry.
              </>
            )}
          </div>

          <div className="qx-btns">
            <button className="qx-btn" onClick={() => begin(count)}>
              Continue Practice
            </button>
            <button className="qx-btn dark" onClick={() => setScreen('results')}>
              Review {score === paper.length ? 'Answers' : 'Mistakes'}
            </button>
            <button className="qx-btn plain" onClick={() => setScreen('home')}>
              Go Home
            </button>
          </div>
        </div>
      </div>
    );
  }

  // The full breakdown, in the app's own layout, with the reasoning added.
  const misses = paper.filter(({ q }) => picked[q.id] !== q.answer);
  return (
    <div className="qx">
      <header className="qx-top">
        <div className="qx-top-row">
          <button className="qx-back chip" onClick={() => setScreen('done')} aria-label="Back">
            ‹
          </button>
          <h1 className="qx-title">Quiz Results</h1>
          <span className="qx-dot" />
        </div>
        <div style={{ height: 14 }} />
      </header>

      <div className="qx-body tint">
        <div className="qx-summary">
          <div className="row">
            <span>Multiple Choice</span>
            <span>{clock(total)}</span>
          </div>
          <div className="big">
            <span className="num">
              {score} <small>/{paper.length}</small>
            </span>
            <span className={`qx-pct ${pct === 100 ? 'good' : 'bad'}`}>{pct}%</span>
          </div>
          <div className={`qx-track ${pct === 100 ? '' : 'bad'}`}>
            <i style={{ width: `${pct}%` }} />
          </div>
        </div>

        <div className="qx-note">
          <span aria-hidden>💡</span>
          <span>
            {pct === 100
              ? `Excellent work! You scored ${score}.0 out of ${paper.length}. Sit it again at a longer length before you stop.`
              : `You scored ${score}.0 out of ${paper.length}. The ${misses.length} you missed ${misses.length === 1 ? 'is' : 'are'} now weighted to the front of your next paper.`}
          </span>
        </div>

        <h2 className="qx-h">Question Breakdown</h2>

        {paper.map(({ q, order }, i) => {
          const mine = picked[q.id];
          const ok = mine === q.answer;
          const mineText = q.options.find((o) => o.id === mine)?.text ?? 'Not answered';
          const keyText = q.options.find((o) => o.id === q.answer)?.text ?? '';
          const t = spent[q.id] ?? 0;
          return (
            <div className={`qx-rcard ${ok ? '' : 'miss'}`} key={q.id}>
              <div className="qx-rhead">
                <span className={`qx-mark ${ok ? 'ok' : 'no'}`}>{ok ? '✓' : '✕'}</span>
                <span className="n">Question {i + 1}</span>
                <span className={`qx-pill ${ok ? 'ok' : 'no'}`}>{ok ? '100%' : '0%'}</span>
              </div>
              <p className="qx-rstem">{q.prompt}</p>
              <hr />
              <dl className="qx-line">
                <dt>Your answer:</dt>
                <dd className={ok ? '' : 'bad'}>{mineText}</dd>
              </dl>
              <dl className="qx-line">
                <dt>Correct answer:</dt>
                <dd className="good">{keyText}</dd>
              </dl>
              <dl className="qx-line">
                <dt>Feedback:</dt>
                <dd style={{ fontWeight: 500 }}>
                  {ok ? 'Correct!' : `Incorrect. The correct answer was: ${keyText}`}
                </dd>
              </dl>

              <div className="qx-why">
                <p>{q.explanation}</p>
                {q.why && (
                  <ul>
                    {order.map((oid) => {
                      const text = q.why?.[oid];
                      if (!text) return null;
                      return (
                        <li key={oid} className={oid === q.answer ? 'key' : undefined}>
                          {text}
                        </li>
                      );
                    })}
                  </ul>
                )}
                <p className="qx-src">
                  {q.slides.join(' · ')} ·{' '}
                  <span className={t > TARGET ? 'slowq' : undefined}>
                    {(t / 1000).toFixed(1)}s spent{t > TARGET ? ', over the 5s target' : ''}
                  </span>
                </p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="qx-foot" style={{ gridTemplateColumns: '1fr 1fr', gap: 12 }}>
        <button className="qx-btn dark" onClick={() => setScreen('home')}>
          Go Home
        </button>
        <button className="qx-btn" onClick={() => begin(count)}>
          Practice again
        </button>
      </div>
    </div>
  );
}
