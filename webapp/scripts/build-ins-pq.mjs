/**
 * INS224's past questions, filed by module instead of by year.
 *
 *     node scripts/build-ins-pq.mjs
 *
 * Three papers inside Learn by doing, for a reader who will answer only the
 * Module One and Module Two theory questions:
 *
 *   pq1  Module One,  the questions whose answerable parts are Module One
 *   pq2  Module Two,  the same for Module Two
 *   pq3  off the plan, the one question with nothing on those two modules,
 *        plus a table of every part skipped elsewhere and where it lives
 *
 * Each question appears ONCE, WHOLE and as printed, because that is how the
 * examiner gives it and because most questions straddle modules. What makes it
 * usable is the label above it: a part by part map saying which parts to answer
 * and which to skip, and the repeat label naming every other paper that set the
 * same thing. Ordered by how often that family has been set, not by year.
 *
 * Nothing is invented. The questions, their Break it down and their model
 * answers are lifted from data/ins224/lessons.json, where both papers are
 * already solved and gated. The course text's own tutor marked assignments are
 * included too, quoted from the text and labelled as assignments, because
 * 24/25 Q1(c) is the clothing line assignment from page 43 almost word for word.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { balanceHtml } from './lib/html-balance.mjs';

/**
 * The teaching half. Every past question is answered in full first and then
 * TAUGHT, because Victor asked for both: the answer as you would write it, then
 * the same ground from nothing. One programme per FAMILY, attached to the most
 * repeated question in it, because three ERD questions do not need the ERD
 * method three times; the others carry a pointer to it instead.
 */

const HERE = dirname(fileURLToPath(import.meta.url));
const FRAMES = JSON.parse(
  readFileSync(new URL('./author/ins224_pq_frames.json', import.meta.url), 'utf8')
);
/** Which question teaches which family, and where the rest should look. */
const TAUGHT = {
  'clothing-line': 'the clothing line assignment at the top of this paper',
  '2425-q2': 'Question Two of 2024/2025, above',
  '2526-q3': 'Question Three of 2025/2026, in this paper',
  'restaurant-car': 'the restaurant and car rental assignment at the top of this paper',
  '2425-q3': 'Question Three of 2024/2025, above',
  '2526-q1': 'Question One of 2025/2026, above',
  '2425-q1': 'Question One of 2024/2025, in this paper',
  'sports-centre': 'the sports centre assignment in this paper',
};
const WEBAPP = join(HERE, '..');
const OUT = join(WEBAPP, 'data', 'ins224', 'doing');

/**
 * The diagrams each past question answer was missing. Some answers already
 * carry one from the manual, so only the gaps are named here: the warehouse
 * answer had its Level 0 DFD but no ERD, the landlord answer had its ERD and
 * Level 0 but no context diagram and no Level 1.
 */
const FIGS = {
  'clothing-line': [],
  retail: [],
  'restaurant-car': ['restaurant-erd', 'carrental-erd'],
  'sports-centre': ['sportscentre-usecase'],
  'paper-2425:8': ['warehouse-erd'],
  'paper-2526:1': ['landlord-context', 'landlord-dfd1'],
  'paper-2425:12': ['ie-cardinality', 'sales-erd', 'researchers-erd'],
  'paper-2425:18': ['appointments-usecase'],
  'paper-2526:5': ['hospital-billing-usecase'],
};

const FIGURES = JSON.parse(
  readFileSync(new URL('../data/ins224/figures.json', import.meta.url), 'utf8')
);

/** The drawings, under the answer that asks for them. */
function drawings(keys) {
  if (!keys?.length) return '';
  return (
    '<p><b>The diagram' +
    (keys.length > 1 ? 's' : '') +
    ' this question asks for, drawn.</b> Copy the shape, not the wording: the entity names and the cardinalities are what carry the marks.</p>' +
    keys.map((k) => {
      if (!FIGURES[k]) throw new Error(`no figure called ${k}`);
      return FIGURES[k];
    }).join('')
  );
}

