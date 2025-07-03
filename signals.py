#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Signals module for crypto bot - Persian Enhanced
سیگنال های ارز دیجیتال - ورژن فارسی
"""

import asyncio
import json
from datetime import datetime
from typing import List, Tuple, Optional
import os

# Import the main bot class
try:
    from crypto_bot_enhanced import CryptoSignalBot
except ImportError:
    # Handle the space in filename
    import importlib.util
    spec = importlib.util.spec_from_file_location("crypto_bot_enhanced", "crypto_bot_enhanced (1).py")
    crypto_bot_enhanced = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(crypto_bot_enhanced)
    CryptoSignalBot = crypto_bot_enhanced.CryptoSignalBot

# Global bot instance
bot = None

def initialize_bot():
    """Initialize the crypto bot"""
    global bot
    if bot is None:
        # You can add your Binance API keys here if needed
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        bot = CryptoSignalBot(api_key, api_secret)
    return bot

async def analyze() -> List[Tuple[str, str]]:
    """
    Main analysis function - Persian enhanced
    تابع اصلی تحلیل سیگنال ها
    """
    try:
        # Initialize bot
        current_bot = initialize_bot()
        
        print("🔍 شروع تحلیل بازار ارز دیجیتال...")
        print("🔍 Starting crypto market analysis...")
        
        # Scan all trading pairs
        signals = current_bot.scan_all_pairs()
        
        # Format results for Persian display
        formatted_signals = []
        
        if not signals:
            print("❌ هیچ سیگنالی یافت نشد")
            print("❌ No signals found")
            return [("STATUS", "🔍 در حال جستجوی سیگنال های جدید...")]
        
        # Process each signal
        for signal in signals:
            if signal and 'symbol' in signal:
                symbol = signal['symbol']
                signal_type = signal.get('signal_type', 'UNKNOWN')
                score = signal.get('score', 0)
                
                # Persian emoji mapping
                signal_emoji = {
                    'LONG': '🟢 خرید',
                    'SHORT': '🔴 فروش',
                    'BUY': '🟢 خرید', 
                    'SELL': '🔴 فروش'
                }
                
                # Create formatted signal message
                signal_text = f"{signal_emoji.get(signal_type, '⚪')} | امتیاز: {score:.1%}"
                
                # Add entry/exit points if available
                if 'entry_exit_points' in signal:
                    entry_points = signal['entry_exit_points']
                    signal_text += f" | ورود: ${entry_points.get('entry_price', 'N/A')}"
                    signal_text += f" | هدف: ${entry_points.get('take_profit_1', 'N/A')}"
                
                formatted_signals.append((symbol, signal_text))
                
                # Save detailed signal to file for reference
                save_signal_details(signal)
        
        # Update active signals
        current_bot.update_active_signals()
        
        # Add market summary
        fear_greed = current_bot.get_fear_greed_index()
        if fear_greed:
            mood = get_persian_mood(fear_greed)
            formatted_signals.append(("MARKET", f"🧠 حس بازار: {mood} ({fear_greed})"))
        
        print(f"✅ {len(formatted_signals)} سیگنال پردازش شد")
        print(f"✅ Processed {len(formatted_signals)} signals")
        
        return formatted_signals
        
    except Exception as e:
        print(f"❌ خطا در تحلیل: {e}")
        print(f"❌ Analysis error: {e}")
        return [("ERROR", f"⚠️ خطا: {str(e)[:50]}...")]

def get_persian_mood(fear_greed_index: int) -> str:
    """Convert fear greed index to Persian mood"""
    if fear_greed_index <= 20:
        return "ترس شدید 😱"
    elif fear_greed_index <= 40:
        return "ترس 😟"
    elif fear_greed_index <= 60:
        return "خنثی 😐"
    elif fear_greed_index <= 80:
        return "طمع 😊"
    else:
        return "طمع شدید 🤑"

def save_signal_details(signal: dict):
    """Save detailed signal information to file"""
    try:
        # Create signals directory if it doesn't exist
        os.makedirs("signals_history", exist_ok=True)
        
        # Prepare signal data
        signal_data = {
            'timestamp': datetime.now().isoformat(),
            'timestamp_persian': datetime.now().strftime('%Y/%m/%d - %H:%M:%S'),
            'signal': signal
        }
        
        # Save to JSON file
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"signals_history/signals_{date_str}.json"
        
        # Load existing signals or create new list
        existing_signals = []
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_signals = json.load(f)
            except:
                existing_signals = []
        
        # Add new signal
        existing_signals.append(signal_data)
        
        # Keep only last 50 signals per day
        if len(existing_signals) > 50:
            existing_signals = existing_signals[-50:]
        
        # Save back to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_signals, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"⚠️ خطا در ذخیره سیگنال: {e}")

async def get_active_signals() -> List[dict]:
    """Get currently active signals"""
    try:
        current_bot = initialize_bot()
        
        if hasattr(current_bot, 'active_signals'):
            active = []
            for symbol, signal in current_bot.active_signals.items():
                status = current_bot.track_signal_status(signal)
                signal_with_status = {
                    **signal,
                    'current_status': status,
                    'symbol': symbol
                }
                active.append(signal_with_status)
            return active
        return []
    except Exception as e:
        print(f"❌ خطا در دریافت سیگنال های فعال: {e}")
        return []

async def get_market_summary() -> dict:
    """Get market summary in Persian"""
    try:
        current_bot = initialize_bot()
        
        # Get Fear & Greed Index
        fear_greed = current_bot.get_fear_greed_index()
        mood = get_persian_mood(fear_greed) if fear_greed else "نامشخص"
        
        # Get top performing pairs
        signals = current_bot.scan_all_pairs()
        
        bullish_count = len([s for s in signals if s and s.get('signal_type') == 'LONG'])
        bearish_count = len([s for s in signals if s and s.get('signal_type') == 'SHORT'])
        
        return {
            'fear_greed_index': fear_greed,
            'mood_persian': mood,
            'bullish_signals': bullish_count,
            'bearish_signals': bearish_count,
            'total_pairs_analyzed': len(current_bot.trading_pairs),
            'timestamp': datetime.now().isoformat(),
            'timestamp_persian': datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
        }
        
    except Exception as e:
        print(f"❌ خطا در خلاصه بازار: {e}")
        return {'error': str(e)}

# Persian welcome message
def print_welcome():
    """Print Persian welcome message"""
    print("=" * 60)
    print("🤖 ربات سیگنال ارز دیجیتال - نسخه پیشرفته")
    print("🚀 Crypto Signal Bot - Enhanced Version")
    print("=" * 60)
    print("📊 تحلیل هوشمند بازار با:")
    print("   • تحلیل تکنیکال پیشرفته")
    print("   • مفاهیم Smart Money")
    print("   • تحلیل حجم معاملات")
    print("   • شاخص ترس و طمع")
    print("=" * 60)

# Initialize on import
if __name__ == "__main__":
    print_welcome()
    
    # Test the analysis function
    async def test():
        signals = await analyze()
        for symbol, signal in signals:
            print(f"{symbol}: {signal}")
    
    asyncio.run(test())