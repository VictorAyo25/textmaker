'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import type { GapMode, Question, Response } from '@/lib/types';
import QuestionView from './QuestionView';

const STYLE_LABEL: Record<string, string> = {
  mcq: 'Single choice',
  multi: 'Multiple response',
  tf: 'True or false',
  match: 'Matching',
  cloze: 'Cloze',
  gap: 'Short answer',
};

function clock(sec: number): string {
  const m = Math.floor(Math.max(0, sec) / 60);
  const s = Math.max(0, sec) % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}

interface Props {
  questions: Question[];
  gapMode: GapMode;
  timeLimitSec: number | null;
  /** What this course calls a module group: "Module", "Topic". */
  moduleNoun: string;
  onFinish: (responses: (Response | null)[]) => void;
  onQuit: () => void;
}

export default function Runner({
  questions,
  gapMode,
  timeLimitSec,
  moduleNoun,
  onFinish,
  onQuit,
}: Props) {
  const [i, setI] = useState(0);
  const [responses, setResponses] = useState<(Response | null)[]>(() =>
    questions.map(() => null)
  );
  const [left, setLeft] = useState<number | null>(timeLimitSec);
  const finished = useRef(false);

  const finish = () => {
    if (finished.current) return;
    finished.current = true;
    onFinish(responses);
  };
  // The latest responses must be visible to the timer's callback, which closes
  // over the first render otherwise and would submit an empty paper.
  const latest = useRef(responses);
  latest.current = responses;

  useEffect(() => {
    if (timeLimitSec == null) return;
    const id = setInterval(() => {
      setLeft((prev) => {
        if (prev == null) return prev;
        if (prev <= 1) {
          clearInterval(id);
          if (!finished.current) {
            finished.current = true;
            onFinish(latest.current);
          }
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeLimitSec]);

  const q = questions[i];
  const answered = responses.filter(Boolean).length;
  const pct = Math.round(((i + 1) / questions.length) * 100);

  const setResponse = (r: Response) =>
    setResponses((prev) => {
      const next = [...prev];
      next[i] = r;
      return next;
    });

  const jumpList = useMemo(
    () =>
      questions.map((_, idx) => ({
        idx,
        done: responses[idx] != null,
      })),
    [questions, responses]
  );

  const low = left != null && left <= 60;

  return (
    <>
      <div className="bar">
        <strong style={{ fontSize: '0.9rem' }}>
          Question {i + 1} of {questions.length}
        </strong>
        <span className="progress">
          <i style={{ width: `${pct}%` }} />
        </span>
        {left != null && (
          <strong
            style={{
              fontVariantNumeric: 'tabular-nums',
              color: low ? 'var(--red)' : 'var(--muted)',
              fontSize: '0.95rem',
            }}
            aria-live="polite"
          >
            {clock(left)}
          </strong>
        )}
      </div>

      <div className="card">
        <div className="qmeta">
          <span className="tag">{STYLE_LABEL[q.style] ?? q.style}</span>
          <span className={`tag ${q.difficulty}`}>{q.difficulty}</span>
          <span className="tag">
            {moduleNoun} {q.module}
          </span>
          <span className="tag">{q.topic}</span>
        </div>
        <p className="prompt">
          {q.style === 'cloze' || q.style === 'gap' ? 'Complete the passage.' : q.prompt}
        </p>
        <QuestionView
          question={q}
          response={responses[i]}
          onChange={setResponse}
          gapMode={gapMode}
        />
      </div>

      <div className="footer-actions">
        <button
          type="button"
          className="btn ghost"
          disabled={i === 0}
          onClick={() => setI((n) => Math.max(0, n - 1))}
        >
          Back
        </button>
        {i < questions.length - 1 ? (
          <button
            type="button"
            className="btn"
            onClick={() => setI((n) => Math.min(questions.length - 1, n + 1))}
          >
            Next
          </button>
        ) : (
          <button type="button" className="btn" onClick={finish}>
            Finish and mark
          </button>
        )}
        <span className="note">
          {answered} of {questions.length} answered
        </span>
        <button
          type="button"
          className="chip"
          style={{ marginLeft: 'auto' }}
          onClick={onQuit}
        >
          Abandon
        </button>
      </div>

      <div className="card" style={{ marginTop: 18 }}>
        <p className="help" style={{ margin: 0 }}>
          Jump to a question. Filled means answered.
        </p>
        <div className="chips" style={{ marginTop: 10 }}>
          {jumpList.map((j) => (
            <button
              type="button"
              key={j.idx}
              className="chip"
              aria-pressed={j.done}
              style={{
                minWidth: 42,
                justifyContent: 'center',
                fontWeight: j.idx === i ? 800 : 400,
                textDecoration: j.idx === i ? 'underline' : 'none',
              }}
              onClick={() => setI(j.idx)}
            >
              {j.idx + 1}
            </button>
          ))}
        </div>
        <button
          type="button"
          className="btn wide"
          style={{ marginTop: 14 }}
          onClick={finish}
        >
          Finish and mark now
        </button>
      </div>
    </>
  );
}
