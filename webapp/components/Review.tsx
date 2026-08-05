'use client';

import { useMemo, useState } from 'react';
import type { Course, Marked, Question } from '@/lib/types';
import { score } from '@/lib/grading';
import Feedback from './Feedback';

interface Props {
  course: Course;
  marked: Marked[];
  title: string;
  onRetryWrong: (questions: Question[]) => void;
  onAgain: () => void;
}

export default function Review({
  course,
  marked,
  title,
  onRetryWrong,
  onAgain,
}: Props) {
  const [filter, setFilter] = useState<'all' | 'wrong'>('all');
  const s = useMemo(() => score(marked), [marked]);

  const shown = filter === 'all' ? marked : marked.filter((m) => !m.correct);
  const wrongQuestions = marked.filter((m) => !m.correct).map((m) => m.question);
  const pct = Math.round(s.percent);
  const tone = pct >= 70 ? '' : pct >= 50 ? 'mid' : 'low';

  return (
    <>
      <div className="card">
        <div className="scorehead">
          <div className={`bignum ${tone}`}>{pct}%</div>
          <div className="scoreline">
            {s.earned.toFixed(2)} of {s.total} marks &middot; {s.fullyCorrect} question
            {s.fullyCorrect === 1 ? '' : 's'} fully correct
          </div>
          <div className="scoreline">{title}</div>
        </div>

        <div className="modbars">
          {Object.keys(s.byModule)
            .map(Number)
            .sort((a, b) => a - b)
            .map((mod) => {
              const row = s.byModule[mod];
              const p = row.total ? (row.earned / row.total) * 100 : 0;
              const meta = course.modules.find((m) => m.number === mod);
              return (
                <div className="modbar" key={mod}>
                  <span title={meta?.title}>
                    {course.moduleNoun} {mod}
                  </span>
                  <span className="track">
                    <i style={{ width: `${p}%` }} />
                  </span>
                  <span className="note" style={{ textAlign: 'right' }}>
                    {Math.round(p)}%
                  </span>
                </div>
              );
            })}
        </div>

        <div className="footer-actions">
          <button type="button" className="btn" onClick={onAgain}>
            New test
          </button>
          {wrongQuestions.length > 0 && (
            <button
              type="button"
              className="btn ghost"
              onClick={() => onRetryWrong(wrongQuestions)}
            >
              Retry the {wrongQuestions.length} I missed
            </button>
          )}
        </div>
      </div>

      <div className="filterrow">
        <button
          type="button"
          className="chip"
          aria-pressed={filter === 'all'}
          onClick={() => setFilter('all')}
        >
          Every question ({marked.length})
        </button>
        <button
          type="button"
          className="chip"
          aria-pressed={filter === 'wrong'}
          onClick={() => setFilter('wrong')}
        >
          Only what I missed ({marked.filter((m) => !m.correct).length})
        </button>
      </div>

      {shown.map((m) => (
        <Feedback
          key={m.question.id}
          course={course}
          m={m}
          label={`Q${marked.indexOf(m) + 1}`}
        />
      ))}
    </>
  );
}
