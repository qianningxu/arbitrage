"""Test get_id_from_pairs functions"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.get_price.get_id_from_pairs import bybit_symbol_to_solana_mints


def test_bybit_symbol_to_solana_mints():
    """Convert SOLUSDT Bybit symbol to Solana mints"""
    mints = bybit_symbol_to_solana_mints("SOLUSDT")
    print(f"SOLUSDT mints: {mints}")


if __name__ == "__main__":
    test_bybit_symbol_to_solana_mints()

