import Link from 'next/link';

/**
 * The way out of any page.
 *
 * Every screen except the landing page carries this, so there is always a route
 * home and always a route one level up. The browser's back button is not
 * enough: a reader arriving from a shared link has no history to go back
 * through, and a reader three lessons deep should not have to press it four
 * times to reach the drill.
 *
 * Rendered on the server as plain links, so it works before hydration and
 * without JavaScript at all.
 */
export interface Crumb {
  label: string;
  href?: string;
}

export default function Crumbs({
  trail,
  aside,
}: {
  trail: Crumb[];
  /** The sideways move: drill to crash course, or crash course to drill. */
  aside?: Crumb;
}) {
  return (
    <nav className="crumbs" aria-label="Breadcrumb">
      <Link className="crumb home" href="/">
        <span aria-hidden="true">&#8962;</span> All courses
      </Link>
      {trail.map((c) => (
        <span key={c.label}>
          <span className="sep" aria-hidden="true">
            /
          </span>
          {c.href ? (
            <Link className="crumb" href={c.href}>
              {c.label}
            </Link>
          ) : (
            <span className="crumb here" aria-current="page">
              {c.label}
            </span>
          )}
        </span>
      ))}
      {aside?.href && (
        <Link className="crumb aside" href={aside.href}>
          {aside.label} &rarr;
        </Link>
      )}
    </nav>
  );
}
