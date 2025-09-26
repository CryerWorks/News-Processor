#!/usr/bin/env python3
"""
Test script for validating the Mac build of News Processor
This runs in GitHub Actions to validate the build before packaging
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

def test_executable_exists():
    """Test if the executable was created"""
    exe_path = Path("dist/NewsProcessorGUI")
    if not exe_path.exists():
        print("❌ Executable not found at dist/NewsProcessorGUI")
        return False
    
    print(f"✅ Executable found: {exe_path}")
    print(f"   Size: {exe_path.stat().st_size / (1024*1024):.2f} MB")
    return True

def test_executable_permissions():
    """Test if executable has proper permissions"""
    exe_path = Path("dist/NewsProcessorGUI")
    try:
        os.chmod(exe_path, 0o755)
        print("✅ Executable permissions set")
        return True
    except Exception as e:
        print(f"❌ Failed to set executable permissions: {e}")
        return False

def test_module_imports():
    """Test if all required modules can be imported"""
    modules_to_test = [
        # Core modules
        "NewsProcessorGUI",
        "NewsToCsv", 
        "NewsChainer",
        "NewsMerger", 
        "NewsSummariser",
        "NewsDigestor",
        "NewsToDocx",
        # Country-specific modules
        "FinlandNewsToCsv",
        "FinlandNewsChainer", 
        "FinlandNewsMerger",
        "FinlandNewsSummariserThirdPass",
        "FinlandNewsDigestor",
        "FinlandNewsToDocx",
        "PolandNewsToCsv",
        "PolandNewsChainer",
        "PolandNewsMerger", 
        "PolandNewsSummariserThirdPass",
        "PolandNewsDigestor",
        "PolandNewsToDocx"
    ]
    
    failed_imports = []
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ Failed to import {len(failed_imports)} modules")
        return False
    else:
        print(f"✅ All {len(modules_to_test)} modules imported successfully")
        return True

def test_dependencies():
    """Test if all required dependencies are available"""
    dependencies = [
        "pandas",
        "sklearn", 
        "openai",
        "docx",
        "tkinter",
        "numpy",
        "dotenv"
    ]
    
    failed_deps = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError as e:
            print(f"❌ {dep}: {e}")
            failed_deps.append(dep)
    
    if failed_deps:
        print(f"❌ Missing {len(failed_deps)} dependencies")
        return False
    else:
        print(f"✅ All {len(dependencies)} dependencies available")
        return True

def test_training_data():
    """Test if training data files are accessible"""
    import pandas as pd
    
    training_files = [
        "TrainingDataFeb2025.xlsx",
        "TrainingDataJan2025.xlsx", 
        "TrainingDataNov2025.xlsx"
    ]
    
    failed_files = []
    total_rows = 0
    
    for file in training_files:
        if not os.path.exists(file):
            print(f"❌ Missing: {file}")
            failed_files.append(file)
            continue
            
        try:
            df = pd.read_excel(file)
            rows = len(df)
            total_rows += rows
            print(f"✅ {file}: {rows} rows")
            
            # Check if required columns exist
            if "Category" not in df.columns:
                print(f"❌ {file}: Missing 'Category' column")
                failed_files.append(file)
            elif "Summary" not in df.columns:
                print(f"❌ {file}: Missing 'Summary' column") 
                failed_files.append(file)
            else:
                print(f"   Required columns present: Category, Summary")
                
        except Exception as e:
            print(f"❌ Error loading {file}: {e}")
            failed_files.append(file)
    
    if failed_files:
        print(f"❌ {len(failed_files)} training data files failed")
        return False
    else:
        print(f"✅ All training data loaded successfully ({total_rows} total rows)")
        return True

def test_assets():
    """Test if required assets are present"""
    assets = [
        "Mundus_Icon.png",
        ".env"
    ]
    
    failed_assets = []
    for asset in assets:
        if not os.path.exists(asset):
            print(f"❌ Missing: {asset}")
            failed_assets.append(asset)
        else:
            print(f"✅ {asset}")
    
    if failed_assets:
        print(f"❌ Missing {len(failed_assets)} assets")
        return False
    else:
        print(f"✅ All assets present")
        return True

def main():
    """Run all tests"""
    print("🧪 Testing Mac Build of News Processor")
    print("=" * 50)
    
    tests = [
        ("Executable Creation", test_executable_exists),
        ("Executable Permissions", test_executable_permissions), 
        ("Module Imports", test_module_imports),
        ("Dependencies", test_dependencies),
        ("Training Data", test_training_data),
        ("Assets", test_assets)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                failed += 1
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        print("❌ BUILD VALIDATION FAILED")
        sys.exit(1)
    else:
        print("✅ BUILD VALIDATION PASSED")
        sys.exit(0)

if __name__ == "__main__":
    main()
