"""Test Jupiter balance functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.Jupiter.balance import check_balance


def test_check_balance(symbol):
    """Check balance for a specific token"""
    balance = check_balance(symbol)
    print(f"{symbol} balance: {balance}")


if __name__ == "__main__":
    test_check_balance("SOL")
    test_check_balance("USDT")

