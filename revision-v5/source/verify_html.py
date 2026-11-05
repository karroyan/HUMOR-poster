from pathlib import Path
import re,json,xml.etree.ElementTree as ET
from html.parser import HTMLParser
r=Path(__file__).resolve().parents[1]
h=(r/'HUMOR-poster.html').read_text();s=(r/'HUMOR-poster-editable.svg').read_text()
assert '<div id="sheet">'+s+'</div>' in h
root=ET.fromstring(s);ids=[n.attrib['id'] for n in root.iter() if 'id' in n.attrib];assert len(ids)==len(set(ids))
external=[]
for n in root.iter():
 for k,v in n.attrib.items():
  if k.endswith('href') and not v.startswith(('data:','#')):external.append(v)
for v in re.findall(r'url\(([^)]+)\)',s):
 if not v.startswith(('data:','#')):external.append(v)
assert not external
class Page(HTMLParser):
 def __init__(self):super().__init__();self.buttons=0;self.scripts=[];self.inscript=False
 def handle_starttag(self,tag,attrs):
  if tag=='button':self.buttons+=1
  if tag=='script':self.inscript=True
 def handle_endtag(self,tag):
  if tag=='script':self.inscript=False
 def handle_data(self,data):
  if self.inscript:self.scripts.append(data)
p=Page();p.feed(h);assert p.buttons==4
(r/'source/viewer.js').write_text(''.join(p.scripts))
v=json.loads((r/'source/validation.json').read_text())
for key in ['containment_issues','text_overlaps','unintended_text_image_intersections','formula_vector_overflow']:assert not v[key]
report=dict(html_svg_matches_standalone=True,unique_svg_ids=len(ids),external_resources=external,embedded_font_faces=s.count('@font-face'),viewer_controls=p.buttons,svg_xml='valid',formula_box_overflow='none',section_overflow='none',browser_runtime_test='not available; no browser screenshot or print claims',js_syntax_check='performed separately with Node')
(r/'source/html-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
