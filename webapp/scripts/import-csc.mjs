/**
 * Turn the CSC242 manual into interactive lessons, scoped to the CCODEL text.
 *
 *     node scripts/import-csc.mjs
 *
 * Run BY HAND, not on deploy. Reads the manual's authored HTML from the course
 * folder outside this app and writes data/csc242/lessons.json.
 *
 * SCOPE. The lecturer set this paper by feeding the CCODEL manual to a model,
 * so that manual is the whole examinable universe. It contains exactly twelve
 * modules, and it contains NO graphs, NO trees, NO Boolean algebra, NO posets
 * and NO descriptive statistics, all of which the 466-page manual covers at
 * length. Those files are deliberately not imported: including them would cost
 * a reader hours they do not have.
 *
 * TITLES ARE NOT TRUSTED. The CCODEL document's Module One is headed
 * "Descriptive Statistics" and contains propositional logic; Module Eight's
 * first subsection is headed "What is Mathematical Induction?" and contains
 * inclusion-exclusion; every page header reads "Elementary Differential
 * Equations". The mapping below was built by reading each module's SUBSECTIONS
 * and vocabulary, never its heading.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, '..', '..', 'courses', 'CSC242 - Discrete Structures', 'build', 'content');
const OUTDIR = join(HERE, '..', 'data', 'csc242');
const OUT = join(OUTDIR, 'lessons.json');

const A = 'Part A: logic';
const B = 'Part B: sets and functions';
const C = 'Part C: counting';
const D = 'Part D: proof and recurrence';
const E = 'Part E: prove it';

/** file, then per <section>: slug, part, CCODEL module it teaches, minutes. */
const PARTS = [
  { file: 'front.html', slugs: ['how-to-pass'], part: 'Start here', modules: [[]], minutes: [8] },
  { file: 'foundations.html', slugs: ['notation'], part: 'Start here', modules: [[]], minutes: [14] },
  { file: 'foundations_f2.html', slugs: ['reading-maths'], part: 'Start here', modules: [[]], minutes: [10] },

  { file: 'p1_logic.html', slugs: ['propositions'], part: A, modules: [[1]], minutes: [18] },
  { file: 'p1_12.html', slugs: ['implication'], part: A, modules: [[1]], minutes: [14] },
  { file: 'p1_13.html', slugs: ['equivalence-laws'], part: A, modules: [[1]], minutes: [14] },
  { file: 'p1_14.html', slugs: ['predicates'], part: A, modules: [[2]], minutes: [18] },
  { file: 'p1_15.html', slugs: ['inference'], part: A, modules: [[2]], minutes: [14] },

  { file: 'p2_sets.html', slugs: ['sets'], part: B, modules: [[3]], minutes: [18] },
  { file: 'p2_22.html', slugs: ['set-operations'], part: B, modules: [[3]], minutes: [16] },
  { file: 'p2_23.html', slugs: ['power-sets'], part: B, modules: [[3]], minutes: [14] },
  { file: 'p4_functions.html', slugs: ['functions'], part: B, modules: [[4]], minutes: [14] },
  { file: 'p4_42.html', slugs: ['function-types'], part: B, modules: [[4]], minutes: [14] },
  { file: 'p4_43.html', slugs: ['composition'], part: B, modules: [[4]], minutes: [12] },

  { file: 'p9_93.html', slugs: ['sequences'], part: C, modules: [[5]], minutes: [18] },
  { file: 'p5_counting.html', slugs: ['counting-rules'], part: C, modules: [[9]], minutes: [18] },
  { file: 'p5_52.html', slugs: ['permutations'], part: C, modules: [[9]], minutes: [18] },
  { file: 'p5_53.html', slugs: ['inclusion-exclusion'], part: C, modules: [[8]], minutes: [18] },
  { file: 'p5_54.html', slugs: ['binomial'], part: C, modules: [[10]], minutes: [14] },
  { file: 'p10_102.html', slugs: ['probability'], part: C, modules: [[11]], minutes: [18] },

  { file: 'p9_proof.html', slugs: ['proof'], part: D, modules: [[6]], minutes: [22] },
  { file: 'p9_92.html', slugs: ['induction'], part: D, modules: [[7]], minutes: [18] },
  { file: 'p9_94.html', slugs: ['recurrence'], part: D, modules: [[12]], minutes: [18] },

  { file: 'reference_r3.html', slugs: ['cram'], part: E, modules: [[]], minutes: [10] },
  { file: 'papers.html', slugs: ['paper-2526'], part: E, modules: [[]], minutes: [90] },
  { file: 'paper_2425.html', slugs: ['paper-2425'], part: E, modules: [[]], minutes: [90] },
];

const VOID = new Set(['hr', 'br', 'img', 'input', 'meta', 'link', 'col', 'source']);

