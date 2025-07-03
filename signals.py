#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crypto Signals Module
This module provides the analyze function for the scheduler
"""

import sys
import os

# Import the CryptoSignalBot class
# Note: Handle the space in filename by importing properly
bot_filename = 'crypto_bot_enhanced (1).py'
if os.path.exists(bot_filename):
    import importlib.util
    spec = importlib.util.spec_from_file_location("crypto_bot_enhanced", bot_filename)
    crypto_bot_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(crypto_bot_module)
    CryptoSignalBot = crypto_bot_module.CryptoSignalBot
else:
    # Fallback - try direct import if file renamed
    try:
        from crypto_bot_enhanced_1 import CryptoSignalBot
    except ImportError:
        print("❌ Could not import CryptoSignalBot. Please ensure crypto_bot_enhanced (1).py exists.")
        sys.exit(1)

# Global bot instance
bot = None

def initialize_bot():
    """Initialize the bot instance"""
    global bot
    if bot is None:
        # Initialize without API keys for read-only operations
        # Users can set their API keys in the crypto_bot_enhanced file if needed
        bot = CryptoSignalBot()
    return bot

async def analyze():
    """
    Main analysis function called by the scheduler
    Returns list of (symbol, signal) tuples
    """
    try:
        # Initialize bot if not already done
        bot_instance = initialize_bot()
        
        # Scan all pairs for signals
        signals = bot_instance.scan_all_pairs()
        
        # Format output for scheduler
        result = []
        for signal in signals:
            if signal and 'symbol' in signal:
                symbol = signal['symbol']
                signal_type = signal.get('signal_type', 'UNKNOWN')
                score = signal.get('score', 0)
                
                # Create readable signal description
                signal_desc = f"{signal_type} (Score: {score:.2f})"
                result.append((symbol, signal_desc))
        
        return result
        
    except Exception as e:
        print(f"❌ Error in analysis: {e}")
        return [("ERROR", f"Analysis failed: {str(e)}")]

# For testing purposes
if __name__ == "__main__":
    import asyncio
    
    async def test_analyze():
        print("🔍 Testing signal analysis...")
        results = await analyze()
        
        if results:
            print("\n📊 Current Signals:")
            for symbol, signal in results:
                print(f"  {symbol}: {signal}")
        else:
            print("  No signals found.")
    
    asyncio.run(test_analyze())