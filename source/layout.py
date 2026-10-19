# Scientific three-column poster; all coordinates in millimetres.
import textwrap, pdfplumber
INK='#172B31'; MUTED='#4E6065'; TEAL='#146C68'; BLUE=TEAL; ORANGE='#A5682D'; LINE='#CBD7D7'; PALE='#EDF4F2'; CREAM='#FAF3E9'; WHITE='#FFFFFF'
fonts=Path('/System/Library/Fonts/Supplemental')
pdfmetrics.registerFont(TTFont('Arial',str(fonts/'Arial.ttf')))
pdfmetrics.registerFont(TTFont('Arial-Bold',str(fonts/'Arial Bold.ttf')))
def para(x,y,w,text,size=10.5,leading=14,fill=INK,bold=False):
    words=text.split(); current=''; yy=y
    for word in words:
        test=(current+' '+word).strip()
        if pdfmetrics.stringWidth(test,'Arial-Bold' if bold else 'Arial',size)>w and current:
            txt(x,yy,current,size,fill,bold); yy+=leading; current=word
        else: current=test
    if current: txt(x,yy,current,size,fill,bold)
    return yy+leading

def heading(x,y,w,num,title):
    txt(x,y,num,15,TEAL,True); txt(x+27,y,title,17,INK,True)
    line(x,y+8,x+w,y+8,TEAL,1.4)

def down(x,y1,y2,col=TEAL):
    line(x,y1,x,y2,col,1.3); line(x-3,y2-4,x,y2,col,1.3); line(x+3,y2-4,x,y2,col,1.3)

rect(0,0,W,H,WHITE,name='White paper')
rect(0,0,1400,6,TEAL)
txt(30,43,'From Perception to Punchline:',29,bold=True)
txt(30,77,'Empowering VLM with the Art of In-the-wild Memes',26,bold=True)
txt(30,101,'Xueyan Li [1]   Yingyi Xue [1,2]   Mengjie Jiang [3]   Qingzi Zhu [1]   Yazhe Niu [4]',12,bold=True)
txt(30,120,'[1] Shanghai Artificial Intelligence Laboratory   [2] Fudan University   [3] Columbia Engineering, Columbia University   [4] CUHK MMLab',9.7,MUTED)
txt(1370,43,'HUMOR',35,TEAL,True,align='right')
txt(1370,63,'Hierarchical Understanding',10,TEAL,align='right')
txt(1370,78,'and Meme Optimization',10,TEAL,align='right')
txt(1370,104,'NeurIPS 2026',12,bold=True,align='right')
line(30,133,1370,133,INK,1.3)
line(422,151,422,850,LINE,.6); line(922,151,922,850,LINE,.6)

sec='1 Task and motivation'
heading(30,157,380,'1','What makes a caption a meme?')
y=para(30,184,380,'Meme generation connects visual relationships to a situation and a punchline. Naming objects is not enough; the same template can express many different intentions.')
y=para(30,y+3,380,'Input: a template plus user intent (emotion, theme, style or keywords). Output: captions assigned to the template’s text regions.',bold=True)
txt(30,290,'One template, three different outcomes',12,TEAL,True)
for xx,f,lab in [(30,'christmas_human.png','Human reference'),(161,'christmas_single_path.png','Single-path CoT'),(292,'christmas_humor_cot.png','HUMOR-CoT')]:
    pic(f,xx,302,118,119); txt(xx+59,436,lab,10,TEAL if lab=='HUMOR-CoT' else INK,True,align='center')
para(30,455,380,'Fig. 16 examples. Single-path reasoning repeats anticipation; the reference supplies a concrete obstacle. HUMOR learns a context-dependent delayed-reward situation.',10,13)

