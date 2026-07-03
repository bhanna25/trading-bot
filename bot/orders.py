"""
Order placement logic — ties together validation and the Binance client.
"""

import logging
from bot.validators import validate_order_input, ValidationError
from bot.client import BinanceFuturesTestnetClient, BinanceClientError

logger = logging.getLogger("trading_bot")


class OrderError(Exception):
    """Raised when an order cannot be placed, wraps validation/client errors."""
    pass


def place_order(client: BinanceFuturesTestnetClient, symbol: str, side: str,
                 order_type: str, quantity, price=None, stop_price=None) -> dict:
    """
    Validate input, place the order via the client, and return a clean summary.

    Returns a dict with:
        - request: the normalized request that was sent
        - response: the raw Binance response
        - summary: key fields extracted for display (orderId, status, etc.)
    """
    # Step 1: Validate input
    try:
        clean_input = validate_order_input(symbol, side, order_type, quantity, price, stop_price)
    except ValidationError as exc:
        logger.error(f"Validation failed: {exc}")
        raise OrderError(f"Invalid input: {exc}")

    logger.info(f"Validated order request: {clean_input}")

    # Step 2: Place the order
    try:
        response = client.place_order(
            symbol=clean_input["symbol"],
            side=clean_input["side"],
            order_type=clean_input["order_type"],
            quantity=clean_input["quantity"],
            price=clean_input["price"],
            stop_price=clean_input["stop_price"],
        )
    except BinanceClientError as exc:
        logger.error(f"Order placement failed: {exc}")
        raise OrderError(str(exc))

    # Step 3: Build a clean summary for display
    summary = {
        "orderId": response.get("orderId") or response.get("algoId"),
        "symbol": response.get("symbol"),
        "status": response.get("status") or response.get("algoStatus"),
        "side": response.get("side"),
        "type": response.get("type") or response.get("orderType"),
        "executedQty": response.get("executedQty", "0.0000"),
        "avgPrice": response.get("avgPrice"),
        "origQty": response.get("origQty") or response.get("quantity"),
        "price": response.get("price"),
    }

    return {
        "request": clean_input,
        "response": response,
        "summary": summary,
    }