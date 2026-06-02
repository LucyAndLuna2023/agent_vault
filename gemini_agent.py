"""AgentVault — Gemini + MongoDB MCP Multi-Agent"""
import requests, json, os

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBQYSLWA0SE0MaBzQqYhN2acs_FXvKj-ZM")
BASE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash"

def call_gemini(prompt, tools=None):
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    if tools:
        body["tools"] = [{"functionDeclarations": tools}]
    r = requests.post(f"{BASE}:generateContent?key={API_KEY}", json=body, timeout=15)
    d = r.json()
    parts = d.get("candidates",[{}])[0].get("content",{}).get("parts",[{}])
    text = parts[0].get("text","") if parts else ""
    calls = parts[0].get("functionCall") if parts else None
    return text, calls, d.get("usageMetadata",{})

MCP_TOOLS = [
    {"name": "store_trade", "description": "Store trade to MongoDB via MCP",
     "parameters": {"type": "object", "properties": {
         "symbol": {"type": "string"}, "side": {"type": "string"},
         "price": {"type": "number"}, "rsi": {"type": "number"}
     }}},
    {"name": "query_trades", "description": "Query recent trades from MongoDB",
     "parameters": {"type": "object", "properties": {
         "symbol": {"type": "string"}, "limit": {"type": "integer", "default": 10}
     }}}
]

if __name__ == "__main__":
    text, _, usage = call_gemini(
        "Analyze: BTC/USDT $69500 RSI=25. Buy/Sell/Hold?", MCP_TOOLS)
    print(text)
    print(f"Tokens: {usage.get('promptTokenCount',0)}+{usage.get('candidatesTokenCount',0)}")
