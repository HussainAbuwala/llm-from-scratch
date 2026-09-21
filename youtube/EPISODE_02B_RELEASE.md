# Episode 02B release checks

Prepared September 20, 2026.

## Video

Output: `~/Movies/llm-series/episode-02b-trigram-language-model-python.mp4`

- Inputs: `episode-02B-part1.mp4` (767.066667 s), then `episode-02B-part2.mp4` (1062.966667 s).
- No content cuts, overlays, or transitions. Original recordings were not modified.
- Final duration: 1830.033333 seconds, approximately 30:30.
- Size: 210,891,524 bytes.
- SHA-256: `f146990112e98dbf0a2a907fd38ba3836637f65c30ddc635a3f1e23aed85f0bc`.
- 1920 x 1080 H.264, regular 30 fps, CRF 18; AAC stereo 48 kHz / 192 kbps; fast-start MP4.
- A stream-copy draft exposed irregular decoded frame timing at the join. The delivered export normalizes video timing with ffmpeg's fps filter. Audio is resampled to a continuous timeline. No intentional loudness adjustment was applied.
- Full decoded playback to ffmpeg's null output completed with zero errors/warnings. Packet DTS strictly increases in each stream: 54,900 video and 85,782 audio packets.
- Video starts at 0.033333 s; audio starts at zero. Endpoints differ by approximately 40 ms.
- Source MP4 parsing emitted UDTA metadata fallback messages; the final output decoded cleanly. These messages were not content-decode failures.
- Sampled frames throughout both parts, directly checked the 05:00 chapter point, and inspected the final join and ending. This is technical and sampled visual QA, not a word-for-word spoken-content review.

Reproduce: `python3 youtube/merge_episode_02b.py ~/Movies/llm-series /tmp/ep02b-new-export`.

## Notebook and companions

The release follows the user's recorded edits: 11 numbered sections, 33 cells,
18 code cells, 12 toy samples, shorter sweep printing, and the final recap.
An ignored `.RECORDING.ipynb` copy preserves the pre-release local notebook.
`lesson.py` is the editable percent-cell source. The build executes reporting
via `release_report.py`, keeping that utility code off the presentation screen.

Fresh-kernel execution succeeded with Python 3.14.2; all 16 tests passed.
Core code matches the tested lab. All 45 positive-k candidate results reproduce
the earlier validation report; five k=0 candidates are included in the recorded
grid and all have infinite validation loss. Test settings are frozen using
validation, and the old test split's prior use is disclosed.

Guides and README now use the recorded section numbers and explain the build.
The unrelated Episode 01 notebook kernel-label edit is excluded from the commit.

## Release assets

- One selected 1280 x 720 JPG thumbnail, below 2 MB; navy series palette.
- The user selected A: LET'S CODE A TRIGRAM LANGUAGE MODEL. Supporting tagline removed; unused options and the comparison sheet removed.
- Metadata includes paste-ready title, description, repository links, seven recording-based chapter navigation points, tags, and an unposted pinned comment.
- No video upload, publication, or scheduling was performed.
