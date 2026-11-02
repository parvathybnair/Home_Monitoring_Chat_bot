# 🔑 API Setup Guide

## Get Your NVIDIA API Key (Free)

### Step 1: Create an Account
1. Go to: https://console.api.nvidia.com
2. Click **"Sign Up"** or **"Login"**
3. Complete the registration with your email

### Step 2: Generate API Key
1. Once logged in, look for **"API Keys"** or **"Credentials"** section
2. Click **"Create New API Key"** or similar button
3. You'll see a long string like:
   ```
   nvapi_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
4. **Copy this entire key** (including the `nvapi_` prefix)

### Step 3: Add Key to .env File

1. Open the `.env` file in your project:
   ```
   home_monitor_chatbot/
   └── .env
   ```

2. Find the line:
   ```
   API_KEY=your_nvidia_api_key_here
   ```

3. Replace it with your actual key:
   ```
   API_KEY=nvapi_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

4. **Save the file**

### Step 4: Test Your Setup

Run this command:
```bash
python main.py
```

If everything works, you should see:
```
Starting Home Monitoring Chatbot...

==================================================
🏠 HOME MONITORING CHATBOT
==================================================
Ask me anything about your home status!
Type 'exit' to quit | 'status' to see full report

You: 
```

Try asking: **"What's the status?"**

---

## ⚠️ Important Security Tips

### DO's ✅
- Keep `.env` file **private** (never commit to Git)
- Use `.env.example` as a **template only**
- **Regenerate API key** if accidentally exposed
- Use environment variables for all sensitive data

### DON'Ts ❌
- **Don't paste API keys** in chat messages
- **Don't commit `.env`** to GitHub/GitLab
- **Don't share `.env`** files via email
- **Don't hardcode keys** in Python files

---

## 🚨 If You Accidentally Exposed Your Key

**IMMEDIATELY DO THIS:**

1. Go to: https://console.api.nvidia.com
2. Find your API key in the dashboard
3. Click **"Delete"** or **"Revoke"**
4. Create a **new API key**
5. Update your `.env` file with the new key
6. If you committed it to Git, contact your DevOps team

---

## 💡 Costs

- NVIDIA Nimble API: **Free tier available**
- Deepseek-V4-Pro: **Pay-as-you-go** (very affordable)
- Typical usage: $0.001-$0.01 per query

Monitor your usage at: https://console.api.nvidia.com/billing

---

## 🆘 Troubleshooting

### Error: "API_KEY not found in .env file"
- Make sure `.env` file exists in the project root
- Check that `API_KEY=` line is uncommented
- Verify you pasted the key correctly

### Error: "Invalid API key"
- Double-check the key format (should start with `nvapi_`)
- Ensure no extra spaces at the beginning/end
- Try generating a new API key

### Error: "Connection refused"
- Check your internet connection
- Verify NVIDIA API is online: https://console.api.nvidia.com
- Try again in a few moments

### Error: "401 Unauthorized"
- Your API key might have expired
- Generate a new key in the dashboard
- Update `.env` with the new key

---

## 📚 Useful Links

- NVIDIA Console: https://console.api.nvidia.com
- Deepseek Docs: https://deepseek.com/docs
- OpenAI Python Docs: https://platform.openai.com/docs/libraries/python-library