function nodes(html) {
  const out = [];
  let i = 0;
  while (i < html.length) {
    const lt = html.indexOf('<', i);
    if (lt === -1) break;
    if (html.startsWith('<!--', lt)) {
      i = html.indexOf('-->', lt) + 3;
      continue;
    }
    const gt = html.indexOf('>', lt);
    if (gt === -1) break;
    const open = html.slice(lt, gt + 1);
    const tag = (open.match(/^<\s*([a-zA-Z][\w-]*)/) ?? [])[1];
    if (!tag) {
      i = gt + 1;
      continue;
    }
    if (VOID.has(tag.toLowerCase()) || open.endsWith('/>')) {
      out.push({ tag, attrs: open, inner: '', raw: open });
      i = gt + 1;
      continue;
    }
    let depth = 1;
    let scan = gt + 1;
    const openRe = new RegExp(`<\\s*${tag}(\\s|>|/)`, 'gi');
    const closeRe = new RegExp(`</\\s*${tag}\\s*>`, 'gi');
    let end = -1;
    while (depth > 0) {
      closeRe.lastIndex = scan;
      const c = closeRe.exec(html);
      if (!c) break;
      openRe.lastIndex = scan;
      let o = openRe.exec(html);
      while (o && o.index < c.index) {
        depth += 1;
        openRe.lastIndex = o.index + 1;
        o = openRe.exec(html);
      }
      depth -= 1;
      scan = c.index + c[0].length;
      if (depth === 0) end = c.index;
    }
    if (end === -1) {
      out.push({ tag, attrs: open, inner: html.slice(gt + 1), raw: html.slice(lt) });
      break;
    }
    out.push({ tag, attrs: open, inner: html.slice(gt + 1, end), raw: html.slice(lt, scan) });
    i = scan;
  }
  return out;
}