sec='2 Evaluation formulation'
heading(30,515,380,'2','Why compare within a template?')
para(30,542,380,'A global “funniness score” assumes that unrelated jokes share one scale. We instead learn relative quality inside a coherent group G, usually one template.',10.5,14)
pic('evaluation-comparison.png',30,574,380,116.14602615846813,name='combined_parallel_coordinates_plot_print.png')
para(30,703,380,'Fig. 4. Absolute VLM scores (left) poorly separate real memes from blank images; group-wise ranks (right) provide clearer distinctions. Lower rank is better.',9.6,12.8)
para(30,750,380,'Independent check: 9 annotators, 5 groups, 30 memes. Gemini–human agreement: Spearman 0.72; Kendall τ = 0.63.',10.4,14,bold=True)
para(30,799,380,'Data: 3,345 train / 368 test instances. Teacher: Doubao-1.5-Vision-Pro. Human ratings and MaxDiff rankings are separate from constructed training pairs.',10.3,13.5)

sec='3 Hierarchical multi-path reasoning'
heading(435,157,475,'3','Explore contexts, then ground a path')
para(435,184,475,'Direct caption supervision hides the associations behind a joke. HUMOR builds traces that preserve several plausible contexts before grounding one path in a real meme.',10.5,14)
# A concrete, labelled visual relation, with three branching contexts.
pic('distracted_boyfriend_template.png',435,232,158,105.4)
txt(435,352,'Template interpretation',10.7,TEAL,True)
para(435,369,158,'Attention shifts from an existing commitment to a new attraction.',9.6,12)
arrow(602,281,624,TEAL)
txt(634,244,'MULTI-CONTEXT EXPLORATION',9.7,TEAL,True)
for yy,lab in [(254,'Technology → a new phone'),(290,'Work → a new opportunity'),(326,'Daily life → a tempting purchase')]:
    rect(634,yy,276,28,PALE)
    txt(644,yy+18,lab,10.5)
# Fan-in connects exploration to supervision.
line(772,354,772,369,TEAL,1.2); down(772,369,386)
rect(634,389,276,63,CREAM)
txt(644,409,'GROUND-TRUTH ANCHOR · TRAINING ONLY',9.4,ORANGE,True)
para(644,426,254,'A real caption supplies the actual context; bind its roles to regions and realize the punchline.',10,13)
para(435,423,177,'These context branches illustrate the reusable relation; they are not scored outputs.',8.8,11.7,fill=MUTED)
rect(435,466,475,49,PALE)
txt(446,484,'AT INFERENCE',9.5,TEAL,True)
para(446,501,453,'Template + user intent → hypothesize contexts → select a path → positioned caption. No reference caption is used.',10.2,13)

sec='4 Local preference learning'
heading(435,547,475,'4','Learn preferences, not global scores')
para(435,574,475,'Training pairs share a template. Five constructed difficulty tiers teach a VLM reward model to distinguish disrupted meaning, weak humor and plausible alternatives.',10.3,13.5)
# compact curriculum, two rows; no invented numerical scores
for xx,yy,w,top,bottom in [(435,612,148,'Wrong text','unrelated caption'),(598,612,148,'Wrong location','misplaced roles'),(761,612,149,'Boring','mundane statement'),(435,659,229,'Detailed boring','small edits weaken the joke'),(681,659,229,'Generated','harder model-written alternatives')]:
    line(xx,yy,xx+w,yy,LINE,.8); txt(xx,yy+16,top,10.6,TEAL,True); txt(xx,yy+31,bottom,9.6,MUTED)
txt(435,718,'Pairwise probability',10.5,bold=True)
txt(638,718,'p(i > j | G) = σ[s(i) − s(j)]',12.2,TEAL)
txt(435,741,'Expected Borda Count',10.5,bold=True)
txt(638,741,'EBC(i) = Σ p(i > j | G),  j ≠ i',12.2,TEAL)
para(435,765,475,'Binary cross-entropy trains the pairwise comparator. Expected wins induce a group-local preference distribution q. The policy learns to favor higher-ranked captions while staying near its CoT reference.',10.3,13.5)
rect(435,813,475,34,PALE)
txt(447,834,'Policy loss = −E[Σ q log π(c | I)] + β E[KL(π || πref)]',12,TEAL,True)

