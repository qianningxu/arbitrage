"""Test Jupiter withdrawal function"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main.Jupiter.transfers import withdraw


def test_withdraw(symbol):
    """Test withdrawing a token from Jupiter to Bybit"""
    result = withdraw(symbol)
    print(f"Withdrawal result: {result}")
    if result:
        print(f"✅ Successfully withdrew {result['amount']} {result['coin']} to {result['address']}")
        print(f"Transaction: https://solscan.io/tx/{result['tx_sig']}")
    else:
        print("❌ No funds to withdraw")


if __name__ == "__main__":
    test_withdraw('usdc')

