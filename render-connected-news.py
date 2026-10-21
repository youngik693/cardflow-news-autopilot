"""Question → visual explanation → conclusion. Review only, no publishing."""
import json,pathlib,sys,math
from PIL import Image,ImageDraw,ImageOps
from importlib.util import spec_from_file_location,module_from_spec
spec=spec_from_file_location('deep',pathlib.Path(__file__).with_name('render-deep-news.py'));v=module_from_spec(spec);spec.loader.exec_module(v)
W,H=1080,1350
INK,PAPER,RED,GOLD,GRAY,LINE=v.INK,v.PAPER,v.RED,v.GOLD,v.GRAY,v.LINE
BLUE='#4082a9';SKY='#a6d9f4';IVORY='#eae2d4';LIGHT='#edf4f6';STEPS=['왜 합병','연결 이유','우주 AI','합병 효과','파급효과']
PAGES=[
 {'question':'머스크는 왜\n두 회사를 합치려 하나?','deck':'공시·외부 분석을 종합한 해석 / 합병 미확정','answer':'차·로봇과 우주 AI에 필요한 칩·개발자·돈을\n한 회사에서 함께 쓰려는 구상이다.','next':'03  자동차와 우주는 무슨 관계일까?','refs':'SpaceX 회사 공시 · Morningstar 2026.06.09'},
 {'question':'자동차와 우주,\n왜 연결하나?','deck':'제품은 달라도, 둘 다 더 많은 AI가 필요하다.','answer':'차·로봇도 우주 AI도 고성능 컴퓨터가 필요하다.\n그 핵심 부품인 AI 칩을 함께 만들려는 구상.','next':'04  그렇다면 AI를 왜 우주로 보내나?','refs':'SpaceX SEC 공시 2026.06.05 · Terafab'},
 {'question':'왜 AI 컴퓨터를\n우주로 보내려 하나?','deck':'AI에 필요한 전기를 우주 태양광으로 얻겠다는 계획.','answer':'우주에서 전기를 만들어 AI 컴퓨터를 돌리려는 계획.\n실제로 가능한지, 비용은 얼마나 들지 확인해야 한다.','next':'05  협력만 해도 되는데, 왜 합병까지?','refs':'SpaceX SEC 공시 2026.06.05 · 회사 목표'},
 {'question':'이미 협업 중인데,\n왜 합병까지?','deck':'함께 기술을 만드는 것과 인력·돈을 함께 쓰는 것은 다르다.','answer':'예: 테슬라 개발자를 스페이스X AI 개발에도\n배치하기 쉬워질 수 있다는 분석이다.','next':'06  이 구상이 돈의 흐름을 바꿀까?','refs':'Morningstar 2026.06.09 · 독립 분석'},
 {'question':'이 구상의\n파급효과는?','deck':'기대 효과가 실제 이익이 되려면 조건이 필요하다.','answer':'개발비가 줄고 장비 주문이 늘어날지는 실행에 달렸다.\n주주에게 유리한지는 합병 조건도 확인해야 한다.','next':'07  마지막 한 장에 다섯 가지 핵심 요약 →','refs':'SpaceX 공시 · Morningstar · 조건부 시나리오'}
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
 if i==0:
  tx(d,'1분속보리포트',52,23,35,'#c5352c',True);tx(d,'테슬라·스페이스X / 2026.10.21',340,33,21,GRAY)
 else:tx(d,'테슬라·스페이스X / 2026.10.21 기준',52,29,24,GRAY)
 tx(d,f'{i+2:02}/07',941,30,23)
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
 tx(d,'2026.10.21',64,32,28,GRAY);tx(d,'테슬라·스페이스X 합병 검토',407,35,25,INK);tx(d,'01/07',942,36,23,INK)
 im.paste(ImageOps.fit(Image.open(photo).convert('RGB'),(1080,748),centering=(.5,.28)),(0,109));d=ImageDraw.Draw(im)
 d.rectangle((0,807,1080,857),fill=INK)
 tx(d,'자료사진 NASA / Keegan Barber · 2024.09.27',64,817,21,'#d1dae0')
 d.rectangle((0,857,1080,1350),fill=INK)
 tx(d,'테슬라 × 스페이스X',64,884,56,'#a6d9f4',True)
 d.line((64,979,1016,979),fill='#3e4d57',width=2)
 box(d,'왜 합병을 검토하나',64,1000,952,102,73,'white',True)
 box(d,'자동차·로봇과 우주 AI,\n두 회사를 하나로 묶으려는 이유',64,1121,952,108,38,'#eae2d4')
 d.line((64,1253,1016,1253),fill='#3e4d57',width=1)
 tx(d,'마지막 장에 핵심 요약 →',64,1274,26,'#a6d9f4',True)
 tx(d,'합병 미확정 · 자료 종합 해석',64,1314,18,'#b9c4cc')
 return im

def summary_card():
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 tx(d,'테슬라·스페이스X / 핵심 요약',52,34,27,GRAY);tx(d,'07/07',941,34,23,INK)
 d.line((52,103,1028,103),fill=LINE,width=2)
 tx(d,'다섯 장을 한눈에',52,141,28,BLUE,True)
 box(d,'머스크의 합병 구상,\n핵심은 이 다섯 가지',52,190,976,166,61,INK,True)
 rows=[('왜 합치나?','AI 칩·개발자·돈을 한 회사에서 함께 쓰려는 구상'),('차와 우주는?','차·로봇도 우주 AI도 고성능 컴퓨터가 필요'),('왜 우주 AI?','우주 태양광으로 AI 컴퓨터를 돌리려는 계획'),('협업보다 합병?','개발자가 두 회사의 AI 개발을 오가기 쉬워질 수 있음'),('경제적 파장은?','개발비·장비 주문·주주에게 남는 몫을 확인')]
 for j,(question,answer) in enumerate(rows):
  y=400+j*122
  tx(d,f'0{j+1}',52,y+12,28,BLUE,True)
  tx(d,question,115,y+5,31,GRAY,True)
  box(d,answer,115,y+51,913,61,35,INK,True)
  d.line((115,y+117,1028,y+117),fill=LINE,width=1)
 panel(d,(52,1056,1028,1215),SKY)
 tx(d,'그래서 무엇을 봐야 하나',77,1072,25,INK,True)
 box(d,'AI에 필요한 칩·사람·돈을 함께 쓰려는 구상.\n실제 이익이 날지, 합병 조건이 유리할지 봐야 한다.',77,1116,926,88,35,INK,True)
 tx(d,'2026.10.21 기준 · 합병 미확정 · 계획·분석·조건부 전망의 요약',52,1246,22,GRAY)
 tx(d,'근거: SpaceX 공시 · Terafab · Morningstar 2026.06.09',52,1288,22,GRAY)
 return im

def render(model,out,photo):
 global PAGES
 PAGES=model.get('copy',PAGES)
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
   for x,title,sub,kind,col in [(52,'테슬라','차가 스스로 운전하고\n로봇이 움직이게 할 AI','car',RED),(573,'스페이스X','AI 컴퓨터를\n우주에서도 돌릴 계획','rocket',BLUE)]:
    panel(d,(x,525,x+455,684),'#ffffff',LINE)
    tx(d,title,x+23,538,34,col,True)
    box(d,sub,x+23,594,409,80,28,INK)
    small=Image.new('RGB',(115,105),'white');icon(ImageDraw.Draw(small),kind,5,3,col);im.paste(small.resize((66,60)),(x+365,537))
   d=ImageDraw.Draw(im)
   d.line([(280,685),(280,708),(800,708),(800,685)],fill=GRAY,width=3);v.down(d,540,707,BLUE)
   tx(d,'둘 다 AI를 돌릴 장비와 전기가 필요하다',52,761,36,INK,True)
   for j,(title,meaning) in enumerate([('AI 칩','AI가 계산하는 부품'),('컴퓨터','AI 프로그램을 실행하는 기계'),('전기','칩과 컴퓨터를 작동시킴')]):
    x=52+j*334;panel(d,(x,829,x+308,952),LIGHT)
    tx(d,title,x+20,841,32,BLUE,True)
    box(d,meaning,x+20,897,268,50,24,INK)
   panel(d,(52,974,1028,1057),IVORY)
   box(d,'그래서 → AI 칩을 함께 만드는 공장(Terafab) 추진',75,994,930,52,30,INK,True)
  elif i==2:
   for j,(title,sub,kind) in enumerate([('태양광','태양빛으로 전기를 만들어\nAI 컴퓨터에 공급한다','sun'),('로켓','AI 컴퓨터를 실은 위성을\n로켓으로 우주에 보낸다','rocket'),('위성 기술','위성을 만들고 운영한 기술을\n우주 AI 컴퓨터에도 쓴다','sat')]):
    y=525+j*157;panel(d,(52,y,1028,y+145),'#ffffff',LINE);icon(d,kind,78,y+24,BLUE);tx(d,title,215,y+36,34,INK,True);arrow(d,455,y+72,BLUE);box(d,sub,520,y+29,480,105,31)
   box(d,'회사의 구상이다. 실제로 우주에서 컴퓨터를 돌릴 때 드는 비용과\n열을 식히는 문제, 고장 없이 운영할 수 있는지는 더 확인해야 한다.',52,1008,976,69,24,GRAY)
  elif i==3:
   panel(d,(52,535,1028,748),'#ffffff',LINE);tx(d,'지금: 서로 다른 회사',78,548,31,GRAY,True)
   for x,title,col in [(79,'테슬라',RED),(589,'스페이스X',BLUE)]:
    panel(d,(x,610,x+412,718),PAPER);tx(d,title,x+22,619,31,col,True);tx(d,'인력·돈을 따로 관리',x+22,668,25,GRAY)
   v.down(d,540,760,BLUE)
   panel(d,(52,827,1028,977),LIGHT);tx(d,'합병하면 이런 배치가 쉬워질 수 있다',78,841,32,BLUE,True)
   tx(d,'예: 테슬라 개발자  →  스페이스X AI 개발',78,903,35,INK,True)
   box(d,'위 인력 배치는 Morningstar 분석을 풀어 쓴 예시로, 확정 인사가 아니다.\n실제로 개발이 빨라지고 이익이 늘지는 아직 확인되지 않았다.',52,1000,976,77,24,GRAY)
  else:
   for j,(a,b,c) in enumerate([('AI 개발 비용','개발 시간·비용 절감','필요한 칩의 공급·성능이 좋아질 때'),('공장·설비 업체','관련 주문 증가 가능','실제 공장 투자·장비 주문이 있어야'),('주주에게 남는 몫','합병 조건에 따라 달라짐','받을 주식 수·투자 부담을 확인')]):
    y=535+j*155;panel(d,(52,y,1028,y+139),'#ffffff',LINE)
    d.ellipse((74,y+28,142,y+96),fill=BLUE);tx(d,str(j+1),95,y+36,33,'white',True)
    box(d,a,166,y+19,260,99,31,INK,True);arrow(d,438,y+62,RED);box(d,b,516,y+17,485,52,30,BLUE,True);box(d,c,516,y+75,485,54,24,GRAY)
   tx(d,'조건부 전망 · 확정 수혜나 합병에 따른 절감액은 아직 없음',52,1030,24,GRAY)
  tail(d,i);im.save(out/f'{i+2:02}.jpg',quality=95,optimize=True);pages.append(im)
 pages.append(summary_card());pages[-1].save(out/'07.jpg',quality=95,optimize=True)
 sheet=Image.new('RGB',(1680,2155),'#dedbd6')
 for i,im in enumerate(pages):sheet.paste(im.resize((540,675)),(10+(i%3)*560,10+(i//3)*715))
 sheet.save(out/'preview.jpg',quality=95)
if __name__=='__main__':render(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2],sys.argv[3])
