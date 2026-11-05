from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
svg=(ROOT/'HUMOR-poster-editable.svg').read_text()
page=(ROOT/'source/viewer_template.html').read_text().replace('%%POSTER_SVG%%',svg)
(ROOT/'HUMOR-poster.html').write_text(page)
print('Built',ROOT/'HUMOR-poster.html')
