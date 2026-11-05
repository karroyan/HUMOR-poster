"""New HUMOR poster design, independently composed from source-paper claims.
Uses the Paper2Poster repository skill and configuration loader, with offline exports.
"""
from pathlib import Path
import json,io,base64,html,re,xml.etree.ElementTree as ET,importlib.util,os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties,fontManager
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.mathtext import math_to_image
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'assets'; W,H=1400,900
spec=importlib.util.spec_from_file_location('p2p_config',Path(__file__).with_name('config_utils.py'));cfgmod=importlib.util.module_from_spec(spec);spec.loader.exec_module(cfgmod)
os.chdir(ROOT);cfg=cfgmod.load_poster_yaml_config(str(ROOT/'source/paper.pdf'))
assert cfg['poster_width_cm']==140 and cfg['poster_height_cm']==90
for f in (ROOT/'fonts').glob('*.ttf'):fontManager.addfont(str(f))
plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none','image.composite_image':False})
INK='#162F3F';TEXT='#334B59';MUTE='#607786';TEAL='#007F79';BLUE='#2854A1';GOLD='#A36012';PALE='#EDF7F5';BG='#F5F8FA';LINE='#D4E1E7';WHITE='#FFFFFF'
nodes=[];panels=[];section='header';parent=None
rr=RendererAgg(10,10,72)
def measure(s,sz,b=False):return rr.get_text_width_height_descent(s,FontProperties(family='DejaVu Sans',size=sz,weight='bold' if b else 'normal'),False)[0]
def add(t,**kw):n=dict(type=t,section=section,parent=parent,**kw);nodes.append(n);return n
def rect(x,y,w,h,c,r=3,stroke=None):return add('rect',name='Background',x=x,y=y,w=w,h=h,fill=c,stroke=stroke,radius=r,strokeWidth=.45)
def text(x,y,s,sz=11,c=TEXT,b=False,align='left'):return add('text',name=s,x=x,y=y,text=s,size=sz,fill=c,weight='bold' if b else 'regular',align=align,italic=False)
def rule(x,y,x2,y2,c=LINE,sw=.5,dash=None):return add('line',name='Rule',x1=x,y1=y,x2=x2,y2=y2,stroke=c,strokeWidth=sw,dash=dash)
def para(x,y,w,s,sz=11,leading=15,c=TEXT,b=False):
 line=''
 for word in s.split():
  test=(line+' '+word).strip()
  if measure(test,sz,b)>w and line:text(x,y,line,sz,c,b);y+=leading;line=word
  else:line=test
 if line:text(x,y,line,sz,c,b)
 return y+leading

def pic(name,x,y,w):
 p=A/(name+'.png');im=Image.open(p);h=w*im.height/im.width
 add('image',name=name,x=x,y=y,w=w,h=h,data=base64.b64encode(p.read_bytes()).decode());return h

def math(x,y,w,h,s,sz=10):return add('math',name=s,x=x,y=y,w=w,h=h,expr=s,size=sz,fill=INK)
def panel(name,x,y,w,h,label,color=TEAL):
 global section,parent
 section=name;parent=name;panels.append(dict(name=name,x=x,y=y,w=w,h=h))
 rect(x,y,w,h,WHITE,5,LINE)
 sz=15
 while measure(label,sz,True)>w-34:sz-=.25
 text(x+17,y+28,label,sz,color,True);rule(x+17,y+40,x+w-17,y+40,color,.7)
def arrow(x,y,x2,y2,c=TEAL):
 rule(x,y,x2,y2,c,1.1)
 import math as m
 a=m.atan2(y2-y,x2-x)
 for d in [-.55,.55]:rule(x2,y2,x2-4*m.cos(a+d),y2-4*m.sin(a+d),c,1.1)
# Revision v6: oral presentation, essential labels only, larger tables and a compact rank plot.
def fbox(x,y,w,h,expr,size=10.4):
 rect(x,y,w,h,WHITE,3,'#C8D6E7');math(x+4,y+2,w-8,h-4,expr,size)
rect(0,0,W,H,BG,0);rect(0,0,W,6,TEAL,0)
text(25,35,'From Perception to Punchline:',26,INK,True)
text(25,66,'Empowering VLM with the Art of In-the-wild Memes',22,INK,True)
xx=25
for name,marks in [('Xueyan Li','*1'),('Yingyi Xue','*1,2'),('Mengjie Jiang','3'),('Qingzi Zhu','1'),('Yazhe Niu','†4')]:
 text(xx,86,name,10.6,INK,True);xx+=measure(name,10.6,True)+1
 text(xx,81,marks,7.3,INK,True);xx+=measure(marks,7.3,True)+13
