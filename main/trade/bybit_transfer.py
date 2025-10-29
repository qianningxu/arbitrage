import os
import sys
import json
import uuid
import requests

# Handle imports
try:
    from main.trade.bybit_auth import sign_request
    from main.trade.bybit_balance import get_all_fund_balances
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.trade.bybit_auth import sign_request
    from main.trade.bybit_balance import get_all_fund_balances


def internal_transfer(coin, amount, from_account="FUND", to_account="UNIFIED"):
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
        "https://api.bybit.com/v5/asset/transfer/inter-transfer",
        json=params,
        headers=sign_request(json.dumps(params))
    )
    
    data = response.json()
    if data.get("retCode") != 0:
        raise ValueError(f"Transfer failed: {data.get('retMsg')}")
    
    print(f"✅ Transferred {amount} {coin} from {from_account} to {to_account}")
    return data["result"]


def transfer_all_to_unified():
    """Transfer all coins from FUND to UNIFIED account"""
    balances = get_all_fund_balances()
    
    if not balances:
        print("ℹ️  No funds in FUND account to transfer")
        return []
    
    print(f"📦 Transferring all assets from FUND to UNIFIED...")
    results = []
    
    for coin, amount in balances.items():
        try:
            result = internal_transfer(coin, amount, "FUND", "UNIFIED")
            results.append({"coin": coin, "amount": amount, "success": True, "result": result})
        except Exception as e:
            print(f"⚠️  Failed to transfer {coin}: {str(e)}")
            results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
    
    return results

