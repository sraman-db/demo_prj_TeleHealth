// diagnosis_chat.js
// Handles chat between user and disease prediction model with clean UI and auto-scroll fix.

// ------------------------------
// ✅ Get CSRF Token Helper
// ------------------------------
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

// ------------------------------
// 🧱 DOM Elements
// ------------------------------
const form = document.getElementById('diagnosis-form');
const input = document.getElementById('diagnosis-input');
const messages = document.getElementById('chat-messages');

// ------------------------------
// 💬 Append a message to chat box
// ------------------------------
function appendMessage(text, cls = 'bot') {
  const wrap = document.createElement('div');
  wrap.className = cls === 'user' ? 'user-message' : 'bot-message';

  const p = document.createElement('p');
  p.innerHTML = text; // allows basic emoji + formatting
  wrap.appendChild(p);
  messages.appendChild(wrap);

  // ✅ Auto-scroll to bottom if user near bottom already
  const isAtBottom =
    messages.scrollHeight - messages.scrollTop <= messages.clientHeight + 80;
  if (isAtBottom) {
    messages.scrollTo({
      top: messages.scrollHeight,
      behavior: "smooth"
    });
  }
}

// ------------------------------
// 🚀 Form Submit Handler
// ------------------------------
if (form) {
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    // Show user message
    appendMessage(text, 'user');
    input.value = '';

    // Show loading indicator
    const loading = document.createElement('div');
    loading.className = 'bot-message loading';
    loading.textContent = 'Analyzing symptoms...';
    messages.appendChild(loading);

    // Scroll to bottom on new message
    messages.scrollTo({ top: messages.scrollHeight, behavior: "smooth" });

    // Endpoint (fallback to /predict/)
    const predictUrl = form.dataset.predictUrl || '/predict/';

    // Send request to backend
    fetch(predictUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ text: text })
    })
    .then(resp => resp.json())
    .then(data => {
      loading.remove();

      if (data.error) {
        appendMessage('⚠️ Error: ' + data.error, 'bot');
        return;
      }

      // 🩺 Disease Prediction
      if (data.prediction) {
        if (data.alternates && data.alternates.length > 1) {
          appendMessage(
            `🩺 Based on your symptoms, you may be experiencing <b>${data.alternates.join('</b> or <b>')}</b>.`,
            'bot'
          );
        } else {
          appendMessage(
            `🩺 Based on your symptoms, you may be experiencing <b>${data.prediction}</b>.`,
            'bot'
          );
        }
      }

      // 🧩 Detected symptoms: (hidden from chat UI)
      // -- keeping this for debugging/logging if needed --
      // console.log("Detected features:", data.extracted);

      // 🏥 Recommended Department
      if (data.department) {
        appendMessage(`🏥 Recommended Department: <b>${data.department}</b>`, 'bot');
      }

      if (!data.prediction && !data.error) {
        appendMessage('No prediction returned.', 'bot');
      }

      // ✅ Scroll to bottom after response
      messages.scrollTo({
        top: messages.scrollHeight,
        behavior: "smooth"
      });
    })
    .catch(err => {
      loading.remove();
      appendMessage('Request failed: ' + err, 'bot');
      messages.scrollTo({
        top: messages.scrollHeight,
        behavior: "smooth"
      });
    });
  });
} else {
  console.warn('diagnosis_chat.js: diagnosis form not found');
}
