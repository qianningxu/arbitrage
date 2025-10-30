"""Test jupiter_swap functions"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../main/trade'))

from main.Jupiter.trading import trade, crypto_to_u, u_to_crypto


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


def test_crypto_to_u():
    """Swap all SOL balance to USDT"""
    print("Swapping all SOL -> USDT...")
    tx = crypto_to_u("SOL")
    print(f"Done: {tx}")


def test_u_to_crypto():
    """Swap all USDT balance to SOL"""
    print("Swapping all USDT -> SOL...")
    tx = u_to_crypto("SOL")
    print(f"Done: {tx}")


if __name__ == "__main__":
    # test_usdt_to_sol()
    # test_sol_to_usdt()
    test_crypto_to_u()
    # test_u_to_crypto()

