// Handles the colour change of the country selection dropdown based on whether a country is selected.

document.addEventListener('DOMContentLoaded', function() {
    // Get the country dropdown element and initial selected country value
    const countryDropdown = document.getElementById('id_default_country');
    let countrySelected = countryDropdown.value;

    // Set the dropdown colour if no country is selected
    if (!countrySelected) {
        countryDropdown.style.color = '#9ba6db';
    }
    // Change event listener for the dropdown
    countryDropdown.addEventListener('change', function() {
        countrySelected = this.value;

        // Update the dropdown color based on selection
        if (!countrySelected) {
            this.style.color = '#9ba6db';
        } else {
            this.style.color = '#000';
        }
    });
});
