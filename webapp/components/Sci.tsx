import { Fragment } from 'react';

/**
 * Renders exponents written as carets, so "2.478 x 10^-9 F" reaches the reader
 * as 2.478 x 10⁻⁹ F.
 *
 * Question text is deliberately NOT html: prompts, options and verdicts are
 * plain strings rendered as React children, which is what keeps a bank file
 * from being an injection surface. So superscripts cannot be marked up the way
 * the crash-course lessons mark them up. This turns the caret notation into
 * real <sup> at render time instead, with no dangerouslySetInnerHTML anywhere
 * near the drill.
 *
 * The caret notation is also what the examiner uses: PHY121's own Test 1 prints
 * its options as "2.478 x 10^-9 F". Keeping it in the data means the stored
 * question stays verbatim, and only the presentation improves.
 *
 * Applies to every course. IFT222 is full of 2^32 and 10^-9 too.
 */
const EXP = /\^(-?\d+)/g;

export function Sci({ text }: { text: string }) {
  if (!text || !text.includes('^')) return <>{text}</>;

  const out: React.ReactNode[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  EXP.lastIndex = 0;
  while ((m = EXP.exec(text)) !== null) {
    if (m.index > last) out.push(text.slice(last, m.index));
    out.push(<sup key={m.index}>{m[1]}</sup>);
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(text.slice(last));

  return (
    <>
      {out.map((piece, i) => (
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
