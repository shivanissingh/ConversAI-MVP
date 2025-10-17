#!/usr/bin/env python3
"""
ConversAI MVP Setup Script
Automates the initial setup process
Author: ConversAI MVP
Run: python setup.py
"""

import os
import sys
import subprocess
import platform

def print_header(title):
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    else:
        print("✅ Python version is compatible")
        return True

def setup_virtual_environment():
    """Create and activate virtual environment"""
    print_header("Setting up Virtual Environment")
    
    # Check if venv already exists
    if os.path.exists("venv"):
        print("Virtual environment already exists")
        return True
    
    # Create virtual environment
    if not run_command("python3 -m venv venv", "Creating virtual environment"):
        return False
    
    # Determine activation script based on OS
    if platform.system() == "Windows":
        activate_script = "venv\\Scripts\\activate"
        pip_command = "venv\\Scripts\\pip"
    else:
        activate_script = "venv/bin/activate"
        pip_command = "venv/bin/pip"
    
    print(f"\nTo activate the virtual environment, run:")
    if platform.system() == "Windows":
        print(f"  {activate_script}")
    else:
        print(f"  source {activate_script}")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    # Determine pip command based on OS
    if platform.system() == "Windows":
        pip_command = "venv\\Scripts\\pip"
    else:
        pip_command = "venv/bin/pip"
    
    # Upgrade pip first
    if not run_command(f"{pip_command} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{pip_command} install -r backend/requirements.txt", "Installing requirements"):
        return False
    
    return True

def initialize_database():
    """Initialize the SQLite database"""
    print_header("Initializing Database")
    
    # Determine python command based on OS
    if platform.system() == "Windows":
        python_command = "venv\\Scripts\\python"
    else:
        python_command = "venv/bin/python"
    
    if not run_command(f"{python_command} -c \"from backend.database import init_db; init_db()\"", "Initializing database"):
        return False
    
    return True

def run_tests():
    """Run the test suite"""
    print_header("Running Tests")
    
    # Determine python command based on OS
    if platform.system() == "Windows":
        python_command = "venv\\Scripts\\python"
    else:
        python_command = "venv/bin/python"
    
    if not run_command(f"{python_command} backend/run_tests.py", "Running test suite"):
        print("⚠️  Some tests failed, but setup can continue")
        return False
    
    return True

def print_next_steps():
    """Print instructions for next steps"""
    print_header("Setup Complete! Next Steps")
    
    print("🎉 ConversAI MVP is ready to use!")
    print("\nTo start the application:")
    print("1. Activate the virtual environment:")
    
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
        print("2. Start the backend server:")
        print("   python backend\\app.py")
    else:
        print("   source venv/bin/activate")
        print("2. Start the backend server:")
        print("   python backend/app.py")
    
    print("3. Open your browser and go to: http://localhost:5000")
    print("4. Click the microphone button and start talking!")
    
    print("\n📚 Additional Information:")
    print("- Check README.md for detailed documentation")
    print("- Run 'python backend/test_model.py' to test the AI model")
    print("- Run 'python backend/run_tests.py' for comprehensive testing")
    
    print("\n🐛 Troubleshooting:")
    print("- If voice doesn't work, try Chrome or Edge browser")
    print("- Ensure microphone permissions are granted")
    print("- Check that port 5000 is not in use")
    print("- For model loading issues, ensure you have 2GB+ RAM")

def main():
    """Main setup function"""
    print("ConversAI MVP - Automated Setup")
    print("This script will set up your ConversAI MVP environment")
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Python version incompatible")
        return False
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("\n❌ Setup failed: Could not create virtual environment")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        return False
    
    # Initialize database
    if not initialize_database():
        print("\n❌ Setup failed: Could not initialize database")
        return False
    
    # Run tests (optional)
    run_tests()
    
    # Print next steps
    print_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
