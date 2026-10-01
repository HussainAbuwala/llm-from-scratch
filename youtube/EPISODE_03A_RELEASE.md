# Episode 03A release checks

**Publication status:** Published, confirmed by the presenter on September 30, 2026.
The checks below describe the earlier preparation and export session.

## Recording and edit

Source directory: `/Users/hussainabuwala/Movies/llm-series`.

| Source | Duration | Start in merged timeline |
|---|---:|---:|
| episode-03A-part1.mp4 | 529.800000 s | 00:00.000 |
| episode-03A-part2.mp4 | 515.766667 s | 08:49.800 |
| episode-03A-part3.mp4 | 338.033333 s | 17:25.567 |
| episode-03A-part4.mp4 | 265.966667 s | 23:03.600 |

All four recordings are 1920 × 1080 H.264 with AAC audio at 48 kHz. Joined in
numeric order, with no editorial cuts or added transitions. Originals retained.
The initial stream-copy draft exposed non-monotonic frame timestamps during a
full decode check. The final export therefore normalizes video to 30 fps using
H.264 CRF 18, veryfast preset, and AAC 192 kb/s with asynchronous resampling.
The MP4 uses faststart for web playback. Reproduce with `merge_episode_03a.py`.

Final delivery: `/Users/hussainabuwala/Movies/llm-series/episode-03a-from-counts-to-weights.mp4`.

Chapter labels were checked against stills at 5 and 100 seconds in each source
clip. These are broad part-boundary navigation points, not transcript-derived
first mentions. No word-by-word audio or caption review was performed.

## Canvas and companion

- `canvas/episode_03_final.excalidraw`: exact byte-for-byte copy of the user-supplied edited canvas; 19 live frames, valid unique IDs and frame references.
- SHA-256: `d5cfe824492f39f4cacd5014d9e5cd4fb1e99a52d15e5ace362977979e743d21`.
- This is the authoritative recording canvas. The generated 20-frame HTML, canvas and presenter guide remain preparation references; rebuilding those does not overwrite the final file.
- All 10 Episode 03 numerical/concept tests passed.
- `git diff --check` passed.
- No full Episode 03B coding notebook is claimed or included.

## Upload assets

- Paste-ready title, alternatives, description, chapters, tags, settings and pinned-comment draft in `EPISODE_03A_METADATA.md`.
- Three thumbnails, each 1280 × 720 JPG, under 200 KB; visually reviewed on the comparison sheet.
- Cream/plum Learn palette follows `SERIES_VISUAL_THEMES.md`.
- No YouTube upload, publication or Git push performed.
- Unrelated pre-existing Episode 01 notebook kernel-display-name change excluded from the release commit.

## Final export verification

- Duration: 1649.566666 seconds (27:29.57); size: 128,697,210 bytes.
- Full final video/audio decode completed with no errors or timestamp warnings.
- Final video: 1920 × 1080, 30 fps H.264; audio: AAC, 48 kHz.
- Representative join and closing stills visually checked.
- Delivered file matches verified export SHA-256: `861769b7843eac997b48084771981e88b76285eee59fdee0a13bd5fadb4bd45e`.
