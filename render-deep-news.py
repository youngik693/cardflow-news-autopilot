"""Evidence-led research edition, six distinct pages. No publishing side effects."""
import json,sys,pathlib,os,math
from PIL import Image,ImageDraw,ImageFont,ImageOps
W,H=1080,1350
INK='#101820';PAPER='#f6f3ed';RED='#e64b3c';GOLD='#ffc94a';BLUE='#285cde';GRAY='#66717a';LINE='#d6d9db';GREEN='#148166'
REG=os.environ.get('CARDFLOW_FONT','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');BOLD=os.environ.get('CARDFLOW_BOLD_FONT',REG.replace('Regular','Bold'))
def font(n,b=False):return ImageFont.truetype(BOLD if b else REG,n,index=1)
def tx(d,s,x,y,n=32,c=INK,b=False):d.text((x,y),s,font=font(n,b),fill=c)
def lines(s,n,width,b=False):
 f=font(n,b);out=[]
 for p in s.split('\n'):
  cur=''
  for ch in p:
   if f.getlength(cur+ch)>width and cur:out.append(cur);cur=''
   cur+=ch
  out.append(cur)
 return out

def box(d,s,x,y,w,h,n=40,c=INK,b=False,sp=1.28):
 original=n
 while n>=original-12:
  ls=lines(s,n,w,b)
  if len(ls)*n*sp<=h:break
  n-=2
 else:raise ValueError('TEXT_OVERFLOW:'+s)
 for l in ls:tx(d,l,x,y,n,c,b);y+=n*sp
 return y

def base(page,dark=False):
 im=Image.new('RGB',(W,H),INK if dark else PAPER);d=ImageDraw.Draw(im);fg='white' if dark else INK
 tx(d,'카드플로우',52,26,33,fg,True);tx(d,'사건 · 이유 · 돈의 흐름',275,34,23,'#aebac5' if dark else GRAY);tx(d,f'{page:02} / 06',919,35,22,fg)
 d.line((52,98,1028,98),fill='#48545e' if dark else LINE,width=2)
 return im,d

def footer(d,refs,dark=False,note='2026.10.21 자료 기준 · 합병 미확정'):
 c='#b9c4cc' if dark else GRAY;d.line((52,1240,1028,1240),fill='#48545e' if dark else LINE,width=1)
 tx(d,refs,52,1260,20,c);tx(d,note,52,1295,20,c)
def eyebrow(d,s,dark=False):tx(d,s,52,139,25,GOLD if dark else RED,True)
def down(d,x,y,c=RED):d.line((x,y,x,y+37),fill=c,width=4);d.polygon([(x,y+48),(x-10,y+34),(x+10,y+34)],fill=c)

def cover(m,photo):
 im,d=base(1,True);im.paste(ImageOps.fit(photo,(1080,660),Image.Resampling.LANCZOS,centering=(.5,.28)),(0,108));d=ImageDraw.Draw(im)
 d.rectangle((52,141,297,192),fill=GOLD);tx(d,'합병 검토 · 배경 해설',65,147,24,INK,True)
 d.rectangle((0,692,1080,790),fill=INK);tx(d,'자료사진 2024.09.27 · NASA / Keegan Barber',52,718,22,'#c3ced6')
 box(d,'테슬라·스페이스X\n왜 합치려 하나',52,802,976,215,79,'white',True)
 d.rectangle((52,1048,1028,1206),fill=GOLD)
 box(d,'AI 칩·컴퓨터·인력을 함께 배분해\n차·로봇·우주 사업을 키우려는 구상',77,1070,926,110,39,INK,True)
 footer(d,'핵심 문장은 자료 종합 해석 · 직접 인용 아님',True);return im

def reason(m):
 im,d=base(2);eyebrow(d,'이유 ①  공통으로 막히는 곳')
 box(d,'로봇도, 우주 AI도\n더 많은 ‘두뇌’가 필요하다',52,207,976,185,62,INK,True)
 # Demands converge into a common bottleneck, then a documented project plan.
 for x,title,sub in [(52,'테슬라','자율주행 · 로봇'),(565,'스페이스X','AI 서비스 · 우주 연산 구상')]:
  d.line((x,450,x+463,450),fill=RED if x==52 else BLUE,width=6);tx(d,title,x,475,35,INK,True);box(d,sub,x,532,463,100,31,GRAY)
 down(d,540,610)
 d.rectangle((52,690,1028,874),fill=INK);tx(d,'회사 측이 지목한 병목',80,711,25,GOLD,True)
 tx(d,'칩 생산  ·  연산 인프라  ·  전력',80,774,42,'white',True)
 down(d,540,894)
 tx(d,'이미 추진 중인 공동 칩 공장',52,969,29,GRAY)
 tx(d,'Terafab',52,1021,67,RED,True)
 box(d,'테슬라 차·로봇용 칩 + 스페이스X 우주용 칩',52,1121,976,65,33)
 footer(d,'근거 S2 회사 공시 · S3 Terafab 공식 설명');return im

