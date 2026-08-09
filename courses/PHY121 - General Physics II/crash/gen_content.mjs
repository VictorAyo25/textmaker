/**
 * Turn the PHY121 crash course into the printed crash manual.
 *
 *     node gen_content.mjs
 *
 * The lessons were authored as data for the platform, in webapp/data/phy121/
 * lessons.json, where the bank gate checks that every drilled fact is taught by
 * some block. Rather than write the book a second time and let the two drift,
 * this converts that same data into content/*.html in the manual's own grammar.
 *
 * The direction is the opposite of IFT222, where the manual came first and
 * scripts/import-crash.mjs carried it to the screen. The rule is the same in
 * both: the words exist once, and are converted, never retyped.
 *
 * The two computer-based tests are appended as a question bank built from the
 * same drill bank the app serves, so the book is self-sufficient: every
 * question the examiner set is printed, answered, and explained option by
 * option, exactly as it is on screen.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA = join(HERE, '..', '..', '..', 'webapp', 'data', 'phy121');
const OUT = join(HERE, 'content');

const lessons = JSON.parse(readFileSync(join(DATA, 'lessons.json'), 'utf8'));

/** The manual groups lessons into parts; the lesson's own `part` already does. */
const kickOf = (l) => l.part.replace(/^Part [A-F]:\s*/, '').replace(/^./, (c) => c.toUpperCase());

const esc = (s) => String(s).replace(/&(?![a-zA-Z#0-9]+;)/g, '&amp;');

/** One programmed frame: the check that answers the frame above, then the step. */
function frame(f) {
  const bits = [];
  if (f.check) bits.push(`<span class="chk">${f.check}</span>`);
  bits.push(f.teach);
  if (f.ask) bits.push(`<span class="ask">${f.ask}</span>`);
  return `<div class="fr"><p>${bits.join(' ')}</p></div>`;
}

function block(b) {
  switch (b.kind) {
    case 'heading':
      return `<h3 class="s">${esc(b.text)}</h3>`;
    case 'prose':
      return b.html;
    case 'teach':
    case 'rules':
    case 'trap': {
      const cls = b.kind === 'rules' ? 'key' : b.kind === 'trap' ? 'trap' : 'teach';
      const label = b.label || (b.kind === 'trap' ? 'Trap' : '');
      return (
        `<div class="box ${cls}"><div class="bar"><span>${esc(label)}</span>` +
        `<span class="tag">${esc(b.tag || '')}</span></div>` +
        `<div class="body">${b.html}</div></div>`
      );
    }
    case 'frames':
      return (
        `<div class="box prog"><div class="bar"><span>${esc(b.label)}</span>` +
        `<span class="tag">${esc(b.tag)}</span></div><div class="body">` +
        `<p class="howto">${esc(b.howto)}</p>` +
        b.frames.map(frame).join('\n') +
        `</div></div>`
      );
    case 'worked':
      return (
        `<div class="box work"><div class="bar"><span>${esc(b.label)}</span>` +
        `<span class="tag">${esc(b.tag)}</span></div><div class="body">` +
        (b.problem ? `<p class="q">${b.problem}</p>` : '') +
        b.working +
        (b.answer ? `<div class="answerbox"><span class="alabel">Answer</span> ${b.answer}</div>` : '') +
        (b.redo ? `<p class="redo"><b>Redo it.</b> ${b.redo}</p>` : '') +
        `</div></div>`
      );
    case 'recall':
      return (
        `<div class="box recall"><div class="bar"><span>${esc(b.label)}</span>` +
        `<span class="tag">${esc(b.tag)}</span></div><div class="body">` +
        b.question +
        `<div class="answerbox"><span class="alabel">Answer</span> ${b.answer}</div>` +
        `</div></div>`
      );
    case 'lockin':
      return `<div class="lockin"><span class="clab">Lock it in</span><p class="big">${b.big}</p><p class="sub">${b.sub}</p></div>`;
    case 'drill':
      // The questions themselves are printed whole in the bank at the back, so
      // the lesson points at them rather than repeating them.
      return (
        `<p class="note"><b>${esc(b.label)}.</b> Every one is printed in full, with its ` +
        `answer and a verdict on each option, in <i>The Two Tests, Every Question Answered</i> ` +
        `at the back. Work them now, before you move on.</p>`
      );
    default:
      return '';
  }
}

let written = 0;
for (const l of lessons) {
  const html =
    `<!-- ===================== ${l.title.toUpperCase()} ===================== -->\n` +
    `<section>\n<div class="kick">${esc(kickOf(l))}</div>\n` +
    `<h2 class="title">${esc(l.title)}</h2>\n<hr class="rule">\n` +
    `<p class="lead">${l.lead}</p>\n` +
    `<p class="lo"><b>About ${l.minutes} minutes.</b> Work every step yourself before reading on. ` +
    `Nothing here is a summary to skim: each box is one small piece of the skill, in order.</p>\n\n` +
    l.blocks.map(block).join('\n\n') +
    `\n</section>\n`;
  writeFileSync(join(OUT, `skill_${l.slug.replace(/-/g, '_')}.html`), html, 'utf8');
  written += 1;
}

console.log(`wrote ${written} lesson files to content/`);
console.log(lessons.map((l) => `skill_${l.slug.replace(/-/g, '_')}.html`).join('\n'));
