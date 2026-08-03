'use client';

import { useMemo, useState } from 'react';
import type { Course, Marked, Question } from '@/lib/types';
import { score } from '@/lib/grading';

function optText(q: Question, id: string): string {
  if (q.style === 'tf') return id === 'true' ? 'True' : 'False';
  return q.options?.find((o) => o.id === id)?.text ?? id;
}

/** How the student answered, in words. */
function yourAnswer(m: Marked): string {
  const { question: q, response: r } = m;
  if (!r) return 'not answered';
  switch (r.kind) {
    case 'choice':
      return optText(q, r.value);
    case 'choices':
      return r.value.length
        ? r.value
            .slice()
            .sort()
            .map((v) => `${v.toUpperCase()}. ${optText(q, v)}`)
            .join('  |  ')
        : 'nothing selected';
    case 'pairs':
      return (q.pairs ?? [])
        .map((p) => `${p.left} -> ${r.value[p.left] || 'blank'}`)
        .join('  |  ');
    case 'blanks':
      return (q.blanks ?? [])
        .map((_, i) => `${i + 1}. ${r.value[i]?.trim() || 'blank'}`)
        .join('  |  ');
    default:
      return 'not answered';
  }
}

/** The key, in words. */
function rightAnswer(q: Question): string {
  switch (q.style) {
    case 'mcq':
      return `${String(q.answer).toUpperCase()}. ${optText(q, String(q.answer))}`;
    case 'tf':
      return q.answer === 'true' ? 'True' : 'False';
    case 'multi':
      return ((q.answer as string[]) ?? [])
        .slice()
        .sort()
        .map((v) => `${v.toUpperCase()}. ${optText(q, v)}`)
        .join('  |  ');
    case 'match':
      return (q.pairs ?? []).map((p) => `${p.left} -> ${p.right}`).join('  |  ');
    case 'cloze':
    case 'gap':
      return (q.blanks ?? []).map((b, i) => `${i + 1}. ${b.accept[0]}`).join('  |  ');
    default:
      return '';
  }
}

/** Is this option id part of the key? Handles mcq and multiple response alike. */
function isKeyed(q: Question, id: string): boolean {
  return Array.isArray(q.answer) ? q.answer.includes(id) : q.answer === id;
}

/**
 * The option-by-option verdict.
 *
 * Getting a question right for the wrong reason is worth nothing in the test,
 * so the review never stops at the key: it states why the key is the key, and
 * what is wrong with each of the other options. Questions carrying a `why`
 * block get this; the bank gate makes sure that block covers every option.
 */
function WhyGrid({ q }: { q: Question }) {
  if (!q.why || !q.options) return null;
  const rows = q.options
    .slice()
    .sort((a, b) => a.id.localeCompare(b.id))
    .filter((o) => q.why?.[o.id]);
  if (!rows.length) return null;
  return (
    <div className="whygrid">
      <p className="whyhead">Every option, and why</p>
      {rows.map((o) => {
        const ok = isKeyed(q, o.id);
        return (
          <p className={`whyrow ${ok ? 'ok' : 'no'}`} key={o.id}>
            <span className="mk" aria-hidden="true">
              {ok ? '✓' : '✗'}
            </span>
            <span>
              <b>{o.id.toUpperCase()}.</b> {o.text}
              <span className="verdict-note">{q.why?.[o.id]}</span>
            </span>
          </p>
        );
      })}
    </div>
  );
}

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

      {shown.map((m) => {
        const cls = m.correct ? 'right' : m.fraction > 0 ? 'part' : 'wrong';
        const verdict = m.correct
          ? 'Correct'
          : m.fraction > 0
            ? `Part marks: ${m.fraction.toFixed(2)}`
            : 'Wrong';
        const n = marked.indexOf(m) + 1;
        return (
          <div className={`review ${cls}`} key={m.question.id}>
            <div className="qmeta">
              <span className="verdict">
                Q{n} &middot; {verdict}
              </span>
            </div>
            <p style={{ margin: '4px 0 8px', fontWeight: 600, fontSize: '0.97rem' }}>
              {m.question.prompt.replace(/\{\{(\d+)\}\}/g, '____')}
            </p>
            {!m.correct && (
              <p className="yours">
                You said: <b>{yourAnswer(m)}</b>
              </p>
            )}
            <p className="theirs">
              Answer: <b>{rightAnswer(m.question)}</b>
            </p>
            <p className="why">{m.question.explanation}</p>
            <WhyGrid q={m.question} />
            <div className="qmeta" style={{ marginTop: 8 }}>
              {m.question.slides.map((sl) => (
                <span className="tag slide" key={sl}>
                  {sl}
                </span>
              ))}
              <span className="tag">
                {course.moduleNoun} {m.question.module}
              </span>
              <span className={`tag ${m.question.difficulty}`}>
                {m.question.difficulty}
              </span>
              <span className="tag">{m.question.topic}</span>
            </div>
          </div>
        );
      })}
    </>
  );
}
