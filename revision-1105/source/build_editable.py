"""Offline Paper2Poster skill export. Native DrawingML text/shapes; SVG formulas.
Exports the newly composed HUMOR redesign scene, not the API-driven PosterAgent pipeline.
Run with /usr/bin/python3 (Pillow), from any directory.
"""
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr
import xml.etree.ElementTree as ET
import json, zipfile, base64, io, shutil, hashlib, re
from PIL import Image, ImageFont
ROOT=Path(__file__).resolve().parents[1]
A='http://schemas.openxmlformats.org/drawingml/2006/main'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL='http://schemas.openxmlformats.org/package/2006/relationships'
NS=f'xmlns:a="{A}" xmlns:p="{P}" xmlns:r="{R}"'
scene=json.loads((ROOT/'source/scene.json').read_text())
svg=ET.parse(ROOT/'HUMOR-poster-editable.svg').getroot()
maths=iter([n for n in svg if n.tag.endswith('}svg')])
preview=Image.open(ROOT/'HUMOR-poster-preview.png').convert('RGBA')
files={}; shapes=[];rels=[];sid=1
emu=lambda x: str(round(x*36000))
def xml(path,s):files[path]=s.encode('utf-8')
def rgb(c):return c.lstrip('#').upper()
def fill(c):return f'<a:solidFill><a:srgbClr val="{rgb(c)}"/></a:solidFill>' if c else '<a:noFill/>'
def line(c=None,w=.3,dash=None):
 d=f'<a:prstDash val="{dash}"/>' if dash else ''
 return f'<a:ln w="{emu(w)}">{fill(c)}{d}</a:ln>'
def xfrm(x,y,w,h,attrs=''):return f'<a:xfrm {attrs}><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(max(.01,w))}" cy="{emu(max(.01,h))}"/></a:xfrm>'
def nv(name,pic=False):
 global sid
 sid+=1
 tag='Pic' if pic else 'Sp'
 return f'<p:nv{tag}Pr><p:cNvPr id="{sid}" name={quoteattr(name[:200])}/><p:cNv{tag}Pr/><p:nvPr/></p:nv{tag}Pr>'
def media(data,ext):
 name=f'asset{len(rels)+1}.{ext}'; rid=f'rId{len(rels)+2}'
 files['ppt/media/'+name]=data;rels.append((rid,'../media/'+name,'image'));return rid

def picture(n,data,ext='png',vector=None):
 rid=media(data,ext);ex=''
 if vector:
  vr=media(vector,'svg')
  ex=f'<a:extLst><a:ext uri="{{96DAC541-7B7A-43D3-8B79-37D633B846F1}}"><asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="{vr}"/></a:ext></a:extLst>'
 return f'<p:pic>{nv(n.get("name","Figure"),True)}<p:blipFill><a:blip r:embed="{rid}">{ex}</a:blip><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr>{xfrm(n["x"],n["y"],n["w"],n["h"])}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>'

# Resolve original draw order: cards < figures/rules < role badges < text.
def z(n):return n.get('zorder', {'rect':1,'line':2,'image':2,'text':3,'math':3}[n['type']])
mathnodes={}
for i,n in enumerate(scene['nodes']):
 if n['type']=='math':mathnodes[i]=next(maths)
fonts={}
for i,n in sorted(enumerate(scene['nodes']),key=lambda it:z(it[1])):
 t=n['type']
 if t=='rect':
  geom='roundRect' if n.get('radius',0) else 'rect'
  shape=f'<p:sp>{nv(n["name"])}<p:spPr>{xfrm(n["x"],n["y"],n["w"],n["h"])}<a:prstGeom prst="{geom}"><a:avLst><a:gd name="adj" fmla="val 900"/></a:avLst></a:prstGeom>{fill(n["fill"])}{line(n.get("stroke"),n["strokeWidth"])}</p:spPr></p:sp>'
 elif t=='line':
  x1,y1,x2,y2=(n[k] for k in ['x1','y1','x2','y2'])
  attrs=('flipH="1" ' if x2<x1 else '')+('flipV="1"' if y2<y1 else '')
  shape=f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{sid+1}" name="Rule"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr>{xfrm(min(x1,x2),min(y1,y2),abs(x2-x1),abs(y2-y1),attrs)}<a:prstGeom prst="line"><a:avLst/></a:prstGeom>{line(n["stroke"],n["strokeWidth"],n.get("dash"))}</p:spPr></p:cxnSp>';sid+=1
 elif t=='image':shape=picture(n,base64.b64decode(n['data']))
 elif t=='math':
  el=mathnodes[i];x,y,w,h=[float(el.get(k)) for k in ['x','y','width','height']]
  el.attrib.pop('x',None);el.attrib.pop('y',None)
  vec=ET.tostring(el,encoding='utf-8',xml_declaration=True)
  sx=preview.width/1400;sy=preview.height/900
  fallback=preview.crop((round(x*sx),round(y*sy),round((x+w)*sx),round((y+h)*sy)))
  buf=io.BytesIO();fallback.save(buf,format='PNG')
  shape=picture(dict(x=x,y=y,w=w,h=h,name=n['name']),buf.getvalue(),vector=vec)
  (ROOT/'assets'/f'formula_{i}.svg').write_bytes(vec)
 elif t=='text':
  bold=n['weight']=='bold';italic=n.get('italic',False)
  fname='DejaVuSans-Bold.ttf' if bold else 'DejaVuSans-Oblique.ttf' if italic else 'DejaVuSans.ttf'
  if fname not in fonts:fonts[fname]=ImageFont.truetype(str(ROOT/'fonts'/fname),1000)
  f=fonts[fname];sz=n['size'];w=f.getlength(n['text'])/1000*sz+.4
  x=n['x']-w if n['align']=='right' else n['x']-w/2 if n['align']=='center' else n['x']
  y=n['y']-f.getmetrics()[0]/1000*sz
  fs=round(sz*72/25.4*100)
  shape=f'<p:sp>{nv(n["text"])}<p:spPr>{xfrm(x,y,w+2,sz*1.5)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/>{line()}</p:spPr><p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/><a:p><a:pPr><a:lnSpc><a:spcPct val="100000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="0"/></a:spcAft></a:pPr><a:r><a:rPr lang="en-US" sz="{fs}" b="{int(bold)}" i="{int(italic)}" dirty="0">{fill(n["fill"])}<a:latin typeface="DejaVu Sans"/><a:ea typeface="DejaVu Sans"/><a:cs typeface="DejaVu Sans"/></a:rPr><a:t xml:space="preserve">{escape(n["text"])}</a:t></a:r><a:endParaRPr sz="{fs}"/></a:p></p:txBody></p:sp>'
 else:raise ValueError(t)
 shapes.append(shape)
