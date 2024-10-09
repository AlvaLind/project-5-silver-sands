// Manages the visibility of the search form and navbar icons based on user interactions.

document.addEventListener("DOMContentLoaded", function() {
    // Toggle search form visibility on search icon click
    document.querySelector('.search-icon').addEventListener('click', function() {
        var form = document.querySelector('.form-inline');
        form.classList.toggle('d-none');
        form.classList.toggle('d-block');
    });

    // Handle navbar toggle events to manage logo and basket visibility
    var navbarToggle = document.querySelector('.navbar-toggler');
    var navbarIconsLogo = document.querySelector('.navbar-icons-logo');
    var navbarIconsBasket = document.querySelector('.navbar-icons-basket');

    navbarToggle.addEventListener('click', function() {
        // Check if the navbar is expanded and hide and show logo and basket accordingly
        if (navbarIconsLogo.classList.contains('d-none') && navbarIconsBasket.classList.contains('d-none')) {
            navbarIconsLogo.classList.remove('d-none');
            navbarIconsBasket.classList.remove('d-none');
        } else {
            navbarIconsLogo.classList.add('d-none');
            navbarIconsBasket.classList.add('d-none');
        }
    });

    // Bootstrap events for handling collapse
    var navbarCollapse = document.getElementById('navbarText');

    // Show icons when navbar is fully collapsed
    navbarCollapse.addEventListener('hidden.bs.collapse', function () {
        navbarIconsLogo.classList.remove('d-none');
        navbarIconsBasket.classList.remove('d-none');
    });

    // Hide icons when navbar is fully expanded
    navbarCollapse.addEventListener('shown.bs.collapse', function () {
        navbarIconsLogo.classList.add('d-none');
        navbarIconsBasket.classList.add('d-none');
    });
});
