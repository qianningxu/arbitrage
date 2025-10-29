import requests


def get_pair_info(symbol):
    """Get trading pair info"""
    response = requests.get("https://api.bybit.com/v5/market/instruments-info", params={
        "category": "spot", "symbol": symbol
    })
    data = response.json()
    if data.get("retCode") == 0 and data.get("result", {}).get("list"):
        info = data["result"]["list"][0]
        return {
            "base": info["baseCoin"],
            "quote": info["quoteCoin"],
            "minQty": float(info["lotSizeFilter"]["minOrderQty"]),
            "precision": float(info["lotSizeFilter"]["basePrecision"])
        }

