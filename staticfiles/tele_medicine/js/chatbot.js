const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbotWidget = document.getElementById('chatbot-widget');
const closeChat = document.getElementById('close-chat');
const chatbotInput = document.getElementById('chatbot-input');
const sendMessage = document.getElementById('send-message');
const chatbotMessages = document.getElementById('chatbot-messages');

let conversationStep = 0;
let userData = {
    name: '',
    age: '',
    concern: ''
};

// Toggle chatbot open/close
chatbotToggle.addEventListener('click', () => {
    chatbotWidget.classList.remove('chatbot-collapsed');
    chatbotWidget.classList.add('chatbot-expanded');
    chatbotToggle.style.display = 'none';

    if (conversationStep === 0) {
        setTimeout(() => {
            addBotMessage("To help you better, may I know your name?");
            conversationStep = 1;
        }, 1000);
    }
});

// Close chatbot
closeChat.addEventListener('click', () => {
    chatbotWidget.classList.remove('chatbot-expanded');
    chatbotWidget.classList.add('chatbot-collapsed');
    chatbotToggle.style.display = 'flex';
});

// Send message on button click
sendMessage.addEventListener('click', handleUserMessage);

// Send message on Enter key
chatbotInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleUserMessage();
    }
});

function handleUserMessage() {
    const message = chatbotInput.value.trim();
    if (message === '') return;
    addUserMessage(message);
    chatbotInput.value = '';

    setTimeout(() => {
        processConversation(message);
    }, 500);
}

function processConversation(message) {
    switch(conversationStep) {
        case 1:
            userData.name = message;
            addBotMessage(`Nice to meet you, ${userData.name}! 😊`);
            setTimeout(() => {
                addBotMessage("May I know your age?");
                conversationStep = 2;
            }, 1000);
            break;

        case 2:
            userData.age = message;
            addBotMessage("Thank you!");
            setTimeout(() => {
                addBotMessage("How can I assist you today? Are you looking for diagnosis, doctor details, or nearest medical centers?");
                conversationStep = 3;
            }, 1000);
            break;

        case 3:
            const lowerMessage = message.toLowerCase();
            if (lowerMessage.includes('diagnosis') || lowerMessage.includes('symptom') || lowerMessage.includes('diagnos')) {
                addBotMessage("I can help you with diagnosis! Please click on the 'diagnosis-chat' card on the main page to start your medical consultation. 🏥");
            } else if (lowerMessage.includes('doctor') || lowerMessage.includes('appointment')) {
                addBotMessage("You can find doctor details by clicking on the 'doctor-details' card on the main page. 👨‍⚕");
            } else if (lowerMessage.includes('location') || lowerMessage.includes('nearest') || lowerMessage.includes('center') || lowerMessage.includes('centre')) {
                addBotMessage("To find the nearest medical help center, click on the 'Nearest Medi-Help Centre' card on the main page. 📍");
            } else if (lowerMessage.includes('help')) {
                addBotMessage("I can help you with:\n• Medical Diagnosis\n• Finding Doctors\n• Locating Nearest Medical Centers\n\nWhat would you like to know more about?");
            } else if (lowerMessage.includes('thank') || lowerMessage.includes('thanks')) {
                addBotMessage("You're welcome! Feel free to ask if you need anything else. 😊");
            } else if (lowerMessage.includes('bye') || lowerMessage.includes('goodbye')) {
                addBotMessage("Goodbye! Take care and stay healthy! 👋");
            } else {
                addBotMessage("I can assist you with diagnosis, finding doctors, or locating medical centers. How can I help you?");
            }
            break;
    }
}

function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'user-message';
    messageDiv.innerHTML = '<p>${message}</p>';
    chatbotMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'bot-message';
    messageDiv.innerHTML = '<p>${message}</p>';
    chatbotMessages.appendChild(messageDiv);
    scrollToBottom();
}

function scrollToBottom() {
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}