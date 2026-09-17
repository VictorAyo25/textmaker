/**
 * Turn the IFT222 crash manual into interactive lessons.
 *
 *     node scripts/import-crash.mjs
 *
 * Run BY HAND, not on deploy. It reads the crash course's authored HTML from the
 * course folder outside this app and writes data/ift222/lessons.json, which is
 * committed. Vercel only ever builds `webapp/`, so nothing here runs there.
 *
 * WHY A CONVERTER AND NOT RETYPING. The teaching text has already been written,
 * house-styled, numerically verified and gated in the manual build. Retyping it
 * would put every one of those checks at risk for no gain. This lifts it
 * verbatim and only restructures it, so the words a reader sees on screen are
 * the words the gates passed.
 *
 * WHAT INTERACTIVE MEANS HERE. The manual's programmed frames say "cover the
 * page with a card and slide it down". On paper the reader has to be honest; on
 * screen the app holds the card. Each frame is revealed one at a time, the check
 * that answers it stays hidden until asked for, worked examples hide their
 * working, and every "Your turn" hides its answer behind a self-mark. That is
 * the whole point of the port: the discipline the print edition can only ask
 * for, the screen can enforce.
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { balanceBlock } from './lib/html-balance.mjs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const CRASH = join(
  HERE,
  '..',
  '..',
  'courses',
  'IFT222 - Computer Architecture and Organisation',
  'crash',
  'content'
);
const OUT = join(HERE, '..', 'data', 'ift222', 'lessons.json');

// Source file, slug, the drill topics the skill maps onto, and a rough sitting
// time. Order is the manual's own BODY_PARTS order, minus mcq_bank.html, whose
// 120 questions are already the drill.
const PARTS = [
  { file: 'front.html', slug: 'plan', part: 'Start here', modules: [], minutes: 6 },
  { file: 'skill_bigpicture.html', slug: 'big-picture', part: 'Part A: foundations and data', modules: [1, 2, 10], minutes: 22 },
  { file: 'skill_numbers.html', slug: 'numbers', part: 'Part A: foundations and data', modules: [3], minutes: 18 },
  { file: 'skill_signed.html', slug: 'signed', part: 'Part A: foundations and data', modules: [4], minutes: 20 },
  { file: 'skill_ieee.html', slug: 'ieee', part: 'Part A: foundations and data', modules: [5], minutes: 18 },
  { file: 'skill_image.html', slug: 'image', part: 'Part A: foundations and data', modules: [10, 8], minutes: 10 },
  { file: 'skill_instr.html', slug: 'instructions', part: 'Part B: the machine', modules: [6, 2], minutes: 18 },
  { file: 'skill_addr.html', slug: 'addressing', part: 'Part B: the machine', modules: [7], minutes: 15 },
  { file: 'skill_perf.html', slug: 'performance', part: 'Part B: the machine', modules: [9], minutes: 14 },
  { file: 'skill_pipeline.html', slug: 'pipelining', part: 'Part B: the machine', modules: [9], minutes: 15 },
  { file: 'skill_memory.html', slug: 'memory', part: 'Part B: the machine', modules: [8], minutes: 20 },
  { file: 'skill_riscisc.html', slug: 'risc-cisc', part: 'Part C: prove it', modules: [9, 10], minutes: 12 },
  { file: 'final_2526.html', slug: 'final-paper', part: 'Part C: prove it', modules: [], minutes: 120 },
  { file: 'cram.html', slug: 'night-before', part: 'Part C: prove it', modules: [], minutes: 8 },
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
    // Find the matching close, counting nested opens of the same tag.
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
    out.push({
      tag,
      attrs: open,
      inner: html.slice(gt + 1, end),
      raw: html.slice(lt, scan),
    });
    i = scan;
  }
  return out;
}

const cls = (n) => ((n.attrs.match(/class="([^"]*)"/) ?? [])[1] ?? '').trim();
const has = (n, c) => cls(n).split(/\s+/).includes(c);
const text = (h) =>
  h
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
const tidy = (h) => h.replace(/^\s+|\s+$/g, '');

/** The bar of a box carries its label and an optional tag. */
function barOf(body) {
  const bar = body.find((n) => has(n, 'bar'));
  if (!bar) return { label: '', tag: '' };
  const spans = nodes(bar.inner).filter((s) => s.tag === 'span');
  return {
    label: text(spans[0]?.inner ?? ''),
    tag: text(spans.find((s) => has(s, 'tag'))?.inner ?? ''),
  };
}