def why_now(m):
 im,d=base(3);eyebrow(d,'배경  자동차 회사가 왜 우주와 연결되나')
 box(d,'AI가 커질수록 필요한 전력,\n우주에서도 찾겠다는 구상',52,207,976,190,61,INK,True)
 tx(d,'스페이스X가 공시에 제시한 연결 고리',52,455,29,GRAY)
 rows=[('우주 태양광','궤도에서 AI를 돌릴 전력 확보'),('재사용 로켓','AI 위성과 설비를 우주로 운송'),('위성 운영 기술','기존 경험을 궤도 연산망에 활용')]
 for j,(a,b) in enumerate(rows):
  yy=545+j*160;d.line((52,yy,1028,yy),fill=LINE,width=2)
  tx(d,a,52,yy+34,36,RED,True);box(d,b,365,yy+35,663,100,33)
 d.rectangle((52,1080,1028,1206),fill=INK)
 box(d,'차·로봇용 AI와 우주 AI 인프라를\n칩·인력·투자 전략 하나로 묶으려는 논리.',77,1100,926,90,32,'white',True)
 footer(d,'근거 S2 회사 공시 · 궤도 AI의 경제성은 검증 과제');return im

def merger(m):
 im,d=base(4,True);eyebrow(d,'이유 ②  이미 협업하는데, 왜 합병까지?',True)
 box(d,'인력과 투자금을\n한 회사 안에서 조정',52,207,976,200,68,'white',True)
 tx(d,'합병의 추가 논리 · Morningstar 분석',52,452,28,'#b9c4cc')
 # A compact before/after table expresses the governance issue without claiming legal duties disappear.
 d.line((52,536,1028,536),fill='#57616a',width=2)
 tx(d,'현재: 서로 다른 회사',52,569,35,'white',True)
 box(d,'회사별 인력·예산을 두고\n거래와 자원 이동을 조율',52,636,976,130,40,'#c3ced6')
 d.line((52,817,1028,817),fill='#57616a',width=2)
 tx(d,'합병 시: 하나의 법인',52,851,35,GOLD,True)
 box(d,'AI 프로젝트에 필요한 인력·투자를\n내부에서 더 유연하게 배분할 가능성',52,919,976,145,40,'white')
 box(d,'편집 해석: 기술 협력에 더해, 자원을 나눠 쓰는 마찰을 줄이려는 논리.',52,1134,976,85,25,'#b9c4cc')
 footer(d,'근거 S4 Morningstar 2026.06.09 · 실현 효과는 미검증',True);return im

def effects(m):
 im,d=base(5);eyebrow(d,'파급효과  이 구상이 실행된다면')
 box(d,'기대 효과와 확인 조건을\n함께 봐야 한다',52,207,976,190,62,INK,True)
 # Conditional scenarios, not measured merger benefits or security recommendations.
 tx(d,'기대되는 변화',52,468,29,GRAY,True);tx(d,'실제로 확인할 것',607,468,29,GRAY,True)
 rows=[('AI 개발·운영 효율','칩 공급·원가가 개선되는가'),('설비·공급망 투자 수요','실제 발주·투자가 집행되는가'),('주주의 통합 사업 참여','기업가치·교환비율은 공정한가')]
 for j,(a,b) in enumerate(rows):
  yy=545+j*178;d.line((52,yy,1028,yy),fill=LINE,width=2);tx(d,f'0{j+1}',52,yy+29,25,RED,True)
  box(d,a,114,yy+26,440,110,35,INK,True);box(d,b,607,yy+27,421,115,32)
 d.rectangle((52,1100,1028,1206),fill=INK);box(d,'개발 속도·원가 개선은 목표.\n합병만으로 이익이 늘어난다는 수치는 아직 없다.',77,1115,926,82,28,'white')
 footer(d,'S2·S4 기반의 조건부 시나리오 · 특정 종목 수혜 확정 아님');return im

def risks(m):
 im,d=base(6);eyebrow(d,'독자가 가져갈 판단 기준')
 box(d,'주주 몫을 가르는 건\n합병 조건과 실행력',52,207,976,190,63,INK,True)
 tx(d,'196억 달러',52,452,89,RED,True)
 tx(d,'스페이스X 3분기 설비투자 · 합병 비용이 아님',52,588,26,GRAY)
 d.line((52,676,1028,676),fill=LINE,width=2)
 items=[('교환비율','통합 회사에서 내 지분은 얼마나 남나'),('투자 부담','큰 설비투자가 실제 수익으로 이어지나'),('양산 일정','Terafab 2028년 목표를 달성할 수 있나')]
 for j,(a,b) in enumerate(items):
  yy=719+j*130;tx(d,a,52,yy,33,INK,True);box(d,b,280,yy+2,748,90,30)
 d.rectangle((0,1126,1080,1232),fill=INK);tx(d,'사건 → 이유 → 돈의 흐름',52,1141,32,'white',True);tx(d,'근거까지 읽는 뉴스 · 카드플로우',52,1190,23,GOLD)
 footer(d,'S1 경영진 목표 · S2 지연·실패 위험 · 합병 조건 미합의');return im

def render(m,out,photo_path):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True);photo=Image.open(photo_path).convert('RGB')
 pages=[cover(m,photo),reason(m),why_now(m),merger(m),effects(m),risks(m)]
 for i,im in enumerate(pages):im.save(out/f'{i+1:02}.jpg','JPEG',quality=95,optimize=True)
 sheet=Image.new('RGB',(1680,1440),'#dedbd6')
 for i,im in enumerate(pages):sheet.paste(im.resize((540,675)),(10+(i%3)*560,10+(i//3)*715))
 sheet.save(out/'preview.jpg','JPEG',quality=95)
 return [str(out/f'{i+1:02}.jpg') for i in range(len(pages))]
if __name__=='__main__':print(json.dumps(render(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2],sys.argv[3])))
