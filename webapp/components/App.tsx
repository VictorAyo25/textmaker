'use client';

import { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { courseByCode } from '@/data/courses';
import { presentQuestion, selectQuestions, shuffle } from '@/lib/bank';
import { markAll } from '@/lib/grading';
import type {
  FeedbackMode,
  GapMode,
  Marked,
  Paper,
  Question,
  Response,
} from '@/lib/types';
import Setup, { type StartArgs } from './Setup';
import Runner from './Runner';
import Review from './Review';
import Sheet from './Sheet';
import AuthBar from './AuthBar';

type Stage = 'setup' | 'running' | 'review' | 'export';

interface Attempt {
  title: string;
  percent: number;
  total: number;
  created_at: string;
}

// History is kept per course, so a TMC221 run never shows up under IFT222. The
// bare v1 key was TMC221's before the platform took a second course, and it is
// still read for that one so nobody loses their existing history.
const historyKey = (code: string) =>
  code === 'TMC221' ? 'tmc-drill-history-v1' : `drill-history-v1:${code}`;

export default function App({
  code,
  authEnabled,
  hasCrashCourse = false,
}: {
  code: string;
  authEnabled: boolean;
  hasCrashCourse?: boolean;
}) {
  const course = courseByCode(code);
  const HISTORY_KEY = historyKey(course.code);
  const [stage, setStage] = useState<Stage>('setup');
  // A lesson can hand off to the drill with ?topic=8, which preselects that
  // topic here. Read after mount, so the server and client first paint agree.
  const [initialModules, setInitialModules] = useState<number[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [gapMode, setGapMode] = useState<GapMode>('typed');
  const [feedback, setFeedback] = useState<FeedbackMode>('end');
  const [timeLimit, setTimeLimit] = useState<number | null>(null);
  const [marked, setMarked] = useState<Marked[]>([]);
  const [title, setTitle] = useState('');
  const [sheet, setSheet] = useState<{ questions: Question[]; title: string }>({
    questions: [],
    title: '',
  });
  const [history, setHistory] = useState<Attempt[]>([]);
  const [synced, setSynced] = useState(false);

  const loadHistory = useCallback(async () => {
    // The server is asked first. It answers with an empty, unsynced list when
    // nobody is signed in or Supabase is not configured, and we fall back to
    // whatever this browser remembers.
    try {
      const res = await fetch(`/api/attempts?course=${encodeURIComponent(course.code)}`);
      const json = await res.json();
      if (json.synced) {
        setSynced(true);
        setHistory(json.attempts ?? []);
        return;
      }
    } catch {
      /* offline or not deployed with a database: fall through */
    }
    setSynced(false);
    try {
      const raw = localStorage.getItem(HISTORY_KEY);
      setHistory(raw ? JSON.parse(raw) : []);
    } catch {
      /* storage blocked: history is simply unavailable */
    }
  }, [course.code, HISTORY_KEY]);

  useEffect(() => {
    void loadHistory();
  }, [loadHistory]);

  useEffect(() => {
    const wanted = new URLSearchParams(window.location.search)
      .getAll('topic')
      .flatMap((t) => t.split(','))
      .map(Number)
      .filter((n) => course.modules.some((m) => m.number === n));
    if (wanted.length) setInitialModules(wanted);
  }, [course]);

  const remember = async (a: Attempt, earned: number) => {
    const next = [a, ...history].slice(0, 50);
    setHistory(next);
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(next.slice(0, 12)));
    } catch {
      /* ignore */
    }
    try {
      await fetch('/api/attempts', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          course: course.code,
          title: a.title,
          percent: a.percent,
          total: a.total,
          earned,
        }),
      });
    } catch {
      /* a failed sync must not disturb the results screen */
    }
  };

  const begin = (
    qs: Question[],
    mode: GapMode,
    limit: number | null,
    label: string,
    fb: FeedbackMode
  ) => {
    setQuestions(qs);
    setGapMode(mode);
    setTimeLimit(limit);
    setTitle(label);
    setFeedback(fb);
    setStage('running');
    if (typeof window !== 'undefined') window.scrollTo(0, 0);
  };

  const onStart = ({ config, timeLimitSec }: StartArgs) => {
    const sel = selectQuestions(course, config);
    if (!sel.questions.length) return;
    const prepared = sel.questions.map((q) => presentQuestion(q, config.shuffleOptions));
    const noun = course.moduleNoun;
    const mods = config.modules.length
      ? `${noun}${config.modules.length === 1 ? '' : 's'} ${[...config.modules]
          .sort((a, b) => a - b)
          .join(', ')}`
      : `All ${noun.toLowerCase()}s`;
    const drawn = config.source === 'exam' ? ' · past questions only' : '';
    begin(
      prepared,
      config.gapMode,
      timeLimitSec,
      `${mods} · ${sel.actual.easy} easy, ${sel.actual.medium} medium, ${sel.actual.hard} hard${drawn}`,
      config.feedback
    );
  };

  const onStartPaper = (paper: Paper, limit: number | null, fb: FeedbackMode) => {
    begin(paper.questions, 'choice', limit, paper.title, fb);
  };

  const onFinish = (responses: (Response | null)[]) => {
    const m = markAll(questions, responses);
    setMarked(m);
    setStage('review');
    const earned = m.reduce((t, x) => t + x.fraction, 0);
    void remember(
      {
        title,
        percent: m.length ? Math.round((earned / m.length) * 100) : 0,
        total: m.length,
        created_at: new Date().toISOString(),
      },
      earned
    );
    if (typeof window !== 'undefined') window.scrollTo(0, 0);
  };

  const onExport = (qs: Question[], label: string) => {
    setSheet({ questions: qs, title: label });
    setStage('export');
    if (typeof window !== 'undefined') window.scrollTo(0, 0);
  };

  const retryWrong = (qs: Question[]) => {
    begin(shuffle(qs), gapMode, null, `Retry: ${qs.length} you missed`, feedback);
  };

  return (
    <main className="wrap" data-course={course.code}>
      <header className="masthead">
        <span className="code">{course.code}</span>
        <h1>{course.title}</h1>
        <span className="sub">{course.tagline}</span>
        <Link className="backlink" href="/">
          All courses
        </Link>
      </header>

      {stage === 'setup' && (
        <>
          <div className="authbar">
            <AuthBar authEnabled={authEnabled} />
          </div>
          {hasCrashCourse && (
            <Link className="card crashcard" href={`/${course.code.toLowerCase()}/learn`}>
              <span>
                <span className="t">Never studied this? Start with the crash course</span>
                <br />
                <span className="b">
                  The whole course taught from zero in programmed steps: one small step
                  at a time, and you answer before the page tells you anything. Worked
                  examples, the traps, and the real paper answered in full.
                </span>
              </span>
              <span className="cnt">Learn it</span>
            </Link>
          )}
          <Setup
            key={initialModules.join(',')}
            course={course}
            initialModules={initialModules}
            onStart={onStart}
            onStartPaper={onStartPaper}
            onExport={onExport}
          />
          {history.length > 0 && (
            <div className="card" style={{ marginTop: 22 }}>
              <h2>Your recent attempts</h2>
              <p className="help">
                {synced
                  ? 'Saved to your account, so they follow you between devices.'
                  : 'Kept in this browser only. Sign in to carry them between devices.'}
              </p>
              <ul className="plain">
                {history.slice(0, 12).map((h, idx) => (
                  <li key={idx}>
                    <b>{h.percent}%</b> &middot; {h.total} questions &middot; {h.title}{' '}
                    <span className="note">
                      ({new Date(h.created_at).toLocaleDateString()})
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}

      {stage === 'running' && (
        <Runner
          questions={questions}
          gapMode={gapMode}
          timeLimitSec={timeLimit}
          course={course}
          feedback={feedback}
          onFinish={onFinish}
          onQuit={() => setStage('setup')}
        />
      )}

      {stage === 'review' && (
        <Review
          course={course}
          marked={marked}
          title={title}
          onRetryWrong={retryWrong}
          onAgain={() => {
            void loadHistory();
            setStage('setup');
          }}
        />
      )}

      {stage === 'export' && (
        <Sheet
          course={course}
          questions={sheet.questions}
          title={sheet.title}
          onBack={() => setStage('setup')}
        />
      )}
    </main>
  );
}
