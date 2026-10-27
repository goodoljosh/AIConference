document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const chatSubmit = document.getElementById('chatSubmit');
    const chatMode = document.getElementById('chatMode');

    const BACKEND_API_URL = 'https://nasty-spooky-toad-7x5qg6vq9qphx54x-5000.app.github.dev/api/chat';

    if (!chatInput || !chatMessages || !chatSubmit) {
        console.error('Chatbot elements not found in DOM.');
        return;
    }

    async function sendMessage() {
        const text = chatInput.value.trim();
        const mode = chatMode ? chatMode.value : 'rag';
        if (!text) return;

        appendMessage(text, 'user');
        chatInput.value = '';

        const modeLabel = mode === 'rag' ? 'RAG Database' : 'Direct Llama';
        const botMessageDiv = appendMessage(`Thinking (${modeLabel})...`, 'bot');
        chatInput.disabled = true;
        chatSubmit.disabled = true;

        try {
            const response = await fetch(BACKEND_API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, mode: mode })
            });

            const data = await response.json();

            if (response.ok) {
                botMessageDiv.innerText = data.response;
            } else {
                botMessageDiv.innerText = 'Error: ' + (data.error || 'Failed to get a response.');
            }
        } catch (error) {
            console.error(error);
            botMessageDiv.innerText = 'Error: Could not connect to Flask backend.';
        } finally {
            chatInput.disabled = false;
            chatSubmit.disabled = false;
            chatInput.focus();
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.innerText = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return messageDiv;
    }

    chatSubmit.addEventListener('click', sendMessage);
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});