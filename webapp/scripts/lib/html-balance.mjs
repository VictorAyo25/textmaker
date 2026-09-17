/**
 * Close what was left open, drop what was never opened.
 *
 * The manual's worked examples are one box in print: a problem, then the working
 * under it. The app splits that box into two fields, because the working hides
 * behind a button, and the split can land INSIDE a div. Each half is then valid
 * on its own only by accident: one ends with a div still open, the other starts
 * with a closing tag for a div it never opened.
 *
 * A browser repairs both, silently and differently from the server's rendering,
 * which is exactly what React reports as hydration error 418. It was live on the
 * 2025/2026 paper page before this existed. Balancing each field as it is stored
 * fixes the page for good and costs nothing at run time.
 */
const VOID = new Set(['br', 'hr', 'img', 'input', 'meta', 'link', 'col', 'source', 'area', 'base']);

export function balanceHtml(html) {
  if (typeof html !== 'string' || !html.includes('<')) return html;
  const stack = [];
  let out = '';
  let last = 0;
  const tag = /<(\/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(\/?)>/g;
  let m;
  while ((m = tag.exec(html))) {
    const [whole, closing, name, selfClose] = m;
    const lower = name.toLowerCase();
    out += html.slice(last, m.index);
    last = m.index + whole.length;
    if (VOID.has(lower) || selfClose) {
      out += whole;
      continue;
    }
    if (!closing) {
      stack.push(lower);
      out += whole;
      continue;
    }
    // A closing tag for something never opened here: the other half of the split
    // holds its opener, so dropping it is the repair.
    const at = stack.lastIndexOf(lower);
    if (at === -1) continue;
    // Close anything left open inside it, then it.
    while (stack.length > at + 1) out += `</${stack.pop()}>`;
    stack.pop();
    out += whole;
  }
  out += html.slice(last);
  while (stack.length) out += `</${stack.pop()}>`;
  return out;
}

/** Every string field of a block, balanced. */
export function balanceBlock(block) {
  const fixed = { ...block };
  for (const [k, v] of Object.entries(fixed))
    if (typeof v === 'string' && v.includes('<')) fixed[k] = balanceHtml(v);
  if (Array.isArray(fixed.frames))
    fixed.frames = fixed.frames.map((f) => balanceBlock(f));
  return fixed;
}
