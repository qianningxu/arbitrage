"""Test Jupiter balance functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.jupiter.account.balance import check_balance


def test_check_balance(symbol):
    """Check balance for a specific token"""
    balance = check_balance(symbol)
    print(f"{symbol} balance: {balance}")


if __name__ == "__main__":
    test_check_balance("SOL")
    test_check_balance("USDT")

