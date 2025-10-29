import os
import json
import requests
import time
import hmac
import hashlib
from solders.keypair import Keypair


def get_solana_wallet_address():
    """Get Solana wallet address from private key"""
    keypair = Keypair.from_base58_string(os.getenv("SOLANA_PRIVATE_KEY"))
    return str(keypair.pubkey())


def check_bybit_balance(coin_symbol):
    """Check Bybit balance for a specific coin"""
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError("BYBIT_API_KEY and BYBIT_API_SECRET must be set")
    
    coin_symbol = coin_symbol.upper()
    url = "https://api.bybit.com/v5/asset/transfer/query-account-coins-balance"
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    param_str = f"accountType=FUND&coin={coin_symbol}"
    
    sign_str = f"{timestamp}{api_key}{recv_window}{param_str}"
    signature = hmac.new(api_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
    }
    
    response = requests.get(url, params={"accountType": "FUND", "coin": coin_symbol}, headers=headers)
    data = response.json()
    
    if data.get("retCode") == 0:
        balance_info = data.get("result", {}).get("balance", [])
        if balance_info:
            return float(balance_info[0].get("walletBalance", 0))
    return 0


def withdraw_from_bybit(coin_symbol, amount):
    """Withdraw coins from Bybit to Solana wallet"""
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError("BYBIT_API_KEY and BYBIT_API_SECRET must be set")
    
    coin_symbol = coin_symbol.upper()
    
    # Check balance first
    balance = check_bybit_balance(coin_symbol)
    print(f"💰 Current {coin_symbol} balance in Bybit: {balance}")
    
    if balance < amount:
        raise ValueError(f"Insufficient balance. Have {balance}, need {amount}")
    
    # Get destination address (Solana wallet)
    destination_address = get_solana_wallet_address()
    print(f"📍 Destination Solana wallet: {destination_address}")
    
    # Bybit withdrawal endpoint
    url = "https://api.bybit.com/v5/asset/withdraw/create"
    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    
    # Withdrawal parameters
    params = {
        "coin": coin_symbol,
        "chain": "SOL",
        "address": destination_address,
        "amount": str(amount)
    }
    
    # Create parameter string (must include all params in body)
    param_str = json.dumps(params)
    
    # Create signature
    sign_str = f"{timestamp}{api_key}{recv_window}{param_str}"
    signature = hmac.new(api_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "Content-Type": "application/json"
    }
    
    print(f"💸 Withdrawing {amount} {coin_symbol} from Bybit to Solana...")
    
    # Make withdrawal request
    response = requests.post(url, json=params, headers=headers)
    data = response.json()
    
    if data.get("retCode") != 0:
        raise ValueError(f"Bybit withdrawal error: {data.get('retMsg')}")
    
    withdrawal_id = data.get("result", {}).get("id")
    print(f"✅ Withdrawal initiated!")
    print(f"   Withdrawal ID: {withdrawal_id}")
    print(f"   Destination: {destination_address}")
    
    return {
        "withdrawal_id": withdrawal_id,
        "coin": coin_symbol,
        "amount": amount,
        "destination": destination_address
    }


if __name__ == "__main__":
    withdraw_from_bybit("SOL", 0.001)

