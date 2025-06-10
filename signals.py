import aiohttp
import asyncio
from datetime import datetime

BINANCE_API = 'https://api.binance.com'

async def fetch_symbols():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BINANCE_API}/api/v3/exchangeInfo') as res:
            data = await res.json()
            return [s['symbol'] for s in data['symbols'] if s['isSpotTradingAllowed'] and s['quoteAsset'] == 'USDT']

async def fetch_klines(symbol):
    async with aiohttp.ClientSession() as session:
        url = f'{BINANCE_API}/api/v3/klines?symbol={symbol}&interval=5m&limit=20'
        async with session.get(url) as res:
            return await res.json()

def detect_signal(candles):
    if len(candles) < 2:
        return None

    last = candles[-1]
    prev = candles[-2]

    close_now = float(last[4])
    close_prev = float(prev[4])

    if close_now > close_prev * 1.01:
        return "LONG"
    elif close_now < close_prev * 0.99:
        return "SHORT"
    return None

async def analyze():
    results = []
    symbols = await fetch_symbols()
    for symbol in symbols:
        try:
            candles = await fetch_klines(symbol)
            signal = detect_signal(candles)
            if signal:
                results.append((symbol, signal))
        except:
            continue
    return results
