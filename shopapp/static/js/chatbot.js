document.addEventListener('DOMContentLoaded', function() {
    var chatbotTrigger = document.getElementById('chatbotTrigger');
    var chatbotContainer = document.getElementById('chatbotContainer');
    var closeChatbot = document.getElementById('closeChatbot');
    var chatInput = document.getElementById('chatInput'); // Input field for user messages
    var chatContent = document.querySelector('.chatbot-content'); // Container for chat messages

    // Open chatbot
    chatbotTrigger.addEventListener('click', function() {
        chatbotContainer.style.display = 'block';
    });

    // Close chatbot
    closeChatbot.addEventListener('click', function() {
        chatbotContainer.style.display = 'none';
    });

    // Send message and get response
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            var message = chatInput.value;
            chatInput.value = ''; // Clear input field

            // Display user message
            chatContent.innerHTML += '<div>User: ' + message + '</div>';

            // Send message to server
            fetch('/chatbot-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            })
            .then(response => response.json())
            .then(data => {
                // Display bot response
                chatContent.innerHTML += '<div>Bot: ' + data.reply + '</div>';
            });
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    var chatbotContainer = document.getElementById('chatbotContainer');
    var chatContent = document.querySelector('.chatbot-content');
    var chatInput = document.getElementById('chatInput');
    var sendMessageButton = document.getElementById('sendMessage');

    function sendMessage() {
        var message = chatInput.value.trim();
        if (message) {
            chatInput.value = ''; // Clear input field
            chatContent.innerHTML += '<div>User: ' + message + '</div>';

            // Send message to server
            fetch('/path_to_chatbot_endpoint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            })
            .then(response => response.json())
            .then(data => {
                chatContent.innerHTML += '<div>Bot: ' + data.reply + '</div>';
            });
        }
    }

    sendMessageButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
