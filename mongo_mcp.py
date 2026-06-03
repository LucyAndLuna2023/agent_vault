"""MongoDB MCP Server — reads URI from environment"""
from pymongo import MongoClient
import os
URI = os.environ.get("MONGODB_URI", "")
client = MongoClient(URI, serverSelectionTimeoutMS=5000) if URI else None
db = client.agent_vault if client else None
def store_signal(s, sig, p, r): 
    if db: db.signals.insert_one({"symbol":s,"signal":sig,"price":p,"rsi":r})
def query_signals(s=None, limit=10):
    return list(db.signals.find({"symbol":s} if s else {}).sort("_id",-1).limit(limit)) if db else []
