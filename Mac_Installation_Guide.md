# Mundus News Processor - Mac Installation Guide

## 🍎 Installing on macOS

The Mundus News Processor is currently **unsigned**, which means macOS will show security warnings. This is normal for many applications distributed outside the Mac App Store. Follow these steps to install safely:

## 📥 Installation Steps

### Step 1: Download the DMG
1. Download `NewsProcessor.dmg` from the provided source
2. Double-click to mount the disk image

### Step 2: Handle Security Warning (First Time)
When you first try to open the app, macOS will show a security warning:

**If you see: "Cannot be opened because the developer cannot be verified"**

✅ **Solution:**
1. **Don't click "Move to Trash"**
2. Instead, **right-click** (or Control+click) on the `NewsProcessorGUI` app
3. Select **"Open"** from the context menu
4. Click **"Open"** in the new dialog that appears
5. The app will now launch and be trusted for future use

### Step 3: Alternative Method via System Preferences
If the right-click method doesn't work:

1. Try to open the app normally (it will be blocked)
2. Go to **System Preferences** → **Security & Privacy**
3. Click the **"General"** tab
4. You'll see a message about the blocked app
5. Click **"Open Anyway"**
6. Confirm by clicking **"Open"**

### Step 4: Configure OpenAI API Key
Once the app opens:

1. The app includes a template `.env` file
2. You'll need to provide your OpenAI API key
3. The app will guide you through this process

## 🔒 Security Information

### Why These Warnings Appear
- The app is not signed with an Apple Developer ID ($99/year)
- This is common for open-source and independent software
- The warnings are macOS protecting you from potentially malicious software

### Is It Safe?
- ✅ The source code is open and reviewable
- ✅ Built using GitHub Actions with transparent build process  
- ✅ No network access except to OpenAI API (with your key)
- ✅ No system modifications or admin privileges required

### What the App Does
- Processes markdown news files locally
- Uses your OpenAI API key for summarization
- Creates Word documents and CSV files
- All processing happens on your computer

## 🛠️ Troubleshooting

### Problem: "App is damaged and can't be opened"
**Solution:** This usually means the download was corrupted
1. Re-download the DMG file
2. Try the installation steps again

### Problem: App won't launch after bypassing security
**Possible causes:**
1. **Missing OpenAI API Key**: Add your key to the `.env` file
2. **Permissions**: Make sure the app has necessary permissions
3. **macOS Version**: Requires macOS 10.15 (Catalina) or later

### Problem: Corporate/Work Mac blocks the app
**Solution:** Contact your IT administrator
- They may need to whitelist the application
- Or provide an exception for development tools

## 🔧 Advanced Users

### Command Line Installation
If you're comfortable with Terminal:

```bash
# Remove quarantine attribute (bypasses Gatekeeper)
sudo xattr -rd com.apple.quarantine /Applications/NewsProcessorGUI.app

# Or if the app is elsewhere:
sudo xattr -rd com.apple.quarantine /path/to/NewsProcessorGUI
```

### Verify App Integrity
You can check the app's integrity:

```bash
# Check if app is signed (it won't be)
codesign -dv /path/to/NewsProcessorGUI

# Check app architecture
file /path/to/NewsProcessorGUI
```

## 📞 Support

If you continue to have issues:
1. Check that you're running macOS 10.15 or later
2. Ensure you have admin privileges on your Mac
3. Try restarting your Mac and attempting installation again
4. Contact support with specific error messages

## 🎯 For Organizations

If you're distributing this within an organization:
1. Consider getting an Apple Developer ID for signing ($99/year)
2. Use Mobile Device Management (MDM) to whitelist the app
3. Provide IT support with this installation guide
4. Test on a variety of Mac configurations

---

**Remember**: These security steps are only needed the **first time** you install the app. Once trusted, it will launch normally like any other application.
