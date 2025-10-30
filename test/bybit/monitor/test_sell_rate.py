"""Test get_sell_rate function"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.bybit.monitor.pricing import get_sell_rate

def test_get_sell_rate(symbol, amount):
    """Get average sell price"""
    rate = get_sell_rate(symbol, amount)
    print(f"Sell {amount} {symbol.replace('USDT', '')} at: ${rate:.2f}")

if __name__ == "__main__":
    test_get_sell_rate("SOLUSDT", 1)

