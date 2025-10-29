"""Test bybit_swap functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.trade.bybit_swap import swap


def test_sol_to_usdt():
    """Swap 0.1 SOL to USDT"""
    print("Swapping 0.1 SOL -> USDT...")
    result = swap('SOL', 'USDT', 0.1, 'in')
    print(f"Order ID: {result['orderId']}")
    print(f"Done: {result}")


if __name__ == "__main__":
    # test_swap()
    test_sol_to_usdt()

