"""Test bybit_to_jupiter - Simple withdrawal example"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.transfer.bybit_to_jupiter import (
    get_solana_wallet_address,
    withdraw_from_bybit
)


def test_simple_sol_withdrawal():
    """Simple example: Withdraw 0.03 SOL from Bybit to Jupiter"""
    try:
        result = withdraw_from_bybit("SOL", 0.03)
        print(f"✅ Withdrawal ID: {result['withdrawal_id']}")
        return result
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None


if __name__ == "__main__":
    test_simple_sol_withdrawal()
