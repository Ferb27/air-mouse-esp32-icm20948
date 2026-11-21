// Công cụ tùy chọn: dùng trình duyệt và Playwright đã có, không tải/cài gói.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
async function main() {
  const executable = process.argv[2];
  if (!executable) throw new Error('Cần truyền đường dẫn trình duyệt Chromium/Edge đã có.');
  const { chromium } = require(process.argv[3] || 'playwright');
  const root = path.resolve(__dirname, '..');
  const figures = JSON.parse(fs.readFileSync(path.join(__dirname, 'du_lieu_hinh.json'), 'utf8')).figures;
  const browser = await chromium.launch({ executablePath: executable, headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 3 });
    const remoteRequests = [];
    await page.route(/^https?:/, route => { remoteRequests.push(route.request().url()); return route.abort(); });
    const checks = [];
    for (const [name] of figures) {
      await page.goto(pathToFileURL(path.join(root, 'hinh', name + '.svg')).href);
      await page.evaluate(() => document.fonts.ready);
      const outside = await page.evaluate(() => {
        const svg = document.querySelector('svg');
        const v = svg.viewBox.baseVal;
        return [...svg.querySelectorAll('text')].flatMap(t => {
          const b = t.getBBox();
          return b.x < -0.5 || b.y < -0.5 || b.x + b.width > v.width + 0.5 || b.y + b.height > v.height + 0.5
            ? [{ text: t.textContent, x: b.x, y: b.y, width: b.width, height: b.height }] : [];
        });
      });
      await page.locator('svg').screenshot({ path: path.join(root, 'hinh', name + '.png') });
      checks.push({ name, outside });
    }
    await page.goto(pathToFileURL(path.join(root, 'hinh', '00_TONG_HOP_HINH.html')).href);
    const htmlSvgCount = await page.locator('section svg').count();
    await page.locator('section').first().screenshot({ path: path.join(root, 'tools', 'kiem_tra_html.png') });
    const report = { png_count: checks.length, html_svg_count: htmlSvgCount, remote_requests: remoteRequests.length, checks };
    fs.writeFileSync(path.join(root, 'tools', 'kiem_tra_trinh_duyet.json'), JSON.stringify(report, null, 2));
    console.log(JSON.stringify(report));
    if (checks.some(c => c.outside.length) || remoteRequests.length || htmlSvgCount !== 12) process.exitCode = 1;
  } finally { await browser.close(); }
}
main().catch(e => { console.error(e.message); process.exitCode = 1; });
