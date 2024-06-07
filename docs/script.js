// script.js

async function main() {
  // Get wishlists paths
  const wishlist_paths_path = "/docs/data/wishlist_names.txt";

  // Holds selected checkboxes
  var selectedFilters = {
    include: [],
    exclude: [],
  };

  const baseLink =
    "https://raw.githubusercontent.com/2Pillows/dim_wishlist_splitter/main";

  const wishlist_paths = await (async () => {
    try {
      const response = await fetch(wishlist_paths_path);

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      return await response.json();
    } catch (error) {
      console.error("Wishlist Paths Fetch Error:", error);
      return null;
    }
  })();

  const wishlists = await Promise.all(
    wishlist_paths.map(async (wishlist_path) => {
      file_name = wishlist_path.replace("./wishlists/", "").replace(".txt", "");

      // Convert file path to case sensitive name
      let label = file_name;

      label = label.replace(/_/g, " ");

      label = label.replace("all", "All Rolls");
      label = label.replace("mkb", "MKB");
      label = label.replace("ctr", "CTR");
      label = label.replace("pve", "PvE");
      label = label.replace("pvp", "PvP");
      label = label.replace("pandapaxxy", "PandaPaxxy");
      label = label.replace("god", "God");
      label = label.replace("!backups", "!Backups");
      label = label.replace("perks", "Perks");
      label = label.replace("dupes", "Dupes");

      // Get tags based on name
      let tags = file_name;

      // Add PvE or PvP if neither is found
      if (!tags.includes("pve") && !tags.includes("pvp")) {
        tags += "_pve_pvp";
      }

      // add MKB or CTR if neither is found
      if (!tags.includes("mkb") && !tags.includes("ctr")) {
        tags += "_mkb_ctr";
      }

      // Use file path and replace starting directory with baseLink
      let link = wishlist_path.replace(".", baseLink);

      return {
        label: label,
        tags: tags,
        link: link,
      };
    })
  );

  // Setup onClick for buttons
  function setupButtons() {
    const filterButtons = document.querySelectorAll(".filter-button");

    // Set onclick to change state of button and update wishlists
    filterButtons.forEach((button) => {
      button.addEventListener("click", function () {
        // tag for btn
        let btn_option = button.id.replace("-btn", "");

        // set button to include state
        if (button.classList.contains("default-btn")) {
          // change from default to include
          button.classList.remove("default-btn");
          button.classList.add("include-btn");
          selectedFilters.include.push(btn_option);
        }
        // set button to exclude state
        else if (button.classList.contains("include-btn")) {
          // change from include to exclude
          button.classList.remove("include-btn");
          button.classList.add("exclude-btn");
          selectedFilters.exclude.push(btn_option);
          selectedFilters.include = selectedFilters.include.filter(
            (i) => i !== btn_option
          );
        }
        // set btn to default state
        else if (button.classList.contains("exclude-btn")) {
          // change from exclude to default
          button.classList.remove("exclude-btn");
          button.classList.add("default-btn");
          selectedFilters.exclude = selectedFilters.exclude.filter(
            (i) => i !== btn_option
          );
        }

        // update wishlists
        updateWishlists();
      });
    });
  }

  // Add wishlists to wishlist-selection
  function updateWishlists() {
    // Remove all wishlists in html
    const wishlistContainer = document.getElementById("wishlist-container");
    wishlistContainer.innerHTML = "";

    // Loop through dict and add valid lists
    wishlists.forEach((wishlist) => {
      // Exclude is false if wishlist doesn't have filter
      let include = true;
      selectedFilters.include.forEach((includeTag) => {
        if (!wishlist.tags.includes(includeTag)) {
          include = false;
          return;
        }
      });

      // Exclude is true if wishlist has exclude
      let exclude = false;
      selectedFilters.exclude.forEach((excludeTag) => {
        if (wishlist.tags.includes(excludeTag)) {
          exclude = true;
          return;
        }
      });

      if (include && !exclude) {
        let wishlistDiv = document.createElement("div");
        wishlistDiv.classList.add("wishlist-text");

        let wishlistTitle = document.createElement("span");
        wishlistTitle.classList.add("wishlist-title");
        wishlistTitle.textContent = wishlist.label + ": ";

        let wishlistLink = document.createElement("a");
        wishlistLink.classList.add("wishlist-link");
        wishlistLink.href = wishlist.link;
        wishlistLink.textContent = wishlist.link;

        wishlistDiv.appendChild(wishlistTitle);
        wishlistDiv.appendChild(wishlistLink);

        wishlistContainer.appendChild(wishlistDiv);
      }
    });
  }

  setupButtons();
  updateWishlists();
}

// Function to set the favicon based on the color scheme
function setFavicon() {
  // Get the favicon link element
  const faviconLink = document.getElementById("favicon");

  // Check if the current mode is dark or light
  const isDarkMode =
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;

  // Set the href of the favicon based on the mode
  if (isDarkMode) {
    // Dark mode
    faviconLink.href = "icons/github-mark-white.png";
  } else {
    // Light mode
    faviconLink.href = "icons/github-mark.png";
  }
}
setFavicon();

// Listen for changes in the color scheme (light/dark mode)
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", setFavicon);

main();
