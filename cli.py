"""
CLI entry point for the trading bot.

Usage examples:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
"""

import argparse
import sys

from bot.logging_config import setup_logger
from bot.client import BinanceFuturesTestnetClient, BinanceClientError
from bot.orders import place_order, OrderError

logger = setup_logger()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simplified Trading Bot for Binance Futures Testnet (USDT-M)"
    )
    parser.add_argument("--symbol", required=True, help="Trading pair symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"],
                         help="Order side: BUY or SELL")
    parser.add_argument("--type", dest="order_type", required=True,
                         choices=["MARKET", "LIMIT", "market", "limit"],
                         help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", required=False, type=float, default=None,
                         help="Price (required for LIMIT orders)")

    return parser.parse_args()


def print_summary(result: dict):
    req = result["request"]
    summary = result["summary"]

    print("\n--- Order Request Summary ---")
    print(f"  Symbol   : {req['symbol']}")
    print(f"  Side     : {req['side']}")
    print(f"  Type     : {req['order_type']}")
    print(f"  Quantity : {req['quantity']}")
    if req["price"] is not None:
        print(f"  Price    : {req['price']}")

    print("\n--- Order Response Details ---")
    print(f"  Order ID     : {summary['orderId']}")
    print(f"  Status       : {summary['status']}")
    print(f"  Executed Qty : {summary['executedQty']}")
    print(f"  Avg Price    : {summary['avgPrice']}")
    print(f"  Orig Qty     : {summary['origQty']}")
    if summary["price"] not in (None, "0", "0.00000000"):
        print(f"  Order Price  : {summary['price']}")

    print("\n✅ SUCCESS: Order placed successfully.\n")


def main():
    args = parse_args()

    try:
        client = BinanceFuturesTestnetClient()
    except BinanceClientError as exc:
        logger.error(f"Client initialization failed: {exc}")
        print(f"\n❌ FAILURE: {exc}\n")
        sys.exit(1)

    try:
        result = place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        print_summary(result)

    except OrderError as exc:
        logger.error(f"Order failed: {exc}")
        print(f"\n❌ FAILURE: {exc}\n")
        sys.exit(1)

    except Exception as exc:
        # Catch-all for anything truly unexpected, so the CLI never crashes ugly
        logger.exception(f"Unexpected error: {exc}")
        print(f"\n❌ UNEXPECTED FAILURE: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()