text(25,100,'[1] Shanghai AI Laboratory   [2] Fudan University   [3] Columbia Engineering, Columbia University   [4] CUHK MMLab',8.7,MUTE)
text(1375,37,'HUMOR',32,TEAL,True,'right');text(1375,59,'NeurIPS 2026',10.8,INK,True,'right')
text(1375,77,'Hierarchical Understanding and Meme Optimization',8.6,TEAL,align='right')
rule(25,108,1375,108,TEAL,.8)
# 01: Fig.4 motivates within-group comparison, rather than an absolute per-image score.
panel('Task',25,119,270,334,'01  What makes a caption a meme?')
para(40,178,240,'Same visual relation, different context-specific punchlines.',10.5,13,c=INK,b=True)
text(94.5,205,'Template',10.2,INK,True,'center');text(223.5,205,'Meme',10.2,TEAL,True,'center')
pic('template',40,214,109);pic('apple-fans',169,214,109)
rect(40,303,240,30,PALE,3);text(50,315,'USER INPUT',8.8,TEAL,True);text(50,328,'Technology · “Apple fanatic”',10.1,TEAL,True)
for x,tag,value in [(40,'A · Subject','APPLE FANS'),(122,'B · New focus','IPHONE 11'),(204,'C · Neglected','IPHONE 10')]:
 rect(x,342,76,35,WHITE,3,'#BADAD6');text(x+38,355,tag,8.8,TEAL,True,'center');text(x+38,370,value,9.4,INK,True,'center')
text(40,398,'Why rank within a group?',10.7,TEAL,True)
para(40,415,240,'Single-image scores barely separate quality. In-group ranks make differences easier to compare.',10.1,12.6)
# 02: keep A/B/C; formulas have an explicit interpretation and a visible hand-off.
panel('Method',315,119,1060,334,'02  HUMOR: hierarchical reasoning → local preferences → stable optimization',BLUE)
for x,w,k,title in [(330,329,'A','Hierarchical CoT'),(680,329,'B','Template-local reward'),(1030,330,'C','Group-wise optimization')]:
 rect(x,167,w,273,'#F0F4FB' if k!='B' else PALE,4)
 rect(x+10,177,17,17,BLUE if k!='B' else TEAL,3);text(x+18.5,189,k,10,WHITE,True,'center')
 text(x+34,190,title,12,BLUE if k!='B' else TEAL,True)
arrow(662,286,677,286,BLUE);arrow(1012,286,1027,286,BLUE)
# A: match the reference's blue scenario selection, gold reverse anchor and inference strip.
text(341,210,'Template intent → diverse contextual groundings.',9.9,INK)
rect(341,222,222,13,BLUE,2);text(348,232,'1  MULTI-SCENARIO ASSOCIATION',8.9,WHITE,True)
pic('bean-template',341,241,44)
for yy,s in [(251,'A confusing work problem → bewildered reaction'),(271,'A bad joke → exaggerated "painful" response'),(291,'Social ignorance → refusing to listen')]:
 selected=yy==291
 rect(400,yy-13,245,19,'#DFEAF9' if selected else WHITE,2,BLUE if selected else LINE)
 text(409,yy,s,9.3,BLUE)
