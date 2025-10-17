/**
 * ConversAI MVP Frontend JavaScript
 * Handles Web Speech API, chat interface, and TTS
 * Author: ConversAI MVP
 */
console.log('Script.js is loading!');
class ConversAI {
    constructor() {
        console.log('ConversAI constructor is called');
        this.sessionId = this.generateSessionId();
        this.isRecording = false;
        this.recognition = null;
        this.synth = window.speechSynthesis;
        
        // DOM elements
        this.micButton = document.getElementById('mic-button');
        this.micStatus = document.getElementById('mic-status');
        this.chatMessages = document.getElementById('chat-messages');
        this.interimTranscript = document.getElementById('interim-transcript');
        this.fallbackContainer = document.getElementById('fallback-container');
        this.textInput = document.getElementById('text-input');
        this.sendButton = document.getElementById('send-button');
        this.loading = document.getElementById('loading');
        this.sessionIdElement = document.getElementById('session-id');
        
        this.init();
    }
    
    init() {
        console.log('ConversAI init is called');
        // Set session ID
        this.sessionIdElement.textContent = this.sessionId.substring(0, 8) + '...';
        
        // Initialize speech recognition
        this.initSpeechRecognition();
        
        // Initialize text-to-speech
        this.initTextToSpeech();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Check for Web Speech API support
        this.checkSpeechSupport();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    initSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            console.log('Speech recognition is supported');
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            console.log('Speech recognition object created:', this.recognition);

            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
            
            // Add these settings to prevent immediate timeout
            this.recognition.maxAlternatives = 1;
        
            // Add timeout handling
            this.recognitionTimeout = null;

            
            this.recognition.onstart = () => {
                console.log('Speech recognition started');
                this.isRecording = true;
                this.micButton.classList.add('recording');
                this.micStatus.textContent = 'Listening... Speak now';
                this.interimTranscript.textContent = '';

            // Set a longer timeout for detailed responses
            this.recognitionTimeout = setTimeout(() => {
                console.log('Speech recognition timeout - no speech detected');
                this.micStatus.textContent = 'No speech detected. Try again.';
                this.recognition.stop();
            }, 15000); // 15 second timeout for better user experience
            };
            
            this.recognition.onresult = (event) => {
                console.log('Speech recognition result');
                // Clear the timeout since we got a result
                if (this.recognitionTimeout) {
                    clearTimeout(this.recognitionTimeout);
                    this.recognitionTimeout = null;
                }
                
                let interimTranscript = '';
                let finalTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript;
                    } else {
                        interimTranscript += transcript;
                    }
                }
    
                console.log('Interim:', interimTranscript);
                console.log('Final:', finalTranscript);
                
                this.interimTranscript.textContent = interimTranscript;
                
                if (finalTranscript) {
                    console.log('Processing final transcript:', finalTranscript);
                    this.interimTranscript.textContent = '';
                    this.handleUserInput(finalTranscript.trim());
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                console.error('Error details:', event);
                
                // Clear timeout on error
                if (this.recognitionTimeout) {
                    clearTimeout(this.recognitionTimeout);
                    this.recognitionTimeout = null;
                }
                
                this.micStatus.textContent = 'Error: ' + event.error;
                this.stopRecording();
            };
            
            this.recognition.onend = () => {
                console.log('Speech recognition ended');
                // Clear timeout
                if (this.recognitionTimeout) {
                    clearTimeout(this.recognitionTimeout);
                    this.recognitionTimeout = null;
                }
                this.stopRecording();
            };
        } else {
            console.log('Speech recognition NOT supported');
        }
    }
    
    initTextToSpeech() {
        // Check if speech synthesis is supported
        if (!this.synth) {
            console.warn('Speech synthesis not supported');
        }
    }
    
    setupEventListeners() {
        // Microphone button
        this.micButton.addEventListener('click', () => {
            console.log('Mic button clicked');
            if (this.isRecording) {
                this.stopRecording();
            } else {
                this.startRecording();
            }
        });
        
        // Text input fallback
        this.sendButton.addEventListener('click', () => {
            const message = this.textInput.value.trim();
            if (message) {
                this.handleUserInput(message);
                this.textInput.value = '';
            }
        });
        
        this.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendButton.click();
            }
        });
    }
    
    checkSpeechSupport() {
        if (!this.recognition) {
            console.warn('Speech recognition not supported, showing text input fallback');
            this.fallbackContainer.style.display = 'block';
            this.micButton.style.display = 'none';
        }
    }
    
    startRecording() {
        console.log('startRecording called');
        console.log('recognition object:', this.recognition);
        console.log('isRecording:', this.isRecording);
        
        if (this.recognition && !this.isRecording) {
            try {
                console.log('Starting speech recognition...');
                this.recognition.start();
                console.log('Speech recognition started successfully');
            } catch (error) {
                console.error('Error starting speech recognition:', error);
                this.micStatus.textContent = 'Error starting microphone';
            }
        } else {
            console.log('Cannot start recording - recognition:', !!this.recognition, 'isRecording:', this.isRecording);
        }
    }
    
    stopRecording() {
        this.isRecording = false;
        this.micButton.classList.remove('recording');
        this.micStatus.textContent = 'Click to start talking';
        this.interimTranscript.textContent = '';
        
        if (this.recognition) {
            this.recognition.stop();
        }
    }
    
    async handleUserInput(message) {
        if (!message.trim()) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Show loading with longer timeout for detailed responses
        this.showLoading(true);
        this.micStatus.textContent = 'AI is thinking... This may take a moment for detailed responses.';
        
        try {
            // Send to backend
            const response = await this.sendToBackend(message);
            
            if (response.reply) {
                // Add bot response to chat
                this.addMessage(response.reply, 'bot');
                
                // Speak the response
                this.speak(response.reply);
            } else {
                this.addMessage('Sorry, I didn\'t get a response. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Error communicating with backend:', error);
            this.addMessage('Sorry, there was an error. Please check if the backend is running.', 'bot');
        } finally {
            this.showLoading(false);
        }
    }
    
    async sendToBackend(message) {
        console.log('Sending message to backend:', message);
        const response = await fetch('http://localhost:5001/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: this.sessionId
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'ConversAI'}:</strong> ${content}`;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString();
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    speak(text) {
        if (this.synth) {
            // Cancel any ongoing speech
            this.synth.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 0.8;
            
            // Try to use a pleasant voice
            const voices = this.synth.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.name.includes('Google') || 
                voice.name.includes('Microsoft') ||
                voice.name.includes('Samantha')
            );
            
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            this.synth.speak(utterance);
        }
    }
    
    showLoading(show) {
        this.loading.style.display = show ? 'flex' : 'none';
        this.micButton.disabled = show;
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired');
    new ConversAI();
});

// Handle page visibility changes to manage speech recognition
document.addEventListener('visibilitychange', () => {
    if (document.hidden && window.conversAI && window.conversAI.isRecording) {
        window.conversAI.stopRecording();
    }
});
