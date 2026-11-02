# 🚀 Deployment Guide

This guide covers different ways to deploy your Home Monitoring Chatbot.

## 📋 Prerequisites

- Python 3.8+
- NVIDIA API key (from console.api.nvidia.com)
- `.env` file with your API key configured

---

## 🏠 Local Development

**Quickest way to test:**

```bash
python web_server.py
```

- Runs on: **http://localhost:5000**
- Perfect for testing and development
- Hot reload enabled (auto-restarts on code changes)

---

## 🖥️ Production with Gunicorn

**Production-ready WSGI server:**

### 1. Install Gunicorn

```bash
pip install gunicorn
```

### 2. Run the server

```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 4 --worker-class sync --timeout 60
```

**Parameters:**
- `--workers 4` - Number of worker processes (2-4x CPU cores)
- `--bind 0.0.0.0:5000` - Listen on all interfaces, port 5000
- `--timeout 60` - Worker timeout in seconds

### 3. Run in background (Linux/Mac)

```bash
nohup gunicorn app:app --bind 0.0.0.0:5000 --workers 4 > server.log 2>&1 &
```

---

## 🐳 Docker Deployment

### 1. Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
```

### 2. Build Docker image

```bash
docker build -t home-monitor:latest .
```

### 3. Run Docker container

```bash
docker run -d \
  --name home-monitor \
  -p 5000:5000 \
  --env-file .env \
  home-monitor:latest
```

### 4. View logs

```bash
docker logs -f home-monitor
```

---

## ☁️ Cloud Deployment Options

### **Heroku** (Free tier)

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Create `.gitignore` additions:
```
.env
venv/
*.pyc
```

3. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku config:set API_KEY=your_api_key
```

### **Render** (Easy deployment)

1. Push code to GitHub
2. Connect to Render at render.com
3. Select "Python" and "Gunicorn"
4. Add environment variable: `API_KEY=your_key`
5. Deploy!

### **DigitalOcean App Platform**

1. Push code to GitHub
2. Create new app on app.digitalocean.com
3. Connect GitHub repo
4. Set environment: `API_KEY=your_key`
5. Deploy automatically

### **AWS EC2** (with Nginx reverse proxy)

```bash
# Connect to EC2 instance
ssh -i key.pem ubuntu@your-instance.com

# Install Python and dependencies
sudo apt update
sudo apt install python3-pip python3-venv

# Clone your code
git clone your-repo
cd home-monitor-chatbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run with Gunicorn
gunicorn app:app --bind 127.0.0.1:5000
```

Then set up Nginx as a reverse proxy.

---

## 🔒 Environment Variables in Production

**Never commit `.env` file!**

### For Heroku/Render:
Use their dashboard to set environment variables

### For Docker:
```bash
docker run -e API_KEY="your_key" -p 5000:5000 home-monitor
```

### For Linux/AWS:
```bash
export API_KEY="your_key"
gunicorn app:app --bind 0.0.0.0:5000
```

---

## 📊 Monitoring & Logging

### View logs with Gunicorn

```bash
# Verbose logging
gunicorn app:app --bind 0.0.0.0:5000 --access-logfile - --error-logfile -
```

### Health check endpoint (optional)

Add to `app.py`:
```python
@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200
```

---

## 🔄 Auto-restart on crash

### Using systemd (Linux)

Create `/etc/systemd/system/home-monitor.service`:

```ini
[Unit]
Description=Home Monitoring Chatbot
After=network.target

[Service]
User=www-data
WorkingDirectory=/app
ExecStart=/app/venv/bin/gunicorn app:app --bind 0.0.0.0:5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable home-monitor
sudo systemctl start home-monitor
```

---

## 🛡️ Security Checklist

- [ ] `.env` is in `.gitignore`
- [ ] API key is never hardcoded
- [ ] Use HTTPS in production
- [ ] Set `DEBUG = False` in Flask
- [ ] Use strong database credentials (if added)
- [ ] Enable CORS only for trusted domains
- [ ] Rate limit API endpoints
- [ ] Keep dependencies updated

---

## 💰 Cost Estimation

| Service | Cost | Notes |
|---------|------|-------|
| **Heroku** | $7-50/mo | Good for small projects |
| **Render** | $7-20/mo | Simple deployment |
| **DigitalOcean** | $5-40/mo | Good value |
| **AWS** | $0-100/mo | Pay-as-you-go |
| **NVIDIA API** | $0.001-0.01/query | Very affordable |

---

## 📞 Troubleshooting Deployment

**500 Error on website:**
- Check Flask logs: `docker logs` or `heroku logs`
- Verify `.env` variables are set
- Test API locally first

**Website super slow:**
- Increase worker count in Gunicorn
- Check API response times
- Monitor server resources (CPU, RAM)

**Can't connect to NVIDIA API:**
- Verify internet connection
- Check API key validity
- Test with: `curl -H "Authorization: Bearer YOUR_KEY" https://integrate.api.nvidia.com`

---

**Need help?** Check the main [README.md](README.md) or SETUP.md files!
