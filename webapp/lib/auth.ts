import type { NextAuthOptions } from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

/**
 * Google sign-in, JWT sessions, no database tables for auth itself.
 *
 * The identity we key results on is the Google account's email. Sessions are
 * JWTs, so signing in costs no database round trip and the app keeps working
 * even when Supabase is unreachable.
 *
 * Auth is OPTIONAL by design. With no Google credentials configured the
 * provider list is empty, `authEnabled` is false, and the app falls back to
 * browser-local history. A missing env var must never break the build or the
 * deploy, only remove the sync feature.
 */
const googleId = process.env.GOOGLE_CLIENT_ID;
const googleSecret = process.env.GOOGLE_CLIENT_SECRET;

export const authEnabled = Boolean(googleId && googleSecret);

export const authOptions: NextAuthOptions = {
  providers: authEnabled
    ? [GoogleProvider({ clientId: googleId!, clientSecret: googleSecret! })]
    : [],
  session: { strategy: 'jwt' },
  // NEXTAUTH_SECRET is required in production; in dev NextAuth generates one.
  secret: process.env.NEXTAUTH_SECRET,
  callbacks: {
    async session({ session, token }) {
      if (session.user && token.sub) {
        (session.user as { id?: string }).id = token.sub;
      }
      return session;
    },
  },
};
