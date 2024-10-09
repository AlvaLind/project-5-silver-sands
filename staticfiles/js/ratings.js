// Handles the visual representation of product ratings using star icons.

document.addEventListener('DOMContentLoaded', function () {
    // Select elements for star icons and average product rating
    const starIcons = document.querySelectorAll('.product-rating-star');
    const averageRatingElement = document.getElementById('average-rating');

    // Function to update star icons based on average rating
    function fillProductStars(averageRating) {
        starIcons.forEach(starIcon => {
            const starValue = parseInt(starIcon.getAttribute('data-value'));
            const isFullStar = averageRating >= starValue;
            const isHalfStar = averageRating - Math.floor(averageRating) >= 0.3 && averageRating - Math.floor(averageRating) <= 0.7 && Math.floor(averageRating) === starValue - 1;

            // Handle full and half-filled stars
            if (isFullStar) {
                starIcon.classList.add('fas'); // Fill the star
                starIcon.classList.remove('far');
            } else {
                starIcon.classList.remove('fas'); // Empty the star
                starIcon.classList.add('far');
            }

            // Handle half-filled stars
            if (isHalfStar) {
                starIcon.classList.add('half-filled');
                starIcon.classList.add('fas');
            } else {
                starIcon.classList.remove('half-filled');
            }
        });
    }

    // Get the average rating from the text content and update star icons on page load
    const averageRating = parseFloat(averageRatingElement.textContent);
    fillProductStars(averageRating);
});
