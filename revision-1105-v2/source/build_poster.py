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
# 01: end on the two questions that A and B will answer.
panel('Task',25,119,270,365,'01  What makes a caption a meme?')
para(40,179,240,'Same visual relation, different context-specific punchlines.',10.7,14,c=INK,b=True)
text(94.5,210,'Template',10.2,INK,True,'center');text(223.5,210,'Meme',10.2,TEAL,True,'center')
pic('template',40,219,109);pic('apple-fans',169,219,109)
rect(40,309,240,31,PALE,3);text(50,321,'USER INPUT',8.8,TEAL,True);text(50,335,'Technology · “Apple fanatic”',10.1,TEAL,True)
for x,tag,value in [(40,'A · Subject','APPLE FANS'),(122,'B · New focus','IPHONE 11'),(204,'C · Neglected','IPHONE 10')]:
 rect(x,350,76,36,WHITE,3,'#BADAD6');text(x+38,364,tag,8.8,TEAL,True,'center');text(x+38,379,value,9.4,INK,True,'center')
text(40,409,'One template, many possible jokes.',10,TEAL,True)
para(40,430,240,'How do we explore different ideas, then learn which captions work better?',11,15,c=INK,b=True)
text(40,473,'Explore meanings → compare expressions',8.8,BLUE)
# 02: supervision construction, local comparison, and quality control.
panel('Method',315,119,1060,365,'02  HUMOR: explore before seeing the answer → compare locally → update with quality control',BLUE)
for x,w,k,title in [(330,329,'A','Two-stage reasoning supervision'),(680,329,'B','Local preference learning'),(1030,330,'C','Diversity with quality control')]:
 rect(x,167,w,303,'#F0F4FB' if k!='B' else PALE,4)
 rect(x+10,177,17,17,BLUE if k!='B' else TEAL,3);text(x+18.5,189,k,10,WHITE,True,'center')
 text(x+34,190,title,11.1,BLUE if k!='B' else TEAL,True)
arrow(662,321,677,321,BLUE);arrow(1012,321,1027,321,BLUE)
# A: no answer in initial search. Reveal reference only after paths exist.
text(341,212,'1  EXPLORE · REFERENCE CAPTION HIDDEN',9.2,BLUE,True)
para(341,230,305,'Infer the template’s intent; explore plausible situations before seeing the answer.',9.7,12.3)
pic('bean-template',341,259,44)
for yy,s in [(270,'Confusing work problem → bewilderment'),(292,'Bad joke → an exaggerated painful response'),(314,'Social ignorance → refusing to listen')]:
 selected=yy==314;rect(400,yy-13,245,20,'#DFEAF9' if selected else WHITE,2,BLUE if selected else LINE);text(408,yy,s,9.2,BLUE)
