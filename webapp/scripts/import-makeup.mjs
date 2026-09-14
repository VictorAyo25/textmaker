/**
 * Bring a MAKEUP crash course onto the drill: its lessons, its past theory
 * questions, and its objective questions.
 *
 *     node scripts/import-makeup.mjs COS221
 *     node scripts/import-makeup.mjs CSC241
 *
 * Run BY HAND, not on deploy, exactly like import-crash.mjs. It reads authored
 * HTML from the course folder outside this app and writes committed JSON under
 * data/<code>/. Vercel only ever builds webapp/, so nothing here runs there.
 *
 * WHY THIS IS NOT import-crash.mjs WITH A FLAG. The makeup lessons carry code.
 * A Java or Python frame is a paragraph, then a listing, then the output that
 * listing actually printed, then the question. The original importer keeps only
 * the first paragraph of a frame, which is right for IFT222's one-sentence
 * frames and would silently delete every listing here. Frames are therefore
 * kept WHOLE, and LessonView renders a frame with block content in a div
 * rather than a paragraph, since a <pre> inside a <p> is invalid HTML that the
 * browser would break apart on a server render.
 *
 * THREE THINGS COME OUT, and none of it is retyped:
 *
 *   lessons.json     the crash course, frame by frame, from the makeup build
 *                    whose code gate compiled or ran every listing; then one
 *                    lesson per past paper, where each question is printed as
 *                    the examiner set it, the break-down hides behind a self
 *                    mark, and the model answer hides until you have written
 *                    your own in your book.
 *   objective.json   the objective questions from the study manual, with the
 *                    verdict on every option carried across, so review can say
 *                    why each wrong option is wrong.
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const COURSES_DIR = join(HERE, '..', '..', 'courses');
const DATA = join(HERE, '..', 'data');

// ---------------------------------------------------------------- per course

const CONFIG = {
  COS221: {
    dir: 'cos221',
    folder: 'COS221 - Computer Programming I (Java)',
    crash: 'makeup/content_crash',
    manual: 'build/content',
    // slug, file, topics, minutes. The drill for a topic goes at the END of
    // the last lesson that teaches it, so a question is asked exactly once.
    lessons: [
      ['first-program', 'l1_1_first.html', [1], 18],
      ['what-java-is', 'l1_2_java.html', [1], 12],
      ['types', 'l1_3_types.html', [2], 22],
      ['operators', 'l1_4_operators.html', [2], 22],
      ['input-output', 'l1_5_io.html', [2], 18],
      ['dry-run', 'l1_6_dryrun.html', [3], 22],
      ['if-ladder', 'l2_1_if.html', [3], 20],
      ['switch', 'l2_2_switch.html', [3], 16],
      ['loops', 'l2_3_loops.html', [3], 20],
      ['for-to-while', 'l2_4_convert.html', [3], 14],
      ['break-continue', 'l2_5_break.html', [3], 16],
      ['methods', 'l2_6_methods.html', [4], 20],
      ['overloading', 'l2_7_overload.html', [4], 16],
      ['arrays', 'l2_8_arrays.html', [7], 24],
      ['strings', 'l2_9_strings.html', [6], 20],
      ['classes', 'l3_1_classes.html', [5], 20],
      ['encapsulation', 'l3_2_encap.html', [5], 16],
      ['inheritance', 'l3_3_inherit.html', [5], 20],
      ['polymorphism', 'l3_4_poly.html', [5], 16],
      ['recursion', 'l3_5_recursion.html', [8], 16],
      ['exceptions', 'l3_6_exceptions.html', [9], 18],
      ['files', 'l3_7_files.html', [9], 18],
    ],
    // [slug, title, files]: every past paper, as theory to answer in your book
    theory: [
      ['paper-2526', 'The 2025/2026 Paper, Every Question', ['sol_2526_a.html', 'sol_2526_b.html', 'sol_2526_c.html']],
      ['paper-2425', 'The 2024/2025 Paper, Every Question', ['sol_2425_a.html', 'sol_2425_b.html', 'sol_2425_c.html']],
    ],
    reference: ['reference', 'The Reference Card', 'content_crash/d4_reference.html'],
    // [slug, title, question files, answer files]: practice papers, sat in the book
    mocks: [
      ['mock-b', 'Mock Paper B, in the Current Shape', ['mock_b.html'], ['mock_b_sol.html']],
      ['mock-a', 'Mock Paper A, in the Older Shape', ['mock_a.html'], ['mock_a_sol.html']],
    ],
    // Each topic's drill sits at the end of the last lesson of that topic that
    // the dated plan actually has you read. Put it on an optional lesson and a
    // reader who is short of time loses the questions along with the lesson.
    drillAt: { 1: 'what-java-is', 2: 'input-output', 3: 'for-to-while', 4: 'methods', 5: 'polymorphism',
               6: 'strings', 7: 'arrays', 8: 'recursion', 9: 'files' },
    objective: 'objective.html',
    // the objective sections, in order, become the drill topics
    topicOf: (title) =>
      ({
        'The Language, the Toolchain and Objects': 1,
        'Types, Operators, Input and Output': 2,
        'Control Structures': 3,
        Methods: 4,
        'Object-Oriented Programming': 5,
        Strings: 6,
        Arrays: 7,
        Recursion: 8,
        'Exceptions and File Input and Output': 9,
      })[title],
    idPrefix: 'cos',
  },
  CSC241: {
    dir: 'csc241',
    folder: 'CSC241 - Python Programming Language I',
    crash: 'makeup/content_crash',
    manual: 'build/content',
    lessons: [
      ['how-python-runs', 'l1_1_running.html', [1], 16],
      ['types', 'l1_2_types.html', [2], 18],
      ['operators', 'l1_3_operators.html', [2], 20],
      ['strings', 'l1_4_strings.html', [2], 24],
      ['finding-errors', 'l1_5_errors.html', [2], 20],
      ['decisions', 'l2_1_decisions.html', [3], 18],
      ['loops', 'l2_2_loops.html', [3], 20],
      ['lists-tuples', 'l2_3_lists.html', [3], 20],
      ['sets-dicts', 'l2_4_sets.html', [3], 22],
      ['functions', 'l3_1_functions.html', [4], 22],
      ['modules', 'l3_2_modules.html', [4], 14],
      ['files', 'l3_3_files.html', [4], 22],
      ['exceptions', 'l3_4_exceptions.html', [4], 16],
      ['databases', 'l3_5_databases.html', [5], 26],
      ['gui', 'l3_6_gui.html', [5], 14],
    ],
    theory: [['paper-2526', 'The 2025/2026 Paper, Every Question', ['paper2526.html']]],
    reference: ['reference', 'The Reference Card and Cram Sheet', 'content_crash/d4_reference.html'],
    mocks: [
      ['mock-1', 'Mock Paper One', ['mock1.html'], ['mock1_answers.html']],
      ['mock-2', 'Mock Paper Two', ['mock2.html'], ['mock2_answers.html']],
      ['mock-3', 'Mock Paper Three', ['mock3.html'], ['mock3_answers.html']],
    ],
    drillAt: { 1: 'how-python-runs', 2: 'finding-errors', 3: 'lists-tuples', 4: 'files', 5: 'databases' },
    objective: 'objective.html',
    topicOf: (title) =>
      ({
        'Introduction to Python Programming': 1,
        'Python Basics, Syntax, Operators and Strings': 2,
        'Control Flow, Lists, Tuples, Sets and Dictionaries': 3,
        'Functions, Modules, Files and Exceptions': 4,
        'Databases and GUI Development': 5,
      })[title],
    idPrefix: 'csc',
  },
  // INS224's lessons and bank were put on the platform earlier and are not
  // rebuilt here. Only its two past papers come in, from the shipped manual,
  // which quotes both verbatim and answers every part. They are MERGED into the
  // existing lessons file, replacing any earlier copy, so a re-run is harmless.
  INS224: {
    dir: 'ins224',
    folder: 'INS224 - Systems Analysis and Design',
    manual: 'build/content',
    theoryOnly: true,
    theory: [
      ['paper-2526', 'The 2025/2026 Paper, Every Question', ['paper2526.html']],
      ['paper-2425', 'The 2024/2025 Paper, Every Question', ['paper2425.html']],
    ],
    // The format changed after both papers were set. Saying so here stops a
    // reader from practising the choice of questions they will not be given.
    theoryLead:
      'Every question on this paper, quoted exactly as the examiner set it. <b>Your paper is not in this format:</b> it is an objective section, then THREE written questions with no choice, one from each module of the course text. So do not practise choosing. Answer every question here, because each one is a question on one of those three modules. For each: read it, write or draw your full answer in your book, and only then open the model answer.',
    insertBefore: 'cram',
    // Six questions a paper, answered in outline: the list points in full and
    // each diagram sketched, which is what three hours on Wednesday morning allow.
    theoryMinutes: 60,
    mocks: [
      ['mock-1', 'Mock Paper One', ['mock1.html'], []],
      ['mock-2', 'Mock Paper Two', ['mock2.html'], []],
      ['mock-3', 'Mock Paper Three', ['mock3.html'], []],
    ],
    // written before the format changed, like both past papers
    mockLead:
      'Six practice questions in the older shape of the paper. <b>Your paper is three written questions with no choice, one from each module</b>, so answer all six here: each one is practice on one module. Write or draw your answer in your book first, then open the model answer.',
  },
  // IFT222's lessons come from import-crash.mjs; only its three mock papers are
  // brought in here, merged in before the last-hour sheet.
  IFT222: {
    dir: 'ift222',
    folder: 'IFT222 - Computer Architecture and Organisation',
    manual: 'build/content',
    theoryOnly: true,
    theory: [],
    insertBefore: 'night-before',
    mocks: [
      ['mock-1', 'Mock Paper One', ['mock1.html'], ['mock1_answers.html']],
      ['mock-2', 'Mock Paper Two', ['mock2.html'], ['mock2_answers.html']],
      ['mock-3', 'Mock Paper Three', ['mock3.html'], ['mock3_answers.html']],
    ],
  },
};

// ---------------------------------------------------------------- the parser

const VOID = new Set(['hr', 'br', 'img', 'input', 'meta', 'link', 'col', 'source']);

/** Walk a fragment and return its top-level elements, in order. */
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
  h
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/&middot;/g, '·')
    .replace(/&amp;/g, '&')
    .replace(/&#8217;/g, '’')
    .replace(/\s+/g, ' ')
    .trim();
/**
 * The Java manual marks a listing <pre class="src">. On this platform `.src`
 * already means something else: the small uppercase "the examiner's words"
 * label under a quoted question. Left alone, every Java listing would render
 * shrunken and in capitals. So listings are renamed on the way in, and the
 * platform styles `.jsrc` as code with line numbers.
 */
const tidy = (h) =>
  supCaret(h.replace(/^\s+|\s+$/g, '').replace(/<pre class="src\b/g, '<pre class="jsrc'));

/**
 * A caret written as an exponent, "digits^3", reaches the reader as a literal
 * caret. In prose it becomes a real superscript. Inside code, <pre> or <code>,
 * a caret is MEANT literally: a Java comment arrow pointing at a word, or the
 * lesson quoting the paper's "H^2" to warn that Python's power operator is **.
 * Rewriting those would change what the lesson says, so there the caret is
 * written as its character reference, which renders as the very same caret.
 */
function supCaret(html) {
  return html
    .split(/(<pre[\s\S]*?<\/pre>|<code[\s\S]*?<\/code>)/)
    .map((seg) =>
      /^<(pre|code)/.test(seg)
        ? seg.replace(/\^/g, '&#94;')
        : seg
            .replace(/([\w)])\^\(([^()]*)\)/g, '$1<sup>$2</sup>')
            .replace(/(\w)\^(-?\d+)/g, '$1<sup>$2</sup>')
            .replace(/\^(?=-?[A-Za-z0-9(])/g, '&#94;')
    )
    .join('');
}

/**
 * The platform renders some block fields as plain text (tags, labels, the lock
 * in lines) and the bank gate therefore refuses an entity in any of them. The
 * recall question is rendered as HTML, but it is on the same list, so it is
 * held to the same rule. Store the literal character wherever the HTML parser
 * cannot mistake it for markup: "&gt;" always, "&lt;" when what follows cannot
 * start a tag (so "i &lt; 5" becomes "i < 5" but "a&lt;b" is left escaped), and
 * "&amp;" when what follows cannot start an entity. Rendering is unchanged.
 */
function plainSafe(s) {
  return s
    .replace(/&gt;/g, '>')
    .replace(/&lt;(?![a-zA-Z!\/?])/g, '<')
    .replace(/&amp;(?![a-zA-Z#])/g, '&')
    .replace(/&middot;/g, '·')
    .replace(/&#8217;/g, '’')
    .replace(/&nbsp;/g, ' ');
}
/** Every entity the manuals use, decoded, for text that is never HTML again. */
function decode(s) {
  return s
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&middot;/g, '·')
    .replace(/&times;/g, '×')
    .replace(/&divide;/g, '÷')
    .replace(/&le;/g, '≤')
    .replace(/&ge;/g, '≥')
    .replace(/&ne;/g, '≠')
    .replace(/&rarr;/g, '→')
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&amp;/g, '&');
}

/**
 * A question's words as PLAIN TEXT, which is what the drill renders: a bank
 * file is never HTML. Line breaks inside an option ("5<br>6<br>7", three lines
 * of output) survive as real newlines, and everything else is flattened.
 */
function plain(html) {
  const s = decode(html.replace(/<br\s*\/?>/g, '\n').replace(/<[^>]+>/g, ''));
  return s
    .split('\n')
    .map((l) => l.replace(/[ \t\r]+/g, ' ').trim())
    .join('\n')
    .replace(/^\n+|\n+$/g, '');
}

/**
 * A listing as plain text, every space kept. The Java manual writes each line
 * as <span class="l">, with no newline between them, and the line numbers are
 * drawn by CSS; the Python manual writes real newlines. Both come out as lines.
 */
function codeText(preHtml) {
  const inner = preHtml.replace(/^<pre[^>]*>/, '').replace(/<\/pre>$/, '');
  const marked = inner.includes('class="l"') ? inner.replace(/<span class="l">/g, '') : inner;
  let s = decode(marked.replace(/<[^>]+>/g, ''));
  if (s.includes('')) s = s.split('').filter((l, i) => i > 0 || l.trim()).join('\n');
  return s.replace(/\s+$/g, '').replace(/^\n+/, '');
}

const PLAIN_FIELDS = ['tag', 'label', 'text', 'big', 'sub', 'howto', 'question'];
function cleanPlainFields(block) {
  for (const k of PLAIN_FIELDS) if (typeof block[k] === 'string') block[k] = plainSafe(block[k]);
  return block;
}

/**
 * The print edition cuts a long programme into stages, "stage 2 of 4", so no
 * stage is taller than a page, and each stage's last question is answered at the
 * top of the next. A screen has no pages. Kept apart, every stage would end on a
 * question nothing answers; joined, it is one continuous run revealed a frame at
 * a time, which is what the stages were only ever standing in for.
 */
function joinStages(blocks) {
  const out = [];
  for (const b of blocks) {
    const prev = out[out.length - 1];
    if (b.kind === 'frames' && prev && prev.kind === 'frames') prev.frames.push(...b.frames);
    else out.push(b);
  }
  return out;
}

/**
 * Difficulty and facets for an objective question, read from what it asks.
 *
 * The facets mean what the course's facet guide says they mean: numbers is
 * "what a program prints", names is the named classes, functions and modules,
 * lists is the rules and orders (a loop's start, test and step, a switch
 * falling through, try then except then finally), wording is the exact
 * distinctions. The words of the question and the listing are read apart, so
 * the "class" in every Java listing's first line does not make every question
 * a question about names.
 */
function tagQuestion(prompt, options) {
  const code = (prompt.match(/<pre[\s\S]*?<\/pre>/g) ?? []).map((c) => text(c.replace(/<\/span><span class="l">/g, '\n'))).join('\n');
  const words = text(prompt.replace(/<pre[\s\S]*?<\/pre>/g, ' ')).toLowerCase();
  const opts = options.map((o) => text(o.text)).join(' | ');
  const multiLine = options.some((o) => /<br/.test(o.text));
  const loop = /\b(for|while)\b/.test(code);

  let difficulty = 'easy';
  if (code) difficulty = multiLine || loop || /\breturn\b[\s\S]*\breturn\b|extends|finally/.test(code) ? 'hard' : 'medium';
  else if (/\b(not|except|two|best|why)\b/.test(words)) difficulty = 'medium';

  const facets = new Set();
  if (code || /\b(print|prints|output|value|how many|result)\b/.test(words)) facets.add('numbers');
  const NAMED =
    /\b(scanner|joptionpane|stringbuilder|javac|jvm|jdk|jre|main|extends|super|abstract|interface|static|bufferedreader|filereader|filewriter|printwriter|sqlite3|commit|cursor|execute|fetchall|tkinter|import|append|extend|split|join|strip|upper|lower|replace|input|len|range|open|readline|readlines|math)\b/i;
  if (NAMED.test(words) || NAMED.test(code) || /\w+Exception\b|\w+Error\b/.test(code + ' ' + words + ' ' + opts)) facets.add('names');
  if (loop || /\b(switch|try|finally|elif)\b/.test(code) || /\b(order|sequence|steps?|precedence|first|checked|how many times)\b/.test(words))
    facets.add('lists');
  if (/defin|describ|distinguish|\btrue\b|\bfalse\b|\bbest\b|\bwhy\b|mean|called|\bterm\b|difference|purpose|which statement/.test(words) || facets.size === 0)
    facets.add('wording');
  return { difficulty, facets: [...facets] };
}

/** The bar of a box carries its label and an optional tag. The Java manual
 *  writes both in ONE span, "MUST-MEMORISE · The shape", so split on the dot. */
function barOf(children) {
  const bar = children.find((n) => has(n, 'bar'));
  if (!bar) return { label: '', tag: '' };
  const spans = nodes(bar.inner).filter((s) => s.tag === 'span');
  let label = text(spans[0]?.inner ?? '');
  let tag = text(spans.find((s) => has(s, 'tag'))?.inner ?? '');
  if (!tag && label.includes(' · ')) {
    const [a, ...rest] = label.split(' · ');
    label = a;
    tag = rest.join(' · ');
  }
  // THE MANUAL SHOUTS ITS LABELS; the app styles them, so store them calm
  label = label.charAt(0) + label.slice(1).toLowerCase();
  return { label: label.replace(/-/g, ' '), tag };
}

const bodyOf = (box) => nodes(box.inner).find((n) => has(n, 'body'));

/**
 * A programmed frame, kept WHOLE.
 *
 * The check is the green-ticked answer that opens a frame; the ask is the task
 * that closes it; the teach is everything between, and for a code course that
 * includes listings and their output. Only when the frame is a single paragraph
 * is it unwrapped, which reproduces the IFT222 importer exactly for that case.
 */
function frameParts(fr) {
  let inner = fr.inner.trim();
  const top = nodes(inner);
  const single = top.length === 1 && top[0].tag === 'p';
  if (single) inner = top[0].inner;

  let check = '';
  const chk = inner.match(/<span class="chk">([\s\S]*?)<\/span>/);
  // the check counts only if it OPENS the frame, before any words of teaching
  if (chk) {
    const before = inner.slice(0, chk.index).replace(/<[^>]+>/g, '').trim();
    if (!before) {
      check = tidy(chk[1]);
      inner = inner.slice(0, chk.index) + inner.slice(chk.index + chk[0].length);
    }
  }
  let ask = '';
  const askM = inner.match(/<span class="ask">([\s\S]*?)<\/span>/);
  if (askM) {
    ask = tidy(askM[1]);
    inner = inner.replace(askM[0], '');
  }
  // removing the two spans can leave an empty paragraph behind; take it out
  inner = inner.replace(/<p>\s*<\/p>/g, '').replace(/<p>\s+/g, '<p>');
  return { check, teach: tidy(inner), ask };
}

const unknown = [];

/** Worked examples whose first paragraph explains rather than asks. */
const WORK_PROBLEM = {
  'l2_4_sets.html':
    '<p><b>Question.</b> A program keeps four things: the registered students, one workshop\'s details (title, room, day, capacity), the attendance with no repeats, and each student\'s score. Name the most suitable Python collection for each, and give the reason in one sentence. The paper wants the name AND the reason; the reason is what separates full marks from half.</p>',
};

/**
 * Review text written for a printed page, where the options sit in a fixed
 * order, may say "the second option". On screen the options are shuffled, so
 * such a line points at nothing. These restate them by content.
 */
const WHY_FIX = {
  'cos-o03-07': {
    d: 'Wrong on the first line, for the same reason as 6, 6, 7: the post-increment gives back the value BEFORE the increment, so the first line is 5.',
  },
};

/**
 * The print edition runs to its own calendar, "Day 1" to "Day 4", 9 to 12
 * September, and says "tomorrow's lesson" meaning its own next day. On the
 * platform the dated plan owns the schedule and every lesson carries its real
 * date, so a reference to the book's days is wrong here and is rewritten to
 * name the lesson instead. Each fix must still match: a fix that finds
 * nothing stops the import, so a changed source cannot let the old wording
 * through unnoticed. The bank gate backs this with a schedule-word rule.
 */
const TEXT_FIX = {
  COS221: [
    ['first-program', /before you read tomorrow's lesson/g, 'before your next Java sitting'],
    ['classes', /Everything else on Day 3 is built on this page\./g, 'Everything else in the object lessons is built on this page.'],
  ],
  CSC241: [
    ['types', /(<code>(?:list|tuple)<\/code>[\s\S]*?)<td>Day 2<\/td>/g, '$1<td>see Lists and Tuples</td>'],
    ['types', /(<code>(?:set|dict)<\/code>[\s\S]*?)<td>Day 2<\/td>/g, '$1<td>see Sets and Dictionaries</td>'],
    ['operators', /which is Day 2's work/g, 'which is the work of the loops lesson'],
    ['sets-dicts', /the trap from Day 1's error lesson/g, 'the trap from the Finding the Errors lesson'],
    ['gui', /objective questions of Day 3/g, 'objective questions of the course'],
  ],
};

function applyTextFixes(code, lessons) {
  for (const [slug, re, to] of TEXT_FIX[code] ?? []) {
    const l = lessons.find((x) => x.slug === slug);
    if (!l) throw new Error(`TEXT_FIX: no lesson ${slug}`);
    let hits = 0;
    const walk = (v) => {
      if (typeof v === 'string') return v.replace(re, (...m) => (hits++, to.replace(/\$(\d)/g, (_, n) => m[Number(n)])));
      if (Array.isArray(v)) return v.map(walk);
      if (v && typeof v === 'object') return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, walk(x)]));
      return v;
    };
    Object.assign(l, walk(l));
    if (!hits) throw new Error(`TEXT_FIX: ${slug} ${re} matched nothing; the source changed, so review this fix`);
  }
}

function convertBox(box, file) {
  const kind = cls(box).replace('box', '').trim().split(/\s+/)[0];
  const bodyNode = bodyOf(box);
  const children = nodes(box.inner);
  const { label, tag } = barOf(children);
  const body = bodyNode ? nodes(bodyNode.inner) : [];

  if (kind === 'prog') {
    const howto = body.find((n) => has(n, 'howto'));
    const frames = body.filter((n) => has(n, 'fr')).map(frameParts);
    return { kind: 'frames', label: 'Work it frame by frame', tag, howto: howto ? tidy(howto.inner) : '', frames };
  }
  if (kind === 'recall') {
    const cutIdx = body.findIndex((n) => n.tag === 'hr' && has(n, 'cut'));
    const q = body.slice(0, cutIdx === -1 ? body.length : cutIdx);
    const a = body.slice(cutIdx === -1 ? body.length : cutIdx + 1).filter((n) => !has(n, 'alabel'));
    return {
      kind: 'recall',
      label: 'Your turn',
      tag,
      question: tidy(q.map((n) => n.raw).join('\n')),
      answer: tidy(a.map((n) => n.raw).join('\n')),
    };
  }
  if (kind === 'work') {
    // The button hides the working, so the question it answers must sit above
    // it. The manual opens every worked example with that question, most as
    // "Question." and one as a paragraph setting the task; either way it is the
    // first paragraph. An override names the task where the paragraph alone
    // does not ask one.
    const first = body.find((n) => n.tag === 'p');
    const override = WORK_PROBLEM[file.split(/[\\/]/).pop()];
    const problem = override ?? (first ? tidy(first.raw) : '');
    const rest = body.filter((n) => override || n !== first).map((n) => n.raw).join('\n');
    return {
      kind: 'worked',
      mode: 'example',
      label: 'Worked example',
      tag,
      problem,
      working: tidy(rest || bodyNode?.inner || ''),
      answer: '',
      redo: '',
    };
  }
  return {
    kind: kind === 'mem' ? 'rules' : kind === 'trap' ? 'trap' : 'teach',
    label: kind === 'mem' ? 'Must memorise' : kind === 'trap' ? 'Trap' : label || 'Teach',
    tag,
    html: tidy(bodyNode?.inner ?? box.inner),
  };
}

/** One crash lesson. Its closing pointer to the paper book becomes a drill. */
function convertLesson(file, slug, modules, minutes, part, drillHere) {
  const raw = readFileSync(file, 'utf8');
  const section = nodes(raw).find((n) => n.tag === 'section');
  const top = nodes(section ? section.inner : raw);
  const lesson = { slug, part, kick: '', title: '', lead: '', minutes, modules, blocks: [] };
  for (const n of top) {
    // "Day 1 · Lesson 1.1": the print book's days were 9 to 12 September. On
    // the platform the date comes from the dated plan, so only the number stays.
    if (has(n, 'kick')) lesson.kick = text(n.inner).replace(/^Day \d+ · /, '');
    else if (n.tag === 'h2' && has(n, 'title')) lesson.title = text(n.inner);
    else if (n.tag === 'hr') continue;
    else if (has(n, 'lead') && !lesson.lead) lesson.lead = tidy(n.inner);
    else if (has(n, 'mustdo')) {
      // "What you must be able to do": the lesson's one line exam skill
      const p = nodes(n.inner).find((x) => x.tag === 'p');
      lesson.blocks.push({ kind: 'rules', label: 'What you must be able to do', tag: '', html: p ? p.raw : tidy(n.inner) });
    } else if (has(n, 'qref')) {
      // the print edition sent you to the other book; here the questions ARE here
      if (drillHere.length)
        lesson.blocks.push({
          kind: 'drill',
          label: 'Now prove it',
          tag: 'every objective question on this topic',
          pick: 'all',
          topics: drillHere,
        });
    } else if (n.tag === 'h3') lesson.blocks.push({ kind: 'heading', text: text(n.inner) });
    else if (has(n, 'lockin')) {
      const parts = nodes(n.inner);
      lesson.blocks.push({
        kind: 'lockin',
        big: tidy(parts.find((p) => has(p, 'big'))?.inner ?? ''),
        sub: tidy(parts.find((p) => has(p, 'sub'))?.inner ?? ''),
      });
    } else if (has(n, 'box')) lesson.blocks.push(convertBox(n, file));
    else if (['p', 'figure', 'table', 'ul', 'ol', 'pre', 'div'].includes(n.tag)) {
      if (text(n.inner) || n.inner.includes('<svg')) lesson.blocks.push({ kind: 'prose', html: tidy(n.raw) });
    } else unknown.push(`${file.split(/[\\/]/).pop()}: <${n.tag} class="${cls(n)}">`);
  }
  return lesson;
}

/**
 * A past paper as theory you answer in your book.
 *
 * The manual prints each question AS PRINTED, then BREAK IT DOWN, then the
 * answer spread over several boxes (the answer, its code, its dry run). On the
 * screen the question stays visible, the break-down hides behind a self mark,
 * and every answer box that follows is gathered into ONE model answer that
 * stays hidden until asked for. Write first, then look.
 */
function convertTheory(files, slug, title, part, lead) {
  const lesson = {
    slug,
    part,
    kick: 'Past theory questions',
    title,
    lead:
      lead ??
      'Every question on this paper, printed exactly as the examiner set it. For each one: read it, write your full answer in your book, and only then open the model answer. Reading an answer you have not attempted teaches you almost nothing.',
    minutes: 90,
    modules: [],
    blocks: [],
  };
  let answer = null; // the model answer being gathered
  let questions = 0;
  const flush = () => {
    if (answer && answer.parts.length)
      lesson.blocks.push({
        kind: 'worked',
        mode: 'model',
        label: 'Model answer',
        tag: answer.tag,
        // the button needs a visible line above it saying what it answers
        problem: /^[\d.]+ marks?$/i.test(answer.tag)
          ? `<p>Write your answer to the question above in your book first. It carries <b>${answer.tag.toLowerCase()}</b>, so write one clear point for every mark. Then open the model answer and mark yourself against it.</p>`
          : `<p>Write your answer to <b>${answer.tag || 'the question above'}</b> in your book first, one clear point for every mark. Then open the model answer and mark yourself against it.</p>`,
        working: answer.parts.join('\n'),
        answer: '',
        redo: '',
      });
    answer = null;
  };
  for (const file of files) {
    const raw = readFileSync(file, 'utf8');
    const sections = nodes(raw).filter((n) => n.tag === 'section');
    for (const sec of sections.length ? sections : [{ inner: raw }]) {
      for (const n of nodes(sec.inner)) {
        if (n.tag === 'h2' && has(n, 'title')) {
          flush();
          lesson.blocks.push({ kind: 'heading', text: text(n.inner) });
        } else if (has(n, 'box')) {
          const kind = cls(n).replace('box', '').trim().split(/\s+/)[0];
          const children = nodes(n.inner);
          const { tag } = barOf(children);
          const body = bodyOf(n);
          if (kind === 'paper') {
            flush();
            questions += 1;
            const printed = body ? nodes(body.inner) : [];
            const pre = printed.find((x) => x.tag === 'pre' && has(x, 'asprinted'));
            lesson.blocks.push({
              kind: 'asprinted',
              label: 'As printed',
              tag,
              src: 'the examiner’s words, unedited',
              printed: body
                ? printed
                    .filter((x) => !has(x, 'src') && !has(x, 'flag'))
                    .map((x) => x.raw)
                    .join('\n')
                : tidy(n.inner),
            });
            // A flag is OUR note about the paper (a figure it printed, a typo
            // kept as evidence). It is not the examiner's words, so it must not
            // sit inside the box that says it is. It follows the box instead.
            for (const f of printed.filter((x) => has(x, 'flag')))
              lesson.blocks.push({
                kind: 'prose',
                html: `<p class="flag"><b>Note on the paper.</b> ${tidy(f.inner).replace(/\s+/g, ' ')}</p>`,
              });
            void pre;
            answer = { tag, parts: [] };
          } else if (kind === 'brk' || kind === 'unpack') {
            lesson.blocks.push({
              kind: 'recall',
              label: 'Break it down first',
              tag: 'before you write a word',
              question:
                '<p>What is this question <b>actually</b> asking, what have you been given, and what do the marks tell you about how much to write? Decide, then check.</p>',
              answer: tidy(body?.inner ?? n.inner),
            });
          } else if (answer) {
            // an answer box, a listing, a dry run: all part of the model answer
            const { label: l2 } = barOf(children);
            answer.parts.push(
              `<div class="mpart"><div class="mlab">${l2}${tag ? ' · ' + tag : ''}</div>${tidy(body?.inner ?? n.inner)}</div>`
            );
          } else {
            // teaching that introduces the paper, before any question
            lesson.blocks.push(convertBox(n, file));
          }
        } else if (['p', 'figure', 'table', 'ul', 'ol', 'pre', 'div'].includes(n.tag) && answer) {
          if (text(n.inner)) answer.parts.push(tidy(n.raw));
        }
      }
      flush();
    }
  }
  lesson.questions = questions;
  return lesson;
}

const WORDS = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight'];
/** The question a label belongs to: "Question Two", "Q2 A", "Mock 1 · Q2" all give 2. */
function questionNo(label) {
  const w = label.match(/Question (One|Two|Three|Four|Five|Six|Seven|Eight)\b/);
  if (w) return WORDS.indexOf(w[1]) + 1;
  const n = label.match(/\bQ(\d+)\b/) ?? label.match(/Question (\d+)\b/);
  return n ? Number(n[1]) : null;
}

/**
 * A mock paper as a lesson: every question in full, then its model answer
 * behind the button, to be sat in the reader's book first.
 *
 * The manuals lay mocks out three ways (one box per question with a separate
 * answers file; one box per PART under a "Question One" heading, with a
 * solutions file whose "Question One, worked in full" heading gathers the
 * answer, its code, its dry run and its traps; or questions and answers in one
 * file), but in every one a label names the question: "Question One", "Q1 A",
 * "Mock 1 · Q1". So each box is filed under its question number and nothing
 * depends on the order the files happen to use. A question with no answer, or
 * an answer with no question, stops the import.
 */
function convertMock(qFiles, aFiles, slug, title, part, minutes, lead) {
  const questions = new Map(); // n -> { tag, parts: [] }
  const answers = new Map(); // n -> [html]
  const intro = [];
  const notes = [];
  const addQ = (n, tag, html) => {
    if (!questions.has(n)) questions.set(n, { tag: '', parts: [] });
    const q = questions.get(n);
    if (tag && !q.tag) q.tag = tag;
    q.parts.push(html);
  };
  const addA = (n, html) => {
    if (!answers.has(n)) answers.set(n, []);
    answers.get(n).push(html);
  };
  const part_ = (label, tag, body) =>
    `<div class="mpart">${label || tag ? `<div class="mlab">${[label, tag].filter(Boolean).join(' · ')}</div>` : ''}${body}</div>`;

  const walk = (file, inAnswers) => {
    const raw = readFileSync(file, 'utf8');
    let current = null;
    let answering = inAnswers;
    const top = nodes(raw).flatMap((n) => (n.tag === 'section' ? nodes(n.inner) : [n]));
    for (const n of top) {
      if (n.tag === 'h2' && has(n, 'title')) {
        const t = text(n.inner);
        if (/^Answers?$/i.test(t)) answering = true;
        const k = questionNo(t);
        current = k ?? (answering ? current : null);
        continue;
      }
      if (!has(n, 'box')) continue;
      const kind = cls(n).replace('box', '').trim().split(/\s+/)[0];
      const children = nodes(n.inner);
      const { label, tag } = barOf(children);
      // span by span: "Question One" and "17.5 marks" must not run together
      const barNode = children.find((c) => has(c, 'bar'));
      const rawBar = barNode
        ? nodes(barNode.inner)
            .filter((s) => s.tag === 'span')
            .map((s) => text(s.inner))
            .join(' · ')
        : '';
      const body = tidy(bodyOf(n)?.inner ?? '');
      const k = questionNo(rawBar) ?? current;
      if (kind === 'qpaper' || (kind === 'qgroup' && !answering)) {
        if (!k) throw new Error(`${file}: a question box with no question number: ${rawBar}`);
        if (kind === 'qpaper') addQ(k, tag, body);
        else addQ(k, '', part_(rawBar.split(' · ')[0].replace(/\s+/g, ' '), tag, body));
      } else if (kind === 'ans' || answering) {
        if (!k) {
          notes.push(convertBox(n, file));
          continue;
        }
        const lbl = kind === 'ans' ? `Answer${tag ? ' · ' + tag : ''}` : label;
        addA(k, part_(lbl, kind === 'ans' ? '' : tag, body));
      } else {
        (questions.size ? notes : intro).push(convertBox(n, file));
      }
    }
  };
  for (const f of qFiles) walk(f, false);
  for (const f of aFiles) walk(f, true);

  const nums = [...questions.keys()].sort((a, b) => a - b);
  const orphans = [...answers.keys()].filter((k) => !questions.has(k));
  const unanswered = nums.filter((k) => !answers.has(k));
  if (orphans.length || unanswered.length)
    throw new Error(`${slug}: answers for missing questions ${orphans.join(',')}; questions with no answer ${unanswered.join(',')}`);

  const blocks = [...intro];
  for (const k of nums) {
    const q = questions.get(k);
    const name = `Question ${WORDS[k - 1]}`;
    blocks.push({ kind: 'heading', text: name });
    blocks.push({ kind: 'teach', label: 'Mock question', tag: q.tag || name, html: q.parts.join('\n') });
    blocks.push({
      kind: 'worked',
      mode: 'model',
      label: 'Model answer',
      tag: name,
      problem: `<p>Write your full answer to <b>${name}</b> in your book first, one clear point for every mark. Then open the model answer and mark yourself against it.</p>`,
      working: answers.get(k).join('\n'),
      answer: '',
      redo: '',
    });
  }
  if (notes.length) blocks.push({ kind: 'heading', text: 'After you have marked it' }, ...notes);
  return {
    slug,
    part,
    kick: 'Mock paper',
    title,
    lead:
      lead ??
      'A full practice paper in the shape of the real one, written from the course and not from a past paper. Sit it in your book against the clock, one question at a time, and only then open each model answer and mark yourself honestly.',
    minutes,
    modules: [],
    blocks: joinStages(blocks).map(cleanPlainFields),
    questions: nums.length,
  };
}

/** The reference card, from the manual's reference part, all as teaching. */
function convertReference(file, slug, title) {
  const raw = readFileSync(file, 'utf8');
  const lesson = {
    slug,
    part: 'Day 4: the night before',
    kick: 'Reference',
    title,
    lead: 'Everything you must have cold, on one card. Read it last thing before the paper, and again in the morning.',
    minutes: 15,
    modules: [],
    blocks: [],
  };
  for (const sec of nodes(raw).filter((n) => n.tag === 'section')) {
    for (const n of nodes(sec.inner)) {
      if (n.tag === 'h2' && has(n, 'title')) lesson.blocks.push({ kind: 'heading', text: text(n.inner) });
      else if (has(n, 'box')) lesson.blocks.push(convertBox(n, file));
      else if (['p', 'table', 'ul', 'ol', 'pre'].includes(n.tag) && text(n.inner) && !has(n, 'lead'))
        lesson.blocks.push({ kind: 'prose', html: tidy(n.raw) });
    }
  }
  return lesson;
}

// ---------------------------------------------------------------- objective

/**
 * The manual wrote its key first or second almost every time: Java's 51
 * questions had 50 keys on the first two options. The drill shuffles options,
 * but a lesson drill is rendered on the server and shows them in stored order,
 * so a reader there would learn the POSITION rather than the answer. These are
 * the manual's own questions, not a real paper, so their order carries no
 * authority. The key is moved to a position fixed by a hash of the question's
 * id: spread evenly, the same on every import, and no pattern to learn. The
 * other options keep their order, so no position-dependent option can break,
 * and none of these says "all of the above".
 */
function balanceKey(item) {
  const ids = 'abcdef';
  let h = 0;
  for (const ch of item.id) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  const keyOpt = item.options.find((o) => o.id === item.answer);
  const order = item.options.filter((o) => o !== keyOpt);
  order.splice(h % item.options.length, 0, keyOpt);
  const remap = Object.fromEntries(order.map((o, i) => [o.id, ids[i]]));
  item.options = order.map((o, i) => ({ id: ids[i], text: o.text }));
  item.why = Object.fromEntries(order.map((o) => [remap[o.id], item.why[o.id]]));
  item.answer = remap[item.answer];
}

/**
 * The manual's objective questions, as drill questions.
 *
 * Each topic section holds an ordered list of questions and, after it, an
 * answer block giving the key and a verdict on every option IN THE SAME ORDER
 * as the options. The verdict's own opening words repeat the option's text, so
 * the pairing is checked rather than assumed: a mismatch stops the import.
 */
function convertObjective(file, cfg) {
  const raw = readFileSync(file, 'utf8');
  const out = [];
  const problems = [];
  for (const sec of raw.split(/(?=<section)/)) {
    const titleM = sec.match(/<h2 class="title">([\s\S]*?)<\/h2>/);
    if (!titleM) continue;
    const title = text(titleM[1]);
    const topic = cfg.topicOf(title);
    const kickM = sec.match(/<div class="kick">([\s\S]*?)<\/div>/);
    const secNo = (text(kickM?.[1] ?? '').match(/O\.(\d+)/) ?? [])[1];
    const lists = [...sec.matchAll(/<ol class="qlist objq">([\s\S]*?)<\/ol>/g)];
    if (!lists.length) continue;
    if (!topic) {
      problems.push(`no topic for objective section "${title}"`);
      continue;
    }
    const stems = [];
    for (const l of lists)
      for (const li of nodes(l[1]).filter((x) => x.tag === 'li')) {
        const parts = nodes(li.inner);
        const oq = parts.find((x) => has(x, 'oq'));
        const opts = parts.find((x) => x.tag === 'ul' && has(x, 'opts'));
        // anything else in the stem (a listing, a table) belongs to the prompt
        const extra = parts.filter((x) => x !== oq && x !== opts).map((x) => x.raw).join('\n');
        const options = nodes(opts?.inner ?? '')
          .filter((x) => x.tag === 'li')
          .map((x, k) => ({
            id: 'abcdef'[k],
            text: tidy(x.inner.replace(/<span class="ol">[\s\S]*?<\/span>\s*/, '')),
          }));
        stems.push({ prompt: tidy((oq?.inner ?? '') + (extra ? '\n' + extra : '')), options });
      }
    const ans = sec.match(/<div class="box obj">([\s\S]*)$/);
    const body = ans ? ans[1] : '';
    const oas = [...body.matchAll(/<p class="oa">([\s\S]*?)<\/p>\s*<ul class="whys">([\s\S]*?)<\/ul>/g)];
    if (oas.length !== stems.length) {
      problems.push(`"${title}": ${stems.length} questions but ${oas.length} answer blocks`);
      continue;
    }
    stems.forEach((q, k) => {
      const [, oa, whysRaw] = oas[k];
      const whys = nodes(whysRaw).filter((x) => x.tag === 'li');
      if (whys.length !== q.options.length) {
        problems.push(`"${title}" Q${k + 1}: ${q.options.length} options, ${whys.length} verdicts`);
        return;
      }
      const why = {};
      let key = null;
      whys.forEach((w, j) => {
        // An option that is several lines of program output is written with
        // line breaks, "true<br>false", and its verdict reads the same lines as
        // "true then false". Read a break as "then" so the two forms compare;
        // a genuinely misaligned verdict still fails.
        const optText = text(q.options[j].text.replace(/<br\s*\/?>/g, ' then ')).replace(/\.$/, '');
        const lead = text((w.inner.match(/<b>([\s\S]*?)<\/b>/) ?? [])[1] ?? '').replace(/\.$/, '');
        if (lead && optText && !lead.startsWith(optText.slice(0, 18)) && !optText.startsWith(lead.slice(0, 18)))
          problems.push(`"${title}" Q${k + 1} option ${q.options[j].id}: verdict is for "${lead.slice(0, 40)}"`);
        why[q.options[j].id] = tidy(w.inner.replace(/^\s*<b>[\s\S]*?<\/b>\s*/, ''));
        if (has(w, 'ok')) key = q.options[j].id;
      });
      if (!key) {
        problems.push(`"${title}" Q${k + 1}: no option is marked correct`);
        return;
      }
      const explanation = tidy(oa.replace(/^\s*<b>\d+\.<\/b>\s*/, ''));
      const { difficulty, facets } = tagQuestion(q.prompt, q.options);
      const qid = `${cfg.idPrefix}-o${String(secNo ?? topic).padStart(2, '0')}-${String(k + 1).padStart(2, '0')}`;
      Object.assign(why, WHY_FIX[qid] ?? {});
      // Options are shuffled on screen, so a letter names nothing. If the manual
      // gave no explanation, name the right option by what it says.
      const keyText = text(q.options.find((o) => o.id === key).text.replace(/<br\s*\/?>/g, ' then '));
      // The drill renders questions as plain text, never HTML: the listing goes
      // in its own field, drawn as a monospace block, and the rest is flattened.
      const listings = [...q.prompt.matchAll(/<pre[\s\S]*?<\/pre>/g)].map((m) => codeText(m[0]));
      const words = plain(q.prompt.replace(/<pre[\s\S]*?<\/pre>/g, ''));
      const item = {
        id: qid,
        module: topic,
        slides: [`Manual O.${secNo ?? topic} Q${k + 1}`],
        style: 'mcq',
        difficulty,
        facets,
        topic: title.toLowerCase(),
        prompt: words,
      };
      if (listings.length) item.code = listings.join('\n\n');
      Object.assign(item, {
        options: q.options.map((o) => ({ id: o.id, text: plain(o.text) })),
        answer: key,
        explanation: text(explanation) ? plain(explanation) : `The answer is "${keyText}".`,
        why: Object.fromEntries(Object.entries(why).map(([id, w]) => [id, plain(w)])),
      });
      balanceKey(item);
      out.push(item);
    });
  }
  return { questions: out, problems };
}

// ---------------------------------------------------------------- run

function run(code) {
  const cfg = CONFIG[code];
  if (!cfg) throw new Error(`no config for ${code}`);
  const root = join(COURSES_DIR, cfg.folder);
  const crash = cfg.crash ? join(root, cfg.crash) : null;
  const manual = join(root, cfg.manual);
  const outDir = join(DATA, cfg.dir);
  if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });

  if (cfg.theoryOnly) {
    const file = join(outDir, 'lessons.json');
    // papers and mocks are replaced, not duplicated, on a re-run
    const slugs = new Set([...cfg.theory, ...(cfg.mocks ?? [])].map(([s]) => s));
    const kept = JSON.parse(readFileSync(file, 'utf8')).filter((l) => !slugs.has(l.slug));
    const papers = cfg.theory.map(([slug, title, files]) => {
      const l = convertTheory(files.map((f) => join(manual, f)), slug, title, 'Past theory questions', cfg.theoryLead);
      if (cfg.theoryMinutes) l.minutes = cfg.theoryMinutes;
      l.blocks = joinStages(l.blocks).map(cleanPlainFields);
      console.log(`  ${slug.padEnd(16)} ${String(l.blocks.length).padStart(3)} blocks, ${l.questions} past questions`);
      delete l.questions;
      return l;
    });
    for (const [slug, title, qf, af] of cfg.mocks ?? []) {
      const l = convertMock(qf.map((f) => join(manual, f)), af.map((f) => join(manual, f)), slug, title, 'Mock papers', 60, cfg.mockLead);
      console.log(`  ${slug.padEnd(16)} ${String(l.blocks.length).padStart(3)} blocks, ${l.questions} mock questions`);
      delete l.questions;
      papers.push(l);
    }
    const at = kept.findIndex((l) => l.slug === cfg.insertBefore);
    kept.splice(at === -1 ? kept.length : at, 0, ...papers);
    if (unknown.length) {
      console.error('\n  IMPORT STOPPED:');
      for (const u of [...new Set(unknown)]) console.error('    x unrecognised ' + u);
      process.exit(1);
    }
    // two-space indent, as the file was written, so the diff is only the papers
    writeFileSync(file, JSON.stringify(kept, null, 2) + '\n');
    console.log(`\n  merged ${papers.length} papers into data/${cfg.dir}/lessons.json`);
    return;
  }

  // each topic's drill goes on the lesson named in drillAt
  const slugs = new Set(cfg.lessons.map(([s]) => s));
  for (const [t2, s] of Object.entries(cfg.drillAt))
    if (!slugs.has(s)) throw new Error(`drillAt ${t2}: no lesson called ${s}`);

  const lessons = [];
  for (const [slug, file, topics, minutes] of cfg.lessons) {
    const day = file.match(/^l(\d)/)[1];
    const drillHere = Object.entries(cfg.drillAt).filter(([, s]) => s === slug).map(([tp]) => Number(tp));
    const l = convertLesson(join(crash, file), slug, topics, minutes, `Day ${day}`, drillHere);
    if (!l.title) throw new Error(`${file}: no title`);
    lessons.push(l);
  }
  for (const [slug, title, files] of cfg.theory) {
    lessons.push(convertTheory(files.map((f) => join(manual, f)), slug, title, 'Past theory questions'));
  }
  for (const [slug, title, qf, af] of cfg.mocks ?? []) {
    lessons.push(convertMock(qf.map((f) => join(manual, f)), af.map((f) => join(manual, f)), slug, title, 'Mock papers', 60));
  }
  const [rslug, rtitle, rfile] = cfg.reference;
  lessons.push(convertReference(join(root, 'makeup', rfile), rslug, rtitle));
  for (const l of lessons) l.blocks = joinStages(l.blocks).map(cleanPlainFields);
  applyTextFixes(code, lessons);

  // The lesson list groups by part, so the part is the DAY the dated plan puts
  // the lesson on. Anything the plan does not place keeps its own part.
  const planFile = join(outDir, 'plan.json');
  if (existsSync(planFile)) {
    const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const plan = JSON.parse(readFileSync(planFile, 'utf8'));
    for (const l of lessons) {
      const s = plan.find((x) => x.lessons.includes(l.slug));
      if (!s) continue;
      const [y, m, d] = s.date.split('-').map(Number);
      l.part = `${DAYS[new Date(Date.UTC(y, m - 1, d)).getUTCDay()]} ${d} ${MONTHS[m - 1]}`;
    }
  }

  const { questions, problems } = convertObjective(join(manual, cfg.objective), cfg);

  // The manual's objective questions are asked by topic at the lesson named in
  // drillAt. They are named by id rather than by topic, so the questions
  // written for single lessons below are not pulled in a second time.
  for (const l of lessons)
    for (const b of l.blocks)
      if (b.kind === 'drill' && (b.topics ?? []).length) {
        b.ids = questions.filter((q) => b.topics.includes(q.module)).map((q) => q.id);
        b.topics = [];
      }

  // Questions written for one lesson (scripts/author/*.py, every program run
  // before it was written out) cite it as "Lesson 1.3" and are asked at the end
  // of that lesson, before its lock-in. The bank gate checks each is asked there.
  const authored = readdirSync(outDir)
    .filter((f) => /^drill\d+[a-z]?\.json$/.test(f) && f !== 'drill01.json')
    .flatMap((f) => JSON.parse(readFileSync(join(outDir, f), 'utf8')));
  for (const l of lessons) {
    const num = (l.kick.match(/^Lesson (\d+\.\d+)/) ?? [])[1];
    if (!num) continue;
    const ids = authored.filter((q) => (q.slides ?? []).includes(`Lesson ${num}`)).map((q) => q.id);
    if (!ids.length) continue;
    const at = l.blocks.findIndex((b) => b.kind === 'lockin');
    l.blocks.splice(at === -1 ? l.blocks.length : at, 0, {
      kind: 'drill',
      label: 'Practise this lesson',
      tag: `${ids.length} questions on exactly this lesson, every program run for real`,
      pick: 'all',
      topics: [],
      ids,
    });
  }

  // ---- report, so nothing is dropped in silence ----
  for (const l of lessons) {
    const c = {};
    for (const b of l.blocks) c[b.kind] = (c[b.kind] ?? 0) + 1;
    const fr = l.blocks.filter((b) => b.kind === 'frames').reduce((t, b) => t + b.frames.length, 0);
    console.log(
      `  ${l.slug.padEnd(16)} ${String(l.blocks.length).padStart(3)} blocks${fr ? `, ${fr} frames` : ''}${
        l.questions ? `, ${l.questions} past questions` : ''
      }  ${Object.entries(c)
        .map(([k, v]) => `${k} ${v}`)
        .join(', ')}`
    );
    delete l.questions;
  }
  const byTopic = {};
  for (const q of questions) byTopic[q.module] = (byTopic[q.module] ?? 0) + 1;
  console.log(`\n  ${questions.length} objective questions, by topic:`, byTopic);
  if (problems.length || unknown.length) {
    console.error('\n  IMPORT STOPPED:');
    for (const p of problems) console.error('    x ' + p);
    for (const u of [...new Set(unknown)]) console.error('    x unrecognised ' + u);
    process.exit(1);
  }
  writeFileSync(join(outDir, 'lessons.json'), JSON.stringify(lessons, null, 1));
  // drill01.json: the name the bank gate recognises. objective.json would be a
  // file of questions the gate never opens, which it rightly refuses.
  writeFileSync(join(outDir, 'drill01.json'), JSON.stringify(questions, null, 1));
  console.log(`\n  wrote data/${cfg.dir}/lessons.json and drill01.json`);
}

const which = process.argv[2];
if (!which) {
  console.error('usage: node scripts/import-makeup.mjs COS221|CSC241|all');
  process.exit(2);
}
for (const code of which === 'all' ? Object.keys(CONFIG) : [which.toUpperCase()]) {
  console.log(`\n=== ${code} ===`);
  run(code);
}
