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

export interface Question {
  id: string;
  module: number; // 1..5 for TMC221
  lecture: number; // the source lecture number
  slides: string[]; // provenance, e.g. ["L1 S9"] - shown in review
  style: Style;
  difficulty: Difficulty;
  facets: Facet[];
  topic: string; // short label, e.g. "OKR", "the 7 Kits"
  prompt: string; // for cloze/gap the blanks are marked {{1}}, {{2}}, ...
  options?: Option[]; // mcq, multi
  answer?: string | string[]; // mcq: 'c'   multi: ['a','b']   tf: 'true' | 'false'
  pairs?: Pair[]; // match
  extraLabels?: string[]; // match: decoy labels added to the dropdown
  blanks?: Blank[]; // cloze, gap
  explanation: string; // always shown in review
}

export interface Paper {
  /** A fixed, ordered paper such as the real test. Not shuffled, not filtered. */
  id: string;
  title: string;
  subtitle: string;
  note: string;
  questions: Question[];
}

export interface ModuleMeta {
  number: number;
  title: string;
  lecture: number;
  blurb: string;
}

export interface Course {
  code: string;
  title: string;
  modules: ModuleMeta[];
  questions: Question[];
  papers: Paper[];
}

// ---- what the setup screen produces ----

export type GapMode = 'typed' | 'choice';

export interface TestConfig {
  modules: number[]; // empty means every module
  facets: Facet[]; // empty means no facet restriction
  mix: Record<Difficulty, number>; // percentages, normalised before use
  count: number;
  gapMode: GapMode;
  shuffleOptions: boolean;
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
