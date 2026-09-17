import type { Lesson } from '@/lib/types';
import ift222Lessons from './ift222/lessons.json';
import phy121Lessons from './phy121/lessons.json';
import dts224Lessons from './dts224/lessons.json';
import csc242Lessons from './csc242/lessons.json';
import ins224Lessons from './ins224/lessons.json';
import cos221Lessons from './cos221/lessons.json';
import csc241Lessons from './csc241/lessons.json';

/**
 * Crash-course lessons, kept OUT of data/courses.ts on purpose.
 *
 * courses.ts is imported by the client drill, and the lesson bodies are a few
 * hundred kilobytes of teaching HTML. Importing them here means only the learn
 * routes touch them, and only the one lesson being read is ever serialised down
 * to the browser.
 *
 * A course with no crash course simply has no entry, and the platform hides
 * every trace of the section for it.
 */
const BY_COURSE: Record<string, Lesson[]> = {
  IFT222: ift222Lessons as unknown as Lesson[],
  PHY121: phy121Lessons as unknown as Lesson[],
  DTS224: dts224Lessons as unknown as Lesson[],
  CSC242: csc242Lessons as unknown as Lesson[],
  INS224: ins224Lessons as unknown as Lesson[],
  COS221: cos221Lessons as unknown as Lesson[],
  CSC241: csc241Lessons as unknown as Lesson[],
};

export function lessonsFor(code: string): Lesson[] {
  return BY_COURSE[code.toUpperCase()] ?? [];
}

export function lessonBySlug(code: string, slug: string): Lesson | undefined {
  return lessonsFor(code).find((l) => l.slug === slug);
}

/** Enough to draw the index without shipping a single lesson body. */
export interface LessonCard {
  slug: string;
  part: string;
  kick: string;
  title: string;
  lead: string;
  minutes: number;
  modules: number[];
  frames: number;
  worked: number;
  recalls: number;
  /** A Learn by doing paper, which lives in its own section. */
  revision: boolean;
}

export function lessonCards(code: string): LessonCard[] {
  return lessonsFor(code).map((l) => ({
    slug: l.slug,
    part: l.part,
    kick: l.kick,
    title: l.title,
    lead: l.lead,
    minutes: l.minutes,
    modules: l.modules,
    frames: l.blocks
      .filter((b) => b.kind === 'frames')
      .reduce((t, b) => t + (b.kind === 'frames' ? b.frames.length : 0), 0),
    worked: l.blocks.filter((b) => b.kind === 'worked').length,
    recalls: l.blocks.filter((b) => b.kind === 'recall').length,
    revision: Boolean(l.revision),
  }));
}

export function courseHasCrashCourse(code: string): boolean {
  return lessonsFor(code).length > 0;
}

/** The Learn by doing papers: one module sat whole, in their own section. */
export function doingCards(code: string): LessonCard[] {
  return lessonCards(code).filter((c) => c.revision);
}

export function courseHasDoing(code: string): boolean {
  return lessonsFor(code).some((l) => l.revision);
}

/**
 * Where a lesson lives. A Learn by doing paper has its own section and its own
 * route, so every link to one has to be built here rather than by hand, or a
 * link sends the reader to a page that no longer serves it.
 */
export function lessonHref(code: string, lesson: { slug: string; revision?: boolean }): string {
  return `/${code.toLowerCase()}/${lesson.revision ? 'doing' : 'learn'}/${lesson.slug}`;
}
