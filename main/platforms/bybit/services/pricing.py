"""
Bybit pricing services
"""
from ..api.market import get_orderbook, get_ticker


def get_buy_rate(symbol: str, qty: float, depth: int = 100) -> float:
    """Calculate average buy rate (buying from asks)
    
    Args:
        symbol: Trading pair symbol
        qty: Quantity to buy
        depth: Orderbook depth
        
    Returns:
        float: Average buy rate (0 if insufficient liquidity)
    """
    asks = get_orderbook(symbol, depth)["asks"]
    asks.sort()  # Sort by price ascending
    
    remaining, cost = qty, 0
    for price, size in asks:
        if remaining <= 0:
            break
        take = min(remaining, size)
        cost += take * price
        remaining -= take
    
    return cost / (qty - remaining) if qty != remaining else 0


def get_sell_rate(symbol: str, qty: float, depth: int = 100) -> float:
    """Calculate average sell rate (selling into bids)
    
    Args:
        symbol: Trading pair symbol
        qty: Quantity to sell
        depth: Orderbook depth
        
    Returns:
        float: Average sell rate (0 if insufficient liquidity)
    """
    bids = get_orderbook(symbol, depth)["bids"]
    bids.sort(reverse=True)  # Sort by price descending
    
    remaining, proceeds = qty, 0
    for price, size in bids:
        if remaining <= 0:
            break
        take = min(remaining, size)
        proceeds += take * price
        remaining -= take
    
    return proceeds / (qty - remaining) if qty != remaining else 0


def get_mid_price(symbol: str) -> float:
    """Get mid price (average of best bid and ask)
    
    Args:
        symbol: Trading pair symbol
        
    Returns:
        float: Mid price
    """
    ticker = get_ticker(symbol)
    return (ticker["bid"] + ticker["ask"]) / 2


def get_spread(symbol: str) -> dict:
    """Get bid-ask spread information
    
    Args:
        symbol: Trading pair symbol
        
    Returns:
        dict: Spread information with bid, ask, mid, spread_abs, spread_pct
    """
    ticker = get_ticker(symbol)
    bid, ask = ticker["bid"], ticker["ask"]
    mid = (bid + ask) / 2
    spread_abs = ask - bid
    spread_pct = spread_abs / mid if mid > 0 else 0
    
    return {
        "bid": bid,
        "ask": ask,
        "mid": mid,
        "spread_abs": spread_abs,
        "spread_pct": spread_pct
    }

