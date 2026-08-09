/**
 * Bank gate. Runs before every build, so a broken or thin bank cannot deploy.
 *
 *     npm run validate
 *
 * Four jobs, applied per course from the COURSES table below.
 *
 * 1. SCHEMA. Every question is well formed and answerable: unique id, a key that
 *    actually points at an option, dropdown choices that contain the right
 *    answer, no blank without an accepted answer. A question whose key names a
 *    missing option is unanswerable and would silently mark the student wrong
 *    forever, which is the worst failure this thing can have.
 *
 * 2. COVERAGE. The forcing function the manuals themselves use. For TMC221 that
 *    is slide coverage: every content-bearing slide of all five decks must be
 *    cited by at least one question, because a slide nothing asks about is a
 *    slide the student is never tested on. For IFT222 it is question coverage:
 *    all 120 objective questions from both tests must be present, exactly once
 *    each, with no gap and no duplicate.
 *
 * 3. THE KEY. IFT222 questions are cross-checked, letter by letter, against the
 *    answer key transcribed from the original test screenshots and held here
 *    independently of the JSON. Two transcriptions that disagree fail the build
 *    rather than shipping a wrong answer.
 *
 * 4. THE VERDICTS. Where a course explains its options, EVERY option must carry
 *    a verdict: why the key is the key, and what is wrong with each of the
 *    others. Half-explained questions do not ship.
 *
 * 5. THE LEDGER. ENT221 carries data/ent221/ledger/*.json, an enumeration of
 *    every atomic testable fact in its sources. Every fact must be named by at
 *    least one question, and every fact marked hard (numeric, named, listed or
 *    definitional) must be asked in at least two different styles, so it cannot
 *    be memorised as a single phrasing. A question may only name a fact whose
 *    own source reference it also cites, which is what keeps the reference chip
 *    on screen honest.
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildIndex, serialise, INDEX_FILE } from './build-ledger-index.mjs';
import { IFT_DECK_SLIDES } from './ift-slides.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA = join(HERE, '..', 'data');

const STYLES = ['mcq', 'multi', 'tf', 'match', 'cloze', 'gap'];
const DIFFS = ['easy', 'medium', 'hard'];
const FACETS = ['numbers', 'names', 'lists', 'wording'];
const FORMATS = ['word', 'words', 'number', 'percent', 'time', 'name', 'phrase'];

function range(a, b) {
  const out = [];
  for (let i = a; i <= b; i++) out.push(i);
  return out;
}

/**
 * The IFT222 answer key, transcribed from the test screenshots alongside the
 * bank and kept here as an independent second copy. Index 0 is question 1.
 */
const IFT_KEY = {
  'Test 1': (
    'cbbcbcabca' +
    'bbccacdcdb' +
    'dcdadbdbad' +
    'dcdabddadd' +
    'dcadacdaad' +
    'bdcaddaddb'
  ).split(''),
  'Test 2': (
    'bbabacdcdb' +
    'bbbbadabab' +
    'caabbadbbd' +
    'ddbabbbdaa' +
    'cdbbbddcab' +
    'dbdbadbcdb'
  ).split(''),
};

/**
 * The ENT221 answer keys, transcribed here a second time and independently of
 * the bank. Test 2 was captured as a graded 30 out of 30 review page, so every
 * one of its answers is confirmed by the examiner. Test 1 was captured
 * unattempted and carries no printed key, so these are the answers derived from
 * the course text in the shipped ENT221 manual; keeping them here means the
 * drill and the manual can never quietly disagree about what the answer is.
 *
 * Question 4 is absent from Test 1: the examiner omitted it.
 */
const ENT_KEY = {
  'Test 1': {
    1: 'd', 2: 'a', 3: 'value chain', 5: 'satiation', 6: 'b', 7: 'd', 8: 'c',
    9: 'Multiply', 10: 'b', 11: 'a', 12: 'd', 13: 'a', 14: 'Hygiene',
    15: 'agripreneurship', 16: 'd', 17: 'c', 18: 'a', 19: 'a', 20: 'a', 21: 'b',
    22: 'd', 23: 'b', 24: 'c', 25: 'd', 26: 'c', 27: 'a', 28: 'b', 29: 'b', 30: 'c',
  },
  'Test 2': {
    1: 'a', 2: 'c', 3: 'a', 4: 'b', 5: 'b', 6: 'b', 7: 'water', 8: 'true', 9: 'a',
    10: 'a', 11: 'd', 12: 'c', 13: 'high', 14: 'Aquaponic', 15: 'business',
    16: 'art', 17: 'grading', 18: 'a', 19: 'poor', 20: 'water pollution',
    21: 'hatchery', 22: '8.5', 23: 'kitchen', 24: 'b', 25: 'c', 26: 'd',
    27: 'market', 28: 'a', 29: 'false', 30: 'c',
  },
};

/**
 * The PHY121 answer keys, transcribed a second time from the graded review
 * pages and kept here independently of the bank.
 *
 * Test 2 was marked 15 out of 15, so every one of its answers is confirmed by
 * the examiner. Test 1 was marked 14 out of 15: question 9 is the one marked
 * WRONG, and its stem is also truncated in the capture with its figure missing,
 * so no true key exists for it. It is keyed here to the option that was
 * selected, matching the bank, purely so the paper stays answerable end to end.
 * The question's own review says plainly that it cannot be judged.
 */
const PHY_KEY = {
  'Test 1': {
    1: 'e', 2: 'd', 3: 'c', 4: 'c', 5: 'c', 6: 'd', 7: 'c', 8: 'c',
    9: 'c', 10: 'c', 11: 'a', 12: 'a', 13: 'b', 14: 'b', 15: 'b',
  },
  // Every answer on this paper was the first option. That is a real property of
  // the paper, not a transcription slip, and it is why the drill shuffles.
  'Test 2': {
    1: 'a', 2: 'a', 3: 'a', 4: 'a', 5: 'symmetry', 6: 'a', 7: 'a', 8: 'a',
    9: 'a', 10: 'a', 11: 'flux', 12: 'distance', 13: 'a', 14: 'a', 15: 'a',
  },
};

const ENT_TEST1_NUMBERS = range(1, 30).filter((n) => n !== 4);

/**
 * ENT221's three lecture decks.
 *
 * The files Victor dropped are misnamed: the deck called "oil palm cultivation"
 * is the PROCESSING deck, the one called "oil palm processing" is the MODULE
 * FOUR deck, and the one called "value chain" is the CULTIVATION deck. Every
 * reference below and in the bank names the deck by its CONTENT, never by its
 * filename. Title, learning-objective, image-only and self-assessment slides
 * carry nothing testable and are excluded.
 */
