/**
 * Part B of IFT222's Learn by doing papers: PAST QUESTIONS ONLY.
 *
 *     node scripts/build-ift-doing.mjs
 *
 * Nothing here is invented. Every question is one the examiner set, lifted with
 * its wording untouched from two places that have already been gated:
 *
 *   the app's own solved papers   data/ift222/lessons.json, 25/26 and 24/25,
 *                                 each question As printed with its model answer
 *   the manual's teaching modules the 23/24 and 20/21 questions, each with the
 *                                 Break it down and the worked solution the
 *                                 manual prints beside it
 *
 * Then it does the one thing neither source does: it groups them BY TOPIC rather
 * than by year, and labels every repeat. This examiner recycles: the IEEE 754
 * representation question, the average memory access time question, the locality
 * definitions and the signed number table have each been set in three different
 * years. Seeing that is worth more than any prediction.
 *
 * It writes data/ift222/doing/m1.json to m12.json in the same shape the authored
 * courses use, and scripts/build-doing.mjs then assembles the papers.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { paperSites } from './lib/manual-boxes.mjs';
import { balanceHtml } from './lib/html-balance.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const WEBAPP = join(HERE, '..');
const MANUAL = join(
  WEBAPP, '..', 'courses', 'IFT222 - Computer Architecture and Organisation', 'build', 'content'
);
const OUT = join(WEBAPP, 'data', 'ift222', 'doing');

/**
 * Every past question part, with the topic it belongs to and the family it
 * belongs to. A family is one question the examiner asks again and again, so
 * membership is what generates the repeat label on each of them.
 *
 * Keys are the app's own tags for 25/26 and 24/25, and year:question:file for
 * the 23/24 and 20/21 questions, which are read out of the manual and whose
 * question numbers repeat across files.
 */
const APP = {
  '25/26 Q1(a)': ['arch-org', 1],
  '25/26 Q1(b)': ['pipeline-speedup', 12],
  '25/26 Q1(c)': ['signed-table', 4],
  '25/26 Q1(d)': ['cpi-mips', 9],
  '25/26 Q1(e)': ['addressing-trace', 7],
  '25/26 Q2(a)': ['cache-fields', 11],
  '25/26 Q2(b)': ['hazards', 12],
  '25/26 Q2(c)': ['cache-fields', 11],
  '25/26 Q3(a)': ['cache-fields', 11],
  '25/26 Q3(b)': ['pipeline-stages', 12],
  '25/26 Q3(c)': ['amdahl', 9],
  '25/26 Q4(a)': ['float-compare', 5],
  '25/26 Q4(b)': ['instr-formats', 6],
  '25/26 Q4(c)': ['image-memory', 10],
  '25/26 Q5(a)': ['ieee-represent', 5],
  '25/26 Q5(b)': ['pipeline-latch', 12],
  '25/26 Q5(c)': ['locality', 11],
  '25/26 Q5(d)': ['ieee-reverse', 5],
  '24/25 Q1(a)': ['float-compare', 5],
  '24/25 Q1(b)': ['amat', 11],
  '24/25 Q1(c)': ['cache-fields', 11],
  '24/25 Q1(d)': ['instr-formats', 6],
  '24/25 Q2(a)': ['cache-benefit', 11],
  '24/25 Q2(b)': ['locality', 11],
  '24/25 Q2(c)': ['assembly-add', 6],
  '24/25 Q3(a)': ['von-neumann', 10],
  '24/25 Q3(b)': ['signed-table', 4],
  '24/25 Q3(b)(ii)': ['image-memory', 10],
  '24/25 Q3(c)': ['ieee-represent', 5],
  '24/25 Q4(a)': ['risc-cisc', 9],
  '24/25 Q4(b)': ['end-around-carry', 4],
  '24/25 Q4(c)': ['ieee-reverse', 5],
  '24/25 Q5(a)': ['instruction-categories', 6],
  '24/25 Q5(b)': ['pipeline-latch', 12],
  '24/25 Q5(c)': ['ieee-arithmetic', 5],
};

const MAN = {
  '2023-2024:Q1b:module2_unit2.html': ['amdahl', 9],
  '2023-2024:Q1c:module1_unit3.html': ['float-compare', 5],
  '2023-2024:Q1d:module3_unit3.html': ['set-assoc-size', 11],
  '2023-2024:Q3a:module3_unit3.html': ['amat', 11],
  '2023-2024:Q3c:module3.html': ['locality', 11],
  '2023-2024:Q4b:module1_unit2.html': ['signed-table', 4],
  '2023-2024:Q5c:module4.html': ['risc-cisc', 9],
  '2020-2021:Q1a:module2.html': ['address-bus', 8],
  '2020-2021:Q1b:module2_unit3.html': ['pipelining-basics', 12],
  '2020-2021:Q1c:module4.html': ['hazards', 12],
  '2020-2021:Q4b:module4.html': ['risc-cisc', 9],
  '2020-2021:Q5a:module2.html': ['address-bus', 8],
  '2020-2021:Q5a:module1_unit2.html': ['end-around-carry', 4],
  '2020-2021:Q5b:module3_unit2.html': ['dram-sram', 8],
  '2020-2021:Q5b:module1_unit2.html': ['overflow-sum', 4],
};

