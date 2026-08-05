'use client';

import type { Course, Marked, Question } from '@/lib/types';

/**
 * One verdict panel, used in two places.
 *
 * The end-of-test review and the after-every-question teaching mode show the
 * same thing: what you said, what the answer is, why the key is the key, what
 * is wrong with each other option, and where in the source it came from. They
 * share this file so the two can never drift apart, and so a question can
 * never be explained on one screen and bare on the other.
 */

export function optText(q: Question, id: string): string {
  if (q.style === 'tf') return id === 'true' ? 'True' : 'False';
  return q.options?.find((o) => o.id === id)?.text ?? id;
}

/** How the student answered, in words. */
export function yourAnswer(m: Marked): string {
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
export function rightAnswer(q: Question): string {
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
export function isKeyed(q: Question, id: string): boolean {
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
export function WhyGrid({ q }: { q: Question }) {
  if (!q.why) return null;
  const opts =
    q.style === 'tf'
      ? [
          { id: 'true', text: 'True' },
          { id: 'false', text: 'False' },
        ]
      : q.options ?? [];
  const rows = opts
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
              {q.style !== 'tf' && <b>{o.id.toUpperCase()}. </b>}
              {o.text}
              <span className="verdict-note">{q.why?.[o.id]}</span>
            </span>
          </p>
        );
      })}
    </div>
  );
}

/**
 * Part-by-part marking for the styles that carry several answers at once.
 *
 * A joined string cannot show which of four blanks you actually lost, so each
 * part gets its own row with its own tick, your word beside the right one.
 */
function PartGrid({ m }: { m: Marked }) {
  const { question: q, response: r } = m;
  if (!m.parts || !m.parts.length) return null;

  const rows: { label: string; yours: string; right: string; ok: boolean }[] = [];
  if (q.style === 'match' && q.pairs) {
    q.pairs.forEach((p, i) => {
      rows.push({
        label: p.left,
        yours: (r?.kind === 'pairs' ? r.value[p.left] : '') || 'blank',
        right: p.right,
        ok: m.parts?.[i] ?? false,
      });
    });
  } else if (q.blanks) {
    q.blanks.forEach((b, i) => {
      rows.push({
        label: `Blank ${i + 1}`,
        yours: (r?.kind === 'blanks' ? r.value[i]?.trim() : '') || 'blank',
        right: b.accept[0],
        ok: m.parts?.[i] ?? false,
      });
    });
  }
  if (!rows.length) return null;

  return (
    <div className="whygrid">
      <p className="whyhead">Part by part</p>
      {rows.map((row) => (
        <p className={`whyrow ${row.ok ? 'ok' : 'no'}`} key={row.label}>
          <span className="mk" aria-hidden="true">
            {row.ok ? '✓' : '✗'}
          </span>
          <span>
            <b>{row.label}.</b> {row.ok ? row.right : row.yours}
            {!row.ok && <span className="verdict-note">Answer: {row.right}</span>}
          </span>
        </p>
      ))}
    </div>
  );
}

export function verdictOf(m: Marked): { cls: string; text: string } {
  if (m.correct) return { cls: 'right', text: 'Correct' };
  if (m.fraction > 0)
    return { cls: 'part', text: `Part marks: ${m.fraction.toFixed(2)}` };
  return { cls: 'wrong', text: 'Wrong' };
}

interface Props {
  course: Course;
  m: Marked;
  /** Shown before the verdict on the review list, for example "Q7". */
  label?: string;
  /** Repeat the prompt above the verdict. The runner already shows it. */
  showPrompt?: boolean;
}

export default function Feedback({ course, m, label, showPrompt = true }: Props) {
  const q = m.question;
  const v = verdictOf(m);
  return (
    <div className={`review ${v.cls}`}>
      <div className="qmeta">
        <span className="verdict">
          {label ? `${label} · ` : ''}
          {v.text}
        </span>
      </div>
      {showPrompt && (
        <p style={{ margin: '4px 0 8px', fontWeight: 600, fontSize: '0.97rem' }}>
          {q.prompt.replace(/\{\{(\d+)\}\}/g, '____')}
        </p>
      )}
      {!m.correct && (
        <p className="yours">
          You said: <b>{yourAnswer(m)}</b>
        </p>
      )}
      <p className="theirs">
        Answer: <b>{rightAnswer(q)}</b>
      </p>
      <p className="why">{q.explanation}</p>
      <PartGrid m={m} />
      <WhyGrid q={q} />
      <div className="qmeta" style={{ marginTop: 8 }}>
        {q.slides.map((sl) => (
          <span className="tag slide" key={sl}>
            {sl}
          </span>
        ))}
        <span className="tag">
          {course.moduleNoun} {q.module}
        </span>
        <span className={`tag ${q.difficulty}`}>{q.difficulty}</span>
        <span className="tag">{q.topic}</span>
      </div>
    </div>
  );
}
