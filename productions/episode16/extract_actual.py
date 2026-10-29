import json,subprocess,concurrent.futures
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;T=json.loads((R/'timeline.json').read_text());O=R/'actual-frame-review';O.mkdir(exist_ok=True)
P=R/'OLD_CHANNEL_16_EXPORT_PENDING_QA.mp4';assert P.exists()
def extract(s):
 t=(s['start']+s['end'])/60
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(P),'-frames:v','1','-vf','scale=640:360',str(O/f"{s['id']:03d}.png")],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(extract,T['scenes']))
for start in range(0,len(T['scenes']),24):
 count=min(24,len(T['scenes'])-start);c=Image.new('RGB',(2000,300*((count+3)//4)),'#202020');d=ImageDraw.Draw(c)
 for j,i in enumerate(range(start,start+count)):
  im=Image.open(O/f'{i:03d}.png').convert('RGB');im.thumbnail((495,275));x=j%4*500;y=j//4*300;c.paste(im,(x,y));d.text((x+8,y+280),str(i),fill='white')
 c.save(R/f'actual-{start:03d}.jpg')
for name,t in [('beginning',0),('middle',T['audio_duration']/2),('last-second',T['audio_duration']-1),('last-frame',(T['total_frames']-1)/30)]:
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(P),'-frames:v','1',str(O/f'{name}.png')],check=True)
print('ACTUAL_MP4_ALL_SCENE_CONTACTS_READY')