sec='5 Main results'
heading(935,157,435,'5','Generation quality and ablations')
para(935,184,435,'30 native-English raters; 3–5 memes per method per rater. Human scores are means on a 0–5 scale (↑). All fine-tuned variants use the 7B backbone.',10.3,13.5)
# Full set of model comparisons, four human metrics plus context distance.
xs=[935,1154,1203,1252,1301,1355]
txt(935,241,'Model',9.8,bold=True)
for x,t in zip(xs[1:],['Hum.','Read.','Rel.','Orig.','Dist.']): txt(x,241,t,9.2,bold=True,align='right')
line(935,248,1370,248,INK,1)
rows=list(csv.DictReader((ROOT/'source'/'table1.csv').open()))
renames={'Qwen2.5-7B-Instruct':'Qwen2.5-7B','Qwen2.5-32B-Instruct':'Qwen2.5-32B','GLM-4.1V-9B-Thinking':'GLM-4.1V-9B-Thinking','Keye-VL-8B-preview':'Keye-VL-8B-preview'}
for i,r in enumerate(rows):
    yy=264+i*17.5; own=r['model'] in ['HUMOR-CoT','HUMOR-RL (preview)']
    if own: rect(932,yy-12.5,438,17,PALE)
    if i in [5,7]: line(935,yy-13,1370,yy-13,LINE,.7)
    txt(935,yy,renames.get(r['model'],r['model']),9.8,TEAL if own else INK,own)
    for j,key in enumerate(['humor','readability','relevance','originality','context_swap_distance']):
        v=float(r[key]); best=v==max(float(a[key]) for a in rows)
        txt(xs[j+1],yy,format(v,'.3f' if j==4 else '.2f'),9.8,TEAL if own else INK,best,align='right')
line(935,463,1370,463,INK,1)
para(935,480,435,'Table 1. All 12 models/variants. Dist. = context-swap distance, a diversity proxy. Human/AI discriminability is omitted. Bold: column best.',9.2,12)
para(935,517,435,'CoT improves humor 2.39 → 2.68; single-path CoT falls to 1.87. RL reaches 2.83 in preliminary results, with lower originality than CoT (2.79 vs. 2.90).',10.3,13.5)

sec='6 Reward agreement'
heading(935,578,435,'6','Does the reward agree with people?')
para(935,603,435,'Kendall τ against human MaxDiff rankings: 100 participants, 5 templates, 10–15 candidates per group.',10.1,13.2)
txt(935,643,'Reward backbone / state',9.3,bold=True)
for x,t in zip([1174,1221,1268,1315,1362],['G1','G2','G3','G4','G5']): txt(x,643,t,9.3,bold=True,align='right')
line(935,650,1370,650,INK,.8)
rm=[('Qwen2.5-7B · base',[.16,.28,.47,-.10,.29]),('Qwen2.5-7B · trained',[.47,.56,.42,.14,.47]),('Qwen2.5-32B · base',[.16,.16,-.02,.14,.29]),('Qwen2.5-32B · trained',[.29,.47,.07,.30,.42]),('Keye-VL-8B · base',[.05,.09,.16,.29,.16]),('Keye-VL-8B · trained',[.78,.77,.78,.78,.78])]
for i,(lab,vals) in enumerate(rm):
    yy=665+i*17
    if i==5: rect(932,yy-12,438,17,PALE)
    txt(935,yy,lab,9.6,TEAL if i==5 else INK,i==5)
    for x,v in zip([1174,1221,1268,1315,1362],vals): txt(x,yy,f'{v:.2f}',9.6,TEAL if i==5 else INK,i==5,align='right')
line(935,758,1370,758,INK,.8)
para(935,777,435,'Table 2. Keye reward training consistently reaches τ ≈ 0.78. Improvements are less consistent on Qwen backbones; ranking quality depends on the reward model.',10.3,13.5)
para(935,828,435,'Pair construction is synthetic/model-assisted; the evaluation uses human rankings.',9.6,12.5,fill=MUTED)

