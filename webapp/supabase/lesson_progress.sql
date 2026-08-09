-- Crash-course progress, carried between devices.
--
-- One row per account per course, holding the whole progress map. Run this once
-- in the Supabase SQL editor. Until it exists, /api/progress simply reports
-- synced:false and every device keeps its own browser copy, which is exactly
-- how the app behaved before sync was added.

create table if not exists public.lesson_progress (
  user_email  text        not null,
  course      text        not null,
  progress    jsonb       not null default '{}'::jsonb,
  updated_at  timestamptz not null default now(),
  primary key (user_email, course)
);

-- The service role is the only writer: every read and write goes through
-- /api/progress, which resolves the email from the session rather than trusting
-- anything the browser sends. So row-level security is on with no public policy.
alter table public.lesson_progress enable row level security;

create index if not exists lesson_progress_email_idx
  on public.lesson_progress (user_email);
