"""Test get_orderbook function"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.bybit.monitor.pricing import get_orderbook

def test_get_orderbook(base_coin, depth=20):
    """Get orderbook for trading pair"""
    book = get_orderbook(base_coin, depth=depth)
    print(f"Best bid: {book['bids'][0][0]}, Best ask: {book['asks'][0][0]}")
    print(f"Total bids: {len(book['bids'])}, Total asks: {len(book['asks'])}")

if __name__ == "__main__":
    test_get_orderbook("SOL")

