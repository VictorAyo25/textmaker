// The question schema. One shape for every course, so adding a course later is
// dropping in JSON and registering it, never touching the app.
//
// Marking rule for the whole platform: every question is worth 1 mark. Questions
// with several parts (match, cloze, gap) award the fraction of parts you got
// right, so "3 of 4 blanks" scores 0.75 rather than zero. See lib/grading.ts.

export type Difficulty = 'easy' | 'medium' | 'hard';

/** The "specifics" facets. A question carries every facet it actually tests. */
export type Facet =
  | 'numbers' // percentages, counts, dates, scores, times
  | 'names' // authors, people, book titles, organisations
  | 'lists' // enumerations and their order
  | 'wording'; // exact slide phrasing and precise distinctions

export type Style =
  | 'mcq' // one correct option
  | 'multi' // select all that apply
  | 'tf' // true or false
  | 'match' // pair each left item with its right label
  | 'cloze' // blanks filled from long phrase choices (always choice-based)
  | 'gap'; // blanks filled with a short word (typed or choice, per test setting)

export interface Option {
  id: string; // 'a' | 'b' | 'c' | 'd' ...
  text: string;
}

export interface Pair {
  left: string;
  right: string; // the correct label
}

/** What the reader is told to type, so nobody loses a mark guessing the format. */
export type BlankFormat =
  | 'word' // exactly one word
  | 'words' // a short phrase, two or three words
  | 'number' // digits, e.g. 50
  | 'percent' // a percentage, e.g. 71%
  | 'time' // a clock time, e.g. 2:30 a.m.
  | 'name' // a person, book or organisation
  | 'phrase'; // a longer continuation, choice-only

export interface Blank {
  /** Accepted typed answers, first one is the canonical answer shown in review. */
  accept: string[];
  /** Options shown in choice mode. Must contain the canonical answer. */
  choices: string[];
  /** Drives the on-screen "type one word" style hint. Defaults to 'word'. */
  format?: BlankFormat;
  /** Optional extra instruction, e.g. "in figures, not words". */
  hint?: string;
}

/**
 * A diagram a question cannot be answered without.
 *
 * PHY121 needs these: its Test 1 question 2 shows a capacitor network and asks
 * for the total capacitance, which is unanswerable from words alone without
 * doing the reader's work for them. The drawing is held as INLINE SVG rather
 * than an image file so it scales to any width, prints, survives the PDF
 * export, and needs no network, which matters because the app is installable
 * and used offline.
 *
 * The gate rejects a figure carrying a script, a foreignObject or any external
 * reference, so a diagram can never fetch anything or execute anything.
 */
export interface Figure {
  /** Inline SVG markup. Must carry a viewBox so it scales. */
  svg: string;
  /** Read out to screen readers, and printed if the SVG cannot render. */
  alt: string;
  /** Shown beneath the drawing, e.g. "Figure 1". */
  caption?: string;
}

export interface Question {
  id: string;
  module: number; // 1..5 for TMC221, 1..10 for IFT222
  lecture?: number; // the source lecture number, where the course has lectures
  slides: string[]; // provenance, e.g. ["L1 S9"] or ["Test 1 Q16"] - shown in review
  style: Style;
  difficulty: Difficulty;
  facets: Facet[];
  topic: string; // short label, e.g. "OKR", "the 7 Kits"
  prompt: string; // for cloze/gap the blanks are marked {{1}}, {{2}}, ...
  /** A diagram the question depends on, drawn inline. See Figure above. */
  figure?: Figure;
  options?: Option[]; // mcq, multi
  answer?: string | string[]; // mcq: 'c'   multi: ['a','b']   tf: 'true' | 'false'
  pairs?: Pair[]; // match
  extraLabels?: string[]; // match: decoy labels added to the dropdown
  blanks?: Blank[]; // cloze, gap
  explanation: string; // always shown in review
  /**
   * Per-option verdict, keyed by option id: why the key is right and why each
   * distractor is wrong. Review prints every entry, so a reader who guessed
   * right for the wrong reason still learns what the other three were doing
   * there. Where a course supplies these, the bank gate requires one entry for
   * every option, so a question cannot ship half explained.
   */
  why?: Record<string, string>;
  /**
   * Ledger fact ids this question tests, for courses that carry a fact ledger.
   *
   * The ledger enumerates every atomic testable fact in the course sources, and
   * the bank gate requires each one to be named by at least one question, so a
   * fact nothing asks about fails the build rather than quietly going untested.
   * This field never reaches the screen; it exists to be checked.
   */
  facts?: string[];
}

export interface Paper {
  /** A fixed, ordered paper such as the real test. Not shuffled, not filtered. */
  id: string;
  title: string;
  subtitle: string;
  note: string;
  questions: Question[];
  /** Minutes offered by the timed button. Defaults to 20 when absent. */
  minutes?: number;
}

