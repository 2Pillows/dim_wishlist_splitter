const puppeteer = require("puppeteer");
const fs = require("fs");

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
  });
  const page = await browser.newPage();

  const destinySetsUrl = "https://data.destinysets.com";
  const consoleCommand = `
    try {
      const result = $InventoryItem.filter(v => v.itemCategoryHashes.includes(WeaponModsOriginTraits));
      result;
    } catch (error) {
      console.error(error);
    }
  `;

  try {
    await page.goto(destinySetsUrl);

    // Wait for Destiny data to load
    await page.waitForSelector(
      "#root > div > div.styles_body__1L-Jq > div > div > a:nth-child(1)",
      { visible: true }
    );

    // Execute the console command on the page
    const jsHandle = await page.evaluateHandle(consoleCommand);

    // You can now work with the jsHandle as needed
    const resultValue = await jsHandle.jsonValue();

    // Extract just the keys from the result object
    const resultKeys = Object.keys(resultValue);

    // Save the result keys to a text file
    fs.writeFileSync(
      "./wishlist_splitter/data/origin_traits/origin_traits.txt",
      JSON.stringify(resultKeys, null, 2),
      "utf-8"
    );
    await browser.close();
  } catch (error) {
    console.error(error);
  }
})();
