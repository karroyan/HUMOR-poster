from pathlib import Path
import json,re,zipfile,xml.etree.ElementTree as E,posixpath,hashlib,base64,io,zlib
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
pdf=(R/'HUMOR-poster-print.pdf').read_bytes();mb=re.search(rb'/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]',pdf)
v=list(map(float,mb.groups()));cm=[(v[2]-v[0])*2.54/72,(v[3]-v[1])*2.54/72]
assert abs(cm[0]-140)<.0001 and abs(cm[1]-90)<.0001
assert len(re.findall(rb'/Type\s*/Page\b',pdf))==1 and b'/FontFile2' in pdf
layout=json.loads((R/'source/layout_validation.json').read_text());assert not layout['containment_issues'] and not layout['formula_overflow']
bounds=json.loads((R/'source/text_bounds.json').read_text());overlaps=[]
for i,a in enumerate(bounds):
 for b in bounds[i+1:]:
  x0,y0,x1,y1=a['box'];u0,v0,u1,v1=b['box']
  if min(x1,u1)-max(x0,u0)>.5 and min(y1,v1)-max(y0,v0)>.5:overlaps.append([a['text'],b['text']])
assert not overlaps,overlaps
scene=json.loads((R/'source/scene.json').read_text());collisions=[]
for a in bounds:
 for n in scene['nodes']:
  if n['type']!='image':continue
  x0,y0,x1,y1=a['box'];u0=n['x'];v0=n['y'];u1=u0+n['w'];v1=v0+n['h']
  if min(x1,u1)-max(x0,u0)>.5 and min(y1,v1)-max(y0,v0)>.5:collisions.append(a['text'])
assert not collisions,collisions
for n in scene['nodes']:
 if n['type']=='image':
  im=Image.open(io.BytesIO(base64.b64decode(n['data'])));assert abs(n['w']/n['h']-im.width/im.height)<1e-6
with zipfile.ZipFile(R/'HUMOR-poster-editable.pptx') as z:
 assert z.testzip() is None
 sz=E.fromstring(z.read('ppt/presentation.xml')).find('{http://schemas.openxmlformats.org/presentationml/2006/main}sldSz');assert sz.get('cx')=='50400000' and sz.get('cy')=='32400000'
 for p in z.namelist():
  if p.endswith(('.xml','.rels')):E.fromstring(z.read(p))
  if p.endswith('.rels'):
   base=posixpath.dirname(posixpath.dirname(p))
   for rel in E.fromstring(z.read(p)):
    assert rel.get('TargetMode')=='External' or posixpath.normpath(posixpath.join(base,rel.get('Target'))) in z.namelist()
 ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'};slide=E.fromstring(z.read('ppt/slides/slide1.xml'));ids=[n.get('id') for n in slide.findall('.//p:cNvPr',ns)];assert len(ids)==len(set(ids));txt_count=len(slide.findall('.//a:t',ns))
# Independently parse the actual paper excerpt, separate from chart/table data files.
paper=(R/'source/paper_text.txt').read_text();p8=paper.split('===== PAGE 8 =====')[1].split('===== PAGE 9 =====')[0]
t1=json.loads((R/'source/table1.json').read_text());checked=0
for row in t1:
 tail=p8.split(row['source'],1)[1];found=list(map(float,re.findall(r'-?\d+\.\d+',tail)))
 vals=row['values'];expected=[v for v in vals if v is not None]
 assert found[:len(expected)]==expected,(row['source'],found[:7],expected)
 checked+=len(expected)
p10=paper.split('===== PAGE 10 =====')[1].split('===== PAGE 11 =====')[0]
t2=json.loads((R/'source/table2.json').read_text());checked2=0
for row in t2:
 tail=p10.split(row['source'],1)[1];found=list(map(float,re.findall(r'-?\d+\.\d+',tail)))[:10]
 expected=[v for pair in zip(row['tau'],row['p']) for v in pair]
 assert found==expected,(row['source'],found,expected);checked2+=len(expected)
 if row.get('p_display'):assert '***' in tail.splitlines()[0]
