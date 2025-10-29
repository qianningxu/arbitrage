import json
import os


def bybit_symbol_to_solana_mints(symbol):
    """Convert Bybit symbol to Solana mint addresses"""
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../files")
    
    # Load all pairs
    with open(os.path.join(base_dir, "all_pairs.json"), encoding="utf-8") as f:
        pairs = json.load(f)
    
    # Find pair
    pair = None
    for item in pairs:
        if (item.get("symbol") or "").upper() == symbol.upper():
            base = (item.get("baseCoin") or "").upper()
            quote = (item.get("quoteCoin") or "").upper()
            pair = (base, quote) if base and quote else None
            break
    
    if not pair:
        return None
    
    # Load all mints
    with open(os.path.join(base_dir, "all_mints.json"), encoding="utf-8") as f:
        data = json.load(f)
    
    tokens = data if isinstance(data, dict) else {
        (t.get("symbol") or "").upper(): [t] 
        for t in data if t.get("symbol")
    }
    
    # Get mints
    base_candidates = tokens.get(pair[0], [])
    quote_candidates = tokens.get(pair[1], [])
    
    if len(base_candidates) != 1 or len(quote_candidates) != 1:
        return None
    
    base_mint = base_candidates[0].get("mint") or base_candidates[0].get("id")
    quote_mint = quote_candidates[0].get("mint") or quote_candidates[0].get("id")
    
    return (base_mint, quote_mint) if base_mint and quote_mint else None


if __name__ == "__main__":
    print(bybit_symbol_to_solana_mints("SOLUSDC"))
    print(bybit_symbol_to_solana_mints("TRUMPUSDT"))
    print(bybit_symbol_to_solana_mints("ETHBTC"))
    print(bybit_symbol_to_solana_mints("FOOUSDT"))
