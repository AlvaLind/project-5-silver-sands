// Manage quantity selection and updates for items in the bag. 

$(document).ready(function() {
    // Update quantity on clicking the increment and decrement buttons
    $('.increment-qty-sm, .decrement-qty-sm').click(function(e) {
        e.preventDefault();
        e.stopPropagation(); 

        var $input = $(this).siblings('input.qty_input'); // Adjusted to target the input correctly
        var currentVal = parseInt($input.val());

        if ($(this).hasClass('increment-qty-sm')) {
            $input.val(currentVal + 1);
        } else if ($(this).hasClass('decrement-qty-sm') && currentVal > 1) {
            $input.val(currentVal - 1);
        }
    });

    // Update quantity on clicking the 'Update' link - small screens
    $('.update-link').click(function(e) {
        e.preventDefault(); 
        var form = $(this).closest('div.card-body').find('.update-form'); // Adjusted to find the form correctly
        form.submit();
    });

    // Update quantity on clicking the 'Update' link - large screens
    $('.update-link').click(function(e) {
        e.preventDefault(); 
        var form = $(this).closest('td').find('.update-form');
        form.submit();
    });

    // Remove item and reload on click
    $('.remove-item').click(function(e) {
        var csrfToken = "{{ csrf_token }}";
        var itemId = $(this).attr('id').split('remove_')[1];
        var url = `/bag/remove/${itemId}/`;
        var data = {'csrfmiddlewaretoken': csrfToken};

        $.post(url, data)
        .done(function() {
            location.reload();
        });
    });
});
