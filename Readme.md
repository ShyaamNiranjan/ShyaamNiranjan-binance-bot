Binance Futures Trading Bot - Complete Documentation

Project Overview

A professional-grade trading bot for Binance Futures Testnet featuring comprehensive order management, advanced trading strategies, and robust error handling. This project fulfills all requirements plus bonus features for the hiring assessment.

Requirements Checklist:

Core Requirements
- Binance Futures Testnet integration (USDT-M)
- Market order placement (buy/sell)
- Limit order placement (buy/sell)
- Python implementation using python-binance library
- Command-line interface with user input validation
- Comprehensive logging (API requests, responses, errors)
- Error handling for all operations
- Clean, reusable code structure
- Clear input/output handling
- Order status tracking and display

Bonus Features Implemented
- Stop-Limit Orders: Advanced risk management with trigger and limit prices
- TWAP Strategy: Time-Weighted Average Price execution to minimize market impact
- Enhanced CLI: Professional menu-driven interface with formatted output
- Order Management: View open orders, cancel orders, check status
- Account Information: Balance checking and symbol information lookup

Project Structure

```
project_root/
│
├── src/
│   ├── bot.py                  # Main bot class with core functionality
│   ├── market_orders.py        # Market order handler
│   ├── limit_orders.py         # Limit order handler
│   ├── main.py                 # CLI application entry point
│   │
│   └── advanced/               # Bonus features
│       ├── stop_limit.py       # Stop-limit order implementation
│       └── twap.py             # TWAP strategy implementation
│
├── bot.log                     # Execution logs (auto-generated)
├── README.md                   # This file
├── requirements.txt            # Python dependencies
└── report.pdf                  # Analysis report (screenshots & explanations)
```

Quick Start Guide

1. Prerequisites

- Python 3.7+ installed
- pip package manager
- Binance Futures Testnet account

2. Binance Testnet Setup

Register Account
1. Visit: https://testnet.binancefuture.com
2. Click "Register" and create account
3. Verify your email

Generate API Keys
1. Log in to testnet
2. Navigate to API Management
3. Click "Create API" or "Generate HMAC_SHA256 Key"
4. IMPORTANT: Enable "Futures Trading" permission
5. Save API Key and Secret Key securely

Get Test Funds
1. Log in to testnet dashboard
2. Request test USDT from the faucet
3. Verify funds in your Futures account

3. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install python-binance==1.0.17
```

4. Run the Bot

```bash
cd src
python main.py
```

5. Enter Credentials

When prompted, enter your Binance Testnet API credentials:
```
API Key: your_testnet_api_key
API Secret: your_testnet_secret_key
```

Usage Guide

Menu Options

1. Market Order
- Purpose: Instant execution at current market price
- Inputs: Symbol, Side (BUY/SELL), Quantity
- Use Case: Immediate order execution
- Example: Buy 0.001 BTC at current price

2. Limit Order
- Purpose: Execute at specified price or better
- Inputs: Symbol, Side, Quantity, Price, Time-in-Force
- Use Case: Price-specific trading
- Example: Buy 0.001 BTC at $50,000

3. Stop-Limit Order (BONUS)
- Purpose: Risk management with trigger and execution prices
- Inputs: Symbol, Side, Quantity, Stop Price, Limit Price
- Use Case: Stop-loss or take-profit orders
- Example: Sell 0.001 BTC if price drops to $49,000 (stop), execute at $48,900 (limit)

4. TWAP Strategy (BONUS)
- Purpose: Split large orders over time to reduce market impact
- Inputs: Symbol, Side, Total Quantity, Duration (minutes), Number of Orders
- Use Case: Large order execution with minimal slippage
- Example: Buy 0.01 BTC over 10 minutes in 5 equal orders

5. Check Order Status
- Purpose: View current status of any order
- Inputs: Symbol, Order ID
- Output: Status, execution details, filled quantity

6. View Open Orders
- Purpose: List all pending orders
- Inputs: Symbol (optional - leave blank for all)
- Output: All open limit/stop orders

7. Cancel Order
- Purpose: Cancel pending orders
- Inputs: Symbol, Order ID
- Note: Only works for NEW/PENDING orders

8. View Account Balance
- Purpose: Check account funds
- Output: Total balance, available balance, unrealized P&L

9. View Symbol Info
- Purpose: Get trading pair information and current price
- Inputs: Symbol
- Output: Symbol details, price precision, current market price

10. Exit
- Safely closes the application

Technical Details

 Code Structure

#bot.py - Core Bot Class
```python
class BasicBot:
    - __init__(): Initialize with API credentials
    - _validate_connection(): Verify API connectivity
    - validate_order_params(): Parameter validation
    - get_order_status(): Check order status
    - cancel_order(): Cancel pending orders
    - get_account_balance(): Fetch account info
    - get_symbol_info(): Symbol information
    - get_current_price(): Current market price