import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { authEnabled } from '@/lib/auth';
import { COURSES, findCourse } from '@/data/courses';
import { courseHasCrashCourse } from '@/data/lessons';
import Providers from '@/components/Providers';
import App from '@/components/App';

// One route per course, so the browser's back button and a shared link both
// behave. The server component exists to resolve the course and to tell the
// client whether sign-in is configured, without another public env var to keep
// in step.

export function generateStaticParams() {
  return COURSES.map((c) => ({ course: c.code.toLowerCase() }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ course: string }>;
}): Promise<Metadata> {
  const { course } = await params;
  const found = findCourse(course);
  if (!found) return { title: 'Course not found' };
  return {
    title: `${found.code} Drill`,
    description: `Active-recall testing for ${found.code} ${found.title}, built from the study manual.`,
  };
}

export default async function Page({
  params,
}: {
  params: Promise<{ course: string }>;
}) {
  const { course } = await params;
  const found = findCourse(course);
  if (!found) notFound();
  return (
    <Providers>
      <App
        code={found.code}
        authEnabled={authEnabled}
        hasCrashCourse={courseHasCrashCourse(found.code)}
      />
    </Providers>
  );
}
