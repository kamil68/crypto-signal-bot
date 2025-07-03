#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اجرای کامل سیستم سیگنال ارز دیجیتال
Complete Crypto Signal System Runner
"""

import subprocess
import threading
import time
import signal
import sys
import os

def print_banner():
    """Print Persian banner"""
    print("=" * 80)
    print("🤖 سیستم کامل سیگنال ارز دیجیتال - نسخه فارسی")
    print("🚀 Complete Crypto Signal System - Persian Edition")
    print("=" * 80)
    print("📊 شامل:")
    print("   • Bot سیگنال گیری هوشمند")
    print("   • داشبورد فارسی زیبا")
    print("   • API های کامل")
    print("   • تحلیل بلادرنگ بازار")
    print("=" * 80)

def run_main_app():
    """Run the main FastAPI application"""
    try:
        print("🚀 راه‌اندازی Bot اصلی...")
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ خطا در اجرای Bot اصلی: {e}")
    except KeyboardInterrupt:
        print("⏹️ Bot اصلی متوقف شد")

def run_dashboard():
    """Run the Persian dashboard"""
    try:
        print("🌐 راه‌اندازی داشبورد فارسی...")
        subprocess.run([
            sys.executable, "dashboard.py"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ خطا در اجرای داشبورد: {e}")
    except KeyboardInterrupt:
        print("⏹️ داشبورد متوقف شد")

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'ccxt', 'pandas', 
        'numpy', 'requests', 'ta', 'apscheduler', 'aiohttp'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("⚠️ بسته های زیر نصب نشده اند:")
        print(f"   {', '.join(missing_packages)}")
        print("\n📦 برای نصب:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ همه بسته ها نصب شده اند")
    return True

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 در حال توقف سیستم...")
    print("👋 خداحافظ!")
    sys.exit(0)

def main():
    """Main function to run everything"""
    print_banner()
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ لطفاً ابتدا بسته های مورد نیاز را نصب کنید")
        return
    
    print("\n🔧 شروع راه‌اندازی سیستم...")
    
    # Start main app in background thread
    main_thread = threading.Thread(target=run_main_app, daemon=True)
    main_thread.start()
    
    # Wait a bit for main app to start
    time.sleep(3)
    
    # Start dashboard in background thread
    dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
    dashboard_thread.start()
    
    # Wait for both to be ready
    time.sleep(5)
    
    print("\n✅ سیستم آماده است!")
    print("=" * 50)
    print("🌐 لینک ها:")
    print("   • Bot اصلی: http://localhost:8000")
    print("   • داشبورد فارسی: http://localhost:8001")
    print("   • API Documentation: http://localhost:8000/docs")
    print("=" * 50)
    print("💡 نکته: برای توقف Ctrl+C بزنید")
    print("\n🔄 هر ۵ دقیقه تحلیل جدید انجام می‌شود...")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()