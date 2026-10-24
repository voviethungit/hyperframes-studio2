"""Render authored still-image camera shots and dissolve without changing narration."""
import concurrent.futures, json, math, subprocess, time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
T=json.loads((ROOT/'timeline.json').read_text())
FPS=T['fps']; SCENES=T['scenes']; OUT=ROOT/'rendered-scenes'; OUT.mkdir(exist_ok=True)
def camera(mode,n,freeze=False):
    u='1' if freeze else f'on/{max(1,n-1)}'
    if mode==0: z=f'1+0.05*({u})'; x='iw/2-iw/zoom/2'
    elif mode==1: z=f'1.05-0.05*({u})'; x='iw/2-iw/zoom/2'
    elif mode==2: z='1.05'; x=f'(iw-iw/zoom)*({u})'
    else: z='1.05'; x=f'(iw-iw/zoom)*(1-({u}))'
    return f"scale=2048:1152:force_original_aspect_ratio=increase,crop=2048:1152,zoompan=z='{z}':x='{x}':y='ih/2-ih/zoom/2':d={n}:s=1920x1080:fps={FPS},format=yuv420p,settb=1/{FPS}"
def render(i):
    s=SCENES[i]; n=s['end_frame']-s['start_frame']; target=OUT/f'{i+1:04d}.mp4'
    if target.exists():
        try:
            count=int(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','csv=p=0',str(target)]).strip())
            if count==n:return i,'retained'
        except Exception:pass
    cmd=['ffmpeg','-hide_banner','-nostdin','-y','-v','error']
    cur=ROOT/'assets'/(s['asset']+'.png')
    if i and SCENES[i-1]['asset']!=s['asset']:
        prev=SCENES[i-1]
        cmd+=['-i',str(ROOT/'assets'/(prev['asset']+'.png')),'-i',str(cur)]
        # Freeze the previous illustration at its actual final camera pose.
        prev_filter=camera((i-1)%4,n,True)
        fg=f'[0:v]{prev_filter}[a];[1:v]{camera(i%4,n)}[b];[a][b]xfade=transition=fade:duration=0.6:offset=0,format=yuv420p[v]'
        cmd+=['-filter_complex',fg,'-map','[v]','-filter_complex_threads','1']
    else:cmd+=['-i',str(cur),'-vf',camera(i%4,n),'-filter_threads','1']
    cmd+=['-frames:v',str(n),'-an','-c:v','libx264','-preset','veryfast','-crf','22','-threads','2','-pix_fmt','yuv420p','-r',str(FPS),str(target)]
    run=subprocess.run(cmd,capture_output=True,text=True)
    if run.returncode:raise RuntimeError(f'Scene {i+1}: {run.stderr}')
    return i,'rendered'
start=time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    for count,(i,status) in enumerate(pool.map(render,range(len(SCENES))),1):
        print(f'{count}/{len(SCENES)} Scene {i+1} {status}; elapsed {time.time()-start:.1f}s',flush=True)
concat=ROOT/'rendered-concat.txt'
concat.write_text(''.join(f"file '{OUT/(str(i+1).zfill(4)+'.mp4')}'\n" for i in range(len(SCENES))))
final=ROOT/'OLD_CHANNEL_FINAL_VIDEO.mp4'
subprocess.run(['ffmpeg','-hide_banner','-nostdin','-y','-v','warning','-f','concat','-safe','0','-i',str(concat),'-i',str(ROOT/'MASTER_VOICE.mp3'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(T['audio_duration']),'-movflags','+faststart',str(final)],check=True)
print('FINAL_EXPORT_COMPLETE',str(final),flush=True)
