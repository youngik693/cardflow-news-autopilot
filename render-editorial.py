"""Four-page editorial layout. Real archive photography, explicit attribution, no generated scenes."""
import json,sys,pathlib,urllib.request,os
from PIL import Image,ImageDraw,ImageFont,ImageOps
from render import block,font
W,H=1080,1350
INK='#10151c';PAPER='#f5f2ec';RED='#e43932';YELLOW='#ffcf40';MUTED='#66707b'
def f(size,bold=False):
 from render import FONT
 path=os.environ.get('CARDFLOW_BOLD_FONT',FONT.replace('Regular','Bold')) if bold else FONT
 if not pathlib.Path(path).is_file():raise RuntimeError('BOLD_FONT_REQUIRED' if bold else 'KOREAN_FONT_REQUIRED')
 return ImageFont.truetype(path,size,index=1)
def text(d,s,xy,size=30,fill=INK,bold=False):d.text(xy,s,font=f(size,bold),fill=fill)
def para(d,s,x,y,width,height,size=44,fill=INK):return block(d,s,x,y,width,height,size,fill,1.32,minsize=size-8)
def top(im,page,dark=False,section='기업·테크'):
 d=ImageDraw.Draw(im);fg='white' if dark else INK
 text(d,'카드플로우',(54,32),34,fg,True);text(d,section,(295,40),24,'#cbd1d8' if dark else MUTED)
 text(d,f'{page:02} / 04',(916,42),22,fg);d.line((54,104,1026,104),fill='#49505a' if dark else '#b9babe',width=2)
 return d
def footer(d,m,dark=False):
 c='#bfc5cd' if dark else MUTED
 text(d,m['press']['sourceShort'],(54,1247),20,c)
 text(d,m['press']['asOf'],(54,1281),20,c)
def cover(m,photo):
 im=Image.new('RGB',(W,H),INK);p=ImageOps.fit(photo,(W,1110),method=Image.Resampling.LANCZOS,centering=(.5,.35));im.paste(p,(0,110))
 overlay=Image.new('RGBA',(W,H),(0,0,0,0));od=ImageDraw.Draw(overlay)
 for y in range(650,H):od.line((0,y,W,y),fill=(10,14,20,min(255,int((y-650)/550*255))),width=1)
 im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB');d=top(im,1,True)
 d.rectangle((54,151,236,199),fill=YELLOW);text(d,'쟁점 브리핑',(68,154),27,INK,True)
 text(d,'TESLA × SPACEX',(54,748),32,'#f2e4bb',True)
 # Headline uses a bold face; fixed content is constrained to two lines.
 for j,line in enumerate(m['press']['headline'].split('\n')):text(d,line,(48,804+j*112),91,'white',True)
 para(d,m['press']['deck'],54,1054,960,112,36,'white')
 text(d,m['press']['photo']['caption'],(54,1178),21,'#d8dde3')
 footer(d,m,True);return im

def context(m):
 im=Image.new('RGB',(W,H),PAPER);d=top(im,2)
 text(d,'01  왜 중요한가',(54,151),25,RED,True)
 para(d,m['press']['whyTitle'],54,215,972,230,68)
 text(d,'머스크가 기대한다고 밝힌 기술 결합',(54,446),30,MUTED)
 for x,name,sub,items,col in [(54,'TESLA','자동차 · 로봇',['자율주행','휴머노이드'],RED),(568,'SPACEX','우주 · 통신',['위성인터넷','AI 연산 인프라'],INK)]:
  d.line((x,536,x+456,536),fill=col,width=8);text(d,name,(x,570),45,col,True);text(d,sub,(x,648),34)
  for j,it in enumerate(items):text(d,it,(x,725+j*65),32,MUTED)
 d.line((510,626,550,626),fill=RED,width=4);d.polygon([(550,626),(540,619),(540,633)],fill=RED);d.polygon([(510,626),(520,619),(520,633)],fill=RED)
 d.rectangle((54,925,1026,1146),fill=INK);text(d,'핵심 구상',(82,949),24,YELLOW,True)
 para(d,'AI 개발 · 반도체 · 로봇\n협력의 범위를 넓히는 것',82,1000,918,125,42,'white')
 text(d,'결합 효과는 기대 단계이며 실현이 확인된 것은 아닙니다.',(54,1185),23,MUTED)
 footer(d,m);return im

