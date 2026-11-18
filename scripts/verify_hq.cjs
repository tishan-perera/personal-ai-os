const puppeteer = require(process.env.PUPPETEER_CORE);

(async () => {
  const browser = await puppeteer.launch({
    executablePath: process.env.CHROME_PATH || "/usr/local/bin/google-chrome",
    headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  });
  const page = await browser.newPage();
  await page.goto(process.argv[2], { waitUntil: "networkidle0" });
  const expected = {
    all: 22,
    working: 0,
    waiting: 0,
    pending: 1,
    closed: 2,
    not_published: 18,
  };
  const result = await page.evaluate(async (expectedCounts) => {
    const buttons = Array.from(document.querySelectorAll("[data-filter]"));
    const rows = () => Array.from(document.querySelectorAll("tbody tr"));
    const visible = () => rows().filter((row) => !row.hidden).length;
    const empty = document.getElementById("empty");
    const problems = [];
    const text = document.body.innerText;
    ["Illustrative mock", "Amanda", "Credit", "Trading", "Parked", "Blocked-on-owner"].forEach((needle) => {
      if (!text.includes(needle)) problems.push("missing text " + needle);
    });
    for (const [name, count] of Object.entries(expectedCounts)) {
      const button = buttons.find((item) => item.getAttribute("data-filter") === name);
      button.click();
      await new Promise((resolve) => setTimeout(resolve, 20));
      const shown = visible();
      if (shown !== count) problems.push(name + " showed " + shown + " expected " + count);
      const emptyShown = !empty.hidden;
      if ((count === 0) !== emptyShown) problems.push(name + " empty-state mismatch");
    }
    return problems;
  }, expected);
  await browser.close();
  if (result.length) {
    console.error(result.join("\n"));
    process.exit(1);
  }
  console.log("hq filters passed");
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
