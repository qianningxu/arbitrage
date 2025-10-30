"""
Symbol and mint address conversion utilities
"""
from typing import Optional, Tuple
from .data_loader import load_tokens, load_pairs, get_token_info


def bybit_symbol_to_mints(symbol: str) -> Optional[Tuple[str, str]]:
    """Convert Bybit trading pair symbol to Solana mint addresses
    
    Args:
        symbol: Bybit trading pair symbol (e.g., 'SOLUSDT')
        
    Returns:
        tuple or None: (base_mint, quote_mint) or None if not found
    """
    pairs = load_pairs()
    
    # Find the pair
    pair = None
    for item in pairs:
        if (item.get("symbol") or "").upper() == symbol.upper():
            base = (item.get("baseCoin") or "").upper()
            quote = (item.get("quoteCoin") or "").upper()
            pair = (base, quote) if base and quote else None
            break
    
    if not pair:
        return None
    
    # Get mints
    tokens = load_tokens()
    base_candidates = tokens.get(pair[0], [])
    quote_candidates = tokens.get(pair[1], [])
    
    if len(base_candidates) != 1 or len(quote_candidates) != 1:
        return None
    
    base_mint = base_candidates[0].get("mint") or base_candidates[0].get("id")
    quote_mint = quote_candidates[0].get("mint") or quote_candidates[0].get("id")
    
    return (base_mint, quote_mint) if base_mint and quote_mint else None


def symbol_to_mint(symbol: str) -> Optional[str]:
    """Convert token symbol to Solana mint address
    
    Args:
        symbol: Token symbol (e.g., 'SOL', 'USDT')
        
    Returns:
        str or None: Mint address or None if not found
    """
    token_info = get_token_info(symbol)
    return token_info.get("mint") if token_info else None


def mint_to_symbol(mint: str) -> Optional[str]:
    """Convert Solana mint address to token symbol
    
    Args:
        mint: Mint address
        
    Returns:
        str or None: Token symbol or None if not found
    """
    tokens = load_tokens()
    for symbol, token_list in tokens.items():
        if token_list and token_list[0].get("mint") == mint:
            return symbol
    return None

