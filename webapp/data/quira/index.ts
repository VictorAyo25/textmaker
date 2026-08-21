// The side quest: "Towards Mental Exploits" by David Oyedepo, drilled in the
// grammar the Quira app's generator actually uses.
//
// This bank is deliberately NOT registered in data/courses.ts. It is not a CU
// course, it is not on the timetable, and it should not sit on the drill's
// landing page beside Omega semester papers. It lives behind /quira, which is
// skinned to look and feel like the app the challenge is sat on.
//
// The forcing function is data/quira/ledger/*.json: 803 atomic facts covering
// all 79 pages of the book. scripts/validate-quira.mjs fails the build if any
// fact goes untested, because a fact nothing asks about is a question we could
// be asked and could not answer.

import type { Question } from '@/lib/types';

import t01 from './topic01.json';
import t02 from './topic02.json';
import t03 from './topic03.json';
import t04 from './topic04.json';
import t05 from './topic05.json';
import t06 from './topic06.json';
import t07 from './topic07.json';
import t08 from './topic08.json';
import t09 from './topic09.json';
import t10 from './topic10.json';
import t11 from './topic11.json';
import t12 from './topic12.json';
import t13 from './topic13.json';
import t14 from './topic14.json';
import gap from './gapfill.json';

export interface QuiraTopic {
  number: number;
  title: string;
  /** Where in the book, so a wrong answer can be chased to the page. */
  pages: string;
  blurb: string;
}

/**
 * The fourteen passages, in book order.
 *
 * The split follows the book's own sections rather than its chapters, because
 * the generator chunks by passage: quiz 1 took thirty questions out of roughly
 * eleven pages, and quiz 2 took ten questions out of a two-page stretch on
 * understanding and meditation. Chapter 2 alone is four passages.
 */
export const QUIRA_TOPICS: QuiraTopic[] = [
  { number: 1, title: 'Understanding the Mind', pages: 'Introduction and Chapter 1, pages 3 to 8', blurb: 'As he thinketh in his heart. The mind defined, the mad man who has lost his worth, belief as mental assent, the carnal and the spiritual mind, and the mind of Christ.' },
  { number: 2, title: 'Learning and Knowledge', pages: 'Chapter 2, pages 9 to 12', blurb: 'The building that decays through disuse, T. L. Osborn and Abraham Lincoln on learning, Anthony Robbins and his 700 books, Oswald J. Smith at 93, and every divine deposit multiplying with use.' },
  { number: 3, title: 'Understanding and Meditation', pages: 'Chapter 2, pages 12 to 14', blurb: 'Philip and the Ethiopian eunuch, processing knowledge with commitment, two are better than one, David in Psalm 119, and the study that says only 5 per cent think.' },
  { number: 4, title: 'Reasoning', pages: 'Chapter 2, pages 14 to 17', blurb: 'Come now and let us reason together, the prodigal son who neither prayed nor fasted, the tower builder who counts the cost, and if you can think enough what you have is enough.' },
  { number: 5, title: 'Imagination', pages: 'Chapter 2, pages 17 to 20', blurb: 'Imagination as pace-setter for your destination, Abram lifting up his eyes, casting down imaginations, and Zig Ziglar on the most powerful nation.' },
  { number: 6, title: 'The Reality of Supernatural Mentality', pages: 'Chapter 3, pages 21 to 25', blurb: 'Belshazzar and the handwriting on the wall, the queen who knew about Daniel, empowerment defined, the three realms, and Peter starting a church in thirty minutes.' },
  { number: 7, title: 'Your Mind is the Seat of Wisdom', pages: 'Chapter 4, pages 26 to 34', blurb: 'Wisdom as the correct application of knowledge, the four kinds of wisdom in James, Solomon wiser than Ethan and Heman, and the four requirements for divine wisdom.' },
  { number: 8, title: 'Products of Divine Wisdom', pages: 'Chapter 5, pages 35 to 40', blurb: 'Creativity first, then exploits, authority, joy, wealth, pleasantness and peace, dominion and answers. Wealth as a product of wits, and death by debt-pressure.' },
  { number: 9, title: 'Wisdom Can Be Lost', pages: 'Chapter 5, pages 41 to 45', blurb: 'Solomon from wisest to most foolish, seven hundred wives and three hundred concubines, Hadad and Rezon, Ahitophel hanging himself, and keeping the treasure.' },
  { number: 10, title: 'The Place of Inspiration', pages: 'Chapter 6, pages 46 to 50', blurb: 'Inspiration as the Spirit of God in motion in the mental faculty, the 99 per cent that equals zero without the 1, Elisha and the minstrel, and the enemies of inspiration.' },
  { number: 11, title: 'Creating the Right Atmosphere', pages: 'Chapter 7, pages 51 to 54', blurb: 'Quietness, separation and keeping wise company. Elijah at the cave, the seashore at Accra, Isaac sowing practical seeds, and Bill Gates thinking in a corner.' },
  { number: 12, title: 'Exercising the Mind', pages: 'Chapter 8, pages 55 to 64', blurb: 'Newton and the apple, research as fact-finding study, meditation as the missing asset, the ministry of consultants, and insight-expectant prayer.' },
  { number: 13, title: 'Obstacles to Mental Excellence', pages: 'Chapter 9, pages 65 to 73', blurb: 'Sin, accepting the status quo, the trap of past failures, the pride of past achievements, comparison, and the fear of curses and enchantments.' },
  { number: 14, title: 'Mental Revolution, and Now You Know', pages: 'Chapters 10 and 11, pages 74 to 79', blurb: 'The Holy Spirit as the gateway to divine intelligence, the Benin building that lost relevance, and one striking insight worth more than a lifetime of struggles.' },
];

