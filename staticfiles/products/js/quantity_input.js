// This script manages the quantity selection for items, enabling or disabling increment 
// and decrement buttons based on current quantity values.
    
$(document).ready(function() {
    // Function to enable/disable the increment and decrement buttons based on the current value
    function handleEnableDisable(itemId) {
        var currentValue = parseInt($(`#id_qty_${itemId}`).val(), 10); // Ensure base 10 parsing
        var minusDisabled = currentValue <= 1;
        var plusDisabled = currentValue >= 99;
        $(`#decrement-qty_${itemId}`).prop('disabled', minusDisabled);
        $(`#increment-qty_${itemId}`).prop('disabled', plusDisabled);
    }

    // Initialise enable/disable state on page load for each quantity input
    $('.qty_input').each(function() {
        var itemId = $(this).data('item_id');
        handleEnableDisable(itemId);
    });

    // Increment quantity
    $('.increment-qty').off('click').on('click', function(e) {
        e.preventDefault();
        var itemId = $(this).data('item_id');
        var qtyInput = $(`#id_qty_${itemId}`);
        var currentValue = parseInt(qtyInput.val(), 10); // Ensure base 10 parsing
        
        if (currentValue < 99) {
            qtyInput.val(currentValue + 1).trigger('change');
        }
        handleEnableDisable(itemId);
    });

    // Decrement quantity
    $('.decrement-qty').off('click').on('click', function(e) {
        e.preventDefault();
        var itemId = $(this).data('item_id');
        var qtyInput = $(`#id_qty_${itemId}`);
        var currentValue = parseInt(qtyInput.val(), 10); // Ensure base 10 parsing

        if (currentValue > 1) {
            qtyInput.val(currentValue - 1).trigger('change');
        }
        handleEnableDisable(itemId);
    });

    // Ensure the quantity input is properly validated
    $('.qty_input').on('input change', function() {
        var itemId = $(this).data('item_id');
        var currentValue = parseInt($(this).val(), 10); // Ensure base 10 parsing
        
        // Handle invalid inputs or out-of-bound values
        if (isNaN(currentValue) || currentValue < 1) {
            $(this).val(1);
        } else if (currentValue > 99) {
            $(this).val(99);
        }

        handleEnableDisable(itemId);
    });
});
