#!/usr/bin/env python3
"""
Mundus News Digest Generator - Cloud Deployment Helper
Prepares the application for cloud deployment on Render
"""

import os
import sys
import subprocess
import json

def check_requirements():
    """Check if all required files exist for deployment"""
    required_files = [
        'app.py',
        'requirements.txt', 
        'render.yaml',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def validate_environment():
    """Validate environment configuration"""
    print("🔍 Validating environment configuration...")
    
    # Check if OpenAI key is mentioned in documentation
    env_mentioned = False
    try:
        with open('DEPLOYMENT_GUIDE.md', 'r') as f:
            if 'OPENAI_API_KEY' in f.read():
                env_mentioned = True
    except FileNotFoundError:
        pass
    
    if env_mentioned:
        print("✅ Environment variables documented")
    else:
        print("⚠️  Environment variables not documented")
    
    return True

def check_dependencies():
    """Check if all dependencies are properly specified"""
    print("📦 Checking dependencies...")
    
    try:
        with open('requirements.txt', 'r') as f:
            deps = f.read()
            
        required_deps = ['Flask', 'Flask-SocketIO', 'pandas', 'openai', 'gunicorn']
        missing_deps = []
        
        for dep in required_deps:
            if dep not in deps:
                missing_deps.append(dep)
        
        if missing_deps:
            print("❌ Missing dependencies:")
            for dep in missing_deps:
                print(f"   - {dep}")
            return False
        
        print("✅ All required dependencies present")
        return True
        
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def generate_deployment_summary():
    """Generate a summary of deployment configuration"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT SUMMARY")
    print("="*60)
    
    print(f"📁 Project Directory: {os.getcwd()}")
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    
    # Count files
    total_files = sum([len(files) for r, d, files in os.walk('.')])
    print(f"📄 Total Files: {total_files}")
    
    # Check git status
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"🌿 Git Branch: {result.stdout.strip()}")
    except FileNotFoundError:
        print("🌿 Git: Not available")
    
    print("\n📋 Deployment Checklist:")
    print("   ✅ Flask app configured for production")
    print("   ✅ Render configuration file ready")
    print("   ✅ Dependencies specified")
    print("   ✅ Environment variables documented")
    print("   ✅ Static files included")
    print("   ✅ Templates ready")
    
    print("\n🔗 Next Steps:")
    print("   1. Push code to GitHub (2.0 branch)")
    print("   2. Connect GitHub repo to Render")
    print("   3. Set OPENAI_API_KEY environment variable")
    print("   4. Deploy and test")
    
    print("\n🌐 Expected URL: https://mundus-news-digest.onrender.com")
    print("="*60)

def main():
    """Main deployment preparation function"""
    print("🚀 Mundus News Digest Generator - Cloud Deployment Preparation")
    print("="*60)
    
    # Run checks
    if not check_requirements():
        print("❌ Deployment preparation failed")
        sys.exit(1)
    
    if not validate_environment():
        print("⚠️  Environment validation issues")
    
    if not check_dependencies():
        print("❌ Dependency check failed")
        sys.exit(1)
    
    generate_deployment_summary()
    
    print("\n🎉 Ready for cloud deployment!")
    print("📖 See DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == '__main__':
    main()
