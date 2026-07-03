"""
Binance Futures Testnet client wrapper.
Handles connection setup and raw order placement calls.
"""

import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from requests.exceptions import RequestException

load_dotenv()

logger = logging.getLogger("trading_bot")


class BinanceClientError(Exception):
    """Raised for any client-level failure (auth, network, API error)."""
    pass


class BinanceFuturesTestnetClient:
    """
    Thin wrapper around python-binance's Client, configured for
    USDT-M Futures Testnet.
    """

    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise BinanceClientError(
                "Missing BINANCE_API_KEY or BINANCE_API_SECRET. "
                "Please set them in your .env file."
            )

        try:
            self.client = Client(api_key, api_secret, testnet=True)
            # Explicitly point at Futures Testnet base URL
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
            logger.info("Binance Futures Testnet client initialized.")
        except Exception as exc:
            logger.error(f"Failed to initialize Binance client: {exc}")
            raise BinanceClientError(f"Failed to initialize Binance client: {exc}")

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        """
        Place a MARKET or LIMIT order on Futures Testnet.
        Returns the raw order response dict from Binance.
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good Till Cancelled

        logger.info(f"Sending order request: {params}")

        try:
            response = self.client.futures_create_order(**params)
            logger.info(f"Order response received: {response}")
            return response

        except BinanceOrderException as exc:
            logger.error(f"Order rejected by Binance: {exc}")
            raise BinanceClientError(f"Order rejected: {exc}")

        except BinanceAPIException as exc:
            logger.error(f"Binance API error: {exc}")
            raise BinanceClientError(f"Binance API error: {exc}")

        except RequestException as exc:
            logger.error(f"Network error while contacting Binance: {exc}")
            raise BinanceClientError(f"Network error: {exc}")

        except Exception as exc:
            logger.error(f"Unexpected error while placing order: {exc}")
            raise BinanceClientError(f"Unexpected error: {exc}")