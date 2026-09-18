/**
 * Rebuild every downloadable book, in one command.
 *
 *     npm run books
 *
 * The PDFs are printed from the app's own pages, so they go stale the moment a
 * question, an answer or a figure changes. This is the whole pipeline behind one
 * command, so bringing them up to date is never a five step thing somebody
 * forgets half of:
 *
 *   1  next build            the pages the books are printed from
 *   2  next start            served on a spare port, killed again at the end
 *   3  print                 a question book and a theory solutions book a course
 *   4  compress and merge    re-deflate, merge identical objects, build the
 *                            all-in-one, and rewrite data/question-books.json
 *                            with the real page counts the pages display
 *
 * Step 4 needs Python with pypdf, which is what the manual builds already use.
 */
import { spawn, spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const WEBAPP = join(HERE, '..');
const PORT = process.env.BOOKS_PORT ?? '3111';
const npx = process.platform === 'win32' ? 'npx.cmd' : 'npx';

/**
 * Windows needs a shell to run npx, because it is a .cmd and node refuses to
 * spawn one without it, and needs NO shell for node and python, because a shell
 * splits the node binary's own path at the space in C:\Program Files.
 */
function run(cmd, args, label, shell = false, env = process.env) {
  const r = spawnSync(cmd, args, { cwd: WEBAPP, stdio: 'inherit', shell, env });
  if (r.status !== 0) {
    console.error(`\n  ${label} failed, so the books were not rebuilt.`);
    process.exit(r.status ?? 1);
  }
}

async function waitForServer(url, tries = 60) {
  for (let i = 0; i < tries; i += 1) {
    try {
      const res = await fetch(url);
      if (res.ok) return;
    } catch {
      // not up yet
    }
    await new Promise((r) => setTimeout(r, 1000));
  }
  throw new Error(`the server never answered on ${url}`);
}

const main = async () => {
  console.log('\n  1. building the pages the books are printed from');
  run(npx, ['next', 'build'], 'next build', process.platform === 'win32');

  console.log(`\n  2. serving them on port ${PORT}`);
  const server = spawn(npx, ['next', 'start', '-p', PORT], {
    cwd: WEBAPP,
    stdio: 'ignore',
    shell: process.platform === 'win32',
    detached: process.platform !== 'win32',
  });
  try {
    await waitForServer(`http://localhost:${PORT}/`);
    console.log('\n  3. printing');
    // BASE must name THIS server. Without it the printer fell back to its
    // default port, where an older server was still running, and printed books
    // from pages that no longer existed.
    run(process.execPath, [join(HERE, 'make-question-book-pdf.mjs')], 'the printer', false, {
      ...process.env,
      BASE: `http://localhost:${PORT}`,
    });
  } finally {
    if (process.platform === 'win32') spawnSync('taskkill', ['/pid', String(server.pid), '/T', '/F']);
    else process.kill(-server.pid);
  }

  console.log('\n  4. compressing, merging and recording the page counts');
  run('python', [join(HERE, 'compress-pdfs.py')], 'the compressor');
  console.log('\n  the books are up to date. Commit public/pdf and data/question-books.json.\n');
};

main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
