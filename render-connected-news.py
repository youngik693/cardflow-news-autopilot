"""Question → visual explanation → conclusion. Review only, no publishing."""
import json,pathlib,sys,math
from PIL import Image,ImageDraw,ImageOps
from importlib.util import spec_from_file_location,module_from_spec
spec=spec_from_file_location('deep',pathlib.Path(__file__).with_name('render-deep-news.py'));v=module_from_spec(spec);spec.loader.exec_module(v)
W,H=1080,1350
INK,PAPER,RED,GOLD,GRAY,LINE=v.INK,v.PAPER,v.RED,v.GOLD,v.GRAY,v.LINE
BLUE='#4082a9';SKY='#a6d9f4';IVORY='#eae2d4';LIGHT='#edf4f6';STEPS=['왜 합병','연결 이유','우주 AI','합병 효과','파급효과']
PAGES=[
 {'question':'머스크는 왜\n두 회사를 합치려 하나?','deck':'공시·외부 분석을 종합한 해석 / 합병 미확정','answer':'차·로봇과 우주 AI에 필요한 자원을\n한 회사 안에서 배분하려는 구상이다.','next':'03  자동차와 우주는 무슨 관계일까?','refs':'SpaceX 회사 공시 · Morningstar 2026.06.09'},
 {'question':'자동차와 우주,\n왜 연결하나?','deck':'제품은 달라도, 둘 다 더 많은 AI가 필요하다.','answer':'두 사업 모두 AI 칩·연산 자원이 필요해,\n지상용·우주용 칩을 함께 개발하려는 구상.','next':'04  그렇다면 AI를 왜 우주로 보내나?','refs':'SpaceX SEC 공시 2026.06.05 · Terafab'},
 {'question':'왜 AI를 우주에서\n돌리려 하나?','deck':'지상에서 부족해지는 전력을 우주에서도 찾는 구상.','answer':'우주 태양광과 발사·위성 기술로\nAI 연산 기반을 넓히겠다는 계획이다.','next':'05  협력만 해도 되는데, 왜 합병까지?','refs':'SpaceX SEC 공시 2026.06.05 · 회사 목표'},
 {'question':'이미 협업 중인데,\n왜 합병까지?','deck':'기술을 함께 개발하는 것과 자원을 나누는 것은 다르다.','answer':'기술 협력에 더해 인력·투자를\n내부에서 유연하게 배분할 수 있다는 분석.','next':'06  이 구상이 돈의 흐름을 바꿀까?','refs':'Morningstar 2026.06.09 · 독립 분석'},
 {'question':'이 구상의\n파급효과는?','deck':'기대 효과가 실제 이익이 되려면 조건이 필요하다.','answer':'기업의 원가·공급망 발주·주주의 지분,\n이 세 가지가 경제효과를 가른다.','next':'07  마지막 한 장에 다섯 가지 핵심 요약 →','refs':'SpaceX 공시 · Morningstar · 조건부 시나리오'}
]
def tx(d,*a,**kw):return v.tx(d,*a,**kw)
def box(d,*a,**kw):return v.box(d,*a,**kw)
def arrow(d,x,y,c=RED,length=38):
 d.line((x,y,x+length-8,y),fill=c,width=4);d.polygon([(x+length,y),(x+length-14,y-9),(x+length-14,y+9)],fill=c)
def panel(d,r,fill=PAPER,outline=None):d.rounded_rectangle(r,radius=22,fill=fill,outline=outline,width=2)
def bubble(d,y,h,fill,label,text,textcolor):
 panel(d,(52,y,1028,y+h),fill)
 tx(d,label,77,y+15,24,textcolor,True)
 box(d,text,77,y+53,926,h-64,55 if label=='이번 장의 질문' else 38,textcolor,True)
def icon(d,kind,x,y,c=INK):
 if kind=='car':
  d.rounded_rectangle((x,y+28,x+103,y+65),radius=12,outline=c,width=5);d.line([(x+18,y+27),(x+33,y+4),(x+73,y+4),(x+90,y+27)],fill=c,width=5)
  for xx in [x+23,x+81]:d.ellipse((xx-10,y+56,xx+10,y+76),fill=c)
 elif kind=='rocket':
  d.polygon([(x+51,y),(x+76,y+35),(x+76,y+69),(x+27,y+69),(x+27,y+35)],outline=c,width=5);d.ellipse((x+43,y+29,x+59,y+45),outline=c,width=4);d.line((x+41,y+77,x+35,y+97),fill=RED,width=5);d.line((x+62,y+77,x+69,y+97),fill=RED,width=5)
 elif kind=='sun':
  d.ellipse((x+28,y+25,x+74,y+71),outline=c,width=5)
  for k in range(8):
   a=k*math.pi/4;d.line((x+51+34*math.cos(a),y+48+34*math.sin(a),x+51+47*math.cos(a),y+48+47*math.sin(a)),fill=c,width=4)
 elif kind=='sat':
  d.rectangle((x+37,y+29,x+69,y+61),outline=c,width=4)
  for xx in [x,x+77]:d.rectangle((xx,y+24,xx+28,y+67),outline=c,width=4)
  d.line((x+53,y+29,x+70,y+9),fill=c,width=4);d.arc((x+63,y,x+94,y+24),180,350,fill=c,width=4)
 elif kind=='chip':
  d.rectangle((x+24,y+20,x+78,y+74),outline=c,width=5)
  for k in range(4):
   a=29+k*12;d.line((x+9,y+a,x+24,y+a),fill=c,width=3);d.line((x+78,y+a,x+93,y+a),fill=c,width=3)
 elif kind=='power':d.polygon([(x+57,y),(x+23,y+53),(x+49,y+53),(x+40,y+94),(x+83,y+38),(x+57,y+38)],fill=c)
 else:
  for k in range(3):d.rounded_rectangle((x+5+k*30,y+57-k*19,x+26+k*30,y+91),radius=3,fill=c)