const ENT_DECK_SLIDES = [
  ...[2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14].map((n) => `Cultivation S${n}`),
  ...[3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map((n) => `Processing S${n}`),
  ...range(3, 21).filter((n) => n !== 5).map((n) => `Agribusiness S${n}`),
];

/** Every numbered subsection of the 88-page course text, plus its glossary. */
const ENT_TEXT_SECTIONS = [
  ...range(1, 3).map((n) => `Text 1.1.${n}`),
  ...range(1, 9).map((n) => `Text 2.1.${n}`),
  ...range(1, 6).map((n) => `Text 3.1.${n}`),
  ...range(1, 5).map((n) => `Text 3.2.${n}`),
  ...range(1, 6).map((n) => `Text 4.1.${n}`),
  ...range(1, 5).map((n) => `Text 4.2.${n}`),
  ...range(1, 4).map((n) => `Text 4.3.${n}`),
  'Text 5.1.1',
  'Text 5.2.1',
  'Text 5.2.2',
  'Text 5.3.1',
  'Text 5.3.2',
  'Text 5.3.3',
  'Text Glossary',
];

/**
 * Every PHY121 lecture slide that carries a question the lecturer actually set.
 *
 * The five decks are 68 per cent images, so these were recovered by rendering
 * each page and reading it. That work is expensive and easy to lose: a careless
 * edit could drop a question and nothing would notice. Listing the slides here
 * and requiring each to be cited turns the recovery into something the build
 * enforces rather than something a commit message claims.
 *
 * Not a claim that these are the ONLY question slides. It is a floor: what has
 * been found stays found. Add to this list as more are recovered.
 */
const PHY_SLIDE_QUESTIONS = [
  "M1 S55",
  "M1 S56",
  "M1 S57",
  "M1 S58",
  "M1 S59",
  "M1 S60",
  "M1 S61",
  "M1 S62",
  "M1 S63",
  "M1 S64",
  "M1 S65",
  "M1 S66",
  "M1 S67",
  "M1 S68",
  "M1 S69",
  "M1 S70",
  "M1 S75",
  "M2 S11",
  "M2 S17",
  "M2 S18",
  "M2 S19",
  "M2 S20",
  "M2 S21",
  "M2 S23",
  "M2 S24",
  "M3 S6",
  "M3 S8",
  "M3 S9",
  "M3 S18",
  "M3 S19",
  "M3 S23",
  "M3 S37",
  "M3 S38",
  "M3 S46",
  "M3 S47",
  "M3 S51",
  "M3 S52",
  "M3 S55",
  "M3 S57",
  "M3 S62",
  "M3 S63",
  "M3 S64",
  "M3 S66",
  "M3 S67",
  "M3 S92",
  "M3 S93",
  "M3 S95",
  "M3 S96",
  "M3 S97",
  "M3 S98",
  "M3 S99",
  "M4 S35",
  "M4 S36",
  "M4 S50",
  "M4 S63",
  "M4 S84",
  "M4 S86",
  "M4 S89",
  "M4 S90",
  "M4 S104",
  "M5 S29",
  "M5 S30",
  "M5 S32",
  "M5 S34",
  "M5 S36",
  "M5 S37",
  "M5 S42",
  "M5 S43",
  "M5 S44",
  "M5 S45"
];

const COURSES = [
  {
    code: 'TMC221',
    dir: 'tmc221',
    // Content slides per deck: title and closing "Thank You" slides carry
    // nothing testable and are excluded. Matches qa_coverage.py in the build.
    slideRef: /^L[1-5] S\d{1,2}$/,
    slideRefHelp: 'like "L2 S9"',
    requireLecture: true,
    minPerModule: 100,
    requireEveryStyle: true,
    coverages: [
      {
        kind: 'at-least-once',
        required: Object.entries({
          L1: range(2, 20),
          L2: range(2, 19),
          L3: range(2, 15),
          L4: range(2, 19),
          L5: range(2, 19),
        }).flatMap(([deck, slides]) => slides.map((n) => `${deck} S${n}`)),
        noun: 'content slides of the five decks',
      },
    ],
  },
  {
    code: 'IFT222',
    dir: 'ift222',
    // Two shapes of provenance: a numbered slide of one of the eight lecture
    // decks, or a question from one of the two computer-based tests. The deck
    // keys and the content slides they admit live in scripts/ift-slides.mjs.
    slideRef: /^((Intro|Data|ISA|Mem|Cache|RISC|Pipe|Rev) S\d{1,2}|Test [12] Q\d{1,2})$/,
    slideRefHelp: 'like "Mem S37" or "Test 1 Q16"',
    examRef: /^Test [12] Q\d{1,2}$/,
    requireLecture: false,
    minPerModule: 5,
    // The objective tests are pure MCQ, so demanding all six styles of every
    // question would be demanding the drill differ from the exam. The deck
    // questions do carry variety, and requireStyles below insists on it.
    requireEveryStyle: false,
    requireStyles: ['mcq', 'tf', 'gap', 'match', 'cloze', 'multi'],
    requireWhy: true,
    requireFacts: 'non-exam',
    coverages: [
      {
        kind: 'at-least-once',
        required: IFT_DECK_SLIDES,
        noun: 'content slides of the eight lecture decks',
      },
      {
        kind: 'exactly-once',
        required: [
          ...range(1, 60).map((n) => `Test 1 Q${n}`),
          ...range(1, 60).map((n) => `Test 2 Q${n}`),
        ],
        noun: 'objective questions across the two tests',
        pattern: /^Test [12] Q\d+$/,
      },
    ],
    key: IFT_KEY,
    ledger: 'ledger',
    // The crash course split into dated sittings, checked against the week.
    plan: 'plan.json',
    requireFrames: true,
    // Every question the examiner set must be asked inside the lesson that
    // teaches it, so the crash course stands on its own.
    selfSufficient: true,
    examTagPrefixes: ['Test 1 Q', 'Test 2 Q'],
    // The crash course, converted by scripts/import-crash.mjs. Every drill topic
    // must be taught by some lesson: a topic with questions and no lesson is a
    // hole a reader falls into.
    lessons: 'lessons.json',
    // And every one of the 600 ledger facts must be taught by some lesson
    // BLOCK, not merely have its topic mentioned. Armed once all 600 were.
    teachesLedger: true,
  },
  {
    code: 'PHY121',
    dir: 'phy121',
    // Stage one is the two computer-based tests only. The manual-derived bank
    // lands next, and will bring deck refs and a ledger with it.
    // Two shapes of provenance: a question from one of the two computer-based
    // tests, or a numbered section of the study manual's reference sheet. The
    // slide PDFs are almost entirely images, so the 172-page manual is what the
    // ledger is built from. See data/phy121/BUILD.md.
    // Three shapes of provenance: a numbered slide of one of the five
    // lecture decks, a section of the manual's reference sheet, or a
    // question from one of the two computer-based tests.
    slideRef: /^(Test [12] Q\d{1,2}|Ref R\.\d|M[1-5] S\d{1,3})$/,
    slideRefHelp: 'like "Test 1 Q12" or "Ref R.1"',
    examRef: /^Test [12] Q\d{1,2}$/,
    requireLecture: false,
    minPerModule: 2,
    // PHY's test is calculation by five-option MCQ, with fill-in-the-gap used
    // ONLY for concepts, never for a number. Demanding the other four styles
    // would be demanding the drill differ from the exam.
    requireEveryStyle: false,
    requireStyles: ['mcq', 'gap', 'tf'],
    requireWhy: true,
    coverages: [
      {
        kind: 'at-least-once',
        required: PHY_SLIDE_QUESTIONS,
        noun: 'lecture slides carrying a question the lecturer set',
      },
      {
        kind: 'exactly-once',
        required: [
          ...range(1, 15).map((n) => `Test 1 Q${n}`),
          ...range(1, 15).map((n) => `Test 2 Q${n}`),
        ],
        noun: 'questions across the two computer-based tests',
        pattern: /^Test [12] Q\d+$/,
      },
    ],
    key: PHY_KEY,
    // The ledger of the manual's reference sheet: 122 facts, 113 of them hard.
    // Armed once every one of them was tested, so it now holds the line.
    ledger: 'ledger',
    // The 30 computer-based-test questions are transcriptions, not derivations,
    // so they are exempt: their provenance is the paper itself.
    requireFacts: 'non-exam',
    // Every drill topic must be taught by some lesson: a topic with questions
    // and no lesson is a hole a reader falls into.
    lessons: 'lessons.json',
    // The crash course split into dated sittings, checked against the week.
    plan: 'plan.json',
    requireFrames: true,
    // Every question the examiner set must be asked inside the lesson that
    // teaches it, so the crash course stands on its own.
    selfSufficient: true,
    examTagPrefixes: ['Test 1 Q', 'Test 2 Q'],
    // And every fact the drill tests must be taught by some lesson BLOCK. The
    // topic-level check passed while Kirchhoff's laws, the dividers, the
    // dividers' traps, equipotentials and the plane wave were never taught at
    // all. This is what closes that.
    teachesLedger: true,
  },
  {
    code: 'CSC242',
    dir: 'csc242',
    // Two objective tests, 45 questions. The bank is those tests; the teaching
    // and every solved past paper live in the crash course, scoped to the
    // twelve modules of the CCODEL manual, which is what this paper is set
    // from. Filed by PAPER rather than by topic, because one test spans several.
    slideRef: /^Test [12] Q\d{1,2}$/,
    slideRefHelp: 'like "Test 2 Q14"',
    examRef: /^Test [12] Q\d{1,2}$/,
    requireLecture: false,
    minPerModule: 0,
    filesAreTopics: false,
    bankCoversAllTopics: false,
    requireEveryStyle: false,
    requireStyles: ['mcq'],
    requireWhy: true,
    coverages: [
      {
        kind: 'exactly-once',
        required: [
          ...range(1, 15).map((n) => `Test 1 Q${n}`),
          ...range(1, 30).map((n) => `Test 2 Q${n}`),
        ],
        noun: 'questions across the two objective tests',
        pattern: /^Test [12] Q\d+$/,
      },
    ],
    lessons: 'lessons.json',
    plan: 'plan.json',
    requireFrames: true,
    selfSufficient: true,
    examTagPrefixes: ['Test 1 Q', 'Test 2 Q'],
  },
  {
    code: 'DTS224',
    dir: 'dts224',
    // Provenance is the 25/26 objective test. The bank IS that test for now:
    // the teaching, and every past-paper THEORY question, live in the crash
    // course, where each one is printed as the examiner set it and then solved.
    // So minPerModule is 0 deliberately, and says so rather than pretending the
    // bank already covers all ten topics.
    // Two shapes of provenance: a question from the 25/26 objective test, or a
    // module of the manual, which is where the authored drill questions come
    // from now that the taught-but-undrilled topics are being closed.
    slideRef: /^(Test 1 Q\d{1,2}|Manual M[1-5]( U\d| SQL)?)$/,
    slideRefHelp: 'like "Test 1 Q12" or "Manual M4"',
    // Every question the manual prints must reach the crash course.
    printedFrom: 'DTS224 - Data Management I/build/content',
    examRef: /^Test 1 Q\d{1,2}$/,
    requireLecture: false,
    minPerModule: 0,
    // Filed by PAPER, not by topic: one objective test split across two files,
    // whose 30 questions come from four different topics.
    filesAreTopics: false,
    // The bank is the objective test only; the lessons teach all ten topics.
    bankCoversAllTopics: false,
    requireEveryStyle: false,
    requireStyles: ['mcq'],
    requireWhy: true,
    coverages: [
      {
        kind: 'exactly-once',
        required: range(1, 30).map((n) => `Test 1 Q${n}`),
        noun: 'questions on the 25/26 objective test',
        pattern: /^Test 1 Q\d+$/,
      },
    ],
    lessons: 'lessons.json',
    plan: 'plan.json',
    requireFrames: true,
    selfSufficient: true,
    examTagPrefixes: ['Test 1 Q'],
  },
  {
    code: 'ENT221',
    dir: 'ent221',
    // Three shapes of provenance: a numbered section of the 88-page course
    // text, a numbered slide of one of the three lecture decks, or a question
    // from one of the two computer-based tests.
    slideRef:
      /^(Text (\d\.\d\.\d|Glossary)|(Cultivation|Processing|Agribusiness) S\d{1,2}|Test [12] Q\d{1,2})$/,
    slideRefHelp: 'like "Text 2.1.4", "Cultivation S7" or "Test 2 Q22"',
    requireLecture: false,
    minPerModule: 30,
    // The computer-based tests use single-answer MCQ, true or false, and fill
    // in the gap. Matching and cloze are drill-only, added where a list has to
    // be learned whole, so demanding all six styles is right here.
    requireEveryStyle: false,
    requireStyles: ['mcq', 'tf', 'gap'],
    requireWhy: true,
    requireFacts: true,
    coverages: [
      {
        kind: 'at-least-once',
        required: ENT_TEXT_SECTIONS,
        noun: 'sections of the course text',
      },
      {
        kind: 'at-least-once',
        required: ENT_DECK_SLIDES,
        noun: 'content slides of the three lecture decks',
      },
      {
        kind: 'exactly-once',
        required: [
          ...ENT_TEST1_NUMBERS.map((n) => `Test 1 Q${n}`),
          ...range(1, 30).map((n) => `Test 2 Q${n}`),
        ],
        noun: 'questions from the two computer-based tests',
        pattern: /^Test [12] Q\d+$/,
      },
    ],
    key: ENT_KEY,
    ledger: 'ledger',
  },
];

const problems = [];

function check(cond, msg) {
  if (!cond) problems.push(msg);
}

/**
 * Text may never point at an option by its POSITION.
 *
 * Options are shuffled at run time and the letters A, B, C, D are assigned from
 * the position on screen, not from the stored option id. So an explanation that
 * says "option A is MULTIPLY" is telling the reader to look at whichever option
 * happened to land first, which is almost never the one meant. It shipped that
 * way on ENT221 Test 2 Q28 and read as a flat contradiction of the verdicts
 * printed directly beneath it.
 *
 * The fix is always the same: name the option by its CONTENT. "The marketing
 * mix answer is MULTIPLY" survives any shuffle. Per-option verdicts are safe
 * without help, because the `why` map is keyed by option id.
 */
const POSITIONAL = [
  /\b[Oo]ptions?\s+[A-Da-d]\b/,
  /\b(?:the\s+)?(?:first|second|third|fourth|fifth|last)\s+(?:option|answer|choice)\b/i,
  // A lowercase "a" is the English article far more often than an option
  // letter ("choose a location"), so these four accept a bare "a" only when it
  // is capitalised. The keyword itself is matched either way, which is why the
  // case-insensitive flag cannot simply be used on the whole pattern.
  /\b[Aa]nswer\s+(?:[A-D]|[b-d])\b/,
  /\b[Cc]hoice\s+(?:[A-D]|[b-d])\b/,
  /\b(?:[Tt]ake|[Pp]ick|[Cc]hoose|[Ss]elect)\s+(?:[A-D]|[b-d])\b/,
  /\b[Bb]oth\s+(?:[A-D]|[b-d])\s+and\s+[A-Da-d]\b/,
  /\b(?:[A-D]|[b-d])\s+(?:is|was)\s+(?:the\s+)?(?:correct|right|wrong|answer)\b/,
];

function noPositionalRefs(q, cfg) {
  const at = `${cfg.code} [${q.id}]`;
  const texts = [['explanation', q.explanation ?? '']];
  for (const [k, v] of Object.entries(q.why ?? {})) texts.push([`why.${k}`, v ?? '']);
  for (const [where, txt] of texts)
    for (const re of POSITIONAL) {
      const m = txt.match(re);
      if (m)
        check(
          false,
          `${at}: ${where} says ${JSON.stringify(m[0])}, but options are shuffled and letters come from position. Name the option by its content instead.`
        );
    }
}

/**
 * A figure is inline SVG injected into the page, so the gate is what stands
 * between an authored diagram and the DOM.
 *
 * It must: be real SVG, carry a viewBox so it scales to a phone, carry alt
 * text so it is not invisible to a screen reader, and contain nothing that
 * executes or reaches the network. The app is installable and used offline,
 * so a diagram that fetches anything is broken by definition, not merely
 * unsafe.
 */
function checkFigure(q, cfg) {
  if (!q.figure) return;
  const at = `${cfg.code} [${q.id}] figure`;
  const svg = q.figure.svg ?? '';
  check(typeof svg === 'string' && svg.trim().startsWith('<svg'), `${at}: must start with <svg`);
  check(/<\/svg>\s*$/.test(svg.trim()), `${at}: must end with </svg>`);
  check(/viewBox=/.test(svg), `${at}: needs a viewBox, or it cannot scale on a phone`);
  check(
    typeof q.figure.alt === 'string' && q.figure.alt.trim().length > 10,
    `${at}: needs alt text a screen reader can use`
  );
  for (const [re, what] of [
    [/<script/i, 'a script'],
    [/<foreignObject/i, 'a foreignObject'],
    [/\son\w+\s*=/i, 'an inline event handler'],
    [/(?:href|src)\s*=\s*["']?(?:https?:)?\/\//i, 'an external reference'],
    [/url\(\s*["']?(?:https?:)?\/\//i, 'an external url()'],
  ])
    check(!re.test(svg), `${at}: contains ${what}, which must never reach the page`);
}

/**
 * Every question file on disk must actually be imported by data/courses.ts.
 *
 * The gate globs the data directory; the app imports each file BY NAME. Those
 * two can drift, and they did: eight PHY121 slide files passed every check here
 * while being completely invisible in the running app, so the bank read 30 when
 * 122 questions existed. Passing the gate had stopped meaning "a reader can see
 * it", which is the only thing the gate is for.
 */
function checkWired(cfg, files) {
  const src = readFileSync(join(DATA, 'courses.ts'), 'utf8');
  for (const f of files)
    check(
      src.includes(`${cfg.dir}/${f}`),
      `${cfg.code}: ${f} holds questions but data/courses.ts never imports it, so the app cannot serve them`
    );
}

function validate(q, where, cfg, seenIds) {
  const at = `${cfg.code} ${where} [${q.id ?? '(no id)'}]`;
  check(typeof q.id === 'string' && q.id.length > 0, `${at}: missing id`);
  check(!seenIds.has(q.id), `${at}: duplicate id`);
  seenIds.add(q.id);
  check(Number.isInteger(q.module), `${at}: module must be a number`);
  if (cfg.requireLecture)
    check(Number.isInteger(q.lecture), `${at}: lecture must be a number`);
  check(
    Array.isArray(q.slides) && q.slides.length > 0,
    `${at}: needs at least one provenance reference`
  );
  (q.slides ?? []).forEach((s) =>
    check(
      cfg.slideRef.test(s),
      `${at}: malformed provenance ref ${JSON.stringify(s)}, expected ${cfg.slideRefHelp}`
    )
  );
  check(STYLES.includes(q.style), `${at}: unknown style ${q.style}`);
  check(DIFFS.includes(q.difficulty), `${at}: unknown difficulty ${q.difficulty}`);
  check(Array.isArray(q.facets) && q.facets.length > 0, `${at}: needs at least one facet`);
  (q.facets ?? []).forEach((f) => check(FACETS.includes(f), `${at}: unknown facet ${f}`));
  check(typeof q.topic === 'string' && q.topic.length > 0, `${at}: missing topic`);
  check(typeof q.prompt === 'string' && q.prompt.length > 0, `${at}: missing prompt`);
  check(
    typeof q.explanation === 'string' && q.explanation.length > 10,
    `${at}: explanation missing or too thin to teach from`
  );
  if (cfg.requireFacts) {
    // requireFacts: 'non-exam' exempts a question whose every reference is a
    // past-paper one. The paper IS its provenance. IFT222 needs this because
    // the two objective tests range wider than the eight lecture decks do, so
    // forcing a deck ref onto all 120 would mean inventing a source that is
    // not there. Deck-drilled questions are still held to the rule.
    const examOnly =
      cfg.requireFacts === 'non-exam' &&
      cfg.examRef &&
      (q.slides ?? []).length > 0 &&
      (q.slides ?? []).every((s) => cfg.examRef.test(s));
    if (!examOnly)
      check(
        Array.isArray(q.facts) && q.facts.length > 0,
        `${at}: names no ledger fact, so nothing ties it to anything in the source`
      );
  }

  if (q.style === 'mcq' || q.style === 'multi') {
    const ids = (q.options ?? []).map((o) => o.id);
    check(ids.length >= 3, `${at}: needs at least 3 options`);
    check(new Set(ids).size === ids.length, `${at}: duplicate option ids`);
    (q.options ?? []).forEach((o) =>
      check(
        typeof o.text === 'string' && o.text.trim().length > 0,
        `${at}: option ${o.id} has no text`
      )
    );
    if (q.style === 'mcq') {
      check(
        typeof q.answer === 'string' && ids.includes(q.answer),
        `${at}: answer ${JSON.stringify(q.answer)} is not one of the options`
      );
    } else {
      check(
        Array.isArray(q.answer) && q.answer.length >= 2,
        `${at}: a multiple-response needs at least 2 correct options`
      );
      (Array.isArray(q.answer) ? q.answer : []).forEach((a) =>
        check(ids.includes(a), `${at}: answer ${a} is not one of the options`)
      );
      check(
        (q.answer ?? []).length < ids.length,
        `${at}: every option is correct, so there is nothing to discriminate`
      );
    }

    // Every option explained, or none. A partly filled block is worse than an
    // absent one, because the reader assumes the silent options were fine.
    if (cfg.requireWhy || q.why) {
      check(
        q.why && typeof q.why === 'object',
        `${at}: no per-option verdicts, so a reader is never told why the other options fail`
      );
      for (const id of ids)
        check(
          typeof q.why?.[id] === 'string' && q.why[id].trim().length > 15,
          `${at}: option ${id} has no verdict explaining why it is right or wrong`
        );
      for (const id of Object.keys(q.why ?? {}))
        check(ids.includes(id), `${at}: verdict for option ${id}, which does not exist`);
    }
  }

  if (q.style === 'tf') {
    check(
      q.answer === 'true' || q.answer === 'false',
      `${at}: true/false answer must be the string "true" or "false"`
    );
    // A true or false question has two options even though it carries no
    // options array, and a reader who guessed needs both explained.
    if (cfg.requireWhy || q.why) {
      for (const id of ['true', 'false'])
        check(
          typeof q.why?.[id] === 'string' && q.why[id].trim().length > 15,
          `${at}: no verdict for "${id}", so a reader is never told why that side fails`
        );
      for (const id of Object.keys(q.why ?? {}))
        check(
          id === 'true' || id === 'false',
          `${at}: verdict keyed "${id}", but a true/false question only has "true" and "false"`
        );
    }
  }

  if (q.style === 'match') {
    check(
      Array.isArray(q.pairs) && q.pairs.length >= 2,
      `${at}: a matching question needs at least 2 pairs`
    );
    const lefts = (q.pairs ?? []).map((p) => p.left);
    check(new Set(lefts).size === lefts.length, `${at}: duplicate left-hand items`);
    (q.pairs ?? []).forEach((p) =>
      check(
        typeof p.right === 'string' && p.right.trim().length > 0,
        `${at}: pair "${p.left}" has no right-hand label`
      )
    );
  }

  if (q.style === 'cloze' || q.style === 'gap') {
    const marks = [...q.prompt.matchAll(/\{\{(\d+)\}\}/g)].map((m) => Number(m[1]));
    check(marks.length > 0, `${at}: prompt has no {{n}} blank markers`);
    check(
      Array.isArray(q.blanks) && q.blanks.length === marks.length,
      `${at}: ${marks.length} markers in the prompt but ${
        (q.blanks ?? []).length
      } blanks defined`
    );
    marks.forEach((n, idx) =>
      check(n === idx + 1, `${at}: blank markers must run 1,2,3... in order`)
    );
    (q.blanks ?? []).forEach((b, i) => {
      check(
        Array.isArray(b.accept) && b.accept.length > 0,
        `${at}: blank ${i + 1} has no accepted answer`
      );
      check(
        Array.isArray(b.choices) && b.choices.length >= 3,
        `${at}: blank ${i + 1} needs at least 3 dropdown choices`
      );
      check(
        (b.choices ?? []).includes(b.accept?.[0]),
        `${at}: blank ${i + 1} dropdown does not contain its own answer "${b.accept?.[0]}"`
      );
      check(
        new Set(b.choices ?? []).size === (b.choices ?? []).length,
        `${at}: blank ${i + 1} has duplicate choices`
      );
      if (b.format !== undefined)
        check(FORMATS.includes(b.format), `${at}: blank ${i + 1} unknown format ${b.format}`);
      if (q.style === 'gap')
        check(
          b.format !== 'phrase',
          `${at}: blank ${i + 1} is a typed short answer, so it cannot be format "phrase"`
        );
    });
  }
}

/**
 * The crash course.
 *
 * Lessons are converted from the manual, so the words are already gated there.
 * What has to be checked HERE is the conversion and the wiring: that no lesson
 * lost its teaching, that no programmed frame asks a question the reader is
 * never given the answer to, and that every drill topic is actually taught by
 * some lesson.
 */
function checkLessons(cfg, dir, bankModules, ledger, all) {
  const path = join(dir, cfg.lessons);
  const lessons = JSON.parse(readFileSync(path, 'utf8'));
  const slugs = new Set();
  const taught = new Set();
  const undrilled = new Set();
  const taughtFacts = new Set();
  let frames = 0;
  let recalls = 0;
  let worked = 0;

  check(Array.isArray(lessons) && lessons.length > 0, `${cfg.code}: ${cfg.lessons} is empty`);

  for (const l of lessons) {
    const at = `${cfg.code} lesson [${l.slug ?? '(no slug)'}]`;
    check(/^[a-z0-9-]+$/.test(l.slug ?? ''), `${at}: slug must be url-safe lower case`);
    check(!slugs.has(l.slug), `${at}: duplicate slug`);
    slugs.add(l.slug);
    check(Boolean(l.title), `${at}: no title`);
    check(Boolean(l.part), `${at}: no part, so the index cannot group it`);
    check((l.lead ?? '').length > 20, `${at}: lead missing or too thin`);
    check(Number.isFinite(l.minutes) && l.minutes > 0, `${at}: needs a sitting time`);
    check((l.blocks ?? []).length > 0, `${at}: no blocks, the conversion dropped it`);

    for (const m of l.modules ?? []) {
      // A lesson teaching a topic the bank never asks about is normally a
      // mistake. Where a course's bank is only its objective test, though, the
      // crash course legitimately runs ahead of it: the reader is taught
      // normalisation and SQL from the manual and from solved past papers even
      // though no objective question on this paper touched them. Such a course
      // says so with bankCoversAllTopics: false, and the shortfall is printed
      // rather than hidden.
      if (cfg.bankCoversAllTopics === false) {
        if (!bankModules.has(m)) undrilled.add(m);
      } else {
        check(bankModules.has(m), `${at}: teaches topic ${m}, which has no questions`);
      }
      taught.add(m);
    }

    for (const [i, b] of (l.blocks ?? []).entries()) {
      const where = `${at} block ${i} (${b.kind})`;

      // A block may declare the ledger facts it TEACHES, the mirror of the
      // facts a question declares it TESTS. Same discipline, opposite side.
      for (const id of b.facts ?? []) {
        const fact = ledger?.get(id);
        if (!fact) {
          problems.push(`${where}: teaches fact ${id}, which is not in the ledger`);
          continue;
        }
        check(
          (l.modules ?? []).includes(fact.topic),
          `${where}: teaches fact ${id}, which belongs to topic ${fact.topic}, but this lesson covers topic ${(l.modules ?? []).join(', ') || 'nothing'}`
        );
        taughtFacts.add(id);
      }

      if (b.kind === 'frames') {
        check((b.frames ?? []).length >= 2, `${where}: fewer than 2 frames`);
        frames += (b.frames ?? []).length;
        (b.frames ?? []).forEach((f, j) => {
          check(Boolean((f.teach ?? '').trim()), `${where}: frame ${j + 1} has no teaching text`);
          // A question with nothing after it is a reader left hanging: the check
          // that answers frame j lives at the head of frame j + 1.
          // Frame text is rendered as HTML, so a bare caret reaches the
          // reader as a literal "10^-9" instead of a superscript. In a physics
          // course that is on nearly every line.
          for (const [field, txt] of [['check', f.check], ['teach', f.teach], ['ask', f.ask]])
            check(
              !/\^-?\d/.test(txt ?? ''),
              `${where} frame ${j + 1}: ${field} writes an exponent as "^", which renders literally. Use <sup>.`
            );
          if (f.ask && j === b.frames.length - 1)
            check(false, `${where}: the last frame asks a question nothing answers`);
        });
      } else if (b.kind === 'worked') {
        worked += 1;
        check(
          Boolean(b.working || b.answer),
          `${where}: nothing to reveal, so the worked example teaches nothing`
        );
        check(['model', 'example'].includes(b.mode), `${where}: unknown mode ${b.mode}`);
      } else if (b.kind === 'recall') {
        recalls += 1;
        check(Boolean(b.question), `${where}: no question`);
        check(Boolean(b.answer), `${where}: no answer, so it cannot be self-marked`);
      } else if (['rules', 'trap', 'teach', 'prose'].includes(b.kind)) {
        check(Boolean((b.html ?? '').trim()), `${where}: empty body`);
      } else if (b.kind === 'asprinted') {
        check(Boolean((b.printed ?? '').trim()), `${where}: no printed question text`);
      }

      // House style, with the exam's own words exempt: an AS PRINTED block is
      // evidence and is quoted exactly, dashes and all.
      if (b.kind !== 'asprinted')
        for (const v of Object.values(b))
          if (typeof v === 'string' && /[—–]/.test(v))
            problems.push(`${where}: em or en dash in "${v.slice(0, 60)}..."`);
    }
  }

  // The crash course must be SELF-SUFFICIENT: every question the examiner
  // actually set is asked inside the lesson that teaches it, and asked once.
  // A lesson that teaches a skill and then sends the reader elsewhere to be
  // tested on it is a lesson the reader finishes without ever being tested.
  if (cfg.selfSufficient) {
    const examQs = all.filter((q) =>
      (q.slides ?? []).some((s) => cfg.examTagPrefixes.some((t) => s.startsWith(t)))
    );
    const asked = new Map();
    for (const l of lessons) {
      for (const [i, b] of (l.blocks ?? []).entries()) {
        if (b.kind !== 'drill') continue;
        const where = `${cfg.code} lesson [${l.slug}] block ${i} (drill)`;
        check(['exam', 'all'].includes(b.pick), `${where}: pick must be 'exam' or 'all'`);
        check((b.label ?? '').length > 10, `${where}: label missing or too thin`);
        const topics = b.topics ?? l.modules ?? [];
        for (const t of topics)
          check(
            (l.modules ?? []).includes(t),
            `${where}: drills topic ${t}, which this lesson does not teach`
          );
        const picked = examQs.filter(
          (q) => topics.includes(q.module) || (b.ids ?? []).includes(q.id)
        );
        check(picked.length > 0, `${where}: asks no questions at all`);
        for (const q of picked) {
          if (asked.has(q.id))
            problems.push(
              `${cfg.code}: question ${q.id} is asked by two lessons, ${asked.get(q.id)} and ${l.slug}`
            );
          else asked.set(q.id, l.slug);
        }
      }
    }
    const never = examQs.filter((q) => !asked.has(q.id));
    console.log(
      `    ${never.length ? 'x' : '.'} crash course asks: ${asked.size} of ${
        examQs.length
      } questions the examiner set, each in the lesson that teaches it${
        never.length ? `, ${never.length} asked nowhere` : ''
      }`
    );
    for (const q of never.slice(0, 20))
      problems.push(
        `${cfg.code}: ${q.id} (topic ${q.module}, ${q.slides[0]}) is an exam question no lesson asks`
      );
  }

  // The dated reading plan. A plan that has drifted from the lessons is worse
  // than no plan: it sends a reader who is short of time to a lesson that does
  // not exist, or quietly drops one they needed.
  if (cfg.plan) {
    const plan = JSON.parse(readFileSync(join(dir, cfg.plan), 'utf8'));
    // The paper's date comes from data/timetable.ts, the single place the week
    // is written down, so a plan can never outlive a rescheduled exam.
    const timetable = readFileSync(join(dir, '..', 'timetable.ts'), 'utf8');
    const exam = timetable
      .match(/code:\s*'([A-Z]{3}\d{3})',[\s\S]{0,200}?at:\s*'([0-9T:-]+)'/g)
      ?.map((m) => m.match(/code:\s*'([A-Z]{3}\d{3})'[\s\S]*at:\s*'([0-9T:-]+)'/))
      ?.find((m) => m?.[1] === cfg.code)?.[2];
    check(
      Boolean(exam),
      `${cfg.code}: carries a reading plan but the timetable has no paper for it`
    );
    const slugs = new Set(lessons.map((l) => l.slug));
    const scheduled = plan.flatMap((s) => s.lessons);
    const seen = new Set();

    for (const slug of scheduled) {
      check(slugs.has(slug), `${cfg.code} plan: schedules "${slug}", which is not a lesson`);
      check(!seen.has(slug), `${cfg.code} plan: schedules "${slug}" more than once`);
      seen.add(slug);
    }
    const unscheduled = [...slugs].filter((s) => !seen.has(s));
    check(
      unscheduled.length === 0,
      `${cfg.code} plan: ${unscheduled.length} lesson(s) are in no sitting: ${unscheduled.join(', ')}`
    );

    let previous = '';
    for (const s of plan) {
      check(
        /^\d{4}-\d{2}-\d{2}$/.test(s.date ?? ''),
        `${cfg.code} plan: bad date ${JSON.stringify(s.date)}`
      );
      check(
        s.date >= previous,
        `${cfg.code} plan: ${s.date} comes after ${previous}, so the sittings are out of order`
      );
      previous = s.date;
      check((s.goal ?? '').length > 20, `${cfg.code} plan ${s.date}: goal missing or too thin`);
      check(Boolean(s.window), `${cfg.code} plan ${s.date}: no time window`);
      check((s.lessons ?? []).length > 0, `${cfg.code} plan ${s.date}: schedules nothing`);
      if (exam)
        check(
          s.date <= exam.slice(0, 10),
          `${cfg.code} plan: a sitting on ${s.date} falls after the paper on ${exam.slice(0, 10)}`
        );
    }
    console.log(
      `    . reading plan: ${plan.length} dated sittings cover all ${slugs.size} lessons${
        exam ? `, none after the paper on ${exam.slice(0, 10)}` : ''
      }`
    );
  }

  if (cfg.bankCoversAllTopics === false && undrilled.size) {
    const list = [...undrilled].sort((a, b) => a - b).join(', ');
    console.log(
      `    . note: topics ${list} are TAUGHT but not yet drilled, so their questions live only in the solved past papers inside the lessons`
    );
  }

  // A lesson that teaches a topic must ASK before it tells. Guessing wrong
  // first measurably improves what sticks, and it is the one discipline a book
  // can only request while a screen can enforce it. Courses converted from a
  // manual arrive with none, which is exactly how DTS224 and CSC242 shipped
  // their first version, so this stops it happening again silently.
  // Every past-paper question the MANUAL prints must reach the platform. The
  // manual's own build gate refuses to pass while any question in any source is
  // unsolved, so the manual is the authority on what exists; this checks the
  // conversion did not quietly drop any on the way. It found 28 of DTS224's 79
  // missing, all because one "As printed" box can hold several years' wording
  // of the same question and the converter took only the first.
  if (cfg.printedFrom) {
    const dirPath = join(HERE, '..', '..', 'courses', cfg.printedFrom);
    if (existsSync(dirPath)) {
      const tags = new Set();
      for (const f of readdirSync(dirPath).filter((x) => x.endsWith('.html')))
        for (const m of readFileSync(join(dirPath, f), 'utf8').matchAll(/data-src="([^"]+)"/g))
          tags.add(m[1]);
      const whole = readFileSync(join(dir, cfg.lessons), 'utf8');
      const absent = [...tags].filter(
        (t) => !whole.includes(t) && !whole.includes(t.replace(/:/g, ', '))
      );
      console.log(
        `    ${absent.length ? 'x' : '.'} past papers: ${tags.size - absent.length} of ${
          tags.size
        } printed questions in the manual reached the crash course`
      );
      for (const a of absent.slice(0, 15))
        problems.push(`${cfg.code}: the manual prints ${a} but the crash course does not`);
    }
  }

  if (cfg.requireFrames) {
    const bare = lessons
      .filter((l) => (l.modules ?? []).length > 0)
      .filter((l) => !(l.blocks ?? []).some((b) => b.kind === 'frames'))
      .map((l) => l.slug);
    console.log(
      `    ${bare.length ? 'x' : '.'} frames: every topic lesson opens by asking${
        bare.length ? `, except ${bare.join(', ')}` : ''
      }`
    );
    for (const slug of bare)
      problems.push(
        `${cfg.code} lesson [${slug}]: teaches a topic but never asks before it tells, so it has no programmed frames`
      );
  }

  const untaught = [...bankModules].filter((m) => !taught.has(m)).sort((a, b) => a - b);
  console.log(
    `    ${untaught.length ? 'x' : '.'} crash course: ${lessons.length} lessons, ${frames} frames, ${worked} worked, ${recalls} recalls, ${
      untaught.length ? `topics never taught: ${untaught.join(', ')}` : 'every topic taught'
    }`
  );
  check(
    untaught.length === 0,
    `${cfg.code}: topics ${untaught.join(', ')} have questions but no lesson teaches them`
  );

  // "Every topic is taught" is a weak claim: a lesson that mentions topic 5
  // satisfies it while saying nothing about Kirchhoff's laws. This is the real
  // one. Anything the drill TESTS, the crash course must TEACH, fact by fact,
  // or a reader who works through every lesson still meets questions on
  // material they were never shown.
  if (cfg.teachesLedger && ledger) {
    const drilled = [...ledger.values()].filter((f) => f.tested);
    const missing = drilled.filter((f) => !taughtFacts.has(f.id));
    console.log(
      `    ${missing.length ? 'x' : '.'} crash course teaches: ${
        drilled.length - missing.length
      } of ${drilled.length} drilled facts${
        missing.length ? `, ${missing.length} never taught` : ', none left untaught'
      }`
    );
    for (const f of missing.slice(0, 40))
      problems.push(
        `${cfg.code}: fact ${f.id} (topic ${f.topic}) is drilled but no lesson teaches it: "${f.fact.slice(0, 70)}"`
      );
    if (missing.length > 40)
      problems.push(`${cfg.code}: ...and ${missing.length - 40} more facts drilled but never taught`);
  }
}

/**
 * The fact ledger.
 *
 * data/<course>/ledger/*.json enumerates every atomic testable fact in the
 * course sources. This is the leave-no-stone-unturned check, and it bites in
 * three directions:
 *
 *   1. every fact is named by at least one question;
 *   2. every fact marked hard is asked in at least two different styles, so it
 *      cannot be learned as one phrasing and then missed when reworded;
 *   3. a question may only name a fact whose own source reference it also
 *      cites, so the reference chip printed under the answer is the reference
 *      the fact actually came from.
 */
function checkLedger(cfg, dir, all) {
  const ledgerDir = join(dir, cfg.ledger);
  check(existsSync(ledgerDir), `${cfg.code}: no ledger directory at ${ledgerDir}`);
  if (!existsSync(ledgerDir)) return;

  const byId = new Map();
  for (const f of readdirSync(ledgerDir).filter((f) => f.endsWith('.json'))) {
    for (const e of JSON.parse(readFileSync(join(ledgerDir, f), 'utf8'))) {
      check(!byId.has(e.id), `${cfg.code} ledger ${f}: duplicate fact id ${e.id}`);
      check(
        typeof e.fact === 'string' && e.fact.length > 20,
        `${cfg.code} ledger ${f} [${e.id}]: fact text missing or too thin`
      );
      check(
        typeof e.ref === 'string' && cfg.slideRef.test(e.ref),
        `${cfg.code} ledger ${f} [${e.id}]: bad source ref ${JSON.stringify(e.ref)}`
      );
      byId.set(e.id, e);
    }
  }

  const styles = new Map();
  for (const q of all) {
    for (const id of q.facts ?? []) {
      const fact = byId.get(id);
      if (!fact) {
        problems.push(`${cfg.code} [${q.id}]: names fact ${id}, which is not in the ledger`);
        continue;
      }
      check(
        (q.slides ?? []).includes(fact.ref),
        `${cfg.code} [${q.id}]: tests fact ${id} from ${fact.ref} but never cites ${fact.ref}`
      );
      if (!styles.has(id)) styles.set(id, new Set());
      styles.get(id).add(q.style);
    }
  }

  // The browser-side copy must match the ledger it was built from, or the
  // mastery map would name facts that no longer exist and miss ones that do.
  const indexPath = join(dir, INDEX_FILE);
  const expected = serialise(buildIndex(dir));
  const actual = existsSync(indexPath) ? readFileSync(indexPath, 'utf8') : null;
  if (actual !== expected) {
    problems.push(
      `${cfg.code}: ${INDEX_FILE} is out of step with the ledger. Run: node scripts/build-ledger-index.mjs`
    );
    console.log(`    x ledger index: ${INDEX_FILE} is stale`);
  } else {
    console.log(`    . ledger index: ${INDEX_FILE} matches the ledger`);
  }

  const facts = [...byId.values()];
  const untested = facts.filter((f) => !styles.has(f.id));
  const thin = facts.filter((f) => f.hard && (styles.get(f.id)?.size ?? 0) < 2);

  console.log(
    `    ${untested.length ? 'x' : '.'} ledger: ${facts.length} facts, ${
      facts.filter((f) => f.hard).length
    } of them hard, ${facts.length - untested.length} tested`
  );
  if (untested.length) {
    console.log(
      '        never tested: ' +
        untested.slice(0, 12).map((f) => f.id).join(', ') +
        (untested.length > 12 ? ` and ${untested.length - 12} more` : '')
    );
    problems.push(
      `${cfg.code}: ${untested.length} ledger facts are never tested by any question`
    );
  }
  console.log(
    `    ${thin.length ? 'x' : '.'} ledger: every hard fact asked in two or more styles${
      thin.length ? `, ${thin.length} asked in only one` : ''
    }`
  );
  if (thin.length) {
    console.log(
      '        one style only: ' +
        thin.slice(0, 12).map((f) => f.id).join(', ') +
        (thin.length > 12 ? ` and ${thin.length - 12} more` : '')
    );
    problems.push(
      `${cfg.code}: ${thin.length} hard ledger facts are asked in only one style`
    );
  }

  // Handed to checkLessons, which asks the opposite question: of everything the
  // drill tests, what does the crash course never teach?
  for (const f of facts) f.tested = styles.has(f.id);
  return byId;
}

/**
 * The same normalisation the app marks typed answers with, so the key check
 * accepts "8.5" for "8.5 " and "Aquaponic" for "aquaponic" but nothing looser.
 * Kept in step with normalise() in lib/grading.ts.
 */
function normaliseAnswer(raw) {
  return String(raw)
    .toLowerCase()
    .normalize('NFKD')
    .replace(/\b(the|a|an)\b/g, '')
    .replace(/&/g, 'and')
    .replace(/[^a-z0-9]/g, '');
}

/**
 * House style, carried over from the manuals: no em dashes, no en dashes.
 *
 * One exemption, and only one. A question taken from a real test reproduces the
 * examiner's stem and options exactly, dashes and all, because a paper that
 * tidies up its own wording is no longer the paper that was sat. The teaching
 * around it, the explanation and the verdicts, is ours and is held to the rule.
 */
function houseStyle(q, cfg) {
  const quoted = (q.slides ?? []).some((s) => /^Test [12] Q\d+$/.test(s));
  const texts = [
    ...(quoted ? [] : [q.prompt, ...(q.options ?? []).map((o) => o.text)]),
    q.explanation,
    ...Object.values(q.why ?? {}),
  ];
  for (const t of texts)
    if (/[—–]/.test(String(t)))
      problems.push(`${cfg.code} [${q.id}]: em or en dash in "${String(t).slice(0, 60)}..."`);
}

console.log('BANK GATE');
let grandTotal = 0;

for (const cfg of COURSES) {
  const dir = join(DATA, cfg.dir);
  const seenIds = new Set();
  const all = [];
  const perModule = {};

  // module<N>.json holds past-paper questions, deck<N>.json the ones written
  // from the lecture material. A topic whose deck questions outgrew one file
  // splits into deck08a, deck08b and so on; the letter is presentation only,
  // since every question carries its own `module` number.
  const moduleFiles = readdirSync(dir)
    .filter((f) => /^(module|deck|slides|close|second|test|drill)\d+[a-z]?\.json$/.test(f))
    .sort((a, b) => {
      const n = (f) => Number(f.match(/\d+/)[0]);
      return n(a) - n(b) || a.localeCompare(b);
    });

  checkWired(cfg, moduleFiles);

  for (const f of moduleFiles) {
    const items = JSON.parse(readFileSync(join(dir, f), 'utf8'));
    check(Array.isArray(items), `${cfg.code} ${f}: expected a JSON array`);
    for (const q of items) {
      validate(q, f, cfg, seenIds);
      houseStyle(q, cfg);
      noPositionalRefs(q, cfg);
      checkFigure(q, cfg);
    }
    all.push(...items);
    // Most banks are filed BY TOPIC, so the number in the filename is the topic
    // and any disagreement is a filing mistake worth catching: that rule caught
    // a whole PHY file sitting under the wrong topic. A bank filed by PAPER
    // instead, like DTS224's single objective test split across two files,
    // carries questions from many topics on purpose and says so with
    // filesAreTopics: false.
    const byTopic = cfg.filesAreTopics !== false;
    for (const q of items) {
      perModule[q.module] = (perModule[q.module] ?? 0) + 1;
      if (byTopic) {
        const n = Number(f.match(/\d+/)[0]);
        check(
          q.module === n,
          `${cfg.code} ${f} [${q.id}]: module field says ${q.module} but the file is module ${n}`
        );
      }
    }
  }

  for (const f of readdirSync(dir).filter((f) => f.endsWith('-test.json'))) {
    const paper = JSON.parse(readFileSync(join(dir, f), 'utf8'));
    check(typeof paper.id === 'string', `${cfg.code} ${f}: paper needs an id`);
    check(Array.isArray(paper.questions), `${cfg.code} ${f}: paper needs a questions array`);
    for (const q of paper.questions ?? []) {
      validate(q, f, cfg, seenIds);
      houseStyle(q, cfg);
    }
    all.push(...(paper.questions ?? []));
  }

  grandTotal += all.length;
  console.log(`\n  ${cfg.code}: ${all.length} questions in ${moduleFiles.length} files`);

  for (const [n, c] of Object.entries(perModule)) {
    const flag = c >= cfg.minPerModule ? '.' : 'x';
    console.log(`    ${flag} group ${n}: ${c} questions (minimum ${cfg.minPerModule})`);
    if (c < cfg.minPerModule)
      problems.push(
        `${cfg.code} group ${n} has ${c} questions, under the ${cfg.minPerModule} minimum`
      );
  }

  const styleCounts = {};
  const diffCounts = {};
  const facetCounts = {};
  for (const q of all) {
    styleCounts[q.style] = (styleCounts[q.style] ?? 0) + 1;
    diffCounts[q.difficulty] = (diffCounts[q.difficulty] ?? 0) + 1;
    for (const f of q.facets ?? []) facetCounts[f] = (facetCounts[f] ?? 0) + 1;
  }
  console.log(
    '    styles:',
    STYLES.filter((s) => styleCounts[s])
      .map((s) => `${s} ${styleCounts[s]}`)
      .join(', ')
  );
  console.log('    difficulty:', DIFFS.map((d) => `${d} ${diffCounts[d] ?? 0}`).join(', '));
  console.log('    facets:', FACETS.map((f) => `${f} ${facetCounts[f] ?? 0}`).join(', '));

  if (cfg.requireEveryStyle)
    for (const s of STYLES)
      check(
        (styleCounts[s] ?? 0) > 0,
        `${cfg.code}: no question anywhere uses style "${s}", which the real test does use`
      );
  for (const d of DIFFS)
    check(
      (diffCounts[d] ?? 0) > 0,
      `${cfg.code}: no "${d}" question, so the difficulty mix cannot be honoured`
    );
  for (const f of FACETS)
    check((facetCounts[f] ?? 0) > 0, `${cfg.code}: no question carries the "${f}" facet`);

  if (cfg.requireStyles)
    for (const s of cfg.requireStyles)
      check(
        (styleCounts[s] ?? 0) > 0,
        `${cfg.code}: no question anywhere uses style "${s}", which the real test does use`
      );

  // ---- coverage ----
  const cites = new Map();
  for (const q of all)
    for (const s of q.slides ?? []) cites.set(s, (cites.get(s) ?? 0) + 1);

  for (const cov of cfg.coverages) {
    const missing = cov.required.filter((r) => !cites.has(r));
    if (missing.length) {
      console.log(
        `    x coverage: ${missing.length} of ${cov.required.length} ${cov.noun} are never tested`
      );
      console.log('        ' + missing.join(', '));
      problems.push(
        `${cfg.code}: ${missing.length} ${cov.noun} are not covered by any question`
      );
    } else {
      console.log(`    . coverage: all ${cov.required.length} ${cov.noun} are tested`);
    }

    if (cov.kind === 'exactly-once') {
      const dupes = cov.required.filter((r) => (cites.get(r) ?? 0) > 1);
      check(
        dupes.length === 0,
        `${cfg.code}: ${dupes.join(', ')} appear more than once, so a paper would repeat a question`
      );
      // Strays are judged only among refs of this coverage's own shape, so a
      // course whose bank also cites its textbook is not accused of inventing
      // exam questions.
      const strays = [...cites.keys()].filter(
        (k) => (cov.pattern ? cov.pattern.test(k) : true) && !cov.required.includes(k)
      );
      check(
        strays.length === 0,
        `${cfg.code}: provenance refs that do not name a real ${cov.noun}: ${strays.join(', ')}`
      );
      if (!dupes.length && !strays.length)
        console.log('    . coverage: each one cited exactly once, no duplicates, no strays');
    }
  }

  // ---- the key ----
  //
  // The second transcription lives in this file. Two people reading the same
  // screenshot and disagreeing must stop the build, because the one thing a
  // drill may never do is teach the wrong answer.
  if (cfg.key) {
    let checked = 0;
    let wrong = 0;
    for (const q of all) {
      for (const ref of q.slides ?? []) {
        const m = ref.match(/^(Test [12]) Q(\d+)$/);
        if (!m) continue;
        const table = cfg.key[m[1]];
        const n = Number(m[2]);
        const expected = Array.isArray(table) ? table[n - 1] : table?.[n];
        if (expected === undefined) continue;
        checked += 1;
        // A single-choice or true/false question is keyed by its answer; a
        // fill-in-the-gap is keyed by the word the examiner wrote in the box.
        const got =
          q.style === 'gap' || q.style === 'cloze' ? q.blanks?.[0]?.accept?.[0] : q.answer;
        const agrees =
          q.style === 'gap' || q.style === 'cloze'
            ? normaliseAnswer(got ?? '') === normaliseAnswer(expected)
            : got === expected;
        if (!agrees) {
          wrong += 1;
          problems.push(
            `${cfg.code} [${q.id}] ${ref}: bank says "${got}" but the transcribed key says "${expected}"`
          );
        }
      }
    }
    console.log(
      `    ${wrong ? 'x' : '.'} answer key: ${checked} answers cross-checked against the original transcription${
        wrong ? `, ${wrong} disagree` : ', all agree'
      }`
    );
  }

  const ledger = cfg.ledger ? checkLedger(cfg, dir, all) : null;

  if (cfg.lessons)
    checkLessons(cfg, dir, new Set(Object.keys(perModule).map(Number)), ledger, all);

  if (cfg.requireWhy) {
    // Only the styles that present options can carry per-option verdicts; a
    // typed blank has nothing to tick or cross.
    const withOptions = all.filter((q) => ['mcq', 'multi', 'tf'].includes(q.style));
    const explained = withOptions.filter((q) => {
      const ids = q.style === 'tf' ? ['true', 'false'] : (q.options ?? []).map((o) => o.id);
      return q.why && ids.length > 0 && ids.every((id) => q.why[id]);
    }).length;
    console.log(
      `    ${explained === withOptions.length ? '.' : 'x'} verdicts: ${explained} of ${withOptions.length} option-bearing questions explain every option`
    );
  }
}

console.log(`\n  total across all courses: ${grandTotal} questions`);

if (problems.length) {
  console.error(`\nBANK GATE FAILED: ${problems.length} problem(s)`);
  for (const p of problems.slice(0, 60)) console.error('  x ' + p);
  if (problems.length > 60) console.error(`  ... and ${problems.length - 60} more`);
  process.exit(1);
}
console.log('\nBANK GATE: pass');
