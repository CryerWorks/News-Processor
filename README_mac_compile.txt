Mundus News Processor - Mac Compilation Guide
============================================

This guide will help you (or your Mac-using friend) compile the Mundus News Processor into a Mac-compatible app using PyInstaller. This is needed because the provided Windows executable will not run on macOS.

--------------------------------------
What You Need
--------------------------------------
- A Mac computer (required for Mac apps)
- Python 3.9 or newer (download from https://www.python.org/)
- Terminal (built into macOS)
- Internet connection

--------------------------------------
Step-by-Step Instructions
--------------------------------------

1. **Copy the News Processor Folder**
   - Move the entire `News Processor` folder (including all .py files, TrainingData, and Mundus_Icon.png) to your Mac.

2. **Install Python (if needed)**
   - Open Terminal and type:
     python3 --version
   - If Python is not installed, download and install it from https://www.python.org/.

3. **Install pip (if needed)**
   - Most Python installations include pip. Check with:
     pip3 --version

4. **Install Required Python Packages**
   - In Terminal, navigate to the News Processor folder:
     cd /path/to/News\ Processor
   - Install dependencies:
     pip3 install pyinstaller pandas openai python-dotenv scikit-learn python-docx

5. **Create the Mac Executable**
   - In the News Processor folder, run:
     pyinstaller --noconfirm --onefile \
       --add-data "Mundus_Icon.png:." \
       --add-data ".env:." \
       --add-data "TrainingData:TrainingData" \
       --add-data "FinlandNewsToCsv.py:." \
       --add-data "FinlandNewsChainer.py:." \
       --add-data "FinlandNewsMerger.py:." \
       --add-data "FinlandNewsSummariserThirdPass.py:." \
       --add-data "FinlandNewsDigestor.py:." \
       --add-data "FinlandNewsToDocx.py:." \
       --add-data "PolandNewsToCsv.py:." \
       --add-data "PolandNewsChainer.py:." \
       --add-data "PolandNewsMerger.py:." \
       --add-data "PolandNewsSummariserThirdPass.py:." \
       --add-data "PolandNewsDigestor.py:." \
       --add-data "PolandNewsToDocx.py:." \
       --add-data "NewsToCsv.py:." \
       --add-data "NewsChainer.py:." \
       --add-data "NewsMerger.py:." \
       --add-data "NewsSummariser.py:." \
       --add-data "NewsDigestor.py:." \
       --add-data "NewsToDocx.py:." \
       NewsProcessorGUI.py

   - (If you have other folders, add them with --add-data as above.)
   - The `:` is used as a separator on Mac (not `;`).

6. **Find Your App**
   - After building, look in the `dist` folder for the new executable (e.g., `NewsProcessorGUI`).
   - You can rename it or move it anywhere on your Mac.

7. **Run the App**
   - Double-click the executable or run it from Terminal:
     ./dist/NewsProcessorGUI

--------------------------------------
Troubleshooting
--------------------------------------
- If you see a security warning, right-click the app and choose "Open" the first time.
- If you get missing module errors, make sure all dependencies are installed with pip3.
- If you see an error about the OpenAI API key, edit the `.env` file and add your key:
  OPENAI_API_KEY=your-key-here

--------------------------------------
Tips
--------------------------------------
- You do NOT need to install Python to run the final executable, but you do need it to build it.
- All your news files should be in Markdown (.md) format.
- The program works best if you do not move or rename the included files and folders.

If you need help, contact the developer or a Mac-using friend! 