basegroup='<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
xml('ppt/slides/slide1.xml',f'<p:sld {NS}><p:cSld name="HUMOR 140 x 90 cm"><p:spTree>{basegroup}{"".join(shapes)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
def relationships(items):return f'<Relationships xmlns="{REL}">'+''.join(f'<Relationship Id="{rid}" Type="{R}/{typ}" Target="{target}"/>' for rid,target,typ in items)+'</Relationships>'
xml('ppt/slides/_rels/slide1.xml.rels',relationships([('rId1','../slideLayouts/slideLayout1.xml','slideLayout')]+rels))
xml('ppt/presentation.xml',f'<p:presentation {NS}><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst><p:sldSz cx="50400000" cy="32400000" type="custom"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle/></p:presentation>')
xml('ppt/_rels/presentation.xml.rels',relationships([('rId1','slideMasters/slideMaster1.xml','slideMaster'),('rId2','slides/slide1.xml','slide')]))
clr='<p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/>'
xml('ppt/slideMasters/slideMaster1.xml',f'<p:sldMaster {NS}><p:cSld><p:spTree>{basegroup}</p:spTree></p:cSld>{clr}<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>')
xml('ppt/slideMasters/_rels/slideMaster1.xml.rels',relationships([('rId1','../slideLayouts/slideLayout1.xml','slideLayout'),('rId2','../theme/theme1.xml','theme')]))
xml('ppt/slideLayouts/slideLayout1.xml',f'<p:sldLayout {NS} type="blank" preserve="1"><p:cSld name="Blank"><p:spTree>{basegroup}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
xml('ppt/slideLayouts/_rels/slideLayout1.xml.rels',relationships([('rId1','../slideMasters/slideMaster1.xml','slideMaster')]))
colors={'dk1':'1A3A4A','lt1':'FFFFFF','dk2':'293A43','lt2':'EEF6F3','accent1':'1A6B5A','accent2':'2C5AA0','accent3':'B06A0A','accent4':'566975','accent5':'D3DEE2','accent6':'FDF6EC','hlink':'2C5AA0','folHlink':'B06A0A'}
colorxml=''.join(f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k,v in colors.items())
fontxml=''.join(f'<a:{k}Font><a:latin typeface="DejaVu Sans"/><a:ea typeface=""/><a:cs typeface=""/></a:{k}Font>' for k in ['major','minor'])
# Standard complete style matrices, to keep the package compatible with Office.
solid='<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
ln=f'<a:ln w="9525" cap="flat" cmpd="sng" algn="ctr">{solid}<a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>'
xml('ppt/theme/theme1.xml',f'<a:theme xmlns:a="{A}" name="HUMOR"><a:themeElements><a:clrScheme name="HUMOR">{colorxml}</a:clrScheme><a:fontScheme name="DejaVu">{fontxml}</a:fontScheme><a:fmtScheme name="HUMOR"><a:fillStyleLst>{solid*3}</a:fillStyleLst><a:lnStyleLst>{ln*3}</a:lnStyleLst><a:effectStyleLst>{"<a:effectStyle><a:effectLst/></a:effectStyle>"*3}</a:effectStyleLst><a:bgFillStyleLst>{solid*3}</a:bgFillStyleLst></a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>')
xml('_rels/.rels',relationships([('rId1','ppt/presentation.xml','officeDocument')]))
overrides={'/ppt/presentation.xml':'presentation','/ppt/slides/slide1.xml':'slide','/ppt/slideMasters/slideMaster1.xml':'slideMaster','/ppt/slideLayouts/slideLayout1.xml':'slideLayout'}
ct='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Default Extension="svg" ContentType="image/svg+xml"/>'
ct+=''.join(f'<Override PartName="{p}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.{t}+xml"/>' for p,t in overrides.items())
ct+='<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/></Types>'
xml('[Content_Types].xml',ct)
for p,d in files.items():
 if p.endswith(('.xml','.rels')):ET.fromstring(d)
with zipfile.ZipFile(ROOT/'HUMOR-poster-editable.pptx','w',zipfile.ZIP_DEFLATED) as zf:
 for p,d in files.items():zf.writestr(p,d)
print(json.dumps({'output':str(ROOT/'HUMOR-poster-editable.pptx'),'size_cm':[140,90],'native_shapes':len(shapes),'editable_text_shapes':sum(n['type']=='text' for n in scene['nodes']),'vector_formulas':len(mathnodes),'xml_parts_valid':True},indent=2))
