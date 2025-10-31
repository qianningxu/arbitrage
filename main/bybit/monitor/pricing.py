"""Bybit pricing and market data"""
import requests
from main.shared.config import BYBIT_API_BASE

def _to_bybit_symbol(base_coin):
    """Convert base coin to Bybit trading pair symbol"""
    return f"{base_coin}USDT"

def get_orderbook(base_coin, depth=20):
    """Get orderbook from Bybit
    
    Args:
        base_coin: Base coin symbol (e.g., 'SOL')
        depth: Orderbook depth (default 20)
    """
    symbol = _to_bybit_symbol(base_coin)
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

def get_buy_rate(base_coin, qty, depth=20):
    """Calculate average buy rate (buying from asks)
    
    Args:
        base_coin: Base coin symbol (e.g., 'SOL')
        qty: Quantity to buy
        depth: Orderbook depth (default 20)
    """
    asks = get_orderbook(base_coin, depth)["asks"]
    asks.sort()
    remaining, cost = qty, 0
    for price, size in asks:
        if remaining <= 0:
            break
        take = min(remaining, size)
        cost += take * price
        remaining -= take
    rate = cost / (qty - remaining) if qty != remaining else 0
    slippage = estimate_buy_slippage(base_coin, qty, depth)
    return {"rate": rate, "slippage": slippage}

def get_sell_rate(base_coin, qty, depth=20):
    """Calculate average sell rate (selling into bids)
    
    Args:
        base_coin: Base coin symbol (e.g., 'SOL')
        qty: Quantity to sell
        depth: Orderbook depth (default 20)
    """
    bids = get_orderbook(base_coin, depth)["bids"]
    bids.sort(reverse=True)
    remaining, proceeds = qty, 0
    for price, size in bids:
        if remaining <= 0:
            break
        take = min(remaining, size)
        proceeds += take * price
        remaining -= take
    rate = proceeds / (qty - remaining) if qty != remaining else 0
    slippage = estimate_sell_slippage(base_coin, qty, depth)
    return {"rate": rate, "slippage": slippage}

def estimate_buy_slippage(base_coin, qty, depth=20):
    """Estimate buy slippage using depth ratio method
    s^A ≈ 0.01 × V/D_1%
    where V = buy quantity, D_1% = ask depth within 1% of best ask
    
    Args:
        base_coin: Base coin symbol (e.g., 'SOL')
        qty: Quantity to buy
        depth: Orderbook depth (default 20)
    """
    asks = get_orderbook(base_coin, depth)["asks"]
    if not asks:
        return 0
    best_ask = min(p for p, _ in asks)
    threshold = best_ask * 1.01
    depth_1pct = sum(size for price, size in asks if price <= threshold)
    if depth_1pct == 0:
        return 0
    return 0.01 * (qty / depth_1pct)

def estimate_sell_slippage(base_coin, qty, depth=20):
    """Estimate sell slippage using depth ratio method
    s^B ≈ 0.01 × V/D_1%
    where V = sell quantity, D_1% = bid depth within 1% of best bid
    
    Args:
        base_coin: Base coin symbol (e.g., 'SOL')
        qty: Quantity to sell
        depth: Orderbook depth (default 20)
    """
    bids = get_orderbook(base_coin, depth)["bids"]
    if not bids:
        return 0
    best_bid = max(p for p, _ in bids)
    threshold = best_bid * 0.99
    depth_1pct = sum(size for price, size in bids if price >= threshold)
    if depth_1pct == 0:
        return 0
    return 0.01 * (qty / depth_1pct)
