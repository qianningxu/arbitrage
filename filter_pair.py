import json
import sys
import os

ROOT = "/Users/side/Desktop/arbitrage"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from main.get_id import bybit_symbol_to_solana_mints


def filter_valid_pairs():
    pairs_path = os.path.join(ROOT, "files/all_pairs.json")
    output_path = os.path.join(ROOT, "files/valid_pairs.json")
    
    with open(pairs_path, "r", encoding="utf-8") as f:
        all_pairs = json.load(f)
    
    valid_symbols = []
    total = len(all_pairs)
    
    for idx, pair in enumerate(all_pairs, 1):
        symbol = pair.get("symbol")
        if not symbol:
            continue
        
        result = bybit_symbol_to_solana_mints(symbol)
        if result is not None:
            valid_symbols.append(symbol)
            print(f"[{idx}/{total}] {symbol}: ✓")
        else:
            print(f"[{idx}/{total}] {symbol}: ✗")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(valid_symbols, f, indent=2)
    
    print(f"\nFound {len(valid_symbols)} valid pairs out of {total}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    filter_valid_pairs()

