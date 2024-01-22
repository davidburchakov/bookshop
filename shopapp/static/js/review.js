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
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success') {
            // Update the UI to show the new review
            updateReviewList(text, scoreValue);
            form.reset(); // Reset the form after successful submission
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

function updateReviewList(reviewText, score) {
    const reviewList = document.getElementById('review-list');
    const newReview = document.createElement('div');
    newReview.classList.add('review');

    // Create the star rating element
    const starRating = document.createElement('div');
    starRating.classList.add('star-rating');
    for (let i = 1; i <= 5; i++) {
        const star = document.createElement('span');
        star.innerHTML = i <= score ? '&#9733;' : '&#9734;'; // Filled or empty star
        starRating.appendChild(star);
    }
    newReview.appendChild(starRating);

    // Add review text
    if (reviewText) {
        const reviewTextElement = document.createElement('p');
        reviewTextElement.textContent = reviewText;
        newReview.appendChild(reviewTextElement);
    }

    // Append the new review to the list
    reviewList.appendChild(newReview);
}