def facts(m):
 im=Image.new('RGB',(W,H),INK);d=top(im,3,True)
 text(d,'02  사실의 경계',(54,151),25,YELLOW,True)
 para(d,'검토는 시작됐다.\n합병은 결정되지 않았다.',54,222,972,240,64,'white')
 d.line((54,526,1026,526),fill='#424a56',width=2)
 text(d,'확인',(54,572),32,'#91d5b4',True)
 para(d,'양사 특별위원회 구성\n독립 이사들이 합병 가능성 검토',235,566,791,170,40,'white')
 d.line((54,790,1026,790),fill='#424a56',width=2)
 text(d,'미확정',(54,839),32,'#ff8f81',True)
 para(d,'거래 조건은 아직 합의 전\n실제 성사 여부도 미정',235,832,791,170,40,'white')
 text(d,'머스크는 이해상충 때문에 위원회 논의에 참여하지 않는다고 설명.',(54,1107),24,'#bfc5cd')
 footer(d,m,True);return im

def next_steps(m):
 im=Image.new('RGB',(W,H),PAPER);d=top(im,4)
 text(d,'03  다음에 볼 것',(54,151),25,RED,True)
 para(d,'다음 뉴스는\n여기서 갈린다.',54,215,972,220,72)
 steps=[('거래 조건 합의','특별위원회가 조건에 합의하는가'),('주주 승인','주주들이 합병안을 지지하는가'),('실제 거래 성사','최종 합의와 남은 절차가 진행되는가')]
 d.line((83,516,83,938),fill='#c5c7c9',width=4)
 for j,(title,body) in enumerate(steps):
  y=508+j*169;d.ellipse((61,y,105,y+44),fill=RED if j==0 else INK);text(d,str(j+1),(75,y+2),25,'white',True)
  text(d,title,(145,y-3),40,INK,True);text(d,body,(145,y+65),29,MUTED)
 d.rectangle((0,1040,W,1224),fill=INK)
 text(d,'테크·기업 뉴스, 왜 중요한지 4장으로.',(54,1067),37,'white',True)
 text(d,'핵심과 다음 변수까지  ·  @my.love.manual',(54,1142),29,YELLOW)
 footer(d,m);return im

def render_editorial(m,out,photo_path=None):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
 if photo_path:photo=Image.open(photo_path).convert('RGB')
 else:
  u=m['press']['photo']['url']
  from urllib.parse import urlsplit
  p=urlsplit(u)
  if p.scheme!='https' or p.hostname!='images-assets.nasa.gov':raise ValueError('UNAPPROVED_PHOTO_HOST')
  with urllib.request.urlopen(u,timeout=25) as r:
   raw=r.read(6000001)
  if len(raw)>6000000:raise ValueError('PHOTO_TOO_LARGE')
  from io import BytesIO
  photo=Image.open(BytesIO(raw)).convert('RGB')
 pages=[cover(m,photo),context(m),facts(m),next_steps(m)];paths=[]
 for i,im in enumerate(pages):
  p=out/f'{i+1:02}.jpg';im.save(p,'JPEG',quality=95,optimize=True);paths.append(str(p))
 sheet=Image.new('RGB',(1120,1440),'#dedbd6')
 for i,im in enumerate(pages):sheet.paste(im.resize((540,675)),(10+(i%2)*560,10+(i//2)*715))
 sheet.save(out/'preview.jpg','JPEG',quality=94)
 return paths
if __name__=='__main__':print(json.dumps(render_editorial(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2],sys.argv[3] if len(sys.argv)>3 else None)))
