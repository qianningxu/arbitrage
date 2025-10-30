"""Bybit utility functions"""
from main.shared.data import get_pair_info as _get_pair_info

def get_pair_info(symbol: str):
    """Get trading pair info (wrapper for shared data function)"""
    return _get_pair_info(symbol)

