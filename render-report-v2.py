"""Audience-question report layout. Local review assets only; never publishes."""
import json,sys,pathlib,importlib.util
from PIL import Image,ImageDraw,ImageOps
spec=importlib.util.spec_from_file_location('report',pathlib.Path(__file__).with_name('render-report.py'));r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
v=r.v
INK,PAPER,GRAY,LINE,SKY,IVORY,BLUE,RED=r.INK,r.PAPER,r.GRAY,r.LINE,r.SKY,r.IVORY,r.BLUE,r.RED
tx,box,panel=r.tx,r.box,r.panel
TEXT_AUDIT=[]
def text(d,s,x,y,w,h,n=34,c=INK,b=False):
 # Unlike the legacy renderer, body text never silently shrinks.
 ls=v.v.lines(s,n,w,b)
 if len(ls)*n*1.25>h:raise ValueError('TEXT_OVERFLOW: '+s)
 TEXT_AUDIT.append({'text':s,'size':n,'lines':len(ls),'bounds':[x,y,w,h]})
 for line in ls:tx(d,line,x,y,n,c,b);y+=n*1.25
def bubble(d,y,h,fill,label,s):
 panel(d,(52,y,1028,y+h),fill);tx(d,label,78,y+15,25,INK,True)
 text(d,s,78,y+56,924,h-64,51 if label=='이번 장의 질문' else 43,INK,True)
def start(m,page,p):
 im,d=r.header(m,page)
 for j,s in enumerate(m['steps']):
  x=52+j*202;panel(d,(x,94,x+161,147),INK if page-2==j else '#e7e4dd');tx(d,s,x+16,104,25,'white' if page-2==j else GRAY,page-2==j)
  if j<4:r.arrow(d,x+167,120,length=29)
 bubble(d,177,210,IVORY,'이번 장의 질문',p['question'])
 text(d,p['deck'],52,413,976,85,31,GRAY)
 return im,d
def tag(d,s,x,y,w=210):
 panel(d,(x,y,x+w,y+49),'#e5eef3');tx(d,s,x+15,y+5,28,BLUE,True)
def market(d,p):
 for j,a in enumerate(p['metrics']):
  x=52+j*500;panel(d,(x,516,x+476,744),'white',LINE)
  text(d,a[0],x+23,531,430,55,39,BLUE,True)
  text(d,a[1],x+23,588,430,95,71,INK,True)
  text(d,a[2],x+23,685,430,45,29,GRAY)
 text(d,p['comparisonTitle'],52,767,976,47,31,INK,True)
 for j,row in enumerate(p['countries']):
  x=52+j*331;panel(d,(x,823,x+313,930),IVORY if j==1 else '#eeece7')
  text(d,row[0],x+14,832,286,46,34,BLUE if j==1 else INK,True)
  text(d,row[1],x+14,881,286,40,28,GRAY)
 text(d,p['note'],52,948,976,71,25,GRAY)
def outlook(d,p):
 for j,(year,verdict,evidence,meaning) in enumerate(p['yearOutlooks']):
  y=516+j*183;panel(d,(52,y,1028,y+166),'white',LINE)
  tag(d,year,74,y+17,132);text(d,verdict,230,y+16,772,58,43,BLUE,True)
  text(d,evidence,74,y+78,925,43,31,INK,True)
  text(d,meaning,74,y+121,925,36,26,GRAY)
 panel(d,(52,886,1028,966),'#e5eef3')
 text(d,p['risk'],74,894,931,74,29,INK,True)
 text(d,p['note'],52,981,976,41,25,GRAY)
def household(d,p):
 for j,(label,num,desc) in enumerate(p['metrics']):
  x=52+j*331;panel(d,(x,516,x+313,722),'white',LINE)
  text(d,label,x+16,532,281,48,33,INK,True)
  text(d,num,x+16,582,281,80,59,BLUE if j<2 else RED,True)
  text(d,desc,x+16,667,281,42,26,GRAY)
 for j,(label,body) in enumerate(p['contextBoxes']):
  y=743+j*94;panel(d,(52,y,1028,y+82),'#e5eef3' if j==1 else '#eeece7')
  text(d,label,72,y+7,936,32,25,BLUE,True)
  text(d,body,72,y+40,936,39,29,INK,True)
