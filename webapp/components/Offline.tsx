'use client';

import { useEffect, useState } from 'react';

/**
 * Registers the service worker and says so when the network has gone.
 *
 * Registration is deliberately late, after the page has settled, so it never
 * competes with the first paint. It is also skipped in development, where a
 * cached shell only gets in the way of seeing your own changes.
 */
export default function Offline() {
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    const update = () => setOffline(!navigator.onLine);
    update();
    window.addEventListener('online', update);
    window.addEventListener('offline', update);

    let cancel: (() => void) | undefined;
    if (
      'serviceWorker' in navigator &&
      process.env.NODE_ENV === 'production' &&
      window.location.protocol === 'https:'
    ) {
      const id = window.setTimeout(() => {
        navigator.serviceWorker.register('/sw.js').catch(() => {
          /* an unregistrable worker must never break the app */
        });
      }, 2000);
      cancel = () => window.clearTimeout(id);
    }

    return () => {
      window.removeEventListener('online', update);
      window.removeEventListener('offline', update);
      cancel?.();
    };
  }, []);

  if (!offline) return null;
  return (
    <div className="offlinebar" role="status">
      You are offline. Everything already loaded still works, and your answers are
      saved in this browser.
    </div>
  );
}
