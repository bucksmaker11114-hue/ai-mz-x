# backend/ai_core.py
import os, time, random

_model = None
_model_mtime = 0

def load_model():
    # Itt történne a valódi AI betöltés (pl. TensorFlow / sklearn)
    print("AI modell betöltése memóriába...")
    return {"name": "AI-Trader-v2", "version": "2.0"}

def get_model():
    global _model, _model_mtime
    path = "models/model.pkl"
    if not os.path.exists(path):
        return load_model()

    mtime = os.path.getmtime(path)
    if _model is None or mtime != _model_mtime:
        _model = load_model()
        _model_mtime = mtime
    return _model

def get_live_prices():
    # Itt jönnének az aktuális piaci adatok (pl. API-ból)
    return {"price": round(random.uniform(1.0, 2.0), 5), "timestamp": time.time()}

def analyze_market(pair):
    model = get_model()
    prices = get_live_prices()
    signal = random.choice(["BUY", "SELL", "HOLD"])
    confidence = round(random.uniform(60, 95), 2)
    return {
        "pair": pair,
        "signal": signal,
        "confidence": confidence,
        "price": prices["price"],
        "model": model["name"],
        "time": prices["timestamp"]
    }
