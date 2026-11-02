"""
Home Monitoring Chatbot - Main Entry Point
Run with: python main.py
"""

import sys
from home_monitor import run_chat_loop

# Optional: Uncomment below to add GUI support in the future
# from gui import run_gui_app


def main():
    """Main entry point"""
    print("Starting Home Monitoring Chatbot...\n")
    
    # Launch CLI chat interface
    run_chat_loop()
    
    # Uncomment below to launch GUI instead:
    # run_gui_app()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)