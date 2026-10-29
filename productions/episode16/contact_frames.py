from PIL import Image,ImageDraw
from pathlib import Path
import sys
R=Path(__file__).resolve().parent;start=int(sys.argv[1]);count=int(sys.argv[2]) if len(sys.argv)>2 else 24
c=Image.new('RGB',(2000,300*((count+3)//4)),'#202020');d=ImageDraw.Draw(c)
for j,i in enumerate(range(start,start+count)):
 p=R/'frame-review'/f'{i:03d}-held.png'
 if p.exists():
  im=Image.open(p).convert('RGB');im.thumbnail((495,275));x=j%4*500;y=j//4*300;c.paste(im,(x,y));d.text((x+8,y+280),str(i),fill='white')
c.save(R/f'frames-{start:03d}.jpg')
