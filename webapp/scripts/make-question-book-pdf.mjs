/**
 * Print each live course's question book to a PDF you can carry offline.
 *
 *     npx next build && npx next start -p 3100      (in another shell)
 *     PW_EXE=... node scripts/make-question-book-pdf.mjs
 *
 * The page already exists: /<course>/learn/question-book is every question the
 * course owns, the examiner's own tests included, each with its options, the
 * answer marked, why every wrong option is wrong, and the reasoning under it.
 * This prints that page rather than authoring a second copy of it, so the PDF
 * cannot drift from the app: same bank, same explanations, one source.
 *
 * Chromium prints it, because the layout is the app's own CSS and its print
 * block is already tuned: crumbs, buttons and the auth bar are hidden, cards
 * lose their shadows, and a question never splits across a page.
 *
 * Output lands in public/pdf/, which Vercel serves as a static file, so the
 * download is a plain link with no server work behind it.
 */
import { chromium } from 'playwright';
import { mkdirSync, statSync, existsSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, '..', 'public', 'pdf');
const BASE = process.env.BASE ?? 'http://localhost:3100';

/**
 * Which Chromium to print with. PW_EXE wins; otherwise the headless shell
 * Playwright has already installed is found, so `npm run books` needs no
 * environment set up to work on this machine.
 */
function browserPath() {
  if (process.env.PW_EXE) return process.env.PW_EXE;
  const root = join(process.env.LOCALAPPDATA ?? '', 'ms-playwright');
  if (!existsSync(root)) return undefined;
  for (const dir of readdirSync(root).filter((d) => d.startsWith('chromium'))) {
    for (const sub of ['chrome-headless-shell-win64', 'chrome-win']) {
      for (const exe of ['chrome-headless-shell.exe', 'chrome.exe']) {
        const candidate = join(root, dir, sub, exe);
        if (existsSync(candidate)) return candidate;
      }
    }
  }
  return undefined;
}

const COURSES = [
  { code: 'IFT222', title: 'Computer Architecture and Organisation' },
  { code: 'CSC241', title: 'Python Programming Language I' },
  { code: 'COS221', title: 'Computer Programming I, Java' },
];

/** Two books per course: the objective half, and the questions you write. */
const BOOKS = [
  { slug: 'question-book', suffix: 'question-book', what: 'question book, every question solved', count: '.solq' },
  { slug: 'theory-book', suffix: 'theory-solutions', what: 'theory solutions, every written question answered', count: '.lblock.worked' },
];

const footer = (title) => `
  <div style="font-family:system-ui,sans-serif;font-size:8px;color:#555;width:100%;
              padding:0 14mm;display:flex;justify-content:space-between;">
    <span>${title}</span>
    <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
  </div>`;

async function main() {
  mkdirSync(OUT, { recursive: true });
  console.log(`  printing from ${BASE}`);
  const browser = await chromium.launch({ executablePath: browserPath() });
  for (const { code, title } of COURSES) {
    for (const book of BOOKS) {
    const page = await browser.newPage({ colorScheme: 'light' });
    const url = `${BASE}/${code.toLowerCase()}/learn/${book.slug}`;
    const started = Date.now();
    const res = await page.goto(url, { waitUntil: 'networkidle', timeout: 180_000 });
    if (res.status() !== 200) throw new Error(`${url} answered ${res.status()}`);
    const questions = await page.$$eval(book.count, (els) => els.length);
    if (!questions) throw new Error(`${code}: ${book.slug} rendered nothing`);
    await page.emulateMedia({ media: 'print', colorScheme: 'light' });
    const file = join(OUT, `${code}-${book.suffix}.pdf`);
    await page.pdf({
      path: file,
      format: 'A4',
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: footer(`${code} ${book.what}`),
      margin: { top: '14mm', bottom: '16mm', left: '12mm', right: '12mm' },
      timeout: 300_000,
    });
    const mb = (statSync(file).size / 1024 / 1024).toFixed(1);
    console.log(
      `  ${code.padEnd(7)} ${book.suffix.padEnd(17)} ${String(questions).padStart(4)} items  ${mb} MB  ${(
        (Date.now() - started) / 1000
      ).toFixed(0)}s`
    );
    await page.close();
    }
  }
  await browser.close();
}

main();
