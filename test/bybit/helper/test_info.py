"""Test bybit_info functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.shared.data import get_pair_info


def test_get_pair_info(symbol):
    """Get trading pair info"""
    info = get_pair_info(symbol)
    print(f"{symbol}: {info['base']}/{info['quote']}, min qty: {info['minQty']}, precision: {info['precision']}")


if __name__ == "__main__":
    test_get_pair_info("SOLUSDT")

