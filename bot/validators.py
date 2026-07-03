"""
Input validation for the trading bot CLI.
Raises ValidationError with a clear message on bad input.
"""

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP"}


class ValidationError(Exception):
    """Raised when user-supplied CLI input fails validation."""
    pass


def validate_symbol(symbol: str) -> str:
    if not symbol or not symbol.strip():
        raise ValidationError("Symbol cannot be empty (e.g., BTCUSDT).")

    symbol = symbol.strip().upper()

    if not symbol.isalnum():
        raise ValidationError(f"Invalid symbol '{symbol}'. Symbol must be alphanumeric (e.g., BTCUSDT).")

    if not symbol.endswith("USDT"):
        # Not a hard requirement on Binance, but this bot targets USDT-M futures
        raise ValidationError(f"Invalid symbol '{symbol}'. This bot only supports USDT-M pairs (e.g., BTCUSDT).")

    return symbol


def validate_side(side: str) -> str:
    if not side:
        raise ValidationError("Side cannot be empty. Must be BUY or SELL.")

    side = side.strip().upper()

    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be one of {VALID_SIDES}.")

    return side


def validate_order_type(order_type: str) -> str:
    if not order_type:
        raise ValidationError("Order type cannot be empty. Must be MARKET or LIMIT.")

    order_type = order_type.strip().upper()

    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be one of {VALID_ORDER_TYPES}.")

    return order_type


def validate_quantity(quantity: float) -> float:
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Quantity must be a number, got '{quantity}'.")

    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than 0, got {quantity}.")

    return quantity


def validate_price(price, order_type: str):
    """
    Price is required for LIMIT orders, must be None/absent for MARKET orders.
    """
    if order_type in ("LIMIT", "STOP"):
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValidationError(f"Price must be a number, got '{price}'.")
        if price <= 0:
            raise ValidationError(f"Price must be greater than 0, got {price}.")
        return price

    # MARKET order: price should not be used
    return None

def validate_stop_price(stop_price, order_type: str):
    """
    Stop price is required for STOP orders only.
    """
    if order_type == "STOP":
        if stop_price is None:
            raise ValidationError("Stop price is required for STOP orders.")
        try:
            stop_price = float(stop_price)
        except (TypeError, ValueError):
            raise ValidationError(f"Stop price must be a number, got '{stop_price}'.")
        if stop_price <= 0:
            raise ValidationError(f"Stop price must be greater than 0, got {stop_price}.")
        return stop_price

    return None


def validate_order_input(symbol: str, side: str, order_type: str, quantity, price=None, stop_price=None) -> dict:
    """
    Run all validations together and return a clean, normalized dict
    ready to be passed to the order layer.
    """
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_order_type = validate_order_type(order_type)
    clean_quantity = validate_quantity(quantity)
    clean_price = validate_price(price, clean_order_type)
    clean_stop_price = validate_stop_price(stop_price, clean_order_type)

    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "order_type": clean_order_type,
        "quantity": clean_quantity,
        "price": clean_price,
        "stop_price": clean_stop_price,
    }