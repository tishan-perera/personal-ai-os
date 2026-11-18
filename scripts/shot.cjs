const puppeteer = require(process.env.PUPPETEER_CORE);
const fileUrl = process.argv[2];
const outPath = process.argv[3];
const selector = process.argv[4] || "body";
const width = Number(process.argv[5] || "960");

(async () => {
  const browser = await puppeteer.launch({
    executablePath: process.env.CHROME_PATH || "/usr/local/bin/google-chrome",
    headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars", "--font-render-hinting=none"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width, height: 800, deviceScaleFactor: 1 });
  await page.goto(fileUrl, { waitUntil: "networkidle0" });
  await page.evaluate(() => document.fonts.ready);
  const element = await page.$(selector);
  if (!element) {
    throw new Error("missing selector " + selector);
  }
  await element.screenshot({ path: outPath });
  await browser.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
