# 🎯 Quick Start Guide

Get your Home Monitoring Chatbot running in **5 minutes**!

## ⚡ Super Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup .env (copy the template)
cp .env.example .env

# 3. Edit .env and add your API key
# Get key from: https://console.api.nvidia.com

# 4. Run the web server
python web_server.py

# 5. Open in browser
# http://localhost:5000
```

Done! 🎉

---

## 📝 Step-by-Step Setup

### Step 1: Get API Key

1. Go to: https://console.api.nvidia.com
2. Create account or login
3. Find "API Keys" section
4. Click "Create New API Key"
5. Copy the key (looks like: `nvapi_xxxxx`)

### Step 2: Configure .env

1. Open `.env` file in your editor
2. Find this line: `API_KEY=your_nvidia_api_key_here`
3. Replace `your_nvidia_api_key_here` with your actual key
4. Save the file

Example:
```
API_KEY=nvapi_1234567890abcdefghijk
API_BASE_URL=https://integrate.api.nvidia.com/v1
MODEL=deepseek-ai/deepseek-v4-pro
TEMPERATURE=0.5
MAX_TOKENS=200
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - AI API client
- `python-dotenv` - Load .env files
- `Flask` - Web framework
- `Flask-CORS` - Enable cross-origin requests

### Step 4: Run the Server

```bash
python web_server.py
```

You should see:
```
🌐 HOME MONITORING CHATBOT - WEB SERVER
✅ API Key found and validated
🚀 Starting Flask server...
📍 Open your browser:
   http://localhost:5000
```

### Step 5: Open in Browser

Go to: **http://localhost:5000**

You should see:
- Chat box on the right
- Home status sidebar on the left
- Welcome message from the chatbot

### Step 6: Test It!

Try asking:
- "Is the front door open?"
- "What's the temperature?"
- "Show me home status"

---

## 🌐 Running the Web Interface

**Default:**
```bash
python web_server.py
```
Runs on: http://localhost:5000

**Custom port:**
```bash
flask --app app run --port 8000
```

**Production:**
```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 4
```

---

## 💻 Using CLI Instead

Don't want the web interface? Use the command line:

```bash
python main.py
```

Then type questions:
```
You: Is the front door open?
Bot: Yes, the front door is currently open...
```

Type `exit` to quit.

---

## 📂 File Guide

| File | Purpose |
|------|---------|
| `web_server.py` | 🌐 Run the web dashboard |
| `main.py` | 💻 Run CLI chatbot |
| `app.py` | 🔧 Flask API server |
| `home_monitor.py` | 🤖 Chatbot logic |
| `.env` | 🔑 Your API key (keep secret!) |
| `.env.example` | 📋 Template for .env |
| `README.md` | 📚 Full documentation |
| `SETUP.md` | 🔐 API key setup details |
| `DEPLOYMENT.md` | 🚀 Deploy to cloud |

---

## 🆘 Common Issues

### "API_KEY not found"
- Did you create `.env` file from `.env.example`?
- Did you add your API key?
- Is the key correct?

**Solution:** Follow Step 2 above carefully

### "Port 5000 already in use"
```bash
# Try a different port
flask --app app run --port 8000
```

### "Website doesn't load"
- Is Flask running? (Check terminal)
- Did it say "Running on..."?
- Try refreshing: Ctrl+Shift+R (hard refresh)

### "Chat is not responding"
- Check your internet connection
- Verify API key is correct
- Try restarting: `python web_server.py`

---

## 💡 Tips

### Auto-reload on changes
Flask's debug mode auto-reloads when you edit files. Changes appear instantly!

### Clear chat history
Click the "Clear" button in the top-right corner

### Refresh home status
Click the ↻ button next to "Home Status"

### Status auto-refreshes
Home status refreshes automatically every 30 seconds

---

## 🎯 What's Next?

- **Deploy online** → See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Customize home state** → Edit `home_state` in `home_monitor.py`
- **Add real IoT** → Integrate with Arduino/Raspberry Pi
- **Enable voice** → Add SpeechRecognition library

---

**Ready?** Run `python web_server.py` and enjoy! 🚀
