"""
Bybit trading API
"""
import json
import uuid
import requests
from main.core.config import BYBIT_API_BASE
from .auth import sign_request


def place_market_order(symbol: str, side: str, qty: float) -> dict:
    """Place a market order
    
    Args:
        symbol: Trading pair symbol
        side: 'Buy' or 'Sell'
        qty: Order quantity
        
    Returns:
        dict: Order result
        
    Raises:
        ValueError: If order fails
    """
    params = {
        "category": "spot",
        "symbol": symbol,
        "side": side,
        "orderType": "Market",
        "qty": str(qty)
    }
    
    response = requests.post(
        f"{BYBIT_API_BASE}/v5/order/create",
        json=params,
        headers=sign_request(json.dumps(params))
    )
    
    data = response.json()
    if data.get("retCode") != 0:
        raise ValueError(f"Order failed: {data.get('retMsg')}")
    
    return data["result"]


def internal_transfer(coin: str, amount: float, from_account: str, to_account: str) -> dict:
    """Transfer coins between Bybit accounts
    
    Args:
        coin: Coin symbol
        amount: Amount to transfer
        from_account: Source account type ('FUND' or 'UNIFIED')
        to_account: Destination account type ('FUND' or 'UNIFIED')
        
    Returns:
        dict: Transfer result
        
    Raises:
        ValueError: If transfer fails
    """
    coin = coin.upper()
    params = {
        "transferId": str(uuid.uuid4()),
        "coin": coin,
        "amount": str(amount),
        "fromAccountType": from_account,
        "toAccountType": to_account
    }
    
    response = requests.post(
        f"{BYBIT_API_BASE}/v5/asset/transfer/inter-transfer",
        json=params,
        headers=sign_request(json.dumps(params))
    )
    
    data = response.json()
    if data.get("retCode") != 0:
        raise ValueError(f"Transfer failed: {data.get('retMsg')}")
    
    return data["result"]


def create_withdrawal(coin: str, amount: float, address: str, chain: str = "SOL") -> dict:
    """Create withdrawal request
    
    Args:
        coin: Coin symbol
        amount: Amount to withdraw
        address: Withdrawal address
        chain: Blockchain (default: 'SOL')
        
    Returns:
        dict: Withdrawal result with withdrawal_id
        
    Raises:
        ValueError: If withdrawal fails
    """
    import time
    coin = coin.upper()
    params = {
        "coin": coin,
        "chain": chain,
        "address": address,
        "amount": str(amount),
        "timestamp": str(int(time.time() * 1000))
    }
    
    response = requests.post(
        f"{BYBIT_API_BASE}/v5/asset/withdraw/create",
        json=params,
        headers=sign_request(json.dumps(params))
    )
    
    data = response.json()
    if data.get("retCode") != 0:
        raise ValueError(f"Withdrawal failed: {data.get('retMsg')}")
    
    return data["result"]

