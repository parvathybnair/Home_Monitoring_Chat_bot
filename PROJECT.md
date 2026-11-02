# 🏠 Home Monitoring Chatbot - Project Overview

## 🎉 What We Built

A **complete AI-powered home monitoring chatbot website** with:

- ✨ **Modern Web Dashboard** - Beautiful, responsive interface
- 🤖 **AI Assistant** - NVIDIA Deepseek powered responses
- 📊 **Live Status Display** - Real-time home monitoring
- 💬 **Chat Interface** - Ask natural language questions
- 🔌 **REST API** - Full API for integrations
- 🔐 **Security** - Secure API key management
- 📱 **Mobile Ready** - Works on all devices
- 🚀 **Production Ready** - Deploy anywhere

---

## 📁 Project Files

### Core Application
| File | Purpose |
|------|---------|
| `app.py` | Flask backend & REST API |
| `home_monitor.py` | AI chatbot engine |
| `web_server.py` | Web server launcher |
| `main.py` | CLI interface |

### Frontend
| File | Purpose |
|------|---------|
| `templates/index.html` | Web dashboard UI |
| `static/style.css` | Modern styling |
| `static/script.js` | Frontend logic |

### Configuration & Security
| File | Purpose |
|------|---------|
| `.env.example` | Config template |
| `.env` | Your API key (keep secret!) |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Prevents key commits |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | **← Start here!** Complete guide |
| `QUICKSTART.md` | 5-minute setup |
| `SETUP.md` | API key configuration |
| `DEPLOYMENT.md` | Deploy to cloud |

---

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment file
cp .env.example .env

# 3. Add your NVIDIA API key to .env
# Get it from: https://console.api.nvidia.com

# 4. Run the web server
python web_server.py

# 5. Open browser
# http://localhost:5000
```

---

## 🎯 Features

### Web Dashboard
- **Left Sidebar**: Real-time home status
  - Doors & Windows status
  - Temperature & Humidity
  - Lights (on/off)
  - Motion detection
  - Refresh button
  
- **Chat Area**: Ask the AI anything
  - Beautiful message display
  - Timestamp on each message
  - Auto-scroll to latest
  - Clear history button

### Home Status Monitoring
```
Doors: front (closed), back (open), garage (closed)
Windows: living_room (closed), kitchen (open), bedroom (closed)
Temperature: 25°C
Humidity: 45%
Motion: No
Lights: living_room (on), kitchen (off), bedroom (off)
```

### AI Responses
Ask natural questions like:
- "Is the front door open?"
- "What's the temperature?"
- "Any motion detected?"
- "Show me home status"

---

## 💻 Two Ways to Use

### 🌐 Web Interface (Recommended)
```bash
python web_server.py
# Visit: http://localhost:5000
```

### 💻 Command Line
```bash
python main.py
# Use terminal for chat
```

---

## 🔧 REST API Endpoints

Use these to build other apps:

```bash
# Chat message
POST /api/chat
{"message": "Is the door open?"}

# Get home status
GET /api/status

# Update state (testing)
POST /api/update
{"key": "doors.front", "value": "open"}

# Chat history
GET /api/history

