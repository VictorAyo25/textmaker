import type { Metadata } from 'next';
import { authEnabled } from '@/lib/auth';
import Providers from '@/components/Providers';
import SignInButton from '@/components/SignInButton';

export const metadata: Metadata = {
  title: 'Sign in | CU Drill',
  description: 'Sign in to open the drill and the crash courses.',
};

/**
 * The one page anybody can reach signed out.
 *
 * It says what the platform is and offers the button, and nothing else. Where
 * the reader was headed is carried in `from`, so a shared lesson link still
 * lands on that lesson after Google hands them back.
 */
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ from?: string }>;
}) {
  const { from } = await searchParams;
  const target = from && from.startsWith('/') ? from : '/';

  return (
    <main className="wrap signinpage">
      <header className="masthead">
        <span className="code">CU DRILL</span>
        <h1>Sign in to start</h1>
        <span className="sub">
          Active recall built from the study manuals, with a dated reading plan for
          every paper on the timetable.
        </span>
      </header>

      <div className="card">
        <h2>Why you have to sign in</h2>
        <p className="help">
          So the platform can keep <b>your</b> results and <b>your</b> place in every
          crash course, and hand them back on whichever device you pick up next. Read
          four lessons on a laptop at night, open the fifth on your phone in the
          morning.
        </p>
        <Providers>
          <SignInButton enabled={authEnabled} callbackUrl={target} />
        </Providers>
        {!authEnabled && (
          <p className="note">
            Sign-in is not configured on this deployment yet, so nothing can be opened.
            If you own this site, set the Google credentials in the environment and
            redeploy.
          </p>
        )}
      </div>

      <div className="card">
        <h2>What is behind the door</h2>
        <p className="help">
          Every question the examiner has actually set, answered and explained option
          by option, inside the lesson that teaches it. The whole course taught from
          zero in programmed steps, one small step at a time, with worked examples
          done line by line and the traps named. Then the real papers, timed.
        </p>
        <p className="note">
          Your Google account is used for your name and email address only. Nothing is
          posted anywhere, and nothing else in your account is read.
        </p>
      </div>
    </main>
  );
}
