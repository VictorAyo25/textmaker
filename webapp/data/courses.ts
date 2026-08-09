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
import d01 from './ift222/deck01.json';
import d02 from './ift222/deck02.json';
import d03 from './ift222/deck03.json';
import d04 from './ift222/deck04.json';
import d05 from './ift222/deck05.json';
import d06 from './ift222/deck06.json';
import d07 from './ift222/deck07.json';
import d08A from './ift222/deck08a.json';
import d08B from './ift222/deck08b.json';
import d08C from './ift222/deck08c.json';
import d09A from './ift222/deck09a.json';
import d09B from './ift222/deck09b.json';
import d10 from './ift222/deck10.json';
import d11A from './ift222/deck11a.json';
import d11B from './ift222/deck11b.json';
import d12A from './ift222/deck12a.json';
import d12B from './ift222/deck12b.json';
import d12C from './ift222/deck12c.json';

import p1 from './phy121/module1.json';
import p2 from './phy121/module2.json';
import p3 from './phy121/module3.json';
import p4 from './phy121/module4.json';
import p5 from './phy121/module5.json';
import p6 from './phy121/module6.json';
import p7 from './phy121/module7.json';
import p8 from './phy121/module8.json';
import p9 from './phy121/module9.json';
import p10 from './phy121/module10.json';
import pd1 from './phy121/deck1.json';
import pd2 from './phy121/deck2.json';
import pd3 from './phy121/deck3.json';
import pd4 from './phy121/deck4.json';
import pd5 from './phy121/deck5.json';
import pd6 from './phy121/deck6.json';
import pd7 from './phy121/deck7.json';
import pd8 from './phy121/deck8.json';
import pd9 from './phy121/deck9.json';
import ps01 from './phy121/slides01.json';
import ps04 from './phy121/slides04.json';
import ps05 from './phy121/slides05.json';
import ps06 from './phy121/slides06.json';
import ps07 from './phy121/slides07.json';
import ps08 from './phy121/slides08.json';
import ps09 from './phy121/slides09.json';
import ps11 from './phy121/slides11.json';

import e1 from './ent221/module1.json';
import e2 from './ent221/module2.json';
import e3 from './ent221/module3.json';
import e4 from './ent221/module4.json';
import e5 from './ent221/module5.json';
import e6 from './ent221/module6.json';
import e7 from './ent221/module7.json';
import e8 from './ent221/module8.json';
import e9 from './ent221/module9.json';
import e10 from './ent221/module10.json';
import e11 from './ent221/module11.json';
import e12 from './ent221/module12.json';

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
  // Exam sat. Filed under "Exams already taken" on the landing page; the drill
  // itself stays open, because it is still the fastest revision there is.
  taken: true,
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
  ...(d01 as unknown as Question[]),
  ...(d02 as unknown as Question[]),
  ...(d03 as unknown as Question[]),
  ...(d04 as unknown as Question[]),
  ...(d05 as unknown as Question[]),
  ...(d06 as unknown as Question[]),
  ...(d07 as unknown as Question[]),
  ...(d08A as unknown as Question[]),
  ...(d08B as unknown as Question[]),
  ...(d08C as unknown as Question[]),
  ...(d09A as unknown as Question[]),
  ...(d09B as unknown as Question[]),
  ...(d10 as unknown as Question[]),
  ...(d11A as unknown as Question[]),
  ...(d11B as unknown as Question[]),
  ...(d12A as unknown as Question[]),
  ...(d12B as unknown as Question[]),
  ...(d12C as unknown as Question[]),
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
    'All eight lecture decks turned into questions, plus all 120 from both computer-based tests. Every option is explained, not only the right one.',
  blurb:
    'Architecture against organization, number systems and codes, signed numbers, IEEE floating point, instruction formats, addressing modes, the memory hierarchy, cache mapping, pipelining and hazards, and RISC against CISC. Drill by topic, sit either real test end to end, or take the crash course first.',
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
      title: 'Performance, RISC and CISC',
      blurb:
        'The CPU time equation with CPI, why clock frequency is not enough, the two design philosophies from 100 to 250 instructions down to one clock each, and the comparison tables line by line.',
    },
    {
      number: 10,
      title: 'Von Neumann, Harvard and Image Data',
      blurb:
        'One shared memory against two separate ones, the bottleneck and the simultaneous access it prevents, bits per pixel, bitmap against vector.',
    },
    {
      number: 11,
      title: 'Cache Mapping Functions',
      blurb:
        'Direct, fully associative and set associative, worked end to end: address bits, offset, index, tag and tag directory size, with the same machine mapped three ways so the answers can be compared.',
    },
    {
      number: 12,
      title: 'Pipelining and Hazards',
      blurb:
        'The five stages, throughput against latency, speedup and efficiency formulas with every worked example, and the three hazards with forwarding, stalling and scheduling as their remedies.',
    },
  ],
  questions: iftQuestions,
  // The two objective tests are tagged so the "past questions only" filter can
  // rebuild them; the rest of the bank comes from the eight lecture decks.
  examTags: ['Test 1 Q', 'Test 2 Q'],
  hasLedger: true,
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

