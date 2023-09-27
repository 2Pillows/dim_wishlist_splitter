// script.js

// Holds selected checkboxes
const selectedFilters = {
  include: [],
  exclude: [],
};

// Fetch JSON data and add checkboxes to sections
fetch("data/config.json")
  .then((response) => response.json())
  .then((data) => {
    // Create checkboxes
    function createCheckbox(checkboxData, sectionName) {
      const container = document.createElement("div");

      // Unique ID for associated label clicking
      const checkboxId = `${sectionName}-checkbox-${checkboxData.tag}`;

      // Create checkbox
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.id = checkboxId;
      checkbox.name = `${sectionName}-checkbox-${checkboxData.tag}`;
      checkbox.value = checkboxData.tag;

      // Create label
      const label = document.createElement("label");
      label.htmlFor = checkboxId;
      label.textContent = checkboxData.label;

      // Add listener for clicking checkbox
      checkbox.addEventListener("change", function () {
        updateCheckboxState(this);
      });

      container.appendChild(checkbox);
      container.appendChild(label);
      return container;
    }

    // Listener for updating checkbox state
    function updateCheckboxState(checkbox) {
      // Unselected checkbox
      if (checkbox.readOnly) {
        checkbox.checked = checkbox.readOnly = false;

        selectedFilters.include = selectedFilters.include.filter(
          (item) => item !== checkbox.value
        );
        selectedFilters.exclude = selectedFilters.exclude.filter(
          (item) => item !== checkbox.value
        );
      }
      // Exclude checkbox
      else if (!checkbox.checked) {
        checkbox.readOnly = checkbox.indeterminate = true;

        selectedFilters.include = selectedFilters.include.filter(
          (item) => item !== checkbox.value
        );
        selectedFilters.exclude.push(checkbox.value);
      }
      // Include checkbox
      else if (checkbox.checked) {
        checkbox.readOnly = checkbox.indeterminate = false;

        selectedFilters.include.push(checkbox.value);
        selectedFilters.exclude = selectedFilters.exclude.filter(
          (item) => item !== checkbox.value
        );
      }

      // Update URLs after a checkbox has been clicked
      updateWishlistUrls();
    }

    // Sections for type of checkboxes
    const sections = ["input", "gamemode", "author", "misc"];
    // Add checkboxes to each section
    sections.forEach((sectionName) => {
      const section = document.getElementById(`${sectionName}-checkboxes`);
      if (data[sectionName] && data[sectionName].checkboxes) {
        data[sectionName].checkboxes.forEach((checkboxData) => {
          const checkboxContainer = createCheckbox(checkboxData, sectionName);
          section.appendChild(checkboxContainer);
        });
      }
    });

    // Update URLs after a checkbox has been clicked
    function updateWishlistUrls() {
      // Clear URLs
      const urlsList = document.getElementById("urls-list");
      while (urlsList.firstChild) {
        urlsList.removeChild(urlsList.firstChild);
      }

      // Display wishlists that fufill checkboxes
      data.wishlists.urls.forEach((url) => {
        // Check if URL tags meet exclude and include conditions from checkboxes
        excludeFound = false;
        includeFound = true;
        for (let i = 0; i < selectedFilters.exclude.length; i++) {
          if (url.tag.includes(selectedFilters.exclude[i])) {
            excludeFound = true;
          }
        }
        for (let i = 0; i < selectedFilters.include.length; i++) {
          if (!url.tag.includes(selectedFilters.include[i])) {
            includeFound = false;
          }
        }

        // Add URL if meets conditions
        if (includeFound && !excludeFound) {
          const listItem = document.createElement("li");
          const textSpan = document.createElement("span");
          textSpan.textContent = url.label;

          // Add click listener
          textSpan.addEventListener("click", function () {
            // Copy URL to clipboard
            const textarea = document.createElement("textarea");
            textarea.value = url.link;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand("copy");
            document.body.removeChild(textarea);

            // Alert user that URL is copied
            openCustomAlert("URL copied to clipboard: " + textarea.value);
          });

          listItem.appendChild(textSpan);
          urlsList.appendChild(listItem);
        }
      });
    }

    // Initial call to get wishlists
    updateWishlistUrls();
  })
  .catch((error) => console.error("Error fetching JSON:", error));

// Custom alert
function openCustomAlert(message) {
  const alertMessage = document.getElementById("alert-message");
  alertMessage.textContent = message;
  const customAlert = document.querySelector(".custom-alert");
  customAlert.style.display = "flex";
}

// Close custom alert
function closeCustomAlert() {
  const customAlert = document.querySelector(".custom-alert");
  customAlert.style.display = "none";
}
