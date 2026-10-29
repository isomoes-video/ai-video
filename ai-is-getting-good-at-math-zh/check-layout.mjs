import puppeteer from 'puppeteer-core';
import {readFile, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';

const base = new URL('./', import.meta.url);
const timeline = JSON.parse(await readFile(new URL('video-work/timeline.json', base), 'utf8'));
const browser = await puppeteer.launch({executablePath: '/usr/bin/chromium', headless: true, args: ['--no-sandbox', '--allow-file-access-from-files']});
const checks = [];
try {
  const page = await browser.newPage();
  await page.setViewport({width: 1920, height: 1080});
  await page.goto(new URL('video-work/index.html', base).href, {waitUntil: 'domcontentloaded', timeout: 30000});
  await page.waitForFunction(() => Boolean(window.__timelines?.md2video), {timeout: 30000});
  await page.evaluate(async () => { await document.fonts.ready; return true; });
  for (const scene of timeline.scenes) {
    const seconds = scene.from / timeline.fps + Math.min(5, scene.narrationFrames / timeline.fps / 2);
    await page.evaluate((time) => { window.__timelines.md2video.seek(time); }, seconds);
    const issues = await page.evaluate((number) => {
      const root = document.querySelector(`#scene-${number}`);
      return [...root.querySelectorAll('h1, .subtitle, .model, .bullet, pre, blockquote, .caption')]
        .filter((el) => getComputedStyle(el).opacity !== '0')
        .flatMap((el) => {
          const box = el.getBoundingClientRect();
          return box.left < 0 || box.right > 1920 || box.top < 0 || box.bottom > 1080 || el.scrollWidth > el.clientWidth + 2
            ? [{text: el.textContent, bounds: box.toJSON()}] : [];
        });
    }, scene.slide_number);
    checks.push({slide: scene.slide_number, issues});
    if ([1, 6, 9, 12].includes(scene.slide_number)) {
      await page.screenshot({path: fileURLToPath(new URL(`video-work/review-${scene.slide_number}.png`, base))});
    }
  }
} finally {
  await browser.close();
}
await writeFile(new URL('video-work/layout-check.json', base), JSON.stringify(checks, null, 2));
console.log(JSON.stringify(checks, null, 2));
if (checks.some((check) => check.issues.length)) process.exitCode = 1;
