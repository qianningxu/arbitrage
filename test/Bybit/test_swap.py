"""Test bybit_swap functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.Bybit.trading import swap


def test_usdt_to_sol():
    """Swap USDT to SOL"""
    print("Swapping 10 USDT -> SOL...")
    result = swap('USDT', 'SOL', 10, 'in')
    print(f"Order ID: {result['orderId']}")
    print(f"Done: {result}")


def test_sol_to_usdt():
    """Swap SOL to USDT"""
    print("Swapping 0.1 SOL -> USDT...")
    result = swap('SOL', 'USDT', 0.1, 'in')
    print(f"Order ID: {result['orderId']}")
    print(f"Done: {result}")


if __name__ == "__main__":
    test_usdt_to_sol()
    # test_sol_to_usdt()

