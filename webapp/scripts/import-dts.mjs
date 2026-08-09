/**
 * Turn the DTS224 manual into interactive lessons.
 *
 *     node scripts/import-dts.mjs
 *
 * Run BY HAND, not on deploy. It reads the manual's authored HTML from the
 * course folder outside this app and writes data/dts224/lessons.json, which is
 * committed. Vercel only ever builds `webapp/`, so nothing here runs there.
 *
 * WHY A CONVERTER AND NOT RETYPING. The teaching has already been written,
 * house-styled, checked against the CCODEL manual and gated in the manual
 * build, including its coverage gate that refuses to pass while any question in
 * any source is unsolved. Retyping it would put every one of those checks at
 * risk for no gain. This lifts it verbatim and only restructures it.
 *
 * Each <section> in the manual becomes one lesson, because the manual's own
 * sections are already the natural sittings: one idea each, in teaching order.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, '..', '..', 'courses', 'DTS224 - Data Management I', 'build', 'content');
const OUTDIR = join(HERE, '..', 'data', 'dts224');
const OUT = join(OUTDIR, 'lessons.json');

/**
 * Source file, and for each <section> inside it: slug, part, the drill topics
 * it teaches, and a sitting time. Order is the manual's own reading order.
 */
const PARTS = [
  { file: 'front.html', slugs: ['how-to-pass'], part: 'Start here', modules: [[]], minutes: [8] },
  {
    file: 'module1.html',
    slugs: ['foundations', 'architecture'],
    part: 'Part A: what a database is',
    modules: [[1], [2]],
    minutes: [18, 18],
  },
  {
    file: 'module2.html',
    slugs: ['er-model', 'eer-model'],
    part: 'Part B: modelling',
    modules: [[3], [4]],
    minutes: [26, 20],
  },
  {
    file: 'module2_unit34.html',
    slugs: ['xml-json', 'worked-models'],
    part: 'Part B: modelling',
    modules: [[5], [3]],
    minutes: [12, 16],
  },
  {
    file: 'module3.html',
    slugs: ['relational-model', 'logical-design'],
    part: 'Part C: the relational model',
    modules: [[6], [7]],
    minutes: [22, 18],
  },
  {
    file: 'module4.html',
    slugs: ['normalization'],
    part: 'Part C: the relational model',
    modules: [[8]],
    minutes: [26],
  },
  {
    file: 'module5.html',
    slugs: ['relational-algebra'],
    part: 'Part D: asking questions of it',
    modules: [[9]],
    minutes: [20],
  },
  {
    file: 'module5_sql.html',
    slugs: ['sql'],
    part: 'Part D: asking questions of it',
    modules: [[10]],
    minutes: [24],
  },
  {
    file: 'paper2526.html',
    slugs: ['paper-2526-a', 'paper-2526-b'],
    part: 'Part E: prove it',
    modules: [[], []],
    minutes: [60, 60],
  },
];

const VOID = new Set(['hr', 'br', 'img', 'input', 'meta', 'link', 'col', 'source']);

/** Walk a fragment and yield its top-level elements, in order. */
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

/** A box's bar carries its label and an optional tag chip. */
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

/** One manual box becomes one lesson block. */
function toBlock(node) {
  const c = cls(node);
  const { label, tag, rest } = barOf(node.inner);
  const body = bodyOf(rest);

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
  if (c.includes('box work') || c.includes('box ans') || c.includes('box unpack')) {
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
  if (c.includes('box trap')) {
    return { kind: 'trap', label: label || 'Trap', tag, html: body };
  }
  if (c.includes('box mem') || c.includes('box code')) {
    return { kind: 'rules', label: label || 'Must memorise', tag: tag || 'learn this', html: body };
  }
  if (c.includes('box teach')) {
    return { kind: 'teach', label: label || 'Teach', tag, html: body };
  }
  return null;
}

/** Split one file into its sections and convert each. */
function convert(file, spec) {
  const html = readFileSync(join(SRC, file), 'utf8');
  const sections = nodes(html).filter((n) => n.tag === 'section');
  const out = [];

  sections.forEach((sec, i) => {
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
      else if (n.tag === 'p' && text(n.inner).length > 30)
        blocks.push({ kind: 'prose', html: n.raw });
      else if (n.tag === 'table' || n.tag === 'ol' || n.tag === 'ul' || n.tag === 'figure')
        blocks.push({ kind: 'prose', html: n.raw });
    }

    out.push({
      slug: spec.slugs[i],
      part: spec.part,
      kick,
      title,
      lead:
        lead ||
        `<p>${title}, taught from the manual, one idea at a time.</p>`,
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
for (const l of lessons) {
  const kinds = {};
  for (const b of l.blocks) kinds[b.kind] = (kinds[b.kind] ?? 0) + 1;
  console.log(
    `  ${l.slug.padEnd(20)} topics ${JSON.stringify(l.modules).padEnd(6)} ${l.blocks.length
      .toString()
      .padStart(3)} blocks  ${Object.entries(kinds)
      .map(([k, v]) => `${k}:${v}`)
      .join(' ')}`
  );
}