/** A part by part map, rendered as the label above each question. */
const P = (part, module, do_, what) => ({ part, module, do: do_, what });

/** The paper questions, in the order they should be practised. */
const QUESTIONS = {
  pq1: [
    {
      teaches: '2425-q2',
from: ['paper-2425', 4],
      heading: '2024/2025, Question Two: training a team on the life cycle',
      repeat:
        'The SDLC phases have been asked three times: here for their objectives and activities, in <b>2025/2026 Q5(b)</b> as the five project planning activities, and in the course text’s own assignment on page 25. Learn the phases once and all three are answered.',
      parts: [
        P('a', 'Module One', true, 'Objectives and activities of the analysis, design, implementation and support phases'),
        P('b', 'Module One', true, 'Three stakeholders and how each views an information system'),
        P('c', 'Module One', true, 'Tools against techniques, with two examples of each'),
        P('d', 'Module One', true, 'What you would need to know about a business to design for it'),
      ],
    },
    {
      taughtBy: 'clothing-line',
from: ['paper-2526', 15],
      heading: '2025/2026, Question Five: the federal teaching hospital',
      repeat:
        'Choosing a methodology is the most repeated thing in Module One: here as a comparison of seven, in <b>2024/2025 Q1(c)</b> as a choice with the phases mapped, and twice in the course text, pages 26 and 43. Part (b) is the planning activities again, and part (c) belongs to Module Two.',
      parts: [
        P('a', 'Module One', true, 'Compare seven methodologies, saying briefly why each suits this project or does not'),
        P('b', 'Module One', true, 'Five activities in project planning'),
        P('c', 'Module Two', true, 'Formulate business, user, functional, non functional and system requirements'),
      ],
    },
    {
      teaches: '2526-q3',
from: ['paper-2526', 9],
      heading: '2025/2026, Question Three: Tikki Tikka and the Boys',
      repeat:
        'Two families here recur. The analyst’s problem solving approach is asked again in <b>2024/2025 Q6(a)</b>, and the analyst’s skills in <b>2024/2025 Q5(a)</b>. Every part of this question is Module One, which makes it the best single rehearsal for your Question 1.',
      parts: [
        P('a', 'Module One', true, 'The three questions answered during feasibility analysis'),
        P('b', 'Module One', true, 'Six more steps of the problem solving approach, after research and understand'),
        P('c', 'Module One', true, 'How to explain to stakeholders what a model is'),
        P('d', 'Module One', true, 'Another skill the analyst needs, in detail, beyond people skills'),
        P('e', 'Module One', true, 'Three activities the support group takes part in'),
        P('f', 'Module One', true, 'Three other job roles the analyst can fill'),
      ],
    },
    {
      taughtBy: '2526-q3',
from: ['paper-2425', 15],
      heading: '2024/2025, Question Five: recruiting an analyst',
      repeat:
        'Part (a) is the analyst’s skills, also set in <b>2025/2026 Q3(d)</b>. Parts (b) and (c) are Module Three, a hospital class diagram and the object oriented concepts, so they are not yours to answer: read the model answer if you have spare time, since Module Three still appears in the objective half.',
      parts: [
        P('a', 'Module One', true, 'Three skills you would look for in an analyst, in detail'),
        P('b', 'Module Three', false, 'A class diagram for a hospital management system'),
        P('c', 'Module Three', false, 'Polymorphism, inheritance, composition and aggregation'),
      ],
    },
  ],
  pq2: [
    {
      teaches: '2425-q3',
from: ['paper-2425', 8],
      heading: '2024/2025, Question Three: the warehouse receiving stock',
      repeat:
        'The ERD from a narrative is the most asked thing on this paper: four sightings, here and in <b>2025/2026 Q1(a)</b>, <b>2024/2025 Q4(d)</b> and <b>2024/2025 Q4(f)</b>. The DFD theory in parts (a), (b) and (e) is asked again all through 2024/2025 Q4.',
      parts: [
        P('a', 'Module Two', true, 'Four elements of a data flow diagram'),
        P('b', 'Module Two', true, 'What a data store is, and how it should be named'),
        P('c', 'Module Two', true, 'Read a given ERD back, stating the cardinal relationships'),
        P('d', 'Module Two', true, 'The warehouse: an ERD, then a Level 0 DFD'),
        P('e', 'Module Two', true, 'Three ways to validate the integrity of your diagrams'),
      ],
    },
    {
      teaches: '2526-q1',
from: ['paper-2526', 1],
      heading: '2025/2026, Question One: the landlord and the estate agent',
      repeat:
        'An ERD and all three DFD levels from one narrative, which is the heaviest drawing question on either paper. The ERD family has four sightings; reading a diagram back, part (d), is asked again in <b>2024/2025 Q3(c)</b> and <b>Q4(b)</b>. Part (c) is project management, thin in the course text: answer it from the nine principles and the planning phase.',
      parts: [
        P('a', 'Module Two', true, 'An ERD of the entities in the narrative'),
        P('b', 'Module Two', true, 'A context diagram, a Level 0 DFD, and a Level 1 DFD of rent payment'),
        P('c', 'Module One', true, 'Three more reasons a project succeeds and three more why it fails'),
        P('d', 'Module Two', true, 'Read and interpret the printed diagram, forwards and backwards'),
      ],
    },
    {
      taughtBy: '2425-q3',
from: ['paper-2425', 12],
      heading: '2024/2025, Question Four: process and data modelling, end to end',
      repeat:
        'Two more ERDs from narratives, parts (d) and (f), and the cardinality reading again in part (b). Between this question and Question Three, 2024/2025 asks the ERD four times and the DFD theory six times. Part (g) is acquisition strategy, which is off your plan.',
      parts: [
        P('a', 'Module Two', true, 'Four reasons to model the processes first'),
        P('b', 'Module Two', true, 'The cardinal relationships in Information Engineering style, what makes a relationship optional, and data balancing'),
        P('c', 'Module Two', true, 'Three differences between process modelling and data modelling'),
        P('d', 'Module Two', true, 'An ERD for the sales management scenario'),
        P('e', 'Module Two', true, 'Why data cannot move between entities, with a diagram'),
        P('f', 'Module Two', true, 'An ERD for researchers, institutions and research interests'),
        P('g', 'Design', false, 'A system acquisition strategy for a hospital system in one month'),
      ],
    },
    {
      teaches: '2425-q1',
from: ['paper-2425', 1],
      heading: '2024/2025, Question One: the library system, and the clothing line',
      repeat:
        'Requirements elicitation is set twice, here and in <b>2025/2026 Q6(b)</b>, and the requirement categories twice, here and in <b>2025/2026 Q5(c)</b>. <b>Part (c) is the proven repeat:</b> it is the course text’s own assignment from Module One Unit 3, page 43, almost word for word, and it is Module One rather than Module Two.',
      parts: [
        P('a', 'Module Two', true, 'Two elicitation techniques, justified, with an advantage and a limitation each'),
        P('b', 'Module Two', true, 'Three functional and three non functional requirements, and why to ask users at different levels'),
        P('c', 'Module One', true, 'The clothing line: choose a methodology, map the phases, and answer the scope creep question'),
      ],
    },
    {
      taughtBy: '2425-q1',
from: ['paper-2526', 18],
      heading: '2025/2026, Question Six: the AI programming platform',
      repeat:
        'The elicitation plan in part (b) is the same family as <b>2024/2025 Q1(a)</b>. Parts (c), (d) and (e) are UML and class relationships, which is Module Three: skip them in the hall, but they are worth reading, because the objective half draws on all three modules.',
      parts: [
        P('a', 'Module Two', true, 'As-is weaknesses, to-be improvements, and the assumptions to validate'),
        P('b', 'Module Two', true, 'An elicitation plan with four techniques, their stakeholders and what each collects'),
        P('c', 'Module Three', false, 'Short notes on UML, its inventors and uses'),
        P('d', 'Module Three', false, 'The two categories of UML diagram, with two in each'),
        P('e', 'Module Three', false, 'Inheritance, composition, aggregation and association, with diagrams'),
      ],
    },
    {
      taughtBy: 'sports-centre',
from: ['paper-2425', 18],
      heading: '2024/2025, Question Six: the hospital appointments',
      repeat:
        'The use case diagram from a narrative has three sightings: here, <b>2025/2026 Q2(b)</b>, and the course text’s sports centre assignment on page 72. Part (a) is the analyst as problem solver, the same family as <b>2025/2026 Q3(b)</b>. The activity diagram in (b)(ii) is Module Three.',
      parts: [
        P('a', 'Module One', true, 'Why a systems analyst is a problem solver, with reasons'),
        P('b i', 'Module Two', true, 'A use case diagram for the appointments scenario'),
        P('b ii', 'Module Three', false, 'An activity diagram for the same scenario'),
      ],
    },
    {
      taughtBy: 'sports-centre',
from: ['paper-2526', 5],
      heading: '2025/2026, Question Two: the hospital patient billing system',
      repeat:
        'Only part (b), the use case diagram, is yours: it is the third sighting of that family. The rest of this question is Module Three, and it is the clearest evidence that health care scenarios come with UML asks while business scenarios come with ERD and DFD asks.',
      parts: [
        P('a', 'Module Three', false, 'A class diagram with multiplicity'),
        P('b', 'Module Two', true, 'A use case diagram for the system'),
        P('c', 'Module Three', false, 'An activity diagram of the process flow'),
        P('d', 'Module Three', false, 'Three drawbacks of multiple inheritance'),
      ],
    },
  ],
  pq3: [
    {
      teaches: '2526-q4',
from: ['paper-2526', 12],
      heading: '2025/2026, Question Four: Vought Industries and the pharmaceutical system',
      repeat:
        'Nothing in this question is Module One or Module Two. It is acquisition strategy, software and hardware architecture, interface design and relational database design, which the course text covers in its later material and which your confirmed format does not reach. It is here so that you know what it was, not so that you prepare it.',
      parts: [
        P('a', 'Design', false, 'The acquisition strategy for a short time frame, and three supporting factors'),
        P('b', 'Design', false, 'Two software architectural functions'),
        P('c', 'Design', false, 'Two more types of hardware requirement'),
        P('d', 'Design', false, 'Three principles of interface design'),
        P('e', 'Design', false, 'Design and populate a relational database'),
      ],
    },
  ],
};

