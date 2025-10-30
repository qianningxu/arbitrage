"""Test get_jupiter_price functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.jupiter.monitor.pricing import get_exchange_rate, get_price_from_bybit_symbol as get_jupiter_price_from_bybit_symbol


def test_get_exchange_rate(from_symbol, to_symbol, amount):
    """Get exchange rate"""
    rate = get_exchange_rate(from_symbol, to_symbol, amount)
    print(f"Exchange rate {from_symbol}->{to_symbol}: {rate}")


def test_get_jupiter_price_from_bybit_symbol(symbol, amount=10):
    """Get Jupiter price using Bybit symbol"""
    rate = get_jupiter_price_from_bybit_symbol(symbol, amount)
    print(f"{symbol} on Jupiter (amount={amount}): {rate}")


if __name__ == "__main__":
    # test_get_exchange_rate("SOL", "USDT", 0.1)
    test_get_jupiter_price_from_bybit_symbol("SOLUSDT")

