// script.js

async function wishlistsMain() {
  // Text file with json dump array of wishlist paths
  const wishlistPathsPath = "data/wishlist_names.txt";

  // Holds selected checkboxes
  var selectedFilters = {
    include: [],
    exclude: [],
  };

  // Base url for raw wishlist files, requires /wishlists/file_name.txt
  const baseLink =
    "https://raw.githubusercontent.com/2Pillows/dim_wishlist_splitter/main";

  // Get array of wishlist paths
  const wishlistPaths = await (async () => {
    try {
      const response = await fetch(wishlistPathsPath);

      return response.json();
    } catch (error) {
      console.error("Wishlist Paths Fetch Error:", error);
      return null;
    }
  })();

  // Convert wishlist paths to label name, tags, and raw url
  const wishlists = await Promise.all(
    wishlistPaths.map(async (wishlistPaths) => {
      fileName = wishlistPaths.replace("./wishlists/", "").replace(".txt", "");

      // Create labels for lists based off file name
      let label = fileName;

      // Remove _
      label = label.replace(/_/g, " ");

      // Make labels prettier
      const labelReplacements = {
        all: "All Rolls",
        mkb: "MKB",
        ctr: "CTR",
        pve: "PvE",
        pvp: "PvP",
        pandapaxxy: "PandaPaxxy",
        god: "God",
        "!backups": "!Backups",
        perks: "Perks",
        dupes: "Dupes",
      };
      for (const [key, value] of Object.entries(labelReplacements)) {
        label = label.replace(key, value);
      }

      // Create tags for lists based off file name
      let tags = fileName;

      // Add PvE or PvP if neither is found
      if (!tags.includes("pve") && !tags.includes("pvp")) {
        tags += "_pve_pvp";
      }

      // add MKB or CTR if neither is found
      if (!tags.includes("mkb") && !tags.includes("ctr")) {
        tags += "_mkb_ctr";
      }

      // Add baselink to path for website URL
      let link = wishlistPaths.replace(".", baseLink);

      // Return dict with label, tags, link
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

      // Add button if it should be included and not excluded
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

  // Add listeners for buttons
  setupButtons();
  // Fist loop for wishlists
  updateWishlists();
}

function faviconMain() {
  // Favicon element
  const faviconElement = document.getElementById("favicon");

  // Function to set the favicon based on the color scheme
  function setFavicon() {
    // Check if the current mode is dark or light
    const isDarkMode = window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;

    // If darkMode use white, otherwise dark
    faviconElement.href = isDarkMode
      ? "icons/github-mark-white.png"
      : "icons/github-mark.png";
  }

  // Listener for scheme changes
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", setFavicon);
}

// Main function for wishlists
wishlistsMain();

// Main function for favicon based on color scheme
faviconMain();
