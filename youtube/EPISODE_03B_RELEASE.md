# Episode 03B release checks

Prepared October 1, 2026. Recorded and packaged; not uploaded or published here.

## Recording and export

Source directory: `/Users/hussainabuwala/Movies/llm-series`.

| Source | Duration | Start in merged timeline |
|---|---:|---:|
| episode-03B-part1.mp4 | 763.333333 s | 00:00.000 |
| episode-03B-part2.mp4 | 732.166667 s | 12:43.333 |

Both sources are 1920 × 1080 H.264 with AAC audio at 48 kHz. Joined in numeric
order, with no editorial cuts or added transitions; source files retained.
The export follows 03A's normalized 30 fps H.264 CRF 18 / veryfast workflow,
AAC 192 kb/s at 48 kHz with asynchronous resampling, and MP4 faststart.
Reproduce using `merge_episode_03b.py SOURCE_DIRECTORY NEW_OUTPUT_DIRECTORY`.

Delivered file:
`/Users/hussainabuwala/Movies/llm-series/episode-03b-weights-softmax-numpy.mp4`.

- Duration: **1495.500000 seconds (24:55.50)**.
- Size: **160,070,925 bytes**.
- SHA-256: `7eb3ffda0e103985caa4a67e9206a87a2e3d515b3db32964e66b1f1657a6a0b0`.
- Full final audio/video decode completed with no warnings or errors.
- The merge logged source MP4 UDTA metadata parsing retries; encoding completed,
  and the final export's decode log is empty.
- Stills on each side of the join and near the close were visually inspected.
- Delivered copy's hash matches the verified export.

Chapter topics use one-minute source stills and are approximate navigation
anchors, not transcript-derived first mentions. No full audio/caption review
was performed. The recorded route closes after the chosen weight comparison;
the metadata does not promise a generation walkthrough or real-data comparison.

## Preserve the presenter's notebook

`episodes/03_weights/episode_03.ipynb` was left byte-for-byte unchanged throughout
release preparation. SHA-256 before and after:
`26b67c260e2fc5f7d1afcec6dac8f184ff02e1ede550f53e1bc77fd4fe5198d7`.

Its 26 cells (12 code cells) retain the presenter's deletion of the optional
real-data extension and shortened closing notes. Generation code remains in
the saved notebook as additional exploration, although the recording skips it.
`lesson.py` was synchronized FROM that notebook; the HTML reading copy was
exported from its saved outputs. A temporary source copy was executed in a fresh
kernel, avoiding any rewrite of the original notebook.

All 16 current theory/coding checks passed. The integration test specific to
the removed large-data section was removed with that section. Existing tests
still cover the 03A arithmetic, underflow stability, weight changes, boundary
handling, generation, and notebook/source agreement.

## Release assets

- `EPISODE_03B_METADATA.md`: title options, paste-ready description, approximate
  chapters, tags, upload notes, and pinned-comment draft.
- Three 1280 × 720 JPG thumbnail alternatives, each under 2 MB, visually checked
  on `thumbnails/episode-03b-options.jpg`.
- Recommended thumbnail A: `episode-03b-build-it-in-numpy.jpg`.
- Alternatives B and C focus on underflow and overshoot respectively.
- Reproducible code-drawn assets follow the established cream/plum Learn theme.
- `git diff --check` passed before commit.
- No Git push, YouTube upload, or comment posting performed.
- The unrelated pre-existing Episode 01 notebook modification is excluded from
  the release commit.
