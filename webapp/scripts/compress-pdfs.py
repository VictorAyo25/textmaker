"""Squeeze the generated PDFs before they are committed.

    python scripts/compress-pdfs.py

Chromium leaves its content streams lightly compressed and writes the same
objects repeatedly across pages. Re-deflating every stream and merging
identical objects takes a second a book and removes about a third of the bytes,
which matters because these files ship in the repository and are downloaded on
a phone.
"""
import pathlib
from pypdf import PdfWriter

OUT = pathlib.Path(__file__).resolve().parent.parent / "public" / "pdf"

total_before = total_after = 0
for f in sorted(OUT.glob("*.pdf")):
    before = f.stat().st_size
    w = PdfWriter(clone_from=str(f))
    for page in w.pages:
        page.compress_content_streams(level=9)
    w.compress_identical_objects()
    with open(f, "wb") as fh:
        w.write(fh)
    after = f.stat().st_size
    total_before += before
    total_after += after
    print(f"  {f.name:34} {before/1024/1024:5.1f} -> {after/1024/1024:5.1f} MB")
print(f"  total {total_before/1024/1024:.1f} -> {total_after/1024/1024:.1f} MB")
