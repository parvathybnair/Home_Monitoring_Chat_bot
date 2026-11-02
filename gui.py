"""
Home Monitoring Chatbot - GUI Interface (Optional)
Uses tkinter for a simple chat window interface

To enable: Uncomment the import in main.py and replace run_chat_loop() with run_gui_app()
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
from home_monitor import chatbot_response, get_home_status


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏠 Home Monitoring Chatbot")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        
        # Header
        header = tk.Label(
            root,
            text="Home Monitoring Chatbot",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            root,
            height=20,
            width=70,
            font=("Arial", 10),
            bg="white",
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="#2980b9", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("bot", foreground="#27ae60", font=("Arial", 10))
        self.chat_display.tag_config("system", foreground="#e74c3c", font=("Arial", 9, "italic"))
        
        # Input frame
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Input field
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 10),
            bg="white",
            relief=tk.FLAT,
            bd=2
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Send button
        self.send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=20
        )
        self.send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Status button
        self.status_btn = tk.Button(
            input_frame,
            text="Status",
            command=self.show_status,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10),
            relief=tk.FLAT,
            padx=15
        )
        self.status_btn.pack(side=tk.LEFT)
        
        # Welcome message
        self.display_message(
            "Welcome to Home Monitoring Chatbot! 🏠\n"
            "Ask me about your home status. Type 'help' for suggestions.\n"
            "Click 'Status' to see full home report.\n",
            "system"
        )
        
        # Focus on input field
        self.input_field.focus()
    
    def display_message(self, message, tag="bot"):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n", tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        """Handle user message"""
        user_input = self.input_field.get().strip()
        
        if not user_input:
            return
        
        # Display user message
        self.display_message(f"You: {user_input}", "user")
        self.input_field.delete(0, tk.END)
        
        # Get bot response
        response = chatbot_response(user_input)
        self.display_message(f"Bot: {response}", "bot")
    
    def show_status(self):
        """Display full home status"""
        status = get_home_status()
        self.display_message(f"Bot:{status}", "bot")


def run_gui_app():
    """Launch GUI application"""
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui_app()
