import { NextResponse, type NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';

/**
 * Nothing is readable until you sign in.
 *
 * The platform is a study tool for named students, so every page is behind the
 * gate: the landing page, every drill, every crash-course lesson. Only the
 * things needed to GET through the gate are open, listed below.
 *
 * ONE DELIBERATE EXCEPTION. If sign-in is not configured, meaning the Google
 * credentials are absent, the gate opens rather than closing. A locked door
 * with no key is worse than an open one here: a mistyped environment variable
 * would otherwise take the whole platform down the night before an exam, with
 * nobody, including the owner, able to get in. There is nothing secret in the
 * material; the point of the gate is to know who is reading and to give each
 * reader their own saved progress, not to protect the physics.
 */
const OPEN = [
  '/api/auth', // the sign-in flow itself, and its callbacks
  '/signin', // the page that offers the button
  '/offline', // the service worker's fallback, which must never redirect
  '/manifest.webmanifest',
  '/icon', // icon-192.png, icon-512.png, icon.svg
  '/sw.js',
  '/favicon.ico',
];

const authConfigured = Boolean(
  process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET
);

export async function middleware(request: NextRequest) {
  const { pathname, search } = request.nextUrl;

  if (!authConfigured) return NextResponse.next();
  if (OPEN.some((p) => pathname === p || pathname.startsWith(p))) return NextResponse.next();

  const token = await getToken({ req: request, secret: process.env.NEXTAUTH_SECRET });
  if (token) return NextResponse.next();

  // An API route gets a status, not a redirect: a fetch cannot follow one into
  // Google's consent screen, and a 401 is what the client already handles.
  if (pathname.startsWith('/api/')) {
    return NextResponse.json({ error: 'sign in required' }, { status: 401 });
  }

  // Remember where they were headed, so a shared lesson link still lands on
  // that lesson once they are through.
  const to = request.nextUrl.clone();
  to.pathname = '/signin';
  to.search = '';
  to.searchParams.set('from', pathname + search);
  return NextResponse.redirect(to);
}

export const config = {
  // Everything except Next's own build output and the static files it serves.
  matcher: ['/((?!_next/static|_next/image).*)'],
};
