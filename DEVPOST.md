# AgentVault — Multi-Agent Crypto Trading System

Track: **MongoDB**

## What it does
AgentVault uses Gemini 2.5 Flash to orchestrate three specialized AI agents — Market Analyst, Strategy Optimizer, and Risk Monitor — that collaborate to analyze crypto markets, generate trading signals, and manage risk. All agent state and trade history is persisted in MongoDB via MCP (Model Context Protocol), creating a persistent memory layer that survives across sessions.

## How I built it
- **Gemini 2.5 Flash** via Google AI API — reasoning engine for all agent decisions
- **MongoDB Atlas** via MCP Server — persistent storage for signals, market data, and risk alerts
- **Python 3.12** — core agent logic with Binance API integration
- **Google Cloud Agent Builder** ready architecture

## What's next
Deploy to Google Cloud Run with Agent Builder for production scaling. Add more MCP tools for portfolio tracking and automated execution.

## Built With
- gemini-2.5-flash
- mongodb
- python
- binance-api
- google-cloud
