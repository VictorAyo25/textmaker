import { Fragment } from 'react';

/**
 * Renders maths written in plain text: exponents as carets, and fractions
 * written with the word "over", so "2.478 x 10^-9 F" reaches the reader as
 * 2.478 x 10⁻⁹ F and "q1 q2 over 4 π ε₀ r²" is drawn as a real fraction with
 * the numerator above the denominator and a rule between them.
 *
 * Question text is deliberately NOT html: prompts, options and verdicts are
 * plain strings rendered as React children, which is what keeps a bank file
 * from being an injection surface. So none of this can be marked up in the
 * data the way the crash-course lessons mark it up. It is turned into real
 * <sup> and a stacked fraction at render time instead, with no
 * dangerouslySetInnerHTML anywhere near the drill.
 *
 * The caret notation is also what the examiner uses: PHY121's own Test 1 prints
 * its options as "2.478 x 10^-9 F". Keeping it in the data means the stored
 * question stays verbatim, and only the presentation improves.
 *
 * "over" stays in the data rather than being replaced by a slash because a
 * slash is ambiguous the moment the denominator has more than one term:
 * "μ₀ N I / 2 π r" can be read three ways and "μ₀ N I over 2 π r" cannot. The
 * word says exactly where the denominator starts, which is what lets this
 * component draw the rule in the right place.
 *
 * Applies to every course. IFT222 is full of 2^32 and 10^-9 too.
 */
const EXP = /\^(-?\d+)/g;

/**
 * A fraction: everything up to "over", and everything after it until the
 * expression ends. The numerator runs back to the last separator, and the
 * denominator runs forward to the next one, so surrounding prose is untouched.
 */
// The lookahead must NOT stop at a decimal point: "1500 over 0.5" was ending
// the denominator at the dot and drawing a division by zero.
// "+" belongs in a term: a denominator like (R₁ + R₂) is ordinary algebra, and
// without it the match died at the plus and the word "over" printed literally.
const TERM = '[A-Za-z0-9εμθΦλσρτπΔ₀₁₂₃₄₅₆₇₈₉²³⁻^()+\\s-]';
const FRACTION = new RegExp(
  `(${TERM}+?)\\s+over\\s+((?:${TERM}|\\.(?=\\d))+?)` +
    `(?=[,;]|\\.(?!\\d)|\\s+(?:where|which|and|so|if|is|means|gives|equals|then)\\b|$)`
);

/**
 * "over" is an ordinary English word as well as a fraction bar, and the matcher
 * cannot tell them apart on its own. It was drawing "the influence of a point
 * charge spreads OVER the surface of a sphere" as a stacked fraction, which is
 * worse than not drawing one at all.
 *
 * So both sides must look like algebra before a rule is drawn. A side is
 * algebra when it holds no run of three or more lowercase letters, since every
 * symbol in this course is one or two letters (m, g, q, kQ, mv, emf) while
 * every English word that matters here is longer. The few genuine three-letter
 * maths words are named rather than guessed at.
 */
const MATH_WORDS = /^(sin|cos|tan|log|ln|exp|emf|sqrt)$/;
const isAlgebra = (side: string) =>
  side.trim().length > 0 &&
  !side
    .split(/[^A-Za-z]+/)
    .some((w) => w.length >= 3 && w === w.toLowerCase() && !MATH_WORDS.test(w));

function sup(text: string): React.ReactNode[] {
  const out: React.ReactNode[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  EXP.lastIndex = 0;
  while ((m = EXP.exec(text)) !== null) {
    if (m.index > last) out.push(text.slice(last, m.index));
    out.push(<sup key={`s${m.index}`}>{m[1]}</sup>);
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

export function Sci({ text }: { text: string }) {
  if (!text) return <>{text}</>;

  // Draw a fraction only when there is exactly ONE in the sentence. With
  // several, as in "1 over C = 1 over C1 + 1 over C2", the matcher pairs the
  // first numerator with the last denominator and draws 1 over C2, which is
  // simply wrong maths. Wrong is far worse than plain, so those stay as words.
  if (text.includes(' over ') && text.split(' over ').length === 2) {
    const m = FRACTION.exec(text);
    if (m && isAlgebra(m[1]) && isAlgebra(m[2])) {
      const before = text.slice(0, m.index);
      const after = text.slice(m.index + m[0].length);
      return (
        <>
          {before && <Sci text={before} />}
          <span className="frac">
            <span className="fnum">{sup(m[1].trim()).map((p, i) => <Fragment key={i}>{p}</Fragment>)}</span>
            <span className="fden">{sup(m[2].trim()).map((p, i) => <Fragment key={i}>{p}</Fragment>)}</span>
          </span>
          {after && <Sci text={after} />}
        </>
      );
    }
  }

  if (!text.includes('^')) return <>{text}</>;
  return (
    <>
      {sup(text).map((piece, i) => (
        <Fragment key={i}>{piece}</Fragment>
      ))}
    </>
  );
}

/** The same transform for a plain string, where JSX cannot be used. */
export function sciText(text: string): string {
  const SUPS: Record<string, string> = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    '-': '⁻',
  };
  return text.replace(EXP, (_, d: string) =>
    [...d].map((c) => SUPS[c] ?? c).join('')
  );
}
