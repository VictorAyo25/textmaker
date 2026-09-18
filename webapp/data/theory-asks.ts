import ift222 from './ift222/theory-asks.json';

/**
 * The theory asks: every question on a course's past papers that is answered in
 * words rather than in arithmetic, gathered into one section at the front of the
 * theory solutions book.
 *
 * The solutions book itself is filed by PAPER, which is what practice wants and
 * the opposite of what revision wants: "State Amdahl's law" appears once, in the
 * middle of a cache calculation, and "Explain the following terms" three times
 * on three different papers. Here they are grouped by what the examiner asks you
 * to DO, with every paper that set the ask and the marks it carried.
 *
 * Written by scripts/author/<course>_theory_asks.py, which slices every quote
 * out of the printed question rather than retyping it. A course with no such
 * file simply has no section.
 */
export interface TheoryAskSource {
  /** The session, as the paper prints it: "2024/2025". */
  paper: string;
  /** The part, as the paper numbers it: "Q3(a)(ii)". */
  part: string;
  /** What it was worth, or null where the paper shares marks across parts. */
  marks: number | null;
  /** Why the marks are null, where they are. */
  note?: string;
  /** The ask in the examiner's own words, sliced from the printed question. */
  quote: string;
}

export interface TheoryAsk {
  id: string;
  /** The crash course topic it belongs to, shown as a chip. */
  topic: string;
  /** What the ask hangs off, where it cannot be read on its own. */
  context?: string;
  papers: TheoryAskSource[];
  /** The answer, at the length the marks buy. HTML. */
  answer: string;
}

export interface TheoryAskGroup {
  /** What the examiner asks you to do: "Define it", "List it". */
  kind: string;
  /** What that kind of ask wants, in one or two sentences. */
  when: string;
  asks: TheoryAsk[];
}

export interface TheoryAskBook {
  lead: string;
  groups: TheoryAskGroup[];
}

const BY_COURSE: Record<string, TheoryAskBook> = {
  IFT222: ift222 as TheoryAskBook,
};

export function theoryAsksFor(code: string): TheoryAskBook | undefined {
  return BY_COURSE[code.toUpperCase()];
}

/** How many asks, and how many marks each paper put on them. */
export function theoryAskTally(book: TheoryAskBook) {
  const asks = book.groups.flatMap((g) => g.asks);
  const papers = new Map<string, { asks: number; marks: number; shared: boolean }>();
  for (const ask of asks)
    for (const source of ask.papers) {
      const row = papers.get(source.paper) ?? { asks: 0, marks: 0, shared: false };
      row.asks += 1;
      if (source.marks === null) row.shared = true;
      else row.marks += source.marks;
      papers.set(source.paper, row);
    }
  return {
    asks: asks.length,
    papers: [...papers.entries()]
      .sort((a, b) => b[0].localeCompare(a[0]))
      .map(([paper, row]) => ({ paper, ...row })),
  };
}
