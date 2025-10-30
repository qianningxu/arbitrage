"""Bybit pricing and market data"""
import requests
from main.shared.config import BYBIT_API_BASE

def get_orderbook(symbol, depth=100):
    """Get orderbook from Bybit"""
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

def get_ticker(symbol):
    """Get ticker (best bid/ask) from Bybit"""
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

def get_buy_rate(symbol, qty, depth=100):
    """Calculate average buy rate (buying from asks)"""
    asks = get_orderbook(symbol, depth)["asks"]
    asks.sort()
    remaining, cost = qty, 0
    for price, size in asks:
        if remaining <= 0:
            break
        take = min(remaining, size)
        cost += take * price
        remaining -= take
    return cost / (qty - remaining) if qty != remaining else 0

def get_sell_rate(symbol, qty, depth=100):
    """Calculate average sell rate (selling into bids)"""
    bids = get_orderbook(symbol, depth)["bids"]
    bids.sort(reverse=True)
    remaining, proceeds = qty, 0
    for price, size in bids:
        if remaining <= 0:
            break
        take = min(remaining, size)
        proceeds += take * price
        remaining -= take
    return proceeds / (qty - remaining) if qty != remaining else 0

def get_mid_price(symbol):
    """Get mid price (average of best bid and ask)"""
    ticker = get_ticker(symbol)
    return (ticker["bid"] + ticker["ask"]) / 2

def get_spread(symbol):
    """Get bid-ask spread information"""
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

