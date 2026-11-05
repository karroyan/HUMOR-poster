"""Optional independent evidence check. Requires pypdf, matplotlib, Pillow."""
from pathlib import Path
import re,json,csv,xml.etree.ElementTree as ET
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];PAPER=ROOT.parent/'assets/Meme_NeurIPS_2026.pdf'
r=PdfReader(PAPER)
# Exact decimal sequence accommodates adjacent text runs in the source PDF.
t=r.pages[7].extract_text(extraction_mode='layout')
rows=list(csv.DictReader((ROOT/'source/table1.csv').open()))
source_names=['Qwen2.5-7B-Instruct','Qwen2.5-32B-Instruct','InternVL3-8B','GLM-4.1V-9B-Thinking','Keye-VL-8B-preview','GPT-4o','Gemini-2.5-flash','HUMOR-CoT','CoT with Single Path','CoT with Self-Improve','CoT with Subquestion','HUMOR-RL (preview)']
for row,name in zip(rows,source_names):
 ln=next(x for x in t.splitlines() if x.strip().startswith(name))
 ln=ln.split(']')[-1] if ']' in ln else ln[len(ln)-len(ln.lstrip())+len(name):]
 m=re.search(r'(\d\.\d{2})\s*(\d\.\d{2})\s*(\d\.\d{2})\s*(\d\.\d{2})\s*(0\.\d{3})\s*(0\.\d{3})',ln)
 assert m,(name,ln)
 vals=list(map(float,m.groups()))
 for k,v in zip(['humor','readability','relevance','originality','context_swap_distance'],vals[:4]+vals[5:6]):assert float(row[k])==v,(name,k)
# Original embedded Fig.5 vector coordinates, separate from supplied extracted chart data.
p=r.pages[9];forms=[o.get_object() for o in p['/Resources']['/XObject'].values() if o.get_object().get('/Subtype')=='/Form']
f=next(o for o in forms if b'(Caption)' in o.get_data() and b'(Theme)' in o.get_data())
paths=re.findall(rb'((?:[\d.]+ [\d.]+ [ml]\s*){8})S',f.get_data())
assert len(paths)==7,len(paths)
names=['Human','HUMOR-CoT','GLM','InternVL','Keye','Qwen 7B','Qwen 32B']
supplied={s['model']:s['ranks'] for s in json.loads((ROOT/'source/unseen-figure-data.json').read_text())['series']}
independent={}
for n,path in zip(names,paths):
 pts=re.findall(rb'([\d.]+) ([\d.]+) [ml]',path)
 vals=[round(1+(413.9330-float(y))/(413.9330-362.3437),1) for x,y in pts]
 assert vals==supplied[n],(n,vals,supplied[n]);independent[n]=vals
# Match all 30 Kendall tau entries, skipping alternating p-values.
t=r.pages[9].extract_text();states=['Qwen2.5-VL-7B (Base)','Qwen2.5-VL-7B (Finetuned)','Qwen2.5-VL-32B (Base)','Qwen2.5-VL-32B (Finetuned)','Keye-VL-8B (Base)','Keye-VL-8B (Finetuned)']
expected=[[.16,.28,.47,-.10,.29],[.47,.56,.42,.14,.47],[.16,.16,-.02,.14,.29],[.29,.47,.07,.30,.42],[.05,.09,.16,.29,.16],[.78,.77,.78,.78,.78]]
for state,vs in zip(states,expected):
 ln=next(x for x in t.splitlines() if x.startswith(state));found=list(map(float,re.findall(r'-?\d\.\d{2}',ln)))[::2]
 assert found==vs,(state,found)
scene=json.loads((ROOT/'source/scene.json').read_text())
# Embedded image boxes preserve exact source aspect ratios.
from PIL import Image
from io import BytesIO
import base64
for n in scene['nodes']:
 if n['type']=='image':
  im=Image.open(BytesIO(base64.b64decode(n['data'])));assert abs(n['w']/n['h']-im.width/im.height)<1e-6
pdf=PdfReader(ROOT/'HUMOR-poster-print.pdf');assert len(pdf.pages)==1
p=pdf.pages[0];mm=[float(p.mediabox.width)*25.4/72,float(p.mediabox.height)*25.4/72]
assert all(abs(a-b)<.01 for a,b in zip(mm,[1400,900]))
assert len(p.images)==sum(n['type']=='image' for n in scene['nodes'])
fonts=[]
for o in p['/Resources']['/Font'].values():
 font=o.get_object();fonts.append(str(font['/BaseFont']))
 desc=font['/DescendantFonts'][0].get_object()['/FontDescriptor'].get_object()
 assert '/FontFile2' in desc
ET.parse(ROOT/'HUMOR-poster-editable.svg')
v=json.loads((ROOT/'source/validation.json').read_text());assert not v['containment_issues'];assert not v['text_overlaps'];assert not v['unintended_text_image_intersections'];assert not v['formula_vector_overflow']
assert all(supplied['Human'][i]<supplied['HUMOR-CoT'][i]<min(supplied[n][i] for n in names[2:]) for i in range(8))
report=dict(paper=str(PAPER),table1_values_checked=60,table2_tau_values_checked=30,figure5_vector_values_checked=56,figure5_values=independent,pdf_pages=1,pdf_size_mm=mm,pdf_embedded_fonts=fonts,pdf_image_count=len(p.images),image_aspect_ratios='preserved',svg_xml='valid',text_bounds='pass',text_intersections='none',figma_client_test='not performed',statistics='descriptive means; no invented CIs or significance tests')
(ROOT/'source/evidence-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
