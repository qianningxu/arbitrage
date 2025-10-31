"""Token and fee data loading from jupiter_bybit_overlap.json - single source of truth"""
import os
import json

_overlap_cache = None

def _get_data_path(filename):
    """Get absolute path to data file in files/ directory"""
    return os.path.join(os.path.dirname(__file__), "../../files", filename)

def load_overlap_data(force_reload=False):
    """Load Jupiter-Bybit overlap data from jupiter_bybit_overlap.json"""
    global _overlap_cache
    if _overlap_cache is None or force_reload:
        path = _get_data_path("jupiter_bybit_overlap.json")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            # Convert list to dict for faster lookup
            _overlap_cache = {item["symbol"]: item for item in data}
    return _overlap_cache

def load_tokens(force_reload=False):
    """Load token metadata (compatible with old interface)"""
    overlap = load_overlap_data(force_reload)
    # Convert to old format: {symbol: [token_info]}
    tokens = {}
    for symbol, item in overlap.items():
        tokens[symbol] = [{
            "mint": item["contractAddress"],
            "name": item["name"],
            "decimals": item["decimals"]
        }]
    return tokens

def load_pairs(force_reload=False):
    """Load trading pairs - returns pairs that can be traded with USDT"""
    overlap = load_overlap_data(force_reload)
    # Generate pairs with USDT as quote coin
    pairs = []
    for symbol, item in overlap.items():
        if symbol not in ["USDT", "USDC"]:  # Exclude stablecoins as base
            pairs.append({
                "symbol": f"{symbol}USDT",
                "baseCoin": symbol,
                "quoteCoin": "USDT",
                "lotSizeFilter": {
                    "minOrderQty": "0.001",
                    "minOrderAmt": "1",
                    "maxOrderAmt": "1000000",
                    "basePrecision": str(item["decimals"]),
                    "quotePrecision": "6"
                }
            })
    return pairs

def load_withdrawal_fees(force_reload=False):
    """Load withdrawal fees from overlap data"""
    overlap = load_overlap_data(force_reload)
    fees = {}
    for symbol, item in overlap.items():
        bybit_info = item.get("bybit", {})
        fees[symbol] = {
            "coin": symbol,
            "chain": "SOL",
            "withdrawFee": bybit_info.get("withdrawFee", "0"),
            "minWithdrawAmount": bybit_info.get("withdrawMin", "0")
        }
    return fees

def get_token_info(symbol):
    """Get token information by symbol"""
    overlap = load_overlap_data()
    item = overlap.get(symbol.upper())
    if item:
        return {
            "mint": item["contractAddress"],
            "name": item["name"],
            "decimals": item["decimals"]
        }
    return None

def get_pair_info(symbol):
    """Get trading pair information by symbol (e.g. SOLUSDT)"""
    # Extract base coin from pair symbol
    if symbol.endswith("USDT"):
        base = symbol[:-4]
    elif symbol.endswith("USDC"):
        base = symbol[:-4]
    else:
        return None
    
    overlap = load_overlap_data()
    item = overlap.get(base.upper())
    if item:
        return {
            "base": base,
            "quote": "USDT" if symbol.endswith("USDT") else "USDC",
            "minQty": 0.001,
            "precision": item["decimals"]
        }
    return None

def get_withdrawal_fee(coin):
    """Get withdrawal fee for a coin on SOL network"""
    overlap = load_overlap_data()
    item = overlap.get(coin.upper())
    if item and "bybit" in item:
        try:
            return float(item["bybit"].get("withdrawFee", 0))
        except (ValueError, TypeError):
            return 0
    return None

def symbol_to_mint(symbol):
    """Convert token symbol to Solana mint address (contract address)"""
    overlap = load_overlap_data()
    item = overlap.get(symbol.upper())
    return item["contractAddress"] if item else None

def mint_to_symbol(mint):
    """Convert Solana mint address to token symbol"""
    overlap = load_overlap_data()
    for symbol, item in overlap.items():
        if item["contractAddress"] == mint:
            return symbol
    return None

def bybit_symbol_to_mints(symbol):
    """Convert Bybit trading pair symbol to Solana mint addresses
    Example: SOLUSDT -> (SOL_mint, USDT_mint)
    """
    # Extract base and quote from pair symbol
    if symbol.endswith("USDT"):
        base = symbol[:-4]
        quote = "USDT"
    elif symbol.endswith("USDC"):
        base = symbol[:-4]
        quote = "USDC"
    else:
        return None
    
    overlap = load_overlap_data()
    base_item = overlap.get(base.upper())
    quote_item = overlap.get(quote.upper())
    
    if base_item and quote_item:
        return (base_item["contractAddress"], quote_item["contractAddress"])
    return None

def get_all_tradeable_symbols():
    """Get list of all symbols that can be traded (excluding stablecoins)"""
    overlap = load_overlap_data()
    return [s for s in overlap.keys() if s not in ["USDT", "USDC"]]

def is_deposit_enabled(symbol):
    """Check if deposit is enabled for a symbol"""
    overlap = load_overlap_data()
    item = overlap.get(symbol.upper())
    if item and "bybit" in item:
        return item["bybit"].get("depositEnabled", False)
    return False

def is_withdraw_enabled(symbol):
    """Check if withdrawal is enabled for a symbol"""
    overlap = load_overlap_data()
    item = overlap.get(symbol.upper())
    if item and "bybit" in item:
        return item["bybit"].get("withdrawEnabled", False)
    return False
