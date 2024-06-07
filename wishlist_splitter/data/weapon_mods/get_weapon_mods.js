const puppeteer = require("puppeteer");
const fs = require("fs");

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });
  const page = await browser.newPage();

  const destinySetsUrl = "https://data.destinysets.com";
  const originTraits = `
  try {
    const result = $InventoryItem.filter(v => v.itemCategoryHashes.includes(WeaponModsOriginTraits));
    result;
  } catch (error) {
    console.error(error);
  }
  `;

  const frameMods = `
  try {
    const result = $InventoryItem.filter(v => v.itemCategoryHashes.includes(WeaponModsFrame));
    result;
  } catch (error) {
    console.error(error);
  }
  `;

  try {
    await page.goto(destinySetsUrl);

    // Promise to wait for Destiny data to load
    const waitForSelectorPromise = page.waitForSelector(
      "#root > div > div.styles_body__1L-Jq > div > div > a:nth-child(1)",
      { visible: true }
    );

    // Promise for timeout of 5 minutes. Stops script when done
    const timeoutPromise = new Promise((resolve, reject) => {
      setTimeout(() => {
        reject(new Error("Timeout occurred while waiting for selector"));
      }, 300000);
    });

    // Wait for the selector or timeout
    await Promise.race([waitForSelectorPromise, timeoutPromise]);

    // Execute the console command on the page
    const jsHandle = await page.evaluateHandle(originTraits);

    // You can now work with the jsHandle as needed
    const resultValue = await jsHandle.jsonValue();

    // Extract just the keys from the result object
    const resultKeys = Object.keys(resultValue);

    // Save the result keys to a text file
    fs.writeFileSync(
      "origin_traits.txt",
      JSON.stringify(resultKeys, null, 2),
      "utf-8"
    );
  } catch (error) {
    console.error(error);
  }
  // finally {
  //   await browser.close();
  // }
})();
