// Dropdown functionality for filtering and sorting items

document.addEventListener('DOMContentLoaded', function() {
    // Selecting necessary DOM elements
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdownContent = document.querySelector('.dropdown-content');
    const sortDropdownBtn = document.getElementById('sortDropdownBtn');
    const sortDropdownContent = document.getElementById('sortDropdownContent');
    
    // Toggle filter dropdown and close sort dropdown if it's open
    dropdownBtn.addEventListener('click', function(event) {
        event.stopPropagation();
        dropdownContent.classList.toggle('show');
        sortDropdownContent.classList.remove('show'); 
    });

    // Toggle sort dropdown and close filter dropdown if it's open
    sortDropdownBtn.addEventListener('click', function(event) {
        event.stopPropagation();
        sortDropdownContent.classList.toggle('show');
        dropdownContent.classList.remove('show');
    });

    // Close the dropdowns if the user clicks outside of them
    document.addEventListener('click', function(event) {
        if (!dropdownContent.contains(event.target) && !dropdownBtn.contains(event.target)) {
            dropdownContent.classList.remove('show');
        }
        if (!sortDropdownContent.contains(event.target) && !sortDropdownBtn.contains(event.target)) {
            sortDropdownContent.classList.remove('show');
        }
    });
});

// Delete a product from the product list - admin user
function setDeleteProductAction(wineId) {
    const form = document.getElementById('deleteProductForm');
    form.action = `/management_dashboard/delete/${wineId}/`;
}
