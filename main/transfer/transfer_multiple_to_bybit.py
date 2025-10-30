"""
Batch transfer multiple cryptos from Solana (Jupiter) to Bybit exchange
"""
import os
import sys

# Handle imports
try:
    from main.transfer.transfer_to_bybit import transfer_to_bybit
    from main.transfer.solana_wallet import _load_tokens
    from main.trade.jupiter_helpers import check_balance
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.transfer.transfer_to_bybit import transfer_to_bybit
    from main.transfer.solana_wallet import _load_tokens
    from main.trade.jupiter_helpers import check_balance


def transfer_multiple_to_bybit(crypto_names):
    """Transfer multiple cryptos from Solana wallet to Bybit exchange
    
    This function will check the balance of each crypto in the Solana wallet
    and transfer the available amount (minus a small buffer for fees) to Bybit.
    
    Args:
        crypto_names: List of coin symbols to transfer (e.g., ['SOL', 'USDT', 'USDC'])
                     Can also be a single string (e.g., 'SOL')
                     Pass None or empty list to transfer ALL available cryptos
        
    Returns:
        dict: Summary of all transfers with the following structure:
            {
                "total": int,
                "successful": int,
                "failed": int,
                "results": [list of individual transfer results]
            }
            
    Examples:
        # Transfer specific cryptos
        transfer_multiple_to_bybit(['SOL', 'USDT'])
        
        # Transfer a single crypto
        transfer_multiple_to_bybit('SOL')
        
        # Transfer all available cryptos
        transfer_multiple_to_bybit(None)
    """
    print("\n" + "="*60)
    print("🚀 JUPITER TO BYBIT BATCH TRANSFER")
    print("="*60 + "\n")
    
    # Handle different input types
    if crypto_names is None:
        # Transfer all available cryptos
        tokens = _load_tokens()
        crypto_names = list(tokens.keys())
        print("📦 Mode: Transfer ALL available cryptos")
    elif isinstance(crypto_names, str):
        # Single crypto
        crypto_names = [crypto_names]
        print(f"📦 Mode: Transfer single crypto - {crypto_names[0]}")
    else:
        # List of cryptos
        print(f"📦 Mode: Transfer {len(crypto_names)} specified cryptos")
    
    results = []
    
    for coin_symbol in crypto_names:
        coin_symbol = coin_symbol.upper()
        
        try:
            print(f"\n{'='*60}")
            print(f"Processing: {coin_symbol}")
            print(f"{'='*60}")
            
            # Check balance
            balance = check_balance(coin_symbol)
            print(f"💰 Current balance: {balance} {coin_symbol}")
            
            if balance <= 0:
                print(f"⚠️  Skipping {coin_symbol}: Zero balance")
                results.append({
                    "coin": coin_symbol,
                    "balance": balance,
                    "amount_transferred": 0,
                    "success": False,
                    "error": "Zero balance"
                })
                continue
            
            # Calculate transfer amount (leave small buffer for fees)
            if coin_symbol == "SOL":
                # For SOL, leave 0.01 SOL for future transaction fees
                transfer_amount = max(0, balance - 0.01)
                if transfer_amount <= 0:
                    print(f"⚠️  Skipping {coin_symbol}: Balance too low (need buffer for fees)")
                    results.append({
                        "coin": coin_symbol,
                        "balance": balance,
                        "amount_transferred": 0,
                        "success": False,
                        "error": "Balance too low (need buffer for fees)"
                    })
                    continue
            else:
                # For SPL tokens, transfer all (SOL covers the fee)
                transfer_amount = balance
            
            # Execute transfer
            print(f"🔄 Transferring {transfer_amount} {coin_symbol} to Bybit...")
            tx_sig = transfer_to_bybit(coin_symbol, transfer_amount)
            
            results.append({
                "coin": coin_symbol,
                "balance": balance,
                "amount_transferred": transfer_amount,
                "success": True,
                "tx_signature": tx_sig
            })
            
        except Exception as e:
            print(f"❌ Failed to transfer {coin_symbol}: {str(e)}")
            results.append({
                "coin": coin_symbol,
                "balance": balance if 'balance' in locals() else 0,
                "amount_transferred": 0,
                "success": False,
                "error": str(e)
            })
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    print("\n" + "="*60)
    print("📊 TRANSFER SUMMARY")
    print("="*60)
    print(f"Total processed: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print("="*60 + "\n")
    
    return {
        "total": len(results),
        "successful": successful,
        "failed": failed,
        "results": results
    }


if __name__ == "__main__":
    # Example 1: Transfer specific cryptos
    # result = transfer_multiple_to_bybit(['SOL', 'USDT'])
    
    # Example 2: Transfer all available cryptos
    # result = transfer_multiple_to_bybit(None)
    
    # Example 3: Transfer single crypto
    # result = transfer_multiple_to_bybit('SOL')
    
    pass

