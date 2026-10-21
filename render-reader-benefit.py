"""Render a precise reader-benefit review card from verified source facts; no publishing."""
import json,pathlib,sys,importlib.util
from PIL import Image,ImageDraw,ImageFont
spec=importlib.util.spec_from_file_location('report',pathlib.Path(__file__).with_name('render-report-v2.py'));r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def render(data,out):
 im=Image.new('RGB',(1080,1350),'#fafaf8');d=ImageDraw.Draw(im)
 def text(s,x,y,w,h,n=32,c=r.INK,b=False):r.text(d,s,x,y,w,h,n,c,b)
 d.rectangle((52,35,190,72),fill='#cc1722');text('BREAK',63,36,120,40,26,'white',True)
 text('BRIEFING',52,78,500,76,51,r.INK,True);d.line((52,150,1028,150),fill='#cc1722',width=3)
 text(data['headline'],52,180,976,182,66,r.INK,True)
 text(data['context'],52,366,976,54,29,r.GRAY)
 r.panel(d,(52,443,1028,601),'#f1f2f2')
 text('현재 월 9,900원 × 12개월',76,461,928,47,32,r.GRAY,True)
 text('연 118,800원',76,511,928,80,57,'#c31c2b',True)
 text('내비·업데이트 때문에 구독했다면?',52,633,976,56,39,r.INK,True)
 for j,s in enumerate(['기본 내비·교통 반영 경로: 스탠더드에 포함','무선 업데이트: 프리미엄 가입 없이도 지원','FSD 작동 방식: 프리미엄 구독 여부와 무관']):
  text(s,70,705+j*60,940,52,32,r.INK,j==0)
 text('해지 전 확인',52,912,976,40,29,'#c31c2b',True)
 text('스탠더드 유효 기간·무료 프리미엄 대상 여부 확인\n위성 지도·교통 시각화·셀룰러 스트리밍 등 유료 기능 차이 확인',52,961,976,86,28,r.GRAY)
 r.panel(d,(52,1080,1028,1229),'#e5eef3')
 text('앱 → 업그레이드 → 관리 → 구독 확인',76,1097,928,58,36,r.INK,True)
 text('필요 기능이 기본 제공된다면 유료 구독을 다시 판단하자.',76,1161,928,48,28,r.INK)
 text('현재 요금으로 12개월 유료 이용할 때의 금액. 전원 절약 보장 아님.',52,1250,976,37,23,r.GRAY)
 text('근거: Tesla 한국 공식 커넥티비티 지원 · 2026.10.21 확인',52,1300,976,34,22,r.GRAY)
 p=pathlib.Path(out);p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
if __name__=='__main__':render(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2])
