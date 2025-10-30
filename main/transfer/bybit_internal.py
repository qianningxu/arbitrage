import os
import sys

# Handle imports
try:
    from main.trade.bybit_balance import get_all_unified_balances
    from main.trade.bybit_transfer import internal_transfer
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.trade.bybit_balance import get_all_unified_balances
    from main.trade.bybit_transfer import internal_transfer


def transfer_unified_to_fund():
    """Transfer all coins from UNIFIED to FUND account
    
    Returns:
        list: List of transfer results with coin, amount, success status
    """
    balances = get_all_unified_balances()
    
    if not balances:
        print("ℹ️  No funds in UNIFIED account to transfer")
        return []
    
    print(f"📦 Found {len(balances)} coins in UNIFIED account")
    print(f"💰 Transferring all assets from UNIFIED to FUND...")
    results = []
    
    for coin, amount in balances.items():
        try:
            result = internal_transfer(coin, amount, "UNIFIED", "FUND")
            results.append({"coin": coin, "amount": amount, "success": True, "result": result})
        except Exception as e:
            print(f"⚠️  Failed to transfer {coin}: {str(e)}")
            results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
    
    return results

