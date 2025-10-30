"""Check minimum order requirements for Bybit trading pairs"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

def get_min_order_info(symbol):
    """Get minimum order requirements for a trading pair"""
    pairs_file = Path(__file__).parent.parent.parent.parent / "files" / "all_pairs.json"
    with open(pairs_file, encoding="utf-8") as f:
        pairs = json.load(f)
    
    for pair in pairs:
        if pair["symbol"] == symbol.upper():
            lot_size = pair["lotSizeFilter"]
            return {
                "symbol": pair["symbol"],
                "base": pair["baseCoin"],
                "quote": pair["quoteCoin"],
                "minOrderQty": float(lot_size["minOrderQty"]),
                "minOrderAmt": float(lot_size["minOrderAmt"]),
                "maxOrderAmt": float(lot_size["maxOrderAmt"]),
                "basePrecision": float(lot_size["basePrecision"]),
                "quotePrecision": float(lot_size["quotePrecision"]),
            }
    return None

def display_min_order_info(symbol):
    """Display minimum order requirements"""
    info = get_min_order_info(symbol)
    if not info:
        print(f"❌ Trading pair {symbol} not found")
        return
    
    print(f"\n📊 Minimum Order Requirements for {info['symbol']}")
    print(f"{'='*60}")
    print(f"Base Coin:              {info['base']}")
    print(f"Quote Coin:             {info['quote']}")
    print(f"Min Order Quantity:     {info['minOrderQty']} {info['base']}")
    print(f"Min Order Amount:       {info['minOrderAmt']} {info['quote']}")
    print(f"Max Order Amount:       {info['maxOrderAmt']} {info['quote']}")
    print(f"Base Precision:         {info['basePrecision']}")
    print(f"Quote Precision:        {info['quotePrecision']}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # Check common pairs
    pairs = ["SOLUSDT", "BTCUSDT", "ETHUSDT", "BNBUSDT"]
    
    for pair in pairs:
        display_min_order_info(pair)

