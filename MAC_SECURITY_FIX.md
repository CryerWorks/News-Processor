# 🍎 Mac Security Fix - Mundus News Digest Generator

## ⚠️ **Common Issue: "Permission Denied" Error**

When you first download and try to run `Mundus News Digest.command` on Mac, you may encounter:
- **"Permission denied"** error
- **"You do not have access privileges"** message
- **"Cannot be opened because it is from an unidentified developer"**

This is normal macOS security behavior for downloaded files.

---

## 🔧 **Solutions (Choose One)**

### **Method 1: Right-Click Method** ⭐ (Recommended)
1. **Right-click** on `Mundus News Digest.command`
2. Select **"Open"** from the context menu
3. A security dialog will appear
4. Click **"Open"** to confirm
5. The application will start normally
6. **Future runs**: Just double-click normally

### **Method 2: Terminal Method**
1. Open **Terminal** (Applications → Utilities → Terminal)
2. Navigate to the download folder:
   ```bash
   cd ~/Downloads/News-Processor-main  # or wherever you extracted it
   ```
3. Make the file executable:
   ```bash
   chmod +x "Mundus News Digest.command"
   ```
4. Now double-click the file normally

### **Method 3: System Preferences Method**
1. Try to double-click `Mundus News Digest.command`
2. When blocked, go to **System Preferences** → **Security & Privacy**
3. Click **"Open Anyway"** for the blocked file
4. Double-click the file again
5. Confirm by clicking **"Open"**

### **Method 4: Gatekeeper Override** (Advanced)
```bash
# Remove quarantine attribute (one-time fix)
xattr -d com.apple.quarantine "Mundus News Digest.command"
```

---

## 🎯 **Why This Happens**

### **macOS Security Features**
- **Gatekeeper**: Prevents unsigned apps from running
- **Quarantine**: Flags downloaded files as potentially unsafe
- **Code Signing**: Requires developer signatures for easy execution

### **Our File Status**
- ✅ **Safe to run**: Contains only standard shell commands
- ❌ **Not code signed**: We're not a registered Apple developer
- ⚠️ **Downloaded**: Triggers macOS security warnings

---

## 🚀 **After First Fix**

Once you've used any of the methods above **once**:

1. **Double-click** `Mundus News Digest.command` (works normally)
2. **No more security warnings**
3. **Automatic browser opening**
4. **Full functionality available**

---

## 🛡️ **Alternative: Use the Mac App Bundle**

If you prefer a more "native" experience:

1. Use `Mundus News Digest.app` instead
2. Still requires right-click → Open first time
3. Appears like a regular Mac application
4. Same functionality, different presentation

---

## 🆘 **Still Having Issues?**

### **If Terminal Method Fails**
```bash
# Check file permissions
ls -la "Mundus News Digest.command"

# Should show: -rwxr-xr-x (executable)
# If not, try again with sudo:
sudo chmod +x "Mundus News Digest.command"
```

### **If All Methods Fail**
**Fallback Option**: Use Python directly
```bash
python3 run_web_app.py
```
Then visit `http://localhost:5000` in your browser.

---

## 💡 **Pro Tips**

### **For Developers**
- This is why we provide multiple launch methods
- Python method always works as fallback
- Consider code signing for production distribution

### **For Users**
- This is a **one-time setup** only
- All future launches work normally
- Same security fix applies to other `.command` files

---

**🎉 Once fixed, enjoy the seamless Mundus News Digest Generator experience on Mac!**
