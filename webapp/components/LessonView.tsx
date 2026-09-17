'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import type { Course, Frame, Lesson, LessonBlock, Question } from '@/lib/types';
import {
  lessonProgressKey,
  pullProgress,
  pushProgress,
  readProgress,
  writeProgress,
} from '@/lib/progress';
import LessonDrill from '@/components/LessonDrill';
import { longDate } from '@/data/timetable';

/** Repository HTML lifted from the manual, never user input. */
function Html({ html, className }: { html: string; className?: string }) {
  return <div className={className} dangerouslySetInnerHTML={{ __html: html }} />;
}

/**
 * The same, inline.
 *
 * Checks and answers carry real markup: 16<sup>2</sup>, bold terms, the odd
 * entity. Flattening them to text would print "162" where the manual prints
 * "16 squared", which is a wrong answer on a page whose whole job is to be
 * right.
 */
function Inline({ html, className }: { html: string; className?: string }) {
  return <span className={className} dangerouslySetInnerHTML={{ __html: html }} />;
}

/** Does this frame's teaching hold block content: paragraphs, listings, tables? */
const BLOCK_RE = /<(p|pre|table|ul|ol|div|figure|h\d)\b/i;
const isBlock = (html: string) => BLOCK_RE.test(html);

/** Put the check back at the head of the frame's first paragraph, or on a line
 *  of its own when the frame opens with something that is not a paragraph. */
function withCheck(check: string, teach: string): string {
  if (!check) return teach;
  const chk = `<span class="chk">${check}</span> `;
  return /^\s*<p>/.test(teach) ? teach.replace(/^\s*<p>/, `<p>${chk}`) : `<p>${chk}</p>${teach}`;
}

/**
 * The programmed frames.
 *
 * On paper the instruction is "cover the page with a card and slide it down".
 * Here the app holds the card: one frame at a time, and the check that answers
 * the question you are looking at does not exist on screen until you ask for
 * it. Frames already read stay above you, exactly as they would on the page.
 */
function Frames({
  block,
  reached,
  onReach,
}: {
  block: Extract<LessonBlock, { kind: 'frames' }>;
  reached: number;
  onReach: (n: number) => void;
}) {
  const total = block.frames.length;
  const shown = Math.min(Math.max(reached, 1), total);
  const next: Frame | undefined = block.frames[shown];

  return (
    <div className="lblock frames">
      <div className="lbar">
        <span>{block.label || 'Work it frame by frame'}</span>
        <span className="ltag">
          {shown} of {total}
        </span>
      </div>
      <div className="lbody">
        {block.howto && <Html className="howto" html={block.howto} />}
        <div className="frametrack">
          <i style={{ width: `${(shown / total) * 100}%` }} />
        </div>

        {block.frames.slice(0, shown).map((f, i) => (
          <div className={`frame ${i === shown - 1 ? 'live' : 'past'}`} key={i}>
            {isBlock(f.teach) ? (
              // A code course's frame holds paragraphs, a listing and the output it
              // printed. A <pre> cannot live inside a <p>: on a server render the
              // browser would close the paragraph early and scatter the frame. So a
              // frame with block content is a div, with the check opening its first
              // paragraph exactly where the print edition put it.
              <Html className="frbody" html={withCheck(f.check, f.teach)} />
            ) : (
              <p>
                {f.check && <Inline className="chk" html={f.check} />}{' '}
                <Inline html={f.teach} />
              </p>
            )}
            {f.ask && (
              <p className="askrow">
                <span className="asklab">Your turn</span>
                <Inline html={f.ask} />
              </p>
            )}
          </div>
        ))}

        {shown < total ? (
          <button type="button" className="btn wide" onClick={() => onReach(shown + 1)}>
            {next?.check ? 'Check my answer' : 'Continue'}
          </button>
        ) : (
          <p className="donebar">
            That is every frame in this skill. The facts are in; now prove them below.
          </p>
        )}
        {shown > 1 && (
          <button type="button" className="chip restart" onClick={() => onReach(1)}>
            Start these frames again
          </button>
        )}
      </div>
    </div>
  );
}

function Worked({ block }: { block: Extract<LessonBlock, { kind: 'worked' }> }) {
  // Shown by default, on Victor's instruction: he is revising against the clock
  // and wants to read, not click. The button still hides it, so the discipline
  // of attempting it first is a choice rather than something the page enforces.
  const [open, setOpen] = useState(true);
  const model = block.mode === 'model';
  return (
    <div className={`lblock worked ${model ? 'model' : ''}`}>
      <div className="lbar">
        <span>{block.label}</span>
        {block.tag && <span className="ltag">{block.tag}</span>}
      </div>
      <div className="lbody">
        {block.problem && <Html html={block.problem} />}
        {!open ? (
          <button type="button" className="btn ghost" onClick={() => setOpen(true)}>
            {model ? 'Show the model answer' : 'Show the working'}
          </button>
        ) : (
          <>
            <button type="button" className="btn ghost hideans" onClick={() => setOpen(false)}>
              {model ? 'Hide the model answer' : 'Hide the working'}
            </button>
            {block.working && <Html html={block.working} />}
            {block.answer && <Html className="answerbox" html={block.answer} />}
            {block.redo && <Html className="redo" html={block.redo} />}
          </>
        )}
        {!open && (
          <p className="note nudge">
            {model
              ? 'Attempt it on paper first. Reading a model answer you have not tried teaches you nothing.'
              : 'Try it yourself first, then check the working line by line.'}
          </p>
        )}
      </div>
    </div>
  );
}

