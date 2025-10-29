"""Test bybit_balance functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.trade.bybit_balance import get_balance, check_balance


def test_get_balance():
    """Check USDT balance"""
    balance = get_balance("USDT")
    print(f"USDT balance: {balance}")


def test_check_balance():
    """Check if you have 1 USDT"""
    try:
        check_balance("USDT", 1)
        print("✅ You have at least 1 USDT")
    except ValueError as e:
        print(f"❌ {e}")


if __name__ == "__main__":
    test_get_balance()
    test_check_balance()

