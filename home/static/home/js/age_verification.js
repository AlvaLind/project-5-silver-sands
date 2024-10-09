// This script manages the age verification modal for users visiting the site.

document.addEventListener('DOMContentLoaded', function () {
    const ageModal = document.getElementById('age-modal');
    const confirmAgeBtn = document.getElementById('confirm-age');
    const exitSiteBtn = document.getElementById('exit-site');

    // Assign the access denied URL using Django's URL template tag
    const accessDeniedUrl = "{% url 'access_denied' %}";

    // Check if the user has already confirmed their age
    if (!localStorage.getItem('ageVerified')) {
        ageModal.style.display = 'flex';
    } else {
        ageModal.style.display = 'none';
    }

    // Event listener for the "I am 18 or older" button
    confirmAgeBtn.addEventListener('click', function () {
        localStorage.setItem('ageVerified', 'true');
        ageModal.style.display = 'none';
    });

    // Event listener for the "I am under 18" button
    exitSiteBtn.addEventListener('click', function () {
        window.location.href = accessDeniedUrl;
    });
});
