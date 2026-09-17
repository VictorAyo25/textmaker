/**
 * Read the IFT222 manual's box grammar out of its built HTML.
 *
 * The manual writes every past question as three boxes in a row: AS PRINTED,
 * which is the examiner's words untouched, BREAK IT DOWN, and WORKED EXAMPLE.
 * All three have been house-styled, numerically checked and gated in the manual
 * build, so lifting them is safer than retyping them, and the words a reader
 * meets on screen are the words those gates passed.
 *
 * A depth counting scan rather than a regular expression, because the boxes
 * nest divs and a regular expression cannot match a closing tag it cannot count.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

/** Every `<div class="box ...">` in the file, with its label, tag and body. */
export function boxes(html) {
  const found = [];
  const open = /<div class="box ([a-z][a-z ]*)"/g;
  let m;
  while ((m = open.exec(html))) {
    const raw = slice(html, m.index);
    found.push({
      kind: m[1].trim().split(/\s+/)[0],
      classes: m[1].trim(),
      raw,
      label: (raw.match(/<div class="bar"><span>([^<]*)<\/span>/) ?? [])[1] ?? '',
      tag: (raw.match(/<span class="tag">([^<]*)<\/span>/) ?? [])[1] ?? '',
      body: inner(raw, '<div class="body">'),
      at: m.index,
    });
  }
  return found;
}

/** The whole element starting at `from`, by counting div openings and closings. */
function slice(html, from) {
  const re = /<\/?div\b[^>]*>/g;
  re.lastIndex = from;
  let depth = 0;
  let m;
  while ((m = re.exec(html))) {
    depth += m[0].startsWith('</') ? -1 : 1;
    if (depth === 0) return html.slice(from, m.index + m[0].length);
  }
  return html.slice(from);
}

/** What sits inside the first div whose opening tag starts with `marker`. */
function inner(raw, marker) {
  const at = raw.indexOf(marker);
  if (at === -1) return '';
  const whole = slice(raw, at);
  const open = whole.indexOf('>') + 1;
  return whole.slice(open, whole.length - '</div>'.length).trim();
}

/** Every past question site in the manual, in reading order, file by file. */
export function paperSites(dir) {
  const sites = [];
  for (const file of readdirSync(dir).filter((f) => f.endsWith('.html')).sort()) {
    const html = readFileSync(join(dir, file), 'utf8');
    const found = boxes(html);
    found.forEach((box, i) => {
      if (box.kind !== 'paper' && box.kind !== 'qpaper') return;
      const src = box.body.match(/data-src="(\d{4}-\d{4}):(Q[0-9a-z]+)"/);
      if (!src) return;
      // The two boxes that follow, while they belong to this question: the
      // manual always writes them in this order and never interleaves.
      const after = found.slice(i + 1, i + 4);
      const stop = after.findIndex((b) => b.kind === 'paper' || b.kind === 'qpaper');
      const near = stop === -1 ? after : after.slice(0, stop);
      sites.push({
        file,
        year: src[1],
        q: src[2],
        tag: box.tag,
        printed: inner(box.raw, '<div class="asprinted"') || box.body,
        unpack: near.find((b) => b.kind === 'unpack')?.body ?? '',
        work: near.find((b) => b.kind === 'work')?.body ?? '',
        workTag: near.find((b) => b.kind === 'work')?.tag ?? '',
      });
    });
  }
  return sites;
}
