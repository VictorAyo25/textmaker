'use client';

import { useMemo } from 'react';
import type { BlankFormat, GapMode, Question, Response } from '@/lib/types';
import { matchLabels } from '@/lib/bank';

/** The on-screen instruction for a typed blank, so nobody guesses the format. */
export function formatHint(fmt: BlankFormat | undefined, extra?: string): string {
  const base: Record<BlankFormat, string> = {
    word: 'one word',
    words: 'two or three words',
    number: 'a number, in figures',
    percent: 'a percentage, e.g. 40%',
    time: 'a time, e.g. 2:30 a.m.',
    name: 'a name',
    phrase: 'choose the continuation',
  };
  const b = base[fmt ?? 'word'];
  return extra ? `${b}, ${extra}` : b;
}

interface Props {
  question: Question;
  response: Response | null;
  onChange: (r: Response) => void;
  gapMode: GapMode;
  /** Set on the review screen: show the state, take no input. */
  readOnly?: boolean;
}

export default function QuestionView({
  question: q,
  response,
  onChange,
  gapMode,
  readOnly,
}: Props) {
  // Labels are computed once per question so the dropdown order does not jump
  // around on every keystroke elsewhere in the paper.
  const labels = useMemo(
    () => (q.style === 'match' ? matchLabels(q) : []),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [q.id]
  );

  if (q.style === 'mcq' || q.style === 'tf') {
    const opts =
      q.style === 'tf'
        ? [
            { id: 'true', text: 'True' },
            { id: 'false', text: 'False' },
          ]
        : q.options ?? [];
    const chosen = response?.kind === 'choice' ? response.value : null;
    return (
      <div>
        {opts.map((o) => (
          <button
            key={o.id}
            type="button"
            className="opt"
            aria-pressed={chosen === o.id}
            disabled={readOnly}
            onClick={() => onChange({ kind: 'choice', value: o.id })}
          >
            <span className="mk one">{q.style === 'tf' ? '' : o.id.toUpperCase()}</span>
            <span>{o.text}</span>
          </button>
        ))}
      </div>
    );
  }

  if (q.style === 'multi') {
    const chosen = response?.kind === 'choices' ? response.value : [];
    const toggle = (id: string) => {
      const next = chosen.includes(id)
        ? chosen.filter((c) => c !== id)
        : [...chosen, id];
      onChange({ kind: 'choices', value: next });
    };
    return (
      <div>
        <p className="note" style={{ marginTop: 0 }}>
          Select all that apply. Marked all or nothing, exactly like the real test.
        </p>
        {(q.options ?? []).map((o) => (
          <button
            key={o.id}
            type="button"
            className="opt"
            aria-pressed={chosen.includes(o.id)}
            disabled={readOnly}
            onClick={() => toggle(o.id)}
          >
            <span className="mk many">{chosen.includes(o.id) ? '✓' : ''}</span>
            <span>{o.text}</span>
          </button>
        ))}
      </div>
    );
  }

  if (q.style === 'match') {
    const chosen = response?.kind === 'pairs' ? response.value : {};
    const set = (left: string, right: string) =>
      onChange({ kind: 'pairs', value: { ...chosen, [left]: right } });
    return (
      <div>
        <p className="note" style={{ marginTop: 0 }}>
          Pair every row. Part marks apply: each correct row earns its share.
        </p>
        {(q.pairs ?? []).map((p) => (
          <div className="pairrow" key={p.left}>
            <span>{p.left}</span>
            <select
              value={chosen[p.left] ?? ''}
              disabled={readOnly}
              aria-label={`Match for ${p.left}`}
              onChange={(e) => set(p.left, e.target.value)}
            >
              <option value="">Choose...</option>
              {labels.map((l) => (
                <option key={l} value={l}>
                  {l}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
    );
  }

  // cloze and gap
  const blanks = q.blanks ?? [];
  const values = response?.kind === 'blanks' ? response.value : blanks.map(() => '');
  const setBlank = (i: number, v: string) => {
    const next = [...values];
    while (next.length < blanks.length) next.push('');
    next[i] = v;
    onChange({ kind: 'blanks', value: next });
  };

  // A cloze holds long continuations, so it is always a dropdown. A gap holds a
  // single word or number, so it honours the test's typed/choice setting.
  const useTyping = q.style === 'gap' && gapMode === 'typed';

  const pieces = q.prompt.split(/(\{\{\d+\}\})/g);

  return (
    <div>
      {q.style === 'gap' && useTyping && (
        <p className="note" style={{ marginTop: 0 }}>
          Type your answer. Capitals and punctuation do not matter, spelling does.
        </p>
      )}
      <div className={q.style === 'cloze' ? 'clozebody' : 'clozebody'}>
        {pieces.map((piece, idx) => {
          const m = piece.match(/^\{\{(\d+)\}\}$/);
          if (!m) return <span key={idx}>{piece}</span>;
          const i = parseInt(m[1], 10) - 1;
          const blank = blanks[i];
          if (!blank) return <span key={idx}>___</span>;
          return (
            <span className="blank-wrap" key={idx}>
              {useTyping ? (
                <input
                  className="blank-input"
                  type="text"
                  value={values[i] ?? ''}
                  disabled={readOnly}
                  aria-label={`Blank ${i + 1}`}
                  autoComplete="off"
                  autoCapitalize="none"
                  spellCheck={false}
                  onChange={(e) => setBlank(i, e.target.value)}
                />
              ) : (
                <select
                  className="blank-select"
                  value={values[i] ?? ''}
                  disabled={readOnly}
                  aria-label={`Blank ${i + 1}`}
                  onChange={(e) => setBlank(i, e.target.value)}
                >
                  <option value="">Choose...</option>
                  {blank.choices.map((c) => (
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </select>
              )}
              {useTyping && (
                <span className="blank-hint">{formatHint(blank.format, blank.hint)}</span>
              )}
            </span>
          );
        })}
      </div>
    </div>
  );
}
