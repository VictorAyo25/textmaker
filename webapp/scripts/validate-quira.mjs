/**
 * The side-quest gate.
 *
 *     node scripts/validate-quira.mjs
 *
 * The challenge is judged on speed and accuracy against questions an AI writes
 * from the book, so "we covered the main themes" is not a standard. The forcing
 * function is the ledger: every atomic fact in all 79 pages must be asked about
 * by at least one question, or this fails and the build stops.
 *
 * Eight checks.
 *
 * 1. SCHEMA. Unique ids, a key that points at a real option, four options on
 *    every multiple-choice question because that is what the app shows, and gap
 *    choices that actually contain the accepted answer. A question whose key
 *    names a missing option would mark you wrong forever.
 *
 * 2. LEDGER. Every fact is named by some question, and every question only
 *    names facts that exist. Without this the bank drifts back to whatever was
 *    interesting to write rather than whatever could be asked.
 *
 * 3. PROVENANCE. A question may only name a fact whose own source reference it
 *    also cites. That is what keeps the page reference under each review honest,
 *    so a miss can be chased back to the book in seconds.
 *
 * 4. VERDICTS. Every option of every multiple-choice and true/false question
 *    carries a reason. Half-explained questions do not ship, because the whole
 *    point is learning why the three plausible ones are wrong.
 *
 * 5. NO LETTERS. The app shows options unlettered and in whatever order it
 *    likes, and this trainer shuffles them. So no explanation may refer to an
 *    option by letter or position. This rule was learned the hard way on
 *    another course and it is enforced here from the start.
 *
 * 6. TOPIC SPREAD. Every one of the fourteen passages carries questions, so no
 *    stretch of the book can be quietly skipped.
 *
 * 7. RENDERABLE. Enough of the bank must be drawable as four-option
 *    single-select, because that is the only shape the challenge uses.
 *
 * 8. THE KEY. Forty questions were sat on the real app and marked by it, thirty
 *    in quiz 1 and ten in quiz 2. Those are the only answers in this whole
 *    exercise confirmed by the examiner rather than by us, so the bank is
 *    cross-checked against every one of them. If the bank ever disagrees with
 *    an answer Quira itself marked correct, the bank is wrong and the build
 *    stops.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DIR = join(HERE, '..', 'data', 'quira');

const STYLES = ['mcq', 'multi', 'tf', 'match', 'cloze', 'gap'];
const DIFFS = ['easy', 'medium', 'hard'];
const FACETS = ['numbers', 'names', 'lists', 'wording'];
const TOPICS = 14;

const problems = [];
const check = (ok, msg) => {
  if (!ok) problems.push(msg);
};

// ---- load -----------------------------------------------------------------

const ledger = new Map();
for (const f of readdirSync(join(DIR, 'ledger')).filter((f) => f.endsWith('.json'))) {
  let rows;
  try {
    rows = JSON.parse(readFileSync(join(DIR, 'ledger', f), 'utf8'));
  } catch (e) {
    problems.push(`ledger ${f}: not valid JSON (${e.message})`);
    continue;
  }
  for (const e of rows) {
    check(!ledger.has(e.id), `ledger ${f}: duplicate fact id ${e.id}`);
    check(
      typeof e.fact === 'string' && e.fact.length > 24,
      `ledger ${f} [${e.id}]: fact text missing or too thin`
    );
    check(
      typeof e.ref === 'string' && /^(Intro|Ch\d{1,2}) p\d{1,2}$/.test(e.ref),
      `ledger ${f} [${e.id}]: bad source ref ${JSON.stringify(e.ref)}`
    );
    check(
      Number.isInteger(e.topic) && e.topic >= 1 && e.topic <= TOPICS,
      `ledger ${f} [${e.id}]: topic out of range`
    );
    ledger.set(e.id, e);
  }
}

const questions = [];
for (const f of readdirSync(DIR).filter((f) => f.endsWith('.json'))) {
  let rows;
  try {
    rows = JSON.parse(readFileSync(join(DIR, f), 'utf8'));
  } catch (e) {
    problems.push(`${f}: not valid JSON (${e.message})`);
    continue;
  }
  for (const q of rows) questions.push({ ...q, __file: f });
}

// ---- 1. schema ------------------------------------------------------------

const ids = new Set();
for (const q of questions) {
  const at = `${q.__file} [${q.id}]`;
  check(typeof q.id === 'string' && q.id.length > 0, `${at}: missing id`);
  check(!ids.has(q.id), `${at}: duplicate question id`);
  ids.add(q.id);

  check(STYLES.includes(q.style), `${at}: unknown style ${q.style}`);
  check(DIFFS.includes(q.difficulty), `${at}: unknown difficulty ${q.difficulty}`);
  check(
    Array.isArray(q.facets) && q.facets.length > 0 && q.facets.every((f) => FACETS.includes(f)),
    `${at}: facets missing or unknown`
  );
  check(
    Number.isInteger(q.module) && q.module >= 1 && q.module <= TOPICS,
    `${at}: module out of range`
  );
  check(
    Array.isArray(q.slides) && q.slides.length > 0,
    `${at}: no provenance, so nothing ties it to the book`
  );
  check(
    typeof q.prompt === 'string' && q.prompt.length > 10,
    `${at}: prompt missing or too thin`
  );
  check(
    typeof q.explanation === 'string' && q.explanation.length > 30,
    `${at}: explanation missing or too thin`
  );

  if (q.style === 'mcq') {
    check(Array.isArray(q.options), `${at}: mcq without options`);
    check(
      q.options?.length === 4,
      `${at}: mcq has ${q.options?.length} options; the app always shows four`
    );
    check(
      q.options?.some((o) => o.id === q.answer),
      `${at}: answer ${JSON.stringify(q.answer)} names no option, so it is unanswerable`
    );
    const texts = new Set((q.options ?? []).map((o) => o.text.trim().toLowerCase()));
    check(texts.size === (q.options ?? []).length, `${at}: two options carry the same text`);
  }

  if (q.style === 'tf') {
    check(
      q.answer === 'true' || q.answer === 'false',
      `${at}: true/false answer must be 'true' or 'false'`
    );
  }

  if (q.style === 'gap' || q.style === 'cloze') {
    check(Array.isArray(q.blanks) && q.blanks.length > 0, `${at}: no blanks`);
    for (const [i, b] of (q.blanks ?? []).entries()) {
      check(
        Array.isArray(b.accept) && b.accept.length > 0,
        `${at}: blank ${i + 1} accepts nothing`
      );
      const lower = (b.choices ?? []).map((c) => c.toLowerCase());
      check(
        lower.includes((b.accept?.[0] ?? '').toLowerCase()),
        `${at}: blank ${i + 1} choices do not contain the answer, so it cannot be answered`
      );
      const markers = (q.prompt.match(/\{\{\d+\}\}/g) ?? []).length;
      check(
        markers === q.blanks.length,
        `${at}: ${markers} blank markers in the prompt but ${q.blanks.length} blanks`
      );
    }
  }

  if (q.style === 'match') {
    check(Array.isArray(q.pairs) && q.pairs.length >= 3, `${at}: match needs at least three pairs`);
  }
}

// ---- 2 and 3. the ledger, and honest provenance ---------------------------

const named = new Set();
for (const q of questions) {
  const at = `${q.__file} [${q.id}]`;
  check(
    Array.isArray(q.facts) && q.facts.length > 0,
    `${at}: names no ledger fact, so nothing ties it to anything in the book`
  );
  for (const id of q.facts ?? []) {
    const fact = ledger.get(id);
    if (!fact) {
      problems.push(`${at}: names fact ${id}, which is not in the ledger`);
      continue;
    }
    named.add(id);
    check(
      q.slides.includes(fact.ref),
      `${at}: names fact ${id} from ${fact.ref} but does not cite ${fact.ref}`
    );
    check(
      fact.topic === q.module,
      `${at}: is in topic ${q.module} but names fact ${id} from topic ${fact.topic}`
    );
  }
}

const untested = [...ledger.keys()].filter((id) => !named.has(id));
check(
  untested.length === 0,
  `${untested.length} ledger facts are never asked about: ${untested.slice(0, 12).join(', ')}${untested.length > 12 ? ' ...' : ''}`
);

// ---- 4. every option explained -------------------------------------------

for (const q of questions) {
  if (q.style !== 'mcq' && q.style !== 'tf') continue;
  const at = `${q.__file} [${q.id}]`;
  if (!q.why) {
    problems.push(`${at}: no per-option verdicts`);
    continue;
  }
  for (const o of q.options ?? []) {
    const v = q.why[o.id];
    check(
      typeof v === 'string' && v.length > 15,
      `${at}: option ${o.id} has no real verdict, so the review would ship half explained`
    );
  }
  const extra = Object.keys(q.why).filter((k) => !(q.options ?? []).some((o) => o.id === k));
  check(extra.length === 0, `${at}: verdicts for options that do not exist: ${extra.join(', ')}`);
}

// ---- 5. never name an option by its letter or position -------------------

// Options are shuffled before they are shown, so "option A" or "the third one"
// is meaningless by the time a reader sees it.
const LETTER = /\b(option|answer|choice)\s+[abcd]\b|\boption\s*\(?[abcd]\)?[.,]|\b(the\s+)?(first|second|third|fourth|last)\s+(option|answer|choice)\b/i;
for (const q of questions) {
  const at = `${q.__file} [${q.id}]`;
  const texts = [q.explanation, ...Object.values(q.why ?? {})];
  for (const t of texts) {
    if (typeof t === 'string' && LETTER.test(t)) {
      problems.push(
        `${at}: names an option by letter or position (${JSON.stringify(t.match(LETTER)[0])}); options are shuffled, so name it by its content`
      );
    }
  }
}

// ---- 6. every passage is drilled -----------------------------------------

for (let t = 1; t <= TOPICS; t++) {
  const n = questions.filter((q) => q.module === t).length;
  check(n >= 15, `topic ${t} has only ${n} questions; every passage needs real coverage`);
  const facts = [...ledger.values()].filter((f) => f.topic === t).length;
  check(facts >= 20, `topic ${t} has only ${facts} ledger facts; the passage is under-read`);
}

// ---- 7. enough of it is drawable in the app's own shape ------------------

const renderable = questions.filter(
  (q) =>
    (q.style === 'mcq' && q.options?.length === 4) ||
    q.style === 'tf' ||
    (q.style === 'gap' && q.blanks?.length === 1)
).length;
check(
  renderable >= 350,
  `only ${renderable} questions can be drawn as single-select; the challenge is multiple choice`
);

// ---- 8. the examiner's own answer key ------------------------------------

/**
 * Every question the real app has actually marked for us, transcribed from the
 * two results screens in "side quest/sources/quiz1" and "side quest/ui of the
 * app". Held here as [distinctive bit of the stem, distinctive bit of the key].
 *
 * This is an INDEPENDENT second copy of the key. The bank was authored from the
 * book; this list was read off the app's own green "Correct answer" lines. Two
 * sources that disagree mean one of them is wrong, and it fails the build
 * rather than shipping a wrong answer into tomorrow.
 */
