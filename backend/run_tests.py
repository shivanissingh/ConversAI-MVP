#!/usr/bin/env python3
"""
Comprehensive test suite for ConversAI MVP
Runs all tests and provides detailed reporting
Author: ConversAI MVP
Run: python run_tests.py
"""

import sys
import os
import time
import subprocess
import requests
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_test_result(test_name, success, details=""):
    """Print test result with formatting"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{test_name:<40} {status}")
    if details:
        print(f"  Details: {details}")

def test_imports():
    """Test that all required modules can be imported"""
    print_header("Testing Imports")
    
    tests = [
        ("Flask", lambda: __import__('flask')),
        ("Flask-CORS", lambda: __import__('flask_cors')),
        ("Transformers", lambda: __import__('transformers')),
        ("Torch", lambda: __import__('torch')),
        ("Database module", lambda: __import__('database')),
        ("Model module", lambda: __import__('model')),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            test_func()
            print_test_result(test_name, True)
            results.append(True)
        except ImportError as e:
            print_test_result(test_name, False, str(e))
            results.append(False)
    
    return all(results)

def test_database():
    """Test database operations"""
    print_header("Testing Database Operations")
    
    try:
        from database import init_db, save_conversation, get_recent
        
        # Test database initialization
        init_db()
        print_test_result("Database initialization", True)
        
        # Test saving conversation
        test_session = "test_session_" + str(int(time.time()))
        success = save_conversation(test_session, "Hello", "Hi there!")
        print_test_result("Save conversation", success)
        
        # Test retrieving conversation
        conversations = get_recent(test_session, 1)
        success = len(conversations) > 0
        print_test_result("Retrieve conversation", success, f"Found {len(conversations)} conversations")
        
        return True
        
    except Exception as e:
        print_test_result("Database operations", False, str(e))
        return False

def test_model_loading():
    """Test model loading and basic inference"""
    print_header("Testing Model Loading")
    
    try:
        from model import get_model
        
        print("Loading model (this may take a few minutes on first run)...")
        start_time = time.time()
        model = get_model()
        load_time = time.time() - start_time
        
        if model.model is not None and model.tokenizer is not None:
            print_test_result("Model loading", True, f"Loaded in {load_time:.2f}s")
            
            # Test basic inference
            test_response = model.get_response("Hello", "test_session")
            success = test_response and len(test_response) > 0
            print_test_result("Basic inference", success, f"Response: '{test_response[:50]}...'")
            
            return True
        else:
            print_test_result("Model loading", False, "Model or tokenizer is None")
            return False
            
    except Exception as e:
        print_test_result("Model loading", False, str(e))
        return False

def test_flask_app():
    """Test Flask application startup and endpoints"""
    print_header("Testing Flask Application")
    
    try:
        # Import the app
        from app import app
        
        # Test app creation
        print_test_result("Flask app creation", True)
        
        # Test app configuration
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            success = response.status_code == 200
            print_test_result("Health endpoint", success, f"Status: {response.status_code}")
            
            # Test chat endpoint
            response = client.post('/api/chat', 
                                 json={'message': 'Hello', 'session_id': 'test'},
                                 content_type='application/json')
            success = response.status_code == 200
            print_test_result("Chat endpoint", success, f"Status: {response.status_code}")
            
            if success:
                data = response.get_json()
                print_test_result("Chat response format", 'reply' in data, f"Keys: {list(data.keys())}")
        
        return True
        
    except Exception as e:
        print_test_result("Flask application", False, str(e))
        return False

def test_frontend_files():
    """Test that frontend files exist and are valid"""
    print_header("Testing Frontend Files")
    
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    required_files = ['index.html', 'style.css', 'script.js']
    
    results = []
    for filename in required_files:
        filepath = os.path.join(frontend_dir, filename)
        exists = os.path.exists(filepath)
        print_test_result(f"Frontend file: {filename}", exists)
        results.append(exists)
    
    return all(results)

def test_integration():
    """Test end-to-end integration"""
    print_header("Testing End-to-End Integration")
    
    try:
        from model import get_response
        from database import save_conversation, get_recent
        
        # Simulate a conversation
        session_id = "integration_test_" + str(int(time.time()))
        
        # Test conversation flow
        user_input = "What is artificial intelligence?"
        print(f"User: {user_input}")
        
        # Get AI response
        start_time = time.time()
        ai_response = get_response(user_input, session_id)
        response_time = time.time() - start_time
        
        print(f"AI: {ai_response}")
        print(f"Response time: {response_time:.2f}s")
        
        # Save to database
        save_success = save_conversation(session_id, user_input, ai_response)
        
        # Retrieve from database
        conversations = get_recent(session_id, 1)
        
        success = (ai_response and len(ai_response) > 0 and 
                  save_success and len(conversations) > 0)
        
        print_test_result("End-to-end integration", success, 
                         f"Response time: {response_time:.2f}s")
        
        return success
        
    except Exception as e:
        print_test_result("End-to-end integration", False, str(e))
        return False

def run_performance_test():
    """Run basic performance tests"""
    print_header("Performance Testing")
    
    try:
        from model import get_response
        
        test_inputs = [
            "Hello",
            "How are you?",
            "What can you help me with?",
            "Tell me about machine learning",
            "Goodbye"
        ]
        
        session_id = "perf_test_" + str(int(time.time()))
        response_times = []
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"Test {i}/{len(test_inputs)}: {test_input}")
            start_time = time.time()
            response = get_response(test_input, session_id)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            response_times.append(response_time)
            
            print(f"  Response: {response[:50]}...")
            print(f"  Time: {response_time:.2f}ms")
        
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        print(f"\nPerformance Summary:")
        print(f"  Average response time: {avg_time:.2f}ms")
        print(f"  Min response time: {min_time:.2f}ms")
        print(f"  Max response time: {max_time:.2f}ms")
        
        # Consider it successful if average is under 10 seconds
        success = avg_time < 10000
        print_test_result("Performance test", success, f"Avg: {avg_time:.2f}ms")
        
        return success
        
    except Exception as e:
        print_test_result("Performance test", False, str(e))
        return False

def main():
    """Run all tests"""
    print("ConversAI MVP - Comprehensive Test Suite")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    test_results = []
    
    test_results.append(("Imports", test_imports()))
    test_results.append(("Database", test_database()))
    test_results.append(("Model Loading", test_model_loading()))
    test_results.append(("Flask App", test_flask_app()))
    test_results.append(("Frontend Files", test_frontend_files()))
    test_results.append(("Integration", test_integration()))
    test_results.append(("Performance", run_performance_test()))
    
    # Print summary
    print_header("Test Summary")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your ConversAI MVP is ready to use!")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Start conversing with your AI!")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Check Python version (3.8+ required)")
        print("- Ensure sufficient RAM (2GB+ recommended)")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
