/**
 * The content slides of the eight IFT222 lecture decks.
 *
 * A slide is excluded only when there is nothing on it that can be tested
 * faithfully. Four kinds qualify:
 *
 *   - deck title slides and section dividers ("UNIT 1:", "Addressing Modes",
 *     "MID-LECTURE QUIZ", "End of Unit");
 *   - slides whose whole body is a picture, so the extractor sees a title and
 *     "[images: 1]" and nothing else. A question about a diagram nobody can
 *     read would be a question about nothing;
 *   - course objective and learning outcome slides, which say what a student
 *     should be able to do rather than stating a fact about the machine;
 *   - the closing exhortations of the revision deck ("ENSURE YOU PREPARE FOR
 *     THE EXAMINATION").
 *
 * Everything else is in, and the build gate fails if any slide listed here is
 * never cited by a question. Kept beside the extracted decks in
 * courses/IFT222 .../sources/extracted/, one file per deck, 413 slides in all.
 */

const DECKS = {
  Intro: { total: 57, skip: [1, 2, 3, 5, 6, 8, 10, 14, 16, 27, 45, 57] },
  Data: { total: 73, skip: [1, 4, 14, 27, 32, 38, 42, 58, 60, 62, 64, 70, 73] },
  ISA: {
    total: 60,
    skip: [1, 2, 4, 12, 13, 21, 28, 29, 30, 31, 32, 42, 43, 44, 45, 46, 48, 50, 56, 57, 59, 60],
  },
  Mem: { total: 65, skip: [1, 3, 11, 16, 27, 29, 33, 36, 41, 42, 51, 65] },
  Cache: { total: 14, skip: [1, 14] },
  RISC: { total: 36, skip: [1, 2, 28, 31, 33, 36] },
  Pipe: { total: 57, skip: [1, 2, 7, 8, 9, 26, 27, 35, 36, 37, 44, 45, 46, 57] },
  Rev: { total: 51, skip: [1, 16, 34, 37, 50, 51] },
};

export const IFT_DECK_SLIDES = Object.entries(DECKS).flatMap(([deck, { total, skip }]) =>
  Array.from({ length: total }, (_, i) => i + 1)
    .filter((n) => !skip.includes(n))
    .map((n) => `${deck} S${n}`)
);

export const IFT_DECK_KEYS = Object.keys(DECKS);
