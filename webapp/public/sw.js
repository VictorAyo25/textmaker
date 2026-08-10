/* CU Drill service worker.
 *
 * The whole question bank is compiled into the JavaScript chunks, so caching
 * the static assets caches the course. That makes revision on a phone with no
 * signal work, which is the point.
 *
 * The strategy is deliberately conservative, because the failure mode of a
 * careless service worker is serving a stale page forever:
 *
 *   navigations   network first, cache as a fallback. A new deploy is always
 *                 picked up the moment there is a network, and only a genuine
 *                 offline visit is served from the cache.
 *   /_next/static cache first. Those filenames carry a content hash, so a file
 *                 at a given URL never changes and a stale copy is impossible.
 *   everything else  left alone.
 *
 * The cache name carries a version. Bump it to evict everything.
 */
/* v2 evicts every entry written by v1, which could poison itself: see below. */
const CACHE = 'cu-drill-v2';

/* Only ever store a response that actually succeeded.
 *
 * v1 cached whatever came back, including errors. During a deploy a request for
 * an asset URL can 404, that 404 was written to the cache, and because static
 * assets are served cache-first it was then handed back forever. Victor hit
 * exactly this: the page rendered with no stylesheet on production while the
 * same URL returned a perfectly good 200 to anything but his browser, and only
 * clearing site data could evict it. */
const keep = (req, res) => {
  if (!res || !res.ok || res.status !== 200 || res.type === 'opaque') return res;
  const copy = res.clone();
  caches
    .open(CACHE)
    .then((c) => c.put(req, copy))
    .catch(() => undefined);
  return res;
};
const SHELL = ['/', '/offline'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((c) => c.addAll(SHELL))
      .catch(() => undefined)
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((names) =>
        Promise.all(names.filter((n) => n !== CACHE).map((n) => caches.delete(n)))
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  // Signing in and saving attempts must never be answered from a cache.
  if (url.pathname.startsWith('/api/')) return;

  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then((res) => keep(req, res))
        .catch(() =>
          caches.match(req).then((hit) => hit || caches.match('/offline') || caches.match('/'))
        )
    );
    return;
  }

  if (url.pathname.startsWith('/_next/static/') || url.pathname.startsWith('/icon')) {
    event.respondWith(
      caches.match(req).then((hit) => {
        // A cached entry is only trusted if it succeeded. Anything else is
        // discarded and refetched, so a bad entry can never become permanent.
        if (hit && hit.ok) return hit;
        if (hit) caches.open(CACHE).then((c) => c.delete(req)).catch(() => undefined);
        return fetch(req).then((res) => keep(req, res));
      })
    );
  }
});
