"""
Solana balance management services
"""
from main.core.data_loader import load_tokens
from ..api.wallet import get_sol_balance, get_token_balance


def check_balance(symbol: str) -> float:
    """Check balance for a token symbol
    
    Args:
        symbol: Token symbol (e.g., 'SOL', 'USDT')
        
    Returns:
        float: Token balance
    """
    return get_token_balance(symbol)


def get_all_balances() -> dict:
    """Get all token balances
    
    Returns:
        dict: Balances keyed by symbol
    """
    tokens = load_tokens()
    balances = {}
    
    for symbol in tokens.keys():
        try:
            balance = get_token_balance(symbol)
            if balance > 0:
                balances[symbol] = balance
        except:
            continue
    
    return balances

