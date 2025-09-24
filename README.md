# f(x) Protocol Quiz Application

A beginner-friendly quiz application built with Streamlit to test your knowledge about the f(x) Protocol ecosystem - a decentralized stablecoin solution built on Ethereum.

## ✨ Features

- **🎯 Interactive Quiz**: 10 randomly selected True/False questions from a pool of 59
- **⚡ Instant Feedback**: See immediately if your answer is correct (green) or wrong (red)
- **📚 Learn as You Go**: Detailed explanations appear after each answer to help you understand
- **🎮 Manual Control**: Click "Next Question" to proceed at your own pace (no rushing!)
- **🏆 Smart Leaderboard**: Tracks your best scores and total points across all attempts
- **👤 Personal Tracking**: Your scores are saved under your username
- **🔄 Replay Anytime**: Start a new quiz whenever you want
- **🎨 Clean Interface**: Easy-to-use design that works on any device

## 🎯 What You'll Learn

The quiz teaches you about f(x) Protocol including:
- 🤖 **DeFi Basics**: How decentralized finance and stablecoins work
- 💰 **Token Economics**: Understanding FXN, fxUSD, and governance tokens
- 🏦 **Stability Systems**: How the protocol maintains price stability
- 🌐 **Network Expansion**: Growth to Base layer-2 blockchain
- 🎁 **Community Rewards**: How participants earn incentives
- 📈 **Protocol History**: Key events and developments

## 🚀 Super Simple Setup (5 Minutes)

### ✅ What You Need
- A computer with internet
- About 5 minutes of time

### 📥 Step-by-Step Installation

**Step 1: Get the Files**
- Download all the files in this project to a folder on your computer
- Keep them all together in one folder (like "fx-quiz-project")

**Step 2: Run the Setup (Easiest Way)**
```bash
# Open Terminal/Command Prompt in the project folder
# Then copy and paste this command:

./setup.sh
```

**What happens next:**
- ✅ Python environment gets created automatically
- ✅ All required software gets installed
- ✅ Everything gets configured

**Step 3: Start the Quiz**
```bash
# After setup finishes, run:
streamlit run appl.py
```

**Step 4: Open Your Browser**
- The quiz will open automatically at: **http://localhost:8501**
- If it doesn't open, just type that address into your web browser

### 🛠️ If Setup Doesn't Work

If the automated setup fails, here's the manual way:

```bash
# Step 1: Create Python environment
python3 -m venv venv

# Step 2: Activate it
source venv/bin/activate

# Step 3: Install software
pip install -r requirements.txt

# Step 4: Start quiz
streamlit run appl.py
```

**Need help?** Check the troubleshooting section below!

## 🎮 How to Play

**Super Easy Steps:**

1. **🔤 Enter Your Name**: Type any username you want
2. **❓ Answer Questions**: Click "True" or "False" - take your time!
3. **✅ See Results**: Instantly see if you're right (green) or wrong (red)
4. **📚 Learn Why**: Read the explanation to understand the topic better
5. **👆 Your Pace**: Click "Next Question" when you're ready to continue
6. **🏆 Check Progress**: Watch your score grow in the top-right corner
7. **🎯 Finish Strong**: Complete all 10 questions to see your final ranking
8. **🔄 Play Again**: Hit "Replay" to try for a better score!

**Pro Tips:**
- Take your time reading explanations - they're designed to teach you!
- No rush - you control when to move to the next question
- Your best scores are saved automatically

## 📁 What's in This Project

```
fx-quiz-project/
├── 🎮 appl.py              # Main quiz application (the game!)
├── ❓ question_model.py    # Handles quiz questions and answers
├── 🧠 quiz_brain.py       # Game logic and scoring system
├── 📊 data.py            # Quiz questions and leaderboard data
├── 👤 username.py         # Username handling
├── 🏆 leaderboard.py      # Score tracking system
├── 📈 leaderboard.json    # Your scores (automatically created)
├── 📦 requirements.txt    # List of needed software
├── ⚙️ setup.sh           # One-click setup script
└── 📖 README.md          # This guide you're reading
```

