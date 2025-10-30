"""Jupiter utility functions"""
from main.shared.data import get_token_info as _get_token_info

def get_token_info(symbol):
    """Get token info (wrapper for shared data function)"""
    return _get_token_info(symbol)

