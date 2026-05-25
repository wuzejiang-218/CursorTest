/**
 * 使用本机 Chrome + 微软雅黑渲染 Mermaid，修复 PNG 中文显示为 ??? 的问题
 */
import puppeteer from "puppeteer-core";
import { readFileSync, writeFileSync, copyFileSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CHROME =
  process.env.CHROME_PATH ||
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const FONT_INIT = `%%{init: {"themeVariables": {"fontFamily": "Microsoft YaHei, SimHei, sans-serif", "fontSize": "14px"}}}%%`;

const FILES = [
  "01-overview",
  "02-domains",
  "03-risk-matrix",
  "04-timeline",
  "05-trace",
];

function withFontInit(source) {
  const s = source.trim();
  if (s.startsWith("%%{init:")) return s;
  return `${FONT_INIT}\n${s}`;
}

function buildPageHtml(mermaidSource) {
  const code = withFontInit(mermaidSource);
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <style>
    * { font-family: "Microsoft YaHei", "SimHei", "PingFang SC", sans-serif !important; }
    body { margin: 20px; background: #fff; }
    #wrap { display: inline-block; padding: 8px; }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11.4.0/dist/mermaid.min.js"></script>
</head>
<body>
  <div id="wrap"><pre class="mermaid"></pre></div>
  <script>
    const src = ${JSON.stringify(code)};
    document.querySelector(".mermaid").textContent = src;
    mermaid.initialize({
      startOnLoad: false,
      theme: "default",
      themeVariables: {
        fontFamily: "Microsoft YaHei, SimHei, sans-serif",
        fontSize: "14px"
      },
      flowchart: { htmlLabels: true, useMaxWidth: false },
      timeline: { useMaxWidth: false },
      securityLevel: "loose"
    });
    window.__mermaidLogs = [];
    mermaid.run({ nodes: document.querySelectorAll(".mermaid") }).then(() => {
      document.body.dataset.ready = "1";
    }).catch(e => {
      window.__mermaidLogs.push(e.message || String(e));
      document.body.dataset.error = String(e);
    });
  </script>
</body>
</html>`;
}

async function renderOne(page, name) {
  const mmdPath = join(__dirname, `${name}.mmd`);
  const pngPath = join(__dirname, `${name}.png`);
  const source = readFileSync(mmdPath, "utf8");

  await page.setContent(buildPageHtml(source), {
    waitUntil: "domcontentloaded",
    timeout: 90000,
  });

  await page.waitForFunction(
    () => typeof window.mermaid !== "undefined",
    { timeout: 60000 }
  );

  await page.waitForFunction(
    () =>
      document.body.dataset.ready === "1" || document.body.dataset.error,
    { timeout: 90000 }
  );

  const err = await page.evaluate(() => document.body.dataset.error);
  if (err) {
    const logs = await page.evaluate(() =>
      (window.__mermaidLogs || []).join("\n")
    );
    throw new Error(`${name}: ${err}\n${logs}`);
  }

  await page.waitForSelector("#wrap svg", { timeout: 15000 });
  const wrap = await page.$("#wrap");
  await wrap.screenshot({ path: pngPath, type: "png" });
  console.log(`OK ${pngPath}`);
}

async function main() {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  for (const name of FILES) {
    const p = await browser.newPage();
    await p.setViewport({ width: 2400, height: 1800, deviceScaleFactor: 2 });
    p.setDefaultNavigationTimeout(90000);
    p.setDefaultTimeout(90000);
    try {
      await renderOne(p, name);
    } catch (e) {
      console.error(`Retry ${name}...`, e.message);
      await renderOne(p, name);
    }
    await p.close();
  }

  await browser.close();

  console.log(`Rendered PNG/MMD in ${__dirname}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
