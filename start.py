#!/usr/bin/env python3
"""
ConversAI MVP Launcher
Quick start script for the application
Author: ConversAI MVP
Run: python start.py
"""

import os
import sys
import subprocess
import platform
import webbrowser
import time
import threading

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    ConversAI MVP Launcher                   ║
║              AI Driven Digital Human - Voice Chat           ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_setup():
    """Check if the application is properly set up"""
    print("🔍 Checking setup...")
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("❌ Virtual environment not found. Please run 'python3 setup.py' first.")
        return False
    
    # Check if requirements are installed
    if not os.path.exists("backend/requirements.txt"):
        print("❌ Backend requirements not found.")
        return False
    
    # Check if database exists
    if not os.path.exists("backend/conversations.db"):
        print("⚠️  Database not found. Initializing...")
        try:
            if platform.system() == "Windows":
                python_cmd = "venv\\Scripts\\python"
            else:
                python_cmd = "venv/bin/python"
            
            subprocess.run(f"{python_cmd} -c \"from backend.database import init_db; init_db()\"", 
                         shell=True, check=True)
            print("✅ Database initialized")
        except:
            print("❌ Failed to initialize database")
            return False
    
    print("✅ Setup looks good!")
    return True

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting backend server...")
    
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    try:
        # Start the Flask app
        subprocess.run([python_cmd, "backend/app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def open_browser():
    """Open the web browser after a short delay"""
    time.sleep(3)  # Wait for server to start
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:5000")

def main():
    """Main launcher function"""
    print_banner()
    
    # Check setup
    if not check_setup():
        print("\n❌ Setup incomplete. Please run 'python setup.py' first.")
        return False
    
    print("\n🎯 Starting ConversAI MVP...")
    print("📝 Instructions:")
    print("   - The backend server will start on port 5000")
    print("   - Your browser will open automatically")
    print("   - Click the microphone button to start talking")
    print("   - Press Ctrl+C to stop the server")
    print("\n" + "="*60)
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the backend server
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n👋 Thanks for using ConversAI MVP!")
    
    return True

if __name__ == "__main__":
    main()
