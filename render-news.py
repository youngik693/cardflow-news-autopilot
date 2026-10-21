"""Render a manually fact-checked news brief, with original text and graphics."""
import sys,json,pathlib
from PIL import ImageDraw
from render import base,block,font,pill

def render_news(model,out):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True);paths=[]
 for i,slide in enumerate(model['slides']):
  im,d,dark,accent,paper,fg=base('technology',i,light=i==1)
  pill(d,(64,145),'BUSINESS / 뉴스 브리핑',accent,dark,24)
  d.text((900,155),f'{i+1:02}/03',font=font(24),fill=fg)
  block(d,slide['heading'],64,245,950,290,76,fg,1.23,minsize=44)
  for j,item in enumerate(slide['items']):
   y=600+j*175
   d.rounded_rectangle((64,y,1016,y+149),radius=22,fill=dark if i==1 else paper)
   block(d,item,94,y+26,890,110,37,paper if i==1 else dark,minsize=29)
  block(d,model['sourceLabel'],64,1160,950,60,23,fg,minsize=20)
  block(d,'2026.10.21 보도 기준 · 합병 확정 아님',64,1230,950,46,22,fg,minsize=20)
  path=out/f'{i+1:02}.jpg';im.save(path,'JPEG',quality=94);paths.append(str(path))
 return paths
if __name__=='__main__':print(json.dumps(render_news(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2])))
