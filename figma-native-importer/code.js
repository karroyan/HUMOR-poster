// Offline scene importer. Coordinates are millimetres in the source scene.
figma.showUI(__html__, { width: 440, height: 310 });
const S = 96 / 25.4;
function color(hex) {
  if (!/^#[0-9a-fA-F]{6}$/.test(hex || '')) throw new Error('Invalid color: ' + hex);
  return { r: parseInt(hex.slice(1, 3), 16) / 255, g: parseInt(hex.slice(3, 5), 16) / 255, b: parseInt(hex.slice(5, 7), 16) / 255 };
}
function paint(hex) { return [{ type: 'SOLID', color: color(hex) }]; }
function decode64(data) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
  const raw = data.replace(/^data:[^;]+;base64,/, '').replace(/\s/g, '');
  if (!/^[A-Za-z0-9+/]*={0,2}$/.test(raw) || raw.length % 4) throw new Error('Invalid base64 image');
  const out = [];
  let bits = 0, buffer = 0;
  for (const ch of raw) {
    if (ch === '=') break;
    buffer = (buffer << 6) | chars.indexOf(ch); bits += 6;
    if (bits >= 8) { bits -= 8; out.push((buffer >> bits) & 255); }
  }
  return new Uint8Array(out);
}
async function fonts() {
  for (const family of ['Arial', 'Inter']) {
    try {
      const regular = { family, style: 'Regular' }, bold = { family, style: 'Bold' };
      await figma.loadFontAsync(regular); await figma.loadFontAsync(bold);
      return { regular, bold, family };
    } catch (_) { /* Try the next installed family. */ }
  }
  throw new Error('Neither Arial nor Inter is available. Install either font and retry.');
}
figma.ui.onmessage = async (message) => {
  if (message.type !== 'import') return;
  let frame;
  try {
    const scene = message.scene;
    if (!scene || scene.width !== 1400 || scene.height !== 900 || !Array.isArray(scene.nodes)) throw new Error('Expected a 1400 × 900 mm poster scene.');
    const font = await fonts();
    frame = figma.createFrame();
    frame.name = 'HUMOR — NeurIPS 2026 — 140 × 90 cm';
    frame.resize(scene.width * S, scene.height * S);
    frame.fills = paint('#FFFFFF'); frame.clipsContent = true;
    const center = figma.viewport.center;
    frame.x = center.x - frame.width / 2; frame.y = center.y - frame.height / 2;
    for (const n of scene.nodes) {
      let node;
      if (n.type === 'text') {
        node = figma.createText();
        node.fontName = n.weight === 'bold' ? font.bold : font.regular;
        node.fontSize = n.size * S;
        node.textAutoResize = 'WIDTH_AND_HEIGHT';
        node.characters = String(n.text);
        node.fills = paint(n.fill || '#000000');
        node.textAlignHorizontal = (n.align || 'left').toUpperCase();
        node.x = n.x * S;
        if (n.align === 'center') node.x -= node.width / 2;
        if (n.align === 'right') node.x -= node.width;
        // SVG source stores baseline y; Figma stores top of text box.
        node.y = (n.y - n.size * 0.905) * S;
      } else if (n.type === 'line') {
        node = figma.createLine();
        const dx = n.x2 - n.x1, dy = n.y2 - n.y1;
        node.resize(Math.max(0.01, Math.sqrt(dx * dx + dy * dy) * S), 0);
        node.rotation = -Math.atan2(dy, dx) * 180 / Math.PI;
        node.x = n.x1 * S; node.y = n.y1 * S;
        node.strokes = paint(n.stroke || '#000000');
        node.strokeWeight = (n.strokeWidth || 1) * S;
      } else if (n.type === 'rect' || n.type === 'image') {
        node = figma.createRectangle();
        node.resize(n.w * S, n.h * S);
        node.x = n.x * S; node.y = n.y * S;
        if (n.type === 'image') {
          const image = figma.createImage(decode64(n.data));
          node.fills = [{ type: 'IMAGE', imageHash: image.hash, scaleMode: 'FILL' }];
        } else {
          node.fills = n.fill ? paint(n.fill) : [];
          node.cornerRadius = (n.radius || 0) * S;
          if (n.stroke) { node.strokes = paint(n.stroke); node.strokeWeight = (n.strokeWidth || 1) * S; }
        }
      } else { throw new Error('Unsupported node type: ' + n.type); }
      frame.appendChild(node);
      node.name = (n.section ? n.section + ' / ' : '') + (n.name || n.type);
    }
    figma.currentPage.selection = [frame];
    figma.viewport.scrollAndZoomIntoView([frame]);
    figma.ui.postMessage({ type: 'success', count: scene.nodes.length, font: font.family });
    figma.notify('Poster imported as editable layers. Check text placement before printing.');
  } catch (err) {
    if (frame) frame.remove();
    figma.ui.postMessage({ type: 'error', message: String(err.message || err) });
  }
};
