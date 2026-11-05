"""HUMOR v5: self-contained HTML + vector SVG/PDF from one measured scene."""
from pathlib import Path
import base64,csv,json,re,html,shutil,io,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,Rectangle
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.mathtext import math_to_image
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'source';A=ROOT/'assets';OLD=ROOT.parent
W,H=1400,900
INK='#1A3A4A';BODY='#293A43';MUTED='#566975';GREEN='#1A6B5A';BLUE='#2C5AA0';GOLD='#B06A0A';WHITE='#FFFFFF';LINE='#D3DEE2'
PGREEN='#EEF6F3';PBLUE='#F0F4FA';PGOLD='#FDF6EC';GTRAIN='#FFF0D9'
nodes=[];containers=[];section='Header';parent=None
renderer=RendererAgg(10,10,72)
def font(size,b=False,it=False,fam='DejaVu Sans'):return FontProperties(family=fam,size=size,weight='bold' if b else 'normal',style='italic' if it else 'normal')
def measure(t,size,b=False,it=False):return renderer.get_text_width_height_descent(t,font(size,b,it),False)[0]
def add(t,**kw):nodes.append(dict(type=t,section=section,parent=parent,**kw));return nodes[-1]
def rect(x,y,w,h,c,stroke=None,r=3,sw=.6,name='Card'):return add('rect',name=name,x=x,y=y,w=w,h=h,fill=c,stroke=stroke,radius=r,strokeWidth=sw)
def txt(x,y,t,size=10.5,c=BODY,b=False,align='left',it=False):return add('text',name=t,x=x,y=y,text=t,size=size,fill=c,weight='bold' if b else 'regular',align=align,italic=it)
def line(x1,y1,x2,y2,c=LINE,sw=.6):add('line',name='Rule',x1=x1,y1=y1,x2=x2,y2=y2,stroke=c,strokeWidth=sw)
def arrow(x1,y1,x2,y2,c=BLUE):
 line(x1,y1,x2,y2,c,1)
 a=math.atan2(y2-y1,x2-x1)
 for d in [-.5,.5]:line(x2,y2,x2-3*math.cos(a+d),y2-3*math.sin(a+d),c,1)
def para(x,y,w,t,size=10.5,leading=14,c=BODY,b=False,it=False):
 cur=''
 for word in t.split():
  test=(cur+' '+word).strip()
  if measure(test,size,b,it)>w and cur:txt(x,y,cur,size,c,b,it=it);y+=leading;cur=word
  else:cur=test
 if cur:txt(x,y,cur,size,c,b,it=it)
 return y+leading

def rich(x,y,w,t,size=10.5,leading=14,c=BODY):
 # Measured runs preserve semantic bold emphasis without risking hand-set line lengths.
 toks=re.split(r'(\*\*.*?\*\*|_.*?_)',t);xx=x
 for tok in toks:
  b=tok.startswith('**');it=not b and tok.startswith('_');s=tok[2:-2] if b else tok[1:-1] if it else tok
  for word in re.findall(r'\s+|\S+',s):
   if word.isspace():
    if xx>x:xx+=measure(word,size,b,it)
    continue
   advance=measure(word,size,b,it)
   if xx+advance>x+w and xx>x:xx=x;y+=leading
   txt(xx,y,word,size,INK if b else c,b,it=it);xx+=advance
 return y+leading

def pic(name,x,y,w):
 p=A/name;im=Image.open(p);h=w*im.height/im.width
 add('image',name=name,x=x,y=y,w=w,h=h,data=base64.b64encode(p.read_bytes()).decode())
 return h

def panel(name,x,y,w,h,color,accent,title):
 global parent,section
 section=name;parent=name;containers.append(dict(name=name,x=x,y=y,w=w,h=h))
 rect(x,y,w,h,color,r=5,name=name)
 title_size=15
 while measure(title,title_size,True)>w-28:title_size-=.2
 txt(x+14,y+24,title,title_size,accent,True);line(x+14,y+33,x+w-14,y+33,accent,1)
def tag(x,y,t,c=BLUE):
 ww=measure(t,8.8,True)+14;rect(x,y-11,ww,16,c,r=2);txt(x+7,y,t,8.8,WHITE,True)
