import type { Metadata, Viewport } from 'next';
import './globals.css';
import Offline from '@/components/Offline';

export const metadata: Metadata = {
  title: { default: 'CU Drill', template: '%s' },
  description:
    'Active-recall testing for the CU study manuals. Every question marked instantly and reviewed option by option.',
  manifest: '/manifest.webmanifest',
  appleWebApp: { capable: true, title: 'CU Drill', statusBarStyle: 'default' },
  icons: { icon: '/icon.svg', apple: '/icon-192.png' },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  // The drill is read on phones with the text scaled up, so pinch zoom stays.
  maximumScale: 5,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#15803d' },
    { media: '(prefers-color-scheme: dark)', color: '#0b120e' },
  ],
  viewportFit: 'cover',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Offline />
        {children}
      </body>
    </html>
  );
}
