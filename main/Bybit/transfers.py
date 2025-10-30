"""Bybit internal transfers and withdrawals"""
import json
import time
import uuid
import hmac
import hashlib
import requests
from main.shared.config import BYBIT_API_BASE, get_bybit_credentials
from .auth import sign_request

def internal_transfer(coin: str, amount: float, from_account: str, to_account: str) -> dict:
    """Transfer coins between Bybit accounts"""
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

def transfer_to_fund(coin: str = None, amount: float = None) -> list:
    """Transfer from UNIFIED to FUND"""
    from .balance import get_balance, get_all_unified_balances
    if coin:
        if amount is None:
            amount = get_balance(coin, "UNIFIED")
        if amount <= 0:
            return []
        try:
            result = internal_transfer(coin, amount, "UNIFIED", "FUND")
            print(f"✅ Transferred {amount} {coin} from UNIFIED to FUND")
            return [{"coin": coin, "amount": amount, "success": True, "result": result}]
        except Exception as e:
            print(f"❌ Failed to transfer {coin}: {str(e)}")
            return [{"coin": coin, "amount": amount, "success": False, "error": str(e)}]
    else:
        balances = get_all_unified_balances()
        if not balances:
            print("ℹ️  No funds in UNIFIED account")
            return []
        print(f"📦 Transferring {len(balances)} coins from UNIFIED to FUND...")
        results = []
        for coin, amount in balances.items():
            try:
                result = internal_transfer(coin, amount, "UNIFIED", "FUND")
                results.append({"coin": coin, "amount": amount, "success": True, "result": result})
            except Exception as e:
                print(f"⚠️  Failed to transfer {coin}: {str(e)}")
                results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
        return results

def transfer_to_unified(coin: str = None, amount: float = None) -> list:
    """Transfer from FUND to UNIFIED"""
    from .balance import get_balance, get_all_fund_balances
    if coin:
        if amount is None:
            amount = get_balance(coin, "FUND")
        if amount <= 0:
            return []
        try:
            result = internal_transfer(coin, amount, "FUND", "UNIFIED")
            print(f"✅ Transferred {amount} {coin} from FUND to UNIFIED")
            return [{"coin": coin, "amount": amount, "success": True, "result": result}]
        except Exception as e:
            print(f"❌ Failed to transfer {coin}: {str(e)}")
            return [{"coin": coin, "amount": amount, "success": False, "error": str(e)}]
    else:
        balances = get_all_fund_balances()
        if not balances:
            print("ℹ️  No funds in FUND account")
            return []
        print(f"📦 Transferring {len(balances)} coins from FUND to UNIFIED...")
        results = []
        for coin, amount in balances.items():
            try:
                result = internal_transfer(coin, amount, "FUND", "UNIFIED")
                results.append({"coin": coin, "amount": amount, "success": True, "result": result})
            except Exception as e:
                print(f"⚠️  Failed to transfer {coin}: {str(e)}")
                results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
        return results

def get_deposit_address(coin: str, chain: str = "SOL") -> str:
    """Get deposit address for a coin"""
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

def create_withdrawal(coin: str, amount: float, address: str, chain: str = "SOL") -> dict:
    """Create withdrawal request"""
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

