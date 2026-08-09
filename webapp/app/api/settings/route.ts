import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '@/lib/auth';
import { supabaseAdmin } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

/**
 * Per-reader settings, one row per account.
 *
 * Currently just the list of courses they have already sat, but the column is a
 * jsonb blob so the next setting needs no migration.
 *
 * Not signed in, or no Supabase configured: 200 with `synced: false`, never an
 * error. The browser copy then stands alone.
 */

export async function GET() {
  const session = await getServerSession(authOptions);
  const db = supabaseAdmin();
  const email = session?.user?.email;
  if (!db || !email) return NextResponse.json({ synced: false, settings: null });

  const { data, error } = await db
    .from('user_settings')
    .select('settings')
    .eq('user_email', email)
    .maybeSingle();

  if (error) {
    console.error('settings read failed', error.message);
    return NextResponse.json({ synced: false, settings: null });
  }
  return NextResponse.json({ synced: true, settings: data?.settings ?? null });
}

export async function POST(request: Request) {
  const session = await getServerSession(authOptions);
  const db = supabaseAdmin();
  const email = session?.user?.email;
  if (!db || !email) return NextResponse.json({ synced: false });

  let body: { settings?: unknown };
  try {
    body = (await request.json()) as { settings?: unknown };
  } catch {
    return NextResponse.json({ error: 'bad json' }, { status: 400 });
  }
  if (typeof body.settings !== 'object' || body.settings === null) {
    return NextResponse.json({ error: 'bad payload' }, { status: 400 });
  }

  const { error } = await db.from('user_settings').upsert(
    {
      user_email: email,
      settings: body.settings,
      updated_at: new Date().toISOString(),
    },
    { onConflict: 'user_email' }
  );

  if (error) {
    console.error('settings write failed', error.message);
    return NextResponse.json({ synced: false });
  }
  return NextResponse.json({ synced: true });
}
