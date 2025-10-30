"""Bybit internal transfers and withdrawals"""
import json
import time
import uuid
import hmac
import hashlib
import requests
from main.shared.config import BYBIT_API_BASE, get_bybit_credentials
from main.bybit.helper.auth import sign_request

def internal_transfer(coin, amount, from_account, to_account):
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

def transfer_to_fund(coin=None, amount=None):
    """Transfer from UNIFIED to FUND"""
    from main.bybit.account.balance import get_balance, get_all_unified_balances
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

def transfer_to_unified(coin=None, amount=None):
    """Transfer from FUND to UNIFIED"""
    from main.bybit.account.balance import get_balance, get_all_fund_balances
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

def get_deposit_address(coin, chain="SOL"):
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

def create_withdrawal(coin, amount, address, chain="SOL"):
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

def withdraw(symbol, chain="SOL"):
    """Withdraw all funds of a symbol to Jupiter wallet"""
    from main.bybit.account.balance import get_balance
    from main.jupiter.helper.client import get_address
    from main.shared.data import get_withdrawal_fee
    
    coin = symbol.upper()
    print(f"🔄 Starting withdrawal process for {coin}...")
    
    # Step 1: Transfer from UNIFIED to FUND
    unified_balance = get_balance(coin, "UNIFIED")
    if unified_balance > 0:
        print(f"📦 Found {unified_balance} {coin} in UNIFIED account")
        transfer_result = transfer_to_fund(coin, unified_balance)
        if not transfer_result or not transfer_result[0].get("success"):
            raise ValueError(f"Failed to transfer {coin} from UNIFIED to FUND")
    else:
        print(f"ℹ️  No {coin} in UNIFIED account")
    
    # Step 2: Get total balance in FUND account
    fund_balance = get_balance(coin, "FUND")
    if fund_balance <= 0:
        print(f"❌ No {coin} available in FUND account to withdraw")
        return None
    
    # Step 3: Get withdrawal fee
    withdrawal_fee = get_withdrawal_fee(coin)
    if not withdrawal_fee:
        raise ValueError(f"Withdrawal fee not found for {coin}")
    
    # Step 4: Calculate withdrawal amount (balance minus fee)
    withdrawal_amount = round(fund_balance - withdrawal_fee, 8)
    
    if withdrawal_amount <= 0:
        print(f"❌ Balance ({fund_balance}) is less than or equal to withdrawal fee ({withdrawal_fee})")
        return None
    
    print(f"💰 Balance: {fund_balance} {coin}, Fee: {withdrawal_fee} {coin}, Withdrawing: {withdrawal_amount} {coin}")
    
    # Step 5: Get Jupiter wallet address
    jupiter_address = get_address()
    print(f"📍 Jupiter wallet address: {jupiter_address}")
    
    # Step 6: Create withdrawal
    print(f"🚀 Withdrawing {withdrawal_amount} {coin} to Jupiter...")
    withdrawal_result = create_withdrawal(coin, withdrawal_amount, jupiter_address, chain)
    print(f"✅ Withdrawal created: {withdrawal_result}")
    
    return {
        "coin": coin,
        "balance": fund_balance,
        "fee": withdrawal_fee,
        "amount": withdrawal_amount,
        "address": jupiter_address,
        "result": withdrawal_result
    }