/**
 * The course text's own tutor marked assignments, quoted from the text, with
 * the model answer the manual already prints for them. One of these has
 * already appeared on a paper, which is why they sit beside the paper questions.
 */
const ASSIGNMENTS = {
  pq1: [
    {
      teaches: 'clothing-line',
      tag: 'Course text, Module One Unit 3, page 43',
      heading: 'The course text’s clothing line assignment, the one he lifted',
      answerFrom: ['practical-one', 3],
      repeat:
        '<b>This is the strongest repeat evidence you have.</b> The examiner set this assignment as <b>2024/2025 Q1(c)</b> almost word for word: same project manager, same unclear requirements, same client demanding features near the end, same three cogent reasons. Work it here, then compare it with that paper question.',
      printed:
        'You are the chosen project manager for a new clothing line about to be launched. You very much need the project to succeed and are willing to give it your all.\n1. Outline and discuss five skills you must possess to make the project flourish.\n2. Define the scope of the project, state activities to be conducted, and give a detailed outline of the timeline of your project (for the space of six months)\n3. What are those criteria you will need to select good team members? List and explain 4 most important ones to you.\n4. The requirements of this work MAY NOT be clearly stated at the beginning. Choose an appropriate SDLC methodology and map the project’s phases.\n5. You are nearing the end of the project, and the client is insisting on adding new features, but you want to prevent scope and feature creep. Do you refuse or agree to add the new features? Give three cogent reasons for your decision as PM.',
      parts: [
        P('1', 'Module One', true, 'Five skills a project manager needs'),
        P('2', 'Module One', true, 'Scope, activities and a six month timeline'),
        P('3', 'Module One', true, 'Four criteria for selecting team members'),
        P('4', 'Module One', true, 'Choose a methodology for unclear requirements and map the phases'),
        P('5', 'Module One', true, 'Refuse or agree to late features, with three reasons'),
      ],
    },
    {
      taughtBy: 'clothing-line',
      tag: 'Course text, Module One Unit 2, pages 25 and 26',
      heading: 'The course text’s retail company assignment',
      answerFrom: ['practical-one', 2],
      repeat:
        'The same shape as every methodology question on both papers: a scenario, then identify, justify and outline. Its first part, explaining the Planning and Analysis phases, is the same family as <b>2024/2025 Q2(a)</b> and <b>2025/2026 Q5(b)</b>.',
      printed:
        '1. Explain the Planning and Analysis phases of the System Development Life Cycle (SDLC), highlighting their objectives and key activities.\n2. A medium-sized retail company wants to develop a new online sales and inventory management system. The company expects frequent changes in customer requirements, plans to introduce new features regularly, and seeks continuous user feedback throughout development. As a systems analyst,\na) Identify the most suitable software development approach for this project.\nb) Justify your choice by explaining how the selected approach addresses the company’s needs.\nc) Outline the key activities that would be carried out using this approach during system development.',
      parts: [
        P('1', 'Module One', true, 'The Planning and Analysis phases, objectives and activities'),
        P('2a', 'Module One', true, 'Identify the most suitable approach'),
        P('2b', 'Module One', true, 'Justify it against the company’s stated needs'),
        P('2c', 'Module One', true, 'Outline the key activities'),
      ],
    },
  ],
  pq2: [
    {
      teaches: 'restaurant-car',
      tag: 'Course text, Module Two Unit 4, pages 92 and 93',
      heading: 'The course text’s restaurant and car rental ERD assignments',
      answerFrom: ['practical-two', 3],
      repeat:
        'The ERD from a narrative has four sightings on the papers, and these two assignments are where the course text drills it. The car rental one is the associative entity case, which is the part most answers get wrong.',
      printed:
        '1. A restaurant wants to keep track of Customers and the Orders they place. A customer can place many orders, but each order belongs to one customer. Each order also contains one or more Menu Items, and a menu item can appear on many orders.\na. Identify all the entities involved.\nb. List at least three attributes for each entity and mark the identifier.\nc. Draw the complete ER diagram, showing all relationships and their cardinality\n2. A car rental company wants to keep track of Customers and the Vehicles they rent. A customer can rent many vehicles over time, and a vehicle can be rented by many different customers over time, but never by more than one customer at once.\na. Identify all the entities involved, including any associative entity needed to record each individual rental.\nb. List at least three attributes for each entity and mark the identifier for each.\nc. Draw the ER diagram, stating the cardinality and ordinality of every relationship shown',
      parts: [
        P('1', 'Module Two', true, 'The restaurant: entities, attributes with identifiers, and the ERD with cardinality'),
        P('2', 'Module Two', true, 'The car rental: the associative entity, and cardinality with ordinality'),
      ],
    },
    {
      teaches: 'sports-centre',
      tag: 'Course text, Module Two Unit 2, pages 71 and 72',
      heading: 'The course text’s sports centre use case assignment',
      answerFrom: ['practical-two', 2],
      repeat:
        'The use case diagram from a narrative has three sightings on the papers, in <b>2025/2026 Q2(b)</b> and <b>2024/2025 Q6(b)(i)</b>. This is the course text’s own version, and it asks for the narrative as well, which a paper question may also do.',
      printed:
        'A sports centre offers facilities such as football pitches, tennis courts, basketball courts, and a gym. Customers can book these facilities for specific dates and time slots using an online booking system.\nA Customer must first create an account and log in to the system. After logging in, the customer can view available sports facilities, check time slot availability, and make a booking for a preferred facility.\nWhen making a booking, the system displays available time slots. The customer selects a suitable date and time, confirms the booking, and proceeds to make payment. Once payment is successful, the booking is confirmed and recorded in the system. The customer can also view, modify, or cancel bookings. The system sends a booking confirmation notification (via email or SMS) after a successful reservation.\nA Staff/Admin manages the system by adding or updating facilities, setting availability schedules, and monitoring bookings. The admin can also generate reports on facility usage and customer bookings.\ni. Create a use case diagram for the sports centre booking system in this scenario.\nii. Develop a use case narrative for ANY four use cases in the diagram',
      parts: [
        P('i', 'Module Two', true, 'The use case diagram, with actors, boundary, include and extend'),
        P('ii', 'Module Two', true, 'A use case narrative for four of them, all seven parts each'),
      ],
    },
  ],
  pq3: [],
};

