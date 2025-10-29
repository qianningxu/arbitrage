import requests
import json
import os


def get_all_bybit_spot_pairs():
    """Fetch all Bybit spot trading pairs"""
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
    
    output_path = os.path.join(os.path.dirname(__file__), "../../files/all_pairs.json")
    with open(output_path, 'w') as f:
        json.dump(all_pairs, f, indent=4)
    
    print(f"Saved {len(all_pairs)} pairs")


def get_all_jupiter_tokens():
    """Fetch all verified Jupiter tokens"""
    url = "https://lite-api.jup.ag/tokens/v2/tag?query=verified"
    data = requests.get(url).json()
    
    output_path = os.path.join(os.path.dirname(__file__), "../../files/all_jupiter_data.json")
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Saved {len(data)} tokens")


if __name__ == "__main__":
    get_all_bybit_spot_pairs()
    get_all_jupiter_tokens()