def formula(x,y,w,h,expr,size=11,c=INK):
 rect(x,y,w,h,WHITE,stroke='#B8C7D6',r=3)
 add('math',name=expr,x=x+5,y=y+3,w=w-10,h=h-6,expr=expr,size=size,fill=c)
# Local copies; inputs do not depend on network.
for f in ['table1.csv','unseen-figure-data.json']:
 if (OLD/'revision-v4/source'/f).exists():shutil.copy2(OLD/'revision-v4/source'/f,S/f)
 elif not (S/f).exists():raise FileNotFoundError(f)
for src,dst in [('template.png','template.png'),('apple-fans.png','apple-fans.png'),('fig16-single.png','work-single.png'),('fig16-humor.png','work-humor.png')]:
 if (OLD/'revision-v4/assets'/src).exists():shutil.copy2(OLD/'revision-v4/assets'/src,A/dst)
 elif not (A/dst).exists():raise FileNotFoundError(dst)
if (OLD/'assets/evaluation-comparison.png').exists():shutil.copy2(OLD/'assets/evaluation-comparison.png',A/'evaluation-comparison.png')
for src,dst in [('p32-2.png','bean-template.png'),('p32-0.png','bean-gold.png'),('p22-6.png','pair-original.png'),('p22-7.png','pair-wrong-text.png'),('p22-11.png','pair-wrong-position.png')]:shutil.copy2(A/src,A/dst)
rect(0,0,W,H,WHITE,r=0);rect(0,0,W,6,GREEN,r=0)
txt(30,43,'From Perception to Punchline:',29,INK,True)
txt(30,77,'Empowering VLM with the Art of In-the-wild Memes',25,INK,True)
txt(30,102,'Xueyan Li* [1]   Yingyi Xue* [1,2]   Mengjie Jiang [3]   Qingzi Zhu [1]   Yazhe Niu† [4]',11.4,INK,True)
txt(30,121,'[1] Shanghai AI Laboratory   [2] Fudan University   [3] Columbia Engineering, Columbia University   [4] CUHK MMLab',9.6,MUTED)
txt(1370,45,'HUMOR',34,GREEN,True,'right')
txt(1370,66,'Hierarchical Understanding',9.8,MUTED,align='right');txt(1370,81,'and Meme Optimization',9.8,MUTED,align='right')
txt(1370,103,'NeurIPS 2026',11,INK,True,'right');txt(1370,122,'* Equal contribution   † Corresponding author',7.8,MUTED,align='right')
line(30,136,1370,136,GREEN,1.3)
# 1a: two appearances of this template; none elsewhere.
panel('1a Task',30,150,340,347,PGREEN,GREEN,'1a  What makes a caption a meme?')
rich(44,200,312,'**Meme generation goes beyond captioning:** a shared visual relation supports many _context-specific punchlines_.',10.5,14)
txt(44,242,'Template + roles',9.5,GREEN,True);txt(213,242,'Technology / Apple fanatic',8.8,GREEN,True)
pic('template.png',44,251,140);pic('apple-fans.png',213,251,140)
for x,y,t in [(128,328,'A'),(86,333,'B'),(167,325,'C')]:rect(x-6,y-10,12,14,GREEN,r=1)['zorder']=2.5;txt(x,y,t,9,WHITE,True,'center')
for x,a,b,v in [(44,'A','Subject','APPLE FANS'),(150,'B','New focus','IPHONE 11'),(256,'C','Neglected','IPHONE 10')]:
 rect(x,354,98,39,WHITE,stroke='#B8D4C8',r=3)
 txt(x+49,367,a+' · '+b,8.2,GREEN,True,'center');txt(x+49,384,v,9.2,INK,True,'center')
