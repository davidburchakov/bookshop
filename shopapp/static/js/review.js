document.getElementById('review-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const form = this;
    const actionUrl = form.getAttribute('data-action-url');
    const text = form.elements['text'].value;
    const scoreRadios = form.elements['score'];
    let scoreValue = null;

    // Loop through radio buttons to find the checked one
    for (const radio of scoreRadios) {
        if (radio.checked) {
            scoreValue = radio.value;
            break;
        }
    }

    const formData = new FormData();
    formData.append('text', text);
    if (scoreValue !== null) {
        formData.append('score', scoreValue);
    }

    fetch(actionUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Assuming you have a function to get cookies
        },
        body: formData
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
