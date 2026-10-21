"""Five connected editorial cards. Review images only; no publishing calls."""
import json, pathlib, sys
from PIL import Image,ImageDraw,ImageOps
from importlib.util import spec_from_file_location,module_from_spec
spec=spec_from_file_location('deep',pathlib.Path(__file__).with_name('render-deep-news.py'));v=module_from_spec(spec);spec.loader.exec_module(v)
W,H=1080,1350
INK,PAPER,RED,GOLD,GRAY,LINE=v.INK,v.PAPER,v.RED,v.GOLD,v.GRAY,v.LINE
STEPS=['구상','병목','우주','합병','파장']
PAGES=[
 {'theme':'차·로봇과 우주 AI를 한 전략으로','headline':'테슬라·스페이스X,\n왜 합치려 하나','next':'AI를 함께 키우려면?','nextTopic':'02  먼저 해결할 공통 병목','refs':'근거: SpaceX 공시 · Morningstar 2026.06.09'},
 {'theme':'AI 확대의 병목은 칩·연산·전력','headline':'서로 다른 사업이\n같은 자원을 필요로 한다','next':'전력 부족을 어디서 풀까?','nextTopic':'03  우주 인프라가 맡을 역할','refs':'근거: SpaceX SEC 공시 2026.06.05 · Terafab'},
 {'theme':'우주 전력을 AI 인프라로 활용','headline':'로켓·위성 기술을\nAI 확장의 기반으로','next':'그런데, 이미 협력하는데?','nextTopic':'04  합병이 더하는 자원 배분','refs':'근거: SpaceX SEC 공시 2026.06.05 · 회사 구상'},
 {'theme':'합병의 추가 논리는 내부 자원 배분','headline':'인력과 투자금을\n한 회사 안에서 조정','next':'그럼 실제로 무엇이 달라질까?','nextTopic':'05  경제효과와 확인 조건','refs':'근거: Morningstar 2026.06.09 · 독립 분석'},
 {'theme':'경제효과는 원가·발주·지분으로 판단','headline':'합병 소식 다음엔\n실제 이익이 되는지 본다','next':'구상 → 병목 → 우주 → 합병 → 파장','nextTopic':'핵심: 연결의 논리와 실행 조건을 함께 본다','refs':'근거: SpaceX 공시 · Morningstar · 조건부 시나리오'}
]
def tx(d,*a,**kw):return v.tx(d,*a,**kw)
def box(d,*a,**kw):return v.box(d,*a,**kw)
def arrow(d,x,y,c):
 d.line((x,y,x+28,y),fill=c,width=3);d.polygon([(x+36,y),(x+24,y-7),(x+24,y+7)],fill=c)
def base(i):
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 tx(d,'카드플로우',52,22,32,INK,True);tx(d,'테슬라·스페이스X / 합병 검토',280,29,25,GRAY);tx(d,f'{i+1:02}/05',941,30,23)
 for j,s in enumerate(STEPS):
  x=52+j*202;active=j==i
  d.rounded_rectangle((x,96,x+157,151),radius=27,fill=INK if active else '#e9e6df')
  tx(d,f'{j+1} {s}',x+19,105,26,'white' if active else GRAY,active)
  if j<4:arrow(d,x+164,124,RED)
 p=PAGES[i]
 # The large topic sign is an informative conclusion, directly below the masthead/reading route.
 d.rounded_rectangle((52,186,1028,276),radius=20,fill=GOLD)
 d.polygon([(97,275),(123,297),(147,275)],fill=GOLD)
 box(d,p['theme'],76,201,928,64,43,INK,True)
 box(d,p['headline'],52,323,976,177,65,INK,True)
 return im,d

def tail(d,i):
 p=PAGES[i]
 d.rounded_rectangle((52,1134,1028,1240),radius=15,fill=INK)
 tx(d,p['next'],75,1146,28,GOLD,True)
 if i<4:
  tx(d,p['nextTopic'],75,1188,29,'white',True);arrow(d,951,1208,GOLD)
 else:tx(d,p['nextTopic'],75,1188,28,'white',True)
 box(d,p['refs'],52,1261,976,36,21,GRAY)
 tx(d,'2026.10.21 자료 기준 · 합병 미확정 · 해석·전망은 본문에 구분',52,1301,20,GRAY)

def rows(d,items,top=570,left=340,gap=162):
 for j,(a,b) in enumerate(items):
  y=top+j*gap;d.line((52,y,1028,y),fill=LINE,width=2)
  box(d,a,52,y+27,left-80,95,35,RED,True)
  box(d,b,left,y+28,1028-left,110,33,INK)