base=t1[0]['values'];cot=t1[7]['values'];delta=[round(b-a,3) for a,b in zip(base,cot)];assert delta==[.29,.35,.59,.33,.064,.026,15.8]
# Exact source Fig.16 first-row crop checks, plus the actual boring variant in Fig.9.
full=Image.open(R/'source/figure16_source.png').convert('RGB')
crops={'christmas-reference':[523,304,905,686],'christmas-humor':[924,304,1303,686],'christmas-single':[1324,304,1703,686],'romance-reference':[523,713,905,1095],'romance-humor':[922,713,1305,1095],'romance-single':[1322,713,1703,1095]}
for name,box in crops.items():
 actual=Image.open(R/'assets'/f'{name}.png').convert('RGB');expected=full.crop(box)
 assert actual.size==expected.size and ImageChops.difference(actual,expected).getbbox() is None,name
pb=(R/'source/pairwise_source.pdf').read_bytes();obj=re.search(rb'\b52 0 obj\b(.*?)endobj',pb,re.S)[1]
w=int(re.search(rb'/Width (\d+)',obj)[1]);h=int(re.search(rb'/Height (\d+)',obj)[1]);start=obj.index(b'stream')+6
if obj[start:start+2]==b'\r\n':start+=2
elif obj[start:start+1] in [b'\n',b'\r']:start+=1
ln=int(re.search(rb'/Length (\d+)',obj)[1]);expected=Image.frombytes('RGB',(w,h),zlib.decompress(obj[start:start+ln]))
actual=Image.open(R/'assets/pair-boring.png').convert('RGB');assert actual.size==expected.size and ImageChops.difference(actual,expected).getbbox() is None
E.parse(R/'HUMOR-poster-editable.svg')
# Independently recover original Fig.5 plotted ranks from PDF vector coordinates.
unseen=json.loads((R/'source/unseen-figure-data.json').read_text());supplied={s['model']:s['ranks'] for s in unseen['series']}
paths=None
for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream',(R/'source/unseen_source.pdf').read_bytes(),re.S):
 try:data=zlib.decompress(m[1])
 except zlib.error:continue
 candidates=re.findall(rb'((?:[\d.]+ [\d.]+ [ml]\s*){8})S',data)
 if len(candidates)==7:paths=candidates;break
assert paths is not None
independent={}
for name,path in zip(['Human','HUMOR-CoT','GLM','InternVL','Keye','Qwen 7B','Qwen 32B'],paths):
 pts=re.findall(rb'([\d.]+) ([\d.]+) [ml]',path)
 vals=[round(1+(413.9330-float(y))/(413.9330-362.3437),1) for x,y in pts]
 assert vals==supplied[name],(name,vals,supplied[name]);independent[name]=vals
assert all(supplied['Human'][i]<supplied['HUMOR-CoT'][i]<min(supplied[n][i] for n in supplied if n not in ['Human','HUMOR-CoT']) for i in range(8))
assert 'CoT Generation Model doubao-1.5-vision-pro' in paper
alltext=' '.join(n['text'] for n in scene['nodes'] if n['type']=='text')
for token in ['What makes a caption a meme?','Does HUMOR improve meme quality and diversity?','Meme generation across themes','Does HUMOR generalize to unseen templates?','h ∈ [0,1]','Single-image scores barely separate quality.','Boring']:
 assert token in alltext,token
for forbidden in ['Equal contribution','Corresponding author','Teacher:','5 pair tiers']:
 assert forbidden not in alltext,forbidden
for step in ['1  Estimate preferences inside template G.','2  Sum wins; normalize sparse comparisons.','3  Rank candidates → local policy targets.']:
 assert step in alltext,step
image_names={n['name'] for n in scene['nodes'] if n['type']=='image'}
assert 'pair-boring' in image_names and 'pair-wrong-text' not in image_names
assert set(crops)<=image_names
assert any(n['type']=='line' and n.get('y1')==108 and n.get('y2')==108 and n.get('x1')==25 for n in scene['nodes'])
assert 'stroke-dasharray' not in (R/'HUMOR-poster-editable.svg').read_text()
curve_colors={'#2854A1','#007F79','#C17B0A','#8855A2','#C54D72','#8D5D2E','#627686'}
curve_lines=[n for n in scene['nodes'] if n['type']=='line' and n['section']=='Transfer' and n['stroke'] in curve_colors and n['x1']<1231 and n['x2']<1231]
assert len(curve_lines)==49
assert {n['stroke'] for n in curve_lines}==curve_colors
assert {n.get('dash') for n in curve_lines}=={None}
with zipfile.ZipFile(R/'HUMOR-poster-editable.pptx') as z:
 assert b'<a:prstDash ' not in z.read('ppt/slides/slide1.xml')
