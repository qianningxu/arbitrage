"""
Test arbitrage strategy with all-in alternating approach
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from main.workflows.arbitrage.strategy_executor import (
    detect_funds_location,
    check_arbitrage_opportunity,
    execute_arbitrage
)


def test_detect_funds_location():
    """Test detecting where funds are currently located"""
    print("\n" + "="*60)
    print("TEST: Detect Funds Location")
    print("="*60 + "\n")
    
    location = detect_funds_location()
    print(f"Location: {location['location']}")
    print(f"Bybit USDT: ${location['bybit_usdt']:.2f}")
    print(f"Solana USDT: ${location['solana_usdt']:.2f}")
    print(f"Total USDT: ${location['total_usdt']:.2f}")


def test_check_opportunity():
    """Test checking for arbitrage opportunity"""
    print("\n" + "="*60)
    print("TEST: Check Arbitrage Opportunity")
    print("="*60 + "\n")
    
    # Check for SOL arbitrage
    opportunity = check_arbitrage_opportunity(
        coins=['SOL'],
        min_profit_threshold=0.1
    )
    
    print(f"\nHas Opportunity: {opportunity['has_opportunity']}")
    print(f"Funds Location: {opportunity['funds_location']}")
    print(f"Available Path: {opportunity['available_path']}")
    print(f"Message: {opportunity['message']}")
    
    if opportunity['has_opportunity']:
        opp = opportunity['opportunity']
        print(f"\nOpportunity Details:")
        print(f"  Coin: {opp['coin']}")
        print(f"  Path: {opp['path']}")
        print(f"  Profit: ${opp['profit_usdt']:.2f} ({opp['profit_pct']:.2f}%)")


def test_execute_arbitrage_dry_run():
    """Test executing arbitrage in dry-run mode (safe)"""
    print("\n" + "="*60)
    print("TEST: Execute Arbitrage (DRY RUN)")
    print("="*60 + "\n")
    
    # First check for opportunity
    opportunity = check_arbitrage_opportunity(
        coins=['SOL'],
        min_profit_threshold=0.1
    )
    
    if opportunity['has_opportunity']:
        print("\n✅ Opportunity found - executing dry run...")
        result = execute_arbitrage(opportunity, dry_run=True)
        print(f"\nResult: {result['message']}")
    else:
        print(f"\n❌ {opportunity['message']}")


if __name__ == "__main__":
    # Run tests
    test_detect_funds_location()
    print("\n" + "="*60 + "\n")
    
    test_check_opportunity()
    print("\n" + "="*60 + "\n")
    
    test_execute_arbitrage_dry_run()