arrow(388,266,397,266,BLUE)
text(400,311,'Trace back to the compatible scene',9.1,GOLD)
arrow(628,317,628,299,GOLD)
rect(341,319,305,57,'#FFF2DA',3,'#E4CDA7');pic('bean-gold',345,323,30)
text(383,331,'2  REVERSE-ANCHOR FROM A REAL MEME',8.6,GOLD,True)
text(383,342,'Gold c → infer U: socializing / ignorance.',9.0,INK)
text(383,353,'Trace back; retain other associations.',9.0,INK)
rect(383,358,253,17,WHITE,2,'#D5C4A3')
math(387,359,245,15,r'$\tilde r=\arg\max_r P_\phi(c\mid r,I,U)$',9.0)
fbox(341,381,305,23,r'$\mathbb{E}_{r\sim P_\theta}[\tilde h_G(r)]\geq 1-(1-\alpha)\delta$',10.4)
text(341,418,'Good-path mass α > 0; mean humor gap ≤ δ.',9.2,MUTE)
rect(341,424,305,15,'#DFEAF9',2)
text(351,435,'INFERENCE  Explore/select; no gold caption.',9.2,BLUE,True)
# B: original vs a real boring construction from Fig.9. Three steps, no spurious "5".
text(691,210,'Compare within a template; learn a group ranking.',10.0,INK)
text(691,226,'Training pairs span five types: wrong text, wrong location,',9.0,TEXT)
text(691,238,'boring, detailed boring, and generated memes.',9.0,TEXT)
text(743,253,'Original',10.1,TEAL,True,'center');text(945,253,'Boring',10.1,MUTE,True,'center')
pic('pair-original',707,261,72);pic('pair-boring',909,261,72);text(844,292,'≻',16,TEAL,True,'center')
rect(691,316,305,43,WHITE,3,'#C8D6E7')
text(701,332,'Preference',9.1,BLUE,True);math(765,319,226,18,r'$p_{ij}^G=\sigma[s_\phi(m_i)-s_\phi(m_j)]$',10.0)
text(701,354,'BCE loss',9.1,BLUE,True);math(760,340,231,17,r'$\ell=-y\log p-(1-y)\log(1-p)$',9.5)
rect(691,364,305,27,WHITE,3,'#C8D6E7');text(701,384,'Expected wins',9.1,BLUE,True)
math(785,365,206,24,r'$\mathrm{EBC}_G(i)=\sum_{j\ne i}p_{ij}^G$',10.2)
text(691,404,'1  Estimate preferences inside template G.',9.7)
text(691,418,'2  Sum wins; normalize sparse comparisons.',9.7)
text(691,432,'3  Rank candidates → local policy targets.',9.7)
# C: prefer high-ranked captions but limit deviation from the CoT reference.
para(1041,210,307,'Use the group ranking as the policy target. Stay close to the CoT reference during optimization.',10.2,12.8)
for yy,s in [(250,'1  Sample captions from the CoT policy'),(276,'2  Pairwise reward → EBC → local targets'),(302,'3  Update policy; keep CoT as reference')]:
 rect(1041,yy-15,305,21,'#DDE8F7',2);text(1050,yy,s,9.8,INK)
rect(1041,317,305,55,WHITE,3,'#C8D6E7')
math(1045,320,297,23,r'$\mathcal{L}=-\mathbb{E}[\sum_k q_G(m_k)\log\pi_\theta(c_k\mid I)]+\beta\Delta_{\mathrm{KL}}$',9.6)
math(1045,346,297,22,r'$\Delta_{\mathrm{KL}}=\mathbb{E}_I[\mathrm{KL}(\pi_\theta\Vert\pi_{\mathrm{CoT}})]$',10)
fbox(1041,379,305,23,r'$H(\pi_\theta)\geq H(\pi_{\mathrm{CoT}})-\sqrt{\Delta_{\mathrm{KL}}/2}$',10.2)
para(1041,418,307,'For h ∈ [0,1], KL bounds possible degradation. It does not guarantee improvement.',9.5,12,c=MUTE)
# 03: table rows expanded vertically; retain only essential, legible score sources.
panel('Generation',25,465,810,266,'03  Does HUMOR improve meme quality and diversity?',TEAL)
t1=json.loads((ROOT/'source/table1.json').read_text());cols=[278,340,402,464,526,588,660]
rect(40,507,632,18,INK,2);text(46,521,'Model / variant',9,WHITE,True)
for xx,ss in zip(cols,['Hum. ↑','Read. ↑','Rel. ↑','Orig. ↑','Sim. ↑','Dist. ↑','Human % ↑']):text(xx,521,ss,8.4,WHITE,True,'right')
for i,row in enumerate(t1):
 yy=540+i*12.1+(4 if i>=5 else 0)+(4 if i>=7 else 0);own=row['model'].startswith('HUMOR');cc=GOLD if 'RL' in row['model'] else BLUE if own else TEXT
 if own:rect(40,yy-9.5,632,12.1,'#FFF0D3' if 'RL' in row['model'] else '#E1EBF8',0)
 if i in [5,7]:rule(40,yy-11.1,672,yy-11.1,TEAL,.65)
 text(46,yy,row['model'],8.9,cc,own)
 for j,(xx,val) in enumerate(zip(cols,row['values'])):
  best=val is not None and val==max(rr['values'][j] for rr in t1 if rr['values'][j] is not None)
  ss='—' if val is None else f'{val:.3f}' if j in [4,5] else f'{val:.1f}' if j==6 else f'{val:.2f}'
  text(xx,yy,ss,9.2,cc,best,'right')
 if i not in [4,6,11]:rule(40,yy+3.5,672,yy+3.5,LINE,.2)
