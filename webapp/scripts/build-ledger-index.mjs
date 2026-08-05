/**
 * Build the browser-side ledger index.
 *
 *     node scripts/build-ledger-index.mjs
 *
 * The ledger proper (data/<course>/ledger/*.json) is a build-time artefact: the
 * gate reads it and nothing ships it. The mastery map, though, has to name the
 * facts you have not been tested on, so it needs the text in the browser.
 *
 * This writes one flat file per course carrying only what the map displays. It
 * is imported dynamically, so it costs the drill nothing until someone opens
 * the map. The file is committed, and the bank gate refuses to pass if it has
 * drifted from the ledger it was built from, so it cannot go stale unnoticed.
 */
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DATA = join(HERE, '..', 'data');

/** The shape the browser reads: id, topic, hard, fact. Nothing else. */
export function buildIndex(dir) {
  const ledgerDir = join(dir, 'ledger');
  const out = [];
  for (const f of readdirSync(ledgerDir).filter((f) => f.endsWith('.json')).sort()) {
    for (const e of JSON.parse(readFileSync(join(ledgerDir, f), 'utf8'))) {
      out.push({ id: e.id, topic: e.topic, hard: !!e.hard, fact: e.fact });
    }
  }
  out.sort((a, b) => a.id.localeCompare(b.id));
  return out;
}

export const INDEX_FILE = 'ledger-index.json';

/** Exactly what gets written, so the gate can compare byte for byte. */
export function serialise(index) {
  return JSON.stringify(index, null, 2) + '\n';
}

if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('build-ledger-index.mjs')) {
  let wrote = 0;
  for (const course of readdirSync(DATA, { withFileTypes: true })) {
    if (!course.isDirectory()) continue;
    const dir = join(DATA, course.name);
    if (!existsSync(join(dir, 'ledger'))) continue;
    const index = buildIndex(dir);
    writeFileSync(join(dir, INDEX_FILE), serialise(index), 'utf8');
    console.log(`${course.name}: ${index.length} facts -> ${INDEX_FILE}`);
    wrote += 1;
  }
  if (!wrote) console.log('no course carries a ledger; nothing to build');
}