rich(44,415,312,'**Reusable template intent:** infatuation with the new and abandonment of the old.',10.4,14)
para(44,451,312,'Input: template + user intent. Output: humorous text assigned to designated image regions.',10.2,14)
# brief value directly following problem, separate visual line
rect(44,477,312,13,'#DDEDE5',r=2);txt(50,486,'A testbed for subjective multimodal generation.',8.8,GREEN,True)
# 1b: reason for preference approach; original evidence + actual dataset variants.
panel('1b Why local',30,512,340,338,PGREEN,GREEN,'1b  Learn preferences, not global scores')
rich(44,562,312,'Humor is **context-dependent**. Global scores assume a common scale across unrelated jokes; within-template pairs share a **coherent semantic structure**.',10.1,13.5)
pic('evaluation-comparison.png',44,611,312)
para(44,700,312,'Fig. 4: absolute scores blur real vs. text-free memes; local ranks separate them more clearly.',9.6,13)
txt(44,734,'Human check: ρ = 0.72; τ = 0.63',10.4,GREEN,True)
txt(44,747,'9 annotators · 5 groups · 30 memes (App. K.5)',8.3,MUTED)
txt(44,760,'5 pair types: wrong text / location / boring / edits / generated.',8.3,MUTED)
for x,f,l in [(44,'pair-original.png','Original'),(151,'pair-wrong-text.png','Wrong text'),(258,'pair-wrong-position.png','Wrong position')]:
 pic(f,x,769,96);txt(x+48,846,l,8.2,GREEN,True,'center')
# 2a: corrected bidirectional logic from Sec 3.1 / B / Fig14.
panel('2a Multi-path',390,150,540,370,PBLUE,BLUE,'2a  Explore multiple scenes, then reverse-anchor')
rich(404,200,512,'**Single-answer rationales expose only one route.** HUMOR separates _template-level intent_ from _context-level grounding_ (§3.1).',10.6,14)
tag(404,237,'1  MULTI-SCENARIO ASSOCIATION')
pic('bean-template.png',404,249,78)
para(404,345,96,'Bewilderment / annoyance',8.5,11,c=MUTED)
arrow(489,291,508,291)
for y,t in [(249,'A confusing work problem → bewildered reaction'),(278,'A bad joke → exaggerated “painful” response'),(307,'Social ignorance → refusing to listen')]:
 rect(518,y,398,24,'#DFEAF9' if t.startswith('Social') else WHITE,stroke=BLUE if t.startswith('Social') else '#D7E2F0',r=3);txt(528,y+16,t,10,BLUE)
