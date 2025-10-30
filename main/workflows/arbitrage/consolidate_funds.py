"""
Fund consolidation utilities

Helper functions to consolidate all funds to one exchange
"""
from main.Bybit.balance import get_all_fund_balances, get_all_unified_balances
from main.Jupiter.balance import get_token_balance
from main.workflows.transfers.bridge import transfer_to_bybit, transfer_to_solana

def get_all_balances():
    """Get all Jupiter/Solana balances"""
    from main.shared.data import load_tokens
    tokens = load_tokens()
    balances = {}
    for symbol in tokens.keys():
        try:
            balance = get_token_balance(symbol)
            if balance > 0:
                balances[symbol] = balance
        except:
            pass
    return balances


def consolidate_to_bybit():
    """Consolidate all funds from Solana to Bybit
    
    This moves ALL available cryptos from Solana to Bybit
    
    Returns:
        dict: Transfer results
    """
    print("\n" + "="*60)
    print("📦 CONSOLIDATING FUNDS → BYBIT")
    print("="*60 + "\n")
    
    balances = get_all_balances()
    results = []
    
    for coin, amount in balances.items():
        if coin == "SOL" and amount < 0.02:
            print(f"⚠️  Skipping {coin}: Keeping {amount} for fees")
            continue
        
        try:
            transfer_amount = amount - 0.01 if coin == "SOL" else amount
            print(f"🔄 Transferring {transfer_amount} {coin} to Bybit...")
            tx_sig = transfer_to_bybit(coin, transfer_amount)
            results.append({"coin": coin, "amount": transfer_amount, "success": True, "tx_signature": tx_sig})
        except Exception as e:
            print(f"❌ Failed to transfer {coin}: {str(e)}")
            results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
    
    successful = sum(1 for r in results if r["success"])
    if successful > 0:
        print(f"\n✅ Successfully moved {successful} coins to Bybit")
        print(f"💰 All funds now on Bybit - ready for Path B")
    else:
        print(f"\n⚠️  No funds transferred")
    
    return {"total": len(results), "successful": successful, "results": results}


def consolidate_to_solana():
    """Consolidate all funds from Bybit to Solana
    
    This moves ALL available cryptos from Bybit to Solana
    
    Returns:
        dict: Transfer results
    """
    from main.Bybit.transfers import transfer_to_fund
    from main.shared.data import get_withdrawal_fee
    
    print("\n" + "="*60)
    print("📦 CONSOLIDATING FUNDS → SOLANA")
    print("="*60 + "\n")
    
    # First move UNIFIED → FUND
    print("Step 1: Moving UNIFIED → FUND...")
    transfer_to_fund()
    
    # Then withdraw all from FUND
    print("\nStep 2: Withdrawing from FUND to Solana...")
    fund_balances = get_all_fund_balances()
    results = []
    
    for coin, amount in fund_balances.items():
        try:
            fee = get_withdrawal_fee(coin)
            if fee and fee >= amount:
                print(f"⚠️  Skipping {coin}: Amount {amount} ≤ Fee {fee}")
                results.append({"coin": coin, "amount": amount, "success": False, "error": f"Amount ≤ withdrawal fee ({fee})"})
                continue
            
            withdrawal_amount = amount - fee if fee else amount
            print(f"🔄 Withdrawing {withdrawal_amount} {coin} to Solana...")
            result = transfer_to_solana(coin, withdrawal_amount)
            results.append({"coin": coin, "amount": withdrawal_amount, "success": True, "result": result})
        except Exception as e:
            print(f"❌ Failed to withdraw {coin}: {str(e)}")
            results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
    
    successful = sum(1 for r in results if r["success"])
    if successful > 0:
        print(f"\n✅ Successfully moved {successful} coins to Solana")
        print(f"💰 All funds now on Solana - ready for Path A")
    else:
        print(f"\n⚠️  No funds transferred")
    
    return {"total": len(results), "successful": successful, "results": results}


def consolidate_to_usdt_on_bybit():
    """Consolidate all coins to USDT on Bybit
    
    This swaps all non-USDT coins to USDT on Bybit
    Useful after receiving various coins
    """
    from main.Bybit.balance import get_all_unified_balances
    from main.Bybit.swap import swap
    
    print("\n" + "="*60)
    print("💱 CONSOLIDATING TO USDT ON BYBIT")
    print("="*60 + "\n")
    
    balances = get_all_unified_balances()
    results = []
    
    for coin, amount in balances.items():
        if coin == "USDT":
            print(f"✅ {coin}: {amount} (already USDT)")
            continue
        
        try:
            print(f"🔄 Converting {amount} {coin} → USDT...")
            result = swap(coin, "USDT", amount, "in")
            results.append({"coin": coin, "amount": amount, "success": True})
        except Exception as e:
            print(f"❌ Failed to convert {coin}: {str(e)}")
            results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
    
    successful = sum(1 for r in results if r["success"])
    print(f"\n✅ Converted {successful}/{len(results)} coins to USDT")
    
    return {"total": len(results), "successful": successful, "results": results}


def consolidate_to_usdt_on_solana():
    """Consolidate all coins to USDT on Solana
    
    This swaps all non-USDT coins to USDT on Jupiter
    """
    from main.Jupiter.swap import swap
    
    print("\n" + "="*60)
    print("💱 CONSOLIDATING TO USDT ON SOLANA")
    print("="*60 + "\n")
    
    balances = get_all_balances()
    results = []
    
    for coin, amount in balances.items():
        if coin == "USDT":
            print(f"✅ {coin}: {amount} (already USDT)")
            continue
        
        if coin == "SOL" and amount < 0.02:
            print(f"⚠️  Skipping {coin}: {amount} (keeping for fees)")
            continue
        
        try:
            # Keep some SOL for fees
            transfer_amount = amount - 0.01 if coin == "SOL" else amount
            print(f"🔄 Converting {transfer_amount} {coin} → USDT...")
            result = swap(coin, "USDT", transfer_amount)
            results.append({"coin": coin, "amount": transfer_amount, "success": True})
        except Exception as e:
            print(f"❌ Failed to convert {coin}: {str(e)}")
            results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
    
    successful = sum(1 for r in results if r["success"])
    print(f"\n✅ Converted {successful}/{len(results)} coins to USDT")
    
    return {"total": len(results), "successful": successful, "results": results}


if __name__ == "__main__":
    # Example: Consolidate to Bybit
    # result = consolidate_to_bybit()
    
    # Example: Consolidate to Solana
    # result = consolidate_to_solana()
    
    # Example: Convert all to USDT on current platform
    # result = consolidate_to_usdt_on_bybit()
    # result = consolidate_to_usdt_on_solana()
    
    pass