rule(685,507,685,689,TEAL,.8);text(698,520,'CoT vs. 7B base',8.9,TEAL,True)
deltas=[('Humor','+0.29'),('Readability','+0.35'),('Relevance','+0.59'),('Originality','+0.33'),('Similarity','+0.064'),('Context swap','+0.026'),('Human Rate','+15.8 pp')]
for i,(title,value) in enumerate(deltas):
 yy=541+i*20.8;text(698,yy,title,8.6,MUTE);text(818,yy,value,10.5,TEAL,True,'right')
text(698,702,'RL preview: 2.83 humor',8.2,GOLD,True);text(698,718,'Orig. 2.90 → 2.79',8.4,GOLD)
text(40,695,'Human scores: 30 Prolific raters, 0–5. Human Rate: Gemini-2.5-pro.',9.0,MUTE)
text(40,710,'Sim.: bge-base-en-v1.5. Dist.: context-swapped generations. Bold = best.',9.0,MUTE)
# 05: larger tau rows and a concise evaluation source, no dense explanatory footnote.
panel('Reward',25,743,810,131,'05  Does the reward recover human preference rankings?',TEAL)
nodes[-2]['y']=765;nodes[-1]['y1']=774;nodes[-1]['y2']=774
t2=json.loads((ROOT/'source/table2.json').read_text());tx=[239,313,387,461,535]
text(40,788,'Reward backbone / state',8.7,INK,True)
for xx,j in zip(tx,range(1,6)):text(xx,788,f'G{j} · τ ↑',9.0,INK,True,'right')
for i,row in enumerate(t2):
 yy=802+i*10.8;own=i==5
 if own:rect(40,yy-8.8,501,10.8,PALE,0)
 if i in [2,4]:rule(40,yy-9.5,541,yy-9.5,LINE,.45)
 text(40,yy,row['model'],8.9,TEAL if own else TEXT,own)
 for xx,t,p in zip(tx,row['tau'],row['p']):
  stars='***' if row.get('p_display') else '**' if p<.01 else '*' if p<.05 else ''
  text(xx,yy,f'{t:.2f}{stars}',9.3,TEAL if own else TEXT,own,'right')
rule(557,787,557,858,LINE,.6)
para(571,799,245,'Human MaxDiff ranks vs. model pairwise + EBC ranks.',9.5,12.5,c=INK,b=True)
para(571,837,245,'Keye aligns best; Qwen gains are mixed or limited.',9.8,12.5,c=TEAL,b=True)
text(40,866,'100 MaxDiff raters · 5 templates · *p<.05, ***p<.001',8.8,MUTE)
# 04: two Fig.16 theme rows in the same card; identical three-column roles.
panel('Qualitative',855,465,520,248,'04  Meme generation across themes',BLUE)
nodes[-2]['y']=489;nodes[-1]['y1']=498;nodes[-1]['y2']=498
for x,title,cc in [(1002,'Human reference',INK),(1120,'Single-path CoT',BLUE),(1238,'HUMOR-CoT',TEAL)]:
 text(x+44.5,510,title,9.3,cc,True,'center')
text(872,541,'Christmas',10.7,BLUE,True)
text(872,559,'Love · humor',9.1,INK)
text(872,577,'Family tradition',9.1,INK)
text(872,595,'Delayed excitement',9.1,INK)
text(872,637,'Romance',10.7,BLUE,True)
text(872,655,'Happiness · humor',9.1,INK)
text(872,673,'Crush · dabbing',9.1,INK)
text(872,691,'Rare moment',9.1,INK)
for y,theme in [(518,'christmas'),(615,'romance')]:
 for x,suffix_name in [(1002,'reference'),(1120,'single'),(1238,'humor')]:
  pic(theme+'-'+suffix_name,x,y,89)
