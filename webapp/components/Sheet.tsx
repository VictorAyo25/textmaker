'use client';

import { useEffect, useState } from 'react';
import { Sci } from '@/components/Sci';
import { Figure } from '@/components/Figure';
import { QCode } from '@/components/QCode';
import type { Course, Question } from '@/lib/types';
import { WhyGrid, rightAnswer } from './Feedback';
import { letterOf, optionsOf } from '@/lib/bank';

/**
 * A printable sheet of questions with their answers.
 *
 * This is the take-it-away view: pick topics, get every question in them, each
 * with its answer, its explanation, every option's verdict and the source it
 * came from. Saving it as a PDF is the browser's own print dialog, which keeps
 * the text selectable and searchable and costs the bundle nothing.
 */

/** Blank markers are for answering on screen; on paper they are just rules. */
function readable(prompt: string): string {
  return prompt.replace(/\{\{(\d+)\}\}/g, '________');
}

/**
 * The options as the reader sees them on paper.
 *
 * Every line carries its own letter, so the list must not also be numbered by
 * the browser, or each option arrives as "1. A. ...". A matching question is
 * skipped entirely: the answer line below already prints every pair, and the
 * left-hand column on its own tells the reader nothing.
 */
function OptionList({ q }: { q: Question }) {
  if (q.style === 'tf' || q.options?.length) {
    return (
      <ul className="sheetopts">
        {optionsOf(q).map((o) => (
          <li key={o.id}>
            <b>{letterOf(q, o.id)}.</b> <Sci text={o.text} />
          </li>
        ))}
      </ul>
    );
  }
  if (q.blanks?.length) {
    return (
      <p className="note" style={{ margin: '4px 0 0' }}>
        {q.blanks.length} blank{q.blanks.length === 1 ? '' : 's'}. Choices:{' '}
        {q.blanks.map((b) => b.choices.join(', ')).join('  |  ')}
      </p>
    );
  }
  return null;
}

interface Props {
  course: Course;
  questions: Question[];
  title: string;
  onBack: () => void;
}

export default function Sheet({ course, questions, title, onBack }: Props) {
  // Rendered only after an interaction, so reading the clock here cannot make
  // the server and the first client paint disagree.
  const [stamp, setStamp] = useState('');
  useEffect(() => setStamp(new Date().toLocaleDateString()), []);

  return (
    <>
      <div className="card noprint">
        <h2>Printable sheet: {questions.length} questions</h2>
        <p className="help">
          Every question below carries its answer, its explanation, the verdict on each
          option and the reference it came from. Use your browser&apos;s print dialog and
          choose Save as PDF for a copy you can keep.
        </p>
        <div className="footer-actions">
          <button type="button" className="btn" onClick={() => window.print()}>
            Save as PDF
          </button>
          <button type="button" className="btn ghost" onClick={onBack}>
            Back to setup
          </button>
        </div>
      </div>

      <div className="sheet">
        <div className="sheethead">
          <h2>
            {course.code} {course.title}
          </h2>
          <p>{title}</p>
          <p className="note">
            {questions.length} questions with answers{stamp ? ` · ${stamp}` : ''}
          </p>
        </div>

        {questions.map((q, i) => (
          <div className="sheetq" key={q.id}>
            <p className="sheetnum">
              {i + 1}. <Sci text={readable(q.prompt)} />
            </p>
            {q.figure && <Figure figure={q.figure} />}
            <QCode code={q.code} />
            <OptionList q={q} />
            <p className="theirs">
              Answer: <b>{rightAnswer(q)}</b>
            </p>
            <p className="why"><Sci text={q.explanation} /></p>
            <WhyGrid q={q} />
            <div className="qmeta" style={{ marginTop: 6 }}>
              {q.slides.map((s) => (
                <span className="tag slide" key={s}>
                  {s}
                </span>
              ))}
              <span className="tag">
                {course.moduleNoun} {q.module}
              </span>
              <span className={`tag ${q.difficulty}`}>{q.difficulty}</span>
              <span className="tag">{q.topic}</span>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
