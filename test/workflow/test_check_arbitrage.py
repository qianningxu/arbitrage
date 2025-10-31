"""测试套利机会检查功能"""
import sys
sys.path.append('/Users/side/Desktop/arbitrage')

from main.workflows.check_arbitrage import check_arbitrage, scan_all_opportunities

def test_check_arbitrage(base_coin="SOL", usdt_balance=100, direction="J→B"):
    result = check_arbitrage(base_coin, usdt_balance, direction)
    
    if not result:
        print(f"{base_coin}[{direction}]: error fetching data")
        return result
    
    print(f"{base_coin}[{direction}]: usdt=${result['usdt_balance']:.2f} B=${result['bybit_price']:.4f} J=${result['jupiter_price']:.4f}", end="")
    
    if result['profitable']:
        print(f" → {result['direction']} profit=${result['profit']:.2f}")
    else:
        print(" → no opportunity")
    
    return result

def test_scan_all_opportunities(usdt_balance=100, direction="J→B"):
    print(f"\nScanning [{direction}]...")
    opportunity = scan_all_opportunities(usdt_balance, direction)
    
    if opportunity:
        print(f"Found: {opportunity['coin']} {opportunity['direction']} profit=${opportunity['profit']:.2f} ({opportunity['profit']/usdt_balance:.2%})")
    else:
        print(f"No opportunities found")
    
    return opportunity

if __name__ == "__main__":
    # test_check_arbitrage("SOL", 100, "B→J")
    # test_check_arbitrage("SOL", 100, "J→B")
    test_scan_all_opportunities(100, "J→B")

