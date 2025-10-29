import os
import json
import requests
import time
import hmac
import hashlib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_withdrawal_fee(coin_symbol):
    """Get withdrawal fee for a specific coin from Bybit API"""
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError("BYBIT_API_KEY and BYBIT_API_SECRET must be set")
    
    url = "https://api.bybit.com/v5/asset/coin/query-info"
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    param_str = f"coin={coin_symbol}"
    
    sign_str = f"{timestamp}{api_key}{recv_window}{param_str}"
    signature = hmac.new(api_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
    }
    
    try:
        response = requests.get(url, params={"coin": coin_symbol}, headers=headers)
        data = response.json()
        
        if data.get("retCode") == 0 and data.get("result", {}).get("rows"):
            for chain in data["result"]["rows"][0]["chains"]:
                if chain.get("chain") == "SOL":
                    return {
                        "coin": coin_symbol,
                        "chain": "SOL",
                        "withdrawFee": chain.get("withdrawFee", "N/A"),
                        "minWithdrawAmount": chain.get("minWithdrawAmount", "N/A"),
                        "withdrawStatus": chain.get("chainWithdraw", 0)
                    }
        return None
    except Exception as e:
        print(f"Error fetching {coin_symbol}: {e}")
        return None


def get_all_withdrawal_fees():
    """Get withdrawal fees for all coins in valid_pairs_usdt.json"""
    # Load valid pairs
    pairs_file = os.path.join(os.path.dirname(__file__), "../../files/valid_pairs_usdt.json")
    with open(pairs_file, "r") as f:
        pairs = json.load(f)
    
    # Extract unique coins (remove USDT suffix)
    coins = set()
    for pair in pairs:
        if pair.endswith("USDT"):
            coin = pair[:-4]  # Remove "USDT"
            if coin != "USDT":  # Skip USDT itself
                coins.add(coin)
    
    print(f"Found {len(coins)} unique coins to check...")
    
    # Get withdrawal fees for each coin
    withdrawal_fees = {}
    for i, coin in enumerate(sorted(coins), 1):
        print(f"[{i}/{len(coins)}] Checking {coin}...")
        fee_info = get_withdrawal_fee(coin)
        if fee_info:
            withdrawal_fees[coin] = fee_info
        time.sleep(0.1)  # Rate limiting
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), "../../files/withdrawal_fees.json")
    with open(output_file, "w") as f:
        json.dump(withdrawal_fees, f, indent=2)
    
    print(f"\n✅ Saved withdrawal fees to {output_file}")
    print(f"   Found fees for {len(withdrawal_fees)} coins on SOL chain")
    
    return withdrawal_fees


if __name__ == "__main__":
    fees = get_all_withdrawal_fees()
    
    # Print summary
    print("\n📊 Summary:")
    for coin, info in sorted(fees.items()):
        if info["withdrawFee"] != "N/A":
            print(f"  {coin}: {info['withdrawFee']} SOL")

