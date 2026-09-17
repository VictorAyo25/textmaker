/**
 * Part B of COS221's Learn by doing papers: PAST QUESTIONS ONLY.
 *
 *     node scripts/build-cos-doing.mjs
 *
 * Nothing here is invented. All 39 parts of the two solved papers are lifted out
 * of data/cos221/lessons.json with their wording untouched, each already
 * carrying the Break it down and the model answer the manual gated, and are
 * regrouped BY TOPIC instead of by paper.
 *
 * Two labels go on each question, because this examiner repeats in two ways:
 *
 *   the SHAPE   define the terms, fix the code, dry run it, write a program.
 *               Both papers are built from those four, so knowing the count is
 *               knowing the paper.
 *   the SUBJECT overloading is defined in both years, the array walk is asked
 *               six times, the file question runs a whole question both years.
 *
 * It writes the questions into data/cos221/doing/m1.json to m9.json, whose
 * teaching half scripts/author/cos221_doing.py wrote, and
 * scripts/build-doing.mjs then assembles the papers.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { balanceHtml } from './lib/html-balance.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const WEBAPP = join(HERE, '..');
const OUT = join(WEBAPP, 'data', 'cos221', 'doing');

/** Block index in the paper lesson: [subject family, topic, shape]. */
const PARTS = {
  'paper-2526': {
    5: ['overloading', 4, 'define'],
    8: ['checked-unchecked', 9, 'define'],
    11: ['array-walk-fix', 7, 'fix'],
    14: ['digit-program', 3, 'program'],
    18: ['encapsulation', 5, 'define'],
    21: ['override-vs-overload', 5, 'define'],
    24: ['array-walk-fix', 7, 'fix'],
    27: ['digit-program', 3, 'program'],
    31: ['array-walk-program', 7, 'program'],
    35: ['file-program', 9, 'program'],
    39: ['inheritance-program', 5, 'program'],
    44: ['joptionpane-program', 2, 'program'],
    48: ['array-walk-program', 7, 'program'],
    52: ['digit-program', 3, 'program'],
    56: ['array-walk-program', 7, 'program'],
  },
  'paper-2425': {
    4: ['overloading', 4, 'define'],
    7: ['debug-snippet', 4, 'fix'],
    10: ['dry-run', 3, 'trace'],
    13: ['overloading-program', 4, 'program'],
    17: ['array-terms', 7, 'define'],
    20: ['debug-snippet', 7, 'fix'],
    23: ['dry-run', 3, 'trace'],
    26: ['array-walk-program', 7, 'program'],
    30: ['file-classes', 9, 'define'],
    33: ['debug-snippet', 9, 'fix'],
    36: ['file-output', 9, 'trace'],
    39: ['file-program', 9, 'program'],
    43: ['control-terms', 3, 'define'],
    46: ['debug-snippet', 3, 'fix'],
    49: ['dry-run', 3, 'trace'],
    52: ['class-program', 5, 'program'],
    56: ['oop-terms', 5, 'define'],
    59: ['array-walk-program', 7, 'program'],
    62: ['debug-snippet', 5, 'fix'],
    65: ['inheritance-program', 5, 'program'],
    69: ['loop-types', 3, 'program'],
    72: ['recursion-trace', 8, 'trace'],
    75: ['debug-snippet', 3, 'fix'],
    78: ['digit-program', 3, 'program'],
  },
};

const SUBJECT = {
  overloading: 'defining overloading and the method signature',
  'checked-unchecked': 'checked against unchecked exceptions',
  'array-walk-fix': 'a broken array walk to correct',
  'digit-program': 'a program over the digits of a number',
  encapsulation: 'defining encapsulation',
  'override-vs-overload': 'overloading against overriding',
  'array-walk-program': 'a program that walks an array and reports on it',
  'file-program': 'a program that writes records to a file and reads them back',
  'inheritance-program': 'a program built on inheritance and polymorphism',
  'joptionpane-program': 'a JOptionPane program that prices and summarises',
  'debug-snippet': 'a snippet to debug, with the errors listed and corrected',
  'dry-run': 'a dry run, stating the output of each pass',
  'overloading-program': 'a program that overloads one method name',
  'array-terms': 'defining the array terms',
  'file-classes': 'defining the file classes',
  'file-output': 'stating what the file ends up containing',
  'control-terms': 'defining the control structure terms',
  'class-program': 'a class with fields, a constructor and methods',
  'oop-terms': 'defining inheritance, polymorphism and overriding',
  'loop-types': 'a snippet demonstrating each loop type',
  'recursion-trace': 'tracing a recursive method by hand',
};

