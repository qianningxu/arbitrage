"""
Bybit market data API
"""
import requests
from main.core.config import BYBIT_API_BASE


def get_orderbook(symbol: str, depth: int = 100) -> dict:
    """Get orderbook from Bybit
    
    Args:
        symbol: Trading pair symbol (e.g., 'SOLUSDT')
        depth: Orderbook depth (max 200 for spot, 1000 for some pairs)
        
    Returns:
        dict: Orderbook data with bids and asks
    """
    response = requests.get(f"{BYBIT_API_BASE}/v5/market/orderbook", params={
        "category": "spot",
        "symbol": symbol,
        "limit": depth
    })
    result = response.json()["result"]
    return {
        "bids": [(float(p), float(sz)) for p, sz in result["b"]],
        "asks": [(float(p), float(sz)) for p, sz in result["a"]]
    }


def get_ticker(symbol: str) -> dict:
    """Get ticker (best bid/ask) from Bybit
    
    Args:
        symbol: Trading pair symbol
        
    Returns:
        dict: Ticker data with best bid/ask
    """
    response = requests.get(f"{BYBIT_API_BASE}/v5/market/tickers", params={
        "category": "spot",
        "symbol": symbol
    })
    result = response.json()["result"]["list"][0]
    return {
        "symbol": result["symbol"],
        "bid": float(result["bid1Price"]),
        "ask": float(result["ask1Price"]),
        "last": float(result["lastPrice"])
    }

