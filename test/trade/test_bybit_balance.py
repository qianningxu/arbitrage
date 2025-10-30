"""Test bybit_balance functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.platforms.bybit.services.balance import get_fund_balance, get_unified_balance, get_all_fund_balances


def test_get_fund_balance():
    """Check SOL balance in FUND account"""
    balance = get_fund_balance("SOL")
    print(f"SOL FUND balance: {balance}")


def test_get_unified_balance():
    """Check SOL balance in UNIFIED account"""
    balance = get_unified_balance("SOL")
    print(f"SOL UNIFIED balance: {balance}")


def test_get_all_fund_balances():
    """Get all balances in FUND account"""
    balances = get_all_fund_balances()
    print("All FUND balances:")
    for coin, amount in balances.items():
        print(f"  {coin}: {amount}")


if __name__ == "__main__":
    test_get_fund_balance()
    test_get_unified_balance()
    test_get_all_fund_balances()

