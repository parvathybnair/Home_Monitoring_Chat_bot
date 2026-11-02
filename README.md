# 🏠 Home Monitoring Chatbot

An AI-powered chatbot that monitors home status using NVIDIA's Deepseek AI model. Ask it about doors, windows, temperature, and more! Features both a **CLI interface** and a **modern web dashboard**.

## 📋 Features

- ✅ **Web Dashboard** - Modern, responsive chat interface with live home status
- ✅ **CLI Interface** - Command-line chatbot for quick queries
- ✅ Real-time home status monitoring (doors, windows, temperature, humidity)
- ✅ AI-powered natural language responses
- ✅ Motion detection alerts
- ✅ Secure API key management with `.env` files
- ✅ Extensible architecture for IoT integration
- ✅ REST API endpoints for integration

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup API Key (IMPORTANT!)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Get your free NVIDIA API key:
   - Visit: https://console.api.nvidia.com
   - Create an account and generate an API key
   - Copy the key to your `.env` file

3. Your `.env` should look like:
   ```
   API_KEY=your_actual_api_key_here
   API_BASE_URL=https://integrate.api.nvidia.com/v1
   MODEL=deepseek-ai/deepseek-v4-pro
   ```

### 3. Choose Your Interface

#### 🌐 Web Dashboard (Recommended)
```bash
python web_server.py
```
Then open: **http://localhost:5000**

Features:
- Beautiful chat interface
- Real-time home status sidebar
- Status refresh button
- Chat history management
- Mobile responsive design

#### 💻 Command-Line Interface
```bash
python main.py
```

Features:
- Quick text-based interaction
- Perfect for scripting
- Lightweight and fast

## 🎯 Example Usage

### Via Web Dashboard
1. Open http://localhost:5000 in your browser
2. Ask questions in the chat box
3. View real-time home status on the sidebar

**Example queries:**
- "Is the back door open?"
- "What's the current temperature?"
- "Any motion detected?"
- "Show me the complete home status"

### Via CLI
```
You: Is the back door open?
Bot: Yes, the back door is currently open. You may want to close it if you weren't expecting that.

You: What's the current temperature?
Bot: The current temperature is 25°C with humidity at 45%. Your home is at a comfortable temperature.

You: status
Bot: [Shows complete home status report]
```

## 🔐 Security Best Practices

⚠️ **NEVER:**
- Commit `.env` file to Git
- Paste API keys in public code
- Share your `.env` file

✅ **ALWAYS:**
- Use `.env.example` as a template
- Add `.env` to `.gitignore` (already done)
- Regenerate keys if accidentally exposed

## 📁 Project Structure

```
home_monitor_chatbot/
├── main.py                 # CLI entry point
├── web_server.py          # Web server entry point
├── app.py                 # Flask application & API
├── home_monitor.py        # Core chatbot logic
├── gui.py                 # Optional Tkinter GUI
├── requirements.txt       # Python dependencies
├── .env.example           # API config template
├── .env                   # Your actual credentials (not committed)
├── .gitignore             # Git ignore rules
├── README.md             # This file
├── SETUP.md              # API key setup guide
├── templates/            # Flask templates
│   └── index.html        # Web dashboard HTML
└── static/               # Static files
    ├── style.css         # Dashboard styling
    └── script.js         # Frontend JavaScript
```

## 🔌 REST API Endpoints

If you're building integrations, use these endpoints:

```bash
# Send a chat message
POST /api/chat
Body: { "message": "Is the front door open?" }
Response: { "success": true, "response": "Yes, the front door..." }

# Get current home status
GET /api/status
Response: { "success": true, "state": {...}, "status": "..." }

# Update home state (for testing)
POST /api/update
Body: { "key": "doors.front", "value": "open" }
Response: { "success": true, "state": {...} }

# Get chat history
GET /api/history
Response: { "success": true, "history": [...] }

# Clear chat history
POST /api/clear-history
Response: { "success": true, "message": "Chat history cleared" }
```

**Example using curl:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the temperature?"}'
```

## 🎯 Deployment Options

### Local Development (Recommended for testing)
```bash
python web_server.py
```
Accessible at: http://localhost:5000

### Production Deployment

**Using Gunicorn** (recommended for production):
```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 4
```

**Using Docker** (optional):
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
```

Then build and run:
```bash
docker build -t home-monitor .
docker run -p 5000:5000 --env-file .env home-monitor
```

## 🎯 Example Usage

```
You: Is the back door open?
Bot: Yes, the back door is currently open. You may want to close it if you weren't expecting that.

You: What's the current temperature?
Bot: The current temperature is 25°C with humidity at 45%. Your home is at a comfortable temperature.

You: status
Bot: [Shows complete home status report]
```

## 🔮 Future Enhancements

- [x] Web Dashboard with Flask
- [x] REST API endpoints
- [ ] Tkinter GUI interface
- [ ] Real IoT device integration (Raspberry Pi, Arduino)
- [ ] Mobile app integration
- [ ] Voice commands (SpeechRecognition library)
- [ ] Automated alerts & notifications
- [ ] Dashboard with graphs & history
- [ ] Machine learning anomaly detection

## 📞 Troubleshooting

**Error: API_KEY not found**
- Make sure you've created `.env` file from `.env.example`
- Check that your API key is correctly pasted
- Run: `pip install -r requirements.txt`

**Error: Port 5000 already in use**
```bash
# Use a different port
flask --app app run --port 5001
```

**Error: Connection failed when opening website**
- Check if Flask server is running (`python web_server.py`)
- Verify API key is valid in `.env` file
- Check your internet connection

**Website doesn't load the status sidebar**
- Make sure Flask server has started (watch console for "Running on")
- Try refreshing the page (F5 or Cmd+R)
- Check browser console for JavaScript errors (F12)

## 📚 References

- [OpenAI Python Client](https://github.com/openai/openai-python)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [NVIDIA API Console](https://console.api.nvidia.com)
- [Deepseek Model Documentation](https://deepseek.com/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
