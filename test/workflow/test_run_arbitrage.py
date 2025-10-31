"""测试扫描并执行套利功能"""
import sys
sys.path.append('/Users/side/Desktop/arbitrage')

from main.workflows.run_arbitrage import run_arbitrage

def test_run_arbitrage(direction="J→B"):
    """
    Test scanning and executing arbitrage
    
    Args:
        direction: Direction to execute ('B→J' or 'J→B', default: "J→B")
    """
    print(f"\n{'='*60}")
    print(f"Testing run_arbitrage")
    print(f"Direction: {direction}")
    print(f"{'='*60}\n")
    
    result = run_arbitrage(direction, skip_confirmation=True)
    
    print(f"\n{'='*60}")
    print(f"Test Complete:")
    print(f"  Overall Success: {result['success']}")
    
    if result['scan_result']:
        print(f"\n  Scan Result:")
        print(f"    Coin Found: {result['scan_result']['coin']}")
    else:
        print(f"\n  Scan Result: No opportunities found")
    
    if result['execution_result']:
        print(f"\n  Execution Result:")
        print(f"    Success: {result['execution_result']['success']}")
        if not result['execution_result']['success']:
            print(f"    Error: {result['execution_result']['error']}")
    
    print(f"{'='*60}\n")
    
    return result

if __name__ == "__main__":
    test_run_arbitrage("J→B")