def base(i):
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im);p=PAGES[i]
 tx(d,'1분 리포트',52,23,32,INK,True);tx(d,'테슬라·스페이스X / 2026.10.21 기준',277,29,22,GRAY);tx(d,f'{i+2:02}/07',941,30,23)
 for j,s in enumerate(STEPS):
  x=52+j*202;panel(d,(x,94,x+161,147),INK if i==j else '#e7e4dd');tx(d,s,x+16,104,25,'white' if i==j else GRAY,i==j)
  if j<4:arrow(d,x+167,120,length=29)
 bubble(d,179,222,IVORY,'이번 장의 질문',p['question'],INK)
 box(d,p['deck'],52,440,976,76,30,GRAY)
 return im,d

def tail(d,i):
 p=PAGES[i];bubble(d,1080,155,SKY,'한 줄 결론',p['answer'],INK)
 tx(d,p['next'],52,1264,23,INK,True)
 tx(d,'근거: '+p['refs']+' · 합병 미확정',52,1304,19,GRAY)

def cover(photo):
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 tx(d,'1분 리포트',52,24,39,INK,True);tx(d,'2026.10.21 / 합병 검토',485,35,25,GRAY);tx(d,'01/07',942,36,23,INK)
 im.paste(ImageOps.fit(Image.open(photo).convert('RGB'),(1080,748),centering=(.5,.28)),(0,109));d=ImageDraw.Draw(im)
 d.rectangle((0,857,1080,1350),fill=INK)
 tx(d,'테슬라 × 스페이스X',52,885,27,'#a6d9f4',True)
 box(d,'왜 합병을\n검토하나',52,939,976,221,88,'white',True)
 box(d,'자동차·로봇과 우주 AI를\n하나의 전략으로 묶으려는 이유',52,1170,976,100,37,'#eae2d4')
 tx(d,'자료사진 NASA / Keegan Barber · 2024.09.27',52,811,20,'white')
 tx(d,'바쁘다면 마지막 장 핵심 요약 →',52,1287,26,'#a6d9f4',True)
 tx(d,'합병 미확정 · 공시와 외부 분석을 종합한 해설',52,1324,16,'#b9c4cc')
 return im

def summary_card():
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 tx(d,'1분 리포트',52,25,35,INK,True);tx(d,'테슬라·스페이스X / 핵심 요약',278,34,24,GRAY);tx(d,'07/07',941,34,23,INK)
 d.line((52,103,1028,103),fill=LINE,width=2)
 tx(d,'다섯 장을 한눈에',52,141,28,BLUE,True)
 box(d,'머스크의 합병 구상,\n핵심은 이 다섯 가지',52,190,976,166,61,INK,True)
 rows=[('왜 합치나?','AI 칩·인력·투자를 함께 배분'),('차와 우주는?','차·로봇도 우주 AI도 연산 자원이 필요'),('왜 우주 AI?','태양광·발사·위성 기술로 연산 기반 확대'),('협업보다 합병?','회사 간 자원 이동의 마찰을 줄일 가능성'),('경제적 파장은?','원가·실제 발주·주주 지분을 확인')]
 for j,(question,answer) in enumerate(rows):
  y=400+j*122
  tx(d,f'0{j+1}',52,y+12,28,BLUE,True)
  tx(d,question,115,y+5,31,GRAY,True)
  box(d,answer,115,y+51,913,61,35,INK,True)
  d.line((115,y+117,1028,y+117),fill=LINE,width=1)
 panel(d,(52,1056,1028,1215),SKY)
 tx(d,'그래서 무엇을 봐야 하나',77,1072,25,INK,True)
 box(d,'AI 자원을 묶는 구상, 이익은 실행에 달렸다.\n실제 투자·원가·합병 조건을 확인하자.',77,1116,926,88,35,INK,True)
 tx(d,'2026.10.21 기준 · 합병 미확정 · 계획·분석·조건부 전망의 요약',52,1246,22,GRAY)
 tx(d,'근거: SpaceX 공시 · Terafab · Morningstar 2026.06.09',52,1288,22,GRAY)
 return im

