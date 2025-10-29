import os
import sys
import requests

try:
    from main.trade.bybit_auth import sign_request
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.trade.bybit_auth import sign_request


def get_balance(coin):
    """Get spot balance for a coin"""
    coin = coin.upper()
    response = requests.get(
        "https://api.bybit.com/v5/account/wallet-balance",
        params={"accountType": "SPOT"},
        headers=sign_request("accountType=SPOT")
    )
    data = response.json()
    if data.get("retCode") == 0:
        for c in data.get("result", {}).get("list", [{}])[0].get("coin", []):
            if c.get("coin") == coin:
                return float(c.get("availableToWithdraw", 0))
    return 0


def check_balance(coin, amount):
    """Check if balance is sufficient"""
    balance = get_balance(coin)
    if balance < amount:
        raise ValueError(f"Insufficient {coin}: have {balance:.4f}, need {amount:.4f}")

