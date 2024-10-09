// Manages review grid scrolling and form handling for editing and deleting reviews.

function scrollReviews(direction) {
    const reviewGrid = document.querySelector('.reviews-grid');
    const scrollAmount = 813;

    // Scroll the review grid left or right
    if (direction === 'left') {
        reviewGrid.scrollBy({ left: -scrollAmount, behaviour: 'smooth' });
    } else if (direction === 'right') {
        reviewGrid.scrollBy({ left: scrollAmount, behaviour: 'smooth' });
    }
}

// Fills the edit review form with provided details and sets the form action URL
function fillReviewForm(rating, comment, reviewId, wineId) {
    // Populate the edit review form fields
    document.getElementById('id_rating').value = rating;
    document.getElementById('id_comment').value = comment;
    document.getElementById('reviewId').value = reviewId;
    document.getElementById('wineId').value = wineId;

    // Set the form action URL to the edit review view
    let reviewForm = document.getElementById('reviewForm');
    reviewForm.setAttribute("action", `/products/${wineId}/review/${reviewId}/edit/`);
}

// Dynamically sets the action URL for deleting a review
function setDeleteReviewAction(wineId, reviewId) {
    let deleteForm = document.getElementById('deleteReviewForm');
    deleteForm.setAttribute('action', `/products/${wineId}/review/${reviewId}/delete/`);
}
