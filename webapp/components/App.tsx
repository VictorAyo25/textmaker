'use client';

import { useCallback, useEffect, useState } from 'react';
import { COURSES } from '@/data/courses';
import { presentQuestion, selectQuestions, shuffle } from '@/lib/bank';
import { markAll } from '@/lib/grading';
import type { GapMode, Marked, Paper, Question, Response } from '@/lib/types';
import Setup, { type StartArgs } from './Setup';
import Runner from './Runner';
import Review from './Review';
import AuthBar from './AuthBar';

type Stage = 'setup' | 'running' | 'review';

interface Attempt {
  title: string;
  percent: number;
  total: number;
  created_at: string;
}

const HISTORY_KEY = 'tmc-drill-history-v1';

export default function App({ authEnabled }: { authEnabled: boolean }) {
  const course = COURSES[0];
  const [stage, setStage] = useState<Stage>('setup');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [gapMode, setGapMode] = useState<GapMode>('typed');
  const [timeLimit, setTimeLimit] = useState<number | null>(null);
  const [marked, setMarked] = useState<Marked[]>([]);
  const [title, setTitle] = useState('');
  const [history, setHistory] = useState<Attempt[]>([]);
  const [synced, setSynced] = useState(false);

  const loadHistory = useCallback(async () => {
    // The server is asked first. It answers with an empty, unsynced list when
    // nobody is signed in or Supabase is not configured, and we fall back to
    // whatever this browser remembers.
    try {
      const res = await fetch('/api/attempts');
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
      if (raw) setHistory(JSON.parse(raw));
    } catch {
      /* storage blocked: history is simply unavailable */
    }
  }, []);

  useEffect(() => {
    void loadHistory();
  }, [loadHistory]);

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

  const begin = (qs: Question[], mode: GapMode, limit: number | null, label: string) => {
    setQuestions(qs);
    setGapMode(mode);
    setTimeLimit(limit);
    setTitle(label);
    setStage('running');
    if (typeof window !== 'undefined') window.scrollTo(0, 0);
  };

  const onStart = ({ config, timeLimitSec }: StartArgs) => {
    const sel = selectQuestions(course, config);
    if (!sel.questions.length) return;
    const prepared = sel.questions.map((q) => presentQuestion(q, config.shuffleOptions));
    const mods = config.modules.length
      ? `Modules ${[...config.modules].sort((a, b) => a - b).join(', ')}`
      : 'All modules';
    begin(
      prepared,
      config.gapMode,
      timeLimitSec,
      `${mods} · ${sel.actual.easy} easy, ${sel.actual.medium} medium, ${sel.actual.hard} hard`
    );
  };

  const onStartPaper = (paper: Paper, limit: number | null) => {
    begin(paper.questions, 'choice', limit, paper.title);
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

  const retryWrong = (qs: Question[]) => {
    begin(shuffle(qs), gapMode, null, `Retry: ${qs.length} you missed`);
  };

  return (
    <main className="wrap">
      <header className="masthead">
        <span className="code">{course.code}</span>
        <h1>{course.title}</h1>
        <span className="sub">
          Active recall drilled straight from the study manual. Every answer carries the
          slide it came from.
        </span>
      </header>

      {stage === 'setup' && (
        <>
          <div className="authbar">
            <AuthBar authEnabled={authEnabled} />
          </div>
          <Setup course={course} onStart={onStart} onStartPaper={onStartPaper} />
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
    </main>
  );
}
