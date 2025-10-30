"""Test get_bybit_price functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main.Bybit.pricing import get_orderbook, get_sell_rate, get_buy_rate


def test_get_orderbook(symbol, depth=10):
    """Get orderbook for trading pair"""
    book = get_orderbook(symbol, depth=depth)
    print(f"Best bid: {book['bids'][0][0]}, Best ask: {book['asks'][0][0]}")


def test_get_sell_rate(symbol, amount):
    """Get average sell price"""
    rate = get_sell_rate(symbol, amount)
    print(f"Sell {amount} {symbol.replace('USDT', '')} at: ${rate:.2f}")


def test_get_buy_rate(symbol, amount):
    """Get average buy price"""
    rate = get_buy_rate(symbol, amount)
    print(f"Buy {amount} {symbol.replace('USDT', '')} at: ${rate:.2f}")


if __name__ == "__main__":
    test_get_orderbook("SOLUSDT")
    test_get_sell_rate("SOLUSDT", 1)
    test_get_buy_rate("SOLUSDT", 1)