arrow(388,283,397,283,BLUE)
rect(341,340,305,70,'#FFF2DA',3,'#E4CDA7');pic('bean-gold',345,358,31)
text(350,355,'2  REVERSE-ANCHOR · REFERENCE REVEALED',8.6,GOLD,True)
para(385,373,249,'Infer the actual context from the caption; explain why an existing path fits it.',9.4,12)
text(385,402,'Keep the other explored associations.',9.1,GOLD)
arrow(628,339,628,323,GOLD)
para(341,429,305,'Reveal the answer only after exploration to reduce answer-driven rationalization.',9.7,12.5,c=BLUE,b=True)
text(341,463,'Generation: template + user intent; no reference caption.',8.7,MUTE)
# B: subjective scores -> conditional comparisons -> data -> expected wins.
para(691,212,305,'Humor is subjective; an absolute score is hard to calibrate. With the template and intended theme fixed, relative preference is easier to interpret.',9.4,12.2)
text(691,266,'Where do the training comparisons come from?',9.4,TEAL,True)
para(691,282,305,'Five difficulty tiers: wrong text, wrong location, boring, detailed boring, and generated memes.',9.3,12)
text(745,315,'Original',9.2,TEAL,True,'center');text(944,315,'Boring',9.2,MUTE,True,'center')
pic('pair-original',708,322,70);pic('pair-boring',909,322,70);text(844,352,'≻',16,TEAL,True,'center')
text(691,383,'Train pair preferences with binary cross-entropy.',9.1,INK)
fbox(691,390,305,25,r'$p_{ij}^G=\sigma[s_\phi(m_i)-s_\phi(m_j)]$',10.0)
fbox(691,419,305,27,r'$\mathrm{EBC}_G(i)=\sum_{j\ne i}p_{ij}^G$',10.0)
text(691,461,'Expected wins → group scores → ranking → target q',9.0,TEAL,True)
# C: two different conditional statements, no unconditional preservation claim.
para(1041,212,305,'Exploration broadens ideas but can include weaker jokes. Preferences guide quality; KL limits drift.',9.6,12.5)
text(1041,256,'A  Bound the gap in normalized path humor',9.4,BLUE,True)
fbox(1041,264,305,24,r'$1-\mathbb{E}_{r\sim P_\theta}[\tilde h_G(r)]\leq (1-\alpha)\delta$',10.5)
text(1041,301,'Best-path mass α; other paths’ mean gap ≤ δ.',9.1,MUTE)
text(1041,324,'B  Turn expected wins into local targets q',9.4,TEAL,True)
text(1041,341,'Favor captions that beat more alternatives.',9.5,INK)
text(1041,364,'C  Update the policy near the CoT reference',9.3,BLUE,True)
fbox(1041,373,305,28,r'$\mathcal{L}=-\mathbb{E}[\sum_k q_G(m_k)\log\pi_\theta(c_k\mid I)]+\beta\Delta_{\mathrm{KL}}$',9.3)
fbox(1041,407,305,23,r'$H_\theta\geq H_{\mathrm{CoT}}-\sqrt{\Delta_{\mathrm{KL}}/2}$',10.2)
para(1041,445,305,'H: normalized caption humor. ΔKL: drift from CoT. Bounds on loss are conditional; diversity gains are empirical.',8.5,11,c=MUTE)
# 03: retain source table; replace redundant delta list with a tradeoff plot.
panel('Generation',25,496,810,224,'03  Generation quality and diversity',TEAL)
t1=json.loads((ROOT/'source/table1.json').read_text());cols=[275,328,381,434,487,540,610]
rect(40,539,580,16,INK,2);text(45,551,'Model / variant',8.3,WHITE,True)
for xx,ss in zip(cols,['Hum. ↑','Read. ↑','Rel. ↑','Orig. ↑','Sim. ↑','Dist. ↑','Human % ↑']):text(xx,551,ss,7.8,WHITE,True,'right')
for i,row in enumerate(t1):
 yy=568+i*9.5+(3 if i>=5 else 0)+(3 if i>=7 else 0);own=row['model'].startswith('HUMOR');cc=GOLD if 'RL' in row['model'] else BLUE if own else TEXT
 if own:rect(40,yy-7.8,580,9.5,'#FFF0D3' if 'RL' in row['model'] else '#E1EBF8',0)
 if i in [5,7]:rule(40,yy-9,620,yy-9,TEAL,.5)
 text(45,yy,row['model'],8.0,cc,own)
 for j,(xx,val) in enumerate(zip(cols,row['values'])):
  best=val is not None and val==max(rr['values'][j] for rr in t1 if rr['values'][j] is not None)
  ss='—' if val is None else f'{val:.3f}' if j in [4,5] else f'{val:.1f}' if j==6 else f'{val:.2f}'
  text(xx,yy,ss,8.2,cc,best,'right')
text(40,696,'Human scores: 30 raters, 0–5. Human %: Gemini human/AI judgment.',8.1,MUTE)
text(40,709,'Sim.: bge embeddings. Dist.: context-swap distance, a diversity proxy. Table 1.',8.1,MUTE)
# Scatter: x is a diversity proxy, not an absolute creative-quality measure.
text(643,550,'Humor × context variation',9.4,TEAL,True)
sx=lambda d:666+(d-.56)/.04*138;sy=lambda h:649-(h-1.6)/1.4*81
for h in [2,2.5,3]:
 yy=sy(h);rule(666,yy,804,yy,LINE,.4);text(659,yy+2,str(h),7.4,MUTE,align='right')
rule(666,568,666,649,MUTE,.6);rule(666,649,804,649,MUTE,.6)
for d in [.56,.58,.60]:text(sx(d),661,f'{d:.2f}',7.4,MUTE,align='center')
pts=[('7B',.564,2.39,MUTE,4,-5),('Single',.570,1.87,MUTE,4,8),('Self',.578,2.38,MUTE,4,10),('Subq.',.597,1.85,MUTE,-5,10),('CoT',.590,2.68,TEAL,-7,11),('RL*',.588,2.83,GOLD,-9,-5)]
for lab,d,h,col,dx,dy in pts:
 rect(sx(d)-1.7,sy(h)-1.7,3.4,3.4,col,1.7);text(sx(d)+dx,sy(h)+dy,lab,8,col,lab in ['CoT','RL*'],align='right' if dx<0 else 'left')
text(735,674,'Context-swap distance →',8,MUTE,align='center')
para(643,691,176,'CoT improves both vs. 7B. RL* is preliminary; originality falls 2.90 → 2.79.',8.1,10.4,c=TEAL)
# 04: keep the actual outputs, two contexts and three comparable columns.
panel('Qualitative',855,496,520,224,'04  How do the jokes change?',BLUE)
for x,title,cc in [(1002,'Human reference',INK),(1120,'Single-path CoT',BLUE),(1238,'HUMOR-CoT',TEAL)]:text(x+40,548,title,8.8,cc,True,'center')
for y,theme,title,tags in [(554,'christmas','Christmas',['Family tradition','Delayed excitement']),(635,'romance','Romance',['Crush · dabbing','Rare moment'])]:
 text(872,y+22,title,10.4,BLUE,True)
 for j,t in enumerate(tags):text(872,y+42+j*15,t,9,INK)
 for x,suffix_name in [(1002,'reference'),(1120,'single'),(1238,'humor')]:pic(theme+'-'+suffix_name,x,y,77)
