# Kairos - Cross-Chain Arbitrage Agent

**ETHGlobal Hackathon Submission**  
**Tracks:** Polygon, 1inch, Hedera

A sophisticated cross-chain arbitrage detection and execution agent that identifies profitable trading opportunities between Polygon and Hedera networks.

## 🎯 Project Overview

Kairos is an intelligent arbitrage agent that:
- 🔍 **Detects arbitrage opportunities** across multiple blockchains
- 🔄 **Executes cross-chain trades** automatically when profitable
- 📊 **Monitors live prices** from Polygon (via 1inch) and Hedera networks
- 💰 **Maximizes trading profits** through automated execution

## 🏗️ Architecture

### Smart Contracts
- **KairosVault.sol**: Deployed on Polygon Amoy testnet
- **Owner-controlled trade execution** with detailed logging
- **Gas-optimized** for frequent arbitrage transactions

### Python Agent
- **Multi-chain price fetching** (1inch API + Hedera Mirror Node)
- **Cross-chain arbitrage detection** with configurable thresholds
- **Automated trade execution** on profitable opportunities
- **Real-time monitoring** with comprehensive logging

## 🚀 Partner Track Integration

### Polygon Track ✅
- ✅ **Smart contract deployed** on Polygon Amoy testnet
- ✅ **1inch API integration** for real-time swap quotes
- ✅ **Live trade execution** with transaction confirmations
- ✅ **Gas optimization** for frequent trading

### 1inch Track ✅
- ✅ **1inch Swap API v5.2** integration
- ✅ **Real-time price quotes** for WETH/USDC pairs
- ✅ **Multi-token support** (WETH, USDC, POL)
- ✅ **Quote comparison** for arbitrage detection

### Hedera Track ✅
- ✅ **Hedera SDK integration** for real HBAR transfers
- ✅ **Hedera Mirror Node API** integration
- ✅ **Testnet account** setup and balance monitoring
- ✅ **Cross-chain price comparison** between Polygon and Hedera
- ✅ **Real transaction execution** on Hedera testnet

## 📋 Features

### Core Functionality
- **Real-time Price Monitoring**: Fetches live prices from both networks
- **Arbitrage Detection**: Identifies profitable cross-chain opportunities
- **Automated Execution**: Executes trades when profit thresholds are met
- **Risk Management**: Configurable profit thresholds and gas limits

### Cross-Chain Capabilities
- **Polygon Integration**: Real smart contract interaction with web3.py
- **Hedera Integration**: Real HBAR transfers using Hedera SDK
- **Price Synchronization**: Real-time comparison across networks
- **Automated Execution**: Smart trade routing to most profitable chain

## 🛠️ Technical Stack

- **Smart Contracts**: Solidity, Hardhat, OpenZeppelin
- **Backend**: Python, web3.py, requests, Hedera SDK
- **APIs**: 1inch Swap API, Hedera Mirror Node API
- **Networks**: Polygon Amoy, Hedera Testnet
- **Notifications**: Desktop notifications via plyer
- **Security**: Environment variables, private key management

## 📦 Installation & Setup

### Prerequisites
```bash
Node.js >= 16
Python >= 3.8
Java JDK >= 11 (required for Hedera SDK)
```

### Environment Setup
1. Clone the repository
2. Install dependencies:
```bash
npm install
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```env
# Polygon Configuration
AMOY_RPC_URL=your_polygon_amoy_rpc_url
PRIVATE_KEY=your_private_key
CONTRACT_ADDRESS=your_deployed_contract_address

# 1inch API
ONEINCH_API_KEY=your_1inch_api_key

# Hedera Configuration
HEDERA_ACCOUNT_ID=0.0.your_account_id
HEDERA_PRIVATE_KEY=your_hedera_private_key
```

### Deploy Smart Contract
```bash
npx hardhat run scripts/deploy.cjs --network amoy
```

### Run with Frontend Dashboard (Recommended)
```bash
# Quick start - runs both API server and frontend
start-dashboard.bat  # Windows

