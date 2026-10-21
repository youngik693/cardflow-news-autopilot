import json,sys,os,pathlib,math
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1350
FONT=os.environ.get('CARDFLOW_FONT','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
def font(size):
 if not pathlib.Path(FONT).is_file():raise RuntimeError('KOREAN_FONT_REQUIRED')
 return ImageFont.truetype(FONT,size,index=1)
def wrap(draw,text,f,width):
 out=[]
 for para in str(text).split('\n'):
  line=''
  if not para:out.append('');continue
  for ch in para:
   if draw.textlength(line+ch,font=f)>width and line:out.append(line);line=ch
   else:line+=ch
  out.append(line)
 return out
def block(draw,text,y,maxheight,size=72,color='#302840',width=890,spacing=1.42):
 while size>=24:
  f=font(size);lines=wrap(draw,text,f,width)
  if len(lines)*size*spacing<=maxheight:break
  size-=2
 else:raise RuntimeError('TEXT_OVERFLOW')
 for line in lines:draw.text((88,y),line,font=f,fill=color);y+=size*spacing
 return y
def render(model,out):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
 title=model['title'];summary=model.get('description') or '공개 소개문이 제공되지 않은 기사입니다. 원문에서 구체적인 내용을 확인하세요.'
 cards=[(title,'주요 포털에서 확인한 지금의 소식','NEWS NOTE'),('지금 알려진 내용',summary,'SOURCE BRIEF'),('원문에서 이어보세요',model['source']+'\n'+model.get('timeLabel','기사 시각 미제공')+'\n\n'+model['url']+'\n\n기사 제목·공개 소개문을 바탕으로 만든 카드입니다.','READ THE SOURCE')]
 images=[]
 for i,(heading,body,tag) in enumerate(cards):
  image=Image.new('RGB',(W,H),'#eee9f8');d=ImageDraw.Draw(image)
  d.ellipse((690,310,1500,1120),fill='#e2d9f0');d.ellipse((865,460,1240,835),fill='#d5c7e9')
  d.line((88,132,992,132),fill='#c8bbda',width=2);d.line((88,1220,992,1220),fill='#c8bbda',width=2)
  d.text((88,65),'@MY.LOVE.MANUAL',font=font(25),fill='#78638f');d.text((88,178),tag,font=font(23),fill='#9d80b4')
  block(d,heading,285,410 if i==0 else 270,size=84 if i==0 else 72)
  block(d,body,785 if i==0 else 625,260 if i==0 else 500,size=34 if i==0 else 37)
  source=model['source']+' · '+model.get('timeLabel','시각 미제공')
  d.text((88,1163),source[:68],font=font(18),fill='#8c7a9a');d.text((88,1258),'CARDFLOW NEWS',font=font(21),fill='#9683a5');d.text((870,1258),f'{i+1:02d} / 03',font=font(21),fill='#9683a5')
  name=out/f'{i+1:02d}.jpg';image.save(name,'JPEG',quality=92,optimize=True);images.append(str(name))
 return images
if __name__=='__main__':
 model=json.loads(pathlib.Path(sys.argv[1]).read_text());print(json.dumps(render(model,sys.argv[2])))