**Don't worry about these files!** The setup script handles everything automatically. Just run `./setup.sh` and you'll be ready to play!

## 🎓 Want to Learn More?

This quiz helps you learn about **DeFi (Decentralized Finance)** - a revolutionary way to handle money without traditional banks!

**Key Topics Covered:**
- 🔐 How blockchain technology works
- 💰 Understanding stablecoins and their importance
- 🏛️ How f(x) Protocol maintains price stability
- 🎯 Community governance and decision-making
- 📊 Real-world events that shaped DeFi

**Learning Tip:** Take your time reading the explanations - they're designed to teach you something new with each question!

## 🏆 How Scoring Works

**Your scores are saved automatically!** The system tracks:

- 🥇 **High Score**: Your best single quiz performance
- 📈 **Total Points**: All your points added together from every quiz
- 💾 **Auto-Save**: Everything is saved automatically - no setup needed!

**Where are scores stored?** In a file called `leaderboard.json` - you don't need to touch this file, it works automatically!

## 🆘 Having Problems? Let's Fix It!

### 💻 "Command not found" Errors

**Problem**: When you type `./setup.sh`, you get "command not found"
**Solution**:
```bash
# Try this instead:
bash setup.sh
```

### 🐍 Python Not Found

**Problem**: "Python is not installed" or "python3 command not found"
**Solution**:
1. **Mac**: Install Python from https://python.org
2. **Windows**: Download from Microsoft Store or https://python.org
3. **Linux**: Use your package manager: `sudo apt install python3`

### 🚫 Setup Script Fails

**Problem**: `./setup.sh` gives errors
**Solution**: Use the manual setup (it's just as easy!):
```bash
# Step 1: Create environment
python3 -m venv venv

# Step 2: Activate it
source venv/bin/activate

# Step 3: Install software
pip install -r requirements.txt

# Step 4: Start quiz
streamlit run appl.py
```

### 🌐 Browser Won't Open

**Problem**: Quiz doesn't open automatically
**Solution**:
1. Open any web browser (Chrome, Firefox, Safari, Edge)
2. Type: `http://localhost:8501`
3. Press Enter - the quiz should appear!

### 🔄 Port Already in Use

**Problem**: "Port 8501 is already in use"
**Solution**: Close other applications or try a different port:
```bash
streamlit run appl.py --server.port 8502
```
Then visit: `http://localhost:8502`

### 📱 Nothing Happens After Setup

**Problem**: Setup completes but quiz won't start
**Solution**:
1. Make sure you're in the project folder
2. Try: `streamlit run appl.py --server.headless true`
3. If still stuck, restart your computer and try again

### ❓ Still Having Issues?

**Quick Checklist:**
- ✅ Downloaded all files to one folder?
- ✅ Opened Terminal/Command Prompt in that folder?
- ✅ Ran `./setup.sh` or the manual commands?
- ✅ Typed `streamlit run appl.py`?
- ✅ Opened `http://localhost:8501` in browser?

**Still stuck?** The manual setup method almost always works - just follow the steps one by one!

## 💡 Tips for Success

- **🎯 Focus on Learning**: Don't worry about getting every answer right - the explanations teach you!
- **⏰ Take Your Time**: Read each explanation carefully to understand the concepts
- **🔄 Practice Makes Perfect**: Try the quiz multiple times to improve your score
- **📝 Make Notes**: Keep track of interesting facts you learn
- **🌐 Explore Further**: Use what you learn as a starting point for deeper research

## 🎉 You're Ready to Learn!

**This quiz makes learning about DeFi fun and interactive!** Each question comes with detailed explanations that help you understand complex topics in simple terms.

**Remember**: The goal is to learn, not to get a perfect score. Every wrong answer is a learning opportunity!

---

**🌟 Educational Note**: This quiz teaches you about decentralized finance (DeFi) and the f(x) Protocol ecosystem. Always do your own research and understand the risks involved in DeFi protocols before participating.