# 06: align the card with 04; retain a tall plot, seven colors and solid curves.
panel('Transfer',855,725,520,149,'06  Does HUMOR generalize to unseen templates?',TEAL)
transfer=json.loads((ROOT/'source/unseen-figure-data.json').read_text());series={s['model']:s['ranks'] for s in transfer['series']}
xp=[890+j*(340/7) for j in range(8)];yrank=lambda v:779+(v-1)*(66/6)
for v in range(1,8):
 yy=yrank(v);rule(885,yy,1234,yy,'#E0E8ED',.3);text(876,yy+2.5,str(v),8.3,MUTE,align='right')
styles={'Human':(BLUE,None,1.1),'HUMOR-CoT':(TEAL,None,1.2),'Qwen 32B':('#C17B0A',None,.8),'Keye':('#8855A2',None,.8),'InternVL':('#C54D72',None,.8),'Qwen 7B':('#8D5D2E',None,.8),'GLM':('#627686',None,.8)}
for name in ['GLM','Qwen 7B','InternVL','Keye','Qwen 32B','Human','HUMOR-CoT']:
 col,dash,sw=styles[name];vals=series[name]
 for j in range(7):rule(xp[j],yrank(vals[j]),xp[j+1],yrank(vals[j+1]),col,sw,dash)
 for xx,val in zip(xp,vals):rect(xx-.7,yrank(val)-.7,1.4,1.4,col,.7 if name=='HUMOR-CoT' else 0)
for xx,s in zip(xp,['Caption','Theme','Emotion','Humor','Punchline','Cultural','Context','Spread']):text(xx,858,s,7.8,MUTE,align='center')
for i,name in enumerate(['Human','HUMOR-CoT','Qwen 32B','Keye','InternVL','Qwen 7B','GLM']):
 col,dash,sw=styles[name];yy=782+i*11.8;rule(1250,yy-3,1264,yy-3,col,sw,dash);text(1269,yy,name,8.1,col,name in ['Human','HUMOR-CoT'])
text(870,867,'20 unseen templates · Gemini-2.5-pro mean rank ↓',8.8,TEAL,True)
# Oral-presentation version: minimal footer only; full limitations are in the speaking notes.
section='Footer';parent=None
rule(25,883,1375,883,TEAL,.7)
text(25,895,'HUMOR · NeurIPS 2026',9.5,TEAL,True);text(1375,895,'yingyixue7@gmail.com',10,TEAL,True,'right')

# Render all formats from the new scene.
fig=plt.figure(figsize=(W/25.4,H/25.4));ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off')
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="1400mm" height="900mm">']
css=''
for fn,weight in [('DejaVuSans.ttf',400),('DejaVuSans-Bold.ttf',700)]:
 css+=f'@font-face{{font-family:PosterSans;src:url(data:font/ttf;base64,{base64.b64encode((ROOT/"fonts"/fn).read_bytes()).decode()}) format("truetype");font-weight:{weight};}}'
