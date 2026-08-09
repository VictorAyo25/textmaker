import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '@/lib/auth';
import { supabaseAdmin } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

/**
 * Crash-course progress, carried between devices for the signed-in account.
 *
 * One row per account per course, holding the whole progress map as JSON. It is
 * small: a slug, a frame count and a handful of self-marks per lesson. Writing
 * it whole avoids any per-lesson row bookkeeping, and the client debounces, so
 * reading a lesson costs one write a few seconds after you stop, not one per
 * button press.
 *
 * Not signed in, or no Supabase configured: 200 with `synced: false` and no
 * data, never an error. The browser copy then stands alone, exactly as before.
 * Nothing about the crash course may depend on being online.
 */

export async function GET(request: Request) {
  const session = await getServerSession(authOptions);
  const db = supabaseAdmin();
  const email = session?.user?.email;
  if (!db || !email) return NextResponse.json({ synced: false, progress: null });

  const course = new URL(request.url).searchParams.get('course') ?? '';
  const { data, error } = await db
    .from('lesson_progress')
    .select('progress, updated_at')
    .eq('user_email', email)
    .eq('course', course)
    .maybeSingle();

  if (error) {
    console.error('progress read failed', error.message);
    return NextResponse.json({ synced: false, progress: null });
  }
  return NextResponse.json({
    synced: true,
    progress: data?.progress ?? null,
    updated_at: data?.updated_at ?? null,
  });
}

export async function POST(request: Request) {
  const session = await getServerSession(authOptions);
  const db = supabaseAdmin();
  const email = session?.user?.email;
  if (!db || !email) return NextResponse.json({ synced: false });

  let body: { course?: string; progress?: unknown };
  try {
    body = (await request.json()) as { course?: string; progress?: unknown };
  } catch {
    return NextResponse.json({ error: 'bad json' }, { status: 400 });
  }

  const course = String(body.course ?? '').slice(0, 32);
  if (!course || typeof body.progress !== 'object' || body.progress === null) {
    return NextResponse.json({ error: 'bad payload' }, { status: 400 });
  }

  const { error } = await db.from('lesson_progress').upsert(
    {
      user_email: email,
      course,
      progress: body.progress,
      updated_at: new Date().toISOString(),
    },
    { onConflict: 'user_email,course' }
  );

  if (error) {
    console.error('progress write failed', error.message);
    return NextResponse.json({ synced: false });
  }
  return NextResponse.json({ synced: true });
}