const entFacets: FacetGuide[] = [
  {
    id: 'numbers',
    label: 'Figures, ranges and thresholds',
    help: 'pH 6.5 to 8.5, dissolved oxygen 5 to 8 mg/L, feed at 60 to 70% of cost, 20 to 30% water changes, 25 to 34C, 2000 to 2500 mm, 143 palms per hectare, NPKMg 12:12:17:2, 40C for 70 to 80 days, 140 to 150C for 60 to 90 minutes',
  },
  {
    id: 'names',
    label: 'Named species, organisms and models',
    help: 'Elaeis guineensis, Dura and Pisifera and Tenera, Nigrescens and Virescens and Albescens, Aeromonas and Pseudomonas, Nitrosomonas and Nitrobacter, Ganoderma, POME and PKC and EFB, SWOT and SMART, NAFDAC',
  },
  {
    id: 'lists',
    label: 'Enumerated lists and their order',
    help: 'The 3M, the ten MAKE principles, the 7Ps and 4Cs, the five fish farm departments, the five processing stages, the six types of value addition, the three forms, POCD, the eleven aspects of agriculture',
  },
  {
    id: 'wording',
    label: 'Exact definitions and the absolutes',
    help: 'The precise phrasing of agriculture, value chain, water quality, value addition and pisciculture, and the every, all, only and entirely that mark a wrong option',
  },
];

const entQuestions: Question[] = [
  ...(e1 as unknown as Question[]),
  ...(e2 as unknown as Question[]),
  ...(e3 as unknown as Question[]),
  ...(e4 as unknown as Question[]),
  ...(e5 as unknown as Question[]),
  ...(e6 as unknown as Question[]),
  ...(e7 as unknown as Question[]),
  ...(e8 as unknown as Question[]),
  ...(e9 as unknown as Question[]),
  ...(e10 as unknown as Question[]),
  ...(e11 as unknown as Question[]),
  ...(e12 as unknown as Question[]),
];

/**
 * The two computer-based tests, rebuilt from the bank rather than stored twice.
 *
 * Same idea as IFT222: filter on the provenance tag, sort by the examiner's own
 * question number, and the paper reassembles itself. Test 1 skips question 4
 * because the examiner omitted it, so that paper is 29 questions and its
 * numbering has a hole in it exactly where the original did.
 */
function entPaper(tag: string, id: string, title: string, note: string, mins: number): Paper {
  const num = (q: Question) =>
    Number(q.slides.find((s) => s.startsWith(`${tag} Q`))?.match(/Q(\d+)$/)?.[1] ?? 0);
  const questions = entQuestions
    .filter((q) => q.slides.some((s) => s.startsWith(`${tag} Q`)))
    .sort((a, b) => num(a) - num(b));
  return { id, title, subtitle: 'The test as it was actually set, in its own order, one mark each.', note, questions, minutes: mins };
}