def render(model,out,photo):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True);pages=[cover(photo)]
 pages[0].save(out/'01.jpg',quality=95,optimize=True)
 for i in range(5):
  im,d=base(i)
  if i==0:
   im.paste(ImageOps.fit(Image.open(photo).convert('RGB'),(976,286),centering=(.5,.3)),(52,529));d=ImageDraw.Draw(im)
   tx(d,'자료사진 NASA / Keegan Barber · 2024.09.27',52,823,20,GRAY)
   for x,title,sub,col in [(52,'테슬라','차 · 로봇',RED),(573,'스페이스X','우주 · 통신 · AI',BLUE)]:
    panel(d,(x,883,x+455,1024),'#ffffff',LINE);tx(d,title,x+24,897,36,col,True);tx(d,sub,x+24,957,29,GRAY)
   tx(d,'+',523,926,42,INK,True)
  elif i==1:
   for x,title,sub,kind,col in [(52,'테슬라','차·로봇의 AI','car',RED),(573,'스페이스X','AI 서비스·우주 연산','rocket',BLUE)]:
    panel(d,(x,535,x+455,756),'#ffffff',LINE);icon(d,kind,x+27,564,col);tx(d,title,x+150,558,38,col,True);box(d,sub,x+150,622,283,88,29,GRAY)
   d.line([(280,759),(280,790),(800,790),(800,759)],fill=GRAY,width=4);v.down(d,540,790)
   for j,(title,kind) in enumerate([('AI 칩','chip'),('연산 설비','bars'),('전력','power')]):
    x=52+j*334;panel(d,(x,856,x+308,1014),LIGHT);icon(d,kind,x+15,884,BLUE);tx(d,title,x+122,908,32,INK,True)
   tx(d,'Terafab: 지상용·우주용 칩 개발 구상 / 외부 조달도 지속',52,1033,23,GRAY)
  elif i==2:
   for j,(title,sub,kind) in enumerate([('태양광','AI를 돌릴 전력 확보','sun'),('재사용 로켓','AI 위성을 궤도로 운송','rocket'),('위성 운영 기술','궤도 연산망에 경험 활용','sat')]):
    y=535+j*151;panel(d,(52,y,1028,y+135),'#ffffff',LINE);icon(d,kind,78,y+17,BLUE);tx(d,title,215,y+20,34,INK,True);arrow(d,492,y+65,BLUE);box(d,sub,566,y+38,432,73,32)
   box(d,'회사 계획: 지상 전력 제약을 넘으려는 접근.\n우주 AI의 비용·냉각·운영 경제성은 검증 과제.',52,1001,976,77,25,GRAY)
  elif i==3:
   panel(d,(52,535,1028,748),'#ffffff',LINE);tx(d,'지금: 서로 다른 회사',78,548,31,GRAY,True)
   for x,title,col in [(79,'테슬라',RED),(589,'스페이스X',BLUE)]:
    panel(d,(x,610,x+412,718),PAPER);tx(d,title,x+22,619,31,col,True);tx(d,'인력·예산을 별도로 조율',x+22,668,25,GRAY)
   v.down(d,540,760,BLUE)
   panel(d,(52,827,1028,977),LIGHT);tx(d,'합병 시: 하나의 회사 안에서',78,841,32,BLUE,True)
   tx(d,'AI 프로젝트  ←  인력 · 투자  →  AI 프로젝트',78,903,35,INK,True)
   box(d,'Morningstar의 합병 논리. 자원 이동의 마찰을 줄일 가능성이며,\n실제 개발 속도·이익 개선이 입증됐다는 뜻은 아니다.',52,1000,976,77,24,GRAY)
  else:
   for j,(a,b,c) in enumerate([('AI 개발 효율','원가·개발 기간 개선','칩 공급과 성능 개선이 전제'),('공급망 투자','공장·설비 발주 기회','실제 투자 집행이 전제'),('주주의 이익','통합 사업 성과 참여','교환비율·투자 부담을 확인')]):
    y=535+j*155;panel(d,(52,y,1028,y+139),'#ffffff',LINE)
    d.ellipse((74,y+28,142,y+96),fill=BLUE);tx(d,str(j+1),95,y+36,33,'white',True)
    tx(d,a,166,y+19,33,INK,True);arrow(d,438,y+62,RED);tx(d,b,516,y+17,31,BLUE,True);tx(d,c,516,y+75,25,GRAY)
   tx(d,'조건부 전망 · 확정 수혜나 합병에 따른 절감액은 아직 없음',52,1030,24,GRAY)
  tail(d,i);im.save(out/f'{i+2:02}.jpg',quality=95,optimize=True);pages.append(im)
 pages.append(summary_card());pages[-1].save(out/'07.jpg',quality=95,optimize=True)
 sheet=Image.new('RGB',(1680,2155),'#dedbd6')
 for i,im in enumerate(pages):sheet.paste(im.resize((540,675)),(10+(i%3)*560,10+(i//3)*715))
 sheet.save(out/'preview.jpg',quality=95)
if __name__=='__main__':render(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2],sys.argv[3])