/** Where each paper's questions come first, so the highest value sits at the top. */
const ORDER = { pq1: ['assignments', 'questions'], pq2: ['assignments', 'questions'], pq3: ['questions'] };

const META = {
  pq1: {
    kick: 'Past questions, Module One',
    title: 'Past Questions: Module One',
    lead: 'Every past question whose answerable parts are Module One, filed by module rather than by year, most repeated first, with the course text assignments he draws from.',
    minutes: 95,
    partBHeading: 'The questions, most repeated first',
    intro:
      '<p><b>Past questions only, and nothing else.</b> This is your Question 1 practice: the parts of both papers that sit in Module One of the course text, plus the two tutor marked assignments the examiner draws from.</p>' +
      '<div class="keypoint"><span class="kplab">How to read the label above each question</span><p>Every question is here <b>whole and as printed</b>, because that is how you will meet it. The table above each one says, part by part, which module it belongs to and whether you answer it. The line under that names every other paper where the same thing was set.</p></div>' +
      '<p><b>Order is by repetition, not by year.</b> The clothing line assignment is first because he set it as a paper question almost word for word.</p>',
    lockin: {
      big: '"Module One has no diagrams, so every mark is a named list tied to a phrase in the scenario. Identify, justify, outline."',
      sub: 'Methodology choice, the analyst’s eight steps, the analyst’s skills and the SDLC phases are the four families he keeps returning to. Learn those four and Question 1 is answered.',
    },
  },
  pq2: {
    kick: 'Past questions, Module Two',
    title: 'Past Questions: Module Two',
    lead: 'Every past question whose answerable parts are Module Two, filed by module rather than by year, most repeated first, with the course text assignments that drill the same diagrams.',
    minutes: 120,
    partBHeading: 'The questions, most repeated first',
    intro:
      '<p><b>Past questions only, and nothing else.</b> This is your Question 2 practice, and it is the heavier of the two: Module Two is where the drawing marks are.</p>' +
      '<div class="keypoint"><span class="kplab">How to read the label above each question</span><p>Every question is here <b>whole and as printed</b>. The table above each one says, part by part, which module it belongs to and whether you answer it. The line under that names every other paper where the same thing was set.</p></div>' +
      '<p><b>Draw every diagram by hand.</b> The ERD from a narrative has four sightings across the two papers, the DFD levels two, and reading a diagram back three. Those three between them are most of this module’s marks.</p>',
    lockin: {
      big: '"ERD from a narrative, DFD in three levels, use case from a narrative, and reading a diagram back. Four things, asked over and over."',
      sub: 'Name every relationship with a verb, resolve a many to many with an associative entity, give cardinality AND ordinality, and write the balancing sentence under every levelled DFD.',
    },
  },
  pq3: {
    kick: 'Past questions, off your plan',
    title: 'Past Questions: Off Your Plan',
    lead: 'The one past question with nothing on Modules One or Two, kept rather than deleted, plus a map of every part skipped elsewhere and where its answer lives.',
    minutes: 25,
    partBHeading: 'The question you are not preparing',
    intro:
      '<p><b>You are answering Modules One and Two.</b> This paper exists so that nothing is hidden from you: it holds the one past question that has no part on your two modules, and below it a map of every part skipped in the other two papers.</p>' +
      '<p>Two reasons to spend twenty minutes here anyway: the objective half of your paper draws on <b>all three modules</b>, and if one of your two written questions turns out worse than you hoped, Question 3 is the fallback.</p>',
    lockin: {
      big: '"Skipped is not the same as unknown. You know what you left out, and where its answer is."',
      sub: 'Module Three is objects, class diagrams and the behavioural diagrams. Design and acquisition sit outside your format entirely.',
    },
  },
};

