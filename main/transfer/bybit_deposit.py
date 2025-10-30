import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()


def get_bybit_deposit_address(coin_symbol):
    """Get Bybit deposit address for a specific coin via API
    
    Args:
        coin_symbol: Coin symbol (e.g., 'SOL', 'USDT')
        
    Returns:
        str: Bybit deposit address for the coin on Solana chain
        
    Raises:
        ValueError: If API returns error or no address found
    """
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError("BYBIT_API_KEY and BYBIT_API_SECRET must be set")
    
    url = "https://api.bybit.com/v5/asset/deposit/query-address"
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    coin = coin_symbol.upper()
    
    param_str = f"coin={coin}&chainType=SOL"
    sign_str = f"{timestamp}{api_key}{recv_window}{param_str}"
    signature = hmac.new(api_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
    }
    
    response = requests.get(url, params={"coin": coin, "chainType": "SOL"}, headers=headers)
    data = response.json()
    
    if data.get("retCode") != 0:
        raise ValueError(f"Bybit API error: {data.get('retMsg')}")
    
    for chain in data.get("result", {}).get("chains", []):
        if chain.get("chainType") == "SOL" and chain.get("addressDeposit"):
            address = chain["addressDeposit"]
            print(f"📍 Bybit deposit address for {coin}: {address}")
            return address
    
    raise ValueError(f"No SOL deposit address found for {coin}")

