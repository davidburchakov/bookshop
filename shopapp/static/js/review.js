document.getElementById('review-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = this;
    const actionUrl = form.getAttribute('data-action-url');
    const text = form.elements['text'].value;

    fetch(actionUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Assuming you have a function to get cookies
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'text=' + encodeURIComponent(text)
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success') {
            // Append the new review to the review list
            const reviewList = document.getElementById('review-list');
            const newReview = document.createElement('div');
            newReview.textContent = data.review;
            reviewList.appendChild(newReview);
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});
