import type { Course, FacetGuide, Paper, Question } from '@/lib/types';

import m1 from './tmc221/module1.json';
import m2 from './tmc221/module2.json';
import m3 from './tmc221/module3.json';
import m4 from './tmc221/module4.json';
import m5 from './tmc221/module5.json';
import realTest from './tmc221/real-test.json';

import i1 from './ift222/module1.json';
import i2 from './ift222/module2.json';
import i3 from './ift222/module3.json';
import i4 from './ift222/module4.json';
import i5 from './ift222/module5.json';
import i6 from './ift222/module6.json';
import i7 from './ift222/module7.json';
import i8 from './ift222/module8.json';
import i9 from './ift222/module9.json';
import i10 from './ift222/module10.json';

// Adding a course later: create data/<code>/*.json in the same shape, import it
// here, and push one more entry into COURSES. Nothing else in the app changes.

const tmcFacets: FacetGuide[] = [
  {
    id: 'numbers',
    label: 'Numbers, percentages, dates',
    help: '71% vs 32%, 0.76, 85%, +51%, 95%, 76%, blow 50, 37x, 2:30 a.m., 65 years',
  },
  {
    id: 'names',
    label: 'Names, authors, book titles',
    help: 'Duckworth, Dweck, Clear, Leaf, Peale, de Bono, Young, Moran, Gollwitzer, Ries and Trout',
  },
  {
    id: 'lists',
    label: 'Lists, steps and their order',
    help: 'The 7 Kits, SWITCH, the 7-Step Plan, W.I.S.E., WOOP, the Six Hats, the three Pillars',
  },
  {
    id: 'wording',
    label: 'Exact definitions and wording',
    help: 'The precise slide phrasing: Key Result vs activity, replaced not managed, launch pad not limitation',
  },
];

