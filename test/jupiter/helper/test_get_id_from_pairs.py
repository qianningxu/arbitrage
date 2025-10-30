"""Test get_id_from_pairs functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.shared.data import symbol_to_mint


def test_symbol_to_mint(symbol):
    """Get Solana mint address from symbol"""
    mint = symbol_to_mint(symbol)
    print(f"{symbol} mint: {mint}")


if __name__ == "__main__":
    test_symbol_to_mint("SOL")
    test_symbol_to_mint("USDT")

