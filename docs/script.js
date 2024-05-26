// script.js

// Holds selected checkboxes
var selectedFilters = {
  include: [],
  exclude: [],
};

const baseLink =
  "https://raw.githubusercontent.com/2Pillows/dim_wishlist_splitter/main/wishlists/";

const wishlists = [
  {
    label: "All Rolls",
    tags: "mkb_ctr_pve_pvp",
    link: "all.txt",
  },
  {
    label: "PvE",
    tags: "pve_mkb_ctr",
    link: "pve.txt",
  },
  {
    label: "PvP",
    tags: "pvp_mkb_ctr",
    link: "pvp.txt",
  },
  {
    label: "MKB",
    tags: "mkb_pve_pvp",
    link: "mkb.txt",
  },
  {
    label: "CTR",
    tags: "ctr_pvp_pve",
    link: "ctr.txt",
  },
  {
    label: "MKB_Perks",
    tags: "mkb_perks_pve_pvp",
    link: "mkb_perks.txt",
  },
  {
    label: "CTR_Perks",
    tags: "ctr_perks_pve_pvp",
    link: "ctr_perks.txt",
  },
  {
    label: "MKB_Perks_Dupes",
    tags: "mkb_perks_dupes_pve_pvp",
    link: "mkb_perks_dupes.txt",
  },
  {
    label: "CTR_Perks_Dupes",
    tags: "ctr_perks_dupes_pve_pvp",
    link: "ctr_perks_dupes.txt",
  },
  {
    label: "MKB_PvE",
    tags: "mkb_pve",
    link: "mkb_pve.txt",
  },
  {
    label: "MKB_PvP",
    tags: "mkb_pvp",
    link: "mkb_pvp.txt",
  },
  {
    label: "CTR_PvE",
    tags: "ctr_pve",
    link: "ctr_pve.txt",
  },
  {
    label: "CTR_PvP",
    tags: "ctr_pvp",
    link: "ctr_pvp.txt",
  },
  {
    label: "Panda",
    tags: "panda_mkb_ctr_pve_pvp",
    link: "panda.txt",
  },
  {
    label: "Panda_MKB",
    tags: "mkb_panda_pve_pvp",
    link: "mkb_panda.txt",
  },
  {
    label: "Panda_MKB_PvE",
    tags: "mkb_panda_pve",
    link: "mkb_panda_pve.txt",
  },
  {
    label: "Panda_MKB_PvP",
    tags: "mkb_panda_pvp",
    link: "mkb_panda_pvp.txt",
  },
  {
    label: "Panda_CTR",
    tags: "ctr_panda_pve_pvp",
    link: "ctr_panda.txt",
  },
  {
    label: "Panda_CTR_PvE",
    tags: "ctr_panda_pve",
    link: "ctr_panda_pve.txt",
  },
  {
    label: "Panda_CTR_PvP",
    tags: "ctr_panda_pvp",
    link: "ctr_panda_pvp.txt",
  },
  {
    label: "Panda_MKB_Perks",
    tags: "mkb_panda_perks_pve_pvp",
    link: "mkb_panda_perks.txt",
  },
  {
    label: "MKB_God",
    tags: "mkb_god_pve_pvp",
    link: "mkb_god.txt",
  },
  {
    label: "MKB_!Backups",
    tags: "mkb_!backup_pve_pvp",
    link: "mkb_!backup.txt",
  },
  {
    label: "MKB_!Backups_Perks",
    tags: "mkb_!backup_perks_pve_pvp",
    link: "mkb_!backup_perks.txt",
  },
  {
    label: "MKB_!Backups_Perks_Dupes",
    tags: "mkb_!backup_perks_dupes_pve_pvp",
    link: "mkb_!backup_perks_dupes.txt",
  },
  {
    label: "MKB_PvE_!Backups_Perks",
    tags: "mkb_pve_!backup_perks_pve_pvp",
    link: "mkb_pve_!backup_perks.txt",
  },
  {
    label: "MKB_PvE_!Backups_Perks_Dupes",
    tags: "mkb_pve_!backup_perks_dupes_pve_pvp",
    link: "mkb_pve_!backup_perks_dupes.txt",
  },
  {
    label: "CTR_God",
    tags: "ctr_god_pve_pvp",
    link: "ctr_god.txt",
  },
  {
    label: "CTR_!Backups",
    tags: "ctr_!backup_pve_pvp",
    link: "ctr_!backup.txt",
  },
  {
    label: "CTR_!Backups_Perks",
    tags: "ctr_!backup_perks_pve_pvp",
    link: "ctr_!backup_perks.txt",
  },
  {
    label: "CTR_!Backups_Perks_Dupes",
    tags: "ctr_!backup_perks_dupes_pve_pvp",
    link: "ctr_!backup_perks_dupes.txt",
  },
];

// Setup onClick for buttons
function setupButtons() {
  const filterButtons = document.querySelectorAll(".filter-button");

  // Set onclick to change state of button and update wishlists
  filterButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // tag for btn
      let btn_option = button.id.split("-btn")[0];

      // add to include
      if (button.classList.contains("default-btn")) {
        button.classList.remove("default-btn");
        button.classList.add("include-btn");
        selectedFilters.include.push(btn_option);
      }
      // add to exclude, remove from include
      else if (button.classList.contains("include-btn")) {
        button.classList.remove("include-btn");
        button.classList.add("exclude-btn");
        selectedFilters.exclude.push(btn_option);
        selectedFilters.include = selectedFilters.include.filter(
          (i) => i !== btn_option
        );
      }
      // remove from exclude
      else if (button.classList.contains("exclude-btn")) {
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
  const wishlistContainer = document.getElementById("wishlist-container");
  wishlistContainer.innerHTML = "";
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
      wishlistLink.href = baseLink + wishlist.link;
      wishlistLink.textContent = baseLink + wishlist.link;

      wishlistDiv.appendChild(wishlistTitle);
      wishlistDiv.appendChild(wishlistLink);

      wishlistContainer.appendChild(wishlistDiv);
    }
  });
}

function setupPage() {
  setupButtons();
  updateWishlists();
}

setupPage();
