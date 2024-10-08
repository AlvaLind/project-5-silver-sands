/* global Stripe */

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', { style: style });
card.mount('#card-element');

// Handle real-time validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    // Clear previous error messages
    clearFormErrors();

    // Validate required fields
    const requiredFields = [
        'id_full_name',
        'id_email',
        'id_phone_number',
        'id_street_address1',
        'id_town_or_city',
        'id_county',
        'id_postcode',
        'id_country'
    ];

    let allFilled = true;

    requiredFields.forEach(function (fieldId) {
        const field = document.getElementById(fieldId);
        if (!field.value.trim()) {
            allFilled = false;
            field.classList.add("is-invalid"); // Add Bootstrap invalid class
        } else {
            field.classList.remove("is-invalid"); // Remove invalid class if filled
        }
    });

    if (!allFilled) {
        alert("Please fill out all required fields.");
        return; // Exit the function if validation fails
    }

    // Disable form fields to prevent duplicate submissions
    card.update({ 'disabled': true });
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // Get form data we can't put in the payment intent
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };

    // URL to post the above data to the cache checkout data view
    var url = '/checkout/cache_checkout_data/';

    // Post the postData to the view which updates the payment intent and returns a 200 response
    $.post(url, postData).done(function () {
        // Call the confirm card payment method from stripe
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
        }).then(function (result) {
            // If there are errors allow user to update the form and try again
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                // Show the loading overlay and enable form fields again
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false });
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        }).fail(function () {
            // Handle errors during post request
            location.reload();
        });
    }).fail(function () {
        // Handle errors during the post request
        location.reload();
    });
});

// Function to clear form validation errors
function clearFormErrors() {
    const requiredFields = [
        'id_full_name',
        'id_email',
        'id_phone_number',
        'id_street_address1',
        'id_town_or_city',
        'id_county',
        'id_postcode',
        'id_country'
    ];

    requiredFields.forEach(function (fieldId) {
        const field = document.getElementById(fieldId);
        field.classList.remove("is-invalid"); // Remove invalid class if present
    });
}
