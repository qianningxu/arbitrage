"""Test jupiter_swap functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.Jupiter.account.swap import crypto_to_u, u_to_crypto


def test_crypto_to_u(symbol):
    """Swap all crypto balance to USDT"""
    print(f"Swapping all {symbol} -> USDT...")
    tx = crypto_to_u(symbol)
    print(f"Done: {tx}")


def test_u_to_crypto(symbol):
    """Swap all USDT balance to crypto"""
    print(f"Swapping all USDT -> {symbol}...")
    tx = u_to_crypto(symbol)
    print(f"Done: {tx}")


if __name__ == "__main__":
    # test_crypto_to_u("USDC")
    test_u_to_crypto("USDC")
    pass