const CONFIRMED = [
  ['as he thinketh in his heart, so is he', 'Thoughts shape personal reality'],
  ['appropriate use of one', 'Overcoming fear and worry'],
  ['fundamental relationship between a person', 'Thoughts serve as the primary key'],
  ['success is primarily a product', 'Right use of the sense'],
  ['define the mind?', 'Seat of feelings or thoughts and the intelligence faculty'],
  ['mad man" has no value', 'Because he is mentally grounded'],
  ['concept of belief', 'As a product of conviction and mental assent'],
  ['mind and the spirit is asserted', 'The mind is as important as the spirit'],
  ['carnally minded individual experience', 'Death'],
  ['in Christ becomes a new creature', '2 Corinthians 5:17'],
  ["Spirit will do to believers' mortal bodies", 'Quicken them by the Spirit that dwelleth in you'],
  ['carnal mind and the spiritual mind regarding', 'The carnal mind results in death'],
  ['bring new things into being', 'The mind of Christ'],
  ["quality of a person's life", "The state of one's mind"],
  ['when one uses their mind appropriately', 'All personal crises in family, business, or finances'],
  ['building analogy', 'Both require regular use to prevent deterioration'],
  ["T. L. Osborn's view", 'When you stop learning, you start dying'],
  ['mastery over astrologers and magicians', 'Daniel'],
  ['about half of the New Testament', 'Paul'],
  ['failing to engage in continuous learning', 'A decline in both mental and physical vitality'],
  ['stop learning after leaving school', 'Reading only the introduction and conclusion of a book'],
  ['knowledge can set a person free', 'John 8:32'],
  ['cannot benefit from classroom instruction', 'Because his mind is out of use'],
  ['Oswald J. Smith still consulting his dictionary', '93'],
  ['Norman Vincent Pearle an ordained minister', '72 years'],
  ['actively using one', 'Every divine deposit multiplies with use'],
  ["Paul's prayer in Ephesians 1:17-18", 'The spirit of wisdom and revelation'],
  ['Ethiopian eunuch', 'Understandest thou what thou readest?'],
  ['knowledge becomes understanding', 'By processing knowledge with commitment'],
  ['Two are better than one', 'Collaboration enhances outcomes'],
  ['truthfulness of God', "God's Word is always true"],
  ['marriages fail to reach the state', 'A lack of understanding and incorrect application'],
  ['distinguish between knowledge and understanding', 'Knowledge is based on physical senses'],
  ['greater understanding than the ancients', 'His meditation on God'],
  ['percentage of the human population', '5%'],
  ['true understanding effectively achieved', 'By engaging in a conscious process of meditation'],
  ['define "reasoning"', 'Engaging in logical, rational and analytical thinking'],
  ['eat the good of the land', 'Be willing and obedient'],
  ['return to colour and beauty', 'He reasoned his way back'],
  ['before beginning to build a tower', 'Sit down and count the cost'],
];

