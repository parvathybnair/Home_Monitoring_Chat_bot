"""
Home Monitoring Chatbot - Web Server Entry Point
Quick launcher for the Flask web interface

Run with: python web_server.py
Or: python -m flask --app app run
"""

import sys
import os

# Ensure .env is loaded
from dotenv import load_dotenv
load_dotenv()

# Check if API key exists
if not os.getenv('API_KEY'):
    print("❌ ERROR: API_KEY not found in .env file!")
    print("\n📋 Quick Setup:")
    print("  1. Copy .env.example to .env:")
    print("     cp .env.example .env")
    print("  2. Add your NVIDIA API key to .env")
    print("  3. See SETUP.md for detailed instructions")
    sys.exit(1)

# Import and run Flask app
from app import app

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 HOME MONITORING CHATBOT - WEB SERVER")
    print("="*60)
    print("\n✅ API Key found and validated")
    print("\n🚀 Starting Flask server...")
    print("\n📍 Open your browser:")
    print("   http://localhost:5000")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
