"""Exact Remotion frame caching: motion then a provably static hold, CFR30."""
import json,shutil,subprocess,time,sys
from pathlib import Path
R=Path(__file__).resolve().parent;P=(R.parents[1]/'remotion-studio');T=json.loads((R/'timeline.json').read_text());out=R/'rendered-shots';out.mkdir(exist_ok=True)
repair=json.loads((R/'rerender-required.json').read_text()) if '--repair' in sys.argv or '--repair-only' in sys.argv else []
for i,s in enumerate(T['scenes']):
 if '--repair-only' in sys.argv and i not in repair:continue
 needed=[s]+([T['scenes'][i-1]] if i and s['transition']=='dissolve' else [])
 while any(not (R/'assets/scenes'/f"{x['id']:03d}.png").is_file() for x in needed):
  print('Waiting for scene',i+1,flush=True);time.sleep(30)
 for x in needed:shutil.copyfile(R/'assets/scenes'/f"{x['id']:03d}.png",P/'public'/x['image'])
 target=out/f'{i:03d}.mp4'
 if target.exists() and i not in repair:continue
 cache=R/'render-cache'/f'{i:03d}';cache.mkdir(parents=True,exist_ok=True)
 count=min(90,s['duration'])
 with (R/f'render-shot-{i:03d}.log').open('w') as log:
  subprocess.run([str(P/'node_modules/.bin/remotion'),'render','src/index.ts','OldChannel16',str(cache),'--sequence','--image-format=png',f"--frames={s['start']}-{s['start']+count-1}",'--muted','--browser-executable=/usr/bin/chromium','--concurrency=4','--overwrite'],cwd=P,stdout=log,stderr=log,check=True)
 files=sorted(cache.glob('*.png'));assert len(files)==count,(i,len(files),count)
 subprocess.run(['ffmpeg','-hide_banner','-nostdin','-y','-v','error','-framerate','30','-pattern_type','glob','-i',str(cache/'*.png'),'-vf',f"tpad=stop_mode=clone:stop={s['duration']-count},format=yuv420p",'-frames:v',str(s['duration']),'-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-an',str(target)],check=True)
 # Remotion's camera and opacity are constant from local frame89 onward.
 # Cached holds repeat exactly that rendered state, never skipping any speech.
 review=R/'frame-review';review.mkdir(exist_ok=True)
 shutil.copyfile(files[0],review/f'{i:03d}-in.png');shutil.copyfile(files[-1],review/f'{i:03d}-held.png')
 for f in files:f.unlink()
 print(f'Rendered scene {i+1}/{len(T["scenes"])}; {s["duration"]} CFR frames; {count} distinct frame captures',flush=True)
if '--repair-only' in sys.argv:
 print('REPAIRED_SELECTED_SHOTS',flush=True);sys.exit(0)
(R/'shots.txt').write_text(''.join("file '"+str(out/f'{i:03d}.mp4')+"'\n" for i in range(len(T['scenes']))))
subprocess.run(['ffmpeg','-hide_banner','-nostdin','-y','-v','warning','-f','concat','-safe','0','-i',str(R/'shots.txt'),'-i',str(R/'MASTER_VOICE.mp3'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(T['audio_duration']),'-movflags','+faststart',str(R/'OLD_CHANNEL_16_EXPORT_PENDING_QA.mp4')],check=True)
print('FULL_EXPORT_PENDING_QA',flush=True)