def region(d,p):
 text(d,'수혜지역',52,512,450,58,42,BLUE,True)
 text(d,'비교지역',579,512,449,58,42,INK,True)
 panel(d,(52,581,512,774),'#e5eef3');panel(d,(552,581,1028,774),'white',LINE)
 text(d,'이천 · 화성\n청주 등',75,601,414,134,49,INK,True)
 text(d,'반도체 종사자\n거주 비중이 낮은 곳',575,606,430,124,35,GRAY,True)
 text(d,'수혜지역 소비  최대 약 4%↑',52,801,976,83,51,BLUE,True)
 text(d,'비교지역 대비 · 성과급 지급 후 효과 추정',52,884,976,48,30,GRAY)
 text(d,p['note'],52,949,976,76,26,GRAY)
def policy(d,p):
 for j,pb in enumerate(p['benefitBoxes']):
  y=510+j*258;panel(d,(52,y,1028,y+244),'white',LINE)
  text(d,pb['title'],74,y+12,931,44,31,BLUE,True)
  text(d,pb['benefit'],74,y+61,931,58,41,INK,True)
  text(d,pb['detail'],74,y+125,931,73,28,INK)
  text(d,pb['action'],74,y+201,931,40,27,RED if j==0 else GRAY,True)
def end(d,p):
 bubble(d,1039,203,SKY,'한 줄 결론',p['answer'])
 text(d,p['next'],52,1254,976,38,23,INK,True)
 text(d,'근거: '+p['refs'],52,1300,976,36,20,GRAY)
def cover(m,photo):
 im,d=r.header(m,1);im.paste(ImageOps.fit(photo,(1080,672),centering=(.5,.45)),(0,105));d=ImageDraw.Draw(im)
 d.rectangle((0,777,1080,1350),fill=INK)
 tx(d,'바르셀로나항 자료사진(2016) · Igor Ovsyannykov / CC0',52,788,20,'#c6cfd5')
 text(d,m['cover']['label'],52,838,976,95,35,SKY,True)
 text(d,m['cover']['headline'],52,947,976,192,74,'white',True)
 text(d,m['cover']['sub'],52,1150,976,113,31,IVORY)
 tx(d,'반도체 전망 → 내 살림 → 확정 혜택   /   핵심 요약은 마지막 장',52,1293,25,SKY,True)
 return im
def summary(m):
 im,d=r.header(m,7)
 tx(d,'저장해 두는 핵심 요약',52,132,30,BLUE,True)
 text(d,'수출 호황,\n누구의 지갑이 두꺼워질까?',52,192,976,163,57,INK,True)
 for j,(q,a) in enumerate(m['summary']):
  y=390+j*121;tx(d,f'0{j+1}',52,y+7,29,BLUE,True)
  tx(d,q,121,y,32,GRAY,True);text(d,a,121,y+49,907,70,34,INK,True)
  d.line((121,y+114,1028,y+114),fill=LINE,width=1)
 bubble(d,1039,203,SKY,'오늘의 판단',m['summaryAnswer'])
 tx(d,'오늘 집계·과거 연구·향후 전망은 서로 다른 기간의 자료입니다.',52,1260,23,GRAY)
 tx(d,'근거: 관세청·산업부·TrendForce·Micron·한국은행·국가데이터처·금융위',52,1305,20,GRAY)
 return im
def render(m,out,photo):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True);photo=Image.open(photo).convert('RGB')
 pages=[cover(m,photo)]
 for i,p in enumerate(m['slides']):
  im,d=start(m,i+2,p)
  {'market':market,'outlook':outlook,'household':household,'region':region,'policy':policy}[p['type']](d,p)
  end(d,p);pages.append(im)
 pages.append(summary(m));assert len(pages)==7
 for i,im in enumerate(pages):
  im.save(out/f'{i+1:02}.png');im.save(out/f'{i+1:02}.jpg',quality=95,optimize=True)
 sheet=Image.new('RGB',(1680,1400),'#dedbd6')
 for i,im in enumerate(pages[:6]):sheet.paste(im.resize((540,675)),(10+(i%3)*560,10+(i//3)*700))
 sheet.save(out/'preview-6.png')
 mobile=Image.new('RGB',(1170,976),'#dedbd6')
 for i,im in enumerate(pages[1:]):mobile.paste(im.resize((390,488)),((i%3)*390,(i//3)*488))
 mobile.save(out/'mobile-check.png')
 (out/'text-layout-audit.json').write_text(json.dumps(TEXT_AUDIT,ensure_ascii=False,indent=2))
if __name__=='__main__':render(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2],sys.argv[3])
