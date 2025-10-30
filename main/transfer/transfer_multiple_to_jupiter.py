"""
Batch transfer multiple cryptos from Bybit exchange to Solana (Jupiter) wallet
"""
import os
import sys
import json

# Handle imports
try:
    from main.trade.bybit_balance import get_all_fund_balances, get_all_unified_balances
    from main.transfer.bybit_internal import transfer_unified_to_fund
    from main.transfer.bybit_withdraw import withdraw_from_bybit
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.trade.bybit_balance import get_all_fund_balances, get_all_unified_balances
    from main.transfer.bybit_internal import transfer_unified_to_fund
    from main.transfer.bybit_withdraw import withdraw_from_bybit


def transfer_multiple_to_jupiter(crypto_names=None):
    """Transfer multiple cryptos from Bybit exchange to Solana wallet
    
    This function performs a complete transfer workflow:
    1. Transfers specified assets from UNIFIED account to FUND account
    2. Withdraws specified coins to the Solana wallet (after accounting for withdrawal fees)
    
    Args:
        crypto_names: List of coin symbols to transfer (e.g., ['SOL', 'USDT', 'USDC'])
                     Can also be a single string (e.g., 'SOL')
                     Pass None or empty list to transfer ALL available cryptos
        
    Returns:
        dict: Summary of transfers and withdrawals with the following structure:
            {
                "total_processed": int,
                "successful_transfers": int,
                "successful_withdrawals": int,
                "transfers": [list of transfer results],
                "withdrawals": [list of withdrawal results]
            }
            
    Examples:
        # Transfer specific cryptos
        transfer_multiple_to_jupiter(['SOL', 'USDT'])
        
        # Transfer a single crypto
        transfer_multiple_to_jupiter('SOL')
        
        # Transfer all available cryptos
        transfer_multiple_to_jupiter(None)
    """
    print("\n" + "="*60)
    print("🚀 BYBIT TO JUPITER BATCH TRANSFER")
    print("="*60 + "\n")
    
    # Handle different input types
    if crypto_names is None:
        # Transfer all available cryptos
        print("📦 Mode: Transfer ALL available cryptos")
        transfer_all = True
        crypto_set = None
    elif isinstance(crypto_names, str):
        # Single crypto
        crypto_names = [crypto_names.upper()]
        crypto_set = set(crypto_names)
        transfer_all = False
        print(f"📦 Mode: Transfer single crypto - {crypto_names[0]}")
    else:
        # List of cryptos
        crypto_names = [c.upper() for c in crypto_names]
        crypto_set = set(crypto_names)
        transfer_all = False
        print(f"📦 Mode: Transfer {len(crypto_names)} specified cryptos")
    
    # Step 1: Transfer from UNIFIED to FUND
    print("\n📍 STEP 1: Transfer UNIFIED → FUND")
    print("-" * 60)
    
    # Get balances to transfer
    unified_balances = get_all_unified_balances()
    
    if not unified_balances:
        print("ℹ️  No funds in UNIFIED account")
        transfer_results = []
    else:
        # Filter balances if specific cryptos requested
        if not transfer_all:
            unified_balances = {k: v for k, v in unified_balances.items() if k in crypto_set}
        
        if not unified_balances:
            print(f"⚠️  None of the requested cryptos found in UNIFIED account")
            transfer_results = []
        else:
            print(f"Found {len(unified_balances)} coins to transfer: {', '.join(unified_balances.keys())}")
            
            # Import internal_transfer for individual transfers
            from main.trade.bybit_transfer import internal_transfer
            
            transfer_results = []
            for coin, amount in unified_balances.items():
                try:
                    result = internal_transfer(coin, amount, "UNIFIED", "FUND")
                    transfer_results.append({"coin": coin, "amount": amount, "success": True, "result": result})
                except Exception as e:
                    print(f"⚠️  Failed to transfer {coin}: {str(e)}")
                    transfer_results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
    
    # Display transfer summary
    if transfer_results:
        print(f"\n✅ Transferred {sum(1 for r in transfer_results if r['success'])}/{len(transfer_results)} coins successfully")
    
    # Step 2: Get FUND balances
    print("\n📍 STEP 2: Check FUND account balances")
    print("-" * 60)
    fund_balances = get_all_fund_balances()
    
    # Filter balances if specific cryptos requested
    if not transfer_all and fund_balances:
        fund_balances = {k: v for k, v in fund_balances.items() if k in crypto_set}
    
    if not fund_balances:
        print("⚠️  No funds available in FUND account for withdrawal")
        return {
            "total_processed": len(transfer_results),
            "successful_transfers": sum(1 for r in transfer_results if r['success']),
            "successful_withdrawals": 0,
            "transfers": transfer_results,
            "withdrawals": []
        }
    
    print(f"💰 Available in FUND account:")
    for coin, amount in fund_balances.items():
        print(f"   {coin}: {amount}")
    
    # Step 3: Withdraw to Jupiter
    print("\n📍 STEP 3: Withdraw FUND → Jupiter (Solana)")
    print("-" * 60)
    withdrawal_results = []
    
    # Load withdrawal fees
    fees_path = os.path.join(os.path.dirname(__file__), "../../files/withdrawal_fees.json")
    try:
        with open(fees_path, 'r') as f:
            withdrawal_fees = json.load(f)
    except Exception as e:
        print(f"⚠️  Could not load withdrawal fees: {e}")
        withdrawal_fees = {}
    
    for coin, amount in fund_balances.items():
        try:
            if coin in withdrawal_fees:
                fee = float(withdrawal_fees[coin]["withdrawFee"])
                if fee >= amount:
                    print(f"⚠️  Skipping {coin}: Amount {amount} ≤ Fee {fee}")
                    withdrawal_results.append({
                        "coin": coin, 
                        "amount": amount, 
                        "success": False, 
                        "error": f"Amount less than withdrawal fee ({fee})"
                    })
                    continue
                
                # Withdraw (amount - fee to account for the fee)
                withdrawal_amount = amount - fee
                result = withdraw_from_bybit(coin, withdrawal_amount)
                withdrawal_results.append({
                    "coin": coin, 
                    "amount": withdrawal_amount, 
                    "fee": fee,
                    "success": True, 
                    "result": result
                })
            else:
                print(f"⚠️  No fee info for {coin}, attempting full withdrawal...")
                result = withdraw_from_bybit(coin, amount)
                withdrawal_results.append({
                    "coin": coin, 
                    "amount": amount, 
                    "success": True, 
                    "result": result
                })
                
        except Exception as e:
            print(f"❌ Failed to withdraw {coin}: {str(e)}")
            withdrawal_results.append({
                "coin": coin, 
                "amount": amount, 
                "success": False, 
                "error": str(e)
            })
    
    # Final Summary
    successful_transfers = sum(1 for r in transfer_results if r['success'])
    successful_withdrawals = sum(1 for r in withdrawal_results if r['success'])
    
    print("\n" + "="*60)
    print("📊 TRANSFER SUMMARY")
    print("="*60)
    print(f"✅ Transfers: {successful_transfers}/{len(transfer_results)}")
    print(f"✅ Withdrawals: {successful_withdrawals}/{len(withdrawal_results)}")
    print("="*60 + "\n")
    
    return {
        "total_processed": len(crypto_set) if crypto_set else len(set(list(unified_balances.keys() if unified_balances else []) + list(fund_balances.keys()))),
        "successful_transfers": successful_transfers,
        "successful_withdrawals": successful_withdrawals,
        "transfers": transfer_results,
        "withdrawals": withdrawal_results
    }


if __name__ == "__main__":
    # Example 1: Transfer specific cryptos
    # result = transfer_multiple_to_jupiter(['SOL', 'USDT'])
    
    # Example 2: Transfer all available cryptos
    # result = transfer_multiple_to_jupiter(None)
    
    # Example 3: Transfer single crypto
    # result = transfer_multiple_to_jupiter('SOL')
    
    pass

