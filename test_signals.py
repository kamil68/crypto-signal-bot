#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست سیستم سیگنال ها
Test script for signal system
"""

import asyncio
import json
from datetime import datetime
import sys

async def test_signals():
    """Test the signal system"""
    print("🧪 شروع تست سیستم سیگنال ها...")
    print("🧪 Starting signal system test...")
    
    try:
        # Import signals module
        from signals import analyze, get_market_summary, print_welcome
        
        # Print welcome message
        print_welcome()
        
        # Test market summary
        print("\n📊 تست خلاصه بازار...")
        market_summary = await get_market_summary()
        print("✅ خلاصه بازار:")
        print(json.dumps(market_summary, indent=2, ensure_ascii=False))
        
        # Test signal analysis
        print("\n🔍 تست تحلیل سیگنال ها...")
        signals = await analyze()
        
        print(f"\n📈 نتایج ({len(signals)} سیگنال):")
        print("-" * 50)
        
        for i, (symbol, signal_text) in enumerate(signals, 1):
            print(f"{i:2d}. {symbol:12s} → {signal_text}")
        
        print("-" * 50)
        print("✅ تست با موفقیت تمام شد!")
        print("✅ Test completed successfully!")
        
        return True
        
    except ImportError as e:
        print(f"❌ خطا در import: {e}")
        print("💡 مطمئن شوید که همه فایل ها موجود هستند")
        return False
        
    except Exception as e:
        print(f"❌ خطا در تست: {e}")
        print(f"❌ Test error: {e}")
        return False

async def test_bot_import():
    """Test importing the main bot"""
    print("🤖 تست import bot اصلی...")
    
    try:
        # Try importing the main bot
        import importlib.util
        spec = importlib.util.spec_from_file_location("crypto_bot", "crypto_bot_enhanced (1).py")
        crypto_bot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(crypto_bot)
        
        # Create bot instance
        bot = crypto_bot.CryptoSignalBot()
        print("✅ Bot با موفقیت import شد")
        print(f"✅ تعداد جفت ارزها: {len(bot.trading_pairs)}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در import bot: {e}")
        return False

def test_dependencies():
    """Test if all dependencies are available"""
    print("📦 بررسی بسته های مورد نیاز...")
    
    dependencies = [
        'fastapi', 'uvicorn', 'ccxt', 'pandas', 
        'numpy', 'requests', 'ta', 'apscheduler', 'aiohttp'
    ]
    
    missing = []
    available = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            available.append(dep)
        except ImportError:
            missing.append(dep)
    
    print(f"✅ موجود ({len(available)}): {', '.join(available)}")
    
    if missing:
        print(f"❌ ناموجود ({len(missing)}): {', '.join(missing)}")
        print("\n📦 برای نصب:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("✅ همه بسته ها موجود هستند")
    return True

async def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 آزمون کامل سیستم سیگنال ارز دیجیتال")
    print("🧪 Complete Crypto Signal System Test")
    print("=" * 60)
    
    # Test 1: Dependencies
    print("\n1️⃣ تست بسته ها...")
    deps_ok = test_dependencies()
    
    if not deps_ok:
        print("\n❌ لطفاً ابتدا بسته های ناموجود را نصب کنید")
        return
    
    # Test 2: Bot import
    print("\n2️⃣ تست import bot...")
    bot_ok = await test_bot_import()
    
    # Test 3: Signals
    print("\n3️⃣ تست سیگنال ها...")
    signals_ok = await test_signals()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 خلاصه نتایج:")
    print(f"   • بسته ها: {'✅' if deps_ok else '❌'}")
    print(f"   • Bot: {'✅' if bot_ok else '❌'}")
    print(f"   • سیگنال ها: {'✅' if signals_ok else '❌'}")
    
    if all([deps_ok, bot_ok, signals_ok]):
        print("\n🎉 همه تست ها موفق! سیستم آماده است")
        print("🚀 می‌توانید run_all.py را اجرا کنید")
    else:
        print("\n⚠️ برخی تست ها ناموفق - لطفاً مشکلات را بررسی کنید")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ تست متوقف شد")
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}")