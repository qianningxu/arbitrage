"""
Single coin transfer workflows
"""
from main.core.data_loader import get_token_info
from main.platforms.bybit.api.account import get_deposit_address
from main.platforms.bybit.api.trading import create_withdrawal
from main.platforms.solana.api.wallet import get_address
from main.platforms.solana.api.transactions import send_sol, send_token


def transfer_to_bybit(coin: str, amount: float) -> str:
    """Transfer coin from Solana to Bybit
    
    Args:
        coin: Coin symbol (e.g., 'SOL', 'USDT')
        amount: Amount to transfer
        
    Returns:
        str: Transaction signature
        
    Raises:
        ValueError: If token not found or transfer fails
    """
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


def transfer_to_solana(coin: str, amount: float) -> dict:
    """Transfer coin from Bybit to Solana
    
    Args:
        coin: Coin symbol (e.g., 'SOL', 'USDT')
        amount: Amount to transfer
        
    Returns:
        dict: Withdrawal result with withdrawal_id
        
    Raises:
        ValueError: If withdrawal fails
    """
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

