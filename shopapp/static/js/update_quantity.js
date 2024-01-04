// Function to get the value of a cookie by name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateQuantity(bookId, change) {
        const csrftoken = getCookie('csrftoken');  // Get CSRF token from cookies

        fetch('/update-cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken  // Include CSRF token in the request header
            },
            body: JSON.stringify({book_id: bookId, change: change})
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                window.location.reload();
            } else {
                alert(data.message);
            }
        });
    }