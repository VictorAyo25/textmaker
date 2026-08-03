import { createClient, type SupabaseClient } from '@supabase/supabase-js';

/**
 * Server-side Supabase client.
 *
 * Uses the SERVICE ROLE key, so it must only ever be imported from route
 * handlers, never from a component that ships to the browser. Every query it
 * runs is already scoped to the signed-in user's email by the route that calls
 * it, which is why the tables also carry row level security as a second lock.
 *
 * Returns null when the environment is not configured. Callers treat that as
 * "no sync available" and fall back to browser-local history, so a missing env
 * var degrades one feature instead of breaking the site.
 */
let cached: SupabaseClient | null | undefined;

export function supabaseAdmin(): SupabaseClient | null {
  if (cached !== undefined) return cached;
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  cached =
    url && key
      ? createClient(url, key, { auth: { persistSession: false } })
      : null;
  return cached;
}

export const syncEnabled = () =>
  Boolean(process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.SUPABASE_SERVICE_ROLE_KEY);
