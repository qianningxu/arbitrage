"""Test Bybit withdrawal function"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.bybit.account.transfers import withdraw


def test_withdraw(symbol):
    """Test withdrawing a token from Bybit to Jupiter"""
    try:
        result = withdraw(symbol)
        if result:
            print(f"\n✅ Withdrawal successful!")
            print(f"   Coin: {result['coin']}")
            print(f"   Amount: {result['amount']}")
            print(f"   Address: {result['address']}")
            print(f"   Balance: {result['balance']}")
            print(f"   Fee: {result['fee']}")
        else:
            print("\n❌ No funds to withdraw")
    except ValueError as e:
        print(f"\n⚠️  Withdrawal error: {str(e)}")
        if "not whitelisted" in str(e):
            print("💡 This is expected - please whitelist the address in Bybit first")


if __name__ == "__main__":
    test_withdraw('USDC')

