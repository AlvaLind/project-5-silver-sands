document.addEventListener('DOMContentLoaded', function () {
    const ageModal = document.getElementById('age-modal');
    const confirmAgeBtn = document.getElementById('confirm-age');
    const exitSiteBtn = document.getElementById('exit-site');

    // Check if the user has already confirmed their age
    if (!localStorage.getItem('ageVerified')) {
        ageModal.style.display = 'flex';
    } else {
        // If the age is already verified, ensure the modal is hidden
        ageModal.style.display = 'none';
    }

    // Event listener for the "I am 18 or older" button
    confirmAgeBtn.addEventListener('click', function () {
        // Set ageVerified in local storage to true
        localStorage.setItem('ageVerified', 'true');
        ageModal.style.display = 'none';
    });

    // Event listener for the "I am under 18" button
    exitSiteBtn.addEventListener('click', function () {
        window.location.href = accessDeniedUrl;
    });
});
