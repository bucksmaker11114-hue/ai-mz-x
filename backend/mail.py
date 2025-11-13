# backend/main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os, asyncio, json, datetime
from concurrent.futures import ThreadPoolExecutor

# Helyes import
from .ai_core import get_model, analyze_market, get_live_prices

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)

# --- Környezeti változók ---
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
API_KEY = os.getenv("API_KEY", "changeme")

# --- CORS engedélyezés ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Itt a többi websocket / route definíciód maradhat változatlan

def log_trade(pair, result):
    os.makedirs("reports", exist_ok=True)
    entry = {
        "time": datetime.datetime.now().isoformat(),
        "pair": pair,
        "result": result
    }
    with open("reports/trade_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# --- Futás Railway-en (opcionális, csak lokalhoz kell) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
