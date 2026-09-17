/**
 * What each course's Learn by doing papers actually contain.
 *
 * The four papers are not the same shape, so the section cannot describe them
 * in one sentence. INS224 is the only one whose every theory question carries a
 * practical, because that is what its lecturer confirmed; IFT222 and COS221
 * carry past questions only, on Victor's instruction; CSC241 follows its own
 * paper, which mixes theory with a listing to trace and a program to write.
 *
 * Kept here rather than in the component so the page that knows the course can
 * hand the right words to the index, and so a fifth course only edits data.
 */
export interface DoingCopy {
  /** What Part A of this course's papers holds. */
  partA: string;
  /** What Part B holds, in this course's own terms. */
  partB: string;
}

const COPY: Record<string, DoingCopy> = {
  INS224: {
    partA:
      'the objective questions on that module, the examiner’s own test questions first, every option explained as you answer',
    partB:
      'the theory questions, each with the practical scenario the lecturer confirmed every question carries, and each answered twice: the answer you would write in the hall, then the same question taught from nothing in steps',
  },
  CSC241: {
    partA:
      'the objective questions on that topic, the manual’s own objective sections first, every option explained as you answer',
    partB:
      'the written questions in the shape this paper sets them, some theory, a listing to trace, a listing to fix and a program to write, each answered twice: the answer you would write in the hall, then the same question taught from nothing. Every listing was run before it was printed',
  },
  IFT222: {
    partA:
      'the objective questions on that topic, the two tests’ own questions first and the rest chosen so the set reaches as many separate facts as it can',
    partB:
      'past questions only, nothing invented: every part the examiner has set on that topic across four papers, each with its model answer, and every repeat labelled. Then the method behind them, taught from nothing',
  },
  COS221: {
    partA:
      'the objective questions on that topic, the manual’s own objective sections first, every option explained as you answer',
    partB:
      'past questions only, all 39 parts of both solved papers, each with its model answer and labelled by the shape the examiner keeps reusing. Then the method behind them, taught from nothing, with every listing compiled and run',
  },
};

const FALLBACK: DoingCopy = {
  partA: 'the objective questions on that module, every option explained as you answer',
  partB:
    'the written questions, each answered twice: the answer you would write in the hall, then the same question taught from nothing',
};

export function doingCopy(code: string): DoingCopy {
  return COPY[code] ?? FALLBACK;
}
