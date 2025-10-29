import json
import os
from main.get_price.get_id_from_pairs import bybit_symbol_to_solana_mints
from main.trade.jupiter_helpers import get_jupiter_quote


def _load_tokens():
    """Load tokens from unique_mint_by_symbol.json"""
    path = os.path.join(os.path.dirname(__file__), "../../files/unique_mint_by_symbol.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_exchange_rate(input_symbol, output_symbol, amount):
    """Get Jupiter exchange rate for two symbols"""
    tokens = _load_tokens()
    
    input_data = tokens.get(input_symbol.upper(), [None])[0]
    output_data = tokens.get(output_symbol.upper(), [None])[0]
    
    if not input_data or not output_data:
        return None
    
    input_mint = input_data["mint"]
    output_mint = output_data["mint"]
    input_dec = input_data["decimals"]
    output_dec = output_data["decimals"]
    
    # Get quote
    amount_lamports = int(amount * (10 ** input_dec))
    quote = get_jupiter_quote(input_mint, output_mint, amount_lamports)
    
    if not quote:
        return None
    
    in_amt = quote.get("inAmount")
    out_amt = quote.get("outAmount")
    
    if not in_amt or not out_amt:
        return None
    
    # Calculate rate
    return (float(out_amt) / (10 ** output_dec)) / (float(in_amt) / (10 ** input_dec))


def get_jupiter_price_from_bybit_symbol(symbol):
    """Get Jupiter exchange rate using Bybit symbol"""
    result = bybit_symbol_to_solana_mints(symbol)
    if not result:
        return None
    
    base_mint, quote_mint = result
    tokens = _load_tokens()
    
    # Find symbols for mints
    input_symbol = None
    output_symbol = None
    
    for sym, data in tokens.items():
        if data and len(data) > 0:
            mint = data[0].get("mint")
            if mint == base_mint:
                input_symbol = sym
            if mint == quote_mint:
                output_symbol = sym
            if input_symbol and output_symbol:
                break
    
    if not input_symbol or not output_symbol:
        return None
    
    return get_exchange_rate(input_symbol, output_symbol, 1)



if __name__ == "__main__":
    symbols = ["ETHUSDT", "SOLUSDT", "USDCUSDT", "ETHUSDC"]
    
    for sym in symbols:
        rate = get_jupiter_price_from_bybit_symbol(sym)
        print(f"{sym}: {rate}")
    
    # Test direct
    print(f"\nDirect: SOL->USDT (0.1) = {get_exchange_rate('SOL', 'USDT', 0.1)}")
    print(f"\nDirect: SOL->USDT (0.1) = {get_exchange_rate('USDT','SOL', 0.1)}")

