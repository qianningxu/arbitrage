"""
Batch transfer workflows
"""
from main.core.data_loader import load_tokens, get_withdrawal_fee
from main.platforms.bybit.services.balance import get_all_fund_balances, get_all_unified_balances
from main.platforms.bybit.services.transfer import transfer_to_fund
from main.platforms.solana.services.balance import check_balance
from .single_transfer import transfer_to_bybit, transfer_to_solana


def transfer_multiple_to_bybit(crypto_names=None) -> dict:
    """Batch transfer multiple cryptos from Solana to Bybit
    
    Args:
        crypto_names: List of coin symbols, single string, or None for all
        
    Returns:
        dict: Summary with total, successful, failed, and results list
    """
    print("\n" + "="*60)
    print("🚀 SOLANA TO BYBIT BATCH TRANSFER")
    print("="*60 + "\n")
    
    # Handle input types
    if crypto_names is None:
        tokens = load_tokens()
        crypto_names = list(tokens.keys())
        print("📦 Mode: Transfer ALL available cryptos")
    elif isinstance(crypto_names, str):
        crypto_names = [crypto_names]
        print(f"📦 Mode: Transfer single crypto - {crypto_names[0]}")
    else:
        print(f"📦 Mode: Transfer {len(crypto_names)} specified cryptos")
    
    results = []
    
    for coin in crypto_names:
        coin = coin.upper()
        
        try:
            print(f"\n{'='*60}")
            print(f"Processing: {coin}")
            print(f"{'='*60}")
            
            # Check balance
            balance = check_balance(coin)
            print(f"💰 Current balance: {balance} {coin}")
            
            if balance <= 0:
                print(f"⚠️  Skipping {coin}: Zero balance")
                results.append({"coin": coin, "balance": balance, "amount_transferred": 0, "success": False, "error": "Zero balance"})
                continue
            
            # Calculate transfer amount (leave buffer for fees)
            if coin == "SOL":
                transfer_amount = max(0, balance - 0.01)  # Keep 0.01 SOL for fees
                if transfer_amount <= 0:
                    print(f"⚠️  Skipping {coin}: Balance too low")
                    results.append({"coin": coin, "balance": balance, "amount_transferred": 0, "success": False, "error": "Balance too low"})
                    continue
            else:
                transfer_amount = balance
            
            # Execute transfer
            print(f"🔄 Transferring {transfer_amount} {coin} to Bybit...")
            tx_sig = transfer_to_bybit(coin, transfer_amount)
            
            results.append({"coin": coin, "balance": balance, "amount_transferred": transfer_amount, "success": True, "tx_signature": tx_sig})
            
        except Exception as e:
            print(f"❌ Failed to transfer {coin}: {str(e)}")
            results.append({"coin": coin, "balance": 0, "amount_transferred": 0, "success": False, "error": str(e)})
    
    # Summary
    successful = sum(1 for r in results if r["success"])
    print("\n" + "="*60)
    print("📊 TRANSFER SUMMARY")
    print("="*60)
    print(f"Total processed: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {len(results) - successful}")
    print("="*60 + "\n")
    
    return {"total": len(results), "successful": successful, "failed": len(results) - successful, "results": results}


def transfer_multiple_to_solana(crypto_names=None) -> dict:
    """Batch transfer multiple cryptos from Bybit to Solana
    
    Args:
        crypto_names: List of coin symbols, single string, or None for all
        
    Returns:
        dict: Summary with transfers and withdrawals
    """
    print("\n" + "="*60)
    print("🚀 BYBIT TO SOLANA BATCH TRANSFER")
    print("="*60 + "\n")
    
    # Handle input types
    transfer_all = crypto_names is None
    if transfer_all:
        print("📦 Mode: Transfer ALL available cryptos")
        crypto_set = None
    elif isinstance(crypto_names, str):
        crypto_names = [crypto_names.upper()]
        crypto_set = set(crypto_names)
        transfer_all = False
        print(f"📦 Mode: Transfer single crypto - {crypto_names[0]}")
    else:
        crypto_names = [c.upper() for c in crypto_names]
        crypto_set = set(crypto_names)
        transfer_all = False
        print(f"📦 Mode: Transfer {len(crypto_names)} specified cryptos")
    
    # Step 1: Transfer UNIFIED → FUND
    print("\n📍 STEP 1: Transfer UNIFIED → FUND")
    print("-" * 60)
    
    unified_balances = get_all_unified_balances()
    if not transfer_all and unified_balances:
        unified_balances = {k: v for k, v in unified_balances.items() if k in crypto_set}
    
    transfer_results = []
    if unified_balances:
        print(f"Found {len(unified_balances)} coins: {', '.join(unified_balances.keys())}")
        transfer_results = transfer_to_fund()
    
    # Step 2: Withdraw from FUND
    print("\n📍 STEP 2: Withdraw FUND → Solana")
    print("-" * 60)
    
    fund_balances = get_all_fund_balances()
    if not transfer_all and fund_balances:
        fund_balances = {k: v for k, v in fund_balances.items() if k in crypto_set}
    
    withdrawal_results = []
    if fund_balances:
        print(f"💰 Available: {', '.join(f'{k}: {v}' for k, v in fund_balances.items())}")
        
        for coin, amount in fund_balances.items():
            try:
                fee = get_withdrawal_fee(coin)
                if fee and fee >= amount:
                    print(f"⚠️  Skipping {coin}: Amount {amount} ≤ Fee {fee}")
                    withdrawal_results.append({"coin": coin, "amount": amount, "success": False, "error": f"Amount ≤ withdrawal fee ({fee})"})
                    continue
                
                withdrawal_amount = amount - fee if fee else amount
                result = transfer_to_solana(coin, withdrawal_amount)
                withdrawal_results.append({"coin": coin, "amount": withdrawal_amount, "fee": fee, "success": True, "result": result})
                
            except Exception as e:
                print(f"❌ Failed to withdraw {coin}: {str(e)}")
                withdrawal_results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
    
    # Summary
    successful_transfers = sum(1 for r in transfer_results if r['success'])
    successful_withdrawals = sum(1 for r in withdrawal_results if r['success'])
    
    print("\n" + "="*60)
    print("📊 TRANSFER SUMMARY")
    print("="*60)
    print(f"✅ Transfers: {successful_transfers}/{len(transfer_results)}")
    print(f"✅ Withdrawals: {successful_withdrawals}/{len(withdrawal_results)}")
    print("="*60 + "\n")
    
    return {
        "total_processed": len(set(list(unified_balances.keys() if unified_balances else []) + list(fund_balances.keys() if fund_balances else []))),
        "successful_transfers": successful_transfers,
        "successful_withdrawals": successful_withdrawals,
        "transfers": transfer_results,
        "withdrawals": withdrawal_results
    }


# Aliases for backward compatibility
transfer_all_to_bybit = lambda: transfer_multiple_to_bybit(None)
transfer_all_to_solana = lambda: transfer_multiple_to_solana(None)