/** What each family is, for the label that names the repeat. */
const FAMILY = {
  'arch-org': 'Architecture against organization, and Von Neumann against Harvard',
  'pipeline-speedup': 'Speedup of a pipelined processor over a non pipelined one',
  'signed-table': 'The signed number table: unsigned, sign and magnitude, one’s and two’s complement',
  'cpi-mips': 'CPI and MIPS from an instruction mix',
  'addressing-trace': 'Tracing the addressing modes through a register and memory dump',
  'cache-fields': 'Splitting an address into tag, line or set, and word fields',
  'hazards': 'Data hazards in a code segment',
  'pipeline-stages': 'A five stage pipeline, its cycles and its speedup',
  'amdahl': 'Amdahl’s law',
  'float-compare': 'Three IEEE 754 numbers in registers, compared',
  'instr-formats': 'Zero, one, two and three address instruction formats',
  'image-memory': 'The memory an image needs, from inches and dpi',
  'ieee-represent': 'Representing a decimal number in IEEE 754 single precision',
  'pipeline-latch': 'A four phase pipeline with latch delay',
  'locality': 'Locality of reference, temporal and spatial',
  'ieee-reverse': 'Reading a value back out of an IEEE 754 bit pattern',
  'amat': 'Average memory access time, simultaneous against hierarchical',
  'cache-benefit': 'How cache memory improves performance',
  'assembly-add': 'An assembly program that adds two numbers',
  'von-neumann': 'The Von Neumann concept and its bottleneck',
  'risc-cisc': 'RISC against CISC, with example processors',
  'end-around-carry': 'End around carry in one’s complement',
  'instruction-categories': 'The categories of instruction, with examples',
  'ieee-arithmetic': 'Arithmetic carried out in IEEE 754',
  'set-assoc-size': 'The size of a set associative cache, line, set and whole',
  'address-bus': 'Address bus width against addressable memory',
  'pipelining-basics': 'What pipelining is, and the time it saves',
  'dram-sram': 'DRAM against SRAM',
  'overflow-sum': 'Adding in a fixed width register, and overflow',
};

const YEAR_OF = { '25/26': '2025/2026', '24/25': '2024/2025', '23/24': '2023/2024', '20/21': '2020/2021' };
const short = (year) => year.replace(/^\d\d(\d\d)-\d\d(\d\d)$/, '$1/$2');
const qLabel = (q) => q.replace(/^Q(\d+)([a-z])?$/, (_, n, l) => `Q${n}${l ? `(${l})` : ''}`);

/** The 25/26 and 24/25 questions, As printed and solved, from the app itself. */
function fromApp() {
  const lessons = JSON.parse(readFileSync(join(WEBAPP, 'data', 'ift222', 'lessons.json'), 'utf8'));
  const out = new Map();
  for (const slug of ['final-paper', 'past-paper-2425']) {
    const lesson = lessons.find((l) => l.slug === slug);
    if (!lesson) throw new Error(`no lesson ${slug}: the paper lessons are where Part B comes from`);
    lesson.blocks.forEach((b, i) => {
      if (b.kind !== 'asprinted') return;
      const worked = lesson.blocks[i + 1];
      if (!worked || worked.kind !== 'worked') throw new Error(`${slug}: ${b.tag} has no model answer`);
      out.set(b.tag, {
        key: b.tag,
        year: YEAR_OF[b.tag.slice(0, 5)],
        number: b.tag.slice(6),
        printed: b.printed,
        src: b.src,
        problem: worked.problem,
        answer: [worked.working, worked.answer].filter(Boolean).join('\n'),
        unpack: '',
      });
    });
  }
  return out;
}

/** The 23/24 and 20/21 questions, from the manual's teaching modules. */
function fromManual() {
  const out = new Map();
  for (const site of paperSites(MANUAL)) {
    const key = `${site.year}:${site.q}:${site.file}`;
    if (!MAN[key]) continue;
    out.set(key, {
      key,
      year: site.year.replace('-', '/'),
      number: qLabel(site.q),
      printed: site.printed,
      src: "the examiner's words, unedited",
      problem: '',
      answer: site.work,
      unpack: site.unpack,
    });
  }
  return out;
}

