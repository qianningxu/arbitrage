import requests, json

def get_bybit_price(symbol):
    """Get current spot price from Bybit"""
    url = "https://api.bybit.com/v5/market/tickers"
    params = {"category": "spot", "symbol": symbol}
    response = requests.get(url, params=params)
    data = response.json()
    return float(data["result"]["list"][0]["lastPrice"])


def get_jupiter_price(input_mint, output_mint, amount):
    """Get Jupiter price for one mint pair"""
    url = "https://lite-api.jup.ag/swap/v1/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    if "error" in data:
        return None
    else:
        return int(data["outAmount"]) / int(data["inAmount"])


def get_jupiter_price_lst(bybit_symbol, amount=10):

    with open("files/monitor_pool.json", "r") as f:
        trading_pairs = json.load(f)

    for pair in trading_pairs:
        if pair["bybit_symbol"] == bybit_symbol:
            base_mints = pair["base_token"]["jupiter_mints"]
            quote_mint = pair["quote_token"]["jupiter_mints"][0]["mint"]
            
            # Get all prices
            results = []
            for mint in base_mints:
                price = get_jupiter_price(mint["mint"], quote_mint, amount)
                if price is not None:
                    results.append({"mint": mint["mint"], "price": price})
            return results
    
    return []


if __name__ == "__main__":
    print(get_bybit_price("GAMEUSDT"))
    print(get_jupiter_price_lst("GAMEUSDT", 10))