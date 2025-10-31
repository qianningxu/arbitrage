"""Test estimate slippage functions"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from main.bybit.monitor.pricing import estimate_buy_slippage, estimate_sell_slippage

def test_estimate_buy_slippage(symbol, amount):
    """Estimate buy slippage"""
    slippage = estimate_buy_slippage(symbol, amount)
    print(f"Estimated slippage for buying {amount} {symbol.replace('USDT', '')}: {slippage*100:.2f}%")

def test_estimate_sell_slippage(symbol, amount):
    """Estimate sell slippage"""
    slippage = estimate_sell_slippage(symbol, amount)
    print(f"Estimated slippage for selling {amount} {symbol.replace('USDT', '')}: {slippage*100:.2f}%")

if __name__ == "__main__":
    test_estimate_buy_slippage("SOLUSDT", 1)
    test_estimate_sell_slippage("SOLUSDT", 1)