const ent221: Course = {
  code: 'ENT221',
  title: 'Agripreneurship',
  tagline:
    'Every fact in the course text and all three lecture decks, drilled until none of it is new. Each answer says why it is right and why the others are not.',
  blurb:
    'Agriculture and agripreneurship, the value chain, fish farming from water quality to the 3M model, oil palm cultivation and processing, agribusiness opportunities, value addition and operations management. Drill any topic, or sit either computer-based test end to end.',
  moduleNoun: 'Topic',
  facetGuide: entFacets,
  examTags: ['Test 1 Q', 'Test 2 Q'],
  // Every ENT221 question names the ledger facts it tests, which is what lets
  // the mastery map work fact by fact rather than topic by topic.
  hasLedger: true,
  modules: [
    {
      number: 1,
      title: 'Module One: agriculture, its aspects and its importance',
      blurb:
        'The definition word for word, the eleven key aspects with their glosses, why agriculture matters, and how livestock, crops and soil feed one another.',
    },
    {
      number: 2,
      title: 'Module One: agripreneurship and the agricultural value chain',
      blurb:
        'Entrepreneurship in agriculture, the seven components, the twelve value chain segments, the Nigerian examples, and the agripreneur against the traditional farmer.',
    },
    {
      number: 3,
      title: 'Module Two: fish farming, its departments and its investment potential',
      blurb:
        'Aquaculture and pisciculture, the five departments including the labour room and the kitchen, the fourteen investment opportunities, and the five indices.',
    },
    {
      number: 4,
      title: 'Module Two: water quality, physical, chemical and biological',
      blurb:
        'The three parameter families with every threshold, iron from silvery film to safe limit, the beneficial and harmful organisms, and the thumb rule.',
    },
    {
      number: 5,
      title: 'Module Two: aquarium management and fish behaviour',
      blurb:
        'The four setup steps, the daily, weekly, monthly and long-term schedule, and the four behaviour categories with their patterns, causes and remedies.',
    },
    {
      number: 6,
      title: 'Module Two: the 3M model, Make, Manage and Multiply',
      blurb:
        'The ten MAKE principles, the five MANAGE elements, the six MULTIPLY tasks, the 7Ps and 4Cs, and SWOT and SMART.',
    },
    {
      number: 7,
      title: 'Module Two: marketing fresh and processed fish',
      blurb:
        'The five marketing steps, the four target markets, the brand trio, the online and offline channels, and the five value addition offerings.',
    },
    {
      number: 8,
      title: 'Module Three: oil palm cultivation',
      blurb:
        'Elaeis guineensis, the environmental figures, the five stages, the Dura by Pisifera cross, spacing and density, the pests, the fruit types and the three varieties.',
    },
    {
      number: 9,
      title: 'Module Three: oil palm processing and its by-products',
      blurb:
        'Sterilisation through clarification, the palm kernel line, the four quality factors, and EFB, PKC and POME with what each becomes.',
    },
    {
      number: 10,
      title: 'Module Four: agribusiness opportunities and the value chain',
      blurb:
        'The six evaluation criteria, the nine chain components, the eight common problems, the five market needs and the four technology trends.',
    },
    {
      number: 11,
      title: 'Module Four: value addition and agribusiness innovation',
      blurb:
        'The six types and three forms of value addition, the process flow, the four drivers and four types of innovation, and the strategies and challenges.',
    },
    {
      number: 12,
      title: 'Module Four: production and operations management',
      blurb:
        'Production against operations, the six components, the POCD scope, the advantages and limitations, and the technologies that run modern agribusiness.',
    },
  ],
  questions: entQuestions,
  papers: [
    entPaper(
      'Test 1',
      'ent-cbt-1',
      'Computer-Based Test 1, all 29 questions',
      'The paper was numbered 1 to 30 but question 4 was omitted by the examiner, so it is 29 questions. This copy was captured unattempted, so it carries no printed key: every answer here is derived from the course text and matches the shipped ENT221 manual. Question 8 asks for a figure that appears nowhere in the course text, and its review says so.',
      30
    ),
    entPaper(
      'Test 2',
      'ent-cbt-2',
      'Computer-Based Test 2, all 30 questions',
      'Captured as a graded review page marked 30 out of 30, so every answer on this paper is confirmed by the examiner rather than inferred. Question 19 uses the phrase total plate count, which the course text calls Total Bacterial Count; the review notes the difference.',
      30
    ),
  ],
  // Exam sat. Filed under "Exams already taken" on the landing page; the drill
  // itself stays open, because it is still the fastest revision there is.
  taken: true,
};