# 05: restore reward agreement with human MaxDiff, all backbones and groups.
panel('Reward',25,732,430,142,'05  Does the reward agree with people?',TEAL)
text(40,783,'Human MaxDiff vs. reward ranks · Kendall τ ↑',8.0,INK)
t2=json.loads((ROOT/'source/table2.json').read_text());reward_cols=[251,296,341,386,435]
text(40,796,'Reward model / state',7.9,INK,True)
for xx,j in zip(reward_cols,range(1,6)):text(xx,796,f'G{j}',7.9,INK,True,'right')
rule(40,799,438,799,LINE,.45)
for i,row in enumerate(t2):
 yy=809+i*9.0;own=i==5
 if own:rect(38,yy-7.1,402,9.0,PALE,0)
 if i in [2,4]:rule(40,yy-7.6,438,yy-7.6,LINE,.35)
 text(40,yy,row['model'],7.7,TEAL if own else TEXT,own)
 for xx,t,p in zip(reward_cols,row['tau'],row['p']):
  stars='***' if row.get('p_display') else '**' if p<.01 else '*' if p<.05 else ''
  text(xx,yy,f'{t:.2f}{stars}',7.8,TEAL if own else TEXT,own,'right')
text(40,866,'100 raters · 5 templates · *p<.05, ***p<.001 · Table 2',7.8,MUTE)
# 06: Table 5, user-intent recovery assessed by VLM reclassification.
panel('Intent',470,732,465,142,'06  Does the meme express your intent?',TEAL)
text(485,785,'Requested attributes → generated meme → VLM reclassification',8.4,INK)
intent_models=[('7B base',[42.0,51.5,55.1,52.1],MUTE,-9),('32B base',[57.1,61.1,61.6,60.3],BLUE,0),('HUMOR 7B',[59.7,64.1,60.0,63.9],TEAL,9)]
intent_x=[540,615,690,765];intent_y=lambda v:841-(v-40)*1.4
for v in [40,50,60,70]:
 yy=intent_y(v);rule(510,yy,790,yy,LINE,.4);text(502,yy+2,str(v),7.1,MUTE,align='right')
for name,values,col,dx in intent_models:
 for xx,val in zip(intent_x,values):
  rect(xx+dx-1.9,intent_y(val)-1.9,3.8,3.8,col,1.9)
  if name=='HUMOR 7B':text(xx+dx,intent_y(val)-4,f'{val:.1f}',7.4,TEAL,True,'center')
for xx,lab in zip(intent_x,['Emotion','Intention','Theme','Style']):text(xx,854,lab,8.0,INK,align='center')
for i,(name,values,col,dx) in enumerate(intent_models):
 yy=801+i*12;rect(808,yy-5,3.8,3.8,col,1.9);text(818,yy,name,8.4,col,name=='HUMOR 7B')
para(808,841,113,'Above 32B on 3 of 4 attributes.',8.1,10.5,c=TEAL,b=True)
text(485,866,'Table 5 · reclassification accuracy (%) · higher is better',8.1,MUTE)
# 07: retain transfer evidence but avoid a dominant evaluation block.
panel('Transfer',950,732,425,142,'07  Unseen templates',TEAL)
transfer=json.loads((ROOT/'source/unseen-figure-data.json').read_text());series={s['model']:s['ranks'] for s in transfer['series']}
xp=[979+j*(266/7) for j in range(8)];yrank=lambda v:790+(v-1)*(54/6)
for v in [1,3,5,7]:
 yy=yrank(v);rule(977,yy,1246,yy,'#E0E8ED',.35);text(970,yy+2,str(v),7,MUTE,align='right')
styles={'Human':(BLUE,None,1.1),'HUMOR-CoT':(TEAL,None,1.2),'Qwen 32B':('#C17B0A',None,.65),'Keye':('#8855A2',None,.65),'InternVL':('#C54D72',None,.65),'Qwen 7B':('#8D5D2E',None,.65),'GLM':('#627686',None,.65)}
for name in ['GLM','Qwen 7B','InternVL','Keye','Qwen 32B','Human','HUMOR-CoT']:
 col,dash,sw=styles[name];vals=series[name]
 for j in range(7):rule(xp[j],yrank(vals[j]),xp[j+1],yrank(vals[j+1]),col,sw)
for xx,s in zip(xp,['Caption','Theme','Emotion','Humor','Punchline','Cultural','Context','Spread']):text(xx,855,s,6.1,MUTE,align='center')
for i,name in enumerate(['Human','HUMOR-CoT','Qwen 32B','Keye','InternVL','Qwen 7B','GLM']):
 col,dash,sw=styles[name];yy=791+i*9;rule(1260,yy-2,1270,yy-2,col,sw);text(1275,yy,name,7.2,col,name in ['Human','HUMOR-CoT'])
text(965,866,'20 templates · Gemini-2.5-pro mean rank ↓',8.0,TEAL,True)
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
# SVG is the editable deliverable for this poster revision.
runpy.run_path(str(ROOT/'source/build_viewer.py'),run_name='__main__')
