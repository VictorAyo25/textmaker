'use client';

import { signIn, useSession } from 'next-auth/react';
import Link from 'next/link';

/**
 * The button on the gate page.
 *
 * If someone reaches /signin while already signed in, which happens when a
 * stale tab redirects them, they are shown the way onward rather than being
 * asked to sign in a second time.
 */
export default function SignInButton({
  enabled,
  callbackUrl,
}: {
  enabled: boolean;
  callbackUrl: string;
}) {
  const { data: session, status } = useSession();

  if (status === 'loading') return <p className="note">Checking sign-in...</p>;

  if (session?.user) {
    return (
      <>
        <p className="note">
          Signed in as <b>{session.user.name ?? session.user.email}</b>.
        </p>
        <Link className="btn" href={callbackUrl}>
          Continue
        </Link>
      </>
    );
  }

  return (
    <button
      type="button"
      className="btn"
      disabled={!enabled}
      onClick={() => signIn('google', { callbackUrl })}
    >
      Sign in with Google
    </button>
  );
}