const ALL = [t01, t02, t03, t04, t05, t06, t07, t08, t09, t10, t11, t12, t13, t14, gap].flatMap(
  (f) => f as unknown as Question[]
);

/** The whole bank, in book order, then by id so the order is stable. */
export const QUIRA_BANK: Question[] = [...ALL].sort(
  (a, b) => a.module - b.module || a.id.localeCompare(b.id)
);

/**
 * What the runner can actually show as a Quira question.
 *
 * The challenge is single-select multiple choice with four unlettered options.
 * `match` cannot be drawn that way, so it is held back from the timed paper and
 * kept for the study screens. Single-blank `gap` questions ARE convertible: the
 * blank already carries four choices, so they become an ordinary four-option
 * question with the sentence as the stem.
 */
export function asChoiceQuestion(q: Question): {
  id: string;
  module: number;
  prompt: string;
  options: { id: string; text: string }[];
  answer: string;
  explanation: string;
  why?: Record<string, string>;
  slides: string[];
  topic: string;
  difficulty: string;
} | null {
  if (q.style === 'mcq' || q.style === 'tf') {
    if (!q.options?.length || typeof q.answer !== 'string') return null;
    return {
      id: q.id,
      module: q.module,
      prompt: q.prompt,
      options: q.options,
      answer: q.answer,
      explanation: q.explanation,
      why: q.why,
      slides: q.slides,
      topic: q.topic,
      difficulty: q.difficulty,
    };
  }
  if (q.style === 'gap' && q.blanks?.length === 1) {
    const blank = q.blanks[0];
    const canonical = blank.accept[0];
    const options = blank.choices.map((text, i) => ({ id: String.fromCharCode(97 + i), text }));
    const answer = options.find((o) => o.text.toLowerCase() === canonical.toLowerCase())?.id;
    if (!answer) return null;
    return {
      id: q.id,
      module: q.module,
      // The blank marker is replaced by a rule of underscores, which is how the
      // app renders a gap when its generator produces one.
      prompt: q.prompt.replace(/\{\{1\}\}/g, '______'),
      options,
      answer,
      explanation: q.explanation,
      why: q.why,
      slides: q.slides,
      topic: q.topic,
      difficulty: q.difficulty,
    };
  }
  return null;
}

export type QuiraQuestion = NonNullable<ReturnType<typeof asChoiceQuestion>>;

export const QUIRA_QUESTIONS: QuiraQuestion[] = QUIRA_BANK.map(asChoiceQuestion).filter(
  (q): q is QuiraQuestion => q !== null
);