arrow(850,363,850,337,GOLD)
txt(658,354,'Trace back to the compatible scene',8.7,GOLD,it=True)
rect(404,365,512,97,GTRAIN,stroke='#E4CDA7',r=4)
pic('bean-gold.png',413,373,67)
txt(490,385,'2  REVERSE-ANCHOR FROM A REAL MEME',10.6,GOLD,True)
rich(490,405,412,'**Gold caption c → infer U: socializing / ignorance**, then trace back to a compatible path; retain other associations.',10.1,13)
formula(490,435,412,22,r'$\tilde r=\arg\max_r\,P_\phi(c\mid r,I,U)$',10.4)
txt(413,457,'Real reference',7.7,GOLD,it=True)
rect(404,474,512,24,'#E2EAF6',r=3)
txt(414,490,'INFERENCE  Explore and select internally; no gold caption is available.',9.7,BLUE,True)
txt(404,510,'Fig. 14 / App. B; scenario summaries paraphrase the paper’s traces.',8.6,MUTED,it=True)
# 2b: algorithm and training, more detail than v4.
panel('2b Preference',390,535,540,315,PBLUE,BLUE,'2b  Template-local reward → group-wise optimization')
rich(404,585,512,'Compare memes **only within G** (a shared template). Train a reward model on **constructed preference pairs**, rather than calibrating global humor (§3.2).',10.4,14)
txt(404,619,'PAIRWISE MODEL · BCE TRAINING',8.8,BLUE,True)
txt(668,619,'EXPECTED BORDA COUNT',8.8,BLUE,True)
rect(404,627,248,40,WHITE,stroke='#B8C7D6',r=3)
add('math',name='Pairwise probability',x=409,y=629,w=238,h=16,expr=r'$p_{ij}^G=\sigma[s_\phi(m_i)-s_\phi(m_j)]$',size=9.8,fill=INK)
add('math',name='Binary cross entropy',x=409,y=648,w=238,h=14,expr=r'$\ell=-y\log p-(1-y)\log(1-p)$',size=8.6,fill=INK)
formula(668,627,248,40,r'$\mathrm{EBC}_G(i)=\sum_{j\ne i}p_{ij}^G$',11)
rect(404,673,512,72,WHITE,stroke='#C9D7EA',r=3)
txt(415,689,'GROUP-LOCAL AGGREGATION  ·  Appendix E, Algorithm 1',9.4,BLUE,True)
txt(415,706,'1  Estimate pairs inside the template group; omit missing edges.',9.6)
txt(415,722,'2  Sum expected wins; normalize by observed opponents if sparse.',9.6)
txt(415,738,'3  Rank candidates; optional qG = softmax(EBC / T), T > 0.',9.6)
txt(404,763,'POLICY UPDATE  ·  reference = CoT policy  (§3.3)',8.8,BLUE,True)
formula(404,771,512,36,r'$\mathcal{L}=-\mathbb{E}[\sum_k q_G(m_k)\log\pi_\theta(c_k\mid I)]+\beta\,\mathbb{E}[\mathrm{KL}(\pi_\theta\Vert\pi_{\mathrm{CoT}})]$',9.6)
formula(404,815,512,22,r'$H(\pi_\theta)\geq H(\pi_{\mathrm{CoT}})-\sqrt{\Delta_{\mathrm{KL}}/2}$',10.2)
txt(404,847,'KL bounds potential degradation; it does not guarantee gains.',9.1,MUTED,it=True)
# 3: compact but complete evidence; numbers from local paper, never from the HTML mockup.
panel('3 Evidence',950,150,420,700,PGOLD,GOLD,'3  Evidence: generation, reward & transfer')
para(964,200,392,'30 native-English raters · 3–5 memes / method / rater. Human scores: 0–5 ↑; tuned variants use the same 7B.',9.8,13)
rect(964,232,392,41,'#FFF0CE',stroke='#EAD29E',r=3)
txt(975,250,'Humor: 2.39 → 2.68 with HUMOR-CoT',12,GOLD,True)
txt(975,266,'Single-path: 1.87   |   RL preview: 2.83',9.8,GOLD)
xs=[964,1148,1200,1252,1304,1350]
rect(964,287,392,20,INK,r=2)
txt(970,300,'Model / variant',8.8,WHITE,True)
for x,t in zip(xs[1:],['Hum.','Read.','Rel.','Orig.','Dist.']):txt(x,300,t,8.2,WHITE,True,'right')
rows=list(csv.DictReader((S/'table1.csv').open()));keys=['humor','readability','relevance','originality','context_swap_distance']
ren={'Qwen2.5-7B-Instruct':'Qwen2.5-7B','Qwen2.5-32B-Instruct':'Qwen2.5-32B','GLM-4.1V-9B-Thinking':'GLM-4.1V-9B','Keye-VL-8B-preview':'Keye-VL-8B','HUMOR-RL (preview)':'HUMOR-RL · preview'}
for i,r in enumerate(rows):
 yy=320+i*11.5;own=r['model'].startswith('HUMOR');cc=GOLD if 'RL' in r['model'] and own else BLUE if own else BODY
 if own:rect(964,yy-9,392,11.5,'#FFF0CE' if 'RL' in r['model'] else '#E5EDF9',r=0)
 txt(970,yy,ren.get(r['model'],r['model']),8.5,cc,own)
 for j,k in enumerate(keys):
  v=float(r[k]);best=v==max(float(z[k]) for z in rows)
  txt(xs[j+1],yy,f'{v:.3f}' if j==4 else f'{v:.2f}',8.6,cc,best,'right')
 line(964,yy+3,1356,yy+3,'#E1E1DD',.35)
