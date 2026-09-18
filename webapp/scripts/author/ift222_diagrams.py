"""Draw the diagrams IFT222's answers are asked for, and make the timing charts look drawn.

    python scripts/author/ift222_diagrams.py

Four questions on the two papers say draw, sketch or "include a diagram", and
three of them were answered without one:

  25/26 Q2(b)  the pipeline timing diagram existed as a cell grid but had no
               styling at all, so it rendered as a run of text
  25/26 Q3(b)  its two schedules, with and without forwarding, were plain text
  24/25 Q1(b)  "draw the diagrams representing the two scenarios", 3 of its 7
               marks, answered with formulas only
  24/25 Q4(a)  "include diagram for each", answered in prose, while the same
               pair of diagrams already existed under 25/26 Q1(a)

Idempotent: run it twice and nothing doubles.
"""
import json
import re
from pathlib import Path

WEBAPP = Path(__file__).resolve().parent.parent.parent
LESSONS = WEBAPP / "data" / "ift222" / "lessons.json"


def trace_table(cycles, rows):
    """A pipeline timing chart: one row an instruction, one column a cycle.

    rows is (label, first cycle, [stage per cycle]). An empty cell is a cycle
    that instruction has not reached yet.
    """
    head = "".join(f"<th>{c}</th>" for c in range(1, cycles + 1))
    body = []
    for label, start, stages in rows:
        cells = []
        for c in range(1, cycles + 1):
            i = c - start
            s = stages[i] if 0 <= i < len(stages) else ""
            cls = ""
            if s == "WB":
                cls = ' class="out"'
            elif s == "--":
                cls = ' class="stall"'
            cells.append(f"<td{cls}>{s}</td>")
        body.append(f"<tr><td>{label}</td>{''.join(cells)}</tr>")
    return (
        f'<table class="trace"><tr><th>Cyc</th>{head}</tr>{"".join(body)}</table>'
    )


def svg(width, height, body, caption, label):
    return (
        '<figure class="eerfig">'
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="sans-serif" font-size="12" role="img" aria-label="{label}">'
        '<defs><marker id="iftarrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 1 L 9 5 L 0 9 z" fill="currentColor"/></marker></defs>'
        + body
        + "</svg>"
        f"<figcaption>{caption}</figcaption></figure>"
    )


def box(x, y, w, h, label, sub=None):
    out = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="currentColor" '
        'stroke-width="1.4" rx="4"/>'
    ]
    cy = y + h / 2 + (0 if sub else 4)
    out.append(f'<text x="{x + w / 2}" y="{cy}" text-anchor="middle" font-weight="bold">{label}</text>')
    if sub:
        out.append(f'<text x="{x + w / 2}" y="{cy + 15}" text-anchor="middle" font-size="10">{sub}</text>')
    return "".join(out)


def arrow(x1, y1, x2, y2, label=None, dx=0, dy=-6):
    out = [
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-width="1.3" '
        'marker-end="url(#iftarrow)"/>'
    ]
    if label:
        out.append(
            f'<text x="{(x1 + x2) / 2 + dx}" y="{(y1 + y2) / 2 + dy}" text-anchor="middle" '
            f'font-size="10">{label}</text>'
        )
    return "".join(out)


# ------------------------------------------------ 24/25 Q1(b)(iii), the two organisations
AMAT = svg(
    660,
    250,
    # simultaneous: the CPU starts both at once
    '<text x="165" y="22" text-anchor="middle" font-weight="bold">Simultaneous access</text>'
    + box(20, 50, 90, 46, "CPU")
    + box(210, 40, 110, 40, "Cache", "5 ns")
    + box(210, 120, 110, 40, "Main memory", "100 ns")
    + arrow(110, 66, 210, 58)
    + arrow(110, 78, 210, 134)
    + '<text x="165" y="182" text-anchor="middle" font-size="10" font-style="italic">both started'
    '</text><text x="165" y="196" text-anchor="middle" font-size="10" font-style="italic">'
    'in the same cycle</text>'
    + '<text x="165" y="222" text-anchor="middle" font-size="11">AMAT = h&#215;T'
    '<tspan font-size="8" dy="3">c</tspan><tspan dy="-3"> + (1&#8722;h)&#215;T</tspan>'
    '<tspan font-size="8" dy="3">m</tspan><tspan dy="-3"> = 24 ns</tspan></text>'
    # hierarchical: the cache first, then memory only on a miss
    + '<text x="495" y="22" text-anchor="middle" font-weight="bold">Hierarchical access</text>'
    + box(350, 50, 90, 46, "CPU")
    + box(470, 50, 100, 46, "Cache", "5 ns")
    + box(470, 130, 100, 46, "Main memory", "100 ns")
    + arrow(440, 73, 470, 73)
    + arrow(520, 96, 520, 130, "miss", 18, 4)
    + '<text x="495" y="196" text-anchor="middle" font-size="10" font-style="italic">'
    'memory is reached only after the cache misses</text>'
    + '<text x="495" y="222" text-anchor="middle" font-size="11">AMAT = T'
    '<tspan font-size="8" dy="3">c</tspan><tspan dy="-3"> + (1&#8722;h)&#215;T</tspan>'
    '<tspan font-size="8" dy="3">m</tspan><tspan dy="-3"> = 25 ns</tspan></text>',
    "The two organisations. Simultaneous access starts the cache and main memory together, so a "
    "miss costs the memory time alone: 0.8&#215;5 + 0.2&#215;100 = 24 ns. Hierarchical access "
    "reaches memory only after the cache has missed, so a miss costs both: 5 + 0.2&#215;100 = 25 ns.",
    "Two block diagrams: simultaneous access with the CPU reaching cache and main memory at once, "
    "and hierarchical access with the CPU reaching the cache first and main memory only on a miss",
)


