"""Data-driven researched report renderer; creates review assets, never posts."""
import json,sys,pathlib,importlib.util
from PIL import Image,ImageDraw,ImageOps
spec=importlib.util.spec_from_file_location('visual',pathlib.Path(__file__).with_name('render-connected-news.py'));v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
W,H=1080,1350
INK,PAPER,GRAY,LINE,SKY,IVORY,BLUE,RED=v.INK,v.PAPER,v.GRAY,v.LINE,v.SKY,v.IVORY,v.BLUE,v.RED
tx,box,panel,arrow=v.tx,v.box,v.panel,v.arrow

def header(m,page):
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 if page==2:
  if m.get('brand')=='BREAK BRIEFING':
   d.rectangle((52,12,131,35),fill='#c91925');tx(d,'BREAK',59,12,16,'white',True)
   tx(d,'BRIEFING',52,37,30,INK,True);d.line((52,79,267,79),fill='#c91925',width=2)
  else:tx(d,m.get('brand','뉴스 분석'),52,23,35,'#c5352c',True)
  tx(d,m['context']+' / '+m['asOf'],340,33,21,GRAY)
 else:tx(d,m['context']+' / '+m['asOf']+' 기준',52,29,24,GRAY)
 tx(d,f'{page:02}/07',941,30,23)
 return im,d

def cover(m,photo):
 im,d=header(m,1);im.paste(ImageOps.fit(photo,(1080,695),centering=(.5,.45)),(0,109));d=ImageDraw.Draw(im)
 d.rectangle((0,804,1080,1350),fill=INK)
 tx(d,'바르셀로나항 자료사진(2016년) · Igor Ovsyannykov / CC0',64,815,20,'#b9c4cc')
 tx(d,m['cover']['label'],64,870,30,SKY,True)
 box(d,m['cover']['headline'],64,931,952,207,72,'white',True)
 box(d,m['cover']['sub'],64,1155,952,100,35,IVORY)
 tx(d,'바쁘다면 마지막 장 핵심 요약 →',64,1280,26,SKY,True)
 return im

def start(m,page,p):
 im,d=header(m,page)
 for j,s in enumerate(m['steps']):
  x=52+j*202;panel(d,(x,94,x+161,147),INK if page-2==j else '#e7e4dd');tx(d,s,x+16,104,25,'white' if page-2==j else GRAY,page-2==j)
  if j<4:arrow(d,x+167,120,length=29)
 v.bubble(d,179,222,IVORY,'이번 장의 질문',p['question'],INK)
 box(d,p['deck'],52,439,976,76,30,GRAY)
 return im,d

def body(d,p,m):
 kind=p['type'];rows=p['rows']
 if kind=='compare':
  for j,(label,n,desc) in enumerate(rows):
   x=52+j*513;panel(d,(x,535,x+463,891),'white',LINE);tx(d,label,x+23,554,31,GRAY,True);tx(d,n,x+23,630,76,RED if j==0 else BLUE,True);box(d,desc,x+23,769,417,88,30)
  box(d,p['note'],52,925,976,126,28,GRAY)
 elif kind=='share':
  pct=m['numbers']['chipSharePct'];tx(d,f'약 {pct:.0f}%',52,528,125,BLUE,True);tx(d,'전체 수출에서 반도체가 차지하는 비중',52,709,31,GRAY)
  x=52;y=783;w=976;cut=round(w*pct/100);d.rectangle((x,y,x+w,y+51),fill='#dde3e6');d.rectangle((x,y,x+cut,y+51),fill=BLUE)
  tx(d,'반도체 275억 달러',52,864,34,BLUE,True);tx(d,'전체 616억 달러',580,864,34,INK,True);box(d,p['note'],52,970,976,93,27,GRAY)
 elif kind=='chain':
  for j,(title,meaning) in enumerate(rows):
   y=531+j*156;panel(d,(52,y,1028,y+116),'white',LINE);tx(d,f'0{j+1}',76,y+13,28,BLUE,True);tx(d,title,149,y+10,35,INK,True);box(d,meaning,149,y+65,850,48,28,GRAY)
   if j<2:
    d.line((540,y+118,540,y+140),fill=BLUE,width=3);d.polygon([(540,y+150),(533,y+139),(547,y+139)],fill=BLUE)
  box(d,p['note'],52,1018,976,59,23,GRAY)
 elif kind=='evidence':
  tx(d,'최대 약 4%',52,520,111,BLUE,True);tx(d,'수혜지역 소비 / 비교지역 대비',52,677,31,GRAY)
  for j,(a,b) in enumerate(rows):
   y=748+j*103;d.line((52,y,1028,y),fill=LINE,width=2);tx(d,a,52,y+14,32,INK,True);box(d,b,420,y+17,608,64,29,GRAY)
  box(d,p['note'],52,974,976,99,25,GRAY)
 else:
  for j,(a,b) in enumerate(rows):
   y=535+j*144;panel(d,(52,y,1028,y+124),'white',LINE);box(d,a,76,y+24,230,80,31,BLUE,True);box(d,b,340,y+27,655,85,33,INK,True)
  box(d,p['note'],52,989,976,86,24,GRAY)

def end(d,p,m):
 v.bubble(d,1080,155,SKY,'한 줄 결론',p['answer'],INK)
 tx(d,p['next'],52,1263,23,INK,True);tx(d,'근거: '+p['refs'],52,1305,20,GRAY)

def summary(m):
 im,d=header(m,7);d.line((52,103,1028,103),fill=LINE,width=2);tx(d,'다섯 장을 한눈에',52,141,28,BLUE,True)
 box(d,'수출 호황이 내 살림까지,\n핵심은 이 다섯 가지',52,190,976,166,59,INK,True)
 for j,(q,a) in enumerate(m['summary']):
  y=400+j*122;tx(d,f'0{j+1}',52,y+12,28,BLUE,True);tx(d,q,115,y+5,31,GRAY,True);box(d,a,115,y+51,913,61,34,INK,True);d.line((115,y+117,1028,y+117),fill=LINE,width=1)
 panel(d,(52,1056,1028,1215),SKY);tx(d,'그래서 무엇을 봐야 하나',77,1072,25,INK,True);box(d,m['summaryAnswer'],77,1116,926,88,34,INK,True)
 tx(d,'2026.10.21 잠정 수치 · 지역 연구의 추정과 전국 효과를 구분',52,1246,22,GRAY)
 tx(d,'근거: 관세청 10.21 · 한국은행 BOK 이슈노트 08.31',52,1288,22,GRAY)
 return im

def render(m,out,photo):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True);photo=Image.open(photo).convert('RGB');pages=[cover(m,photo)]
 for i,p in enumerate(m['slides']):
  im,d=start(m,i+2,p);body(d,p,m);end(d,p,m);pages.append(im)
 pages.append(summary(m));assert len(pages)==7
 for i,im in enumerate(pages):im.save(out/f'{i+1:02}.png');im.save(out/f'{i+1:02}.jpg',quality=95,optimize=True)
 sheet=Image.new('RGB',(1680,1400),'#dedbd6')
 for i,im in enumerate(pages[:6]):sheet.paste(im.resize((540,675)),(10+(i%3)*560,10+(i//3)*700))
 sheet.save(out/'preview-6.png')
if __name__=='__main__':render(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2],sys.argv[3])
