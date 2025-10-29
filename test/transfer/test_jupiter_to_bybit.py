"""Test jupiter_to_bybit functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.transfer.jupiter_to_bybit import (
    get_bybit_deposit_address,
    transfer_to_bybit
)


def test_get_bybit_deposit_address():
    """Get Bybit deposit address for SOL"""
    address = get_bybit_deposit_address("SOL")
    print(f"Bybit SOL deposit address: {address}")


def test_transfer_to_bybit():
    """Transfer SOL to Bybit (commented - real transfer)"""
    # Uncomment to execute real transfer:
    # tx = transfer_to_bybit("SOL", 0.1)
    # print(f"Transfer TX: {tx}")
    print("Test transfer_to_bybit - uncomment to run real transfer")


if __name__ == "__main__":
    test_get_bybit_deposit_address()
    test_transfer_to_bybit()

