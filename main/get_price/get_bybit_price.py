import requests


def get_orderbook(symbol, depth=100):
    """Get orderbook from Bybit"""
    response = requests.get("https://api.bybit.com/v5/market/orderbook", params={
        "category": "spot",
        "symbol": symbol,
        "limit": depth
    })
    result = response.json()["result"]
    return {
        "bids": [(float(p), float(sz)) for p, sz in result["b"]],
        "asks": [(float(p), float(sz)) for p, sz in result["a"]]
    }


def get_sell_rate(symbol, qty, depth=100):
    """Get average sell rate (sell into bids)"""
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


def get_buy_rate(symbol, qty, depth=100):
    """Get average buy rate (buy from asks)"""
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


if __name__ == "__main__":
    print(f"Sell rate: {get_sell_rate('SOLUSDT', 1)}")
    print(f"Buy rate: {get_buy_rate('SOLUSDT', 1)}")
