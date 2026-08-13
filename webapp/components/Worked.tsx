import { Sci } from '@/components/Sci';

/**
 * A worked solution laid out the way it should be written on paper.
 *
 * The bank's own explanation field is a paragraph, which is fine for a verdict
 * and useless as a model answer. This renders the structured version instead:
 * the background that makes the idea make sense, then Given, Find, the formula
 * with EVERY symbol defined and a line saying why that formula and not another,
 * then the working one line at a time, then the check.
 *
 * The line-by-line part matters most. A reader copying a paragraph learns to
 * write paragraphs; a reader copying numbered lines learns to lay out a
 * solution, which is what earns method marks when the arithmetic slips.
 */
export interface WorkedSolution {
  background?: string;
  given?: string[];
  find?: string;
  formula?: string;
  why?: string;
  symbols?: string[];
  steps?: string[];
  check?: string;
}

export function Worked({ s }: { s: WorkedSolution }) {
  return (
    <div className="wsol">
      {s.background && (
        <div className="wpart">
          <span className="wlab">Background, so this is not just a formula</span>
          <p>
            <Sci text={s.background} />
          </p>
        </div>
      )}

      {(s.given?.length || s.find) && (
        <div className="wpart wgiven">
          {s.given?.length ? (
            <>
              <span className="wlab">Given</span>
              <ul>
                {s.given.map((g) => (
                  <li key={g}>
                    <Sci text={g} />
                  </li>
                ))}
              </ul>
            </>
          ) : null}
          {s.find && (
            <p className="wfind">
              <b>Find:</b> <Sci text={s.find} />
            </p>
          )}
        </div>
      )}

      {s.formula && (
        <div className="wpart wformula">
          <span className="wlab">Formula</span>
          <p className="weqn">
            <Sci text={s.formula} />
          </p>
          {s.why && (
            <p className="wwhy">
              <b>Why this one.</b> <Sci text={s.why} />
            </p>
          )}
          {s.symbols?.length ? (
            <>
              <span className="wlab">What each symbol means</span>
              <ul className="wsyms">
                {s.symbols.map((x) => (
                  <li key={x}>
                    <Sci text={x} />
                  </li>
                ))}
              </ul>
            </>
          ) : null}
        </div>
      )}

      {s.steps?.length ? (
        <div className="wpart wsteps">
          <span className="wlab">The working, line by line</span>
          <ol>
            {s.steps.map((st) => (
              <li key={st}>
                <Sci text={st} />
              </li>
            ))}
          </ol>
        </div>
      ) : null}

      {s.check && (
        <div className="wpart wcheck">
          <span className="wlab">Check it</span>
          <p>
            <Sci text={s.check} />
          </p>
        </div>
      )}
    </div>
  );
}
