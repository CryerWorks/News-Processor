# 📱 Mundus News Digest Generator - User Guide
*For Non-Technical Users*

## 🎯 What This App Does
Transform your daily news markdown files into professional monthly reports with AI-powered summaries and categorization.

---

## 🚀 Quick Start Guide

### 🍎 **Mac Users** (Easiest Method)

#### **First Time Setup** (Security Fix)
If you get a "permission denied" or "access privileges" error:

**Option A - Right-Click Method** (Recommended):
1. **Right-click** on `Mundus News Digest.command`
2. Select **"Open"** from the context menu
3. Click **"Open"** in the security dialog that appears
4. The application will start normally

**Option B - Terminal Method**:
1. Open **Terminal** (Applications → Utilities → Terminal)
2. Type: `chmod +x ` (with a space at the end)
3. **Drag** `Mundus News Digest.command` into Terminal
4. Press **Enter**
5. Now double-click the file normally

**Option C - System Preferences**:
1. Go to **System Preferences** → **Security & Privacy**
2. Click **"Open Anyway"** if the file was blocked
3. Double-click the file again

#### **After First Time**
1. **Double-click** `Mundus News Digest.command` (works normally now)
2. Follow the on-screen prompts
3. Your web browser will open automatically
4. Start processing your news files!

### 🪟 **Windows Users** (Easiest Method)  
1. **Double-click** `Mundus News Digest.bat`
2. Follow the on-screen prompts
3. Your web browser will open automatically
4. Start processing your news files!

### 🌐 **Alternative Method** (All Platforms)
1. **Double-click** `run_web_app.py`
2. Your web browser will open to the application

---

## 🔑 First-Time Setup

### Step 1: Get Your OpenAI API Key
You'll need an OpenAI account to use the AI features:

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in or create a free account
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-`)
5. When prompted by the app, paste your key

### Step 2: Install Python (If Needed)
The app will check and guide you if Python isn't installed:
- **Mac**: Python may already be installed
- **Windows**: Download from [python.org](https://python.org/downloads/)

---

## 📋 How to Use the App

### 1. **Select Your Country**
Choose from:
- 🇸🇪 Sweden (default)
- 🇫🇮 Finland  
- 🇵🇱 Poland

### 2. **Upload Your Files**
- **Drag & Drop**: Drag your `.md` files onto the upload area
- **Browse**: Click "Browse Files" to select files manually
- **Multiple Files**: You can upload many files at once

### 3. **Generate Your Digest**
- Click **"Generate Monthly Digest"**
- Wait for processing (15-30 minutes for a month of news)
- Watch the progress in real-time

### 4. **Download Your Results**
- Download the ZIP file containing:
  - 📄 **Monthly_News_Digest_[Country].md** (Markdown file)
  - 📄 **Monthly_News_Digest_[Country].docx** (Word document)

---

## 💡 Pro Tips

### ✅ **Best Practices**
- Keep the terminal/command window open while using the app
- Use a stable internet connection for AI processing
- Process files in batches of 30 days or less for best results

### ⚡ **Speed Tips**
- After first setup, the app starts much faster
- Close other applications during processing for better performance
- The app works in the background - you can use other programs

### 🔒 **Privacy & Security**
- Your files are processed locally on your computer
- Only text summaries are sent to OpenAI for processing
- All files are automatically cleaned up after processing

---

## 🆘 Troubleshooting

### **"Python not found" Error**
- **Mac**: Install Python from [python.org](https://python.org/downloads/)
- **Windows**: Install Python and check "Add Python to PATH"

### **"API key missing" Error**
- Get your key from [OpenAI API Keys](https://platform.openai.com/api-keys)
- Create a `.env` file with: `OPENAI_API_KEY=your_key_here`

### **"Dependencies failed" Error**
- Check your internet connection
- Try running the setup scripts again
- On Mac: Try `sudo` if permission errors occur

### **Browser doesn't open**
- Manually visit: `http://localhost:5000`
- Try a different browser (Chrome, Firefox, Safari)

### **Processing takes too long**
- This is normal for large amounts of news
- 30 days of news typically takes 15-30 minutes
- Keep the terminal window open

---

## 📞 Getting Help

### **Quick Solutions**
1. **Restart the app** - Close terminal window and double-click launcher again
2. **Check internet connection** - Required for AI processing
3. **Try fewer files** - Process in smaller batches if having issues

### **File Requirements**
- ✅ **Supported**: `.md` (Markdown files)
- ✅ **Format**: Daily news with **News** section
- ✅ **Structure**: Headlines in `**bold**` format

### **System Requirements**
- **Mac**: macOS 10.15 or later
- **Windows**: Windows 10 or later
- **Internet**: Required for AI processing
- **Storage**: ~500MB free space

---

## 🎉 Success!

When everything works correctly, you'll see:
1. ✅ Dependencies installed
2. 🌐 Web server starting
3. 🔄 Real-time processing progress
4. 📥 Download link for your results

**Your professional monthly news digest is ready!** 📊

---

*Need more help? Check that your markdown files have the correct format with a **News** section and headlines in `**bold**` format.*
