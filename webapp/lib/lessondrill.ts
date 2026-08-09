import type { Course, Lesson, Question } from '@/lib/types';

/**
 * Which questions a lesson's drill block asks.
 *
 * One rule, shared by the page that renders the lesson and the bank gate that
 * checks the crash course is complete, so the two can never disagree about what
 * "every test question relating to this lesson" means.
 *
 *   pick: 'exam' - only questions the examiner actually set, identified by the
 *                  course's examTags appearing in a question's provenance
 *   pick: 'all'  - every question in the lesson's topics
 *
 * Questions are matched on `module`, the drill topic, so a lesson teaching
 * topics 8 and 11 asks the exam questions from both. `ids` adds anything that
 * belongs to this lesson but sits under another topic.
 */
export function isExamQuestion(course: Course, q: Question): boolean {
  const tags = course.examTags ?? [];
  return tags.length > 0 && q.slides.some((s) => tags.some((t) => s.startsWith(t)));
}

export function drillQuestions(
  course: Course,
  lesson: Lesson,
  block: { pick: 'exam' | 'all'; topics?: number[]; ids?: string[] }
): Question[] {
  const wanted = new Set(block.topics ?? lesson.modules);
  const extra = new Set(block.ids ?? []);
  const picked = course.questions.filter((q) => {
    if (extra.has(q.id)) return true;
    if (!wanted.has(q.module)) return false;
    return block.pick === 'all' || isExamQuestion(course, q);
  });
  // Exam order, so the reader meets them as the paper set them, then anything
  // authored afterwards.
  return picked.sort((a, b) => order(course, a) - order(course, b));
}

function order(course: Course, q: Question): number {
  for (const tag of course.examTags ?? []) {
    const hit = q.slides.find((s) => s.startsWith(tag));
    if (hit) {
      const n = Number(hit.match(/Q(\d+)$/)?.[1] ?? 0);
      return (course.examTags ?? []).indexOf(tag) * 1000 + n;
    }
  }
  return 1e6;
}
