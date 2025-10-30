"""Token, pair, and fee data loading - single source of truth"""
import os
import json

_tokens_cache = None
_pairs_cache = None
_withdrawal_fees_cache = None

def _get_data_path(filename):
    """Get absolute path to data file in files/ directory"""
    return os.path.join(os.path.dirname(__file__), "../../files", filename)

def load_tokens(force_reload=False):
    """Load token metadata from unique_mint_by_symbol.json"""
    global _tokens_cache
    if _tokens_cache is None or force_reload:
        path = _get_data_path("unique_mint_by_symbol.json")
        with open(path, encoding="utf-8") as f:
            _tokens_cache = json.load(f)
    return _tokens_cache

def load_pairs(force_reload=False):
    """Load trading pairs from all_pairs.json"""
    global _pairs_cache
    if _pairs_cache is None or force_reload:
        path = _get_data_path("all_pairs.json")
        with open(path, encoding="utf-8") as f:
            _pairs_cache = json.load(f)
    return _pairs_cache

def load_withdrawal_fees(force_reload=False):
    """Load withdrawal fees from withdrawal_fees.json"""
    global _withdrawal_fees_cache
    if _withdrawal_fees_cache is None or force_reload:
        path = _get_data_path("withdrawal_fees.json")
        with open(path, 'r', encoding="utf-8") as f:
            _withdrawal_fees_cache = json.load(f)
    return _withdrawal_fees_cache

def get_token_info(symbol):
    """Get token information by symbol"""
    tokens = load_tokens()
    token_list = tokens.get(symbol.upper(), [])
    return token_list[0] if token_list else None

def get_pair_info(symbol):
    """Get trading pair information by symbol"""
    pairs = load_pairs()
    for pair in pairs:
        if pair["symbol"] == symbol.upper():
            return {
                "base": pair["baseCoin"],
                "quote": pair["quoteCoin"],
                "minQty": float(pair["lotSizeFilter"]["minOrderQty"]),
                "precision": float(pair["lotSizeFilter"]["basePrecision"])
            }
    return None

def get_withdrawal_fee(coin):
    """Get withdrawal fee for a coin"""
    fees = load_withdrawal_fees()
    coin_fee = fees.get(coin.upper())
    if coin_fee:
        return float(coin_fee.get("withdrawFee", 0))
    return None

def symbol_to_mint(symbol):
    """Convert token symbol to Solana mint address"""
    token_info = get_token_info(symbol)
    return token_info.get("mint") if token_info else None

def mint_to_symbol(mint):
    """Convert Solana mint address to token symbol"""
    tokens = load_tokens()
    for symbol, token_list in tokens.items():
        if token_list and token_list[0].get("mint") == mint:
            return symbol
    return None

def bybit_symbol_to_mints(symbol):
    """Convert Bybit trading pair symbol to Solana mint addresses"""
    pairs = load_pairs()
    pair = None
    for item in pairs:
        if (item.get("symbol") or "").upper() == symbol.upper():
            base = (item.get("baseCoin") or "").upper()
            quote = (item.get("quoteCoin") or "").upper()
            pair = (base, quote) if base and quote else None
            break
    if not pair:
        return None
    tokens = load_tokens()
    base_candidates = tokens.get(pair[0], [])
    quote_candidates = tokens.get(pair[1], [])
    if len(base_candidates) != 1 or len(quote_candidates) != 1:
        return None
    base_mint = base_candidates[0].get("mint") or base_candidates[0].get("id")
    quote_mint = quote_candidates[0].get("mint") or quote_candidates[0].get("id")
    return (base_mint, quote_mint) if base_mint and quote_mint else None

