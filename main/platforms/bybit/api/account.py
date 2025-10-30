"""
Bybit account API
"""
import time
import hmac
import hashlib
import requests
from main.core.config import BYBIT_API_BASE, get_bybit_credentials
from .auth import sign_request


def get_balance(coin: str, account_type: str) -> float:
    """Get balance for a specific coin in an account
    
    Args:
        coin: Coin symbol (e.g., 'SOL')
        account_type: 'FUND' or 'UNIFIED'
        
    Returns:
        float: Balance amount
    """
    coin = coin.upper()
    response = requests.get(
        f"{BYBIT_API_BASE}/v5/asset/transfer/query-account-coins-balance",
        params={"accountType": account_type, "coin": coin},
        headers=sign_request(f"accountType={account_type}&coin={coin}")
    )
    data = response.json()
    if data.get("retCode") == 0:
        balance_list = data.get("result", {}).get("balance", [])
        if balance_list:
            return float(balance_list[0].get("walletBalance", 0))
    return 0


def get_all_balances(account_type: str) -> dict:
    """Get all non-zero balances in an account
    
    Args:
        account_type: 'FUND' or 'UNIFIED'
        
    Returns:
        dict: Balances keyed by coin symbol
    """
    response = requests.get(
        f"{BYBIT_API_BASE}/v5/asset/transfer/query-account-coins-balance",
        params={"accountType": account_type},
        headers=sign_request(f"accountType={account_type}")
    )
    data = response.json()
    balances = {}
    if data.get("retCode") == 0:
        balance_list = data.get("result", {}).get("balance", [])
        for item in balance_list:
            coin = item.get("coin")
            balance = float(item.get("walletBalance", 0))
            if balance > 0:
                balances[coin] = balance
    return balances


def get_deposit_address(coin: str, chain: str = "SOL") -> str:
    """Get deposit address for a coin
    
    Args:
        coin: Coin symbol
        chain: Blockchain (default: 'SOL')
        
    Returns:
        str: Deposit address
        
    Raises:
        ValueError: If address not found
    """
    api_key, api_secret = get_bybit_credentials()
    url = f"{BYBIT_API_BASE}/v5/asset/deposit/query-address"
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    coin = coin.upper()
    
    param_str = f"coin={coin}&chainType={chain}"
    sign_str = f"{timestamp}{api_key}{recv_window}{param_str}"
    signature = hmac.new(api_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
    }
    
    response = requests.get(url, params={"coin": coin, "chainType": chain}, headers=headers)
    data = response.json()
    
    if data.get("retCode") != 0:
        raise ValueError(f"Bybit API error: {data.get('retMsg')}")
    
    for chain_info in data.get("result", {}).get("chains", []):
        if chain_info.get("chainType") == chain and chain_info.get("addressDeposit"):
            return chain_info["addressDeposit"]
    
    raise ValueError(f"No {chain} deposit address found for {coin}")

