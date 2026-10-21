import json,sys,os,pathlib,math,random,re
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1350
FONT=os.environ.get('CARDFLOW_FONT','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
PALETTES={'relationships':('#161821','#ff644d','#ffdfa5'),'money_life':('#102e29','#d5fb64','#e8f0d3'),'technology':('#162a62','#84b9ff','#e3edff'),'food_travel':('#352251','#e4a2ff','#ffe9ce'),'other':('#18232e','#ffc35c','#f2eadd')}
def font(size):
 if not pathlib.Path(FONT).is_file():raise RuntimeError('KOREAN_FONT_REQUIRED')
 return ImageFont.truetype(FONT,size,index=1)
def wrap(d,text,f,width):
 out=[]
 for para in str(text).split('\n'):
  line=''
  for token in re.findall(r'\S+|\s+',para):
   if d.textlength(line+token,font=f)<=width:line+=token;continue
   if line.strip():out.append(line.rstrip());line=''
   token=token.lstrip()
   for ch in token:
    if d.textlength(line+ch,font=f)>width and line:out.append(line);line=''
    line+=ch
  out.append(line.rstrip())
 return out
def block(d,text,x,y,width,height,size=60,color='#ffffff',spacing=1.35,minsize=25):
 while size>=minsize:
  f=font(size);lines=wrap(d,text,f,width)
  if len(lines)*size*spacing<=height:break
  size-=2
 else:raise RuntimeError('TEXT_OVERFLOW')
 for line in lines:d.text((x,y),line,font=f,fill=color);y+=size*spacing
 return y
def pill(d,xy,text,bg,fg,size=23):
 f=font(size);x,y=xy;width=d.textlength(text,font=f)+36;d.rounded_rectangle((x,y,x+width,y+size+22),radius=20,fill=bg);d.text((x+18,y+5),text,font=f,fill=fg)
def base(category,page,light=False):
 dark,accent,paper=PALETTES.get(category,PALETTES['other']);bg=paper if light else dark;fg=dark if light else paper
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
 grid=tuple(int(c*.88) for c in im.getpixel((0,0))) if light else tuple(min(255,int(c*1.3)+8) for c in im.getpixel((0,0)))
 for x in range(0,W,60):d.line((x,0,x,H),fill=grid,width=1)
 for y in range(0,H,60):d.line((0,y,W,y),fill=grid,width=1)
 # Bounded deterministic texture gives every edition a printed-paper surface.
 rng=random.Random(81)
 for _ in range(5000):
  x,y=rng.randrange(W),rng.randrange(H);p=im.getpixel((x,y));d.point((x,y),fill=tuple(min(255,max(0,v+rng.randint(-5,5))) for v in p))
 d.rectangle((0,0,16,H),fill=accent);d.text((64,42),'CARDFLOW / NEWS',font=font(26),fill=fg)
 d.text((820,45),'FACT / CONTEXT',font=font(20),fill=fg);d.line((64,103,1016,103),fill=fg,width=2)
 for i in range(5):d.rounded_rectangle((64+i*192,1290,240+i*192,1296),radius=3,fill=accent if i==page else grid)
 return im,d,dark,accent,paper,fg

def art(d,category,area,dark,accent,paper):
 x,y=area
 if category=='relationships':
  d.rounded_rectangle((x+55,y+40,x+640,y+245),radius=42,fill=accent);d.polygon([(x+560,y+220),(x+650,y+280),(x+630,y+200)],fill=accent)
  d.text((x+100,y+80),'어떤 사실인가요?',font=font(43),fill=dark)
  d.rounded_rectangle((x+240,y+230,x+855,y+430),radius=42,fill=paper);d.polygon([(x+300,y+400),(x+220,y+470),(x+260,y+380)],fill=paper)
  d.text((x+290,y+275),'맥락도 봐야죠.',font=font(48),fill=dark)
  d.ellipse((x+690,y+60,x+800,y+170),outline=paper,width=7);d.line((x+720,y+112,x+745,y+138,x+777,y+91),fill=paper,width=7)
 elif category=='money_life':
  d.rounded_rectangle((x+135,y+30,x+790,y+440),radius=28,fill=paper)
  for i in range(12):d.ellipse((x+150+i*52,y+422,x+180+i*52,y+452),fill=dark)
  d.text((x+180,y+64),'THE NUMBERS / 경제',font=font(27),fill=dark);d.line((x+180,y+120,x+740,y+120),fill=dark,width=3)
  d.text((x+180,y+145),'₩',font=font(125),fill=dark);d.text((x+355,y+178),'숫자의 맥락\n확인하기',font=font(43),fill=dark)
  d.rectangle((x+180,y+340,x+730,y+385),fill=accent)
  for i in range(0,500,9):d.rectangle((x+200+i,y+349,x+203+i,y+375),fill=dark)
 elif category=='technology':
  d.rounded_rectangle((x+200,y+5,x+690,y+455),radius=44,fill=paper);d.rounded_rectangle((x+225,y+30,x+665,y+425),radius=28,fill=dark)
  for i in range(4):d.line((x+260,y+240+i*35,x+610-i*35,y+240+i*35),fill=accent,width=8)
  d.text((x+280,y+75),'TRY IT',font=font(74),fill=paper);pill(d,(x+555,y+150),'어떤 변화?',accent,dark,26)
 elif category=='food_travel':
  d.rounded_rectangle((x+70,y+65,x+845,y+405),radius=30,fill=accent);d.line((x+620,y+90,x+620,y+380),fill=dark,width=3)
  d.text((x+110,y+110),'NEXT\nWEEKEND',font=font(73),fill=dark);d.text((x+675,y+160),'GO',font=font(62),fill=dark)
  for cx in [x+70,x+845]:d.ellipse((cx-24,y+210,cx+24,y+258),fill=dark)

 else:
  d.rounded_rectangle((x+100,y+30,x+820,y+435),radius=25,fill=paper)
  d.rectangle((x+100,y+30,x+820,y+130),fill=accent)
  d.text((x+140,y+48),'THE NEWS / 주요 이슈',font=font(35),fill=dark)
  d.text((x+140,y+165),'FACT',font=font(88),fill=dark)
  for j in range(3):d.line((x+145,y+300+j*34,x+755-j*65,y+300+j*34),fill=dark,width=7)

def render(m,out):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True);e=m['editorial'];category=e['category'];paths=[]
 for i in range(5):
  im,d,dark,accent,paper,fg=base(category,i,light=i in [1,3])
  pill(d,(64,145),e['label'],accent,dark);d.text((900,151),f'{i+1:02}/05',font=font(24),fill=fg)
  if i==0:
   block(d,e['headline'],64,235,946,410,85,paper,1.23,minsize=39)
   art(d,category,(48,670),dark,accent,paper)
   pill(d,(64,1170),e['hook']+'  →',accent,dark,29)
  elif i==1:
   block(d,'오늘의 소식, 핵심부터.',64,245,940,140,62,dark)
   d.rounded_rectangle((64,430,1016,1010),radius=28,fill=dark)
   pill(d,(100,465),'기사 제목',accent,dark,22)
   block(d,e['headline'],100,535,875,220,49,paper)
   block(d,e['excerpt'] or '공개 소개문이 없습니다. 구체적인 내용은 출처의 원문에서 확인하세요.',100,795,875,165,34,paper,minsize=25)
   block(d,'출처  '+m['source']+'\n'+m['timeLabel'],64,1050,940,100,25,dark)
  elif i==2:
   block(d,e['lens'],64,240,940,210,64,paper)
   for j,q in enumerate(e['questions']):
    y=530+j*192;d.rounded_rectangle((64,y,1016,y+164),radius=20,outline=accent,width=2)
    d.text((91,y+42),f'0{j+1}',font=font(38),fill=accent);block(d,q,188,y+30,775,110,38,paper)
   block(d,e['opinionLabel'],64,1160,940,55,23,paper,minsize=21)
  elif i==3:
   block(d,'나에게 해당하면, 이 순서로.',64,245,940,140,67,dark)
   pill(d,(64,410),'조건 확인 후 실행 체크리스트',dark,paper,25)
   for j,c in enumerate(e['checks']):
    y=535+j*190;d.rounded_rectangle((64,y,1016,y+160),radius=20,fill=dark)
    d.rectangle((99,y+53,139,y+93),outline=accent,width=3);block(d,c,177,y+30,780,110,37,paper)
   block(d,'편집 체크리스트 · 기사 사실과 구분해 읽어주세요.',64,1160,940,60,23,dark,minsize=21)
  else:
   block(d,e['prompt'],64,250,940,220,69,paper)
   for j,text in enumerate([e['a'],e['b']]):
    y=540+j*170;d.rounded_rectangle((64,y,1016,y+140),radius=24,fill=accent if j==0 else paper)
    d.text((99,y+30),['A','B'][j],font=font(48),fill=dark);block(d,text,190,y+30,770,90,40,dark)
   block(d,e['cta'],64,960,940,160,34,paper)
  footer=m['source']+' · '+m['timeLabel'] if i!=4 else 'CARDFLOW NEWS · '+e['kicker']
  block(d,footer,64,1230,945,48,20,fg,minsize=17)
  name=out/f'{i+1:02}.jpg';im.save(name,'JPEG',quality=92,optimize=True);paths.append(str(name))
 return paths
if __name__=='__main__':print(json.dumps(render(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2])))
