document.addEventListener('DOMContentLoaded', () => {
    const addCartForm = document.querySelector('.add-to-cart-form');
    if (addCartForm) {
        addCartForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const csrftoken = formData.get('csrfmiddlewaretoken'); // Get CSRF token from form data

            fetch(this.action, {
                method: 'POST',
                body: new URLSearchParams(formData).toString(),
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok: ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    displayMessage('Book added to cart!', 'success');
                    const quantityDisplay = document.querySelector('.quantity');
                    if (quantityDisplay) {
                        quantityDisplay.textContent = data.total_quantity;
                    }
                } else {
                    displayMessage('Error: ' + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                displayMessage('Error: ' + error.message, 'error');
            });
        });
    }
});

function displayMessage(message, type) {
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerText = message;
    messageContainer.className = type; // You can use this to apply different styles for success/error messages
}
