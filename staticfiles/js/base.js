document.addEventListener("DOMContentLoaded", function() {
    // Automatically close messages after 3 seconds
    setTimeout(function() {
        let messages = document.querySelectorAll('.alert');
        messages.forEach(function(message) {
            console.log("Hiding message:", message.textContent);
            message.style.display = 'none';
        });
    }, 3000);

    // Toggle search form visibility
    document.querySelector('.search-icon').addEventListener('click', function() {
        var form = document.querySelector('.form-inline');
        form.classList.toggle('d-none');      // Hide/show using d-none class
        form.classList.toggle('d-block');     // Show as block element
    });


    // Handle navbar toggle events to hide nav logo and basket when nav toggle
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

    // Show icons when navbar is fully closed
    navbarCollapse.addEventListener('hidden.bs.collapse', function () {
        navbarIconsLogo.classList.remove('d-none');
        navbarIconsBasket.classList.remove('d-none');
    });

    // Hide icons when navbar is fully opened
    navbarCollapse.addEventListener('shown.bs.collapse', function () {
        navbarIconsLogo.classList.add('d-none');
        navbarIconsBasket.classList.add('d-none');
    });
});
