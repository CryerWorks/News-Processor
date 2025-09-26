# Mundus News Processor - Mac Compilation Guide

This guide explains how to compile the Mundus News Processor for macOS from a Windows computer using GitHub Actions.

## Prerequisites

1. **GitHub Repository**: The code must be in a GitHub repository
2. **GitHub Actions Enabled**: Your repository must have GitHub Actions enabled
3. **OpenAI API Key**: You'll need a valid OpenAI API key for the final executable to work

## Compilation Process

### Method 1: Automatic GitHub Actions Build (Recommended)

The repository includes an automated GitHub Actions workflow that will build the Mac executable for you:

1. **Push to Master Branch**: 
   - Commit and push your changes to the `master` branch
   - The workflow will automatically trigger

2. **Manual Trigger**:
   - Go to your GitHub repository
   - Click on "Actions" tab
   - Find "macOS Build" workflow
   - Click "Run workflow" button
   - Select the branch (usually `master`)
   - Click "Run workflow"

3. **Download the Result**:
   - Wait for the build to complete (usually 5-10 minutes)
   - Go to the completed workflow run
   - Download the "NewsProcessor-macOS" artifact
   - Extract the `NewsProcessor.dmg` file

### What Gets Built

The GitHub Actions workflow will:
- Set up a macOS environment with Python 3.11
- Install all required dependencies:
  - `pyinstaller` (for creating the executable)
  - `pandas` (for data processing)
  - `openai` (for AI summarization)
  - `python-dotenv` (for environment variables)
  - `scikit-learn` (for ML categorization)
  - `python-docx` (for Word document generation)
- Create a template `.env` file with placeholder API key
- Bundle all Python modules and data files
- Create a single executable file
- Package it into a Mac-compatible DMG installer

## Setting Up the Mac Executable

Once you have the DMG file:

1. **Install on Mac**:
   - Double-click the `NewsProcessor.dmg` file
   - Drag the executable to Applications or desired location
   - Right-click and select "Open" the first time (security requirement)

2. **Configure OpenAI API Key**:
   - The executable includes a template `.env` file
   - You need to locate and edit this file with your actual OpenAI API key
   - The file should contain: `OPENAI_API_KEY=your-actual-key-here`

3. **File Location**:
   - If the executable is in Applications, the `.env` file is bundled inside
   - You may need to extract and modify it, or provide the API key through environment variables

## Troubleshooting

### Common Issues:

1. **"Cannot open because developer cannot be verified"**:
   - Right-click the app and select "Open"
   - Click "Open" in the security dialog

2. **Missing OpenAI API Key**:
   - Ensure your `.env` file contains a valid OpenAI API key
   - The key should start with `sk-`

3. **Build Fails**:
   - Check the GitHub Actions logs for specific error messages
   - Ensure all Python files are present in the repository
   - Verify the `TrainingData` folder and `Mundus_Icon.png` are included

### Manual Mac Compilation (Alternative)

If you have access to a Mac computer, you can also compile manually:

```bash
# Install Python dependencies
pip3 install pyinstaller pandas openai python-dotenv scikit-learn python-docx

# Create the executable
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
```

## Final Notes

- The compiled executable will be a single file that includes all dependencies
- The DMG installer makes it easy to distribute to Mac users
- Users will still need to provide their own OpenAI API key
- The executable supports all three countries: Sweden, Finland, and Poland
- All training data and the Mundus logo are bundled in the executable
