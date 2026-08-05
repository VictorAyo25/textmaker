'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import type { Course, FeedbackMode, GapMode, Question, Response } from '@/lib/types';
import { mark } from '@/lib/grading';
import QuestionView from './QuestionView';
import Feedback from './Feedback';

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

/**
 * Is there enough here to mark?
 *
 * Teaching mode has to decide when an answer is committed. A single choice
 * commits the moment it is tapped, but a four-blank cloze would otherwise be
 * marked wrong on the first keystroke, so the multi-part styles wait until
 * every part has something in it and the student presses Check.
 */
function isComplete(q: Question, r: Response | null): boolean {
  if (!r) return false;
  switch (r.kind) {
    case 'choice':
      return !!r.value;
    case 'choices':
      return r.value.length > 0;
    case 'pairs':
      return (q.pairs ?? []).every((p) => !!r.value[p.left]);
    case 'blanks':
      return (q.blanks ?? []).every((_, i) => !!r.value[i]?.trim());
    default:
      return false;
  }
}

interface Props {
  questions: Question[];
  gapMode: GapMode;
  timeLimitSec: number | null;
  course: Course;
  /** 'instant' tells the student after every question instead of at the end. */
  feedback: FeedbackMode;
  onFinish: (responses: (Response | null)[]) => void;
  onQuit: () => void;
}

export default function Runner({
  questions,
  gapMode,
  timeLimitSec,
  course,
  feedback,
  onFinish,
  onQuit,
}: Props) {
  const instant = feedback === 'instant';
  const [i, setI] = useState(0);
  const [responses, setResponses] = useState<(Response | null)[]>(() =>
    questions.map(() => null)
  );
  // Which questions have been checked in teaching mode. A checked question is
  // locked: seeing the answer and then changing yours would teach nothing.
  const [checked, setChecked] = useState<boolean[]>(() => questions.map(() => false));
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
  const shown = instant && checked[i];

  const reveal = (idx: number) =>
    setChecked((prev) => {
      if (prev[idx]) return prev;
      const next = [...prev];
      next[idx] = true;
      return next;
    });

  const setResponse = (r: Response) => {
    if (checked[i]) return;
    setResponses((prev) => {
      const next = [...prev];
      next[i] = r;
      return next;
    });
    // A single choice and a true or false have nothing left to fill in, so
    // tapping the option is the commitment. Anything else waits for Check.
    if (instant && (q.style === 'mcq' || q.style === 'tf')) reveal(i);
  };

  const jumpList = useMemo(
    () =>
      questions.map((_, idx) => ({
        idx,
        done: responses[idx] != null,
      })),
    [questions, responses]
  );

  // The running tally, over what has actually been checked so far.
  const tally = useMemo(() => {
    if (!instant) return null;
    let done = 0;
    let earned = 0;
    checked.forEach((c, idx) => {
      if (!c) return;
      done += 1;
      earned += mark(questions[idx], responses[idx]).fraction;
    });
    return { done, earned };
  }, [instant, checked, responses, questions]);

  const marked = shown ? mark(q, responses[i]) : null;
  const complete = isComplete(q, responses[i]);
  const last = i === questions.length - 1;
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
        {tally && tally.done > 0 && (
          <strong style={{ fontSize: '0.85rem', color: 'var(--muted)' }}>
            {tally.earned.toFixed(tally.earned % 1 === 0 ? 0 : 2)} of {tally.done} right
          </strong>
        )}
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
            {course.moduleNoun} {q.module}
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
          readOnly={shown}
        />
        {marked && (
          <div className="instant" aria-live="polite">
            <Feedback course={course} m={marked} showPrompt={false} />
          </div>
        )}
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

        {instant && !checked[i] && (
          <button
            type="button"
            className="btn"
            disabled={!complete}
            onClick={() => reveal(i)}
          >
            Check answer
          </button>
        )}

        {last ? (
          <button
            type="button"
            className={instant && !checked[i] ? 'btn ghost' : 'btn'}
            onClick={finish}
          >
            Finish and mark
          </button>
        ) : (
          <button
            type="button"
            className={instant && !checked[i] ? 'btn ghost' : 'btn'}
            onClick={() => setI((n) => Math.min(questions.length - 1, n + 1))}
          >
            {instant && !checked[i] ? 'Skip' : 'Next'}
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