# Clear chat
POST /api/clear-history
```

---

## 📱 UI Features

### Dashboard Layout
- **Left Panel** (320px): Home status
- **Right Panel** (Main): Chat interface
- **Responsive**: Works on mobile (stacks vertically)

### Chat Styling
- User messages: Blue gradient (right-aligned)
- Bot messages: Light gray (left-aligned)
- Timestamps on each message
- Auto-scroll to latest

### Status Display
- Color-coded status:
  - **Red**: Doors/Windows open
  - **Green**: Doors/Windows closed
  - **Orange**: Temperature/Humidity
- Refresh button with animation
- Auto-refresh every 30 seconds

---

## 🔐 Security

### What We Did Right
✅ API key in `.env` (never in code)
✅ `.gitignore` prevents accidental commits
✅ Environment variables for all secrets
✅ `.env.example` shows template

### What You Should Do
✅ Never share `.env` file
✅ Never paste API key in chat
✅ Regenerate if accidentally exposed
✅ Use HTTPS when deployed online

---

## 📊 Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0 (Web framework)
- OpenAI SDK (API client)
- NVIDIA Deepseek (AI model)

**Frontend:**
- HTML5
- CSS3 (with gradients & animations)
- Vanilla JavaScript (no frameworks)
- Font Awesome icons
- Responsive design

**Data Flow:**
```
User Input → Browser JavaScript
                    ↓
            POST /api/chat
                    ↓
        Flask receives message
                    ↓
        OpenAI API (Deepseek)
                    ↓
        Returns AI response
                    ↓
        Browser displays message
        + auto-refresh status
```

---

## 🌐 Deployment Options

**Local Development:**
```bash
python web_server.py
```

**Production with Gunicorn:**
```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 4
```

**Cloud Platforms:**
- ☁️ **Heroku** - $7/month (simple)
- ☁️ **Render** - Free tier available
- ☁️ **DigitalOcean** - $5/month
- ☁️ **AWS** - Pay-as-you-go
- 🐳 **Docker** - Container ready

See **DEPLOYMENT.md** for detailed instructions.

---

## 💡 Customization Ideas

### Easy Tweaks
- Change welcome message in `home_monitor.py`
- Modify home state values
- Adjust colors in `style.css`
- Change auto-refresh interval in `script.js`

### Advanced
- Connect real IoT devices (Arduino/Raspberry Pi)
- Add database for chat history
- Integrate voice commands
- Add alerts & notifications
- Create mobile app

---

## 📖 Documentation

| Document | When to Read |
|----------|------------|
| **README.md** | Complete reference |
| **QUICKSTART.md** | First time setup |
| **SETUP.md** | Getting API key |
| **DEPLOYMENT.md** | Going to production |
| **This file** | Overview & features |

---

## ❓ FAQ

**Q: Do I need to pay for the API?**
A: NVIDIA gives free tier. Deepseek is very cheap (~$0.001 per query).

**Q: Can I deploy this online?**
A: Yes! See DEPLOYMENT.md. Works on Heroku, AWS, DigitalOcean, etc.

**Q: Can I connect real home devices?**
A: Yes! Replace `home_state` in `home_monitor.py` with real sensor data.

**Q: Is my API key safe?**
A: Yes! It's in `.env` which is ignored by Git. Never commit it.

**Q: Can I modify the chatbot's personality?**
A: Yes! Edit the `system_prompt` in `home_monitor.py`.

---

## 🎯 Next Steps

1. ✅ **Setup** → Read QUICKSTART.md
2. ✅ **Get API Key** → Read SETUP.md  
3. ✅ **Run locally** → `python web_server.py`
4. ⏭️ **Customize** → Edit `home_state` in `home_monitor.py`
5. ⏭️ **Deploy** → Read DEPLOYMENT.md
6. ⏭️ **Add features** → Integrate IoT, voice, etc.

---

## 🆘 Troubleshooting

**Problem: "API_KEY not found"**
→ Check SETUP.md section 2

**Problem: "Port 5000 in use"**
→ Run: `flask --app app run --port 8000`

**Problem: "Website won't load"**
→ Is Flask running? (Check terminal for "Running on...")

**Problem: "Chat not responding"**
→ Check internet, verify API key, restart Flask

→ See README.md for more troubleshooting

---

## 📞 Support

- 📖 Read the documentation files
- 🔍 Check TROUBLESHOOTING sections
- 💬 Review code comments
- 📚 Visit: https://console.api.nvidia.com (API docs)

---

**Ready to get started?** 🚀

Run: `python web_server.py` and visit http://localhost:5000

Enjoy your AI-powered home monitoring chatbot! 🏠✨
