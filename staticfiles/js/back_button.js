// Stores the referrer URL for the product_detail page and provides a way to navigate back to it.

document.addEventListener('DOMContentLoaded', function() {
    // Store the referrer URL in localStorage if it's available and not already stored
    if (document.referrer && !localStorage.getItem('productDetailsReferrer')) {
        localStorage.setItem('productDetailsReferrer', document.referrer);
    }
});


function goBack() {
    // Retrieve the stored referrer URL from localStorage
    const referrer = localStorage.getItem('productDetailsReferrer');
    
    // If the referrer URL exists, navigate to it and clear it from localStorage
    if (referrer) {
        window.location.href = referrer;
        localStorage.removeItem('productDetailsReferrer');
    } 
    else {
        // If no referrer is stored, go back to the previous page in history
        window.history.back();
    }
}
