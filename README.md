# Simplified Trading Bot — Binance Futures Testnet (USDT-M)

A simple, structured Python CLI application to place MARKET and LIMIT orders
on Binance Futures Testnet (USDT-M), with input validation, logging, and
error handling.

## Features

- Place **MARKET** and **LIMIT** orders
- Support for both **BUY** and **SELL** sides
- CLI input via `argparse` (symbol, side, order type, quantity, price)
- Clean output: order request summary, response details, success/failure message
- Structured codebase: separate client (API) layer, order logic layer, and CLI layer
- Logging of every API request, response, and error to a timestamped log file
- Robust exception handling for invalid input, API errors, and network failures

## Project Structure

## Setup

### 1. Prerequisites
- Python 3.9+
- A Binance Futures Testnet account: https://testnet.binancefuture.com
  (or the Demo Trading environment at https://demo.binance.com)

### 2. Get API credentials
1. Log in to the Futures Testnet / Demo Trading site.
2. Go to **API Management** (or "Demo Trading API" in the account menu).
3. Generate a **System generated (HMAC)** API key and secret.
4. Copy both immediately — the secret is shown only once.

### 3. Clone and install

```bash
git clone <your-repo-url>
cd trading_bot

python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux

pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:
**Never commit `.env` to version control** — it is already excluded via `.gitignore`.

## How to Run

### Place a MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
```

### CLI Arguments

| Argument      | Required          | Description                              |
|---------------|--------------------|-------------------------------------------|
| `--symbol`    | Yes                | Trading pair, e.g. `BTCUSDT`             |
| `--side`      | Yes                | `BUY` or `SELL`                          |
| `--type`      | Yes                | `MARKET` or `LIMIT`                      |
| `--quantity`  | Yes                | Order quantity (must be > 0)             |
| `--price`     | Only for `LIMIT`   | Limit price (must be > 0)                |

### Example Output
--- Order Request Summary ---
Symbol   : BTCUSDT
Side     : BUY
Type     : MARKET
Quantity : 0.01
--- Order Response Details ---
Order ID     : 18744536169
Status       : NEW
Executed Qty : 0.0000
Avg Price    : None
Orig Qty     : 0.0100
 SUCCESS: Order placed successfully.

## Logging

Every run creates a new timestamped log file in `logs/`, e.g.
`logs/trading_bot_20260703_204521.log`. Each log file records:

- The exact request sent to Binance
- The raw response received
- Any validation, API, or network errors

Sample log files from a MARKET and a LIMIT order run are included in the
`logs/` folder as part of this submission.

## Error Handling

The bot handles the following failure cases gracefully (with clear CLI
messages and log entries, without crashing):

- Missing or invalid CLI input (e.g. missing price for a LIMIT order,
  negative quantity, invalid side/order type)
- Missing or invalid API credentials
- Binance API rejections (e.g. invalid symbol, insufficient balance)
- Network failures (timeouts, connectivity issues)

## Assumptions

- This bot only supports USDT-M perpetual futures pairs (symbols ending in `USDT`).
- LIMIT orders are placed with `timeInForce=GTC` (Good Till Cancelled).
- The bot targets Binance Futures Testnet only
  (`https://testnet.binancefuture.com`); it is not intended for live trading.
- Only MARKET and LIMIT order types are implemented in the core scope.

## Tech Stack

- Python 3
- [python-binance](https://github.com/sammchardy/python-binance)
- python-dotenv
- argparse (standard library)