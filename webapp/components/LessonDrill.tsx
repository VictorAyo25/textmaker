'use client';

import { useState } from 'react';
import type { Course, Question, Response } from '@/lib/types';
import QuestionView from '@/components/QuestionView';
import Feedback from '@/components/Feedback';
import { Figure } from '@/components/Figure';
import { Sci } from '@/components/Sci';
import { mark } from '@/lib/grading';

/**
 * The examiner's own questions, asked inside the lesson that teaches them.
 *
 * A crash course that teaches a skill and then sends you elsewhere to be tested
 * on it is not self-sufficient: the reader has to go and find the questions,
 * and in practice does not. So every question the examiner actually set on this
 * lesson's topics is answered here, marked here, and explained here.
 *
 * The questions are NOT copied into the lesson file. They are selected from the
 * one bank at render time, so a correction to a question reaches the drill and
 * the lesson together and the two can never disagree.
 */
export default function LessonDrill({
  course,
  questions,
  label,
  tag,
}: {
  course: Course;
  questions: Question[];
  label: string;
  tag: string;
}) {
  const [responses, setResponses] = useState<Record<string, Response | null>>({});
  const [shown, setShown] = useState<Record<string, boolean>>({});

  const done = questions.filter((q) => shown[q.id]).length;
  const right = questions.filter(
    (q) => shown[q.id] && mark(q, responses[q.id] ?? null).correct
  ).length;

  return (
    <section className="block lessondrill">
      <div className="blabel">
        <span className="bkind">{label}</span>
        {tag && <span className="btag">{tag}</span>}
      </div>
      <p className="help">
        Every question the examiner set on this lesson. Answer each one, then check
        it: the verdict explains why the key is the key and what is wrong with each
        other option.
      </p>
      {done > 0 && (
        <p className="note">
          {right} of {done} right so far, {questions.length - done} still to do.
        </p>
      )}

      {questions.map((q, i) => {
        const r = responses[q.id] ?? null;
        const open = shown[q.id];
        const marked = open ? mark(q, r) : null;
        return (
          <div className="ldq" key={q.id}>
            <p className="ldnum">
              Question {i + 1} of {questions.length}
              {q.slides.length > 0 && <span className="ldsrc">{q.slides[0]}</span>}
            </p>
            <p className="ldprompt">
              <Sci text={q.prompt.replace(/\{\{(\d+)\}\}/g, '____')} />
            </p>
            {q.figure && <Figure figure={q.figure} />}
            <QuestionView
              question={q}
              response={r}
              onChange={(next) => setResponses((s) => ({ ...s, [q.id]: next }))}
              gapMode="choice"
              readOnly={open}
            />
            {!open && (
              <button
                type="button"
                className="btn"
                style={{ marginTop: 12 }}
                onClick={() => setShown((s) => ({ ...s, [q.id]: true }))}
              >
                Check answer
              </button>
            )}
            {marked && (
              <div className="instant" aria-live="polite">
                <Feedback course={course} m={marked} showPrompt={false} />
              </div>
            )}
          </div>
        );
      })}
    </section>
  );
}
