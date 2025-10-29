"""Demo test showing the new swap functionality with auto-transfer"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.trade.bybit_balance import get_fund_balance, get_unified_balance, get_all_fund_balances
from main.trade.bybit_transfer import transfer_all_to_unified


def demo_balance_check():
    """Show current balances in both accounts"""
    print("\n" + "="*60)
    print("CURRENT BALANCES")
    print("="*60)
    
    print("\nFUND Account:")
    fund_balances = get_all_fund_balances()
    if fund_balances:
        for coin, amount in fund_balances.items():
            print(f"  {coin}: {amount}")
    else:
        print("  (empty)")
    
    print("\nUNIFIED Account (checking SOL and USDT):")
    for coin in ['SOL', 'USDT']:
        balance = get_unified_balance(coin)
        if balance > 0:
            print(f"  {coin}: {balance}")
    
    print("="*60)


def demo_transfer():
    """Demo: Transfer all assets from FUND to UNIFIED"""
    print("\n" + "="*60)
    print("DEMO: Transfer All Assets from FUND to UNIFIED")
    print("="*60)
    print("\n⚠️  Uncomment the line below to execute real transfer:")
    print("    results = transfer_all_to_unified()\n")
    
    # Uncomment to execute:
    # results = transfer_all_to_unified()
    # print(f"Transfer results: {results}")


if __name__ == "__main__":
    demo_balance_check()
    demo_transfer()
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\n1. Run: python test/trade/test_bybit_swap.py")
    print("   This will automatically transfer ALL funds from FUND to UNIFIED,")
    print("   then execute the swap.")
    print("\n2. The swap function now always ensures all crypto is in UNIFIED")
    print("   before trading, so you don't need to manually transfer!")
    print("="*60 + "\n")