export interface ModuleMeta {
  number: number;
  title: string;
  lecture?: number;
  blurb: string;
}

/** The facet filter, worded for the course in hand. */
export interface FacetGuide {
  id: Facet;
  label: string;
  help: string;
}

// ---- the crash course ----
//
// Lessons are converted from the crash manual's authored HTML by
// scripts/import-crash.mjs, so the words on screen are the words the manual's
// own gates passed. The html fields are trusted repository content and are
// rendered with dangerouslySetInnerHTML; nothing here is user input.

/** One programmed frame: the check answering the frame before it, the teaching
 *  step, and the question it leaves you on. */
export interface Frame {
  check: string;
  teach: string;
  ask: string;
}

export type LessonBlock =
  | { kind: 'frames'; label: string; tag: string; howto: string; frames: Frame[] }
  | {
      kind: 'worked';
      /** 'model' hides the whole answer, 'example' shows the problem first. */
      mode: 'model' | 'example';
      label: string;
      tag: string;
      problem: string;
      working: string;
      answer: string;
      redo: string;
    }
  | { kind: 'recall'; label: string; tag: string; question: string; answer: string }
  | { kind: 'asprinted'; label: string; tag: string; src: string; printed: string }
  | { kind: 'rules' | 'trap' | 'teach'; label: string; tag: string; html: string }
  | { kind: 'prose'; html: string }
  | { kind: 'heading'; text: string }
  | { kind: 'lockin'; big: string; sub: string };

export interface Lesson {
  slug: string;
  /** The manual's own grouping: "Part A: foundations and data" and so on. */
  part: string;
  kick: string;
  title: string;
  lead: string;
  minutes: number;
  /** Drill topics this skill teaches, so a lesson can hand off to the bank. */
  modules: number[];
  blocks: LessonBlock[];
}

export interface Course {
  code: string;
  title: string;
  /** One line under the code on the course card and the masthead. */
  tagline: string;
  /** What the course covers, shown on the landing page card. */
  blurb: string;
  /** What the app calls a module group: "Module" for TMC221, "Topic" here. */
  moduleNoun: string;
  /** The four facets, described in this course's own vocabulary. */
  facetGuide: FacetGuide[];
  modules: ModuleMeta[];
  questions: Question[];
  papers: Paper[];
  /**
   * Provenance prefixes that mark a question as one the examiner actually set,
   * for example ["Test 1 Q", "Test 2 Q"]. Drives the "past questions only"
   * filter on the setup screen. A course without them simply loses the filter.
   */
  examTags?: string[];
  /**
   * Set once the exam has been sat. The landing page files these under
   * "Exams already taken" instead of listing them with the live courses; the
   * course itself stays open, because revision does not stop at the exam hall.
   */
  taken?: boolean;
  /**
   * True where the course carries a fact ledger, which is what makes the
   * fact-level mastery map possible. The ledger itself is loaded on demand,
   * never bundled with the drill.
   */
  hasLedger?: boolean;
}

// ---- what the setup screen produces ----

/**
 * How a short-answer blank is answered.
 *
 * 'mixed' decides per question rather than per paper, so some blanks arrive as
 * a text box and some as a dropdown and you cannot settle into either. The
 * decision is made once when the paper starts and does not change under you.
 * Long cloze continuations ignore this and stay dropdowns whatever it says.
 */
export type GapMode = 'typed' | 'choice' | 'mixed';

/**
 * When the student is told how they did.
 *
 * 'end' is the real test: answer everything, then mark. 'instant' is the
 * teaching mode: the moment an answer is committed the page says right or
 * wrong, why the key is the key, what is wrong with each other option, and
 * where in the source it came from. Someone who knows nothing about the course
 * can start on instant and learn the course by sitting it.
 */
export type FeedbackMode = 'end' | 'instant';

/** Where the questions may be drawn from. */
export type SourceFilter =
  | 'all' // the whole bank
  | 'exam'; // only questions the examiner actually set, per Course.examTags

export interface TestConfig {
  modules: number[]; // empty means every module
  facets: Facet[]; // empty means no facet restriction
  source: SourceFilter;
  mix: Record<Difficulty, number>; // percentages, normalised before use
  count: number;
  gapMode: GapMode;
  shuffleOptions: boolean;
  feedback: FeedbackMode;
  /** Questions shown on screen at once. 0 means the whole paper on one page. */
  perPage: number;
}

// ---- what the runner collects ----

export type Response =
  | { kind: 'choice'; value: string } // mcq, tf
  | { kind: 'choices'; value: string[] } // multi
  | { kind: 'pairs'; value: Record<string, string> } // match: left -> chosen label
  | { kind: 'blanks'; value: string[] }; // cloze, gap

export interface Marked {
  question: Question;
  response: Response | null;
  fraction: number; // 0..1
  correct: boolean; // fraction === 1
  /** Per-part correctness for match/cloze/gap, for the review screen. */
  parts?: boolean[];
}
