from apscheduler.schedulers.asyncio import AsyncIOScheduler
from signals import analyze

async def job():
    print("🔍 Running analysis...")
    signals = await analyze()
    for symbol, sig in signals:
        print(f"[{symbol}] → {sig}")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, 'interval', minutes=5)
    scheduler.start()