txt(964,465,'Table 1 · Bold: column best. Dist.: context-swap distance ↑.',8.2,MUTED)
rect(964,475,392,35,'#FFF0CE',r=3)
rich(974,489,372,'**RL trade-off:** humor rises to 2.83, while originality drops **2.90 → 2.79**. RL remains a preview.',9.5,12,c=GOLD)
txt(964,530,'Single-path CoT',9.4,INK,True);txt(1134,530,'HUMOR-CoT',9.4,BLUE,True)
pic('work-single.png',964,539,89);pic('work-humor.png',1134,539,89)
para(1060,565,64,'Literal work scenario',8.8,12,c=MUTED)
para(1230,565,126,'Specific conflict: the boss interrupts the repair by email.',9.1,12,c=BLUE,b=True)
txt(964,643,'Fig. 16 · same template / work intent; original outputs.',8.2,MUTED,it=True)
txt(964,666,'Reward–human agreement',12,GOLD,True)
txt(964,681,'100 MaxDiff raters · 5 templates · Kendall τ ↑',8.6,MUTED)
for j,t in enumerate(['G1','G2','G3','G4','G5']):txt(1164+j*43,696,t,8,MUTED,align='center')
rm=[('Qwen 7B · base',[.16,.28,.47,-.10,.29]),('Qwen 7B · trained',[.47,.56,.42,.14,.47]),('Qwen 32B · base',[.16,.16,-.02,.14,.29]),('Qwen 32B · trained',[.29,.47,.07,.30,.42]),('Keye 8B · base',[.05,.09,.16,.29,.16]),('Keye 8B · trained',[.78,.77,.78,.78,.78])]
for i,(lab,vs) in enumerate(rm):
 yy=709+i*9.2
 if i==5:rect(964,yy-7.5,392,9.2,'#FFF0CE',r=0)
 txt(964,yy,lab,8.2,GOLD if i==5 else BODY,i==5)
 for j,v in enumerate(vs):txt(1164+j*43,yy,f'{v:.2f}',8.2,GOLD if i==5 else BODY,i==5,'center')
txt(964,775,'20 unseen templates · Gemini mean rank ↓',11,GOLD,True)
data=json.loads((S/'unseen-figure-data.json').read_text());ser={v['model']:v['ranks'] for v in data['series']}
for j,(a,b) in enumerate([('Img–text',''),('Theme',''),('Emo-','tion'),('Humor',''),('Punch-','line'),('Cultural','fit'),('Con-','text'),('Spread','')]):
 txt(1066+j*38.7,788,a,6.5,MUTED,align='center')
 if b:txt(1066+j*38.7,795,b,6.5,MUTED,align='center')
import matplotlib.colors as mc
import numpy as np
for i,lab in enumerate(['Human','HUMOR-CoT','Qwen 32B','Keye','InternVL','Qwen 7B','GLM']):
 yy=804+i*6.9;txt(964,yy+1,lab,7.4,BLUE if lab=='HUMOR-CoT' else BODY,lab in ['Human','HUMOR-CoT'])
 for j,v in enumerate(ser[lab]):
  rgb=np.array(mc.to_rgb('#2C5AA0'))*(7-v)/7+np.array(mc.to_rgb('#FFFFFF'))*v/7
  rect(1048+j*38.7,yy-5.5,36.7,6.5,mc.to_hex(rgb),r=0)
  txt(1066+j*38.7,yy-.1,f'{v:.1f}',6.7,WHITE if v<3 else BODY,lab=='HUMOR-CoT','center')
# Footer
section='Footer';parent=None
line(30,867,1370,867,GREEN,1)
txt(30,885,'Scope: English meme culture · limited human samples · ~2–3× output tokens · concrete keywords can induce literalism.',8.9,MUTED)
txt(1370,885,'3,345 train / 368 test  |  karroyan13@gmail.com',8.9,GREEN,align='right')
# --- Export and measured validation ---
plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none','image.composite_image':False})
fig=plt.figure(figsize=(W/25.4,H/25.4));ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,W),ylim=(H,0));ax.axis('off')
fontsdir=Path(matplotlib.__file__).parent/'mpl-data/fonts/ttf';(ROOT/'fonts').mkdir(exist_ok=True)
css=''
for fname,weight in [('DejaVuSans.ttf',400),('DejaVuSans-Bold.ttf',700),('DejaVuSans-Oblique.ttf','italic')]:
 shutil.copy2(fontsdir/fname,ROOT/'fonts'/fname)
 css+=f"@font-face{{font-family:PosterSans;src:url(data:font/ttf;base64,{base64.b64encode((fontsdir/fname).read_bytes()).decode()}) format('truetype');font-weight:{weight if weight!='italic' else 400};font-style:{'italic' if weight=='italic' else 'normal'};}}"
