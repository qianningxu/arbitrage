"""Test get_jupiter_price functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.jupiter.monitor.pricing import get_exchange_rate 


def test_get_exchange_rate(from_symbol, to_symbol, amount):
    """Get exchange rate"""
    rate = get_exchange_rate(from_symbol, to_symbol, amount)
    print(f"Exchange rate {from_symbol}->{to_symbol}: {rate}")
    return rate


if __name__ == "__main__":
    test_get_exchange_rate("ACS", "USDT", 0.1)

