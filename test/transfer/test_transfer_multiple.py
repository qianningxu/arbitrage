"""Test batch transfer functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.transfer.transfer_multiple_to_bybit import transfer_multiple_to_bybit
from main.transfer.transfer_multiple_to_jupiter import transfer_multiple_to_jupiter


def test_transfer_multiple_to_bybit():
    """Test batch transfer from Jupiter to Bybit (commented - real transfer)"""
    # Uncomment to execute real transfers:
    
    # Example 1: Transfer specific cryptos
    # result = transfer_multiple_to_bybit(['SOL', 'USDT'])
    # print(f"\nResult: {result}")
    
    # Example 2: Transfer all available cryptos
    # result = transfer_multiple_to_bybit(None)
    # print(f"\nResult: {result}")
    
    # Example 3: Transfer single crypto
    # result = transfer_multiple_to_bybit('SOL')
    # print(f"\nResult: {result}")
    
    print("Test transfer_multiple_to_bybit - uncomment to run real transfers")


def test_transfer_multiple_to_jupiter():
    """Test batch transfer from Bybit to Jupiter (commented - real transfer)"""
    # Uncomment to execute real transfers:
    
    # Example 1: Transfer specific cryptos
    # result = transfer_multiple_to_jupiter(['SOL', 'USDT'])
    # print(f"\nResult: {result}")
    
    # Example 2: Transfer all available cryptos
    # result = transfer_multiple_to_jupiter(None)
    # print(f"\nResult: {result}")
    
    # Example 3: Transfer single crypto
    # result = transfer_multiple_to_jupiter('SOL')
    # print(f"\nResult: {result}")
    
    print("Test transfer_multiple_to_jupiter - uncomment to run real transfers")


def test_transfer_all_cryptos_to_bybit():
    """Transfer ALL cryptos from Jupiter to Bybit (commented - real transfer)"""
    # Uncomment to execute real transfer:
    # result = transfer_multiple_to_bybit(None)
    # print(f"\nResult: {result}")
    # print(f"Successful: {result['successful']}/{result['total']}")
    print("Test transfer ALL cryptos to Bybit - uncomment to run real transfer")


def test_transfer_all_cryptos_to_jupiter():
    """Transfer ALL cryptos from Bybit to Jupiter (commented - real transfer)"""
    # Uncomment to execute real transfer:
    # result = transfer_multiple_to_jupiter(None)
    # print(f"\nResult: {result}")
    # print(f"Transfers: {result['successful_transfers']}")
    # print(f"Withdrawals: {result['successful_withdrawals']}")
    print("Test transfer ALL cryptos to Jupiter - uncomment to run real transfer")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("BATCH TRANSFER TESTS")
    print("="*60 + "\n")
    
    print("Test 1: Transfer multiple specific cryptos to Bybit")
    test_transfer_multiple_to_bybit()
    print()
    
    print("Test 2: Transfer multiple specific cryptos to Jupiter")
    test_transfer_multiple_to_jupiter()
    print()
    
    print("Test 3: Transfer ALL cryptos to Bybit")
    test_transfer_all_cryptos_to_bybit()
    print()
    
    print("Test 4: Transfer ALL cryptos to Jupiter")
    test_transfer_all_cryptos_to_jupiter()
    print()