/** The manual's Break it down box, in the app's own row markup. */
function breakdown(part) {
  if (part.unpack)
    return {
      question:
        '<p>What is this question actually asking, what have you been given, and what do the marks tell you about how much to write? Decide, then check.</p>',
      answer: part.unpack
        .replace(/<div class="urow">/g, '<p class="row">')
        .replace(/<span class="ulab">/g, '<b class="lab">')
        .replace(/<\/span>/g, '</b>')
        .replace(/<\/div>/g, '</p>'),
    };
  return {
    question:
      '<p>Before you write: what are you given, what is actually asked, and what do the marks tell you about the length of the answer?</p>',
    answer:
      '<p class="row"><b class="lab">Work it out first</b> Read the question twice, list what you are given, and say in one line what the answer will look like: a number, a table, a diagram, or a list of points. Then open the answer and mark yourself against it.</p>',
  };
}

function build() {
  const app = fromApp();
  const manual = fromManual();
  const missing = [
    ...Object.keys(APP).filter((k) => !app.has(k)),
    ...Object.keys(MAN).filter((k) => !manual.has(k)),
  ];
  if (missing.length) throw new Error(`these past questions were not found: ${missing.join(', ')}`);

  // Family membership, so every question can name the years it was set in.
  const members = {};
  const all = [];
  for (const [key, [family, topic]] of [...Object.entries(APP), ...Object.entries(MAN)]) {
    const part = app.get(key) ?? manual.get(key);
    const entry = { ...part, family, topic };
    all.push(entry);
    (members[family] ??= []).push(entry);
  }
  for (const list of Object.values(members))
    list.sort((a, b) => b.year.localeCompare(a.year) || a.number.localeCompare(b.number));

  const authored = JSON.parse(readFileSync(join(HERE, 'author', 'ift222_doing.json'), 'utf8'));
  mkdirSync(OUT, { recursive: true });

  for (const [key, meta] of Object.entries(authored)) {
    const topic = Number(key.slice(1));
    const mine = all
      .filter((p) => p.topic === topic)
      .sort((a, b) => b.year.localeCompare(a.year) || a.number.localeCompare(b.number));

    const questions = mine.map((p) => {
      const kin = members[p.family].filter((x) => x !== p);
      const repeat = kin.length
        ? `<p class="flag"><b>This question repeats.</b> The same question, ${FAMILY[
            p.family
          ].toLowerCase()}, was also set in ${kin
            .map((x) => `<b>${x.year} ${x.number}</b>`)
            .join(', ')}. Wording and numbers move; the method does not.</p>`
        : `<p class="flag">Set once, in ${p.year}. It is still the examiner's own question, and the method behind it is on the syllabus.</p>`;
      return {
        heading: `${p.year}, ${p.number}`,
        marks: `${p.year} ${p.number}`,
        scenario: {
          printed: true,
          src: `${p.year}:${p.number}`,
          tag: `${p.year}, Question ${p.number.replace(/^Q/, '')}${kin.length ? `, and in ${kin.length} other paper${kin.length > 1 ? 's' : ''}` : ''}`,
          text: p.printed,
        },
        asked: repeat,
        breakdown: breakdown(p),
        exam: {
          problem:
            p.problem ||
            `<p>Answer <b>${p.year} ${p.number}</b> in full in your book, then open this and mark yourself against it.</p>`,
          // A handful of the older questions are quoted in the manual without a
          // solution beside them, because the manual answers that question under
          // the year it solves in full. Rather than invent one, say where it is.
          answer:
            p.answer ||
            `<p><b>The manual answers this question under its other year.</b> The same question, ${FAMILY[
              p.family
            ].toLowerCase()}, is worked in full at <b>${(kin.find((x) => x.answer) ?? kin[0]).year} ${
              (kin.find((x) => x.answer) ?? kin[0]).number
            }</b>, in this same paper. Read it there, then come back and write this year's wording, which differs only in how many differences it asks for.</p>`,
        },
        frames: [],
      };
    });

    writeFileSync(
      join(OUT, `${key}.json`),
      JSON.stringify({ ...meta, questions }, null, 2) + '\n',
      'utf8'
    );
    console.log(
      `  ${key.padEnd(4)} topic ${String(topic).padStart(2)}: ${String(questions.length).padStart(2)} past questions, ${
        meta.methodFrames?.length ?? 0
      } method frames`
    );
  }
  const years = {};
  for (const p of all) years[p.year] = (years[p.year] ?? 0) + 1;
  console.log(`  ${all.length} past question parts in all: ${Object.entries(years).map(([y, n]) => `${y} ${n}`).join(', ')}`);
  const repeats = Object.entries(members).filter(([, v]) => v.length > 1);
  console.log(`  ${repeats.length} questions the examiner has set more than once, ${repeats.reduce((t, [, v]) => t + v.length, 0)} parts between them`);
}

build();
