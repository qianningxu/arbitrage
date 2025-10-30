"""Test bybit_to_jupiter - Withdrawal examples"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.Jupiter.client import get_address as get_solana_wallet_address
from main.workflows.transfers.bridge import transfer_to_solana as withdraw_from_bybit
from main.workflows.arbitrage.consolidate_funds import consolidate_to_solana as transfer_all_to_jupiter


def test_get_solana_address():
    """Get Solana wallet address"""
    address = get_solana_wallet_address()
    print(f"Solana wallet address: {address}")


def test_simple_sol_withdrawal():
    """Simple example: Withdraw 0.03 SOL from Bybit to Jupiter (commented - real transfer)"""
    # Uncomment to execute real withdrawal:
    # try:
    #     result = withdraw_from_bybit("SOL", 0.03)
    #     print(f"✅ Withdrawal ID: {result['withdrawal_id']}")
    #     return result
    # except Exception as e:
    #     print(f"❌ Failed: {e}")
    #     return None
    print("Test simple_sol_withdrawal - uncomment to run real withdrawal")


def test_transfer_all_to_jupiter():
    """Transfer ALL cryptos from Bybit to Jupiter (commented - real transfer)"""
    # Uncomment to execute real transfer:
    # result = transfer_all_to_jupiter()
    # print(f"✅ Transferred: {result['successful']}/{result['total']}")
    # for r in result['results']:
    #     if r['success']:
    #         print(f"  ✅ {r['coin']}: {r['amount']}")
    #     else:
    #         print(f"  ❌ {r['coin']}: {r['error']}")
    print("Test transfer_all_to_jupiter - uncomment to run real transfer of ALL cryptos")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("BYBIT TO JUPITER TESTS")
    print("="*60 + "\n")
    
    print("Test 1: Get Solana address")
    test_get_solana_address()
    print()
    
    print("Test 2: Simple SOL withdrawal")
    test_simple_sol_withdrawal()
    print()
    
    print("Test 3: Transfer ALL cryptos")
    test_transfer_all_to_jupiter()
    print()
