function scrollReviews(direction) {
    const reviewGrid = document.querySelector('.reviews-grid');
    const scrollAmount = 813; // Adjust this to change scroll distance

    if (direction === 'left') {
        reviewGrid.scrollBy({ left: -scrollAmount, behaviour: 'smooth' });
    } else if (direction === 'right') {
        reviewGrid.scrollBy({ left: scrollAmount, behaviour: 'smooth' });
    }
}

// Handle the edit review form, fill fields and execute edit_review view function
function fillReviewForm(rating, comment, reviewId, wineId) {
    // Fill in the rating, comment, and IDs into the edit review form
    document.getElementById('id_rating').value = rating;
    document.getElementById('id_comment').value = comment;
    document.getElementById('reviewId').value = reviewId;
    document.getElementById('wineId').value = wineId;

    // Dynamically set the action URL for the form to point to and run the edit_review view
    let reviewForm = document.getElementById('reviewForm');
    reviewForm.setAttribute("action", `/products/${wineId}/review/${reviewId}/edit/`);
}

function setDeleteReviewAction(wineId, reviewId) {
    // Set the action URL dynamically
    let deleteForm = document.getElementById('deleteReviewForm');
    deleteForm.setAttribute('action', `/products/${wineId}/review/${reviewId}/delete/`);
}

