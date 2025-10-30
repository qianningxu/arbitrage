"""Test get_buy_rate function"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.bybit.monitor.pricing import get_buy_rate

def test_get_buy_rate(symbol, amount):
    """Get average buy price"""
    rate = get_buy_rate(symbol, amount)
    print(f"Buy {amount} {symbol.replace('USDT', '')} at: ${rate:.2f}")

if __name__ == "__main__":
    test_get_buy_rate("SOLUSDT", 1)

