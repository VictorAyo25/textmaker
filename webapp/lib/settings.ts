/**
 * Per-reader settings, local first and synced to the account.
 *
 * Right now that means one thing: which courses this reader has already sat.
 * The course table carries a `taken` flag, but that is the AUTHOR's answer, and
 * two people using the platform have sat different papers. So the flag becomes
 * the starting position and the reader's own list takes over the moment they
 * touch it.
 *
 * Same shape as lib/progress.ts on purpose: the browser copy is the working
 * copy so nothing waits on the network, the account's copy is folded in on
 * load, and writes are debounced.
 */
export interface Settings {
  /** Course codes this reader has sat. Absent means "use the author's flags". */
  archived?: string[];
}

const KEY = 'drill-settings-v1';

export function readSettings(): Settings {
  if (typeof window === 'undefined') return {};
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as Settings) : {};
  } catch {
    return {};
  }
}

export function writeSettings(s: Settings): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(KEY, JSON.stringify(s));
  } catch {
    /* private mode or a full quota: settings are a convenience, never a blocker */
  }
}

/**
 * Combine two settings objects without losing a decision.
 *
 * Archiving is a deliberate act and un-archiving is too, so neither side can be
 * merged automatically without guessing. The one with more entries wins, which
 * keeps the common case right: a reader who has been marking papers off on one
 * device does not lose them by opening a fresh browser somewhere else.
 */
export function mergeSettings(local: Settings, remote: Settings): Settings {
  if (!remote.archived) return local;
  if (!local.archived) return remote;
  return remote.archived.length >= local.archived.length ? remote : local;
}

export async function pullSettings(): Promise<Settings> {
  const local = readSettings();
  if (typeof window === 'undefined') return local;
  try {
    const r = await fetch('/api/settings');
    if (!r.ok) return local;
    const body = (await r.json()) as { synced?: boolean; settings?: Settings | null };
    if (!body.synced || !body.settings) return local;
    const merged = mergeSettings(local, body.settings);
    writeSettings(merged);
    return merged;
  } catch {
    return local;
  }
}

let pending: ReturnType<typeof setTimeout> | undefined;

export function pushSettings(s: Settings, delay = 800): void {
  if (typeof window === 'undefined') return;
  clearTimeout(pending);
  pending = setTimeout(() => {
    void fetch('/api/settings', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ settings: s }),
    }).catch(() => {
      /* offline, or signed out: the browser copy is still correct */
    });
  }, delay);
}

/**
 * Which courses count as sat, for this reader.
 *
 * Until they have expressed an opinion, the author's `taken` flags stand, so an
 * exam that is genuinely behind everyone is filed away without anyone doing
 * anything. After that, their list is the answer, including when it is empty.
 */
export function archivedSet(s: Settings, authorTaken: string[]): Set<string> {
  return new Set(s.archived ?? authorTaken);
}

export function toggleArchived(s: Settings, authorTaken: string[], code: string): Settings {
  const next = archivedSet(s, authorTaken);
  if (next.has(code)) next.delete(code);
  else next.add(code);
  return { ...s, archived: [...next] };
}
