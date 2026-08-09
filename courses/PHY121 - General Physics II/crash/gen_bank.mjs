/**
 * Print both computer-based tests into the crash manual, every question
 * answered and every option judged.
 *
 *     node gen_bank.mjs
 *
 * Built from the same bank webapp serves, filtered on the provenance tag the
 * drill uses, so the paper in the book and the paper on the screen are one
 * transcription. A correction to a question cannot reach one and miss the other.
 *
 * Options are printed in their STORED order and lettered from that order. The
 * app shuffles them, which is why no explanation anywhere in this project names
 * an option by its letter; each verdict names the option by its content, and
 * that is what makes the same text safe in both places.
 */
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA = join(HERE, '..', '..', '..', 'webapp', 'data', 'phy121');

const SKIP = new Set(['lessons.json', 'ledger-index.json', 'plan.json']);
const bank = [];
for (const f of readdirSync(DATA)) {
  if (!f.endsWith('.json') || SKIP.has(f)) continue;
  bank.push(...JSON.parse(readFileSync(join(DATA, f), 'utf8')));
}

const esc = (s) =>
  String(s)
    .replace(/&(?![a-zA-Z#0-9]+;)/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

/** 10^-9 written with a caret has to become a superscript on paper. */
const sci = (s) => esc(s).replace(/\^(-?\d+)/g, '<sup>$1</sup>');

const num = (q, tag) => Number(q.slides.find((s) => s.startsWith(tag))?.match(/Q(\d+)$/)?.[1] ?? 0);

function paper(tag, title, note) {
  const qs = bank
    .filter((q) => q.slides.some((s) => s.startsWith(`${tag} Q`)))
    .sort((a, b) => num(a, tag) - num(b, tag));

  const rows = qs.map((q, i) => {
    const n = num(q, tag);
    let body = `<p class="q"><b>${n}.</b> ${sci(q.prompt.replace(/\{\{(\d+)\}\}/g, '________'))}</p>`;

    if (q.style === 'mcq' || q.style === 'multi') {
      body +=
        '<div class="qlist">' +
        (q.options ?? [])
          .map(
            (o, j) =>
              `<p class="p"><span class="k">${String.fromCharCode(97 + j)}.</span> ${sci(o.text)}</p>`
          )
          .join('') +
        '</div>';
    } else if (q.style === 'tf') {
      body += '<div class="qlist"><p class="p"><span class="k">a.</span> True</p><p class="p"><span class="k">b.</span> False</p></div>';
    } else if (q.style === 'gap') {
      body += `<p class="note">Fill the blank. ${(q.blanks ?? [])
        .map((b) => `Accepted: <b>${esc((b.accept ?? [])[0] ?? '')}</b>`)
        .join('; ')}</p>`;
    }

    const key =
      q.style === 'tf'
        ? q.answer === 'true'
          ? 'True'
          : 'False'
        : q.style === 'gap'
          ? esc(((q.blanks ?? [])[0]?.accept ?? [])[0] ?? '')
          : sci((q.options ?? []).find((o) => o.id === q.answer)?.text ?? String(q.answer));

    body += `<div class="answerbox"><span class="alabel">Answer</span> ${key}</div>`;
    body += `<p class="note2">${sci(q.explanation)}</p>`;

    if (q.why) {
      body +=
        '<div class="qlist">' +
        Object.entries(q.why)
          .map(([id, text]) => {
            const label =
              q.style === 'tf'
                ? id === 'true'
                  ? 'True'
                  : 'False'
                : sci((q.options ?? []).find((o) => o.id === id)?.text ?? id);
            return `<p class="p"><span class="k">${label}</span> ${sci(text)}</p>`;
          })
          .join('') +
        '</div>';
    }
    return `<div class="box ans"><div class="bar"><span>${tag} Q${n}</span><span class="tag">${esc(q.topic)}</span></div><div class="body">${body}</div></div>`;
  });

  return { count: qs.length, html: `<h3 class="s">${esc(title)}</h3>\n<p class="lo">${note}</p>\n${rows.join('\n')}` };
}

const t1 = paper(
  'Test 1',
  'Computer-Based Test 1, all 15 questions',
  'Captured as a graded review page marked 14 out of 15. Question 9 is quoted as printed and is INCOMPLETE: its stem ends at "represented by" with the figure missing, and it is the one question marked wrong, so no true answer can be recovered from the capture.'
);
const t2 = paper(
  'Test 2',
  'Computer-Based Test 2, all 15 questions',
  'Captured as a graded review page marked 15 out of 15, so every answer here is confirmed by the examiner. Worth knowing: on this paper the correct choice was the FIRST option every single time. The drill shuffles the options, which takes that crutch away.'
);

const html =
  `<!-- ===================== THE TWO TESTS ===================== -->\n` +
  `<section>\n<div class="kick">Prove It</div>\n` +
  `<h2 class="title">The Two Tests, Every Question Answered</h2>\n<hr class="rule">\n` +
  `<p class="lead">Every question the examiner has set on this course, printed in full, answered, ` +
  `and judged option by option. Thirty questions across the two computer-based tests. Cover the ` +
  `answer, attempt the question, then read the verdict on every option, including the ones you did ` +
  `not choose.</p>\n` +
  `<p class="lo">The options are lettered here in the order they are stored. On the platform they ` +
  `are shuffled, so no verdict in this book names an option by its letter: each one names the ` +
  `option by what it says.</p>\n\n${t1.html}\n\n${t2.html}\n</section>\n`;

writeFileSync(join(HERE, 'content', 'bank.html'), html, 'utf8');
console.log(`wrote bank.html: ${t1.count} + ${t2.count} questions`);
