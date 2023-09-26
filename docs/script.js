// script.js

const selectedFilters = {
  include: [],
  exclude: [],
};

// Fetch JSON data and add checkboxes to sections
fetch("data/config.json")
  .then((response) => response.json())
  .then((data) => {
    // Function to create a checkbox element with label
    function createCheckbox(checkboxData, sectionName, tag) {
      const container = document.createElement("div");
      const checkboxId = `${sectionName}-checkbox-${checkboxData.tag}`;
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.id = checkboxId;
      checkbox.name = `${sectionName}-checkbox-${checkboxData.tag}`;
      checkbox.value = checkboxData.tag;
      const label = document.createElement("label");
      label.htmlFor = checkboxId; // Associate label with checkbox
      label.textContent = checkboxData.label;

      checkbox.addEventListener("change", function () {
        updateCheckboxState(this);
      });

      container.appendChild(checkbox);
      container.appendChild(label);
      return container;
    }

    const sections = ["input", "gamemode", "author", "misc"];
    // Add checkboxes to each section based on JSON data
    sections.forEach((sectionName) => {
      const section = document.getElementById(`${sectionName}-checkboxes`);
      if (data[sectionName] && data[sectionName].checkboxes) {
        data[sectionName].checkboxes.forEach((checkboxData) => {
          const checkboxContainer = createCheckbox(checkboxData, sectionName);
          section.appendChild(checkboxContainer);
        });
      }
    });

    // Function to update the checkbox state
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

      updateWishlistUrls();
    }

    function updateWishlistUrls() {
      // Clear urls
      const urlsList = document.getElementById("urls-list");
      while (urlsList.firstChild) {
        urlsList.removeChild(urlsList.firstChild);
      }

      // Display the "wishlists" and "urls" values
      data.wishlists.urls.forEach((url) => {
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
        if (includeFound && !excludeFound) {
          const listItem = document.createElement("li");
          const textSpan = document.createElement("span"); // Create a new span for the text
          textSpan.textContent = url.label;

          // Add a click event listener to the text span
          textSpan.addEventListener("click", function () {
            // Copy the URL to the clipboard
            const textarea = document.createElement("textarea");
            textarea.value = url.link;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand("copy");
            document.body.removeChild(textarea);

            // Optionally, provide user feedback
            openCustomAlert("URL copied to clipboard: " + textarea.value);
          });

          listItem.appendChild(textSpan); // Append the text span to the list item
          urlsList.appendChild(listItem);
        }
      });
    }
    updateWishlistUrls();
  })
  .catch((error) => console.error("Error fetching JSON:", error));

// Function to open the custom alert
function openCustomAlert(message) {
  const alertMessage = document.getElementById("alert-message");
  alertMessage.textContent = message;
  const customAlert = document.querySelector(".custom-alert");
  customAlert.style.display = "flex";
}

// Function to close the custom alert
function closeCustomAlert() {
  const customAlert = document.querySelector(".custom-alert");
  customAlert.style.display = "none";
}
