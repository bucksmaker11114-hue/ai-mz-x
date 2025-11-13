import sqlite3
import os
import datetime

DB_PATH = "data/learn.db"

# Q-learning ügynök tanulásának integrálása az adatbázisba történő mentéssel
def update_learning(pair, action, reward, next_state, agent):
    # Q-learning frissítés
    agent.learn(pair, action, reward, next_state)  # A Q-tábla frissítése

    # A tanulás eredményeinek mentése az adatbázisba
    bias = agent.q_table.loc[pair, action]  # A döntéshez tartozó Q-érték (bias)
    risk = calculate_risk(bias)  # Kockázat kiszámítása, pl. volatilitás alapján
    decision = action  # A választott akció (buy, sell, hold)

    # Az adatbázisba való mentés
    save_to_db(pair, bias, risk, decision)

# Kockázat számítása (pl. egyszerű példa)
def calculate_risk(bias):
    return abs(bias)  # Példa, a kockázat lehet a bias abszolút értéke

# Az adatbázisba történő mentés
def save_to_db(pair, bias, risk, decision):
    # Adatbázis kapcsolat létrehozása
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Tábla létrehozása, ha nem létezik
    cur.execute("""CREATE TABLE IF NOT EXISTS learning (
        ts TEXT, pair TEXT, bias REAL, decision TEXT, risk_pct REAL, leverage INTEGER)""")
    
    # Új adat beszúrása
    cur.execute("INSERT INTO learning VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.datetime.now().isoformat(), pair, bias, decision, risk, 1))  # Tőkeáttétel alapértelmezés szerint 1

    # Változások mentése és kapcsolat lezárása
    conn.commit()
    conn.close()
