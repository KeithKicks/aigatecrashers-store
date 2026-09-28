// Shrink a screenshot PNG to a 256-colour palette PNG (about 4x smaller).
// Used by scripts/gen_og_images.py. Needs `npm install` once (pngjs, upng-js).
//   node scripts/og_quantize.js in.png out.png [colors]
const fs = require('fs');
const { PNG } = require('pngjs');
const UPNG = require('upng-js');

const [, , inp, out, colors] = process.argv;
if (!inp || !out) {
  console.error('usage: node scripts/og_quantize.js in.png out.png [colors]');
  process.exit(2);
}
const png = PNG.sync.read(fs.readFileSync(inp));
const rgba = png.data.buffer.slice(png.data.byteOffset, png.data.byteOffset + png.data.byteLength);
const encoded = UPNG.encode([rgba], png.width, png.height, parseInt(colors || '256', 10));
fs.writeFileSync(out, Buffer.from(encoded));
