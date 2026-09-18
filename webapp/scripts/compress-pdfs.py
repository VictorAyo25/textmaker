"""Squeeze the generated books, build the all-in-one, and record what they are.

    python scripts/compress-pdfs.py

Chromium leaves its content streams lightly compressed and repeats identical
objects across pages. Re-deflating and merging those removes about a sixth of
the bytes, which matters because these files ship in the repository and are
downloaded on a phone.

Then it writes data/question-books.json: the page count and size of every book,
which the landing page and each book page display. That is deliberate: the
numbers a reader sees are read back off the actual files rather than typed in,
so they cannot drift from what downloads.
"""
import json
import pathlib

from pypdf import PdfReader, PdfWriter

WEBAPP = pathlib.Path(__file__).resolve().parent.parent
OUT = WEBAPP / "public" / "pdf"
COURSES = ["IFT222", "CSC241", "COS221"]


def squeeze(path):
    before = path.stat().st_size
    w = PdfWriter(clone_from=str(path))
    for page in w.pages:
        page.compress_content_streams(level=9)
    w.compress_identical_objects()
    with open(path, "wb") as fh:
        w.write(fh)
    return before, path.stat().st_size


def main():
    meta = {}
    total_before = total_after = 0
    for code in COURSES:
        for suffix, key in [("question-book", code), ("theory-solutions", f"{code}-theory")]:
            f = OUT / f"{code}-{suffix}.pdf"
            if not f.exists():
                raise SystemExit(f"{f.name} is missing: run the printer first")
            before, after = squeeze(f)
            total_before += before
            total_after += after
            meta[key] = {
                "file": f"/pdf/{f.name}",
                "pages": len(PdfReader(str(f)).pages),
                "mb": round(after / 1024 / 1024, 1),
            }
            print(f"  {f.name:34} {before/1024/1024:5.1f} -> {after/1024/1024:5.1f} MB")

    # the all-in-one, rebuilt from the freshly printed question books
    combined = OUT / "all-three-question-books.pdf"
    w = PdfWriter()
    for code in COURSES:
        f = OUT / f"{code}-question-book.pdf"
        w.add_outline_item(f"{code} question book", len(w.pages))
        w.append(str(f))
    for page in w.pages:
        page.compress_content_streams(level=9)
    w.compress_identical_objects()
    with open(combined, "wb") as fh:
        w.write(fh)
    meta["ALL"] = {
        "file": f"/pdf/{combined.name}",
        "pages": len(PdfReader(str(combined)).pages),
        "mb": round(combined.stat().st_size / 1024 / 1024, 1),
    }
    print(f"  {combined.name:34} {meta['ALL']['pages']} pages, {meta['ALL']['mb']} MB")

    (WEBAPP / "data" / "question-books.json").write_text(
        json.dumps(meta, indent=2) + chr(10), encoding="utf-8"
    )
    print(f"  total {total_before/1024/1024:.1f} -> {total_after/1024/1024:.1f} MB, "
          f"page counts written to data/question-books.json")


if __name__ == "__main__":
    main()
