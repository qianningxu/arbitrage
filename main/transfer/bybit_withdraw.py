import os
import sys
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Handle imports
try:
    from main.trade.bybit_auth import sign_request
    from main.transfer.solana_wallet import get_solana_wallet_address
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.trade.bybit_auth import sign_request
    from main.transfer.solana_wallet import get_solana_wallet_address


def withdraw_from_bybit(coin, amount):
    """Withdraw coins from Bybit FUND account to Solana wallet
    
    Args:
        coin: Coin symbol (e.g., 'SOL', 'USDT')
        amount: Amount to withdraw
        
    Returns:
        dict: Withdrawal result with withdrawal_id, coin, amount, and address
        
    Raises:
        ValueError: If withdrawal fails
    """
    coin = coin.upper()
    solana_address = get_solana_wallet_address()
    
    # Prepare withdrawal parameters
    timestamp = str(int(time.time() * 1000))
    params = {
        "coin": coin,
        "chain": "SOL",
        "address": solana_address,
        "amount": str(amount),
        "timestamp": timestamp
    }
    
    # Make withdrawal request
    response = requests.post(
        "https://api.bybit.com/v5/asset/withdraw/create",
        json=params,
        headers=sign_request(json.dumps(params))
    )
    
    data = response.json()
    if data.get("retCode") != 0:
        raise ValueError(f"Withdrawal failed: {data.get('retMsg')}")
    
    withdrawal_id = data["result"]["id"]
    print(f"✅ Withdrawal initiated: {amount} {coin} to {solana_address}")
    return {"withdrawal_id": withdrawal_id, "coin": coin, "amount": amount, "address": solana_address}

