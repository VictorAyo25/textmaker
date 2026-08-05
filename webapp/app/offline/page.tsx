import Link from 'next/link';

export const metadata = { title: 'Offline' };

/**
 * The page the service worker falls back to when a navigation is attempted
 * with no network and nothing cached for that URL. Precached at install, so it
 * is always there when it is needed.
 */
export default function Page() {
  return (
    <main className="wrap">
      <header className="masthead">
        <span className="code">CU DRILL</span>
        <h1>You are offline</h1>
        <span className="sub">
          This page has not been opened on this device before, so there is nothing
          saved to show. Anything you have already visited still works.
        </span>
      </header>
      <div className="card">
        <h2>What you can still do</h2>
        <p className="help">
          Courses you have already opened are kept on this device, questions and all.
          Your answers, your weak spots and your history are stored in this browser,
          so nothing is lost while the network is away.
        </p>
        <Link className="btn" href="/">
          Back to the courses
        </Link>
      </div>
    </main>
  );
}
