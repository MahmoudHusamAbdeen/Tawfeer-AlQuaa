#!/usr/bin/env python3
"""
Tawfeer Backend - Quick Start Script
This script checks prerequisites and starts the server.
"""
import subprocess
import sys
import os

def check_python():
    """Check if Python 3.9+ is installed."""
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"  Python: {version}")
        return True
    except Exception:
        print("  ERROR: Python 3.9+ is required but not found!")
        return False

def check_mongodb():
    """Check if MongoDB is running."""
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
        client.server_info()
        print("  MongoDB: Connected")
        return True
    except Exception:
        print("  MongoDB: NOT RUNNING - Please start MongoDB first!")
        print("    - Windows: Start MongoDB service or run 'mongod'")
        print("    - Mac: brew services start mongodb-community")
        print("    - Linux: sudo systemctl start mongod")
        return False

def install_dependencies():
    """Install Python dependencies."""
    print("\nInstalling dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("  Dependencies installed successfully!")
        return True
    except Exception as e:
        print(f"  ERROR: Failed to install dependencies: {e}")
        return False

def check_env_file():
    """Check if .env file exists."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        print("  .env file: Found")
        return True
    else:
        print("  .env file: NOT FOUND - Creating from .env.example")
        example_path = os.path.join(os.path.dirname(__file__), ".env.example")
        if os.path.exists(example_path):
            import shutil
            shutil.copy(example_path, env_path)
            print("  Created .env from .env.example - Please update with your values!")
            return True
        return False

def start_server():
    """Start the FastAPI server."""
    print("\nStarting Tawfeer Backend Server...")
    print("=" * 50)
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"ERROR: Failed to start server: {e}")

if __name__ == "__main__":
    print("Tawfeer Backend - Setup & Start")
    print("=" * 50)

    # Check prerequisites
    print("\nChecking prerequisites...")
    if not check_python():
        sys.exit(1)

    if not check_env_file():
        sys.exit(1)

    if not install_dependencies():
        sys.exit(1)

    if not check_mongodb():
        print("\nWARNING: MongoDB is not running. The server will start but database operations will fail.")
        print("Start MongoDB and restart the server.")

    # Start server
    start_server()
