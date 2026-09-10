# Episode 02A release verification

Prepared September 10, 2026. Video publishing and repository push are separate from this local release commit.

## Video

Output: `~/Movies/llm-series/episode-02a-trigrams-and-sparsity.mp4`

- Inputs: `episode-02A-part1.mp4` through `episode-02A-part5.mp4`, numeric order.
- Requested cut: part 4, interval [554.000, 558.000) seconds (09:14-09:18).
- Part 4's remaining tail, approximately 0.133 seconds, is retained.
- Source files were read without modification; no other content cuts, transitions, or overlays were added.
- Export: 1920 x 1080 H.264, 30 fps timeline, CRF 18; AAC stereo, 48 kHz, 192 kbps; fast-start MP4.
- Container duration: 2623.588 seconds (43:43.588).
- Size: 231,388,459 bytes.
- SHA-256: `34ab830fc03b0c7049238ac8245562afe4654e4380b2c54f57c84cbc0331ff9b`.
- Full ffmpeg decode completed with no errors; final mux log had no warnings.
- All packet decoding timestamps strictly increase within each stream: 78,705 video packets and 122,982 audio packets.
- AAC boundary overlap in the first draft was resolved by decoding and resampling the joined audio, then encoding a continuous audio stream. Original loudness was not intentionally changed.
- Final audio and video endpoints differ by approximately 33 milliseconds. The output retains the source frame cadence, including final-frame timing irregularities in parts 3 and 5.
- Inspected source-part opening frames and frames around the part-4/part-5 edit boundary. This is technical and sampled visual QA, not a word-for-word review of all recorded speech.

Reproduce in a new output directory:

```bash
python3 youtube/merge_episode_02a.py ~/Movies/llm-series /tmp/ep02a-new-export
```

Source durations in seconds: 524.700, 451.933333, 456.866667, 558.133333, 635.933333. After removing four seconds, source-boundary starts are approximately 0, 524.700, 976.633333, 1433.500, and 1987.633333. The metadata rounds these down to chapter seconds.

## Companion materials

- `docs/episode-02-theory.pdf`: 11 pages, rendered equations and worked tables; editable source in the adjacent Markdown file.
- `docs/episode-02-canvas.pdf`: all 29 frames, one per page, with bookmarks and vector text/shapes.
- All guide and canvas PDF pages rendered with Poppler and visually reviewed. No clipped text, broken equations, overlapping tables, or spillover pages remain.
- Canvas content matches the recorded sequence. Reader footer and presenter guide now link to audience PDFs.
- Guide explicitly explains the user's equal/fewer matches example, add-one counts behind 1/5, whole-row backoff limitations, and interpolation as a weighted combination.
- Twelve lab and lesson checks passed. No new experiment was run, and the final test set remains reserved for Episode 02B.
- Local Markdown links and release-description repository targets checked for existing files. Public main-branch links require pushing this commit.

## Thumbnails and metadata

Three 1280 x 720 JPG alternatives, visually checked at full and feed size. All are under 2 MB. Images use native diagram layouts and the existing series font/palette; no private presenter photo is included.

The metadata includes title alternatives, a paste-ready description, five source-boundary chapters, references, tags, upload settings, and a draft pinned comment. No thumbnail was selected, video uploaded, or comment posted.
