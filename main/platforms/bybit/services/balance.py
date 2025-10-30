"""
Bybit balance management services
"""
from ..api.account import get_balance, get_all_balances


def get_fund_balance(coin: str) -> float:
    """Get balance in FUND account
    
    Args:
        coin: Coin symbol
        
    Returns:
        float: Balance amount
    """
    return get_balance(coin, "FUND")


def get_unified_balance(coin: str) -> float:
    """Get balance in UNIFIED account
    
    Args:
        coin: Coin symbol
        
    Returns:
        float: Balance amount
    """
    return get_balance(coin, "UNIFIED")


def get_all_fund_balances() -> dict:
    """Get all balances in FUND account
    
    Returns:
        dict: Balances keyed by coin symbol
    """
    return get_all_balances("FUND")


def get_all_unified_balances() -> dict:
    """Get all balances in UNIFIED account
    
    Returns:
        dict: Balances keyed by coin symbol
    """
    return get_all_balances("UNIFIED")


def get_total_balance(coin: str) -> float:
    """Get total balance across all accounts
    
    Args:
        coin: Coin symbol
        
    Returns:
        float: Total balance
    """
    return get_fund_balance(coin) + get_unified_balance(coin)

