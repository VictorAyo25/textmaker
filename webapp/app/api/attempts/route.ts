import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '@/lib/auth';
import { supabaseAdmin } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

/**
 * Attempt history, scoped to the signed-in Google account.
 *
 * Not signed in, or no Supabase configured: 200 with an empty list and
 * `synced: false`, never an error. The client then uses local history. The
 * point is that the drill keeps working under every configuration.
 */

interface AttemptBody {
  course: string;
  title: string;
  percent: number;
  total: number;
  earned: number;
  detail?: unknown;
}

export async function GET(request: Request) {
  const session = await getServerSession(authOptions);
  const db = supabaseAdmin();
  const email = session?.user?.email;
  if (!db || !email) return NextResponse.json({ synced: false, attempts: [] });

  // Scoped to one course, so a TMC221 run never appears under IFT222. Rows
  // written before the platform took a second course all carry 'TMC221'.
  const course = new URL(request.url).searchParams.get('course');

  let query = db
    .from('attempts')
    .select('id, course, title, percent, total, earned, created_at')
    .eq('user_email', email);
  if (course) query = query.eq('course', course);

  const { data, error } = await query
    .order('created_at', { ascending: false })
    .limit(50);

  if (error) {
    console.error('attempts read failed', error.message);
    return NextResponse.json({ synced: false, attempts: [] });
  }
  return NextResponse.json({ synced: true, attempts: data ?? [] });
}

export async function POST(request: Request) {
  const session = await getServerSession(authOptions);
  const db = supabaseAdmin();
  const email = session?.user?.email;
  if (!db || !email) return NextResponse.json({ synced: false });

  let body: AttemptBody;
  try {
    body = (await request.json()) as AttemptBody;
  } catch {
    return NextResponse.json({ error: 'bad json' }, { status: 400 });
  }

  // Clamp what we trust from the client. A score is a claim, not a fact, but
  // this is a personal study tool: the only thing worth guarding is that a
  // malformed payload cannot poison the table.
  const row = {
    user_email: email,
    user_name: session?.user?.name ?? null,
    course: String(body.course ?? 'TMC221').slice(0, 32),
    title: String(body.title ?? '').slice(0, 200),
    percent: Math.max(0, Math.min(100, Number(body.percent) || 0)),
    total: Math.max(0, Math.min(1000, Math.floor(Number(body.total) || 0))),
    earned: Math.max(0, Math.min(1000, Number(body.earned) || 0)),
    detail: body.detail ?? null,
  };

  const { error } = await db.from('attempts').insert(row);
  if (error) {
    console.error('attempts write failed', error.message);
    return NextResponse.json({ synced: false });
  }
  return NextResponse.json({ synced: true });
}