const phyFacets: FacetGuide[] = [
  {
    id: 'numbers',
    label: 'Calculations and powers of ten',
    help: 'kQ/r and kQ/r squared, 1/2 CV squared and 1/2 LI squared, mv over qB, mu-nought I over 2 pi r, the turns ratio, and the exponent that decides between 10 to the minus 4 and 10 to the minus 6',
  },
  {
    id: 'names',
    label: 'Laws, constants and named quantities',
    help: "Coulomb, Gauss, Ampere, Faraday, Biot-Savart, Lorentz, epsilon-nought, mu-nought, the electronic charge, permittivity, flux, emf, magnetic moment",
  },
  {
    id: 'lists',
    label: 'Procedures and their order',
    help: 'Series before parallel in a capacitor network, current before emf when only the terminal p.d. is given, turns per metre before the solenoid field, and the check that runs at the end of each',
  },
  {
    id: 'wording',
    label: 'Definitions and the exact quantity asked for',
    help: 'Which charge PRODUCES the field and which merely sits in it, terminal p.d. against emf, flux against field, total turns against turns per metre, and distance measured from the centre rather than the surface',
  },
];

const phyQuestions: Question[] = [
  ...(p1 as unknown as Question[]),
  ...(p2 as unknown as Question[]),
  ...(p3 as unknown as Question[]),
  ...(p4 as unknown as Question[]),
  ...(p5 as unknown as Question[]),
  ...(p6 as unknown as Question[]),
  ...(p7 as unknown as Question[]),
  ...(p8 as unknown as Question[]),
  ...(p9 as unknown as Question[]),
  ...(p10 as unknown as Question[]),
  ...(pd1 as unknown as Question[]),
  ...(pd2 as unknown as Question[]),
  ...(pd3 as unknown as Question[]),
  ...(pd4 as unknown as Question[]),
  ...(pd5 as unknown as Question[]),
  ...(pd6 as unknown as Question[]),
  ...(pd7 as unknown as Question[]),
  ...(pd8 as unknown as Question[]),
  ...(pd9 as unknown as Question[]),
  ...(ps01 as unknown as Question[]),
  ...(ps04 as unknown as Question[]),
  ...(ps05 as unknown as Question[]),
  ...(ps06 as unknown as Question[]),
  ...(ps07 as unknown as Question[]),
  ...(ps08 as unknown as Question[]),
  ...(ps09 as unknown as Question[]),
  ...(ps11 as unknown as Question[]),
];

/** Both computer-based tests, rebuilt from the bank by provenance tag. */
function phyPaper(tag: string, id: string, title: string, note: string, mins: number): Paper {
  const num = (q: Question) =>
    Number(q.slides.find((sl) => sl.startsWith(`${tag} Q`))?.match(/Q(\d+)$/)?.[1] ?? 0);
  const questions = phyQuestions
    .filter((q) => q.slides.some((sl) => sl.startsWith(`${tag} Q`)))
    .sort((a, b) => num(a) - num(b));
  return {
    id,
    title,
    subtitle: 'The test as it was actually set, in its own order, one mark each.',
    note,
    questions,
    minutes: mins,
  };
}