const cls = (n) => ((n.attrs.match(/class="([^"]*)"/) ?? [])[1] ?? '').trim();
const has = (n, c) => cls(n).split(/\s+/).includes(c);
const text = (h) =>
  h.replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();

function barOf(inner) {
  const bar = nodes(inner).find((n) => has(n, 'bar'));
  if (!bar) return { label: '', tag: '', rest: inner };
  const spans = nodes(bar.inner).filter((n) => n.tag === 'span');
  return {
    label: text(spans[0]?.inner ?? ''),
    tag: text(spans.find((s) => has(s, 'tag'))?.inner ?? ''),
    rest: inner.replace(bar.raw, ''),
  };
}

const bodyOf = (rest) => {
  const b = nodes(rest).find((n) => has(n, 'body'));
  return (b ? b.inner : rest).trim();
};

function toBlock(node) {
  const c = cls(node);
  const { label, tag, rest } = barOf(node.inner);
  const body = bodyOf(rest);

  if (c.includes('box prog')) {
    const howto = nodes(body).find((n) => has(n, 'howto'));
    const frames = nodes(body)
      .filter((n) => has(n, 'fr'))
      .map((fr) => {
        const p = nodes(fr.inner).find((n) => n.tag === 'p') ?? { inner: fr.inner };
        const chk = nodes(p.inner).find((n) => has(n, 'chk'));
        const ask = nodes(p.inner).find((n) => has(n, 'ask'));
        let teach = p.inner;
        if (chk) teach = teach.replace(chk.raw, '');
        if (ask) teach = teach.replace(ask.raw, '');
        return {
          check: chk ? text(chk.inner) : '',
          teach: teach.trim(),
          ask: ask ? text(ask.inner) : '',
        };
      });
    if (frames.length >= 2) {
      if (frames[frames.length - 1].ask) frames[frames.length - 1].ask = '';
      return {
        kind: 'frames',
        label: label || 'Work it frame by frame',
        tag: tag || 'cover, work, then slide down',
        howto: howto ? text(howto.inner) : 'Cover the page, read a frame, do the task, then slide down to check.',
        frames,
      };
    }
  }
  if (c.includes('box paper') || c.includes('box qpaper')) {
    const ap = nodes(body).find((n) => has(n, 'asprinted'));
    return {
      kind: 'asprinted',
      label: label || 'As printed',
      tag: tag || "the examiner's words",
      src: (node.inner.match(/data-src="([^"]+)"/) ?? [])[1] ?? '',
      printed: ap ? `<pre>${ap.inner.trim()}</pre>` : `<pre>${body}</pre>`,
    };
  }
  if (c.includes('box work') || c.includes('box ans') || c.includes('box unpack') || c.includes('box calc')) {
    const answer = nodes(body).find((n) => has(n, 'answerbox'));
    const redo = nodes(body).find((n) => has(n, 'redo'));
    let working = body;
    if (answer) working = working.replace(answer.raw, '');
    if (redo) working = working.replace(redo.raw, '');
    return {
      kind: 'worked',
      mode: 'model',
      label: label || 'Worked',
      tag: tag || 'cover it, try it, then check',
      problem: '',
      working: working.trim() || '<p>See the answer.</p>',
      answer: answer ? answer.inner.trim() : 'Work the steps above.',
      redo: redo ? text(redo.inner) : '',
    };
  }
  if (c.includes('box recall')) {
    const answer = nodes(body).find((n) => has(n, 'answerbox'));
    return {
      kind: 'recall',
      label: label || 'Your turn',
      tag: tag || 'answer before you look',
      question: answer ? body.replace(answer.raw, '').trim() : body,
      answer: answer ? answer.inner.trim() : 'See the section above.',
    };
  }
  if (c.includes('box trap')) return { kind: 'trap', label: label || 'Trap', tag, html: body };
  if (c.includes('box mem') || c.includes('box key') || c.includes('box code'))
    return { kind: 'rules', label: label || 'Must memorise', tag: tag || 'learn this', html: body };
  if (c.includes('box teach')) return { kind: 'teach', label: label || 'Teach', tag, html: body };
  // ANY other box still carries teaching, and dropping it loses that teaching
  // silently. A sampling check found several lessons had lost most of their
  // content this way, and one past-paper lesson had lost all of it. So an
  // unrecognised box becomes a plain teach block rather than nothing.
  if (/\bbox\b/.test(c))
    return { kind: 'teach', label: label || '', tag, html: body || node.inner };
  if (c.includes('lockin'))
    return {
      kind: 'lockin',
      big: text(nodes(node.inner).find((n) => has(n, 'big'))?.inner ?? label ?? ''),
      sub: text(nodes(node.inner).find((n) => has(n, 'sub'))?.inner ?? ''),
    };
  return null;
}

function convert(file, spec) {
  const html = readFileSync(join(SRC, file), 'utf8');
  // Several files open with a PART DIVIDER: a section carrying the part name
  // and a motif, but no heading and no teaching. Only sections with a title are
  // lessons, and skipping the rest keeps the slug list aligned with reality.
  const sections = nodes(html)
    .filter((n) => n.tag === 'section')
    .filter((n) => /<h2[^>]*class="title"/.test(n.inner));
  const out = [];

  sections.forEach((sec, i) => {
    if (!spec.slugs[i]) return; // a file with more sections than we want
    const top = nodes(sec.inner);
    const title = text(top.find((n) => n.tag === 'h2')?.inner ?? '') || spec.slugs[i];
    const kick = text(top.find((n) => has(n, 'kick'))?.inner ?? '') || 'Skill';
    const lead = (top.find((n) => has(n, 'lead'))?.inner ?? '').trim();

    const blocks = [];
    for (const n of top) {
      if (n.tag === 'h2' || has(n, 'kick') || has(n, 'lead') || has(n, 'part')) continue;
      if (n.tag === 'hr') continue;
      if (n.tag === 'h3') {
        blocks.push({ kind: 'heading', text: text(n.inner) });
        continue;
      }
      const b = toBlock(n);
      if (b) blocks.push(b);
      // Nothing with real text is thrown away. Whatever the manual put here,
      // the reader gets: dropping an unrecognised element loses teaching, and
      // an odd-looking block is far better than a missing one.
      else if (text(n.inner).length > 20) blocks.push({ kind: 'prose', html: n.raw });
    }

    out.push({
      slug: spec.slugs[i],
      part: spec.part,
      kick,
      title,
      lead: lead || `<p>${title}, taught from the manual, one idea at a time.</p>`,
      minutes: spec.minutes[i],
      modules: spec.modules[i],
      blocks,
    });
  });
  return out;
}

if (!existsSync(OUTDIR)) mkdirSync(OUTDIR, { recursive: true });

const lessons = PARTS.flatMap((spec) => convert(spec.file, spec));
writeFileSync(OUT, JSON.stringify(lessons, null, 2) + '\n', 'utf8');

console.log(`wrote ${lessons.length} lessons -> ${OUT}`);
let frames = 0;
let worked = 0;
for (const l of lessons) {
  const kinds = {};
  for (const b of l.blocks) kinds[b.kind] = (kinds[b.kind] ?? 0) + 1;
  frames += (kinds.frames ?? 0);
  worked += (kinds.worked ?? 0);
  console.log(
    `  ${l.slug.padEnd(20)} M${JSON.stringify(l.modules).padEnd(5)} ${String(l.blocks.length).padStart(3)} blocks  ${Object.entries(kinds).map(([k, v]) => `${k}:${v}`).join(' ')}`
  );
}
console.log(`\ntotal: ${lessons.reduce((t, l) => t + l.blocks.length, 0)} blocks, ${frames} frame blocks, ${worked} worked`);
