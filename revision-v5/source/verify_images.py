from pathlib import Path
import json
from pypdf import PdfReader
from PIL import Image,ImageChops
r=Path(__file__).resolve().parents[1];p=PdfReader(r.parent/'assets/Meme_NeurIPS_2026.pdf');d=json.loads((r/'source/provenance.json').read_text());checked=[]
for name,meta in d['figures'].items():
 if 'image_index' not in meta:continue
 src=p.pages[meta['page']-1].images[meta['image_index']].image.convert('RGB')
 if 'crop' in meta:src=src.crop(meta['crop'])
 out=Image.open(r/'assets'/name).convert('RGB')
 assert src.size==out.size,name
 assert ImageChops.difference(src,out).getbbox() is None,name
 checked.append(name)
(r/'source/image-validation.json').write_text(json.dumps({'pixel_exact_with_original_pdf':checked,'other_figures':'Supplied v4 template / Apple output and existing original Fig.4 crop copied without modification.'},indent=2));print('Pixel-identical source images / crops verified:',len(checked))