def render(model,out,photo):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True);pages=[]
 for i in range(5):
  im,d=base(i)
  if i==0:
   im.paste(ImageOps.fit(Image.open(photo).convert('RGB'),(976,320),centering=(.5,.3)),(52,526));d=ImageDraw.Draw(im)
   tx(d,'자료사진: NASA / Keegan Barber · 2024.09.27',52,853,21,GRAY)
   d.rounded_rectangle((52,907,1028,1096),radius=16,fill=INK)
   box(d,'AI 칩·컴퓨터·인력을 함께 확보·배분해\n차·로봇·우주 사업을 키우려는 구상.',77,929,926,112,38,'white',True)
   tx(d,'공시·외부 분석을 종합한 편집 해석 / 직접 인용 아님',77,1058,21,'#b9c4cc')
  elif i==1:
   for x,title,sub in [(52,'테슬라','자율주행 · 로봇 AI'),(565,'스페이스X','AI 서비스 · 우주 연산 구상')]:
    d.line((x,563,x+463,563),fill=RED if x==52 else v.BLUE,width=5);tx(d,title,x,584,35,INK,True);box(d,sub,x,642,463,80,30,GRAY)
   v.down(d,540,719)
   d.rounded_rectangle((52,784,1028,914),radius=14,fill=INK)
   tx(d,'공통 병목: 칩 생산 · 연산 인프라 · 전력',77,823,37,'white',True)
   tx(d,'대응 구상 → 공동 칩 프로젝트 Terafab',52,960,37,RED,True)
   box(d,'차·로봇용과 우주용은 서로 다른 칩 설계.\n외부 공급업체 조달도 계속할 계획이다.',52,1022,976,95,29,GRAY)
  elif i==2:
   tx(d,'지상 전력 제약을 넘으려는 회사의 구상',52,524,29,GRAY)
   rows(d,[('우주 태양광','궤도에서 AI를 돌릴 전력 확보'),('재사용 로켓','AI 위성과 설비를 우주로 운송'),('위성 운영 기술','기존 경험을 궤도 연산망에 활용')],top=593,left=365,gap=150)
   box(d,'궤도 AI의 비용·냉각·운영 경제성은 검증 과제.',52,1074,976,46,27,GRAY)
  elif i==3:
   tx(d,'이미 있는 기술 협력에 더해 기대하는 변화',52,526,29,GRAY)
   rows(d,[('지금: 별도 회사','인력·예산을 각 회사가 관리하고\n회사 간 거래와 자원 이전을 조율'),('합병 시: 내부 배분','AI 프로젝트에 필요한 인력·투자를\n더 유연하게 옮겨 쓸 가능성')],top=594,left=371,gap=214)
   box(d,'Morningstar의 분석을 압축한 설명.\n합병이 실제 개발 속도·이익을 높일지는 미검증.',52,1041,976,83,27,GRAY)
  else:
   tx(d,'예상 효과',52,532,28,GRAY,True);tx(d,'성립하려면 확인할 것',390,532,28,GRAY,True)
   rows(d,[('AI 개발 효율','칩 공급·개발 속도·원가가\n실제로 개선되는가'),('공급망 투자','공장·설비의 실제 발주와\n투자 집행으로 이어지는가'),('주주의 몫','교환비율·투자 부담에 비해\n통합 사업의 이익이 커지는가')],top=586,left=390,gap=151)
   box(d,'확정 수혜·절감액은 아직 없다.\n좋은 구상과 주주에게 유리한 거래는 따로 확인한다.',52,1050,976,77,27,GRAY)
  tail(d,i);im.save(out/f'{i+1:02}.jpg',quality=95,optimize=True);pages.append(im)
 sheet=Image.new('RGB',(1680,1440),'#dedbd6')
 for i,im in enumerate(pages):sheet.paste(im.resize((540,675)),(10+(i%3)*560,10+(i//3)*715))
 d=ImageDraw.Draw(sheet);tx(d,'읽는 순서',1140,844,40,INK,True)
 for j,s in enumerate(['구상 → 공통 병목','우주 인프라 → 합병 논리','경제효과와 확인 조건']):tx(d,s,1140,940+j*70,29,INK)
 sheet.save(out/'preview.jpg',quality=95)
if __name__=='__main__':render(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2],sys.argv[3])
