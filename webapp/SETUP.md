# Setting up the TMC221 drill platform

Four things to do, in this order. The app is built so that **every one of them is
optional**: with nothing configured it still runs and still marks you, it just keeps
your history in the browser instead of your account. So you can deploy first and add
sign-in later without touching code.

Total time, first run through: about 20 minutes.

---

## Step 1. Deploy to Vercel (5 minutes)

The repo root is the manual composer, and the app lives in a subfolder, so the one
setting that matters is the root directory.

1. Go to <https://vercel.com/new> and import `VictorAyo25/textmaker`.
2. When it asks for configuration:
   - **Root Directory**: click Edit and choose `webapp`. This is the important one.
   - **Framework Preset**: it should read **Next.js**. If it still says "Other", change
     it. `webapp/vercel.json` also declares the framework, so a fresh import gets this
     right on its own, but the value shown in the UI wins for an existing project.
   - Leave the build and output settings alone.
3. Deploy.

> If a deployment fails with **`No Output Directory named "public" found after the
> Build completed`**, this is the cause: the preset is on "Other", so Vercel builds the
> app and then looks for a plain static folder that a Next.js app never produces. Set
> Framework Preset to Next.js in Settings then Build and Deployment, and redeploy.

You now have a working drill at `https://<something>.vercel.app`. Note that URL, the
next two steps need it.

Every push to `main` redeploys automatically from now on.

---

## Step 2. Google sign-in (8 minutes)

This is what lets your results follow you from laptop to phone.

1. Open <https://console.cloud.google.com/> and create a project (name it anything,
   for example `tmc-drill`).
2. In the sidebar: **APIs and Services** then **OAuth consent screen**.
   - User type: **External**. Create.
   - App name: `TMC221 Drill`. Support email and developer email: your own.
   - Scopes: skip, the defaults are what we use.
   - Test users: add your own Gmail address, and any classmate who should get in
     while the app is unpublished. Save.
3. Sidebar: **Credentials** then **Create Credentials** then **OAuth client ID**.
   - Application type: **Web application**.
   - **Authorised JavaScript origins**, add both:
     - `http://localhost:3000`
     - `https://<your-app>.vercel.app`
   - **Authorised redirect URIs**, add both:
     - `http://localhost:3000/api/auth/callback/google`
     - `https://<your-app>.vercel.app/api/auth/callback/google`
   - Create. Copy the **Client ID** and **Client secret**.
4. Generate a session secret. In any terminal:

   ```bash
   openssl rand -base64 32
   ```

   If `openssl` is not available, use `node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"`.

5. In Vercel: **Project** then **Settings** then **Environment Variables**. Add these
   three, for Production, Preview and Development:

   | Name | Value |
   | --- | --- |
   | `GOOGLE_CLIENT_ID` | the client ID from step 3 |
   | `GOOGLE_CLIENT_SECRET` | the client secret from step 3 |
   | `NEXTAUTH_SECRET` | the random string from step 4 |

   Vercel sets `NEXTAUTH_URL` for you on its own domains, so you do not need it there.

6. Redeploy (Deployments, then the three dots on the latest, then Redeploy).

The header now offers **Sign in with Google**. Until step 3 is done, signing in works
but there is still nowhere to store results, so history stays local.

> While the consent screen is in Testing mode only the test users you listed can sign
> in. That is usually what you want. To open it to anyone, hit **Publish app** on the
> OAuth consent screen.

---

## Step 3. Supabase, for cross-device results (6 minutes)

1. Go to <https://supabase.com/dashboard>, **New project**. Pick a name, a strong
   database password and the region closest to you. Wait for it to finish building.
2. Open **SQL Editor**, paste all of this, and run it:

   ```sql
   create table if not exists public.attempts (
     id          bigserial primary key,
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

   create index if not exists attempts_user_created_idx
     on public.attempts (user_email, created_at desc);

   -- The app reaches this table only through its own server routes, which have
   -- already checked who you are. RLS with no policy means nothing can read it
   -- with the public key even if that key ever leaks.
   alter table public.attempts enable row level security;
   ```

3. Go to **Project Settings** then **API** and copy two values:
   - **Project URL**
   - **service_role** secret (under Project API keys; reveal it first)

4. Add two more environment variables in Vercel, same three environments as before:

   | Name | Value |
   | --- | --- |
   | `NEXT_PUBLIC_SUPABASE_URL` | the Project URL |
   | `SUPABASE_SERVICE_ROLE_KEY` | the service_role secret |

5. Redeploy.

The attempts card now says results are saved to your account.

> The service role key bypasses row level security, which is why it is only ever read
> inside `app/api/attempts/route.ts` on the server and is never sent to the browser.
> Do not add it to any variable whose name starts with `NEXT_PUBLIC_`.

---

## Step 4. Running it on your own machine (optional)

```bash
cd webapp
npm install
cp .env.example .env.local     # then paste the same values in
npm run dev                    # http://localhost:3000
```

`npm run build` runs the bank gate first, so a malformed question or an untested slide
stops the build before it can reach Vercel.

---

## What is stored, and where

| Thing | Where it lives | Why |
| --- | --- | --- |
| The 560+ questions | JSON in this repo | Reviewed in diffs next to the manual they came from, and gated on every build |
| Your attempt history | Supabase `attempts` | So it follows you across devices |
| A local copy of recent attempts | Browser localStorage | So the app still shows history when signed out or offline |
| Your identity | Google, via a JWT session | No passwords are stored anywhere |

Adding a second course later means dropping `data/<code>/*.json` in the same shape and
registering it in `data/courses.ts`. No database change, no schema change.