shutil.copy2(fontsdir/'LICENSE_DEJAVU',ROOT/'fonts/LICENSE_DEJAVU')
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="1400mm" height="900mm" role="img" aria-label="HUMOR research poster"><defs><style>{css}</style></defs>']
artists=[];math_vector_issues=[]
for idx,n in enumerate(nodes):
 t=n['type']
 if t=='rect':
  ax.add_patch(FancyBboxPatch((n['x'],n['y']),n['w'],n['h'],boxstyle=f'round,pad=0,rounding_size={n["radius"]}',facecolor=n['fill'],edgecolor=n['stroke'] or 'none',lw=n['strokeWidth']*72/25.4,zorder=n.get('zorder',1)))
  svg.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" rx="{n["radius"]}" fill="{n["fill"]}" stroke="{n["stroke"] or "none"}" stroke-width="{n["strokeWidth"]}"/>')
 elif t=='line':
  ax.plot([n['x1'],n['x2']],[n['y1'],n['y2']],color=n['stroke'],lw=n['strokeWidth']*72/25.4,zorder=2,solid_capstyle='butt')
  svg.append(f'<line x1="{n["x1"]}" y1="{n["y1"]}" x2="{n["x2"]}" y2="{n["y2"]}" stroke="{n["stroke"]}" stroke-width="{n["strokeWidth"]}"/>')
 elif t=='image':
  im=Image.open(io.BytesIO(base64.b64decode(n['data'])));ax.imshow(im,extent=(n['x'],n['x']+n['w'],n['y']+n['h'],n['y']),aspect='auto',zorder=2)
  svg.append(f'<image x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" xlink:href="data:image/png;base64,{n["data"]}"/>')
 elif t=='text':
  ar=ax.text(n['x'],n['y'],n['text'],fontsize=n['size']*72/25.4,color=n['fill'],weight='bold' if n['weight']=='bold' else 'normal',style='italic' if n['italic'] else 'normal',ha=n['align'],va='baseline',zorder=3);artists.append((n,ar))
  anchor={'left':'start','right':'end','center':'middle'}[n['align']]
  svg.append(f'<text x="{n["x"]}" y="{n["y"]}" fill="{n["fill"]}" font-family="PosterSans,DejaVu Sans,sans-serif" font-size="{n["size"]}" font-weight="{700 if n["weight"]=="bold" else 400}" font-style="{"italic" if n["italic"] else "normal"}" text-anchor="{anchor}">{html.escape(n["text"])}</text>')
 elif t=='math':
  ar=ax.text(n['x']+n['w']/2,n['y']+n['h']/2,n['expr'],fontsize=n['size']*72/25.4,color=n['fill'],ha='center',va='center',zorder=3);artists.append((n,ar))
  b=io.BytesIO();math_to_image(n['expr'],b,prop=font(n['size']),format='svg',color=n['fill']);ss=b.getvalue().decode();ss=ss[ss.index('<svg'):]
  # Unique vector IDs avoid collisions between mathematical expressions.
  ss=re.sub(r'id="([^"]+)"',lambda m:f'id="f{idx}-{m[1]}"',ss);ss=re.sub(r'(?:xlink:href|href)="#([^"]+)"',lambda m:f'xlink:href="#f{idx}-{m[1]}"',ss);ss=re.sub(r'url\(#([^\)]+)\)',lambda m:f'url(#f{idx}-{m[1]})',ss)
  vb=re.search(r'viewBox="([^"]+)"',ss)[1];_,_,vw,vh=map(float,vb.split());xx=n['x']+(n['w']-vw)/2;yy=n['y']+(n['h']-vh)/2
  if vw>n['w'] or vh>n['h']:math_vector_issues.append(dict(formula=n['expr'],vector_size=[vw,vh],box_size=[n['w'],n['h']]))
  ss=re.sub(r'width="[^"]+"',f'width="{vw}"',ss,count=1);ss=re.sub(r'height="[^"]+"',f'height="{vh}"',ss,count=1);ss=ss.replace('<svg ',f'<svg x="{xx}" y="{yy}" ',1);svg.append(ss)
svg.append('</svg>');sv='\n'.join(svg)
(ROOT/'HUMOR-poster-editable.svg').write_text(sv)
fig.savefig(ROOT/'HUMOR-poster-print.pdf',dpi=160);fig.savefig(ROOT/'HUMOR-poster-preview.png',dpi=48)
fig.canvas.draw();rr=fig.canvas.get_renderer();inv=ax.transData.inverted();bounds=[]
for n,ar in artists:
 p=inv.transform(ar.get_window_extent(rr).get_points());x0,x1=sorted(p[:,0]);y0,y1=sorted(p[:,1]);bounds.append(dict(text=n.get('text',n.get('expr')),type=n['type'],parent=n['parent'],x0=x0,x1=x1,y0=y0,y1=y1))
