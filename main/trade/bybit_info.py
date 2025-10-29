import os
import json

# Cache for all pairs data
_all_pairs = None


def _load_pairs():
    """Load all pairs from JSON file (cached)"""
    global _all_pairs
    if _all_pairs is None:
        path = os.path.join(os.path.dirname(__file__), "../../files/all_pairs.json")
        with open(path, encoding="utf-8") as f:
            _all_pairs = json.load(f)
    return _all_pairs


def get_pair_info(symbol):
    """Get trading pair info from local JSON file"""
    pairs = _load_pairs()
    
    # Find the pair by symbol
    for pair in pairs:
        if pair["symbol"] == symbol.upper():
            return {
                "base": pair["baseCoin"],
                "quote": pair["quoteCoin"],
                "minQty": float(pair["lotSizeFilter"]["minOrderQty"]),
                "precision": float(pair["lotSizeFilter"]["basePrecision"])
            }
    
    return None