# Reserve an entire final scientific strip for theory and generalization.
# Expand canvas downwards? Fixed print dimensions: compress main body vertically into 140..690,
# preserving title and reserving 160 mm for genuinely new evidence.
for nd in nodes:
    if nd['section']!='Header':
        for k in ['y','y1','y2']:
            if k in nd: nd[k]=140+(nd[k]-140)*.775
        if nd['type'] in ['rect','image']: nd['h']*=.775
        # Keep images undistorted by shrinking widths identically, centering within original width.
        if nd['type']=='image' and nd['name'] != 'combined_parallel_coordinates_plot_print.png':
            original=nd['w']; nd['w']*=.775; nd['x']+=(original-nd['w'])/2
        if nd['type']=='text': nd['size']*=.92
# Header vertical separators had Header section; shorten explicitly.
for nd in nodes:
    if nd['type']=='line' and nd.get('y2')==850: nd['y2']=690

sec='7 Conditional analysis'
heading(30,719,630,'7','What the analysis guarantees')
txt(30,747,'Exploration',10.5,TEAL,True)
txt(154,747,'E[h] ≥ 1 − (1 − α)δ',14,TEAL)
para(30,768,610,'If promising paths retain mass α and the remaining quality gap is at most δ, expected normalized humor has this lower bound. More paths alone do not establish the assumptions.',10,13)
txt(30,812,'KL stability',10.5,TEAL,True)
txt(154,812,'H(π) ≥ H(ref) − √(ΔKL / 2)',14,TEAL)
para(30,833,610,'For bounded humor h in [0,1], KL limits possible degradation. Preference consistency additionally assumes a monotone observation model; neither result guarantees monotonic gains.',10,13)

sec='8 Unseen templates'
heading(690,719,680,'8','Generalization to 20 unseen templates')
# Reconstruct exact series coordinates from original vector figure for editable legible chart.
p=pdfplumber.open(A/'unseen.pdf').pages[0]
curves=[c for c in p.curves if len(c['pts'])==8]
seriesnames=['Human','HUMOR-CoT','GLM','InternVL','Keye','Qwen 7B','Qwen 32B']
colors=['#223C46',TEAL,'#B99B79','#AFA7BA','#94ABA2','#9CAEC2','#92B6B3']
chartx=713; charty=749; chartw=414; charth=95
for r in [1,2,3,4,5,6,7]:
    yy=charty+(r-1)*charth/6
    line(chartx,yy,chartx+chartw,yy,LINE,.35); txt(chartx-9,yy+2,str(r),7.2,MUTED,align='right')
extracted=[]
for idx in [2,3,4,5,6,0,1]:
    c=curves[idx]; vals=[round(1+(y-155.410987111)/43.47608983,1) for x,y in c['pts']]; extracted.append({'model':seriesnames[idx],'ranks':vals})
    points=[(chartx+j*chartw/7,charty+(v-1)*charth/6) for j,v in enumerate(vals)]
    for pa,pb in zip(points,points[1:]): line(*pa,*pb,colors[idx],1.35 if idx<2 else .7)
    for x,y in points: rect(x-1.3,y-1.3,2.6,2.6,colors[idx])
for j,s in enumerate(['Caption','Theme','Emotion','Humor','Punchline','Cultural','Context','Spread']): txt(chartx+j*chartw/7,857,s,6.9,MUTED,align='center')
txt(713,737,'Gemini group-wise rank ↓',8.5,MUTED)
for j,(n,col) in enumerate(zip(seriesnames,colors)):
    yy=744+j*15; line(1154,yy-3,1166,yy-3,col,1.5); txt(1173,yy,n,8.6,col,j<2)
para(1280,744,90,'Second to human memes across all eight dimensions.',8.6,11.5,bold=True)
(ROOT/'source'/'unseen-figure-data.json').write_text(json.dumps({'source':'Exact plotted coordinates extracted from original unseen.pdf (Fig. 5), rounded to source precision; not raw evaluation records.','categories':['Caption','Theme','Emotion','Humor','Punchline','Cultural','Context','Spread'],'series':extracted},indent=2))

sec='Footer'
line(30,870,1370,870,TEAL,1)
txt(30,887,'Scope: English meme culture; limited human samples; ~2–3× output-token cost; concrete keywords can induce literalism.',9.2,MUTED)
txt(1370,887,'Paper: arxiv.org/abs/2512.24555  |  karroyan13@gmail.com',9.2,TEAL,align='right')
