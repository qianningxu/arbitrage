import json


def bybit_symbol_to_solana_mints(symbol):
    raw = symbol.upper()

    def load_local_mints():
        path = "/Users/side/Desktop/arbitrage/files/all_mints.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        # Convert list to dict
        result = {}
        for t in data:
            sym = (t.get("symbol") or "").upper()
            if sym:
                result.setdefault(sym, []).append(t)
        return result

    def get_base_quote_from_local(sym):
        path = "/Users/side/Desktop/arbitrage/files/all_pairs.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if (item.get("symbol") or "").upper() == sym:
                base = (item.get("baseCoin") or "").upper()
                quote = (item.get("quoteCoin") or "").upper()
                return (base, quote) if base and quote else None
        return None

    def pick_mint_for_symbol(symbol_upper, tokens_by_symbol):
        candidates = tokens_by_symbol.get(symbol_upper, [])
        
        if not candidates:
            return None
        if len(candidates) > 1:
            return None
        return candidates[0].get("mint") or candidates[0].get("id")

    pair = get_base_quote_from_local(raw)
    if not pair:
        return None
    base, quote = pair

    tokens_by_symbol = load_local_mints()

    base_mint = pick_mint_for_symbol(base, tokens_by_symbol)
    quote_mint = pick_mint_for_symbol(quote, tokens_by_symbol)

    if not base_mint or not quote_mint:
        return None

    return base_mint, quote_mint


if __name__ == "__main__":
    print(bybit_symbol_to_solana_mints("SOLUSDC"))
    print(bybit_symbol_to_solana_mints("TRUMPUSDT"))
    print(bybit_symbol_to_solana_mints("ETHBTC"))
    print(bybit_symbol_to_solana_mints("FOOUSDT"))
