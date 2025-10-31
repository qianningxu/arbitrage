"""测试套利执行功能"""
import sys
sys.path.append('/Users/side/Desktop/arbitrage')

from main.workflows.execute_arbitrage import execute_arbitrage

def test_execute_arbitrage(base_coin="SOL", direction="J→B"):
    """
    Test executing arbitrage
    
    Args:
        base_coin: Base coin symbol (default: "SOL")
        direction: Direction to execute ('B→J' or 'J→B', default: "J→B")
    """
    print(f"\n{'='*60}")
    print(f"Testing execute_arbitrage for {base_coin} [{direction}]")
    print(f"{'='*60}\n")
    
    result = execute_arbitrage(base_coin, direction)
    
    print(f"\n{'='*60}")
    print(f"Test Result:")
    print(f"  Success: {result['success']}")
    print(f"  Coin: {result['coin']}")
    print(f"  Direction: {result['direction']}")
    if result['success']:
        print(f"  Initial Balance: ${result['initial_balance']:.2f}")
        print(f"  Final Balance: ${result['final_balance']:.2f}")
        print(f"  Actual Profit: ${result['actual_profit']:.2f}")
        print(f"  Steps Completed: {len(result['steps'])}")
    else:
        print(f"  Error: {result['error']}")
    print(f"{'='*60}\n")
    
    return result

if __name__ == "__main__":
    # Uncomment the direction you want to test:
    # test_execute_arbitrage("SOL", "B→J")
    test_execute_arbitrage("USDC", "B→J")

