import subprocess,json
from pathlib import Path
from PIL import Image,ImageChops
R=Path(__file__).resolve().parent;P=(R.parents[1]/'remotion-studio');T=json.loads((R/'timeline.json').read_text());rows=[]
for i in [1,2,3,4]:
 s=T['scenes'][i];f=s['end']-2;out=R/'frame-review'/f'{i:03d}-native-end.png'
 subprocess.run([str(P/'node_modules/.bin/remotion'),'still','src/index.ts','OldChannel16',str(out),f'--frame={f}','--browser-executable=/usr/bin/chromium','--overwrite'],cwd=P,stdout=subprocess.DEVNULL,check=True)
 diff=ImageChops.difference(Image.open(out).convert('RGB'),Image.open(R/'frame-review'/f'{i:03d}-held.png').convert('RGB')).getbbox()
 assert diff is None,(i,diff)
 rows.append({'scene':i,'frame':f,'motion':s['motion'],'identical_pixels':True})
(R/'static-cache-verification.json').write_text(json.dumps(rows,indent=2));print(rows)
