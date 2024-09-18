function scrollReviews(direction) {
    const reviewGrid = document.querySelector('.reviews-grid');
    const scrollAmount = 813; // Adjust this to change scroll distance

    if (direction === 'left') {
        reviewGrid.scrollBy({ left: -scrollAmount, behaviour: 'smooth' });
    } else if (direction === 'right') {
        reviewGrid.scrollBy({ left: scrollAmount, behaviour: 'smooth' });
    }
}
