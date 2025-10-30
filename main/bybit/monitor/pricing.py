"""Bybit pricing and market data"""
import requests
from main.shared.config import BYBIT_API_BASE

def get_orderbook(symbol, depth=20):
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

def get_buy_rate(symbol, qty, depth=20):
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

def get_sell_rate(symbol, qty, depth=20):
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

def estimate_sell_slippage(symbol, qty, depth=20):
    """Estimate sell slippage using depth ratio method
    s^B ≈ 0.01 × V/D_1%
    where V = sell quantity, D_1% = bid depth within 1% of best bid
    """
    bids = get_orderbook(symbol, depth)["bids"]
    if not bids:
        return 0
    best_bid = max(p for p, _ in bids)
    threshold = best_bid * 0.99
    depth_1pct = sum(size for price, size in bids if price >= threshold)
    if depth_1pct == 0:
        return 0
    return 0.01 * (qty / depth_1pct)