const phy121: Course = {
  code: 'PHY121',
  title: 'General Physics II',
  tagline:
    'Electricity and magnetism drilled as calculations, the way the test sets them. Five options, every one explained, and the working shown in full.',
  blurb:
    'Charge and the electric field, potential and work, Gauss and flux, capacitance and dielectrics, DC circuits and internal resistance, magnetic force, Biot-Savart and Ampere, induction and transformers. Drill by topic, or sit either real computer-based test end to end.',
  moduleNoun: 'Topic',
  facetGuide: phyFacets,
  modules: [
    { number: 1, title: 'Charge, Coulomb and the Electric Field', blurb: 'Quantisation, F = qE, the field of a point charge, and adding two fields at a midpoint.' },
    { number: 2, title: 'Potential, Work and Energy', blurb: 'V = kQ/r falling as 1/r rather than 1/r squared, and the work done moving a charge.' },
    { number: 3, title: "Gauss's Law and Flux", blurb: 'Flux as EA cos theta, and why a charged conducting sphere behaves outside as a point charge at its centre.' },
    { number: 4, title: 'Capacitance and Dielectrics', blurb: 'Reading a network before reaching for a formula, the parallel plate with a dielectric, C = Q/V, and the energy stored.' },
    { number: 5, title: 'Current, Resistance and DC Circuits', blurb: 'Series resistance and the single current, and Ohm’s law from the terminal p.d.' },
    { number: 6, title: 'emf, Internal Resistance and Terminal Voltage', blurb: 'E = I(R + r) in both directions, and why the emf always exceeds the terminal p.d.' },
    { number: 7, title: 'Magnetic Force and Moving Charges', blurb: 'F = qvB sin theta, the torque on a current loop, and the radius of a circular path.' },
    { number: 8, title: 'Sources of Magnetic Fields', blurb: 'Ampere and symmetry, Biot-Savart and the inverse square, turns per metre in a solenoid, and the long straight wire.' },
    { number: 9, title: 'Electromagnetic Induction', blurb: 'Energy stored in an inductor, and why it is changing FLUX that induces an emf.' },
    { number: 10, title: 'Transformers', blurb: 'Efficiency as output over input, and the turns ratio as a step up or a step down.' },
    {
      number: 11,
      title: "Maxwell's Equations and Electromagnetic Waves",
      blurb:
        'The wave equation Maxwell found, and the moment two laboratory constants gave the speed of light exactly. E = cB, c = f lambda, intensity and the Poynting vector.',
    },
  ],
  questions: phyQuestions,
  examTags: ['Test 1 Q', 'Test 2 Q'],
  papers: [
    phyPaper(
      'Test 1',
      'phy-cbt-1',
      'Computer-Based Test 1, all 15 questions',
      'Captured as a graded review page marked 14 out of 15. Question 9 is quoted as printed and is INCOMPLETE: its stem ends at "represented by" with the figure missing, and it is the one question marked wrong, so the true answer cannot be recovered from the capture. Its review says so on every option.',
      20
    ),
    phyPaper(
      'Test 2',
      'phy-cbt-2',
      'Computer-Based Test 2, all 15 questions',
      'Captured as a graded review page marked 15 out of 15, so every answer here is confirmed by the examiner. Worth knowing: on this paper the correct choice was the FIRST option every single time. The drill shuffles options by default, which takes that crutch away.',
      20
    ),
  ],
};

export const COURSES: Course[] = [phy121, ent221, ift222, tmc221];

export function findCourse(code: string): Course | undefined {
  return COURSES.find((c) => c.code.toLowerCase() === code.toLowerCase());
}

export function courseByCode(code: string): Course {
  const found = findCourse(code);
  if (!found) throw new Error(`unknown course: ${code}`);
  return found;
}
