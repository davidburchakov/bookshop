document.addEventListener('DOMContentLoaded', () => {
    const scoreForm = document.getElementById('score-form');
    const scoreValue = document.getElementById('average-score-value');

    if (scoreForm) {
        document.querySelectorAll('.star-rating input[type="radio"]').forEach(radio => {
            radio.addEventListener('click', function() {
                const formData = new FormData(scoreForm);
                fetch(scoreForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        scoreValue.textContent = data.average_score.toFixed(2) || "Not yet rated";
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    }
});
