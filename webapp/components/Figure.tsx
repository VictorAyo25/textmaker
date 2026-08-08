import type { Figure as Fig } from '@/lib/types';

/**
 * The one place a question's diagram is drawn.
 *
 * Used by the runner while sitting a test, by the review panel afterwards, and
 * by the printable sheet, so the three can never drift apart. That is the same
 * reason Feedback.tsx exists as a shared panel rather than duplicated markup.
 *
 * The SVG is authored in this repository and validated by the bank gate, which
 * rejects scripts, foreignObject and any external reference before a build can
 * ship. It is injected with dangerouslySetInnerHTML because inline SVG is the
 * whole point: it scales with the page, prints at full resolution, and needs no
 * network, which an <img> pointing at a file would not give us offline.
 */
export function Figure({ figure }: { figure: Fig }) {
  return (
    <figure className="qfig" role="group" aria-label={figure.alt}>
      <div className="qfig-draw" dangerouslySetInnerHTML={{ __html: figure.svg }} />
      {figure.caption && <figcaption>{figure.caption}</figcaption>}
    </figure>
  );
}
