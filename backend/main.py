# backend/main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os, asyncio, json, datetime
from concurrent.futures import ThreadPoolExecutor
from ai_core import get_model, analyze_market, get_live_prices

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)

# --- Környezeti változók ---
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
API_KEY = os.getenv("API_KEY", "changeme")

# --- CORS engedélyezés ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REST API végpont ---
@app.get("/api/analyze/{pair}")
async def analyze(pair: str, key: str = None):
    if key != API_KEY:
        return {"error": "Unauthorized"}

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, analyze_market, pair)
    log_trade(pair, result)
    return {"pair": pair, "result": result}

# --- WebSocket: élő frissítés ---
@app.websocket("/ws/live")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        data = get_live_prices()
        await ws.send_json(data)
        await asyncio.sleep(3)

# --- Logolás JSON fájlba ---
def log_trade(pair, result):
    os.makedirs("reports", exist_ok=True)
    entry = {
        "time": datetime.datetime.now().isoformat(),
        "pair": pair,
        "result": result
    }
    with open("reports/trade_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# --- Futás Railway-en ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