issues=[];overlaps=[];text_images=[]
for b in bounds:
 if b['x0']<0 or b['x1']>W or b['y0']<0 or b['y1']>H:issues.append(dict(reason='canvas',**b))
 if b['parent']:
  c=next(c for c in containers if c['name']==b['parent'])
  if b['x0']<c['x']+3 or b['x1']>c['x']+c['w']-3 or b['y0']<c['y']+3 or b['y1']>c['y']+c['h']-1:issues.append(dict(reason='section containment',**b))
 for n in nodes:
  if n['type']=='image' and min(b['x1'],n['x']+n['w'])-max(b['x0'],n['x'])>.45 and min(b['y1'],n['y']+n['h'])-max(b['y0'],n['y'])>.45 and b['text'] not in ['A','B','C']:text_images.append([b['text'],n['name']])
for i,a in enumerate(bounds):
 for b in bounds[i+1:]:
  if min(a['x1'],b['x1'])-max(a['x0'],b['x0'])>.5 and min(a['y1'],b['y1'])-max(a['y0'],b['y0'])>.5:overlaps.append([a['text'],b['text']])
report=dict(canvas_mm=[W,H],text_and_math_count=len(bounds),containment_issues=issues,text_overlaps=overlaps,unintended_text_image_intersections=text_images,formula_vector_overflow=math_vector_issues,browser_layout_check='Browser runtime not installed; HTML embeds the exact measured SVG scene and fonts used for the preview.')
(S/'validation.json').write_text(json.dumps(report,indent=2));(S/'scene.json').write_text(json.dumps(dict(width=W,height=H,nodes=nodes),ensure_ascii=False));(S/'poster-copy.txt').write_text('\n'.join(n['text'] for n in nodes if n['type']=='text'))
# An offline HTML viewer embeds the complete vector poster and fonts, so substitutions cannot alter layout.
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HUMOR · research poster v5</title><style>
*{box-sizing:border-box}body{margin:0;background:#e8edf1;font-family:system-ui,sans-serif}.toolbar{height:56px;display:flex;align-items:center;gap:12px;padding:10px 24px;color:#1a3a4a;background:#fff;border-bottom:1px solid #ccd8df}.toolbar strong{margin-right:auto}button{border:1px solid #b9c8d1;border-radius:6px;background:white;padding:7px 14px;color:#1a3a4a;cursor:pointer}button:hover{background:#eef6f3}#viewport{padding:24px;overflow:auto;min-height:calc(100vh - 56px)}#sheet{margin:auto;box-shadow:0 5px 30px #1a3a4a20;background:white;line-height:0}#sheet>svg{display:block;width:100%;height:auto}small{color:#607681} @page{size:1400mm 900mm;margin:0}@media print{body{background:white;width:1400mm;height:900mm}.toolbar{display:none}#viewport{padding:0;overflow:visible;min-height:0}#sheet{width:1400mm!important;box-shadow:none;margin:0}#sheet>svg{width:1400mm;height:900mm}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style><div class="toolbar"><strong>HUMOR · Poster v5</strong><small>140 × 90 cm · offline vector artwork</small><button onclick="fit()">Fit to window</button><button onclick="zoom(1.25)">＋</button><button onclick="zoom(.8)">−</button><button onclick="window.print()">Print / PDF</button></div><main id="viewport"><div id="sheet">POSTER</div></main><script>const sheet=document.getElementById('sheet');let w=1400;function fit(){w=Math.max(360,window.innerWidth-48);sheet.style.width=w+'px'}function zoom(s){w=Math.max(360,w*s);sheet.style.width=w+'px'}fit();window.addEventListener('resize',fit);window.posterInfo={version:5,widthMM:1400,heightMM:900,embeddedFonts:true};</script></html>'''
(ROOT/'HUMOR-poster.html').write_text(page.replace('POSTER',sv))
print('Exported',len(nodes),'nodes;',len(issues),'containment;',len(overlaps),'text overlaps;',len(text_images),'text/image collisions')