const bodyOf = (box) => nodes(box.inner).find((n) => has(n, 'body'));

/** A programmed frame: the check that answers the frame before it, the teaching
 *  text, and the question it leaves you with. */
function frameParts(fr) {
  let inner = fr.inner.trim();
  const p = nodes(inner).find((n) => n.tag === 'p');
  if (p) inner = p.inner;
  let check = '';
  let ask = '';
  const chk = inner.match(/<span class="chk">([\s\S]*?)<\/span>/);
  if (chk && inner.trim().startsWith('<span class="chk">')) {
    check = tidy(chk[1]);
    inner = inner.replace(chk[0], '');
  }
  const askM = inner.match(/<span class="ask">([\s\S]*?)<\/span>/);
  if (askM) {
    ask = tidy(askM[1]);
    inner = inner.replace(askM[0], '');
  }
  return { check, teach: tidy(inner), ask };
}

const unknown = [];

function convertBox(box, lesson) {
  const kind = cls(box).replace('box', '').trim();
  const bodyNode = bodyOf(box);
  const children = nodes(box.inner);
  const { label, tag } = barOf(children);
  const body = bodyNode ? nodes(bodyNode.inner) : [];

  if (kind === 'prog') {
    const howto = body.find((n) => has(n, 'howto'));
    const frames = body.filter((n) => has(n, 'fr')).map(frameParts);
    return { kind: 'frames', label, tag, howto: howto ? tidy(howto.inner) : '', frames };
  }

  if (kind === 'work') {
    const cut = body.findIndex(
      (n) =>
        (n.tag === 'pre' && has(n, 'calc')) ||
        (n.tag === 'ol' && has(n, 'steps')) ||
        has(n, 'params')
    );
    const ansIdx = body.findIndex((n) => has(n, 'answerbox'));
    const redo = body.find((n) => has(n, 'redo'));
    const upto = cut === -1 ? (ansIdx === -1 ? body.length : ansIdx) : cut;
    const problem = body.slice(0, upto).map((n) => n.raw).join('\n');
    const working = body
      .slice(upto, ansIdx === -1 ? body.length : ansIdx)
      .map((n) => n.raw)
      .join('\n');
    const answer = ansIdx === -1 ? '' : tidy(body[ansIdx].inner);
    const block = {
      kind: 'worked',
      // 'model' is a full exam answer sitting under the question as printed, so
      // the whole thing hides. 'example' states a problem, then hides only the
      // working, which is what a worked example is for.
      mode: label === 'In the hall' ? 'model' : 'example',
      label,
      tag,
      problem: tidy(problem),
      working: tidy(working),
      answer,
      redo: redo ? tidy(redo.inner) : '',
    };
    if (block.mode === 'model' || (!block.working && !block.answer)) {
      block.working = [block.problem, block.working].filter(Boolean).join('\n');
      block.problem = '';
    }
    return block;
  }

  if (kind === 'recall') {
    const cutIdx = body.findIndex((n) => n.tag === 'hr' && has(n, 'cut'));
    const q = body.slice(0, cutIdx === -1 ? body.length : cutIdx);
    const a = body
      .slice(cutIdx === -1 ? body.length : cutIdx + 1)
      .filter((n) => !has(n, 'alabel'));
    return {
      kind: 'recall',
      label,
      tag,
      question: tidy(q.map((n) => n.raw).join('\n')),
      answer: tidy(a.map((n) => n.raw).join('\n')),
    };
  }

  if (kind === 'paper') {
    const src = body.find((n) => has(n, 'src'));
    const printed = body.find((n) => has(n, 'asprinted'));
    return {
      kind: 'asprinted',
      label,
      tag,
      src: src ? text(src.inner) : '',
      printed: printed ? printed.inner : tidy(bodyNode?.inner ?? ''),
    };
  }

  // mem, trap, teach and anything else: keep the body exactly as authored.
  return {
    kind: kind === 'mem' ? 'rules' : kind === 'trap' ? 'trap' : 'teach',
    label,
    tag,
    html: tidy(bodyNode?.inner ?? box.inner),
  };
}

