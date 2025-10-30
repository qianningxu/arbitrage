"""Transfer workflows between Bybit and Jupiter"""
from main.shared.data import get_token_info
from main.Bybit.transfers import get_deposit_address, create_withdrawal
from main.Jupiter.client import get_address
from main.Jupiter.transfers import send_sol, send_token

def transfer_to_bybit(coin, amount):
    """Transfer coin from Jupiter/Solana to Bybit"""
    coin = coin.upper()
    token_info = get_token_info(coin)
    if not token_info:
        raise ValueError(f"Token not found: {coin}")
    print(f"🔍 Fetching Bybit deposit address for {coin}...")
    bybit_address = get_deposit_address(coin)
    print(f"💸 Sending {amount} {coin} to Bybit...")
    if coin == "SOL":
        return send_sol(bybit_address, amount)
    else:
        return send_token(token_info["mint"], bybit_address, amount, token_info["decimals"])

def transfer_to_solana(coin, amount):
    """Transfer coin from Bybit to Jupiter/Solana"""
    solana_address = get_address()
    print(f"📍 Withdrawing {amount} {coin} to Solana address: {solana_address}")
    result = create_withdrawal(coin, amount, solana_address)
    print(f"✅ Withdrawal initiated: ID {result['id']}")
    return {
        "withdrawal_id": result["id"],
        "coin": coin,
        "amount": amount,
        "address": solana_address
    }

