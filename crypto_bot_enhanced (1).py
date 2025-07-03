#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Crypto Signal Bot - Binance Scanner
Enhanced with Volume Analysis + Signal Tracking
Smart Money Concepts + Fundamental Analysis
Intraday Trading (Max 24 hours)
"""

import ccxt
import pandas as pd
import numpy as np
import requests
import json
import time
from datetime import datetime, timedelta
import ta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class CryptoSignalBot:
    def __init__(self, api_key: str = None, api_secret: str = None):
        """
        Initialize Crypto Analysis Bot
        """
        # Binance Setup
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'sandbox': False,  # True for testing
            'enableRateLimit': True,
        })
        
        # Trading pairs
        self.trading_pairs = [
            'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT',
            'MATIC/USDT', 'AVAX/USDT', 'DOT/USDT', 'LINK/USDT',
            'DOGE/USDT', 'XRP/USDT', 'BNB/USDT', 'ATOM/USDT'
        ]
        
        # Timeframes for analysis
        self.timeframes = ['15m', '1h', '4h', '1d']
        
        # Strategy parameters
        self.min_rr_ratio = 2.0  # Minimum Risk/Reward
        self.max_risk_percent = 2.0  # Max risk per trade
        self.min_volume_spike = 1.5  # Minimum volume spike multiplier
        
        # Active signals tracking
        self.active_signals = {}
        
        print("🤖 Enhanced Crypto Analysis Bot Initialized!")
    
    def get_fear_greed_index(self) -> Optional[int]:
        """
        Get Fear & Greed Index
        """
        try:
            url = "https://api.alternative.me/fng/"
            response = requests.get(url, timeout=10)
            data = response.json()
            return int(data['data'][0]['value'])
        except:
            return None
    
    def get_market_data(self, symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
        """
        Fetch price data from Binance
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate Volume-based indicators
        """
        if df.empty or len(df) < 20:
            return df
        
        # Volume Moving Average
        df['volume_ma_20'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma_20']
        
        # Volume Spike Detection
        df['volume_spike'] = df['volume_ratio'] > self.min_volume_spike
        
        # On Balance Volume (OBV)
        df['obv'] = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume']).on_balance_volume()
        df['obv_ma'] = df['obv'].rolling(window=10).mean()
        df['obv_trend'] = df['obv'] > df['obv_ma']
        
        # Volume Price Trend (VPT)
        df['vpt'] = ta.volume.VolumePriceTrendIndicator(df['close'], df['volume']).volume_price_trend()
        df['vpt_ma'] = df['vpt'].rolling(window=10).mean()
        df['vpt_trend'] = df['vpt'] > df['vpt_ma']
        
        # Money Flow Index (MFI)
        df['mfi'] = ta.volume.MFIIndicator(df['high'], df['low'], df['close'], df['volume']).money_flow_index()
        
        return df
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate enhanced technical indicators
        """
        if df.empty or len(df) < 50:
            return df
        
        # ATR
        df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()
        
        # RSI
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
        
        # MACD
        macd = ta.trend.MACD(df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_histogram'] = macd.macd_diff()
        
        # Bollinger Bands
        bb = ta.volatility.BollingerBands(df['close'])
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_lower'] = bb.bollinger_lband()
        df['bb_middle'] = bb.bollinger_mavg()
        
        # EMA
        df['ema_20'] = ta.trend.EMAIndicator(df['close'], window=20).ema_indicator()
        df['ema_50'] = ta.trend.EMAIndicator(df['close'], window=50).ema_indicator()
        
        return df
    
    def detect_market_structure(self, df: pd.DataFrame) -> Dict:
        """
        Enhanced Market Structure detection (SMC)
        """
        if len(df) < 50:
            return {'trend': 'UNKNOWN', 'strength': 0, 'confidence': 0}
        
        # Calculate Swing Highs/Lows with volume confirmation
        df_with_indicators = self.calculate_technical_indicators(df)
        df_with_volume = self.calculate_volume_indicators(df_with_indicators)
        
        # Swing detection with volume
        highs = df_with_volume['high'].rolling(window=5).max()
        lows = df_with_volume['low'].rolling(window=5).min()
        
        # Enhanced trend detection
        recent_highs = highs.tail(10)
        recent_lows = lows.tail(10)
        recent_volume = df_with_volume['volume_spike'].tail(10)
        
        hh_count = sum(recent_highs.diff() > 0)
        ll_count = sum(recent_lows.diff() < 0)
        volume_confirmation = sum(recent_volume) / len(recent_volume)
        
        # EMA trend confirmation
        ema_trend = 1 if df_with_volume['ema_20'].iloc[-1] > df_with_volume['ema_50'].iloc[-1] else -1
        
        if hh_count >= 6 and volume_confirmation > 0.3:
            return {
                'trend': 'BULLISH', 
                'strength': min(hh_count/10, 1.0),
                'confidence': (volume_confirmation + (ema_trend + 1)/2) / 2
            }
        elif ll_count >= 6 and volume_confirmation > 0.3:
            return {
                'trend': 'BEARISH', 
                'strength': min(ll_count/10, 1.0),
                'confidence': (volume_confirmation + (1 - ema_trend)/2) / 2
            }
        else:
            return {
                'trend': 'SIDEWAYS', 
                'strength': 0.5,
                'confidence': volume_confirmation
            }
    
    def find_order_blocks_enhanced(self, df: pd.DataFrame) -> List[Dict]:
        """
        Enhanced Order Blocks detection with volume
        """
        if len(df) < 20:
            return []
        
        df_enhanced = self.calculate_volume_indicators(df)
        order_blocks = []
        
        for i in range(10, len(df_enhanced)-5):
            current_candle = df_enhanced.iloc[i]
            volume_spike = df_enhanced.iloc[i]['volume_spike']
            
            # Enhanced Bullish Order Block
            if (df_enhanced.iloc[i+1]['close'] > df_enhanced.iloc[i]['high'] and 
                df_enhanced.iloc[i+2]['close'] > df_enhanced.iloc[i+1]['close'] and
                volume_spike):
                
                order_blocks.append({
                    'type': 'BULLISH_OB',
                    'high': current_candle['high'],
                    'low': current_candle['low'],
                    'timestamp': current_candle.name,
                    'strength': 0.9 if volume_spike else 0.6,
                    'volume_ratio': df_enhanced.iloc[i]['volume_ratio']
                })
            
            # Enhanced Bearish Order Block
            elif (df_enhanced.iloc[i+1]['close'] < df_enhanced.iloc[i]['low'] and 
                  df_enhanced.iloc[i+2]['close'] < df_enhanced.iloc[i+1]['close'] and
                  volume_spike):
                
                order_blocks.append({
                    'type': 'BEARISH_OB',
                    'high': current_candle['high'],
                    'low': current_candle['low'],
                    'timestamp': current_candle.name,
                    'strength': 0.9 if volume_spike else 0.6,
                    'volume_ratio': df_enhanced.iloc[i]['volume_ratio']
                })
        
        return order_blocks[-5:]  # Last 5 Order Blocks
    
    def detect_divergences(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect RSI and MACD divergences
        """
        if len(df) < 50:
            return []
        
        df_indicators = self.calculate_technical_indicators(df)
        divergences = []
        
        # Look for divergences in last 20 candles
        for i in range(20, len(df_indicators)):
            price_high = df_indicators['high'].iloc[i-20:i].max()
            price_low = df_indicators['low'].iloc[i-20:i].min()
            current_price = df_indicators['close'].iloc[i]
            
            rsi_current = df_indicators['rsi'].iloc[i]
            rsi_prev_extreme = df_indicators['rsi'].iloc[i-20:i-5].max() if current_price > price_high * 0.98 else df_indicators['rsi'].iloc[i-20:i-5].min()
            
            # Bullish Divergence
            if (current_price <= price_low * 1.02 and 
                rsi_current > rsi_prev_extreme and 
                rsi_current < 40):
                divergences.append({
                    'type': 'BULLISH_DIVERGENCE',
                    'indicator': 'RSI',
                    'strength': 0.8,
                    'timestamp': df_indicators.index[i]
                })
            
            # Bearish Divergence
            elif (current_price >= price_high * 0.98 and 
                  rsi_current < rsi_prev_extreme and 
                  rsi_current > 60):
                divergences.append({
                    'type': 'BEARISH_DIVERGENCE',
                    'indicator': 'RSI',
                    'strength': 0.8,
                    'timestamp': df_indicators.index[i]
                })
        
        return divergences[-3:]  # Last 3 divergences
    
    def enhanced_signal_scoring(self, symbol: str, df_15m: pd.DataFrame, 
                              df_1h: pd.DataFrame, df_4h: pd.DataFrame) -> Optional[Dict]:
        """
        Enhanced signal generation with multiple confirmations
        """
        if any(df.empty for df in [df_15m, df_1h, df_4h]):
            return None
        
        # Market Structure Analysis
        structure_1h = self.detect_market_structure(df_1h)
        structure_4h = self.detect_market_structure(df_4h)
        
        # Smart Money Concepts
        order_blocks = self.find_order_blocks_enhanced(df_1h)
        divergences = self.detect_divergences(df_1h)
        
        # Volume Analysis
        df_1h_vol = self.calculate_volume_indicators(df_1h)
        volume_trend = df_1h_vol['obv_trend'].iloc[-1]
        recent_volume_spike = df_1h_vol['volume_spike'].tail(5).sum() >= 2
        
        # Technical Indicators
        df_1h_tech = self.calculate_technical_indicators(df_1h)
        rsi_current = df_1h_tech['rsi'].iloc[-1]
        mfi_current = df_1h_vol['mfi'].iloc[-1]
        
        # Fundamental Analysis
        sentiment = self.get_on_chain_sentiment(symbol)
        
        # LONG Signal Conditions (Enhanced)
        long_conditions = {
            'structure_bullish_1h': structure_1h['trend'] == 'BULLISH',
            'structure_confidence': structure_1h['confidence'] > 0.6,
            'structure_4h_favorable': structure_4h['trend'] in ['BULLISH', 'SIDEWAYS'],
            'bullish_order_blocks': len([ob for ob in order_blocks if ob['type'] == 'BULLISH_OB']) > 0,
            'volume_confirmation': volume_trend and recent_volume_spike,
            'rsi_oversold_recovery': 30 < rsi_current < 70,
            'mfi_favorable': mfi_current > 50,
            'sentiment_positive': sentiment['score'] > 55,
            'bullish_divergence': len([d for d in divergences if d['type'] == 'BULLISH_DIVERGENCE']) > 0
        }
        
        # SHORT Signal Conditions (Enhanced)
        short_conditions = {
            'structure_bearish_1h': structure_1h['trend'] == 'BEARISH',
            'structure_confidence': structure_1h['confidence'] > 0.6,
            'structure_4h_favorable': structure_4h['trend'] in ['BEARISH', 'SIDEWAYS'],
            'bearish_order_blocks': len([ob for ob in order_blocks if ob['type'] == 'BEARISH_OB']) > 0,
            'volume_confirmation': (not volume_trend) and recent_volume_spike,
            'rsi_overbought_decline': 30 < rsi_current < 70,
            'mfi_unfavorable': mfi_current < 50,
            'sentiment_negative': sentiment['score'] < 45,
            'bearish_divergence': len([d for d in divergences if d['type'] == 'BEARISH_DIVERGENCE']) > 0
        }
        
        long_score = sum(long_conditions.values())
        short_score = sum(short_conditions.values())
        
        # Enhanced scoring system
        if long_score >= 6:  # Stricter requirement
            return {
                'signal_type': 'LONG',
                'score': long_score / len(long_conditions),
                'conditions_met': {k: v for k, v in long_conditions.items() if v},
                'structure_1h': structure_1h,
                'structure_4h': structure_4h,
                'order_blocks': order_blocks,
                'divergences': divergences,
                'sentiment': sentiment,
                'volume_analysis': {
                    'volume_trend': volume_trend,
                    'recent_spike': recent_volume_spike,
                    'mfi': mfi_current
                }
            }
        elif short_score >= 6:  # Stricter requirement
            return {
                'signal_type': 'SHORT',
                'score': short_score / len(short_conditions),
                'conditions_met': {k: v for k, v in short_conditions.items() if v},
                'structure_1h': structure_1h,
                'structure_4h': structure_4h,
                'order_blocks': order_blocks,
                'divergences': divergences,
                'sentiment': sentiment,
                'volume_analysis': {
                    'volume_trend': volume_trend,
                    'recent_spike': recent_volume_spike,
                    'mfi': mfi_current
                }
            }
        
        return None
    
    def get_on_chain_sentiment(self, symbol: str) -> Dict:
        """
        Fundamental and On-Chain Analysis (simplified)
        """
        try:
            fear_greed = self.get_fear_greed_index()
            
            if fear_greed is None:
                return {'sentiment': 'NEUTRAL', 'score': 50}
            
            if fear_greed < 20:
                sentiment = 'EXTREME_FEAR'
                score = 85  # Strong buy opportunity
            elif fear_greed < 40:
                sentiment = 'FEAR'
                score = 70
            elif fear_greed > 80:
                sentiment = 'EXTREME_GREED'
                score = 15  # Strong sell signal
            elif fear_greed > 60:
                sentiment = 'GREED'
                score = 30
            else:
                sentiment = 'NEUTRAL'
                score = 50
            
            return {
                'sentiment': sentiment,
                'score': score,
                'fear_greed_index': fear_greed
            }
        except:
            return {'sentiment': 'NEUTRAL', 'score': 50}
    
    def calculate_entry_exit_points(self, df: pd.DataFrame, signal_type: str) -> Dict:
        """
        Calculate entry, stop loss and target points
        """
        if df.empty:
            return {}
        
        df_tech = self.calculate_technical_indicators(df)
        current_price = df_tech.iloc[-1]['close']
        atr = df_tech.iloc[-1]['atr']
        bb_upper = df_tech.iloc[-1]['bb_upper']
        bb_lower = df_tech.iloc[-1]['bb_lower']
        
        if signal_type == 'LONG':
            # Entry: Near support or pullback
            entry_price = current_price * 0.997  # 0.3% below current
            
            # Stop Loss: Below recent low or ATR-based
            recent_low = df['low'].tail(10).min()
            sl_atr = entry_price - (atr * 1.8)
            stop_loss = min(recent_low * 0.995, sl_atr)
            
            # Take Profits with better RR
            risk = entry_price - stop_loss
            tp1 = entry_price + (risk * 1.8)  # 1:1.8 RR
            tp2 = entry_price + (risk * 3.0)  # 1:3 RR  
            tp3 = entry_price + (risk * 5.0)  # 1:5 RR
            
        else:  # SHORT
            # Entry: Near resistance or rejection
            entry_price = current_price * 1.003  # 0.3% above current
            
            # Stop Loss: Above recent high or ATR-based
            recent_high = df['high'].tail(10).max()
            sl_atr = entry_price + (atr * 1.8)
            stop_loss = max(recent_high * 1.005, sl_atr)
            
            # Take Profits
            risk = stop_loss - entry_price
            tp1 = entry_price - (risk * 1.8)
            tp2 = entry_price - (risk * 3.0)
            tp3 = entry_price - (risk * 5.0)
        
        return {
            'entry_price': round(entry_price, 6),
            'stop_loss': round(stop_loss, 6),
            'take_profit_1': round(tp1, 6),
            'take_profit_2': round(tp2, 6),
            'take_profit_3': round(tp3, 6),
            'risk_reward_ratio': round(abs(tp2 - entry_price) / abs(stop_loss - entry_price), 2)
        }
    
    def track_signal_status(self, signal: Dict) -> Dict:
        """
        Track active signal status
        """
        symbol = signal['symbol']
        current_data = self.get_market_data(symbol, '15m', 20)
        
        if current_data.empty:
            return {'status': 'ERROR', 'message': 'Unable to fetch current data'}
        
        current_price = current_data.iloc[-1]['close']
        entry_points = signal['entry_exit_points']
        signal_type = signal['signal_type']
        
        # Check signal status
        if signal_type == 'LONG':
            if current_price <= entry_points['stop_loss']:
                return {'status': 'STOPPED_OUT', 'current_price': current_price, 'pnl_percent': -2.0}
            elif current_price >= entry_points['take_profit_3']:
                return {'status': 'TP3_HIT', 'current_price': current_price, 'pnl_percent': 10.0}
            elif current_price >= entry_points['take_profit_2']:
                return {'status': 'TP2_HIT', 'current_price': current_price, 'pnl_percent': 6.0}
            elif current_price >= entry_points['take_profit_1']:
                return {'status': 'TP1_HIT', 'current_price': current_price, 'pnl_percent': 3.6}
            elif current_price >= entry_points['entry_price']:
                return {'status': 'IN_PROFIT', 'current_price': current_price, 'pnl_percent': ((current_price / entry_points['entry_price']) - 1) * 100}
            else:
                return {'status': 'WAITING_ENTRY', 'current_price': current_price, 'distance_to_entry': ((entry_points['entry_price'] / current_price) - 1) * 100}
        
        else:  # SHORT
            if current_price >= entry_points['stop_loss']:
                return {'status': 'STOPPED_OUT', 'current_price': current_price, 'pnl_percent': -2.0}
            elif current_price <= entry_points['take_profit_3']:
                return {'status': 'TP3_HIT', 'current_price': current_price, 'pnl_percent': 10.0}
            elif current_price <= entry_points['take_profit_2']:
                return {'status': 'TP2_HIT', 'current_price': current_price, 'pnl_percent': 6.0}
            elif current_price <= entry_points['take_profit_1']:
                return {'status': 'TP1_HIT', 'current_price': current_price, 'pnl_percent': 3.6}
            elif current_price <= entry_points['entry_price']:
                return {'status': 'IN_PROFIT', 'current_price': current_price, 'pnl_percent': ((entry_points['entry_price'] / current_price) - 1) * 100}
            else:
                return {'status': 'WAITING_ENTRY', 'current_price': current_price, 'distance_to_entry': ((current_price / entry_points['entry_price']) - 1) * 100}
    
    def generate_signal(self, symbol: str) -> Optional[Dict]:
        """
        Generate complete signal for a coin
        """
        # Skip if already have active signal for this symbol
        if symbol in self.active_signals:
            status = self.track_signal_status(self.active_signals[symbol])
            if status['status'] not in ['STOPPED_OUT', 'TP3_HIT']:
                return None  # Don't generate new signal
            else:
                # Remove completed signal
                del self.active_signals[symbol]
        
        print(f"🔍 Analyzing {symbol}...")
        
        # Fetch data
        df_15m = self.get_market_data(symbol, '15m', 100)
        df_1h = self.get_market_data(symbol, '1h', 100)
        df_4h = self.get_market_data(symbol, '4h', 50)
        
        if any(df.empty for df in [df_15m, df_1h, df_4h]):
            return None
        
        # Enhanced signal analysis
        signal_analysis = self.enhanced_signal_scoring(symbol, df_15m, df_1h, df_4h)
        
        if signal_analysis:
            # Calculate entry/exit points
            entry_exit = self.calculate_entry_exit_points(df_1h, signal_analysis['signal_type'])
            
            if entry_exit and entry_exit.get('risk_reward_ratio', 0) >= self.min_rr_ratio:
                signal = {
                    'symbol': symbol,
                    'signal_type': signal_analysis['signal_type'],
                    'signal_strength': round(signal_analysis['score'], 2),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'current_price': df_1h.iloc[-1]['close'],
                    'conditions_met': signal_analysis['conditions_met'],
                    'market_structure_1h': signal_analysis['structure_1h'],
                    'market_structure_4h': signal_analysis['structure_4h'],
                    'sentiment': signal_analysis['sentiment'],
                    'volume_analysis': signal_analysis['volume_analysis'],
                    'entry_exit_points': entry_exit,
                    'order_blocks': signal_analysis['order_blocks'],
                    'divergences': signal_analysis['divergences']
                }
                
                # Add to active signals
                self.active_signals[symbol] = signal
                return signal
        
        return None
    
    def scan_all_pairs(self) -> List[Dict]:
        """
        Scan all coins and generate signals
        """
        print("🚀 Starting market scan...")
        signals = []
        
        for pair in self.trading_pairs:
            try:
                signal = self.generate_signal(pair)
                if signal:
                    signals.append(signal)
                time.sleep(0.5)  # Prevent rate limiting
            except Exception as e:
                print(f"❌ Error analyzing {pair}: {e}")
                continue
        
        # Sort by signal strength
        signals.sort(key=lambda x: x['signal_strength'], reverse=True)
        return signals
    
    def update_active_signals(self):
        """
        Update status of all active signals
        """
        if not self.active_signals:
            return
        
        print(f"📊 Updating {len(self.active_signals)} active signals...")
        
        for symbol, signal in list(self.active_signals.items()):
            try:
                status = self.track_signal_status(signal)
                signal['current_status'] = status
                
                # Print status update
                if status['status'] in ['TP1_HIT', 'TP2_HIT', 'TP3_HIT']:
                    print(f"🎯 {symbol} {signal['signal_type']}: {status['status']} | PnL: +{status['pnl_percent']:.1f}%")
                elif status['status'] == 'STOPPED_OUT':
                    print(f"🛑 {symbol} {signal['signal_type']}: STOPPED OUT | PnL: {status['pnl_percent']:.1f}%")
                    del self.active_signals[symbol]  # Remove stopped signals
                elif status['status'] == 'IN_PROFIT':
                    print(f"💚 {symbol} {signal['signal_type']}: IN PROFIT | PnL: +{status['pnl_percent']:.1f}%")
                
                # Remove completed signals
                if status['status'] in ['TP3_HIT']:
                    del self.active_signals[symbol]
                    
            except Exception as e:
                print(f"❌ Error updating {symbol}: {e}")
    
    def format_signal_output(self, signal: Dict) -> str:
        """
        Format signal output
        """
        conditions_text = "\n".join([f"• {k.replace('_', ' ').title()}" for k in signal['conditions_met'].keys()])
        
        output = f"""
🎯 {signal['signal_type']} SIGNAL - {signal['symbol']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Signal Overview:
• Strength: {signal['signal_strength']*100:.0f}%
• Current Price: ${signal['current_price']:.4f}
• Timestamp: {signal['timestamp']}

💰 Trading Levels:
• Entry: ${signal['entry_exit_points']['entry_price']:.4f}
• Stop Loss: ${signal['entry_exit_points']['stop_loss']:.4f}
• Target 1: ${signal['entry_exit_points']['take_profit_1']:.4f}
• Target 2: ${signal['entry_exit_points']['take_profit_2']:.4f}
• Target 3: ${signal['entry_exit_points']['take_profit_3']:.4f}
• Risk/Reward: 1:{signal['entry_exit_points']['risk_reward_ratio']}

📈 Technical Analysis:
• Trend 1H: {signal['market_structure_1h']['trend']} (Confidence: {signal['market_structure_1h']['confidence']:.1f})
• Trend 4H: {signal['market_structure_4h']['trend']}
• Order Blocks: {len(signal['order_blocks'])}
• Divergences: {len(signal['divergences'])}

📊 Volume Analysis:
• OBV Trend: {'Bullish' if signal['volume_analysis']['volume_trend'] else 'Bearish'}
• Recent Volume Spike: {'Yes' if signal['volume_analysis']['recent_spike'] else 'No'}
• MFI: {signal['volume_analysis']['mfi']:.1f}

🔍 Market Sentiment:
• Sentiment: {signal['sentiment']['sentiment']}
• Score: {signal['sentiment']['score']}/100
• Fear & Greed: {signal['sentiment'].get('fear_greed_index', 'N/A')}

✅ Conditions Met:
{conditions_text}

⚠️ Risk Management:
• Max Risk: 2% of capital
• Position Size: Calculate based on stop distance
• Time Frame: Max 24 hours
• TP Distribution: TP1=40% | TP2=35% | TP3=25%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        return output
    
    def format_signal_status(self, symbol: str, signal: Dict) -> str:
        """
        Format active signal status
        """
        status = signal.get('current_status', {})
        if not status:
            return f"❓ {symbol}: Status unknown"
        
        status_icons = {
            'WAITING_ENTRY': '⏳',
            'IN_PROFIT': '💚',
            'TP1_HIT': '🎯',
            'TP2_HIT': '🎯🎯',
            'TP3_HIT': '🎯🎯🎯',
            'STOPPED_OUT': '🛑'
        }
        
        icon = status_icons.get(status['status'], '❓')
        
        if status['status'] == 'WAITING_ENTRY':
            return f"{icon} {symbol} {signal['signal_type']}: Waiting Entry | Distance: {status['distance_to_entry']:.2f}%"
        elif 'pnl_percent' in status:
            pnl_sign = '+' if status['pnl_percent'] > 0 else ''
            return f"{icon} {symbol} {signal['signal_type']}: {status['status']} | PnL: {pnl_sign}{status['pnl_percent']:.1f}%"
        else:
            return f"{icon} {symbol} {signal['signal_type']}: {status['status']}"
    
    def run_continuous_scan(self, interval_minutes: int = 30):
        """
        Continuous market scanning with active signal tracking
        """
        print(f"🔄 Starting continuous scan every {interval_minutes} minutes...")
        print("📊 Active signal tracking enabled")
        
        scan_count = 0
        
        while True:
            try:
                scan_count += 1
                print(f"\n🔍 Scan #{scan_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Update active signals first
                self.update_active_signals()
                
                # Show active signals status
                if self.active_signals:
                    print(f"\n📊 Active Signals ({len(self.active_signals)}):")
                    for symbol, signal in self.active_signals.items():
                        print(self.format_signal_status(symbol, signal))
                
                # Scan for new signals
                new_signals = self.scan_all_pairs()
                
                if new_signals:
                    print(f"\n🎉 {len(new_signals)} NEW SIGNALS FOUND!")
                    for signal in new_signals:
                        print(self.format_signal_output(signal))
                        print("=" * 50)
                else:
                    print(f"⏳ No new signals found")
                
                # Summary
                total_active = len(self.active_signals)
                print(f"\n📈 Summary: {total_active} active signals | {len(new_signals)} new signals")
                
                # Wait for next scan
                print(f"⏰ Next scan in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                print("\n⏹️ Scan stopped by user!")
                break
            except Exception as e:
                print(f"❌ Scan error: {e}")
                time.sleep(60)  # Wait 1 minute before retry
    
    def show_performance_summary(self):
        """
        Show performance summary of completed signals
        """
        # This would be enhanced with a database to track historical performance
        print("📊 Performance Summary:")
        print("• Total Signals Generated: Track in database")
        print("• Win Rate: Calculate from completed signals")
        print("• Average RR: Calculate from winning trades")
        print("• Max Drawdown: Track from trading history")
    
    def export_signals_to_json(self, signals: List[Dict], filename: str = None):
        """
        Export signals to JSON file
        """
        if not filename:
            filename = f"crypto_signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(signals, f, indent=2, default=str)
            print(f"📁 Signals exported to {filename}")
        except Exception as e:
            print(f"❌ Export error: {e}")
    
    def get_market_overview(self):
        """
        Get overall market overview
        """
        print("🌐 Market Overview:")
        
        # Fear & Greed Index
        fg_index = self.get_fear_greed_index()
        if fg_index:
            print(f"• Fear & Greed Index: {fg_index}")
        
        # Count trends across all pairs
        bullish_count = 0
        bearish_count = 0
        
        for pair in self.trading_pairs[:6]:  # Check first 6 pairs for speed
            try:
                df = self.get_market_data(pair, '1h', 50)
                if not df.empty:
                    structure = self.detect_market_structure(df)
                    if structure['trend'] == 'BULLISH':
                        bullish_count += 1
                    elif structure['trend'] == 'BEARISH':
                        bearish_count += 1
            except:
                continue
        
        total_checked = bullish_count + bearish_count
        if total_checked > 0:
            print(f"• Market Sentiment: {bullish_count}/{total_checked} pairs bullish")
        
        print(f"• Active Signals: {len(self.active_signals)}")

def main():
    """
    Main execution function
    """
    print("🎯 Enhanced Crypto Signal Bot")
    print("=" * 40)
    print("Features:")
    print("• Volume-based confirmations")
    print("• Active signal tracking")
    print("• Enhanced SMC analysis")
    print("• Divergence detection")
    print("• Real-time status updates")
    print("=" * 40)
    
    # For real API usage, enter your keys
    # api_key = "YOUR_BINANCE_API_KEY"
    # api_secret = "YOUR_BINANCE_API_SECRET"
    
    # Demo mode (without API)
    bot = CryptoSignalBot()
    
    # Show market overview
    bot.get_market_overview()
    
    # Menu options
    print("\nSelect mode:")
    print("1. Single scan")
    print("2. Continuous scan with tracking")
    print("3. Check active signals only")
    print("4. Performance summary")
    
    choice = input("Enter choice (1-4): ")
    
    if choice == "1":
        signals = bot.scan_all_pairs()
        if signals:
            print(f"\n🎉 Found {len(signals)} signals!")
            for signal in signals:
                print(bot.format_signal_output(signal))
            
            # Ask to export
            export = input("\nExport to JSON? (y/n): ")
            if export.lower() == 'y':
                bot.export_signals_to_json(signals)
        else:
            print("❌ No signals found!")
    
    elif choice == "2":
        try:
            interval = int(input("Scan interval (minutes) [default: 30]: ") or "30")
            bot.run_continuous_scan(interval)
        except ValueError:
            print("❌ Invalid number!")
    
    elif choice == "3":
        if bot.active_signals:
            print(f"\n📊 Active Signals ({len(bot.active_signals)}):")
            bot.update_active_signals()
            for symbol, signal in bot.active_signals.items():
                print(bot.format_signal_status(symbol, signal))
        else:
            print("📭 No active signals")
    
    elif choice == "4":
        bot.show_performance_summary()
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()