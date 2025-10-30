"""
Transfer crypto from Solana (Jupiter) to Bybit exchange
"""
import os
import sys

# Handle imports
try:
    from main.transfer.solana_wallet import _load_tokens
    from main.transfer.bybit_deposit import get_bybit_deposit_address
    from main.transfer.solana_send import send_native_sol, send_spl_token
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.transfer.solana_wallet import _load_tokens
    from main.transfer.bybit_deposit import get_bybit_deposit_address
    from main.transfer.solana_send import send_native_sol, send_spl_token


def transfer_to_bybit(coin_symbol, amount):
    """Transfer a specific amount of a coin from Solana wallet to Bybit
    
    Args:
        coin_symbol: Coin symbol (e.g., 'SOL', 'USDT', 'USDC')
        amount: Amount to transfer
        
    Returns:
        str: Transaction signature
        
    Raises:
        ValueError: If token not found or transfer fails
    """
    tokens = _load_tokens()
    coin_symbol = coin_symbol.upper()
    
    coin_data = tokens.get(coin_symbol, [None])[0]
    if not coin_data:
        raise ValueError(f"Token not found: {coin_symbol}")
    
    print(f"🔍 Fetching Bybit deposit address for {coin_symbol}...")
    bybit_address = get_bybit_deposit_address(coin_symbol)
    
    print(f"💸 Sending {amount} {coin_symbol} to Bybit...")
    
    if coin_symbol == "SOL":
        tx_sig = send_native_sol(bybit_address, amount)
    else:
        tx_sig = send_spl_token(coin_data["mint"], bybit_address, amount, coin_data["decimals"])
    
    return tx_sig


if __name__ == "__main__":
    # Example usage
    transfer_to_bybit("SOL", 0.1)

