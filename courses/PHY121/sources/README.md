# PHY121 sources

Raw inputs for this course only. Every course keeps its own copy under
`courses/<COURSE>/sources/`, so nothing here is shared with another course.

```
sources/
├── slides/       the lecturer's decks, numbered in teaching order
├── tests/        CBT test screenshots (test1/, test2/)
├── manual_v1/    the original manual the blend is rebuilt from
└── extracted/    text/images pulled out of the manual, regenerable
```

**`manual_v1/PHY121_Study_Manual.pdf` is load-bearing.** The build reads it to
regenerate any section not yet frozen into `build/content/`, and the QA scripts
diff against it to prove nothing was lost. Do not move or delete it. If you do
move it, update `PDF` in `build/reconstruct.py` and `build/struct_extract.py`.

`extracted/` holds working files (`manual_text.txt`, `manual_boxes_A.png`) used
by the one-off survey scripts. They are derived from the manual and can be
regenerated; nothing in the build depends on them.

`manual_v1/_original_delivery_phy_121.zip` is the untouched delivery archive.
It is deliberately not committed (its contents are already here); it is kept
locally as a last-resort original.

## Adding a new slide deck

Drop the PDF in `slides/` using the next number in teaching order, then follow
the update steps in `../README.md`.