for (const [stem, key] of CONFIRMED) {
  const hit = questions.find((q) => q.prompt.toLowerCase().includes(stem.toLowerCase()));
  if (!hit) {
    problems.push(
      `the app has already asked "${stem}" and the bank no longer contains it, so a confirmed question would go undrilled`
    );
    continue;
  }
  const text = hit.options?.find((o) => o.id === hit.answer)?.text ?? '';
  check(
    text.toLowerCase().includes(key.toLowerCase()),
    `[${hit.id}]: the app marked "${key}" correct, but the bank keys "${text}"`
  );
}

// ---- report ---------------------------------------------------------------

const hard = [...ledger.values()].filter((f) => f.hard).length;
if (problems.length) {
  console.error(`\nQUIRA GATE FAILED with ${problems.length} problem(s):\n`);
  for (const p of problems.slice(0, 60)) console.error('  - ' + p);
  if (problems.length > 60) console.error(`  ... and ${problems.length - 60} more`);
  console.error('');
  process.exit(1);
}

console.log(
  `Quira gate: ${questions.length} questions, ${renderable} drawable as the app draws them, ` +
    `${ledger.size} ledger facts (${hard} hard) across ${TOPICS} passages, all tested, and all ${CONFIRMED.length} answers the app itself marked agree.`
);
