from crypto_bot_enhanced import CryptoSignalBot

# Create global bot instance
bot = CryptoSignalBot()

async def analyze():
    """
    Main analysis function called by scheduler
    Returns list of (symbol, signal) tuples
    """
    print("🔍 Running market analysis...")
    
    # Get new signals
    signals = bot.scan_all_pairs()
    
    # Update existing signals
    bot.update_active_signals()
    
    # Format results
    results = []
    
    # Add new signals
    for signal in signals:
        signal_text = f"{signal['signal_type']} - Strength: {signal['signal_strength']*100:.0f}% - Entry: ${signal['entry_exit_points']['entry_price']:.4f}"
        results.append((signal['symbol'], signal_text))
    
    # Add active signals status
    for symbol, signal in bot.active_signals.items():
        status = signal.get('current_status', {})
        if status:
            status_text = f"ACTIVE {signal['signal_type']} - Status: {status.get('status', 'Unknown')}"
            if 'pnl_percent' in status:
                status_text += f" - PnL: {status['pnl_percent']:.1f}%"
            results.append((symbol, status_text))
    
    return results if results else [("MARKET", "No new signals found")]