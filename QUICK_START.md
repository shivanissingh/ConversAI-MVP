# ConversAI MVP - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Setup (One-time)
```bash
# Clone and navigate to project
cd ConversAI-MVP

# Run automated setup
python3 setup.py
```

### 2. Launch
```bash
# Start the application
python3 start.py
```

### 3. Use
- Browser opens automatically to `http://localhost:5000`
- Click the microphone button 🎤
- Speak clearly into your microphone
- AI responds in text and voice!

## 📋 Manual Verification Checklist

After running the setup, verify these work:

- [ ] **Backend starts**: `python3 backend/app.py` runs without errors
- [ ] **Frontend loads**: Browser shows ConversAI interface
- [ ] **Voice input**: Microphone button responds and captures speech
- [ ] **AI responses**: Bot generates relevant text responses
- [ ] **Text-to-speech**: AI responses are spoken aloud
- [ ] **Database**: Conversations are saved (check `backend/conversations.db`)

## 🧪 Test Commands

```bash
# Test the AI model
python3 backend/test_model.py

# Run comprehensive tests
python3 backend/run_tests.py

# Check database
python3 -c "from backend.database import get_all_sessions; print(get_all_sessions())"
```

## 🐛 Quick Fixes

**"Module not found" errors:**
```bash
# Reinstall dependencies
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
```

**"Voice not working":**
- Use Chrome or Edge browser
- Check microphone permissions
- Try HTTPS or localhost (required for Web Speech API)

**"Model loading slow":**
- First run downloads ~500MB model
- Ensure 2GB+ RAM available
- Check internet connection

## 📊 Success Metrics

Your MVP is working if:
- ✅ Voice input captured and transcribed
- ✅ AI responses generated in 2-6 seconds
- ✅ Text-to-speech working
- ✅ Conversation history saved
- ✅ Multiple conversation turns work

## 🎯 Next Steps

1. **Test with real users** - Get 3-5 people to try it
2. **Collect feedback** - Note what works/doesn't work
3. **Iterate quickly** - Fix 1-3 issues per week
4. **Plan Semester 8** - Add avatar, better models, mobile app

---

**Happy Conversing! 🤖💬**

*Built for Semester 7 MVP validation*
