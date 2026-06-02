"""MongoDB MCP Server for AgentVault"""
from pymongo import MongoClient

URI = "mongodb+srv://admin:Pass0Word1!@cluster0.zlkzidl.mongodb.net/?appName=Cluster0"
client = MongoClient(URI)
db = client.agent_vault

def store_signal(symbol, signal, price, rsi):
    """MCP: Store trading signal"""
    return db.signals.insert_one({
        "symbol": symbol, "signal": signal,
        "price": price, "rsi": rsi,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }).inserted_id

def query_signals(symbol=None, limit=10):
    """MCP: Query trade history"""
    filt = {"symbol": symbol} if symbol else {}
    return list(db.signals.find(filt).sort("_id", -1).limit(limit))

def store_market(symbol, price, change_pct, volume):
    """MCP: Store market snapshot"""
    return db.market.insert_one({
        "symbol": symbol, "price": price,
        "change_pct": change_pct, "volume": volume
    }).inserted_id

print("MongoDB MCP ready")
