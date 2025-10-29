"""Test jupiter_swap functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.trade.jupiter_swap import swap, trade


def test_swap():
    """Test swap with quote (commented - requires real quote)"""
    # Uncomment to test with a real quote:
    # quote = {...}  # Get quote first
    # tx = swap(quote)
    # print(f"Swap TX: {tx}")
    print("Test swap - uncomment to run real swap")


def test_trade():
    """Trade SOL to USDT (commented - real transaction)"""
    # Uncomment to execute real trade:
    # tx = trade("SOL", "USDT", 0.001)
    # print(f"Trade TX: {tx}")
    print("Test trade - uncomment to run: trade('SOL', 'USDT', 0.001)")


if __name__ == "__main__":
    test_swap()
    test_trade()

