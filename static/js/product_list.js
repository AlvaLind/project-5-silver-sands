// Filter and Sort by dropdown box functionality
document.addEventListener('DOMContentLoaded', function() {
    const dropdownBtn = document.querySelector('.dropdown-btn');  // Filter button
    const dropdownContent = document.querySelector('.dropdown-content'); // Filter dropdown content
    const sortDropdownBtn = document.getElementById('sortDropdownBtn'); // Sort button
    const sortDropdownContent = document.getElementById('sortDropdownContent'); // Sort dropdown content
    
    // Filter button click to toggle filter dropdown and close sort by dropdown if open
    dropdownBtn.addEventListener('click', function(event) {
        event.stopPropagation();
        dropdownContent.classList.toggle('show');
        sortDropdownContent.classList.remove('show'); 
    });

    // Sort button click to toggle sort dropdown and close filter dropdown if open
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
