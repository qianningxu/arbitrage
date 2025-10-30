"""Bybit balance operations"""
import requests
from main.shared.config import BYBIT_API_BASE
from main.Bybit.helper.auth import sign_request

def get_balance(coin, account_type):
    """Get balance for a specific coin in an account"""
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

def get_all_balances(account_type):
    """Get all non-zero balances in an account"""
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

def get_fund_balance(coin):
    """Get balance in FUND account"""
    return get_balance(coin, "FUND")

def get_unified_balance(coin):
    """Get balance in UNIFIED account"""
    return get_balance(coin, "UNIFIED")

def get_total_balance(coin):
    """Get total balance across all accounts"""
    return get_fund_balance(coin) + get_unified_balance(coin)

def get_all_fund_balances():
    """Get all non-zero balances in FUND account"""
    return get_all_balances("FUND")

def get_all_unified_balances():
    """Get all non-zero balances in UNIFIED account"""
    return get_all_balances("UNIFIED")

