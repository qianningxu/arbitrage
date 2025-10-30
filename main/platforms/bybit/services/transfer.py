"""
Bybit transfer services
"""
from ..api.trading import internal_transfer
from .balance import get_all_fund_balances, get_all_unified_balances


def transfer_to_fund(coin: str = None, amount: float = None) -> list:
    """Transfer from UNIFIED to FUND
    
    Args:
        coin: Specific coin (None for all)
        amount: Specific amount (None for all available)
        
    Returns:
        list: Transfer results
    """
    if coin:
        # Transfer specific coin
        if amount is None:
            from ..api.account import get_balance
            amount = get_balance(coin, "UNIFIED")
        
        if amount <= 0:
            return []
        
        try:
            result = internal_transfer(coin, amount, "UNIFIED", "FUND")
            print(f"✅ Transferred {amount} {coin} from UNIFIED to FUND")
            return [{"coin": coin, "amount": amount, "success": True, "result": result}]
        except Exception as e:
            print(f"❌ Failed to transfer {coin}: {str(e)}")
            return [{"coin": coin, "amount": amount, "success": False, "error": str(e)}]
    else:
        # Transfer all coins
        balances = get_all_unified_balances()
        if not balances:
            print("ℹ️  No funds in UNIFIED account")
            return []
        
        print(f"📦 Transferring {len(balances)} coins from UNIFIED to FUND...")
        results = []
        for coin, amount in balances.items():
            try:
                result = internal_transfer(coin, amount, "UNIFIED", "FUND")
                results.append({"coin": coin, "amount": amount, "success": True, "result": result})
            except Exception as e:
                print(f"⚠️  Failed to transfer {coin}: {str(e)}")
                results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
        
        return results


def transfer_to_unified(coin: str = None, amount: float = None) -> list:
    """Transfer from FUND to UNIFIED
    
    Args:
        coin: Specific coin (None for all)
        amount: Specific amount (None for all available)
        
    Returns:
        list: Transfer results
    """
    if coin:
        # Transfer specific coin
        if amount is None:
            from ..api.account import get_balance
            amount = get_balance(coin, "FUND")
        
        if amount <= 0:
            return []
        
        try:
            result = internal_transfer(coin, amount, "FUND", "UNIFIED")
            print(f"✅ Transferred {amount} {coin} from FUND to UNIFIED")
            return [{"coin": coin, "amount": amount, "success": True, "result": result}]
        except Exception as e:
            print(f"❌ Failed to transfer {coin}: {str(e)}")
            return [{"coin": coin, "amount": amount, "success": False, "error": str(e)}]
    else:
        # Transfer all coins
        balances = get_all_fund_balances()
        if not balances:
            print("ℹ️  No funds in FUND account")
            return []
        
        print(f"📦 Transferring {len(balances)} coins from FUND to UNIFIED...")
        results = []
        for coin, amount in balances.items():
            try:
                result = internal_transfer(coin, amount, "FUND", "UNIFIED")
                results.append({"coin": coin, "amount": amount, "success": True, "result": result})
            except Exception as e:
                print(f"⚠️  Failed to transfer {coin}: {str(e)}")
                results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
        
        return results

