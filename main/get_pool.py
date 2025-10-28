import requests
import json


def get_all_bybit_spot_pairs():
    url = "https://api.bybit.com/v5/market/instruments-info"
    params = {"category": "spot", "limit": 500}
    all_pairs = []
    
    while True:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        result = response.json()["result"]
        all_pairs.extend(result["list"])
        cursor = result.get("nextPageCursor")
        if not cursor:
            break
        params["cursor"] = cursor
    
    return all_pairs


def get_all_jupiter_tokens():
    jupiter_url = "https://lite-api.jup.ag/tokens/v2/tag?query=verified"
    jupiter_data = requests.get(jupiter_url).json()
    
    # Build symbol-to-mint mapping
    symbol_to_mints = {}
    for token in jupiter_data:
        symbol = token["symbol"]
        if symbol not in symbol_to_mints:
            symbol_to_mints[symbol] = []
        symbol_to_mints[symbol].append({
            "mint": token["id"],  
            "name": token.get("name", ""),
            "decimals": token.get("decimals", 6)
        })
    
    return symbol_to_mints


def get_monitor_pool():
    bybit_data = get_all_bybit_spot_pairs()
    symbol_to_mints = get_all_jupiter_tokens()
    
    # Build trading pairs
    trading_pairs = []
    for pair in bybit_data:
        base = pair["baseCoin"]
        quote = pair["quoteCoin"]
        if base in symbol_to_mints and quote in symbol_to_mints:
            trading_pairs.append({
                "bybit_symbol": pair["symbol"],
                "base_token": {
                    "symbol": base,
                    "jupiter_mints": symbol_to_mints[base]
                },
                "quote_token": {
                    "symbol": quote,
                    "jupiter_mints": symbol_to_mints[quote]
                }
            })
    
    with open("files/monitor_pool.json", "w") as f:
        json.dump(trading_pairs, indent=2, fp=f)


get_monitor_pool()