# Manual setup:
# Terminal 1 - API Server
python api_server.py

# Terminal 2 - Frontend (in ./frontend directory)
cd frontend
npm install
npm run dev
```

### Run Agent Only (Command Line)
```bash
# Activate virtual environment (if using venv)
venv/Scripts/activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run the agent
python kairos_agent.py

# Or run directly with venv path (without activation)
./venv/Scripts/python.exe kairos_agent.py  # Windows
./venv/bin/python kairos_agent.py          # Linux/Mac
```

## 🖥️ Frontend Dashboard

The Kairos dashboard provides a comprehensive interface for monitoring and controlling your arbitrage agent:

### Features:
- **🎮 Agent Control**: Start/stop the arbitrage agent with one click
- **⏱️ Live Timer**: Countdown to next execution cycle (5-minute intervals)
- **💰 Balance Monitoring**: Real-time Polygon and Hedera account balances
- **📊 Trade History**: Recent arbitrage trades with profit tracking
- **🔗 Transaction Links**: Direct links to PolygonScan and HashScan explorers
- **📝 Live Logs**: Real-time agent logs and status updates
- **🔔 Notifications**: Desktop alerts for successful trades and status changes

### Access:
- **Frontend Dashboard**: http://localhost:3000
- **API Server**: http://localhost:8000

## 💡 How It Works

### 1. Price Fetching
- **Polygon**: Uses 1inch API to get real-time swap quotes
- **Hedera**: Queries Mirror Node for token information and prices

### 2. Arbitrage Detection
```python
# Cross-chain profit comparison
polygon_rate = get_quote(WETH, USDC, amount)
hedera_balance = get_hedera_account_balance()
profit_opportunity = detect_cross_chain_arbitrage(polygon_rate, hedera_rate)
```

### 3. Trade Execution
- **Polygon trades**: Smart contract execution via web3.py
- **Hedera trades**: Real HBAR transfers via Hedera SDK
- **Transaction confirmations**: Full hash tracking and verification on both networks

## 📊 Sample Output

```
=== POLYGON PRICES (1inch) ===
INFO: 1 WETH -> USDC: {'toAmount': '3986172438'}
INFO: 4000 USDC -> WETH: {'toAmount': '996777754548471203'}

=== HEDERA NETWORK DATA ===
Hedera Account 0.0.6914928 HBAR balance: 1000.0

=== CROSS-CHAIN ARBITRAGE ANALYSIS ===
INFO: Polygon: Swap 1 WETH -> 3986.172438 USDC, then 4000 USDC -> 0.996778 WETH
INFO: Net WETH after Polygon round-trip: -0.003222
INFO: Hedera: Trade 10 HBAR, profit: 0.3
INFO: Best arbitrage: Hedera
INFO: Executing real Hedera trade: Transfer 10 HBAR
```

## 🏆 ETHGlobal Achievements

### Track Requirements Met
- ✅ **Polygon**: Smart contract deployment and real trade execution
- ✅ **1inch**: API integration and swap quote utilization  
- ✅ **Hedera**: SDK integration with real HBAR transfers

## 🔗 Contract Information

**Network**: Polygon Amoy Testnet  
**Contract Address**: `0x732bF24499402c33BFddfceA22f95F366cdf60A8`  
**Verification**: Verified on PolygonScan

## 🔍 Transaction Verification

### Polygon Transactions
- **Explorer**: [PolygonScan Amoy](https://amoy.polygonscan.com/)
- **Format**: `https://amoy.polygonscan.com/tx/{transaction_hash}`

### Hedera Transactions  
- **Explorer**: [HashScan Testnet](https://hashscan.io/testnet/)
- **Format**: `https://hashscan.io/testnet/transaction/{transaction_id}`


---

*This project demonstrates the future of cross-chain DeFi automation, combining the best of Polygon's scalability, 1inch's liquidity, and Hedera's innovative consensus mechanism.*
