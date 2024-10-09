// Toggles the visibility of additional statistics and updates the button text accordingly.

function toggleMoreStats() {
    var moreStats = document.getElementById("moreStats");
    var button = document.getElementById("showMoreButton");
    
    // Toggle the moreStats section open and closed
    if (moreStats.classList.contains("d-none")) {
        moreStats.classList.remove("d-none");
        button.textContent = "Show Less";
    } else {
        moreStats.classList.add("d-none");
        button.textContent = "Show More";
    }
}

// Fetches order details from the server and populates the modal with the retrieved data.
function fetchOrderDetails(orderId) {
    // Make a request to the server to fetch order details for the given orderId
    fetch(`/management_dashboard/orders/${orderId}/details/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Populate the modal with the order details
            document.getElementById('orderDetailsModalLabel').innerText = `Order #${data.order_number}`;
            const orderDetailsContent = `
                <p><strong>Total Value:</strong> $${data.total_value}</p>
                <p><strong>Status:</strong> ${data.status}</p>
                <p><strong>Customer Details:</strong></p>
                <p>Name: ${data.customer_name}</p>
                <p>Email: ${data.customer_email}</p>
                <p>Street: ${data.customer_street}</p>
                <p>Town/City: ${data.customer_town}</p>
                <p><strong>Items Purchased:</strong>
                <ul>
                    ${data.items.map(item => `<li>${item.quantity} x ${item.name}</li>`).join('')}
                </ul>
            `;
            // Insert the order details into the modal's content area
            document.getElementById('orderDetailsContent').innerHTML = orderDetailsContent;

            // Manage visibility of the delete button based on order status
            const deleteButton = document.getElementById('deleteOrderBtn');
            if (data.status === 'pending') {
                deleteButton.style.display = 'block';
                // Set the form action URL dynamically
                document.getElementById('deleteOrderForm').action = `/management_dashboard/delete-order/${orderId}/`;
            } else {
                deleteButton.style.display = 'none';
            }

            // Create a new modal instance and show the order details modal
            const modal = new bootstrap.Modal(document.getElementById('orderDetailsModal'));
            modal.show();
        })
        .catch(error => console.error('Error fetching order details:', error));
}   
