-- CU Drill: the whole database, in one paste.
--
-- Run this once in the Supabase SQL editor (left sidebar, "SQL Editor", then
-- "New query", paste, Run). It creates both tables the app uses. Running it a
-- second time is harmless: everything is "if not exists".
--
-- Until this exists the app still works. Both sync endpoints report
-- synced:false and every device keeps its own browser copy, which is exactly
-- how the platform behaved before sync was added.

-- ---------------------------------------------------------------------------
-- 1. Attempt history: one row per test you finish, per account.
-- ---------------------------------------------------------------------------
create table if not exists public.attempts (
  id          bigint generated always as identity primary key,
  user_email  text        not null,
  user_name   text,
  course      text        not null default 'TMC221',
  title       text        not null default '',
  percent     numeric     not null default 0,
  total       integer     not null default 0,
  earned      numeric     not null default 0,
  detail      jsonb,
  created_at  timestamptz not null default now()
);

create index if not exists attempts_email_course_idx
  on public.attempts (user_email, course, created_at desc);

-- ---------------------------------------------------------------------------
-- 2. Crash-course progress: one row per account per course.
-- ---------------------------------------------------------------------------
create table if not exists public.lesson_progress (
  user_email  text        not null,
  course      text        not null,
  progress    jsonb       not null default '{}'::jsonb,
  updated_at  timestamptz not null default now(),
  primary key (user_email, course)
);

create index if not exists lesson_progress_email_idx
  on public.lesson_progress (user_email);

-- ---------------------------------------------------------------------------
-- 3. Lock both tables.
-- ---------------------------------------------------------------------------
-- Row level security is ON with NO public policy, which means the anon key can
-- read and write nothing. The app never touches these tables from the browser:
-- every read and write goes through a route handler that resolves the email
-- from the signed-in session and uses the service-role key. So the browser
-- cannot ask for somebody else's rows, because the browser cannot ask at all.
alter table public.attempts        enable row level security;
alter table public.lesson_progress enable row level security;
