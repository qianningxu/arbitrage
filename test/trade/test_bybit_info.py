"""Test bybit_info functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.trade.bybit_info import get_pair_info


def test_get_pair_info():
    """Get trading pair info for SOLUSDT"""
    info = get_pair_info("SOLUSDT")
    print(f"SOLUSDT: {info['base']}/{info['quote']}, min qty: {info['minQty']}, precision: {info['precision']}")


if __name__ == "__main__":
    test_get_pair_info()

