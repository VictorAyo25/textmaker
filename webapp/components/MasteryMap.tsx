'use client';

import { useEffect, useMemo, useState } from 'react';
import type { Course, Question } from '@/lib/types';
import { factState, indexByFact, loadMastery, type Mastery } from '@/lib/mastery';

/**
 * What you have and have not been tested on, fact by fact.
 *
 * Only possible because every question in a ledger course names the facts it
 * tests. A score of 72 per cent on a topic tells you nothing actionable; this
 * tells you that eleven specific facts are still soft and six have never come
 * up at all, and hands you the questions that cover them.
 *
 * The ledger index is fetched on demand rather than bundled, so the drill pays
 * nothing for a screen most sittings never open.
 */

interface LedgerFact {
  id: string;
  topic: number;
  hard: boolean;
  fact: string;
}

interface Props {
  course: Course;
  onDrill: (questions: Question[], title: string) => void;
  onBack: () => void;
}

export default function MasteryMap({ course, onDrill, onBack }: Props) {
  const [ledger, setLedger] = useState<LedgerFact[] | null>(null);
  const [failed, setFailed] = useState(false);
  const [mastery, setMastery] = useState<Mastery>({});
  const [open, setOpen] = useState<number | null>(null);

  useEffect(() => {
    setMastery(loadMastery(course.code));
    let live = true;
    import(`@/data/${course.code.toLowerCase()}/ledger-index.json`)
      .then((m) => {
        if (live) setLedger((m.default ?? m) as LedgerFact[]);
      })
      .catch(() => {
        if (live) setFailed(true);
      });
    return () => {
      live = false;
    };
  }, [course.code]);

  const byFact = useMemo(() => indexByFact(course), [course]);

  const topics = useMemo(() => {
    if (!ledger) return [];
    return course.modules.map((mod) => {
      const facts = ledger.filter((f) => f.topic === mod.number);
      const states = facts.map((f) => ({ f, state: factState(f.id, byFact, mastery) }));
      return {
        mod,
        total: facts.length,
        solid: states.filter((s) => s.state === 'solid').length,
        shaky: states.filter((s) => s.state === 'shaky'),
        untested: states.filter((s) => s.state === 'untested'),
      };
    });
  }, [ledger, course.modules, byFact, mastery]);

  const questionsFor = (facts: { f: LedgerFact }[]): Question[] => {
    const seen = new Set<string>();
    const out: Question[] = [];
    for (const { f } of facts) {
      for (const q of byFact.get(f.id) ?? []) {
        if (!seen.has(q.id)) {
          seen.add(q.id);
          out.push(q);
        }
      }
    }
    return out;
  };

  if (failed) {
    return (
      <div className="card">
        <h2>The fact map could not be loaded</h2>
        <p className="help">
          The drill itself is unaffected. Try again, or go back and set up a test.
        </p>
        <button type="button" className="btn" onClick={onBack}>
          Back to setup
        </button>
      </div>
    );
  }

  if (!ledger) {
    return (
      <div className="card">
        <h2>Working out where you stand</h2>
        <p className="help">Loading the fact list for {course.code}.</p>
      </div>
    );
  }

  const all = topics.reduce(
    (t, x) => ({
      total: t.total + x.total,
      solid: t.solid + x.solid,
      shaky: t.shaky + x.shaky.length,
      untested: t.untested + x.untested.length,
    }),
    { total: 0, solid: 0, shaky: 0, untested: 0 }
  );

  return (
    <>
      <div className="card">
        <h2>Every fact in {course.code}, and where you stand on it</h2>
        <p className="help">
          {all.total} facts drawn from the course text, the lecture decks and the real
          tests. A fact counts as shaky the moment your last answer on it was wrong,
          because being right about something once and wrong twice is not knowing it.
        </p>
        <div className="statrow">
          <span className="stat-tile ok">
            <b>{all.solid}</b> solid
          </span>
          <span className="stat-tile warn">
            <b>{all.shaky}</b> shaky
          </span>
          <span className="stat-tile">
            <b>{all.untested}</b> never asked
          </span>
        </div>
        <div className="footer-actions">
          {all.shaky > 0 && (
            <button
              type="button"
              className="btn"
              onClick={() =>
                onDrill(
                  questionsFor(topics.flatMap((t) => t.shaky)),
                  `Every shaky fact · ${all.shaky} facts`
                )
              }
            >
              Drill every shaky fact
            </button>
          )}
          {all.untested > 0 && (
            <button
              type="button"
              className="btn ghost"
              onClick={() =>
                onDrill(
                  questionsFor(topics.flatMap((t) => t.untested)),
                  `Never asked · ${all.untested} facts`
                )
              }
            >
              Drill what I have never been asked
            </button>
          )}
          <button type="button" className="btn ghost" onClick={onBack}>
            Back to setup
          </button>
        </div>
      </div>

      {topics.map((t) => {
        const pct = t.total ? Math.round((t.solid / t.total) * 100) : 0;
        const isOpen = open === t.mod.number;
        return (
          <div className="card" key={t.mod.number}>
            <button
              type="button"
              className="factrow"
              aria-expanded={isOpen}
              onClick={() => setOpen(isOpen ? null : t.mod.number)}
            >
              <span>
                <span className="t">
                  {course.moduleNoun} {t.mod.number}: {t.mod.title}
                </span>
                <br />
                <span className="b">
                  {t.solid} solid · {t.shaky.length} shaky · {t.untested.length} never
                  asked
                </span>
              </span>
              <span className="factbar" aria-hidden="true">
                <i style={{ width: `${pct}%` }} />
              </span>
              <span className="cnt">{isOpen ? 'Hide' : 'Show'}</span>
            </button>

            {isOpen && (
              <div style={{ marginTop: 12 }}>
                {t.shaky.length > 0 && (
                  <>
                    <p className="whyhead">Shaky, your last answer was wrong</p>
                    <ul className="plain factlist">
                      {t.shaky.map(({ f }) => (
                        <li key={f.id}>{f.fact}</li>
                      ))}
                    </ul>
                  </>
                )}
                {t.untested.length > 0 && (
                  <>
                    <p className="whyhead">Never asked</p>
                    <ul className="plain factlist">
                      {t.untested.map(({ f }) => (
                        <li key={f.id}>{f.fact}</li>
                      ))}
                    </ul>
                  </>
                )}
                {t.shaky.length === 0 && t.untested.length === 0 && (
                  <p className="note">
                    Every fact in this {course.moduleNoun.toLowerCase()} is solid.
                  </p>
                )}
                {(t.shaky.length > 0 || t.untested.length > 0) && (
                  <button
                    type="button"
                    className="btn"
                    style={{ marginTop: 12 }}
                    onClick={() =>
                      onDrill(
                        questionsFor([...t.shaky, ...t.untested]),
                        `${course.moduleNoun} ${t.mod.number} · what is still soft`
                      )
                    }
                  >
                    Drill these {t.shaky.length + t.untested.length} facts
                  </button>
                )}
              </div>
            )}
          </div>
        );
      })}
    </>
  );
}
