from fastapi import FastAPI
from scheduler import start_scheduler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    print("🚀 Bot + Analyzer started")

@app.get("/")
def root():
    return {"status": "Bot is running"}
