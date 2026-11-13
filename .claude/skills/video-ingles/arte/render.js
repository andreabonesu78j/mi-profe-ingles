// Convierte SVG en PNG (fondo transparente) con el Chromium de Playwright.
// Uso: node render.js <carpeta_con_svg> [carpeta_png]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dirIn = path.resolve(process.argv[2]);
  const dirOut = path.resolve(process.argv[3] || dirIn);
  fs.mkdirSync(dirOut, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  const files = fs.readdirSync(dirIn).filter((f) => f.endsWith('.svg'));
  for (const f of files) {
    const svg = fs.readFileSync(path.join(dirIn, f), 'utf8');
    const w = parseInt(svg.match(/width="(\d+)"/)[1], 10);
    const h = parseInt(svg.match(/height="(\d+)"/)[1], 10);
    await page.setViewportSize({ width: w, height: h });
    await page.setContent(
      `<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    await page.screenshot({
      path: path.join(dirOut, f.replace(/\.svg$/, '.png')),
      omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  }
  await browser.close();
  console.log(`OK ${files.length} PNG en ${dirOut}`);
})();
