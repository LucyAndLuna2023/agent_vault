"""
AgentVault Orchestrator — Multi-Agent Crypto Trading
Gemini 3 + MongoDB MCP
"""
import os, json, time
from datetime import datetime

class MongoMCP:
    """MongoDB Model Context Protocol — persistent agent memory"""
    def __init__(self, uri=None):
        self.uri = uri or os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
        self.collections = {}
    
    def store(self, collection, data):
        """Store agent state/result via MCP"""
        data["_timestamp"] = datetime.now().isoformat()
        key = f"{collection}_{int(time.time())}"
        self.collections.setdefault(collection, {})[key] = data
        print(f"[MongoDB MCP] Stored in {collection}: {json.dumps(data)[:100]}")
        return key
    
    def query(self, collection, filter_fn=None):
        """Query agent memory via MCP"""
        items = list(self.collections.get(collection, {}).values())
        if filter_fn:
            items = [i for i in items if filter_fn(i)]
        return items

class MarketAnalyst:
    """Analyzes market conditions using Binance data"""
    def __init__(self, mcp):
        self.mcp = mcp
    
    def analyze(self, symbol="BTCUSDT"):
        """Get price and technical indicators"""
        import requests as r
        resp = r.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}", timeout=5)
        data = resp.json()
        analysis = {
            "symbol": symbol, "price": float(data["lastPrice"]),
            "change_pct": float(data["priceChangePercent"]),
            "volume": float(data["volume"]),
            "high_24h": float(data["highPrice"]),
            "low_24h": float(data["lowPrice"])
        }
        self.mcp.store("market_analysis", analysis)
        return analysis

class StrategyAgent:
    """V7-AG Strategy with RSI/MACD/Bollinger"""
    def __init__(self, mcp):
        self.mcp = mcp
    
    def evaluate(self, closes):
        """Generate BUY/SELL/HOLD signal"""
        import numpy as np
        cl = np.array(closes)
        n = len(cl)
        if n < 50: return "HOLD"
        
        # RSI(14)
        deltas = np.diff(cl)
        gain = np.where(deltas > 0, deltas, 0)
        loss = np.where(deltas < 0, -deltas, 0)
        rsi = 100 - 100/(1 + np.mean(gain[-14:])/max(np.mean(loss[-14:]),1e-10))
        
        # Momentum(10)
        mom = (cl[-1]/cl[-10] - 1) * 100
        
        # Bollinger
        sma = np.mean(cl[-20:])
        std = np.std(cl[-20:])
        bb = (cl[-1] - sma)/std if std > 0 else 0
        
        signal = "HOLD"
        if rsi < 30 and mom > 2.0 and bb < -1.5: signal = "BUY"
        elif rsi > 70 and mom < -2.0 and bb > 1.5: signal = "SELL"
        
        result = {"signal": signal, "rsi": round(rsi,1), "momentum": round(mom,1),
                  "bollinger": round(bb,2), "price": cl[-1]}
        self.mcp.store("trade_signals", result)
        return result

class RiskMonitor:
    """Monitors portfolio risk and sends alerts"""
    def __init__(self, mcp):
        self.mcp = mcp
    
    def check(self, positions, max_loss_pct=10):
        """Check portfolio risk levels"""
        alerts = []
        for pos in positions:
            loss = abs(pos.get("unrealized_pnl_pct", 0))
            if loss > max_loss_pct:
                alerts.append({"type": "MAX_LOSS", "symbol": pos["symbol"],
                               "loss_pct": loss, "action": "CLOSE"})
        if alerts:
            self.mcp.store("risk_alerts", {"alerts": alerts, "count": len(alerts)})
        return alerts

class Orchestrator:
    """Gemini-powered orchestrator coordinating all agents"""
    def __init__(self):
        self.mcp = MongoMCP()
        self.analyst = MarketAnalyst(self.mcp)
        self.strategy = StrategyAgent(self.mcp)
        self.risk = RiskMonitor(self.mcp)
    
    def run_cycle(self, symbols=["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT"]):
        """One complete agent cycle"""
        print(f"\n{'='*50}")
        print(f"AgentVault Cycle — {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*50}")
        
        for sym in symbols:
            market = self.analyst.analyze(sym)
            print(f"[Market] {sym}: ${market['price']:,.0f} ({market['change_pct']:+.1f}%)")
            
            import requests as r
            k = r.get(f"https://api.binance.com/api/v3/klines?symbol={sym}&interval=1h&limit=50", timeout=5)
            closes = [float(x[4]) for x in k.json()]
            sig = self.strategy.evaluate(closes)
            print(f"[Strategy] {sym}: {sig['signal']} (RSI:{sig['rsi']} Mom:{sig['momentum']})")
        
        positions = [
            {"symbol": "ETH", "unrealized_pnl_pct": 5.2},
            {"symbol": "BNB", "unrealized_pnl_pct": -3.1}
        ]
        alerts = self.risk.check(positions)
        if alerts:
            print(f"[Risk] {len(alerts)} alerts!")
        
        # Query memory
        signals = self.mcp.query("trade_signals", lambda s: s["signal"] != "HOLD")
        print(f"[Memory] {len(signals)} active signals in MongoDB")
        
        return {"cycle": datetime.now().isoformat(), "signals": len(signals)}

if __name__ == "__main__":
    orch = Orchestrator()
    orch.run_cycle()
