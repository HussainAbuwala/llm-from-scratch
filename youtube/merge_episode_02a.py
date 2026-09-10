#!/usr/bin/env python3
"""Reproduce the Episode 02A edit with ffmpeg and ffprobe. Originals are read-only.

Example: python3 youtube/merge_episode_02a.py ~/Movies/llm-series /tmp/ep02a-new-export
The output directory must not exist, to prevent accidental overwrites.
"""
from pathlib import Path
import subprocess,json
import argparse
parser=argparse.ArgumentParser(description='Join Episode 02A; cut 09:14-09:18 from part 4.')
parser.add_argument('source',type=Path,help='Directory containing the five original MP4s')
parser.add_argument('output',type=Path,help='New directory for intermediates and the final MP4')
args=parser.parse_args()
root=args.source.expanduser(); out=args.output.expanduser()
out.mkdir(parents=True,exist_ok=False)
parts=[]
for i in range(1,6):
 p=root/f'episode-02A-part{i}.mp4'
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(p)]))
 duration=float(d['format']['duration']); length=duration-(4 if i==4 else 0)
 target=out/f'normalized-{i}.mp4'
 if i==4:
  filters='[0:v]fps=30,split=2[v0][v1];[v0]trim=end=554,setpts=PTS-STARTPTS[va];[v1]trim=start=558,setpts=PTS-STARTPTS[vb];[0:a]asplit=2[a0][a1];[a0]atrim=end=554,asetpts=PTS-STARTPTS[aa];[a1]atrim=start=558,asetpts=PTS-STARTPTS[ab];[va][aa][vb][ab]concat=n=2:v=1:a=1[v][a0out];[a0out]apad,atrim=duration='+str(length)+'[a]'
 else:
  filters=f'[0:v]fps=30,setpts=PTS-STARTPTS[v];[0:a]asetpts=PTS-STARTPTS,apad,atrim=duration={length}[a]'
 cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','warning','-i',str(p),'-filter_complex',filters,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-video_track_timescale','15360','-movflags','+faststart',str(target)]
 print(f'Encoding part {i}, {length:.3f}s',flush=True)
 with (out/f'encode-{i}.log').open('w') as log: subprocess.run(cmd,stdout=log,stderr=log,check=True)
 parts.append(target)
(out/'concat.txt').write_text(''.join(f"file '{p}'\n" for p in parts))
final=out/'episode-02a-trigrams-and-sparsity.mp4'
subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','warning','-f','concat','-safe','0','-i',str(out/'concat.txt'),'-map','0:v:0','-map','0:a:0','-c:v','copy','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(final)],check=True)
print('Merged: '+str(final),flush=True)
