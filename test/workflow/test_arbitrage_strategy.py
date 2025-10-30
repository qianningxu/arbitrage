"""
Test arbitrage strategy with all-in alternating approach
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

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


def test_check_opportunity(coins, min_profit_threshold):
    """Test checking for arbitrage opportunity"""
    print("\n" + "="*60)
    print("TEST: Check Arbitrage Opportunity")
    print("="*60 + "\n")
    
    opportunity = check_arbitrage_opportunity(
        coins=coins,
        min_profit_threshold=min_profit_threshold
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


def test_execute_arbitrage_dry_run(coins, min_profit_threshold):
    """Test executing arbitrage in dry-run mode (safe)"""
    print("\n" + "="*60)
    print("TEST: Execute Arbitrage (DRY RUN)")
    print("="*60 + "\n")
    
    opportunity = check_arbitrage_opportunity(
        coins=coins,
        min_profit_threshold=min_profit_threshold
    )
    
    if opportunity['has_opportunity']:
        print("\n✅ Opportunity found - executing dry run...")
        result = execute_arbitrage(opportunity, dry_run=True)
        print(f"\nResult: {result['message']}")
    else:
        print(f"\n❌ {opportunity['message']}")


if __name__ == "__main__":
    test_detect_funds_location()
    print("\n" + "="*60 + "\n")
    
    test_check_opportunity(['SOL'], 0.1)
    print("\n" + "="*60 + "\n")
    
    test_execute_arbitrage_dry_run(['SOL'], 0.1)

