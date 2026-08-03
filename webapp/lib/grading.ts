import type { Marked, Question, Response } from './types';

/**
 * Typed answers are marked leniently on FORM and strictly on CONTENT.
 *
 * Case is folded, "the/a/an" are dropped, "&" becomes "and", and everything
 * that is not a letter or a digit is removed. What survives must equal one of
 * the accepted answers. So "2:30 a.m.", "2:30am", "2.30 AM" and "2:30 A.M."
 * all pass, and "71%" passes for "71", while "gradual" for "sudden" still
 * fails, which is the whole point.
 *
 * The final strip also removes combining accent marks left by NFKD, so there
 * is no separate diacritics pass to keep in step with it.
 */
export function normalise(raw: string): string {
  return raw
    .toLowerCase()
    .normalize('NFKD')
    .replace(/\b(the|a|an)\b/g, '')
    .replace(/&/g, 'and')
    .replace(/[^a-z0-9]/g, '');
}

export function blankIsCorrect(given: string, accept: string[]): boolean {
  if (!given || !given.trim()) return false;
  const g = normalise(given);
  if (!g) return false;
  return accept.some((a) => normalise(a) === g);
}

function sameSet(a: string[], b: string[]): boolean {
  if (a.length !== b.length) return false;
  const sa = [...a].sort();
  const sb = [...b].sort();
  return sa.every((v, i) => v === sb[i]);
}

/** Mark one question. Every question is worth 1; multi-part questions give the
 *  fraction of parts answered correctly. */
export function mark(question: Question, response: Response | null): Marked {
  const miss: Marked = { question, response, fraction: 0, correct: false };
  if (!response) {
    if (question.style === 'match' && question.pairs) {
      return { ...miss, parts: question.pairs.map(() => false) };
    }
    if (question.blanks) return { ...miss, parts: question.blanks.map(() => false) };
    return miss;
  }

  switch (question.style) {
    case 'mcq':
    case 'tf': {
      if (response.kind !== 'choice') return miss;
      const ok = response.value === question.answer;
      return { question, response, fraction: ok ? 1 : 0, correct: ok };
    }

    case 'multi': {
      if (response.kind !== 'choices') return miss;
      const want = (question.answer as string[]) ?? [];
      // All or nothing, exactly as the real test warns: miss one and you lose it.
      const ok = sameSet(response.value, want);
      return { question, response, fraction: ok ? 1 : 0, correct: ok };
    }

    case 'match': {
      if (response.kind !== 'pairs' || !question.pairs) return miss;
      const parts = question.pairs.map((p) => response.value[p.left] === p.right);
      const got = parts.filter(Boolean).length;
      const fraction = parts.length ? got / parts.length : 0;
      return { question, response, fraction, correct: fraction === 1, parts };
    }

    case 'cloze':
    case 'gap': {
      if (response.kind !== 'blanks' || !question.blanks) return miss;
      const parts = question.blanks.map((b, i) =>
        blankIsCorrect(response.value[i] ?? '', b.accept)
      );
      const got = parts.filter(Boolean).length;
      const fraction = parts.length ? got / parts.length : 0;
      return { question, response, fraction, correct: fraction === 1, parts };
    }

    default:
      return miss;
  }
}

export function markAll(
  questions: Question[],
  responses: (Response | null)[]
): Marked[] {
  return questions.map((q, i) => mark(q, responses[i] ?? null));
}

export interface Score {
  earned: number;
  total: number;
  percent: number;
  fullyCorrect: number;
  byModule: Record<number, { earned: number; total: number }>;
}

export function score(marked: Marked[]): Score {
  const byModule: Record<number, { earned: number; total: number }> = {};
  let earned = 0;
  for (const m of marked) {
    earned += m.fraction;
    const mod = m.question.module;
    if (!byModule[mod]) byModule[mod] = { earned: 0, total: 0 };
    byModule[mod].earned += m.fraction;
    byModule[mod].total += 1;
  }
  const total = marked.length;
  return {
    earned,
    total,
    percent: total ? (earned / total) * 100 : 0,
    fullyCorrect: marked.filter((m) => m.correct).length,
    byModule,
  };
}
