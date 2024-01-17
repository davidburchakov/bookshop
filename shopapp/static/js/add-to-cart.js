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
                    alert('Book added to cart!');
                    const quantityDisplay = document.querySelector('.quantity');
                    if (quantityDisplay) {
                        quantityDisplay.textContent = data.total_quantity;
                    }
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