const SHAPE = {
  define: ['Define the terms', 'the definitions that open a question, three marks for three lines'],
  fix: ['Fix the code', 'a snippet with planted errors, to list and correct'],
  trace: ['Dry run it', 'a table of one row per pass, then the final value'],
  program: ['Write a program', 'a full program, marked on structure as much as on logic'],
};

const YEAR = { 'paper-2526': '2025/2026', 'paper-2425': '2024/2025' };

function build() {
  const lessons = JSON.parse(readFileSync(join(WEBAPP, 'data', 'cos221', 'lessons.json'), 'utf8'));
  const all = [];
  for (const [slug, map] of Object.entries(PARTS)) {
    const lesson = lessons.find((l) => l.slug === slug);
    if (!lesson) throw new Error(`no lesson ${slug}`);
    let heading = '';
    lesson.blocks.forEach((b, i) => {
      if (b.kind === 'heading') heading = b.text;
      const spec = map[i];
      if (!spec) return;
      if (b.kind !== 'asprinted') throw new Error(`${slug} block ${i} is ${b.kind}, not a question`);
      const recall = lesson.blocks[i + 1];
      const worked = lesson.blocks[i + 2];
      if (recall?.kind !== 'recall' || worked?.kind !== 'worked')
        throw new Error(`${slug} block ${i}: expected As printed, Break it down, Model answer`);
      const [subject, topic, shape] = spec;
      all.push({
        year: YEAR[slug],
        section: heading.replace(/,.*$/, ''),
        marks: b.tag,
        subject,
        topic,
        shape,
        printed: balanceHtml(b.printed),
        question: balanceHtml(recall.question),
        answer: balanceHtml(recall.answer),
        problem: balanceHtml(worked.problem ?? ''),
        model: balanceHtml([worked.working, worked.answer].filter(Boolean).join('\n')),
      });
    });
  }
  const expected = Object.values(PARTS).reduce((t, m) => t + Object.keys(m).length, 0);
  if (all.length !== expected) throw new Error(`found ${all.length} parts, expected ${expected}`);

  const bySubject = {};
  const byShape = {};
  for (const p of all) {
    (bySubject[p.subject] ??= []).push(p);
    (byShape[p.shape] ??= []).push(p);
  }

  for (let topic = 1; topic <= 9; topic += 1) {
    const file = join(OUT, `m${topic}.json`);
    const meta = JSON.parse(readFileSync(file, 'utf8'));
    const mine = all.filter((p) => p.topic === topic);

    meta.questions = mine.map((p) => {
      const kin = bySubject[p.subject].filter((x) => x !== p);
      const [shapeName, shapeNote] = SHAPE[p.shape];
      const here = byShape[p.shape].filter((x) => x.topic === topic).length;
      const label =
        `<p class="flag"><b>Shape: ${shapeName}.</b> ${shapeNote[0].toUpperCase()}${shapeNote.slice(1)}. ` +
        `The two papers set this shape <b>${byShape[p.shape].length} times</b> between them, ${here} of them on this topic.</p>` +
        (kin.length
          ? `<p class="flag"><b>And the subject repeats:</b> ${SUBJECT[p.subject]} is also set in ${kin
              .map((x) => `<b>${x.year}, ${x.section}, ${x.marks.toLowerCase()}</b>`)
              .join(', ')}.</p>`
          : '');
      return {
        heading: `${p.year}, ${p.section}, ${p.marks.toLowerCase()}`,
        marks: p.marks,
        scenario: {
          printed: true,
          src: `${p.year}:${p.section}:${p.marks}`,
          tag: `${p.year}, ${p.section}`,
          text: p.printed,
        },
        asked: label,
        breakdown: { question: p.question, answer: p.answer },
        exam: {
          problem:
            p.problem ||
            `<p>Write your full answer to this in your book first, then open the model answer.</p>`,
          answer: p.model,
        },
        frames: [],
      };
    });

    writeFileSync(file, JSON.stringify(meta, null, 2) + '\n', 'utf8');
    console.log(
      `  m${topic}: ${String(mine.length).padStart(2)} past questions, ${meta.methodFrames.length} method frames`
    );
  }

  console.log(`  ${all.length} past question parts, from both solved papers`);
  console.log(
    `  by shape: ${Object.entries(byShape)
      .map(([k, v]) => `${SHAPE[k][0]} ${v.length}`)
      .join(', ')}`
  );
  const repeated = Object.entries(bySubject).filter(([, v]) => v.length > 1);
  console.log(
    `  ${repeated.length} subjects set more than once, ${repeated.reduce((t, [, v]) => t + v.length, 0)} parts between them`
  );
}

build();
