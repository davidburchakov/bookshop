let cookieModal;

window.onload = function() {
    cookieModal = document.getElementById('cookieConsentModal');

    // Check if the cookie consent has been set in this session
    if (!sessionStorage.getItem('cookieConsent')) {
        cookieModal.style.display = 'block';
    }

    let acceptBtn = document.getElementById('acceptCookieBtn');
    let rejectBtn = document.getElementById('rejectCookieBtn');

    acceptBtn.onclick = function() {
        handleCookieConsent('accepted');
    };

    rejectBtn.onclick = function() {
        handleCookieConsent('rejected');
    };
};

function sendCookieConsent(choice) {
    fetch('/set-cookie-consent/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ consent: choice }),
    });
}

function handleCookieConsent(choice) {
    sessionStorage.setItem('cookieConsent', choice);
    cookieModal.style.display = 'none';
    sendCookieConsent(choice); // Send user choice to the backend
}

// Function to get CSRF token from cookies
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

