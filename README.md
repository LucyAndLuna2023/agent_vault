# AgentVault — Multi-Agent Crypto Trading System

Google Cloud Agent Development Kit Hackathon Submission
Track: **MongoDB**

## Overview
AgentVault is a multi-agent system that manages crypto trading strategies using Gemini 3's reasoning and MongoDB's persistent memory. Three specialized agents collaborate: a Market Analyst, a Strategy Optimizer, and a Risk Monitor.

## Architecture
```
User → Orchestrator (Gemini 3)
         ├── Market Analyst Agent
         │     ├── Binance API (live prices)
         │     └── MongoDB MCP (historical data)
         ├── Strategy Agent  
         │     ├── RSI/MACD/Bollinger signals
         │     └── MongoDB MCP (backtest results)
         └── Risk Monitor Agent
               ├── Portfolio tracking
               └── MongoDB MCP (alert history)
```

## Tech Stack
- **Gemini 3** via Google Cloud Agent Builder (reasoning engine)
- **MongoDB MCP Server** (persistent agent memory)
- **Binance API** (real-time market data)
- **Python 3.12** (agent logic)
- Google Cloud Run (deployment)

## Quick Start
1. Set MongoDB connection string in `.env`
2. Set Gemini API key in `.env`
3. Run: `python3 orchestrator.py`
