"""
Flask Web Server for Home Monitoring Chatbot
Run with: python app.py
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_cors import CORS
import os
import sqlite3
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from home_monitor import chatbot_response, get_home_status, home_state

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY', 'super-secret-homeguard-key-2026')
CORS(app)

# Initialize DB for users
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(id=user[0], username=user[1])
    return None

# Store chat history
chat_history = []


@app.route('/')
@login_required
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user_data = c.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[2], password):
            user = User(id=user_data[0], username=user_data[1])
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        flash('Username already exists', 'error')
        conn.close()
        return redirect(url_for('login'))
        
    hashed_password = generate_password_hash(password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    
    flash('Account created successfully! Please login.', 'success')
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get bot response (now returns dict with response + alexa commands)
        result = chatbot_response(user_message)
        
        # Store in history
        chat_history.append({
            'role': 'user',
            'content': user_message
        })
        chat_history.append({
            'role': 'bot',
            'content': result['response']
        })
        
        return jsonify({
            'success': True,
            'response': result['response'],
            'alexa_commands': result.get('commands', []),
            'alexa_results': result.get('alexa_results', [])
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Get current home status"""
    try:
        return jsonify({
            'success': True,
            'status': get_home_status(),
            'state': home_state
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/update', methods=['POST'])
def update():
    """Update home state (simulation)"""
    try:
        data = request.json
        key = data.get('key')
        value = data.get('value')
        
        # Update nested keys (e.g., "doors.front")
        keys = key.split('.')
        current = home_state
        
        for k in keys[:-1]:
            if k in current:
                current = current[k]
            else:
                return jsonify({'error': f'Invalid key path: {key}'}), 400
        
        if keys[-1] in current:
            current[keys[-1]] = value
            return jsonify({
                'success': True,
                'message': f'Updated {key} to {value}',
                'state': home_state
            })
        else:
            return jsonify({'error': f'Key not found: {key}'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def history():
    """Get chat history"""
    return jsonify({
        'success': True,
        'history': chat_history
    })


@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return jsonify({
        'success': True,
        'message': 'Chat history cleared'
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Check if API key is configured
    api_key = os.getenv('API_KEY')
    if not api_key:
        print("[WARNING] API_KEY not found in .env file!")
        print("Please set up your .env file before running the web server.")
        print("See SETUP.md for instructions.")
        exit(1)
    
    print("\n" + "="*60)
    print("[HOME] HOME MONITORING CHATBOT - WEB SERVER")
    print("="*60)
    print("\n[WEB] Open your browser and go to: http://localhost:5000")
    print("\n[API] Endpoints:")
    print("   POST /api/chat       - Send a message")
    print("   GET  /api/status     - Get home status")
    print("   POST /api/update     - Update home state")
    print("   GET  /api/history    - Get chat history")
    print("   POST /api/clear-history - Clear chat")
    print("\n" + "="*60 + "\n")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
