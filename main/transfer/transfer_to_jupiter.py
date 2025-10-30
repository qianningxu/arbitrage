"""
Transfer crypto from Bybit exchange to Solana (Jupiter) wallet
"""
import os
import sys
import json

# Handle imports
try:
    from main.trade.bybit_balance import get_all_fund_balances
    from main.transfer.bybit_internal import transfer_unified_to_fund
    from main.transfer.bybit_withdraw import withdraw_from_bybit
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.trade.bybit_balance import get_all_fund_balances
    from main.transfer.bybit_internal import transfer_unified_to_fund
    from main.transfer.bybit_withdraw import withdraw_from_bybit


def transfer_all_to_jupiter():
    """Complete flow: Transfer all cryptos from UNIFIED to FUND, then withdraw all to Jupiter (Solana) wallet
    
    This function performs a complete transfer workflow:
    1. Transfers all assets from UNIFIED account to FUND account
    2. Gets all balances in FUND account
    3. Withdraws all coins to the Solana wallet (after accounting for withdrawal fees)
    
    Returns:
        dict: Summary of transfers and withdrawals with the following structure:
            {
                "transfers": [list of transfer results],
                "withdrawals": [list of withdrawal results]
            }
    """
    print("\n" + "="*60)
    print("🚀 BYBIT TO JUPITER TRANSFER FLOW")
    print("="*60 + "\n")
    
    # Step 1: Transfer from UNIFIED to FUND
    print("📍 STEP 1: Transfer UNIFIED → FUND")
    print("-" * 60)
    transfer_results = transfer_unified_to_fund()
    
    if not transfer_results:
        print("\n❌ No funds to transfer. Exiting.")
        return {"transfers": [], "withdrawals": []}
    
    # Display transfer summary
    print(f"\n✅ Transferred {sum(1 for r in transfer_results if r['success'])}/{len(transfer_results)} coins successfully")
    
    # Step 2: Get all FUND balances
    print("\n📍 STEP 2: Check FUND account balances")
    print("-" * 60)
    fund_balances = get_all_fund_balances()
    
    if not fund_balances:
        print("⚠️  No funds available in FUND account for withdrawal")
        return {"transfers": transfer_results, "withdrawals": []}
    
    print(f"💰 Available in FUND account:")
    for coin, amount in fund_balances.items():
        print(f"   {coin}: {amount}")
    
    # Step 3: Withdraw to Jupiter
    print("\n📍 STEP 3: Withdraw FUND → Jupiter (Solana)")
    print("-" * 60)
    withdrawal_results = []
    
    for coin, amount in fund_balances.items():
        try:
            # Load withdrawal fees to check if withdrawal is possible
            fees_path = os.path.join(os.path.dirname(__file__), "../../files/withdrawal_fees.json")
            with open(fees_path, 'r') as f:
                withdrawal_fees = json.load(f)
            
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
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"✅ Transfers: {sum(1 for r in transfer_results if r['success'])}/{len(transfer_results)}")
    print(f"✅ Withdrawals: {sum(1 for r in withdrawal_results if r['success'])}/{len(withdrawal_results)}")
    print("="*60 + "\n")
    
    return {
        "transfers": transfer_results,
        "withdrawals": withdrawal_results
    }


if __name__ == "__main__":
    # Example: Run the complete transfer flow
    result = transfer_all_to_jupiter()
    print("\nFinal result:", json.dumps(result, indent=2))

