"""
Fund consolidation utilities

Helper functions to consolidate all funds to one exchange
"""
from main.workflows.transfers.batch_transfer import transfer_multiple_to_bybit, transfer_multiple_to_solana


def consolidate_to_bybit():
    """Consolidate all funds from Solana to Bybit
    
    This moves ALL available cryptos from Solana to Bybit
    
    Returns:
        dict: Transfer results
    """
    print("\n" + "="*60)
    print("📦 CONSOLIDATING FUNDS → BYBIT")
    print("="*60 + "\n")
    
    result = transfer_multiple_to_bybit(None)  # None = transfer ALL
    
    if result["successful"] > 0:
        print(f"\n✅ Successfully moved {result['successful']} coins to Bybit")
        print(f"💰 All funds now on Bybit - ready for Path B")
    else:
        print(f"\n⚠️  No funds transferred")
    
    return result


def consolidate_to_solana():
    """Consolidate all funds from Bybit to Solana
    
    This moves ALL available cryptos from Bybit to Solana
    
    Returns:
        dict: Transfer results
    """
    print("\n" + "="*60)
    print("📦 CONSOLIDATING FUNDS → SOLANA")
    print("="*60 + "\n")
    
    result = transfer_multiple_to_solana(None)  # None = transfer ALL
    
    if result["successful_withdrawals"] > 0:
        print(f"\n✅ Successfully moved {result['successful_withdrawals']} coins to Solana")
        print(f"💰 All funds now on Solana - ready for Path A")
    else:
        print(f"\n⚠️  No funds transferred")
    
    return result


def consolidate_to_usdt_on_bybit():
    """Consolidate all coins to USDT on Bybit
    
    This swaps all non-USDT coins to USDT on Bybit
    Useful after receiving various coins
    """
    from main.platforms.bybit.services.balance import get_all_unified_balances
    from main.platforms.bybit.services.trading import swap
    
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
    from main.platforms.solana.services.balance import get_all_balances
    from main.platforms.solana.services.trading import swap
    
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

