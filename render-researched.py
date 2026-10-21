"""Render structured research using existing Pillow text layout. Private drafts only."""
import sys,json,pathlib
from PIL import Image,ImageDraw
from render import block,font
PAPER='#f5f2ec';INK='#10151c';RED='#dc201e';IVORY='#eae2d4';SKY='#a6d9f4'
def render(model,out):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
 draft=model['draft'];claims={c['id']:c for c in draft['claims']};paths=[];audit=[]
 for i,card in enumerate(draft['cards']):
  im=Image.new('RGB',(1080,1350),PAPER);d=ImageDraw.Draw(im)
  d.rectangle((54,35,310,90),fill=RED);d.text((68,38),'BREAK',font=font(33),fill='white')
  d.text((332,42),'BRIEFING',font=font(29),fill=INK)
  d.text((54,113),'비공개 검토본 · 발행 미승인',font=font(24),fill=RED)
  d.rounded_rectangle((54,182,1026,405),radius=20,fill=IVORY)
  block(d,card['question'],78,205,920,175,57,INK,minsize=44)
  rows=[claims[k]['text'] for k in card['claimIds']]
  if len(rows)>3:raise RuntimeError('TOO_MANY_CLAIMS_FOR_MOBILE')
  for j,text in enumerate(rows):
   y=462+j*175
   d.text((54,y),f'0{j+1}',font=font(30),fill=RED)
   block(d,text,135,y,880,145,37,INK,minsize=32)
   if j<len(rows)-1:d.line((135,y+156,1026,y+156),fill='#d5d1c9',width=2)
  d.rounded_rectangle((54,1020,1026,1200),radius=20,fill=SKY)
  block(d,card['conclusion'],78,1040,920,140,39,INK,minsize=34)
  block(d,model['sourceLabel'],54,1227,972,89,23,INK,minsize=20)
  path=out/f'{i+1:02}.jpg';im.save(path,quality=95);paths.append(str(path))
  audit.append({'page':i+1,'visibleText':[card['question'],*rows,card['conclusion'],model['sourceLabel']],'dimensions':[1080,1350],'status':'layout_only_not_fact_verified'})
 (out/'render-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
 return paths
if __name__=='__main__':print(json.dumps(render(json.loads(pathlib.Path(sys.argv[1]).read_text()),sys.argv[2])))
