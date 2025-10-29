import requests


def get_sell_rate(symbol, qty, depth=100):
    """Get average sell rate from Bybit orderbook"""
    response = requests.get("https://api.bybit.com/v5/market/orderbook", params={
        "category": "spot",
        "symbol": symbol,
        "limit": depth
    })
    
    bids = [(float(p), float(sz)) for p, sz in response.json()["result"]["b"]]
    bids.sort(reverse=True)
    
    remaining, proceeds = qty, 0
    for price, size in bids:
        if remaining <= 0:
            break
        take = min(remaining, size)
        proceeds += take * price
        remaining -= take
    
    return proceeds / (qty - remaining) if qty != remaining else 0


if __name__ == "__main__":
    print(get_sell_rate("SOLUSDT", 1))
