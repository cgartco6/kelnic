// Chatbot functionality
class Chatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.initializeChatbot();
    }
    
    initializeChatbot() {
        this.chatbotButton = document.getElementById('chatbot-button');
        this.chatbotWindow = document.getElementById('chatbot-window');
        this.chatbotMessages = document.getElementById('chatbot-messages');
        this.chatbotInput = document.getElementById('chatbot-input');
        this.sendButton = document.getElementById('send-message');
        
        if (!this.chatbotButton || !this.chatbotWindow) return;
        
        this.chatbotButton.addEventListener('click', () => this.toggleChatbot());
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.chatbotInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Load previous messages from localStorage
        const savedMessages = localStorage.getItem('chatbot_messages');
        if (savedMessages) {
            this.messages = JSON.parse(savedMessages);
            this.renderMessages();
        }
    }
    
    toggleChatbot() {
        this.isOpen = !this.isOpen;
        this.chatbotWindow.classList.toggle('active', this.isOpen);
        
        if (this.isOpen) {
            this.chatbotInput.focus();
        }
    }
    
    addMessage(text, isUser = false) {
        const message = {
            text,
            isUser,
            timestamp: new Date().toISOString()
        };
        
        this.messages.push(message);
        this.saveMessages();
        this.renderMessages();
    }
    
    async sendMessage() {
        const message = this.chatbotInput.value.trim();
        if (!message) return;
        
        this.chatbotInput.value = '';
        this.addMessage(message, true);
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: message })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.addMessage(data.response, false);
            } else {
                this.addMessage("I'm sorry, I'm having trouble connecting right now. Please try again later.", false);
            }
        } catch (error) {
            this.addMessage("I'm sorry, I'm having trouble connecting right now. Please try again later.", false);
        }
    }
    
    renderMessages() {
        if (!this.chatbotMessages) return;
        
        this.chatbotMessages.innerHTML = '';
        
        this.messages.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${message.isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.textContent = message.text;
            this.chatbotMessages.appendChild(messageDiv);
        });
        
        this.chatbotMessages.scrollTop = this.chatbotMessages.scrollHeight;
    }
    
    saveMessages() {
        localStorage.setItem('chatbot_messages', JSON.stringify(this.messages));
    }
}

// Initialize chatbot
document.addEventListener('DOMContentLoaded', () => {
    new Chatbot();
});
