/**
 * Responsive gate: no page may scroll sideways, at any width, on any device.
 *
 *     node scripts/qa-responsive.mjs            # against http://localhost:3000
 *     node scripts/qa-responsive.mjs <base-url>
 *
 * Horizontal overflow is the failure that actually ruins a phone: the page
 * shifts under your thumb, the first and last character of every line vanish,
 * and pinch-zoom fights you. It is also invisible on a laptop, which is why it
 * survives casual checking and needs measuring instead.
 *
 * For each width we check two things and name the culprit rather than just
 * reporting a number:
 *   1. document.scrollWidth exceeds the viewport, meaning the page scrolls
 *   2. any element's right edge lies beyond the viewport, which is the cause
 *
 * Widths cover the narrowest phone still in use (320, an iPhone SE in
 * landscape-locked apps), common Android and iPhone widths, a tablet, and two
 * desktop sizes. Text is also checked at 200 per cent zoom on the narrowest
 * width, because that is what a reader with poor eyesight actually does.
 */
import { chromium } from 'playwright';

const BASE = process.argv[2] ?? 'http://localhost:3000';

const WIDTHS = [320, 360, 390, 414, 768, 1024, 1280];

const PAGES = [
  '/',
  '/signin',
  '/phy121',
  '/phy121/learn',
  '/phy121/learn/powers-and-units',
  '/phy121/learn/electric-field',
  '/phy121/learn/networks-and-kirchhoff',
  '/ift222',
  '/ift222/learn',
  '/ift222/learn/memory',
  '/ift222/learn/past-paper-2425',
  '/ift222/learn/final-paper',
  '/dts224',
  '/dts224/learn',
  '/dts224/learn/er-model',
  '/dts224/learn/normalization',
  '/csc242',
  '/csc242/learn',
  '/csc242/learn/function-types',
  '/csc242/learn/proof',
  '/csc242/learn/paper-2526',
];

/** Runs in the page: is anything wider than the window, and what? */
const AUDIT = () => {
  const vw = document.documentElement.clientWidth;
  const offenders = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    // 1px of tolerance: sub-pixel rounding is not a bug.
    if (r.right > vw + 1 || r.left < -1) {
      const cs = getComputedStyle(el);
      if (cs.position === 'fixed') continue;
      offenders.push({
        tag: el.tagName.toLowerCase(),
        cls: (el.className || '').toString().slice(0, 60),
        right: Math.round(r.right),
        width: Math.round(r.width),
        text: (el.textContent || '').trim().slice(0, 50),
      });
    }
  }
  // Report the widest few only: one overflowing table drags its whole ancestry
  // into the list, and the widest element is nearly always the real cause.
  offenders.sort((a, b) => b.right - a.right);
  return {
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: vw,
    offenders: offenders.slice(0, 6),
  };
};

const problems = [];
const browser = await chromium.launch();

for (const width of WIDTHS) {
  const ctx = await browser.newContext({
    viewport: { width, height: 850 },
    deviceScaleFactor: 2,
    isMobile: width < 768,
    hasTouch: width < 768,
  });
  const page = await ctx.newPage();

  for (const path of PAGES) {
    const res = await page.goto(BASE + path, { waitUntil: 'networkidle' });
    if (!res || res.status() >= 400) {
      problems.push(`${path} @ ${width}: HTTP ${res ? res.status() : 'no response'}`);
      continue;
    }
    const r = await page.evaluate(AUDIT);
    if (r.scrollWidth > r.clientWidth + 1) {
      const who = r.offenders
        .map((o) => `${o.tag}.${o.cls || '(none)'} right=${o.right} w=${o.width} "${o.text}"`)
        .join('\n        ');
      problems.push(
        `${path} @ ${width}: scrolls sideways, ${r.scrollWidth} > ${r.clientWidth}\n        ${who}`
      );
    }
  }
  await ctx.close();
}

// Zoomed text on the narrowest phone: the case that breaks fixed heights.
const ctx = await browser.newContext({
  viewport: { width: 320, height: 850 },
  deviceScaleFactor: 2,
  isMobile: true,
  hasTouch: true,
});
const page = await ctx.newPage();
for (const path of ['/', '/phy121/learn', '/ift222/learn/memory']) {
  await page.goto(BASE + path, { waitUntil: 'networkidle' });
  await page.evaluate(() => {
    document.documentElement.style.fontSize = '200%';
  });
  const r = await page.evaluate(AUDIT);
  if (r.scrollWidth > r.clientWidth + 1) {
    problems.push(
      `${path} @ 320 with text at 200%: scrolls sideways, ${r.scrollWidth} > ${r.clientWidth}\n        ` +
        r.offenders.map((o) => `${o.tag}.${o.cls} right=${o.right}`).join('\n        ')
    );
  }
}
await ctx.close();
await browser.close();

const checked = WIDTHS.length * PAGES.length + 3;
if (problems.length) {
  console.error(`\nRESPONSIVE GATE FAILED: ${problems.length} of ${checked} checks`);
  for (const p of problems) console.error('  x ' + p);
  process.exit(1);
}
console.log(`RESPONSIVE GATE: pass (${checked} checks)`);
console.log(`  . ${PAGES.length} pages at ${WIDTHS.join(', ')} px, none scrolls sideways`);
console.log('  . and none does at 320 px with text at 200 per cent');