const tmc221: Course = {
  code: 'TMC221',
  title: 'Personal Development and Capacity Building',
  tagline:
    'Active recall drilled straight from the study manual. Every answer carries the slide it came from.',
  blurb:
    'Five lectures on goals, positive thinking, personal branding, systems and discouragement. Drilled in the five styles the computer-based test actually uses, plus the real 30-question test.',
  moduleNoun: 'Module',
  facetGuide: tmcFacets,
  modules: [
    {
      number: 1,
      title: 'Goal Setting and Personal Accomplishment',
      lecture: 1,
      blurb:
        'Four levels, three goal types, four frameworks, the psychology of failure, six strategies, Total Man, the 4-Layer Goal Stack.',
    },
    {
      number: 2,
      title: 'Positive Thinking and Creative Problem-Solving',
      lecture: 2,
      blurb:
        'The W.I.S.E. Model from five authors: Oyedepo, Leaf and the SWITCH protocol, Peale, de Bono, Young.',
    },
    {
      number: 3,
      title: 'Personal Branding and Strategic Positioning',
      lecture: 3,
      blurb:
        'Clean the inside first, the self-audit, brand pillars, packaging, positioning and mindshare, niche, the Brand Bank Account.',
    },
    {
      number: 4,
      title: 'Systems for Sustainable Success',
      lecture: 4,
      blurb:
        'The seven interlocking Kits, all beginning with T: Task, Training, Target, Tools, Timing, Tillage, Tarrying.',
    },
    {
      number: 5,
      title: 'Overcoming Discouragement and Sustaining Personal Success',
      lecture: 5,
      blurb:
        'Grit and the 50th blow, vision against dream, the Three Pillars, the Precision Test, the 1% Rule, four strategies, the 7-Step Plan.',
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

const iftFacets: FacetGuide[] = [
  {
    id: 'numbers',
    label: 'Conversions and calculations',
    help: "7D3A to decimal, 2A7F to binary, the two's complement of 00101100, effective addresses, CPI and execution time, bit widths and biases",
  },
  {
    id: 'names',
    label: 'Named schemes and components',
    help: 'BCD, Excess-3, Unicode, IEEE 754, SRAM and DRAM, MAR, the address bus, SIMD, RISC and CISC, Harvard, temporal and spatial locality',
  },
  {
    id: 'lists',
    label: 'Orderings, hierarchies and layouts',
    help: 'The memory hierarchy fastest to slowest, floating-point field order, instruction field widths, address counts per format',
  },
  {
    id: 'wording',
    label: 'Exact definitions and distinctions',
    help: 'Architecture against organization, ISA against microarchitecture, access time against cycle time, overflow, what the ISA does not define',
  },
];

const iftQuestions: Question[] = [
  ...(i1 as unknown as Question[]),
  ...(i2 as unknown as Question[]),
  ...(i3 as unknown as Question[]),
  ...(i4 as unknown as Question[]),
  ...(i5 as unknown as Question[]),
  ...(i6 as unknown as Question[]),
  ...(i7 as unknown as Question[]),
  ...(i8 as unknown as Question[]),
  ...(i9 as unknown as Question[]),
  ...(i10 as unknown as Question[]),
];

/**
 * The two objective tests, rebuilt from the bank rather than stored twice.
 *
 * Every IFT222 question carries its provenance in `slides`, as "Test 1 Q16".
 * Filtering on that tag and sorting by the question number reproduces the paper
 * in its original order, so there is exactly one copy of each question in the
 * repository. A correction can never reach the drill but miss the paper.
 */
function objectiveTest(tag: string, id: string, title: string, note: string): Paper {
  const num = (q: Question) =>
    Number(q.slides.find((s) => s.startsWith(tag))?.match(/Q(\d+)$/)?.[1] ?? 0);
  const questions = iftQuestions
    .filter((q) => q.slides.some((s) => s.startsWith(`${tag} Q`)))
    .sort((a, b) => num(a) - num(b));
  return {
    id,
    title,
    subtitle:
      'The objective test as it was actually set: same 60 questions, same order, one mark each.',
    note,
    questions,
    minutes: 60,
  };
}

const ift222: Course = {
  code: 'IFT222',
  title: 'Computer Architecture and Organisation',
  tagline:
    'All 120 objective questions from both computer-based tests, answered and pulled apart. Every option is explained, not only the right one.',
  blurb:
    'Architecture against organization, number systems and codes, signed numbers, IEEE floating point, instruction formats, addressing modes, the memory hierarchy, performance and RISC against CISC. Drill by topic, or sit either real test end to end.',
  moduleNoun: 'Topic',
  facetGuide: iftFacets,
  modules: [
    {
      number: 1,
      title: 'Architecture versus Organization',
      blurb:
        'The blueprint against the construction: what each term covers, what changed in a scenario, abstraction, domain-specific design, backward compatibility.',
    },
    {
      number: 2,
      title: 'ISA and Microarchitecture',
      blurb:
        'The programmer-visible interface, what the ISA does not define, instruction categories, LOAD and branch, SIMD, binary compatibility.',
    },
    {
      number: 3,
      title: 'Number Systems and Codes',
      blurb:
        'Hex to decimal and back, bits to hex digits, BCD, Excess-3 and self-complementing codes, Unicode, vector against bitmap.',
    },
    {
      number: 4,
      title: 'Signed Numbers and Complements',
      blurb:
        "Unsigned ranges, sign-magnitude, one's and two's complement, the two zeros, end-around carry, overflow, and why two's complement won.",
    },
    {
      number: 5,
      title: 'Floating Point and IEEE 754',
      blurb:
        'Single against double: 32 and 64 bits, 8 and 11 exponent bits, biases 127 and 1023, the two ranges, field order and precision.',
    },
    {
      number: 6,
      title: 'Instruction Types and Formats',
      blurb:
        'Opcode and operand fields, instruction length, the opcode-space trade-off, fixed against variable length, zero to three address formats.',
    },
    {
      number: 7,
      title: 'Addressing Modes',
      blurb:
        'Immediate, direct, indirect, register, register indirect, indexed, base register and PC-relative, with the effective-address arithmetic each one needs.',
    },
    {
      number: 8,
      title: 'Memory, Buses and CPU Components',
      blurb:
        'The hierarchy and its trade-off, SRAM against DRAM, ROM and flash, cache and the memory wall, locality, virtual memory, MAR, the three buses, the control unit.',
    },
    {
      number: 9,
      title: 'Performance, Pipelining, RISC and CISC',
      blurb:
        'The CPU time equation with CPI, why clock frequency is not enough, branch prediction and control hazards, the RISC and CISC philosophies.',
    },
    {
      number: 10,
      title: 'Von Neumann, Harvard and Image Data',
      blurb:
        'One shared memory against two separate ones, the bottleneck and the simultaneous access it prevents, bits per pixel, bitmap against vector.',
    },
  ],
  questions: iftQuestions,
  papers: [
    objectiveTest(
      'Test 1',
      'ift-objective-1',
      'Objective Test 1, all 60 questions',
      'Transcribed from the captured test and its verified answer key, with every calculation recomputed. Question 19 is keyed as the examiner keyed it, Sign, Mantissa, Exponent, though the true IEEE 754 field order is Sign, Exponent, Mantissa. The review says so on that question.'
    ),
    objectiveTest(
      'Test 2',
      'ift-objective-2',
      'Objective Test 2, all 60 questions',
      'Transcribed from the captured test and its verified answer key, with every calculation recomputed. This paper leans conceptual: memory hierarchy, ISA against microarchitecture, addressing modes and performance, with only a handful of calculations.'
    ),
  ],
};

export const COURSES: Course[] = [tmc221, ift222];

export function findCourse(code: string): Course | undefined {
  return COURSES.find((c) => c.code.toLowerCase() === code.toLowerCase());
}

export function courseByCode(code: string): Course {
  const found = findCourse(code);
  if (!found) throw new Error(`unknown course: ${code}`);
  return found;
}
