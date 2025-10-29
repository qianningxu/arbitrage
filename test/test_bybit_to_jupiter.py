"""Test bybit_to_jupiter functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main.bybit_to_jupiter import (
    get_solana_wallet_address,
    check_bybit_balance,
    withdraw_from_bybit
)


def test_get_solana_wallet_address():
    """Get Solana wallet address from private key"""
    address = get_solana_wallet_address()
    print(f"Solana wallet address: {address}")


def test_check_bybit_balance():
    """Check Bybit FUND account balance"""
    balance = check_bybit_balance("SOL")
    print(f"Bybit SOL balance (FUND): {balance}")


def test_withdraw_from_bybit():
    """Withdraw from Bybit to Solana (commented - real withdrawal)"""
    # Uncomment to execute real withdrawal:
    # result = withdraw_from_bybit("SOL", 0.001)
    # print(f"Withdrawal ID: {result['withdrawal_id']}")
    print("Test withdraw_from_bybit - uncomment to run real withdrawal")


if __name__ == "__main__":
    test_get_solana_wallet_address()
    test_check_bybit_balance()
    test_withdraw_from_bybit()

