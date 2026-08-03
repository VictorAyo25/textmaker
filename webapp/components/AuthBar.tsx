'use client';

import { signIn, signOut, useSession } from 'next-auth/react';

export default function AuthBar({ authEnabled }: { authEnabled: boolean }) {
  const { data: session, status } = useSession();

  if (!authEnabled) {
    return (
      <span className="note">
        Results are saved in this browser only. Add Google sign-in to carry them
        between devices.
      </span>
    );
  }

  if (status === 'loading') return <span className="note">Checking sign-in...</span>;

  if (!session?.user) {
    return (
      <button type="button" className="chip" onClick={() => signIn('google')}>
        Sign in with Google to save results across devices
      </button>
    );
  }

  return (
    <span className="authrow">
      <span className="note">
        Signed in as <b>{session.user.name ?? session.user.email}</b>. Results sync
        across your devices.
      </span>
      <button type="button" className="chip" onClick={() => signOut()}>
        Sign out
      </button>
    </span>
  );
}
