import type { Lesson } from '@/lib/types';
import ift222Lessons from './ift222/lessons.json';
import phy121Lessons from './phy121/lessons.json';
import dts224Lessons from './dts224/lessons.json';

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
  }));
}

export function courseHasCrashCourse(code: string): boolean {
  return lessonsFor(code).length > 0;
}
