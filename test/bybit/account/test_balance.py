"""Test bybit_balance functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.bybit.account.balance import get_balance


def test_get_fund_balance(symbol):
    """Check balance in FUND account"""
    balance = get_balance(symbol, "FUND")
    print(f"{symbol} FUND balance: {balance}")


def test_get_unified_balance(symbol):
    """Check balance in UNIFIED account"""
    balance = get_balance(symbol, "UNIFIED")
    print(f"{symbol} UNIFIED balance: {balance}")


if __name__ == "__main__":
    test_get_fund_balance("USDC")
    test_get_unified_balance("USDC")

