"""
Database interface for ConversAI MVP
Handles SQLite operations for conversation storage and retrieval
Author: ConversAI MVP
Run: python -c "from database import init_db; init_db()"
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional

DB_PATH = "conversations.db"

def init_db():
    """Initialize the SQLite database with conversations table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_input TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def save_conversation(session_id: str, user_input: str, bot_response: str) -> bool:
    """
    Save a conversation turn to the database
    
    Args:
        session_id: Unique identifier for the conversation session
        user_input: What the user said
        bot_response: What the bot replied
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (session_id, user_input, bot_response)
            VALUES (?, ?, ?)
        ''', (session_id, user_input, bot_response))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return False

def get_recent(session_id: str, limit: int = 10) -> List[Tuple]:
    """
    Get recent conversations for a session
    
    Args:
        session_id: Session to retrieve conversations for
        limit: Maximum number of conversations to return
        
    Returns:
        List of tuples: (id, session_id, user_input, bot_response, timestamp)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, session_id, user_input, bot_response, timestamp
            FROM conversations
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"Error retrieving conversations: {e}")
        return []

def get_all_sessions() -> List[str]:
    """Get all unique session IDs from the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT session_id
            FROM conversations
            ORDER BY timestamp DESC
        ''')
        
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results
    except Exception as e:
        print(f"Error retrieving sessions: {e}")
        return []

if __name__ == "__main__":
    # Test database initialization
    init_db()
    print("Database setup complete!")
