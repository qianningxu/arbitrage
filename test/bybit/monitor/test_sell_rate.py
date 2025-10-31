"""Test get_sell_rate function"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.bybit.monitor.pricing import get_sell_rate

def test_get_sell_rate(base_coin, amount):
    """Get average sell price"""
    result = get_sell_rate(base_coin, amount)
    print(f"Sell {amount} {base_coin} at: ${result['rate']:.2f}")
    print(f"Estimated sell slippage: {result['slippage']*100:.2f}%")

if __name__ == "__main__":
    test_get_sell_rate("SOL", 1)