function Recall({
  block,
  mark,
  onMark,
}: {
  block: Extract<LessonBlock, { kind: 'recall' }>;
  mark: 'right' | 'wrong' | null;
  onMark: (m: 'right' | 'wrong') => void;
}) {
  const [open, setOpen] = useState(true);
  return (
    <div className={`lblock recall ${mark ?? ''}`}>
      <div className="lbar">
        <span>{block.label || 'Your turn'}</span>
        {block.tag && <span className="ltag">{block.tag}</span>}
      </div>
      <div className="lbody">
        <Html html={block.question} />
        {!open ? (
          <button type="button" className="btn ghost" onClick={() => setOpen(true)}>
            Show the answer
          </button>
        ) : (
          <>
            <button type="button" className="btn ghost hideans" onClick={() => setOpen(false)}>
              Hide the answer
            </button>
            <p className="alabel">Answer</p>
            <Html html={block.answer} />
            <div className="markrow">
              <span className="note">Be honest, it only costs you now:</span>
              <button
                type="button"
                className="chip"
                aria-pressed={mark === 'right'}
                onClick={() => onMark('right')}
              >
                I got it
              </button>
              <button
                type="button"
                className="chip"
                aria-pressed={mark === 'wrong'}
                onClick={() => onMark('wrong')}
              >
                I missed it
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function Block({
  block,
  idx,
  reached,
  onReach,
  marks,
  onMark,
  course,
  drills,
}: {
  block: LessonBlock;
  idx: number;
  reached: number;
  onReach: (n: number) => void;
  marks: Record<string, 'right' | 'wrong'>;
  onMark: (key: string, m: 'right' | 'wrong') => void;
  course: Course;
  drills: Record<number, Question[]>;
}) {
  switch (block.kind) {
    case 'frames':
      return <Frames block={block} reached={reached} onReach={onReach} />;
    case 'worked':
      return <Worked block={block} />;
    case 'recall':
      return (
        <Recall
          block={block}
          mark={marks[String(idx)] ?? null}
          onMark={(m) => onMark(String(idx), m)}
        />
      );
    case 'asprinted':
      return (
        <div className="lblock paper">
          <div className="lbar">
            <span>{block.label || 'As printed'}</span>
            {block.tag && <span className="ltag">{block.tag}</span>}
          </div>
          <div className="lbody">
            {block.src && <p className="src">{block.src}</p>}
            <Html className="asprinted" html={block.printed} />
          </div>
        </div>
      );
    case 'rules':
    case 'trap':
    case 'teach':
      return (
        <div className={`lblock ${block.kind}`}>
          <div className="lbar">
            <span>{block.label || (block.kind === 'trap' ? 'Trap' : '')}</span>
            {block.tag && <span className="ltag">{block.tag}</span>}
          </div>
          <Html className="lbody" html={block.html} />
        </div>
      );
    case 'lockin':
      return (
        <div className="lockin">
          <span className="clab">Lock it in</span>
          <Html className="big" html={block.big} />
          {block.sub && <Html className="sub" html={block.sub} />}
        </div>
      );
    case 'heading':
      return <h2 className="lheading">{block.text}</h2>;
    case 'drill':
      return (
        <LessonDrill
          course={course}
          questions={drills[idx] ?? []}
          label={block.label}
          tag={block.tag}
        />
      );
    default:
      return <Html className="lprose" html={block.html} />;
  }
}

interface Props {
  code: string;
  lesson: Lesson;
  moduleTitles: Record<number, string>;
  moduleCounts: Record<number, number>;
  prev: { slug: string; title: string } | null;
  next: { slug: string; title: string } | null;
  /** Which lesson this is, and how many there are, so "Next" has a context. */
  position: number;
  total: number;
  /** The course, with its bank stripped: the drill blocks carry their own. */
  course: Course;
  /** Questions for each drill block, selected on the server by block index. */
  drills: Record<number, Question[]>;
  /** The dated sitting this lesson belongs to, where the course has a plan. */
  when?: { date: string; window: string } | null;
  /**
   * Which section this page is served from, "learn" or "doing", so Back and
   * Next stay inside it. A Learn by doing paper lives under /doing.
   */
  base?: 'learn' | 'doing';
}

export default function LessonView({
  code,
  lesson,
  moduleTitles,
  moduleCounts,
  prev,
  next,
  position,
  total,
  course,
  drills,
  when,
  base = 'learn',
}: Props) {
  const key = lessonProgressKey(code);
  const [reached, setReached] = useState(1);
  const [marks, setMarks] = useState<Record<string, 'right' | 'wrong'>>({});
  const [done, setDone] = useState(false);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    // Local first, so the lesson opens where you left it with no wait. Then the
    // account's copy is folded in, which is what makes picking this up on
    // another device work.
    const apply = (map: ReturnType<typeof readProgress>) => {
      const p = map[lesson.slug];
      if (p) {
        setReached((r) => Math.max(r, p.frames || 1));
        setMarks((m) => ({ ...p.marks, ...m }));
        setDone((d) => d || Boolean(p.done));
      }
    };
    apply(readProgress(key));
    setLoaded(true);
    let live = true;
    void pullProgress(key).then((map) => {
      if (live) apply(map);
    });
    return () => {
      live = false;
    };
  }, [key, lesson.slug]);

  const save = useCallback(
    (patch: { frames?: number; marks?: Record<string, 'right' | 'wrong'>; done?: boolean }) => {
      if (!loaded) return;
      const all = readProgress(key);
      all[lesson.slug] = { ...(all[lesson.slug] ?? {}), ...patch };
      writeProgress(key, all);
      pushProgress(key, all);
    },
    [key, lesson.slug, loaded]
  );

  const onReach = (n: number) => {
    setReached(n);
    save({ frames: n });
  };
  const onMark = (k: string, m: 'right' | 'wrong') => {
    const nextMarks = { ...marks, [k]: m };
    setMarks(nextMarks);
    save({ marks: nextMarks });
  };
  const toggleDone = () => {
    const v = !done;
    setDone(v);
    save({ done: v });
  };

  const recallCount = useMemo(
    () => lesson.blocks.filter((b) => b.kind === 'recall').length,
    [lesson]
  );
  const missed = Object.values(marks).filter((m) => m === 'wrong').length;
  const got = Object.values(marks).filter((m) => m === 'right').length;

  return (
    <>
      {/* The trail lives in the page's own Crumbs now, which also carries a
          route home; this used to be a partial one that only went up a level. */}
      <div className="card lessonhead">
        {when && (
          <p className="lwhen">
            <b>Read on {longDate(when.date)}</b>
            <span>{when.window}</span>
          </p>
        )}
        <span className="kick">{lesson.kick}</span>
        <h1>{lesson.title}</h1>
        <Html className="lead" html={lesson.lead} />
        <p className="note">
          About {lesson.minutes} minutes
          {lesson.modules.length > 0 && (
            <>
              {' '}
              &middot; drills{' '}
              {lesson.modules
                .map((m) => `${moduleTitles[m] ?? `Topic ${m}`}`)
                .join(' and ')}
            </>
          )}
        </p>
      </div>

      <div className="lesson">
        {lesson.blocks.map((b, i) => (
          <Block
            key={i}
            idx={i}
            block={b}
            reached={reached}
            onReach={onReach}
            marks={marks}
            onMark={onMark}
            course={course}
            drills={drills}
          />
        ))}
      </div>

      <div className="card">
        <h2>Finished this skill?</h2>
        {recallCount > 0 && (
          <p className="help">
            You marked yourself right on {got} of {recallCount} recall
            {recallCount === 1 ? '' : 's'}
            {missed > 0 && `, and missed ${missed}. Read those frames again before you move on.`}
            {missed === 0 && got > 0 && '. Now prove it against the real questions.'}
          </p>
        )}
        <div className="footer-actions">
          <button
            type="button"
            className={`btn ${done ? 'ghost' : ''}`}
            onClick={toggleDone}
          >
            {done ? 'Marked as done' : 'Mark this skill done'}
          </button>
          {lesson.modules.map((m) => (
            <Link
              key={m}
              className="btn ghost"
              href={`/${code.toLowerCase()}?topic=${m}`}
            >
              Drill it: {moduleTitles[m] ?? `Topic ${m}`} ({moduleCounts[m] ?? 0} Q)
            </Link>
          ))}
        </div>
      </div>

      {/* "Next" on its own tells you nothing about how much is left. Naming the
          position turns the footer into a progress indicator. */}
      <p className="lessonpos">
        {base === 'doing' ? 'Paper' : 'Lesson'} {position} of {total}
      </p>

      <div className="prevnext">
        {prev ? (
          <Link className="chip" href={`/${code.toLowerCase()}/${base}/${prev.slug}`}>
            Back: {prev.title}
          </Link>
        ) : (
          <span />
        )}
        {next && (
          <Link className="chip" href={`/${code.toLowerCase()}/${base}/${next.slug}`}>
            Next: {next.title}
          </Link>
        )}
      </div>
    </>
  );
}
