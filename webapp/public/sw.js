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
const CACHE = 'cu-drill-v1';
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
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => undefined);
          return res;
        })
        .catch(() =>
          caches.match(req).then((hit) => hit || caches.match('/offline') || caches.match('/'))
        )
    );
    return;
  }

  if (url.pathname.startsWith('/_next/static/') || url.pathname.startsWith('/icon')) {
    event.respondWith(
      caches.match(req).then(
        (hit) =>
          hit ||
          fetch(req).then((res) => {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => undefined);
            return res;
          })
      )
    );
  }
});
