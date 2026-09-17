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
import { mkdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, '..', 'public', 'pdf');
const BASE = process.env.BASE ?? 'http://localhost:3100';

const COURSES = [
  { code: 'IFT222', title: 'Computer Architecture and Organisation' },
  { code: 'CSC241', title: 'Python Programming Language I' },
  { code: 'COS221', title: 'Computer Programming I, Java' },
];

const footer = (title) => `
  <div style="font-family:system-ui,sans-serif;font-size:8px;color:#555;width:100%;
              padding:0 14mm;display:flex;justify-content:space-between;">
    <span>${title}</span>
    <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
  </div>`;

async function main() {
  mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: process.env.PW_EXE });
  for (const { code, title } of COURSES) {
    const page = await browser.newPage({ colorScheme: 'light' });
    const url = `${BASE}/${code.toLowerCase()}/learn/question-book`;
    const started = Date.now();
    const res = await page.goto(url, { waitUntil: 'networkidle', timeout: 180_000 });
    if (res.status() !== 200) throw new Error(`${url} answered ${res.status()}`);
    const questions = await page.$$eval('.solq', (els) => els.length);
    if (!questions) throw new Error(`${code}: the question book rendered no questions`);
    await page.emulateMedia({ media: 'print', colorScheme: 'light' });
    const file = join(OUT, `${code}-question-book.pdf`);
    await page.pdf({
      path: file,
      format: 'A4',
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '<span></span>',
      footerTemplate: footer(`${code} question book, every question solved`),
      margin: { top: '14mm', bottom: '16mm', left: '12mm', right: '12mm' },
      timeout: 300_000,
    });
    const mb = (statSync(file).size / 1024 / 1024).toFixed(1);
    console.log(
      `  ${code.padEnd(7)} ${String(questions).padStart(4)} questions  ${mb} MB  ${(
        (Date.now() - started) / 1000
      ).toFixed(0)}s  ${title}`
    );
    await page.close();
  }
  await browser.close();
}

main();
