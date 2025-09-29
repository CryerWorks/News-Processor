#!/usr/bin/env python3
"""
Mundus News Digest Generator - Web Application Launcher
Platform-agnostic launcher for the web-based news processing application.
"""

import os
import sys
import webbrowser
import time
import threading
from app import app, socketio

def open_browser():
    """Open the web browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

def main():
    """Main function to run the web application"""
    print("🚀 Starting Mundus News Digest Generator Web Application...")
    print("=" * 60)
    print("Platform: Cross-platform web application")
    print("Access URL: http://localhost:5000")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        print("=" * 60)
    
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Run the Flask-SocketIO application
        print("🌐 Starting web server...")
        print("✅ Application ready! Your browser should open automatically.")
        print("📱 Access from other devices on your network using your IP address")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        socketio.run(
            app, 
            debug=False, 
            host='0.0.0.0', 
            port=5000,
            allow_unsafe_werkzeug=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Mundus News Digest Generator...")
        print("Thank you for using our application!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("Please check your installation and try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()
