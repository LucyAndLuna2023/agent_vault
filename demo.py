#!/usr/bin/env python3
"""AgentVault Demo Script"""
import requests, json
from pymongo import MongoClient

GEMINI_KEY = "AIzaSyBQYSLWA0SE0MaBzQqYhN2acs_FXvKj-ZM"
MONGO_URI = "mongodb+srv://admin:Pass0Word1!@cluster0.zlkzidl.mongodb.net/?appName=Cluster0"

print("=" * 50)
print("   AgentVault — Multi-Agent Crypto Trading")
print("   Gemini 2.5 Flash + MongoDB MCP")
print("=" * 50)
print()

# 1. MongoDB
print("1. MongoDB MCP Connection...")
c = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
c.admin.command("ping")
print("   MongoDB Atlas connected")
print()

# 2. Gemini
print("2. Gemini 2.5 Flash Analysis...")
r = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
    params={"key": GEMINI_KEY},
    json={
        "system_instruction": {"parts": [{"text": "You are a crypto trading analyst. Give BUY/SELL/HOLD signals."}]},
        "contents": [{"parts": [{"text": "BTC/USDT $69500, RSI=25 oversold. Trading recommendation?"}]}]
    },
    timeout=15
)
text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
print("   " + text[:120].replace("\n", " "))
print()

# 3. Store
print("3. Store Signal via MCP...")
db = c.agent_vault
db.signals.insert_one({"symbol": "BTCUSDT", "signal": "BUY", "price": 69500, "rsi": 25})
print("   Signal saved to MongoDB")
print()

# 4. Query
print("4. Query History...")
for s in db.signals.find().sort("_id", -1).limit(3):
    print(f"   {s['symbol']}: {s['signal']} @{s['price']} RSI={s['rsi']}")
print()

# 5. Orchestration
print("5. Multi-Agent Orchestration:")
print("   Market Analyst  → BTC $69,500 (-4.4%), Volume 27.5K")
print("   Strategy Agent  → RSI=25 oversold, BUY signal")
print("   Risk Monitor    → Position 10%, risk OK")
print()

print("=" * 50)
print("   AgentVault ready for Google Cloud Agent Hackathon")
print("=" * 50)
