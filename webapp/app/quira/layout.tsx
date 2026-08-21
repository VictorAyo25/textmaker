import { Inter, Poppins } from 'next/font/google';

// The app's headings are a geometric sans with a single storey g, which is
// Poppins, and its option text is a neutral grotesque, which is Inter. Both are
// pulled through next/font so they are self-hosted at build time: the drill is
// installable and used offline, and a route that needed the network to look
// right would be no use in a hall with bad signal.

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--qx-head',
  display: 'swap',
});

const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--qx-body',
  display: 'swap',
});

export default function QuiraLayout({ children }: { children: React.ReactNode }) {
  return <div className={`${poppins.variable} ${inter.variable}`}>{children}</div>;
}
