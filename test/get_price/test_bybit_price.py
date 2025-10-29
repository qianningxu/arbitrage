"""Test get_bybit_price functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.get_price.get_bybit_price import get_orderbook, get_sell_rate, get_buy_rate


def test_get_orderbook():
    """Get orderbook for SOLUSDT"""
    book = get_orderbook("SOLUSDT", depth=10)
    print(f"Best bid: {book['bids'][0][0]}, Best ask: {book['asks'][0][0]}")


def test_get_sell_rate():
    """Get average sell price for 1 SOL"""
    rate = get_sell_rate("SOLUSDT", 1)
    print(f"Sell 1 SOL at: ${rate:.2f}")


def test_get_buy_rate():
    """Get average buy price for 1 SOL"""
    rate = get_buy_rate("SOLUSDT", 1)
    print(f"Buy 1 SOL at: ${rate:.2f}")


if __name__ == "__main__":
    test_get_orderbook()
    test_get_sell_rate()
    test_get_buy_rate()