svg.append(f'<defs><style>{css}</style></defs>');artists=[];formula_issues=[]
for i,n in enumerate(nodes):
 t=n['type']
 if t=='rect':
  ax.add_patch(FancyBboxPatch((n['x'],n['y']),n['w'],n['h'],boxstyle=f'round,pad=0,rounding_size={n["radius"]}',facecolor=n['fill'],edgecolor=n['stroke'] or 'none',lw=n['strokeWidth']*72/25.4,zorder=1))
  svg.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="{n["radius"]}" fill="{n["fill"]}" stroke="{n["stroke"] or "none"}" stroke-width="{n["strokeWidth"]}"/>')
 elif t=='line':
  dp={'dash':[4,2],'dot':[1,2],'dashDot':[4,2,1,2]}.get(n.get('dash'))
  ls=(0,[v*72/25.4 for v in dp]) if dp else '-'
  ax.plot([n['x1'],n['x2']],[n['y1'],n['y2']],color=n['stroke'],lw=n['strokeWidth']*72/25.4,linestyle=ls,zorder=2)
  da=' stroke-dasharray="'+','.join(map(str,dp))+'"' if dp else ''
  svg.append(f'<line x1="{n["x1"]}" y1="{n["y1"]}" x2="{n["x2"]}" y2="{n["y2"]}" stroke="{n["stroke"]}" stroke-width="{n["strokeWidth"]}"{da}/>')
 elif t=='image':
  ax.imshow(Image.open(io.BytesIO(base64.b64decode(n['data']))),extent=(n['x'],n['x']+n['w'],n['y']+n['h'],n['y']),aspect='auto',zorder=2)
  svg.append(f'<image x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" xlink:href="data:image/png;base64,{n["data"]}"/>')
 elif t=='text':
  ar=ax.text(n['x'],n['y'],n['text'],fontsize=n['size']*72/25.4,color=n['fill'],weight='bold' if n['weight']=='bold' else 'normal',ha=n['align'],va='baseline',zorder=3);artists.append((n,ar))
  anch={'left':'start','center':'middle','right':'end'}[n['align']]
  svg.append(f'<text x="{n["x"]}" y="{n["y"]}" font-family="PosterSans,DejaVu Sans" font-size="{n["size"]}" font-weight="{700 if n["weight"]=="bold" else 400}" fill="{n["fill"]}" text-anchor="{anch}">{html.escape(n["text"])}</text>')
 elif t=='math':
  ar=ax.text(n['x']+n['w']/2,n['y']+n['h']/2,n['expr'],fontsize=n['size']*72/25.4,color=n['fill'],ha='center',va='center',zorder=3);artists.append((n,ar))
  buf=io.BytesIO()
  with plt.rc_context({'svg.fonttype':'path'}):math_to_image(n['expr'],buf,prop=FontProperties(size=n['size']*72/25.4),format='svg',color=n['fill'])
  el=ET.fromstring(buf.getvalue());vb=list(map(float,el.get('viewBox').split()));mw=vb[2]*25.4/72;mh=vb[3]*25.4/72
  if mw>n['w'] or mh>n['h']:formula_issues.append(n['expr'])
  raw=ET.tostring(el,encoding='unicode');ids=re.findall(r'\bid="([^"]+)"',raw)
  for ident in sorted(ids,key=len,reverse=True):raw=raw.replace('id="'+ident+'"','id="f'+str(i)+'_'+ident+'"').replace('#'+ident+'"','#f'+str(i)+'_'+ident+'"').replace('#'+ident+')','#f'+str(i)+'_'+ident+')')
  el=ET.fromstring(raw);el.set('x',str(n['x']+(n['w']-mw)/2));el.set('y',str(n['y']+(n['h']-mh)/2));el.set('width',str(mw));el.set('height',str(mh));svg.append(ET.tostring(el,encoding='unicode'))
svg.append('</svg>');(ROOT/'HUMOR-poster-editable.svg').write_text(''.join(svg))
(ROOT/'source/scene.json').write_text(json.dumps(dict(width=W,height=H,nodes=nodes),ensure_ascii=False))
fig.canvas.draw();renderer=fig.canvas.get_renderer();inva=ax.transData.inverted();bounds=[];issues=[]
for n,ar in artists:
 bb=ar.get_window_extent(renderer).transformed(inva);x0,x1=sorted([bb.x0,bb.x1]);y0,y1=sorted([bb.y0,bb.y1]);bounds.append(dict(text=n.get('text',n.get('expr')),section=n['section'],box=[x0,y0,x1,y1]))
 if n.get('parent'):
  p=next(p for p in panels if p['name']==n['parent'])
  if x0<p['x']+5 or x1>p['x']+p['w']-5 or y0<p['y']+5 or y1>p['y']+p['h']-5:issues.append(dict(text=n.get('text',n.get('expr')),section=n['section'],box=[x0,y0,x1,y1]))
record=dict(canvas_mm=[W,H],new_layout=True,text_count=len(artists),word_count=sum(len(n['text'].split()) for n in nodes if n['type']=='text'),containment_issues=issues,formula_overflow=formula_issues)
(ROOT/'source/layout_validation.json').write_text(json.dumps(record,indent=2));(ROOT/'source/text_bounds.json').write_text(json.dumps(bounds,indent=2))
fig.savefig(ROOT/'HUMOR-poster-print.pdf',dpi=240,metadata={'Title':'HUMOR — redesigned 140 × 90 cm poster','Author':'Xueyan Li; Yingyi Xue; Mengjie Jiang; Qingzi Zhu; Yazhe Niu'})
fig.savefig(ROOT/'HUMOR-poster-preview.png',dpi=55);plt.close(fig)
print(json.dumps(record,indent=2))

# Build the rest of the revision-v5-style deliverables from the same scene.
import runpy
runpy.run_path(str(ROOT/'source/build_editable.py'),run_name='__main__')
runpy.run_path(str(ROOT/'source/build_viewer.py'),run_name='__main__')
