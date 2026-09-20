#!/usr/bin/env python3
"""Join the two Episode 02B recordings with normalized frame timing, no cuts.

Usage: python3 youtube/merge_episode_02b.py ~/Movies/llm-series /tmp/ep02b-new
Requires ffmpeg. The output directory must not exist. Original recordings are read-only.
"""
import argparse
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    parts = [(args.source.expanduser()/f'episode-02B-part{i}.mp4').resolve() for i in (1, 2)]
    for part in parts:
        if not part.is_file():
            raise FileNotFoundError(part)
    out = args.output.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=False)
    listing = out/'concat.txt'
    listing.write_text(''.join("file '"+str(p).replace("'", "'\\''")+"'\n" for p in parts))
    final = out/'episode-02b-trigram-language-model-python.mp4'
    command = ['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'warning',
               '-f', 'concat', '-safe', '0', '-i', str(listing),
               '-map', '0:v:0', '-map', '0:a:0', '-vf', 'fps=30',
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
               '-af', 'aresample=async=1:first_pts=0', '-c:a', 'aac', '-b:a', '192k',
               '-ar', '48000', '-movflags', '+faststart', str(final)]
    with (out/'encode.log').open('w') as log:
        subprocess.run(command, stderr=log, check=True)
    print(final)


if __name__ == '__main__':
    main()
