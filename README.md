# ConversAI MVP: AI Driven Digital Human

A voice-first conversational AI application that enables real-time voice interaction with an AI agent using Microsoft's DialoGPT model.

## 🎯 Project Overview

This Semester 7 MVP validates the core concept of voice-driven AI conversation with the following key features:

- **Voice Input**: Web Speech API for real-time speech-to-text
- **AI Processing**: Microsoft DialoGPT-small for conversation generation
- **Voice Output**: Browser Speech Synthesis for text-to-speech
- **Conversation History**: SQLite database for persistent chat storage
- **Modern UI**: Responsive web interface with real-time feedback

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (recommended: Python 3.10+)
- Modern web browser with Web Speech API support (Chrome, Edge, Safari)
- Microphone access for voice input

### Installation & Setup

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd ConversAI-MVP
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```bash
   python database.py
   ```

5. **Test the model (optional but recommended):**
   ```bash
   python test_model.py
   ```

6. **Start the backend server:**
   ```bash
   python app.py
   ```

7. **Open the frontend:**
   - Navigate to `http://localhost:5000` in your browser
   - Or open `frontend/index.html` directly in your browser

## 🎮 Usage

### Voice Mode (Recommended)
1. Click the microphone button 🎤
2. Speak clearly into your microphone
3. Wait for the AI to process and respond
4. The AI will respond both in text and voice

### Text Mode (Fallback)
1. If voice is not supported, use the text input box
2. Type your message and press Enter or click Send
3. Receive text and voice responses

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS)
├── Web Speech API (STT)
├── Chat Interface
└── Speech Synthesis (TTS)

Backend (Python/Flask)
├── REST API (/api/chat)
├── DialoGPT Model
└── SQLite Database

Data Flow:
Browser Voice → STT → Backend → DialoGPT → Response → TTS → Browser Voice
```

## 📁 Project Structure

```
ConversAI-MVP/
├── frontend/
│   ├── index.html          # Main UI
│   ├── style.css           # Styling
│   └── script.js           # Web Speech API & chat logic
├── backend/
│   ├── app.py              # Flask server
│   ├── model.py            # DialoGPT integration
│   ├── database.py         # SQLite operations
│   ├── test_model.py       # Model testing
│   └── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

## 🔧 API Endpoints

- `GET /` - Serves the frontend
- `POST /api/chat` - Main chat endpoint
  - Input: `{"message": "user input", "session_id": "optional"}`
  - Output: `{"reply": "bot response", "session_id": "session_id"}`
- `GET /api/history/<session_id>` - Get conversation history
- `GET /api/health` - Health check

## 🧪 Testing

### Model Testing
```bash
cd backend
python test_model.py
```

### Manual Testing Checklist
- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] Microphone button responds to clicks
- [ ] Voice input is captured and transcribed
- [ ] AI generates relevant responses
- [ ] Text-to-speech works
- [ ] Conversation history is saved to database
- [ ] Multiple conversation turns work
- [ ] Error handling works (try speaking when mic is off)

## ⚙️ Configuration

### Model Parameters
Edit `backend/model.py` to adjust:
- `max_length`: Maximum response length
- `temperature`: Response creativity (0.1-1.0)
- `top_k`: Vocabulary diversity
- `top_p`: Nucleus sampling

### Speech Recognition
Edit `frontend/script.js` to adjust:
- `recognition.lang`: Language setting
- `utterance.rate`: Speech speed
- `utterance.pitch`: Voice pitch

## 🐛 Troubleshooting

### Common Issues

**"Model not loading"**
- Ensure you have sufficient RAM (2GB+ recommended)
- Check internet connection for model download
- Try running `python test_model.py` to diagnose

**"Speech recognition not working"**
- Check microphone permissions in browser
- Use HTTPS or localhost (required for Web Speech API)
- Try Chrome or Edge browser

**"Backend connection failed"**
- Ensure Flask server is running on port 5000
- Check for firewall blocking
- Verify CORS settings in `app.py`

**"Empty responses"**
- Check model loading in backend logs
- Try simpler inputs first
- Verify database is initialized

### Performance Tips

- **First run**: Model download may take 5-10 minutes
- **Response time**: 2-6 seconds for local inference
- **Memory usage**: ~2GB RAM for DialoGPT-small
- **Browser**: Chrome/Edge recommended for best Web Speech API support

## 📊 Success Metrics

- ✅ Voice input captured and transcribed accurately
- ✅ AI responses generated within 2-6 seconds
- ✅ Text-to-speech working smoothly
- ✅ Conversation history persisted
- ✅ Multiple conversation turns maintained
- ✅ Error handling graceful

## 🔮 Future Enhancements

### Semester 8+ Roadmap
- **Avatar Integration**: 3D/2D digital human rendering
- **Advanced Models**: GPT-3.5/4, Claude, or local fine-tuned models
- **Multi-language Support**: Internationalization
- **Emotion Detection**: Voice emotion analysis
- **Vector Database**: Pinecone for long-term memory
- **Real-time Streaming**: WebSocket for faster responses
- **Mobile App**: React Native or Flutter
- **Cloud Deployment**: AWS/Azure with auto-scaling

### Technical Upgrades
- **Backend**: FastAPI for better performance
- **Frontend**: React/Vue.js for complex UI
- **Database**: PostgreSQL for production scale
- **Caching**: Redis for session management
- **Monitoring**: Prometheus + Grafana
- **CI/CD**: GitHub Actions for automated testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Product Manager**: ConversAI MVP Team
- **Technical Lead**: ConversAI MVP Team
- **Code Generator**: Cursor AI Assistant

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the test results from `python test_model.py`
3. Check browser console for frontend errors
4. Check backend logs for server errors

---

**Happy Conversing! 🤖💬**

*Built with ❤️ for Semester 7 MVP validation*