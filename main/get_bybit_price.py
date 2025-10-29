import requests

def get_sell_rate(symbol: str, qty: float, depth: int = 100):
    r = requests.get("https://api.bybit.com/v5/market/orderbook",
                     params={"category": "spot", "symbol": symbol, "limit": depth})
    bids = [(float(p), float(sz)) for p, sz in r.json()["result"]["b"]]
    bids.sort(key=lambda x: x[0], reverse=True)

    rem, proceeds = qty, 0
    for price, size in bids:
        if rem <= 0: break
        take = min(rem, size)
        proceeds += take * price
        rem -= take

    return proceeds / (qty - rem) if qty != rem else 0

# Example:
rate = get_sell_rate("SOLUSDT", 1)
print(rate)
