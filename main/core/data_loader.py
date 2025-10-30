"""
Centralized data loading for tokens, pairs, and fees
Single source of truth for all data files
"""
import os
import json
from typing import Dict, List, Optional

# Cache for loaded data
_tokens_cache: Optional[Dict] = None
_pairs_cache: Optional[List] = None
_withdrawal_fees_cache: Optional[Dict] = None


def _get_data_path(filename: str) -> str:
    """Get absolute path to data file in files/ directory"""
    return os.path.join(os.path.dirname(__file__), "../../files", filename)


def load_tokens(force_reload: bool = False) -> Dict:
    """Load token metadata from unique_mint_by_symbol.json
    
    Args:
        force_reload: Force reload from disk even if cached
        
    Returns:
        dict: Token data keyed by symbol
    """
    global _tokens_cache
    
    if _tokens_cache is None or force_reload:
        path = _get_data_path("unique_mint_by_symbol.json")
        with open(path, encoding="utf-8") as f:
            _tokens_cache = json.load(f)
    
    return _tokens_cache


def load_pairs(force_reload: bool = False) -> List[Dict]:
    """Load trading pairs from all_pairs.json
    
    Args:
        force_reload: Force reload from disk even if cached
        
    Returns:
        list: List of trading pair dictionaries
    """
    global _pairs_cache
    
    if _pairs_cache is None or force_reload:
        path = _get_data_path("all_pairs.json")
        with open(path, encoding="utf-8") as f:
            _pairs_cache = json.load(f)
    
    return _pairs_cache


def load_withdrawal_fees(force_reload: bool = False) -> Dict:
    """Load withdrawal fees from withdrawal_fees.json
    
    Args:
        force_reload: Force reload from disk even if cached
        
    Returns:
        dict: Withdrawal fees keyed by coin symbol
    """
    global _withdrawal_fees_cache
    
    if _withdrawal_fees_cache is None or force_reload:
        path = _get_data_path("withdrawal_fees.json")
        with open(path, 'r', encoding="utf-8") as f:
            _withdrawal_fees_cache = json.load(f)
    
    return _withdrawal_fees_cache


def get_token_info(symbol: str) -> Optional[Dict]:
    """Get token information by symbol
    
    Args:
        symbol: Token symbol (e.g., 'SOL', 'USDT')
        
    Returns:
        dict or None: Token information or None if not found
    """
    tokens = load_tokens()
    token_list = tokens.get(symbol.upper(), [])
    return token_list[0] if token_list else None


def get_pair_info(symbol: str) -> Optional[Dict]:
    """Get trading pair information by symbol
    
    Args:
        symbol: Trading pair symbol (e.g., 'SOLUSDT')
        
    Returns:
        dict or None: Pair information or None if not found
    """
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


def get_withdrawal_fee(coin: str) -> Optional[float]:
    """Get withdrawal fee for a coin
    
    Args:
        coin: Coin symbol (e.g., 'SOL')
        
    Returns:
        float or None: Withdrawal fee or None if not found
    """
    fees = load_withdrawal_fees()
    coin_fee = fees.get(coin.upper())
    if coin_fee:
        return float(coin_fee.get("withdrawFee", 0))
    return None

