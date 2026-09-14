/**
 * The listing a code question is about, drawn as a monospace block under the
 * prompt. Rendered as a text child, never as HTML, so a listing full of < and &
 * reaches the reader exactly as written and a bank file stays plain text.
 */
export function QCode({ code }: { code?: string }) {
  if (!code) return null;
  return <pre className="qcode">{code}</pre>;
}
