import type { MetadataRoute } from 'next';

/**
 * The web app manifest, so the drill can be installed to a phone's home screen
 * and opened without browser chrome. Served by Next at /manifest.webmanifest.
 */
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'CU Drill',
    short_name: 'CU Drill',
    description:
      'Active recall from the CU study manuals: drill any topic, sit the real papers, and be told why every option is right or wrong.',
    start_url: '/',
    display: 'standalone',
    orientation: 'portrait-primary',
    background_color: '#f7faf8',
    theme_color: '#15803d',
    icons: [
      {
        src: '/icon.svg',
        sizes: 'any',
        type: 'image/svg+xml',
        purpose: 'any',
      },
      { src: '/icon-192.png', sizes: '192x192', type: 'image/png', purpose: 'any' },
      { src: '/icon-512.png', sizes: '512x512', type: 'image/png', purpose: 'any' },
      {
        src: '/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'maskable',
      },
    ],
  };
}
