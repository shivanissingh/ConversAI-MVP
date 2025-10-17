"""
Flask backend server for ConversAI MVP
Provides API endpoints for voice-to-voice conversation
Author: ConversAI MVP
Run: python app.py
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import uuid
import os
import logging
from datetime import datetime

# Import our modules
from model import get_response
from database import init_db, save_conversation, get_recent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=['http://localhost:5001', 'http://127.0.0.1:5001'])
# Initialize database
init_db()

@app.route('/')
def serve_frontend():
    """Serve the main frontend page"""
    try:
        return send_from_directory('../frontend', 'index.html')
    except Exception as e:
        logger.error(f"Error serving frontend: {e}")
        return jsonify({"error": True, "message": "Frontend not available"}), 500

@app.route('/style.css')
def serve_css():
    """Serve the CSS file"""
    return send_from_directory('../frontend', 'style.css')

@app.route('/script.js')
def serve_js():
    """Serve the JavaScript file"""
    return send_from_directory('../frontend', 'script.js')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Accepts: {"message": "user input", "session_id": "optional session id"}
    Returns: {"reply": "bot response", "session_id": "session id"}
    """
    try:
        # Parse JSON request
        data = request.get_json()
        if not data:
            return jsonify({"error": True, "message": "No JSON data provided"}), 400
        
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({"error": True, "message": "No message provided"}), 400
        
        logger.info(f"Received message: '{user_message}' for session: {session_id}")
        
        # Get response from model
        bot_response = get_response(user_message, session_id)
        
        # Save conversation to database
        save_conversation(session_id, user_message, bot_response)
        
        logger.info(f"Generated response: '{bot_response}'")
        
        return jsonify({
            "reply": bot_response,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            "error": True, 
            "message": "Internal server error occurred"
        }), 500

@app.route('/api/history/<session_id>')
def get_history(session_id):
    """Get conversation history for a session"""
    try:
        conversations = get_recent(session_id, limit=20)
        return jsonify({
            "session_id": session_id,
            "conversations": [
                {
                    "id": conv[0],
                    "user_input": conv[2],
                    "bot_response": conv[3],
                    "timestamp": conv[4]
                }
                for conv in conversations
            ]
        })
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({"error": True, "message": "Failed to retrieve history"}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": True  # You could check if model is actually loaded
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": True, "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": True, "message": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting ConversAI MVP Backend...")
    print("Frontend will be available at: http://localhost:5001")
    print("API endpoints:")
    print("  POST /api/chat - Main chat endpoint")
    print("  GET /api/history/<session_id> - Get conversation history")
    print("  GET /api/health - Health check")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
