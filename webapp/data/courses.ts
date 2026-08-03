import type { Course, Paper, Question } from '@/lib/types';

import m1 from './tmc221/module1.json';
import m2 from './tmc221/module2.json';
import m3 from './tmc221/module3.json';
import m4 from './tmc221/module4.json';
import m5 from './tmc221/module5.json';
import realTest from './tmc221/real-test.json';

// Adding a course later: create data/<code>/*.json in the same shape, import it
// here, and push one more entry into COURSES. Nothing else in the app changes.

const tmc221: Course = {
  code: 'TMC221',
  title: 'Personal Development and Capacity Building',
  modules: [
    {
      number: 1,
      title: 'Goal Setting and Personal Accomplishment',
      lecture: 1,
      blurb: 'Four levels, three goal types, four frameworks, the psychology of failure, six strategies, Total Man, the 4-Layer Goal Stack.',
    },
    {
      number: 2,
      title: 'Positive Thinking and Creative Problem-Solving',
      lecture: 2,
      blurb: 'The W.I.S.E. Model from five authors: Oyedepo, Leaf and the SWITCH protocol, Peale, de Bono, Young.',
    },
    {
      number: 3,
      title: 'Personal Branding and Strategic Positioning',
      lecture: 3,
      blurb: 'Clean the inside first, the self-audit, brand pillars, packaging, positioning and mindshare, niche, the Brand Bank Account.',
    },
    {
      number: 4,
      title: 'Systems for Sustainable Success',
      lecture: 4,
      blurb: 'The seven interlocking Kits, all beginning with T: Task, Training, Target, Tools, Timing, Tillage, Tarrying.',
    },
    {
      number: 5,
      title: 'Overcoming Discouragement and Sustaining Personal Success',
      lecture: 5,
      blurb: 'Grit and the 50th blow, vision against dream, the Three Pillars, the Precision Test, the 1% Rule, four strategies, the 7-Step Plan.',
    },
  ],
  questions: [
    ...(m1 as unknown as Question[]),
    ...(m2 as unknown as Question[]),
    ...(m3 as unknown as Question[]),
    ...(m4 as unknown as Question[]),
    ...(m5 as unknown as Question[]),
  ],
  papers: [realTest as unknown as Paper],
};

export const COURSES: Course[] = [tmc221];

export function courseByCode(code: string): Course {
  const found = COURSES.find((c) => c.code === code);
  if (!found) throw new Error(`unknown course: ${code}`);
  return found;
}
