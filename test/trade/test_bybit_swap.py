"""Test bybit_swap functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.trade.bybit_swap import swap


def test_swap():
    """Swap 10 USDT for SOL (commented out - only run when ready)"""
    # Uncomment to execute real trade:
    # result = swap('USDT', 'SOL', 10, 'in')
    # print(f"Order ID: {result['orderId']}")
    
    print("Test swap function - uncomment to run real trade")
    print("Example: swap('USDT', 'SOL', 10, 'in')")


if __name__ == "__main__":
    test_swap()

