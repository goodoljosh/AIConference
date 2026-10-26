//Main not needed anymore
document.addEventListener('DOMContentLoaded', () => {

    // 1. Select Chatbot UI elements
    const chatForm = document.getElementById('chat-form') || document.querySelector('form');
    const chatInput = document.getElementById('chat-input') || document.querySelector('input[type="text"]');
    const chatMessages = document.getElementById('chat-messages') || document.querySelector('.chat-body');
    const sendButton = document.getElementById('send-btn') || document.querySelector('button[type="submit"]');

    if (!chatInput || !chatMessages) {
        console.error('Chatbot input or messages container not found in DOM.');
        return;
    }

    // 2. Main submit handler
    async function handleSendMessage(e) {
        if (e) e.preventDefault();

        const userText = chatInput.value.trim();
        if (!userText) return;

        // Display User Message in UI
        appendMessage('user', userText);
        chatInput.value = '';

        // Show "Thinking..." loading placeholder
        const loadingDiv = appendMessage('ai loading', 'Thinking...');

        // Disable input while awaiting response
        setLoadingState(true);

        try {
            // Relative URL fetch to Flask backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userText })
            });

            const data = await response.json();

            // Remove loading indicator
            if (loadingDiv && loadingDiv.parentNode) {
                loadingDiv.parentNode.removeChild(loadingDiv);
            }

            if (response.ok && data.response) {
                // Display Ollama AI Response
                appendMessage('ai', data.response);
            } else {
                // Display Backend Error Message
                const errorMsg = data.error || 'Failed to get a response from AI.';
                appendMessage('ai error', `Error: ${errorMsg}`);
            }

        } catch (error) {
            console.error('Fetch error:', error);
            if (loadingDiv && loadingDiv.parentNode) {
                loadingDiv.parentNode.removeChild(loadingDiv);
            }
            appendMessage('ai error', 'Error: Could not connect to Flask backend. Make sure python app.py is running on http://127.0.0.1:5000.');
        } finally {
            // Re-enable input controls
            setLoadingState(false);
            chatInput.focus();
        }
    }

    // 3. Helper function to append message elements to the DOM
    function appendMessage(senderClass, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${senderClass}`;

        const textSpan = document.createElement('span');
        textSpan.textContent = text;
        msgDiv.appendChild(textSpan);

        chatMessages.appendChild(msgDiv);

        // Auto-scroll to latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;

        return msgDiv;
    }

    // 4. Helper function to disable/enable inputs
    function setLoadingState(isLoading) {
        chatInput.disabled = isLoading;
        if (sendButton) sendButton.disabled = isLoading;
    }

    // 5. Attach event listeners
    if (chatForm && chatForm.tagName === 'FORM') {
        chatForm.addEventListener('submit', handleSendMessage);
    } else if (sendButton) {
        sendButton.addEventListener('click', handleSendMessage);
    }

    // Allow Enter key submission
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
});