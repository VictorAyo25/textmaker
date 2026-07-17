FINAL_MANUALS — signed-off study manuals only. One per course.
Work in progress belongs in that course's drafts/ folder, never here.

-------------------------------------------------------------------------------
PHY121 - General Physics II - Study Manual v3.pdf   150 pp   signed off 2026-07-16
-------------------------------------------------------------------------------
PHY121 General Physics II, complete manual, Modules 1 to 5.

Contents: Foundations F.1-F.11, Modules 1 to 5 (eighteen units), full solutions
S.1-S.7, mock papers M.1-M.5, reference R.1-R.4. Module 5 is Maxwell's Equations
and Electromagnetic Waves. 55 clickable Contents links, 14 inline diagrams.

What changed from v2 (163 pp):
  + The whole book is real, selectable, searchable text. The back matter used to
    be page images of v1; it is now rebuilt as text, including every table.
  + v2 had shipped defects, all fixed here:
      - fill-in-the-gap blanks were missing, so those exercises could not be
        answered. All 100 are present.
      - bold emphasis had been dropped across the teaching text.
      - italic, monospace, lists and boxed answers had been flattened.
  + Recovered content that earlier builds dropped: 54 solution boxes, 14 circuit
    diagrams, 10 sub-headings, and a worked answer line.
  + Fixed: welded bar labels ("Test 2, q1 worked example..."), hyphens closing up
    into "crosssectional"/"Tjoint", step notes stranded above their steps, and
    kickers printing "REFERENCER.3" for "REFERENCE R.3".
  Teaching text is still the v1 wording, now with its formatting intact.

It is 13 pages shorter than v2 because reflowed text packs denser than the fixed
page images it replaced. Nothing was cut: audited word by word against v1, and
the only differences are hyphenated words correctly rejoined and subscripts
correctly marked up.

Verified: no blank pages; footer numbering sequential; all 55 Contents links
resolve; every number recomputed independently; no em/en dashes; no institution
or methodology-author names. Structural gates (bold, sub/superscript, blanks,
lists, tables, figures) all above floor.

v2 was withdrawn as defective. It remains in git history (commit 2312940) if a
copy is ever needed.

To rebuild or update:  see "courses/PHY121 - General Physics II/README.md"
                       (cd build && python assemble.py)
