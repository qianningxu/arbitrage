"""Test jupiter_to_bybit functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main.Bybit.account.transfers import get_deposit_address as get_bybit_deposit_address
from main.workflows.transfers.bridge import transfer_to_bybit
from main.workflows.arbitrage.consolidate_funds import consolidate_to_bybit as transfer_all_to_bybit


def test_get_bybit_deposit_address(coin):
    """Get Bybit deposit address"""
    address = get_bybit_deposit_address(coin)
    print(f"Bybit {coin} deposit address: {address}")


def test_transfer_to_bybit(coin, amount):
    """Transfer crypto to Bybit (commented - real transfer)"""
    # Uncomment to execute real transfer:
    # tx = transfer_to_bybit(coin, amount)
    # print(f"Transfer TX: {tx}")
    print(f"Test transfer {amount} {coin} to Bybit - uncomment to run real transfer")


def test_transfer_all_to_bybit():
    """Transfer ALL cryptos from Jupiter to Bybit (commented - real transfer)"""
    # Uncomment to execute real transfer:
    # result = transfer_all_to_bybit()
    # print(f"✅ Transferred {result['successful']}/{result['total']} cryptos")
    # for r in result['results']:
    #     if r['success']:
    #         print(f"  ✅ {r['coin']}: {r['amount']}")
    #     else:
    #         print(f"  ❌ {r['coin']}: {r['error']}")
    print("Test transfer_all_to_bybit - uncomment to run real transfer of ALL cryptos")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("JUPITER TO BYBIT TESTS")
    print("="*60 + "\n")
    
    print("Test 1: Get deposit address")
    test_get_bybit_deposit_address("SOL")
    print()
    
    print("Test 2: Transfer single crypto")
    test_transfer_to_bybit("SOL", 0.1)
    print()
    
    print("Test 3: Transfer ALL cryptos")
    test_transfer_all_to_bybit()
    print()