function lift(lessons, [slug, index]) {
  const lesson = lessons.find((l) => l.slug === slug);
  if (!lesson) throw new Error(`no lesson ${slug}`);
  const block = lesson.blocks[index];
  if (!block) throw new Error(`${slug} has no block ${index}`);
  const after = lesson.blocks.slice(index + 1, index + 5);
  return {
    block,
    recall: after.find((b) => b.kind === 'recall'),
    worked: after.find((b) => b.kind === 'worked'),
  };
}

function partTable(parts) {
  const rows = parts
    .map(
      (p) =>
        `<tr><td><b>(${p.part})</b></td><td>${p.module}</td><td>${
          p.do ? '<b>Answer it</b>' : 'Skip on your plan'
        }</td><td>${p.what}</td></tr>`
    )
    .join('');
  const mine = parts.filter((p) => p.do).length;
  return (
    `<p><b>${mine} of ${parts.length} parts are yours.</b></p>` +
    `<table><tr><th>Part</th><th>Module</th><th>On your plan</th><th>What it asks</th></tr>${rows}</table>`
  );
}

function build() {
  const lessons = JSON.parse(readFileSync(join(WEBAPP, 'data', 'ins224', 'lessons.json'), 'utf8'));

  for (const key of ['pq1', 'pq2', 'pq3']) {
    const questions = [];

    const pointer = (q) =>
      q.teaches
        ? ''
        : q.taughtBy
          ? `<p class="flag"><b>The method is taught in this section.</b> Work the frames under ${
              TAUGHT[q.taughtBy]
            }, then come back and write this one against the clock.</p>`
          : '';

    const fromAssignments = (ASSIGNMENTS[key] ?? []).map((a) => {
      const { block, recall, worked } = lift(lessons, a.answerFrom);
      const model = worked ?? block;
      return {
        heading: a.heading,
        marks: a.tag,
        scenario: { printed: true, src: a.tag, tag: `${a.tag}, a tutor marked assignment`, text: a.printed },
        asked: `<p class="flag">${a.repeat}</p>` + partTable(a.parts) + pointer(a),
        breakdown: {
          question:
            '<p>Work this in your book before you open anything. What is given, what is asked, and what would earn nothing?</p>',
          answer: balanceHtml(
            model.problem
              ? `<p class="row"><b class="lab">The manual’s own version</b> ${model.problem}</p>`
              : '<p class="row"><b class="lab">Work it first</b> Write the full answer in your book, then mark yourself against the model below.</p>'
          ),
        },
        exam: {
          problem: `<p>Answer the assignment above in full in your book, then open this.</p>`,
          answer:
            balanceHtml([model.working, model.answer].filter(Boolean).join('\n')) +
            drawings(FIGS[a.teaches ?? ''] ?? []),
        },
        frames: a.teaches ? FRAMES[a.teaches] : [],
      };
    });

    const fromPapers = (QUESTIONS[key] ?? []).map((q) => {
      const { block, recall, worked } = lift(lessons, q.from);
      if (block.kind !== 'asprinted') throw new Error(`${q.from.join(' ')} is ${block.kind}`);
      if (!worked) throw new Error(`${q.from.join(' ')} has no model answer`);
      return {
        heading: q.heading,
        marks: block.tag,
        scenario: {
          printed: true,
          src: block.tag,
          tag: `${block.tag}, as printed`,
          text: balanceHtml(block.printed),
        },
        asked: `<p class="flag">${q.repeat}</p>` + partTable(q.parts) + pointer(q),
        breakdown: recall
          ? { question: balanceHtml(recall.question), answer: balanceHtml(recall.answer) }
          : {
              question: '<p>What is given, what is asked, and how long should each part be?</p>',
              answer:
                '<p class="row"><b class="lab">Work it first</b> Answer in your book, then mark yourself against the model below.</p>',
            },
        exam: {
          problem: balanceHtml(
            worked.problem || `<p>Answer the parts marked yours above, then open the model answer.</p>`
          ),
          answer:
            balanceHtml([worked.working, worked.answer].filter(Boolean).join('\n')) +
            drawings(FIGS[`${q.from[0]}:${q.from[1]}`] ?? []),
        },
        frames: q.teaches ? FRAMES[q.teaches] : [],
      };
    });

    for (const group of ORDER[key])
      questions.push(...(group === 'assignments' ? fromAssignments : fromPapers));

    const meta = { ...META[key], questions };
    writeFileSync(join(OUT, `${key}.json`), JSON.stringify(meta, null, 2) + '\n', 'utf8');
    const mine = questions.length;
    console.log(`  ${key}: ${mine} questions (${fromAssignments.length} from the course text)`);
  }

  // The skipped map, appended to the last paper, so nothing is silently dropped.
  const skipped = [];
  for (const key of ['pq1', 'pq2'])
    for (const q of QUESTIONS[key])
      for (const p of q.parts.filter((x) => !x.do))
        skipped.push(`<tr><td>${q.from[0] === 'paper-2526' ? '2025/2026' : '2024/2025'}, ${q.heading.replace(/^[^:]*: /, '')}</td><td>(${p.part})</td><td>${p.module}</td><td>${p.what}</td></tr>`);
  const file = join(OUT, 'pq3.json');
  const meta = JSON.parse(readFileSync(file, 'utf8'));
  meta.questions.push({
    heading: 'Every part you are skipping, and where its answer is',
    marks: 'the map',
    scenario: {
      printed: false,
      tag: 'so that nothing is hidden',
      text:
        '<p>These are the parts marked "skip on your plan" in the Module One and Module Two papers. Each one is answered in full in the paper lesson it came from, under <b>The 2025/2026 Paper</b> or <b>The 2024/2025 Paper</b>.</p>' +
        `<table><tr><th>Question</th><th>Part</th><th>Module</th><th>What it asks</th></tr>${skipped.join('')}</table>`,
    },
    asked:
      '<p class="flag">Read these only if Module Three’s objective questions feel thin, or if you decide in the hall to attempt Question 3 after all.</p>',
    breakdown: {
      question: '<p>Before you leave this page: which of these could you attempt anyway, if a written question went badly?</p>',
      answer:
        '<p class="row"><b class="lab">The realistic fallback</b> The use case diagram, because you are preparing it for Module Two anyway, and the four class relationships, because they are four labelled sketches.</p>' +
        '<p class="row"><b class="lab">The rest</b> Acquisition strategy, architecture, interface design and relational database design are outside your format and outside the three module theory questions.</p>',
    },
    exam: {
      problem: '<p>Nothing to answer here. The map above is the whole point of the page.</p>',
      answer:
        '<p>Every skipped part is worked in full in the paper it came from. Open <b>The 2025/2026 Paper</b> or <b>The 2024/2025 Paper</b> in the crash course and read the model answer beside the question.</p>',
    },
    frames: [],
  });
  writeFileSync(file, JSON.stringify(meta, null, 2) + '\n', 'utf8');
  console.log(`  pq3: ${skipped.length} skipped parts mapped`);
}

build();
