"""Test get_jupiter_price functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.Jupiter.pricing import get_exchange_rate, get_price_from_bybit_symbol as get_jupiter_price_from_bybit_symbol


def test_get_exchange_rate():
    """Get exchange rate from SOL to USDT"""
    rate = get_exchange_rate("SOL", "USDT", 0.1)
    print(f"Exchange rate SOL->USDT: {rate}")


def test_get_jupiter_price_from_bybit_symbol():
    """Get Jupiter price using Bybit symbol"""
    rate = get_jupiter_price_from_bybit_symbol("SOLUSDT")
    print(f"SOLUSDT on Jupiter: {rate}")


if __name__ == "__main__":
    test_get_exchange_rate()
    test_get_jupiter_price_from_bybit_symbol()

