"""Test jupiter_helpers functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.trade.jupiter_helpers import get_jupiter_quote, check_balance


def test_get_jupiter_quote():
    """Get Jupiter quote for SOL->USDT swap"""
    sol_mint = "So11111111111111111111111111111111111111112"
    usdt_mint = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    quote = get_jupiter_quote(sol_mint, usdt_mint, 100000000)  # 0.1 SOL
    if quote:
        print(f"Quote output amount: {quote.get('outAmount')}")
    else:
        print("Failed to get quote")


def test_check_balance():
    """Check SOL balance"""
    balance = check_balance("SOL")
    print(f"SOL balance: {balance}")


if __name__ == "__main__":
    test_get_jupiter_quote()
    test_check_balance()