function convert(part) {
  const file = join(CRASH, part.file);
  if (!existsSync(file)) throw new Error(`missing ${file}`);
  const raw = readFileSync(file, 'utf8');
  const section = nodes(raw).find((n) => n.tag === 'section');
  const top = nodes(section ? section.inner : raw);

  const lesson = {
    slug: part.slug,
    part: part.part,
    kick: '',
    title: '',
    lead: '',
    minutes: part.minutes,
    modules: part.modules,
    blocks: [],
  };

  for (const n of top) {
    if (has(n, 'kick')) {
      lesson.kick = text(n.inner);
    } else if (n.tag === 'h2' && has(n, 'title')) {
      lesson.title = text(n.inner);
    } else if (n.tag === 'hr') {
      // the rule under the title, and section dividers: presentation only
    } else if (has(n, 'lead') && !lesson.lead) {
      lesson.lead = tidy(n.inner);
    } else if (n.tag === 'h3') {
      lesson.blocks.push({ kind: 'heading', text: text(n.inner) });
    } else if (has(n, 'lockin')) {
      const parts = nodes(n.inner);
      lesson.blocks.push({
        kind: 'lockin',
        big: tidy(parts.find((p) => has(p, 'big'))?.inner ?? ''),
        sub: tidy(parts.find((p) => has(p, 'sub'))?.inner ?? ''),
      });
    } else if (has(n, 'box')) {
      // Balanced as it is stored: a worked box split into problem and working
      // can leave one half with a div open and the other with a stray close,
      // which the browser repairs differently from the server. See
      // lib/html-balance.mjs.
      lesson.blocks.push(balanceBlock(convertBox(n, lesson)));
    } else if (['p', 'figure', 'table', 'ul', 'ol', 'pre', 'div'].includes(n.tag)) {
      if (text(n.inner) || n.inner.includes('<svg'))
        lesson.blocks.push({ kind: 'prose', html: tidy(n.raw) });
    } else {
      unknown.push(`${part.file}: <${n.tag} class="${cls(n)}">`);
    }
  }
  return lesson;
}

const lessons = PARTS.map(convert);

// ---- report, so a silent drop cannot hide ----
let frames = 0;
let recalls = 0;
let worked = 0;
for (const l of lessons) {
  const c = {};
  for (const b of l.blocks) c[b.kind] = (c[b.kind] ?? 0) + 1;
  frames += l.blocks.filter((b) => b.kind === 'frames').reduce((t, b) => t + b.frames.length, 0);
  recalls += c.recall ?? 0;
  worked += c.worked ?? 0;
  console.log(
    `  ${l.slug.padEnd(13)} ${String(l.blocks.length).padStart(3)} blocks  ${Object.entries(c)
      .map(([k, v]) => `${k} ${v}`)
      .join(', ')}`
  );
  if (!l.title) console.error(`  x ${l.slug}: no title`);
}
console.log(
  `\n  ${lessons.length} lessons, ${frames} programmed frames, ${worked} worked examples, ${recalls} recall exercises`
);
if (unknown.length) {
  console.error('\n  UNRECOGNISED NODES (these would be dropped):');
  for (const u of [...new Set(unknown)]) console.error('    ' + u);
  process.exit(1);
}

writeFileSync(OUT, JSON.stringify(lessons, null, 1));
console.log(`\n  wrote ${OUT}`);
