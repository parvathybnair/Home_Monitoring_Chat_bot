# 🚀 Deployment Guide - Home Monitor Chatbot

## Your app is ready for deployment! Follow these steps:

---

## Option 1: Deploy on Render.com (FREE - Recommended)

### Step 1: Install Git
1. Download Git from: https://git-scm.com/download/win
2. Install it (use default settings)
3. Restart your terminal/VS Code after installing

### Step 2: Create a GitHub Repository
1. Go to https://github.com and sign in (or create an account)
2. Click the **"+"** button → **"New repository"**
3. Name it: `home-monitor-chatbot`
4. Keep it **Public** (required for free Render deployment)
5. Do NOT add README, .gitignore, or license (we already have them)
6. Click **"Create repository"**

### Step 3: Push Your Code to GitHub
Open a terminal in your project folder and run these commands:
```bash
git init
git add .
git commit -m "Initial commit - Home Monitor Chatbot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/home-monitor-chatbot.git
git push -u origin main
```
> ⚠️ Replace `YOUR_USERNAME` with your actual GitHub username

### Step 4: Deploy on Render
1. Go to https://render.com and sign in with your GitHub account
2. Click **"New +"** → **"Web Service"**
3. Connect your **home-monitor-chatbot** repository
4. Render will auto-detect the settings from `render.yaml`
5. Set the **Environment Variables**:
   - `API_KEY` = `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`
6. Click **"Create Web Service"**
7. Wait 2-3 minutes for deployment

### Step 5: Your Live URL! 🎉
Render will give you a URL like:
```
https://home-monitor-chatbot.onrender.com
```
Share this link with anyone!

---

## Option 2: Deploy on Railway.app (FREE)

1. Go to https://railway.app
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub Repo"**
4. Select your `home-monitor-chatbot` repo
5. Add environment variable: `API_KEY` = your NVIDIA API key
6. Railway will auto-deploy and give you a public URL

---

## Option 3: Quick Share with ngrok (Temporary)

If you just want to share temporarily without deployment:
1. Download ngrok from https://ngrok.com/download
2. Run your Flask server: `python app.py`
3. In another terminal: `ngrok http 5000`
4. ngrok gives you a public URL like `https://abc123.ngrok.io`
5. Share that URL! (Works as long as ngrok is running)

---

## Files Created for Deployment
- `requirements.txt` - Python dependencies
- `Procfile` - Tells the server how to run your app
- `render.yaml` - Render.com configuration
- `.gitignore` - Protects your API keys from being uploaded

## ⚠️ Important Security Note
Your `.env` file contains API keys and is excluded from git via `.gitignore`.
On Render/Railway, set the API_KEY as an **Environment Variable** in their dashboard.
