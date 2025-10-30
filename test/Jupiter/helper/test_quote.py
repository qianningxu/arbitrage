"""Test jupiter_helpers functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main.Jupiter.pricing import get_quote as get_jupiter_quote


def test_get_jupiter_quote(from_mint, to_mint, amount):
    """Get Jupiter quote for swap"""
    quote = get_jupiter_quote(from_mint, to_mint, amount)
    if quote:
        print(f"Quote output amount: {quote.get('outAmount')}")
    else:
        print("Failed to get quote")


if __name__ == "__main__":
    sol_mint = "So11111111111111111111111111111111111111112"
    usdt_mint = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    test_get_jupiter_quote(sol_mint, usdt_mint, 100000000)  # 0.1 SOL

