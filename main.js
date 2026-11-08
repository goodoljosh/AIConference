document.addEventListener('DOMContentLoaded', () => {
  const chatWidget = document.getElementById('chat-widget');
  const toggleBtn = document.getElementById('toggle-chat-btn');
  const chatForm = document.getElementById('chat-input-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');

  // Minimize / Maximize Chatbot Logic
  let isMinimized = false;
  toggleBtn.addEventListener('click', () => {
    isMinimized = !isMinimized;
    if (isMinimized) {
      chatWidget.classList.add('minimized');
      toggleBtn.textContent = '+';
      toggleBtn.setAttribute('aria-expanded', 'false');
      toggleBtn.setAttribute('aria-label', 'Maximize Chat Window');
    } else {
      chatWidget.classList.remove('minimized');
      toggleBtn.textContent = '−';
      toggleBtn.setAttribute('aria-expanded', 'true');
      toggleBtn.setAttribute('aria-label', 'Minimize Chat Window');
    }
  });

  // Chat message submission
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;

    appendMessage(text, 'user');
    chatInput.value = '';

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      appendMessage(data.response, 'bot');
    } catch (err) {
      appendMessage('Unable to parse response. Please check server connection.', 'bot');
    }
  });

  function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.textContent = text;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});