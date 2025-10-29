import os
import sys
import requests

# Handle imports
try:
    from main.trade.bybit_auth import sign_request
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.trade.bybit_auth import sign_request


def get_fund_balance(coin):
    """Get balance for a coin in FUND account"""
    coin = coin.upper()
    response = requests.get(
        "https://api.bybit.com/v5/asset/transfer/query-account-coins-balance",
        params={"accountType": "FUND", "coin": coin},
        headers=sign_request(f"accountType=FUND&coin={coin}")
    )
    data = response.json()
    if data.get("retCode") == 0:
        balance_list = data.get("result", {}).get("balance", [])
        if balance_list:
            return float(balance_list[0].get("walletBalance", 0))
    return 0


def get_unified_balance(coin):
    """Get balance for a coin in UNIFIED account"""
    coin = coin.upper()
    response = requests.get(
        "https://api.bybit.com/v5/asset/transfer/query-account-coins-balance",
        params={"accountType": "UNIFIED", "coin": coin},
        headers=sign_request(f"accountType=UNIFIED&coin={coin}")
    )
    data = response.json()
    if data.get("retCode") == 0:
        balance_list = data.get("result", {}).get("balance", [])
        if balance_list:
            return float(balance_list[0].get("walletBalance", 0))
    return 0


def get_all_fund_balances():
    """Get all non-zero balances in FUND account"""
    response = requests.get(
        "https://api.bybit.com/v5/asset/transfer/query-account-coins-balance",
        params={"accountType": "FUND"},
        headers=sign_request("accountType=FUND")
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


def get_all_unified_balances():
    """Get all non-zero balances in UNIFIED account"""
    response = requests.get(
        "https://api.bybit.com/v5/asset/transfer/query-account-coins-balance",
        params={"accountType": "UNIFIED"},
        headers=sign_request("accountType=UNIFIED")
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
