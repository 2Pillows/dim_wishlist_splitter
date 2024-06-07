const puppeteer = require("puppeteer");
const fs = require("fs");

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
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

    // Get origin traits
    const originTraitsHandle = await page.evaluateHandle(originTraits);
    const originTraitsValue = await originTraitsHandle.jsonValue();
    const originTraitKeys = Object.keys(originTraitsValue);

    // Write origin traits
    fs.writeFileSync(
      "./wishlist_splitter/data/weapon_mods/origin_traits.txt",
      JSON.stringify(originTraitKeys, null, 2),
      "utf-8"
    );

    // Get weapon mods, 3rd and 4th column
    const frameModsHandle = await page.evaluateHandle(frameMods);
    const frameModsValue = await frameModsHandle.jsonValue();
    const frameModsKeys = Object.keys(frameModsValue);

    // Write frame mods
    fs.writeFileSync(
      "./wishlist_splitter/data/weapon_mods/frame_mods.txt",
      JSON.stringify(frameModsKeys, null, 2),
      "utf-8"
    );
  } catch (error) {
    console.error(error);
  } finally {
    await browser.close();
    process.exit();
  }
})();
