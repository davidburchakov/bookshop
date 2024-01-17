document.getElementById('score-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const bookId = this.getAttribute('data-book-id');
    const score = this.score.value;

    fetch("{% url 'submit_score' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: 'book_id=' + bookId + '&score=' + score
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Score submitted successfully!');
            document.getElementById('average-score-value').textContent = data.average_score;
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});