def load():
    return json.loads(LESSONS.read_text(encoding="utf-8"))


def find(lessons, tag):
    """The As printed block with this tag, and the worked block under it."""
    for lesson in lessons:
        for i, b in enumerate(lesson["blocks"]):
            if b.get("kind") == "asprinted" and (b.get("tag") or "") == tag:
                worked = next(
                    (n for n in lesson["blocks"][i + 1 : i + 4] if n.get("kind") == "worked"), None
                )
                if worked:
                    return lesson, worked
    raise SystemExit(f"no question tagged {tag}")


def main():
    lessons = load()
    changed = []

    # 25/26 Q3(b): the two schedules, as charts rather than lines of text
    _, w = find(lessons, "25/26 Q3(b)")
    if 'class="trace"' not in w["working"]:
        fwd = trace_table(
            15,
            [
                ("I1 MUL", 1, ["IF", "ID", "OF", "EX", "EX", "EX", "WB"]),
                ("I2 DIV", 2, ["IF", "ID", "OF", "--", "--", "EX", "EX", "EX", "EX", "EX", "EX", "WB"]),
                ("I3 ADD", 3, ["IF", "ID", "--", "--", "OF", "--", "--", "--", "--", "--", "EX", "WB"]),
                ("I4 SUB", 4, ["IF", "--", "--", "ID", "--", "--", "--", "--", "--", "OF", "EX", "WB"]),
            ],
        )
        nofwd = trace_table(
            17,
            [
                ("I1 MUL", 1, ["IF", "ID", "OF", "EX", "EX", "EX", "WB"]),
                ("I2 DIV", 2, ["IF", "ID", "OF", "--", "--", "EX", "EX", "EX", "EX", "EX", "EX", "WB"]),
                ("I3 ADD", 3, ["IF", "ID", "--", "--", "OF", "--", "--", "--", "--", "--", "--", "EX", "WB"]),
                ("I4 SUB", 4, ["IF", "--", "--", "ID", "--", "--", "--", "--", "--", "--", "--", "OF", "EX", "WB"]),
            ],
        )
        html = w["working"]
        # drop the two plain text grids and put a chart where each one stood
        html = re.sub(
            r"<p>\s*Instr\s+1\s+2[\s\S]*?</p>", "", html
        )
        for marker, chart in (("(i) With operand forwarding", fwd), ("(ii) Without operand forwarding", nofwd)):
            at = html.find(marker)
            if at == -1:
                raise SystemExit(f"{marker} not found in the 25/26 Q3(b) answer")
            end = html.find("</p>", at)
            end = end + 4 if end != -1 else at + len(marker)
            html = html[:end] + chart + html[end:]
        w["working"] = html
        changed.append("25/26 Q3(b): two timing charts")

    # 24/25 Q1(b): the diagrams the question asks for, worth 3 of its 7 marks
    _, w = find(lessons, "24/25 Q1(b)")
    if "<svg" not in w["working"]:
        w["working"] += AMAT
        changed.append("24/25 Q1(b): the two memory organisations, drawn")

    # 24/25 Q4(a): the same two architecture diagrams 25/26 Q1(a) already carries
    _, source = find(lessons, "25/26 Q1(a)")
    figures = re.findall(r"<figure>.*?</figure>", source["working"], re.S)
    _, w = find(lessons, "24/25 Q4(a)")
    if "<svg" not in w["working"] and figures:
        w["working"] += "".join(figures[:2])
        changed.append(f"24/25 Q4(a): {len(figures[:2])} architecture diagrams carried across")

    LESSONS.write_text(json.dumps(lessons, indent=1, ensure_ascii=False) + chr(10), encoding="utf-8")
    for c in changed:
        print("  " + c)
    if not changed:
        print("  nothing to do: every drawing question already has its diagram")


if __name__ == "__main__":
    main()
