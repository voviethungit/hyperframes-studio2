"""Create review sheets for every transition, without changing video assets."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
scenes=json.loads((ROOT/'timeline.json').read_text())['scenes']
OUT=ROOT/'boundary-review';OUT.mkdir(exist_ok=True)
def grab(args):
    i,offset,label=args
    p=OUT/f'{i+1:04d}-{label}.jpg'
    subprocess.run(['ffmpeg','-hide_banner','-nostdin','-v','error','-y','-threads','1','-ss',str(offset),'-i',str(ROOT/'rendered-scenes'/f'{i+1:04d}.mp4'),'-frames:v','1','-vf','scale=320:180,format=yuvj420p','-threads','1',str(p)],check=True)
    return p
jobs=[]
for i,s in enumerate(scenes):
    jobs.extend([(i,min(.8,max(0,s['duration']-.08)),'in'),(i,max(0,s['duration']-.08),'out')])
with ThreadPoolExecutor(max_workers=2) as pool:
    paths=list(pool.map(grab,jobs))
for page,start in enumerate(range(0,len(paths),64),1):
    sheet=Image.new('RGB',(2560,1600),'#202020');draw=ImageDraw.Draw(sheet)
    for j,p in enumerate(paths[start:start+64]):
        im=Image.open(p).convert('RGB');x=(j%8)*320;y=(j//8)*200
        sheet.paste(im,(x,y));draw.text((x+5,y+182),p.stem,fill='white')
    sheet.save(OUT/f'review-{page:02d}.jpg')
print(f'{len(paths)} boundary frames in {page} sheets')