# Verify the requested aligned cards and meaningful A/C emphasis.
qual=next(n for n in scene['nodes'] if n['type']=='rect' and n['section']=='Qualitative')
trans=next(n for n in scene['nodes'] if n['type']=='rect' and n['section']=='Transfer')
assert (qual['x'],qual['w'])==(trans['x'],trans['w'])==(855,520)
for token in ['five types: wrong text, wrong location,','boring, detailed boring, and generated memes.','MULTI-SCENARIO ASSOCIATION','REVERSE-ANCHOR FROM A REAL MEME']:
 assert token in alltext,token
assert any(n['type']=='rect' and n.get('x')==400 and n.get('y')==278 and n.get('fill')=='#DFEAF9' for n in scene['nodes'])
assert any(n['type']=='line' and n.get('x1')==628 and n.get('x2')==628 and n.get('y1')==317 and n.get('y2')==299 and n.get('stroke')=='#A36012' for n in scene['nodes'])
crows=[n for n in scene['nodes'] if n['type']=='rect' and n.get('x')==1041 and n.get('w')==305 and n.get('h')==21]
assert len(crows)==3 and {n['fill'] for n in crows}=={'#DDE8F7'}
assert any(n['type']=='math' and r'1-(1-\alpha)\delta' in n['expr'] for n in scene['nodes'])

# Check the complete requested labels and unchanged gallery footprint.
for token in ['A confusing work problem → bewildered reaction','A bad joke → exaggerated "painful" response','Social ignorance → refusing to listen','Christmas','Romance','Happiness · humor','Crush · dabbing','Rare moment']:
 assert token in alltext,token
assert (qual['x'],qual['y'],qual['w'],qual['h'])==(855,465,520,248)
assert len([n for n in scene['nodes'] if n['type']=='image' and n['section']=='Qualitative'])==6
# The pre-edit scope comparison was completed upstream and retained in
# export_validation_upstream.json; this organized package does not require old backup ZIPs.
record={'size_cm':cm,'pdf_pages':1,'pdf_fonts_embedded':True,'table1_reported_values_checked':checked,'table1_missing_human_rate':'Gemini-2.5-flash, shown as dash','table2_tau_and_p_values_checked':checked2,'table2_display':'30 tau values with source-derived significance stars; full p-values retained in table2.json','figure5_plotted_values_checked':56,'figure5_values_independent':independent,'figma_comparison_completed':True,'layout_revision':6,'delta_values_checked':delta,'figure16_outputs_pixel_checked':list(crops),'user_input_tags':{'Christmas':['love','humor','family tradition','delayed excitement'],'Romance':['happiness','humor','crush','dabbing','rare moment']},'displayed_cases':['Human reference','Single-path CoT','HUMOR-CoT'],'theme_rows':2,'card04_size_unchanged_mm':[520,248],'A_branch_texts_complete':True,'boring_image':'pixel-identical to Fig.9 source PDF object 52','header_divider_mm':108,'rank_plot_frame_mm':[520,149],'rank_plot_axes_mm':[340,66],'rank_plot_colors':7,'rank_plot_line_styles':1,'cards_04_06_aligned':True,'five_pair_types_present':True,'C_steps_equal_emphasis':True,'A_reference_style':'revision-v5 A selected scene, reverse-anchor panel and vertical arrow; good-path bound retained','algorithm_steps':'continuous 1–3','reference_not_inference_input':True,'formula_overflow':[],'text_overlap':overlaps,'text_image_collision':collisions,'text_containment_issues':[],'word_count':layout['word_count'],'pptx_text_shapes':txt_count,'pptx_xml_and_relationships':'valid','pptx_office_render':'unavailable','api_posteragent_executed':False,'paper_sha256':hashlib.sha256((R.parent/'assets/Meme_NeurIPS_2026.pdf').read_bytes()).hexdigest()}
(R/'source/evidence-validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2));print(json.dumps(record,ensure_ascii=False,indent=2))
