"""Test jupiter_swap functions"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../main/trade'))

from main.trade.jupiter_swap import trade


def test_usdt_to_sol():
    """Swap 2 USDT to SOL"""
    print("Swapping 2 USDT -> SOL...")
    tx = trade("USDT", "SOL", 2)
    print(f"Done: {tx}")


def test_sol_to_usdt():
    """Swap 0.0001 SOL to USDT"""
    print("Swapping 0.0001 SOL -> USDT...")
    tx = trade("SOL", "USDT", 0.0001)
    print(f"Done: {tx}")


if __name__ == "__main__":
    # test_usdt_to_sol()
    test_sol_to_usdt()

