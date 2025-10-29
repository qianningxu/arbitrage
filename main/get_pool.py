import requests, json

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
    
    with open("files/all_pairs.json", 'w') as f:
        json.dump(all_pairs, f, indent=4)


def get_all_jupiter_tokens():
    jupiter_url = "https://lite-api.jup.ag/tokens/v2/tag?query=verified"
    jupiter_data = requests.get(jupiter_url).json()

    with open("files/all_jupiter_data.json", 'w') as f:
        json.dump(jupiter_data, f, indent=4)


if __name__ == "__main__":
    get_all_bybit_spot_pairs()
    get_all_jupiter_tokens()
